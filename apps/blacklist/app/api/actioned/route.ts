import {getDb,articles,articleActions,actor,eq,sql,json,sameOrigin} from '../../lib/server';
import {z} from 'zod';

const input = z.object({articleId:z.string().min(1).max(200),actioned:z.boolean(),expectedVersion:z.number().int().nonnegative()}).strict();
export async function POST(req:Request) {
  if(!sameOrigin(req))return json({error:'Origin rejected'},403);
  const user=await actor();
  if(!user)return json({error:'Sign in to mark shared intelligence.'},401);
  let body;
  try{body=input.parse(await req.json());}catch{return json({error:'Invalid actioned update'},400);}
  try {
    const db=getDb();
    const [report]=await db.select({id:articles.id}).from(articles).where(eq(articles.id,body.articleId));
    if(!report)return json({error:'Briefing not found'},404);
    const [current]=await db.select().from(articleActions).where(eq(articleActions.articleId,body.articleId));
    if((current?.version||0)!==body.expectedVersion)return json({error:'This report changed in another session. The latest state has been reloaded.'},409);
    // Repeated marks must never restart the original seven-day clock.
    if(Boolean(current?.actionedAt)===body.actioned)return json({ok:true,action:current||null,serverTime:new Date().toISOString()});
    const now=new Date().toISOString();
    const values={actionedAt:body.actioned?now:null,actionedBy:body.actioned?user.displayName:'',updatedAt:now};
    const rows=current
      ?await db.update(articleActions).set({...values,version:sql`${articleActions.version}+1`}).where(sql`${articleActions.articleId}=${body.articleId} and ${articleActions.version}=${body.expectedVersion}`).returning()
      :await db.insert(articleActions).values({articleId:body.articleId,...values}).onConflictDoNothing().returning();
    if(!rows.length)return json({error:'This report changed in another session. The latest state has been reloaded.'},409);
    return json({ok:true,action:rows[0],serverTime:now});
  }catch(e){console.error('actioned',e);return json({error:'The actioned state could not be saved. Please retry.'},500);}
}
