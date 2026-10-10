import {realpathSync} from 'node:fs';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire(realpathSync(new URL('../node_modules/drizzle-kit/package.json',import.meta.url)));
const {build}=require('esbuild');
await build({entryPoints:['tests/actioned.test.ts'],bundle:true,platform:'node',format:'esm',outfile:'.sites-runtime/actioned-test.mjs',plugins:[{name:'local-test-server',setup(b){b.onResolve({filter:/^\.\.\/\.\.\/lib\/server$/},()=>({path:fileURLToPath(new URL('./actioned-server.ts',import.meta.url))}));}}]});
await import('../.sites-runtime/actioned-test.mjs');
