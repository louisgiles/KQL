import {runRefresh,json,sameOrigin} from '../../lib/server';
export const dynamic='force-dynamic';
// Private Site dispatch authorises visitors and service callers. Never publish this app publicly.
export async function POST(req:Request){if(!sameOrigin(req))return json({error:'Origin rejected'},403);try{return json(await runRefresh());}catch(e){console.error('refresh',e);return json({error:'Refresh failed; existing intelligence is retained.'},500);}}
