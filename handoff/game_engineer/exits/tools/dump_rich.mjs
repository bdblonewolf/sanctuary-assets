// full dump (spawns, critters, lights, nests, ...) of the generated chart zones from the live bundle copy (routes.mjs)
const noop=()=>{}; const el=()=>({getContext:()=>null,style:{},addEventListener:noop,appendChild:noop,setAttribute:noop});
globalThis.window=globalThis; globalThis.document={createElement:el,getElementById:()=>el(),querySelector:()=>null,addEventListener:noop,body:el(),documentElement:el(),head:el()};
globalThis.localStorage={getItem:()=>null,setItem:noop,removeItem:noop}; globalThis.requestAnimationFrame=noop;
try{ globalThis.navigator ??= {userAgent:'node'} }catch{}
globalThis.location={hostname:'x',pathname:'/',search:'',href:'http://x/'};
await import('./routes.mjs');
const a=globalThis.__X.ll(); const fs=await import('fs'); const out={worlds:{}};
for(const [id,wd] of a.worlds){ const o={}; for(const k in wd){ const v=wd[k]; if(typeof v==='function') continue; o[k]=ArrayBuffer.isView(v)?Array.from(v):v; } out.worlds[id]=o; }
fs.writeFileSync('world_rich.json',JSON.stringify(out)); console.log(Object.keys(out.worlds).length);
