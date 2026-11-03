const {applyExitsPatch}=require('./out/apply_exits_patch.js');const fs=require('fs');
const W=JSON.parse(fs.readFileSync('world_full.json')).worlds;
for(const z of ['coast','wild','desert','mires','briarE','lut','sink']){
  const w=JSON.parse(JSON.stringify(W[z]));const p=JSON.parse(fs.readFileSync(`out/${z}_exits_patch.json`));
  applyExitsPatch(w,p); applyExitsPatch(w,p);
  let msg=z;
  if(fs.existsSync(`after_${z}.json`)){const A=JSON.parse(fs.readFileSync(`after_${z}.json`));
    const key=q=>q.kind+':'+q.x.toFixed(2)+','+q.y.toFixed(2);const s=a=>a.map(key).sort().join('|');
    msg+=` tiles=${JSON.stringify(w.tiles)===JSON.stringify(A.tiles)} solid=${JSON.stringify(w.solid.map(Number))===JSON.stringify(A.solid.map(Number))} exits=${JSON.stringify(w.exits)===JSON.stringify(A.exits)} props=${s(w.props)===s(A.props)} n=${w.props.length}/${A.props.length}`;
    fs.writeFileSync(`v2in/after_${z}_js.json`,JSON.stringify(w));}
  else msg+=' '+JSON.stringify(w.exits);
  console.log(msg);}
