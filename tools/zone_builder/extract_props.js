#!/usr/bin/env node
// Zone Builder: extract game-code props (bonfires, bodies, chests, trees...) per zone from the live Sanctuary bundle.
// Usage:  node extract_props.js            (fetches the current live routes bundle)
//         node extract_props.js r7.js      (use a local copy of the routes-*.js bundle)
// Writes game_props.json next to this script. Read-only: never touches the site or any layout data.
//
// How: the bundle's world builders are run in node (browser globals stubbed) by calling the
// world dispatcher (function with `switch(e){case\`town\`:...case\`wild\``), so the result is
// what the game builds, after its own patches (exits patches, mirror, points_move, ashen fixups).
// Seeded generators (nl(seed)) are deterministic, so their props are included and marked gen:1
// when they're not a literal push in the builder source. Math.random() props differ every load:
// we build each zone twice with different Math.random seeds and drop props that move (counted in notes).
const fs=require('fs'),path=require('path'),os=require('os');
const SITE='https://gold-iris-zippy-bird.grok.me/';
const RAW='https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/';
(async()=>{
 let src,bundleName;
 if(process.argv[2]){src=fs.readFileSync(process.argv[2],'utf8');bundleName=path.basename(process.argv[2])}
 else{const h=await (await fetch(SITE)).text();bundleName=(/\/assets\/(routes-[\w-]+\.js)/.exec(h)||[])[1];if(!bundleName)throw new Error('routes bundle not found in site HTML');src=await (await fetch(SITE+'assets/'+bundleName)).text()}
 const need=(re,what)=>{const m=re.exec(src);if(!m)throw new Error('pattern not found: '+what+' (bundle changed shape)');return m};
 // Current live shape: function xp(e){switch(e){case`town`:return Af()||af(...)
 let d=need(/function (\w+)\(e\)\{switch\(e\)\{case`town`:return (\w+)\(\)/,'world dispatcher');
 let RF=d[1], RD=d[2];
 const puM=/(\w+)=\{[\s\S]{0,80}placements:\w+\.placements/.exec(src);
 if(!puM)throw new Error('pattern not found: town world store (bundle changed shape)');
 const PU=puM[1];
 const disp=src.slice(d.index,src.indexOf('default:return',d.index)+120);
 const idnM=/default:return (\w+)\[e\]\?\w+\(e\)/.exec(disp);
 if(!idnM)throw new Error('pattern not found: data dungeon table (bundle changed shape)');
 const IDN=idnM[1];
 const ids=[...new Set([...disp.matchAll(/case`(\w+)`/g)].map(m=>m[1]))];
 // literal pushes in source, to tell hand-placed props from generated ones
 const lit=new Set();for(const m of src.matchAll(/\{kind:`(\w+)`,x:(-?[\d.]+),y:(-?[\d.]+)/g))lit.add(m[1]+'|'+(+m[2])+'|'+(+m[3]));
 const fixKey=new Set();for(const m of src.matchAll(/to:\{x:(-?[\d.]+),y:(-?[\d.]+)\}/g))fixKey.add((+m[1])+'|'+(+m[2]));
 // build an importable module
 const im=/^import\{([^}]*)\}from"[^"]*";/.exec(src);let s=src;let pre='const __P=()=>{const f=function(){return __P()};return new Proxy(f,{get:(t,k)=>k===Symbol.toPrimitive?()=>"":k==="then"?undefined:__P(),apply:()=>__P(),construct:()=>__P()})};';
 if(im){s=s.slice(im[0].length);pre+=im[1].split(',').map(x=>'const '+(x.split(' as ')[1]||x).trim()+'=__P();').join('')}
 s=pre+s.replace(/export\{[^}]*\};?\s*$/,'')+`;globalThis.__Z={rf:${RF},rd:${RD},ids:Object.keys(${IDN}),setPu:v=>{${PU}=v}};`;
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'zbx-'));fs.writeFileSync(path.join(tmp,'m.mjs'),s);
 const P=()=>{const f=function(){return P()};return new Proxy(f,{get:(t,k)=>k===Symbol.toPrimitive?()=>"":k==="then"?undefined:P(),apply:()=>P(),construct:()=>P()})};
 for(const k of['window','document','localStorage','sessionStorage','requestAnimationFrame','Image','HTMLCanvasElement','AudioContext','self','location','addEventListener','matchMedia'])if(!(k in globalThis))globalThis[k]=P();
 const log=console.log;console.log=()=>{};console.warn=()=>{};
 await import(path.join(tmp,'m.mjs'));const Z=globalThis.__Z;
 try{const cb='?cb='+Date.now(),W=await (await fetch(RAW+'models/town/martsirt_v2_2/martsirt_world.json'+cb)).json(),PL=await (await fetch(RAW+'models/town/martsirt_v2_2/placements.json'+cb)).json();W.placements=PL.placements;Z.setPu(W)}catch(e){log('warn: Martsirt world/placements fetch failed, town falls back',e.message)}
 const all=[...new Set([...ids,...Z.ids])];
 const mkRand=seed=>()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
 const R=Math.random;
 // tag every prop at creation: fixed (literal coords at the call site, or literal args one/two calls up) vs gen (loop/helper/seeded fill)
 const MOD=s,TAG=new WeakMap(),push0=Array.prototype.push,fmtN=v=>{const t=String(+v);return [t,t.replace(/^0\./,'.').replace(/^-0\./,'-.')]};
 const lineStarts=[0];for(let i=0;i<MOD.length;i++)if(MOD.charCodeAt(i)===10)lineStarts.push(i+1);
 function siteText(fr){const m=/m\.mjs:(\d+):(\d+)/.exec(fr);if(!m)return '';const o=lineStarts[m[1]-1]+(+m[2])-1;return MOD.slice(o,o+260)}
 function tagPush(){for(let i=0;i<arguments.length;i++){const p=arguments[i];if(p&&typeof p==='object'&&typeof p.kind==='string'&&typeof p.x==='number'&&!TAG.has(p)){
   const fr=new Error().stack.split('\n').slice(2,5);const xs=fmtN(p.x),ys=fmtN(p.y);let fixed=false;
   for(const f of fr){const t=siteText(f);if(!t)continue;const cut=t.slice(0,t.search(/\)[,;})]/)+1||200);if(xs.some(x=>new RegExp('[:(,]'+x.replace('.','\\.')+'[,)}]').test(cut))&&ys.some(y=>new RegExp('[:(,]'+y.replace('.','\\.')+'[,)}]').test(cut))){fixed=true;break}}
   TAG.set(p,fixed?'f':'g')}}return push0.apply(this,arguments)}
 Error.stackTraceLimit=8;
 function build(id,seed){Math.random=mkRand(seed);Array.prototype.push=tagPush;try{return id==='town'?(Z.rd()||Z.rf(id)):Z.rf(id)}finally{Math.random=R;Array.prototype.push=push0}}
 const r4=v=>Math.round(v*1000)/1000;
 const keepP=p=>{const o={};for(const k in p){const v=p[k];if(typeof v==='number')o[k]=r4(v);else if(typeof v==='string'||typeof v==='boolean')o[k]=v}return o};
 const out={_meta:{bundle:bundleName,extracted:new Date().toISOString(),note:'Props live in game code (read-only). x,y are map tiles = same frame as layout pos[0],pos[2] (town: placements pos + origin). gen:1 = placed by a seeded generator, not a literal in source. solid = walk-blocked tile runs [y,x0,len] from the live builder.'},zones:{}};
 for(const id of all){let a,b;try{a=build(id,12345);b=build(id,98765)}catch(e){out.zones[id]={error:String(e&&e.message||e).slice(0,120),props:[]};continue}
  if(!a||a.id!==id&&!(id==='town'))out.zones[id]={note:'falls back to another world',props:[]};
  const key=p=>p.kind+'|'+r4(p.x)+'|'+r4(p.y);const bk=new Set((b.props||[]).map(key));
  let rnd=0;const props=[];for(const p of a.props||[]){if(typeof p.x!=='number')continue;if(!bk.has(key(p))){rnd++;continue}const q=keepP(p);if(TAG.get(p)!=='f'&&!lit.has(p.kind+'|'+r4(p.x)+'|'+r4(p.y))&&!fixKey.has(r4(p.x)+'|'+r4(p.y)))q.gen=1;props.push(q)}
  const lights=(a.lights||[]).filter(l=>typeof l.x==='number').map(l=>({x:r4(l.x),y:r4(l.y),r:l.r,warm:l.warm?1:0}));
  const notes=[];const g=props.filter(p=>p.gen).length;if(g)notes.push(g+' props are placed by loops/fills/seeded generators, not literal coordinates (shown as the game builds them; change them via prompt)');if(rnd)notes.push(rnd+' props are randomized every load (Math.random) and not shown');
  const water=[];if(a.tiles&&a.w){for(let y=0;y<a.h;y++){let x=0;while(x<a.w){const T=i=>{const t=a.tiles[i];return t===8||t===9?t:(a.water&&a.water.length===a.w*a.h&&a.water[i]?8:0)};const t=T(y*a.w+x);if(t){const x0=x,br=t===9;while(x<a.w&&T(y*a.w+x)===t)x++;water.push(br?[y,x0,x-x0,1]:[y,x0,x-x0])}else x++}}}
  const solid=[];if(a.solid&&a.w){for(let y=0;y<a.h;y++){let x=0;while(x<a.w){if(a.solid[y*a.w+x]){const x0=x;while(x<a.w&&a.solid[y*a.w+x])x++;solid.push([y,x0,x-x0])}else x++}}}
  out.zones[id]={name:a.name||id,w:a.w,h:a.h,props,lights,notes,water,solid};}
 fs.writeFileSync(path.join(__dirname,'game_props.json'),JSON.stringify(out));
 console.log=log;const summ={};for(const [id,z] of Object.entries(out.zones)){const c={};z.props.forEach(p=>c[p.kind]=(c[p.kind]||0)+1);summ[id]={n:z.props.length,w:z.w,h:z.h,c,notes:z.notes,err:z.error}}
 log(JSON.stringify(summ,null,0).replace(/\},"/g,'},\n"'));log('bytes',fs.statSync(path.join(__dirname,'game_props.json')).size,'bundle',bundleName);
 process.exit(0);
})().catch(e=>{console.error('extract failed:',e.message);process.exit(1)});
