import type { Article } from './types';
import { inferCategory } from './packs';
export const feedConfig=[
 {id:'microsoft',name:'Microsoft Security',url:'https://www.microsoft.com/en-us/security/blog/feed/',primary:true},
 {id:'talos',name:'Cisco Talos',url:'https://blog.talosintelligence.com/rss/',primary:true},
 {id:'unit42',name:'Unit 42',url:'https://unit42.paloaltonetworks.com/feed/',primary:true},
 {id:'bleeping',name:'BleepingComputer',url:'https://www.bleepingcomputer.com/feed/',primary:false},
 {id:'cisa',name:'CISA Known Exploited Vulnerabilities',url:'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',primary:true}
];
export function clean(s:string){return s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,'$1').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&#x([a-f0-9]+);/gi,(_,n)=>String.fromCodePoint(Math.min(parseInt(n,16),1114111))).replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(Math.min(Number(n),1114111))).replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&apos;|&#039;/g,"'").replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim();}
export function safeURL(s:string){try{const u=new URL(clean(s));if(u.protocol!=='https:')return '';for(const k of [...u.searchParams.keys()])if(k.startsWith('utm_'))u.searchParams.delete(k);u.hash='';return u.toString();}catch{return '';}}
export async function articleId(url:string){const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(url));return 'intel-'+[...new Uint8Array(hash)].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,24);}
function tag(xml:string,key:string){return xml.match(new RegExp('<'+key+'(?:\\s[^>]*)?>([\\s\\S]*?)</'+key+'>','i'))?.[1]||'';}
export async function parseRSS(xml:string,feed:typeof feedConfig[number],now=new Date()):Promise<Article[]>{
 const items=[...xml.matchAll(/<item(?:\s[^>]*)?>([\s\S]*?)<\/item>/gi)].slice(0,40);const out:Article[]=[];
 for(const [,raw] of items){
  const title=clean(tag(raw,'title'));const url=safeURL(tag(raw,'link'));const desc=clean(tag(raw,'description'));const date=new Date(clean(tag(raw,'pubDate'))||clean(tag(raw,'dc:date')));
  if(!title||!url||!Number.isFinite(+date)||+date>+now+300000||+date<+now-90*86400000)continue;
  const combined=title+' '+desc; const mapped=inferCategory(combined);
  if(mapped.category==='Threat landscape' && !/exploit|vulnerab|attack|threat|breach/i.test(title))continue;
  if(/sponsored|webinar|register now|announcing|perspectives|lessons from|what.s new|guide to.*ignite/i.test(title))continue;
  const active=/active(?:ly)? exploit|in.the.wild|zero.day|mass exploit/i.test(combined);
  const score=Math.min(95,45+(feed.primary?12:0)+(active?23:0)+(mapped.packs.length?8:0)+(+now-+date<7*86400000?7:0));
  const excerpt=desc.split(/\s+/).slice(0,24).join(' ');
  out.push({id:await articleId(url),title,url,publisher:feed.name,publishedAt:date.toISOString(),discoveredAt:now.toISOString(),category:mapped.category,priority:score>=80?'High':score>=60?'Medium':'Context',score,summary:excerpt?excerpt+'…':'Open the source for the full report. No usable publisher excerpt was provided.',reason:(feed.primary?'Primary publisher. ':'Secondary reporting; corroborate with primary research. ')+(active?'The headline or excerpt references active exploitation. ':'')+(mapped.packs.length?'Mapped to candidate behavioural hunts; relevance needs analyst review.':'Requires a tailored telemetry assessment.'),facts:[],sources:[{title,url,publisher:feed.name,type:feed.primary?'Primary research':'Reporting'}],packs:mapped.packs,tags:[...new Set(combined.match(/CVE-\d{4}-\d{4,7}/gi)||[])].slice(0,6),kind:'feed',caveat:'Publisher excerpt, not a researched synthesis. Category, rank and hunt suggestions use text matching and can be wrong. Read the full source before treating any behaviour as campaign-specific.'});
 }return out;
}
export async function fetchText(url:string){
 const r=await fetch(url,{headers:{'Accept':'application/rss+xml, application/json, text/xml, */*','User-Agent':'Huntdesk/1.0 threat research reader'},signal:AbortSignal.timeout(18000)});
 if(!r.ok)throw new Error('Publisher returned HTTP '+r.status);
 const reader=r.body?.getReader();if(!reader)throw new Error('Empty publisher response');let size=0;const chunks:Uint8Array[]=[];
 while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>4000000){await reader.cancel();throw new Error('Feed exceeds size limit');}chunks.push(value);}
 const all=new Uint8Array(size);let off=0;for(const c of chunks){all.set(c,off);off+=c.length;}return new TextDecoder().decode(all);
}
export async function fetchFeed(feed:typeof feedConfig[number]):Promise<Article[]>{
 if(feed.id!=='cisa'){const xml=await fetchText(feed.url);if(!/<rss|<feed/i.test(xml))throw new Error('Publisher did not return a feed');return parseRSS(xml,feed);}
 let raw:string;try{raw=await fetchText(feed.url);}catch{raw=await fetchText('https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json');}
 const json=JSON.parse(raw);if(!Array.isArray(json.vulnerabilities))throw new Error('Unexpected KEV format');const now=new Date();const list=json.vulnerabilities.filter((x:any)=>new Date(x.dateAdded).getTime()>+now-30*86400000&&new Date(x.dateAdded).getTime()<=+now).slice(-45);
 return Promise.all(list.map(async(x:any)=>{const url='https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve='+encodeURIComponent(x.cveID);return {id:await articleId(url),title:x.cveID+': '+x.vulnerabilityName,url,publisher:feed.name,publishedAt:new Date(x.dateAdded).toISOString(),discoveredAt:now.toISOString(),category:'Exploitation',priority:'High' as const,score:74,summary:`CISA added ${x.cveID} affecting ${x.vendorProject} ${x.product} to its known exploited vulnerabilities catalogue. Check asset exposure, the vendor advisory and available forensic evidence. The date shown is the catalogue addition date, not when exploitation began.`,reason:'Inclusion in CISA KEV establishes known exploitation; local product exposure determines your hunt priority.',facts:[{text:'CISA lists this vulnerability as known to have been exploited.',source:0}],sources:[{title:'CISA KEV entry: '+x.cveID,url,publisher:'CISA',type:'Primary research' as const}],packs:[],tags:[x.cveID,x.vendorProject],kind:'catalogue' as const,caveat:'Vulnerability triage is not proof of compromise. Select a suitable hunt from the query library after identifying the product and telemetry; a generic network query is not a CVE-specific detector.'};}));
}
