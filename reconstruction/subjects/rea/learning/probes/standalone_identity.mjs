// OXYCOK-authored positive host comparison; not a readiness assertion.
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
import {readFile} from 'node:fs/promises';
const root=process.env.REA_REFERENCE_ROOT;if(!root)throw Error('REA_REFERENCE_ROOT_REQUIRED');
const {createSystemProcessOwnershipHost}=await import(pathToFileURL(resolve(root,'src/process/ProcessOwnershipObservation.ts')).href);
const host=createSystemProcessOwnershipHost('linux',{});
const entry={pid:process.pid,parentPid:process.ppid,processGroupId:process.pid,state:'S',command:process.execPath};
let proc;
try{const text=await readFile(`/proc/${process.pid}/stat`,'utf8');proc={readable:true,fields:text.trim().split(/\s+/).length};}
catch(e){proc={readable:false,code:e.code};}
console.log(JSON.stringify({version:1,authority:'NONE',probe:'STANDALONE_IDENTITY_CONTEXT',identity:[...await host.processIdentities([entry])],proc},null,2));
