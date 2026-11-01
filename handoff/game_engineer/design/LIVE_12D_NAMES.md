# Stage 12D / A3 / A4 live build — minified names
Bundles: assets/index-Bb23fn_Q.js (i.js), assets/routes-BRGAGLf9.js (r.js). Was 12C: see ../live_12c.
Line numbers refer to prettier-formatted r.js.

## Edge / shore (12B–12D)
- Edge class: `XT` (line 72763; search `edge12b`). Per-room instance: `e.room.edge`.
  - fields: `kitLay` {files: Map<file,[{x,z,ry,sx,sy,sz}]>, cover: Set<y*w+x>, ends: [{x,z}]}
  - methods: `layoutKit(world, seaSet, season)` ~73543, `placeKit(world, season, ...)` ~74031, `placeShore(e,t,n,r,i,a,cover)` ~74074, `sync(world|null, season)`.
- Sea-flag fn: `HT(id, tiles, w, h)` (was VT)
- groundSet fn: `VT(id, season)` (was BT)
- Sea-quadrant table: `zT[id]` (E/N/W/S list); `RT = [E,N,W,S]`; shore-rock table passed to placeShore: `ZT(id)` (was XT), call at line 73472
- Water tile id: `LT = 4` (was IT)
- Hash: `GT(x,y)` (was WT); off-map quadrant: `KT(x,y,w,h)` (was GT)
- GLB loader: `Yw(url)` (was Jw; resolves null + "[3d] asset failed" warn); asset base `FT`; url helpers `UT`, `WT`
- Season fn: `bE(id)` (was yE); outdoor test: `xE(world)` (was bE) = !martsirt && !vE && !_E && !gE
- Call site: `edge.sync(xE(e) ? e : null, bE(e.id))` ~76411

## Audio (A3 / A4)
- Level table `q` (was sl); path builder `sl(e)` (was cl); site loader `cl(e,t)` (was ll); full-URL loader `ll(e,t)`; ramp `ul`
- Music manager class: `dl`, constructor (ctx, town, stone, dread, sfx, theme, ow); built as `new dl(t,i,a,u,o,d,f)`
- Audio class fields: mood / place / outdoor; methods setPlace / setOutdoor / setMood / pump / unlock
- unlock() buses: master `n`, music `r` (.82), town `i`, wild/stone `a`, sfx `o`, rain `s`, wind `c`, compressor `l`, dread `u`, Martsirt theme bus `d`, overworld bus `f`
- Per-frame call site ~81854: setPlace(n), setOutdoor(xE(this.world)), setMood(...)
