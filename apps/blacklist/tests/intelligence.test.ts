import assert from 'node:assert/strict';
import {parseRSS,clean,safeURL} from '../app/lib/feeds';
import {packs,inferCategory} from '../app/lib/packs';
import {seeds} from '../app/lib/seeds';
const now=new Date('2026-10-08T18:00:00Z');
const feed={id:'test',name:'Test publisher',url:'https://example.org/feed',primary:true};
const xml=`<rss><channel><item><title><![CDATA[Active exploitation of CVE-2026-12345]]></title><link>https://example.org/report?utm_source=feed</link><pubDate>Thu, 08 Oct 2026 10:00:00 GMT</pubDate><description><![CDATA[<p>Researchers report active exploitation against exposed appliances.</p>]]></description></item><item><title>Malware future report</title><link>https://example.org/future</link><pubDate>Fri, 09 Oct 2026 10:00:00 GMT</pubDate></item><item><title>Malware unsafe link</title><link>javascript:alert(1)</link><pubDate>Thu, 08 Oct 2026 10:00:00 GMT</pubDate></item></channel></rss>`;
const result=await parseRSS(xml,feed,now);
assert.equal(result.length,1,'Reject future-dated items and unsafe URLs');
assert.equal(result[0].url,'https://example.org/report');
assert.equal(result[0].priority,'High');
assert.equal(result[0].kind,'feed','Fresh feeds must not claim researched analysis');
assert.equal(result[0].facts.length,0);
assert.equal(safeURL('http://example.org'),'');
assert.equal(clean('<script>untrusted()</script><p>Safe &amp; plain</p>'),'Safe & plain');
assert.deepEqual(inferCategory('Google phishing campaign').packs,[],'Do not map Google authentication to Entra queries');
for(const a of seeds){assert.ok(a.facts.every(f=>a.sources[f.source]));assert.ok(a.packs.every(id=>packs[id]));}
for(const p of Object.values(packs)){assert.ok(!/DeviceProcessEvents|DeviceNetworkEvents|Timestamp/.test(p.query));assert.ok(p.query.includes('TimeGenerated'));assert.ok(p.prerequisites&&p.falsePositives.length&&p.limitations);}
console.log('PASS: feed parsing, future dates, URL safety, evidence labels, citations, platform scope and 9 hunt pack contracts.');
