// OXYCOK-authored probe: invoke actual pinned REA modules, never copy their bodies.
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const root = process.env.REA_REFERENCE_ROOT;
if (!root) throw Error('REA_REFERENCE_ROOT_REQUIRED');
const load = p => import(pathToFileURL(resolve(root,p)).href);
const {createEvidenceCompletionLedger,parseEvidenceCompletionLedger}=await load('src/domain/evidenceCompletionLedger.ts');
const {AnalysisInputError}=await load('src/domain/analysisErrorCore.ts');
const {ProviderCleanupError}=await load('src/domain/providerCleanupError.ts');
const {analysisErrorWithCleanupFailure}=await load('src/domain/analysisErrorCleanup.ts');
const {projectAnalysisError}=await load('src/domain/analysisErrorProjection.ts');
const {EvidenceLedger}=await load('src/application/investigation/EvidenceLedger.ts');
const {createEvidence}=await load('src/domain/evidence.ts');
const {proofAuthoritySatisfies}=await load('src/application/ReconstructionObligationAuthority.ts');
const results=[];
const check=(id,run)=>{try{run();results.push({id,outcome:'PASS'});}catch(e){results.push({id,outcome:'FAIL',error:String(e)});}};
const claim=(id,status)=>({claim_id:id,status,evidence_ids:['ev_'+'1'.repeat(64)]});
check('nonpass_statuses_keep_completion_open',()=>{
 for(const status of ['unknown','unsupported','truncated','fail'])
  assert.equal(createEvidenceCompletionLedger([claim('one','pass'),claim('two',status)]).summary.complete,false);
});
check('tampered_derived_summary_is_rejected',()=>{
 const ledger=createEvidenceCompletionLedger([claim('one','unknown')]);
 assert.throws(()=>parseEvidenceCompletionLedger({...ledger,summary:{...ledger.summary,complete:true}}));
 assert.equal(parseEvidenceCompletionLedger(ledger).summary.complete,false);
});
check('cleanup_completion_preserves_primary_failure_and_history',()=>{
 const primary=new AnalysisInputError('inspect');const cleanup=new ProviderCleanupError('fixture',['owned-resource'],{});
 const composed=analysisErrorWithCleanupFailure(primary,cleanup).bindCleanupDependencies([primary,cleanup]);
 assert.equal(projectAnalysisError(composed).code,'cleanup_incomplete');cleanup.resolveCleanup();
 const after=projectAnalysisError(composed);assert.equal(after.code,'invalid_request');assert.ok(after.details.cleanup_history);
});
check('unbound_cleanup_cannot_self_certify_release',()=>{
 const cleanup=new ProviderCleanupError('fixture',['resource'],{});
 const composed=analysisErrorWithCleanupFailure(new AnalysisInputError('inspect'),cleanup);cleanup.resolveCleanup();
 assert.equal(projectAnalysisError(composed).code,'cleanup_incomplete');
});
check('evidence_conflict_rejection_preserves_prior_state',()=>{
 const store=new EvidenceLedger();const e=createEvidence(undefined,{id:'fixture',name:'Fixture',version:null},{operation:'inspect',parameters:{},result:{a:1}});
 assert.equal(store.record(e).ok,true);const before=JSON.stringify(store.export());
 const changed=structuredClone(e);changed.normalized_result={a:2};assert.equal(store.record(changed).ok,false);
 assert.equal(JSON.stringify(store.export()),before);
});
check('unit_authority_does_not_cover_native_boundary',()=>{
 assert.equal(proofAuthoritySatisfies('unit','native-abi'),false);
 assert.equal(proofAuthoritySatisfies('native-abi','native-abi'),true);
});
console.log(JSON.stringify({version:1,probe:'OXYCOK_AUTHORED_REAL_REA_MECHANISMS',authority:'NONE',results,independent_qualification:'NOT_ESTABLISHED'},null,2));
if(results.some(r=>r.outcome==='FAIL'))process.exitCode=1;
