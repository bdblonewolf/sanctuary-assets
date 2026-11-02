// node validate.js file.glb ...  -> per-file errors/warnings/infos + spec checks
const v=require('/tmp/gv/node_modules/gltf-validator'),fs=require('fs');
(async()=>{let bad=0;for(const f of process.argv.slice(2)){const b=new Uint8Array(fs.readFileSync(f));
 const r=await v.validateBytes(b,{maxIssues:200});const I=r.issues;
 const j=JSON.parse(Buffer.from(b.slice(20,20+new DataView(b.buffer).getUint32(12,true))).toString());
 const spec=[];if(b.length>4e6)spec.push('size>4MB');if(j.extensionsUsed)spec.push('ext:'+j.extensionsUsed);if(j.cameras)spec.push('cameras');
 for(const m of j.materials||[]){const e=m.emissiveFactor||[0,0,0];if(Math.max(...e)>1)spec.push('emissive>1')}
 if(I.numErrors)bad++;
 console.log(`${f.split('/').pop()}\t${b.length} B\terr ${I.numErrors} warn ${I.numWarnings} info ${I.numInfos} hints ${I.numHints}\ttris ${r.info.totalTriangleCount}\tspec ${spec.length?spec.join(','):'OK'}`);
 for(const m of I.messages.filter(m=>m.severity<=1).slice(0,8))console.log('   ',m.severity?'W':'E',m.code,m.pointer,m.message)}
 process.exit(bad?1:0)})();
