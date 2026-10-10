import { getDb } from '../../db';
import { articles, articleActions, hunts, notes, members, settings, feedStates } from '../../db/schema';
import { eq, desc, sql } from 'drizzle-orm';
import { getChatGPTUser } from '../chatgpt-auth';
import { seeds } from './seeds';
import { fetchFeed,feedConfig } from './feeds';
import type { Article } from './types';
export { getDb, articles, articleActions, hunts, notes, members, settings, feedStates, eq, desc, sql };
export function json(data:unknown,status=200){return Response.json(data,{status,headers:{'Cache-Control':'no-store'}});}
export function sameOrigin(req:Request){const origin=req.headers.get('origin');return !origin||origin===new URL(req.url).origin;}
export async function actor(){return getChatGPTUser();}
export async function seed(){const db=getDb();for(const a of seeds)await db.insert(articles).values({id:a.id,url:a.url,payload:JSON.stringify(a),publishedAt:a.publishedAt,kind:a.kind}).onConflictDoNothing();}
export async function getSettings(){const rows=await getDb().select().from(settings);return Object.fromEntries(rows.filter(x=>x.key!=='refreshLock').map(x=>[x.key,x.value]));}
export async function setSetting(key:string,value:string){await getDb().insert(settings).values({key,value}).onConflictDoUpdate({target:settings.key,set:{value}});}
export async function runRefresh(){
 const db=getDb(),now=Date.now();
 const lock=await db.insert(settings).values({key:'refreshLock',value:String(now)}).onConflictDoUpdate({target:settings.key,set:{value:String(now)},setWhere:sql`cast(${settings.value} as integer) < ${now-60000}`}).returning();
 if(!lock.length)return {busy:true,message:'An intelligence refresh is already running.'};
 try{
  await seed();const results=await Promise.all(feedConfig.map(async feed=>{
   const checkedAt=new Date().toISOString();try{
    const fetched=await fetchFeed(feed);let added=0;
    for(const a of fetched){const inserted=await db.insert(articles).values({id:a.id,url:a.url,payload:JSON.stringify(a),publishedAt:a.publishedAt,kind:a.kind}).onConflictDoNothing().returning({id:articles.id});added+=inserted.length;if(!inserted.length&&a.kind==='catalogue')await db.update(articles).set({payload:JSON.stringify(a),kind:a.kind}).where(sql`${articles.url}=${a.url} and (${articles.kind} != 'research' or json_extract(${articles.payload}, '$.summary') like 'CISA added %')`);}
    const state={id:feed.id,name:feed.name,url:feed.url,checkedAt,status:'ok',count:fetched.length,error:''};await db.insert(feedStates).values(state).onConflictDoUpdate({target:feedStates.id,set:state});return {name:feed.name,ok:true,added,count:fetched.length};
   }catch(e){const state={id:feed.id,name:feed.name,url:feed.url,checkedAt,status:'error',count:0,error:e instanceof Error?e.message:'Source unavailable'};await db.insert(feedStates).values(state).onConflictDoUpdate({target:feedStates.id,set:state});return {name:feed.name,ok:false,added:0,error:state.error};}
  }));
  await setSetting('lastAttempt',new Date().toISOString());if(results.some(x=>x.ok))await setSetting('lastRefresh',new Date().toISOString());return {busy:false,added:results.reduce((n,x)=>n+x.added,0),sources:results};
 }finally{await setSetting('refreshLock','0');}
}
