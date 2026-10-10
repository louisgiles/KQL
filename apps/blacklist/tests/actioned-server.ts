// Local integration fixture. No Site credentials or production bindings are used.
import {DatabaseSync} from 'node:sqlite';
import {drizzle} from 'drizzle-orm/d1';
import * as schema from '../db/schema';
export * from '../db/schema';
export {eq,desc,sql} from 'drizzle-orm';
export const sqlite = new DatabaseSync(':memory:');
const client={prepare(query:string){return {bind(...values:unknown[]){return {
 async all(){return {results:sqlite.prepare(query).all(...values as any[])};},
 async raw(){const stmt=sqlite.prepare(query);stmt.setReturnArrays(true);return stmt.all(...values as any[]);},
 async run(){return {success:true,meta:sqlite.prepare(query).run(...values as any[])};}
};}};}};
const db=drizzle(client as any,{schema});
export const getDb=()=>db;
export let testUser:{userId:string;displayName:string}|null=null;
export function signIn(value:typeof testUser){testUser=value;}
export async function actor(){return testUser;}
export async function seed(){}
export async function getSettings(){return {};}
export function json(data:unknown,status=200){return Response.json(data,{status,headers:{'Cache-Control':'no-store'}});}
export function sameOrigin(req:Request){const origin=req.headers.get('origin');return !origin||origin===new URL(req.url).origin;}
