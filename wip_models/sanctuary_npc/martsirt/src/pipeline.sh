set -e
n=$1; cd /workspace/sanctuary_npc/martsirt/src
python3 anim.py $n work/$n/raw.glb work/$n/anim.glb
cd work/$n && gltf-transform resample anim.glb r.glb >/dev/null && gltf-transform prune r.glb p.glb >/dev/null && gltf-transform quantize --quantization-volume scene p.glb q0.glb >/dev/null && gltf-transform prune q0.glb q.glb >/dev/null
python3 /workspace/sanctuary_npc/martsirt/src/namefix.py q.glb ../../../glb/$n.glb; ls -l ../../../glb/$n.glb
cd /tmp/gv && node -e "
const v=require('gltf-validator'),fs=require('fs');const b=new Uint8Array(fs.readFileSync('/workspace/sanctuary_npc/martsirt/glb/$n.glb'));
v.validateBytes(b).then(r=>{const i=r.issues;console.log('VALID',i.numErrors,i.numWarnings,i.numInfos,i.numHints);const c={};i.messages.forEach(m=>c[m.code]=(c[m.code]||0)+1);console.log(JSON.stringify(c));console.log('anims',r.info.animationCount,'tris',r.info.totalTriangleCount)})"
