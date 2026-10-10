import {actor,json,sameOrigin,setSetting} from '../../lib/server';
import {z} from 'zod';
import {tableNames} from '../../lib/packs';
export async function POST(req:Request){if(!sameOrigin(req))return json({error:'Origin rejected'},403);if(!await actor())return json({error:'Sign in to update telemetry settings.'},401);try{const b=z.object({telemetry:z.array(z.string().refine(s=>tableNames.includes(s))).max(10)}).parse(await req.json());await setSetting('telemetry',JSON.stringify(b.telemetry));return json({ok:true});}catch{return json({error:'Invalid settings'},400);}}
