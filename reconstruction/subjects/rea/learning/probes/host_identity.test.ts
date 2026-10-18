// OXYCOK-authored observation harness; not an upstream regression test.
import { it } from 'vitest';
import { readFile } from 'node:fs/promises';
import { createSystemProcessOwnershipHost } from './ProcessOwnershipObservation.js';
it('records host identity availability without converting unavailability to pass', async () => {
  const host = createSystemProcessOwnershipHost('linux', {});
  const entry = {pid:process.pid,parentPid:process.ppid,processGroupId:process.pid,state:'S',command:process.execPath};
  const identity = [...await host.processIdentities!([entry])];
  let proc;
  try { const value = await readFile(`/proc/${process.pid}/stat`, 'utf8'); proc = {readable:true,fields:value.trim().split(/\s+/).length}; }
  catch (cause) { proc = {readable:false,code:(cause as NodeJS.ErrnoException).code}; }
  console.log('OXYCOK_HOST_DIAGNOSTIC='+JSON.stringify({identity,proc,pid:process.pid}));
});
