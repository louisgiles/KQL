import {getDb,articles,articleActions,hunts,notes,members,feedStates,actor,seed,getSettings,desc,json,eq} from '../../lib/server';
import {isNotNull,gt,and} from 'drizzle-orm';
import {ACTIONED_RETENTION_MS} from '../../lib/actioned';
export const dynamic='force-dynamic';
export async function GET(req:Request){
 try{
  const user=await actor();await seed();const db=getDb();
  if(user)await db.insert(members).values({id:user.userId,name:user.displayName,seenAt:new Date().toISOString()}).onConflictDoUpdate({target:members.id,set:{name:user.displayName,seenAt:new Date().toISOString()}});
  const brief=new URL(req.url).searchParams.get('brief');
  const [a,h,n,m,f,s,actions,actionedArticles,linked]=await Promise.all([
   db.select().from(articles).orderBy(desc(articles.publishedAt)).limit(700),db.select().from(hunts),db.select().from(notes).orderBy(desc(notes.createdAt)).limit(500),db.select({id:members.id,name:members.name}).from(members),db.select().from(feedStates),getSettings(),db.select().from(articleActions),
   db.select({payload:articles.payload,id:articles.id}).from(articles).innerJoin(articleActions,eq(articles.id,articleActions.articleId)).where(and(isNotNull(articleActions.actionedAt),gt(articleActions.actionedAt,new Date(Date.now()-ACTIONED_RETENTION_MS).toISOString()))),
   brief?db.select().from(articles).where(eq(articles.id,brief)):Promise.resolve([])
  ]);
  const all=new Map([...a,...actionedArticles,...linked].map(x=>[x.id,JSON.parse(x.payload)]));
  return json({articles:[...all.values()],actions,hunts:h,notes:n,members:m,feeds:f,settings:s,user:user?{userId:user.userId,displayName:user.displayName}:null,serverTime:new Date().toISOString()});
 }catch(e){console.error('workspace',e);return json({error:'Workspace could not be loaded. Please retry.'},500);}
}
