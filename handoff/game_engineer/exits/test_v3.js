// exits_v3 checks: apply v2/v3 patches to the live generated worlds (world_rich.json), verify the mirror (tiles, props and every
// nested point: spawns, patrol routes, nests, critters + facing, lights, npcs), that every spawn/nest/route point/critter is on an
// open tile reachable from the player spawn, patrol legs, points_move, edges, arrivals and idempotency, and simulate the in-game chart (port of Od/wd/Td/Ed from the routes bundle) with NO override.
const fs = require('fs'), path = require('path');
const D = __dirname, P = f => fs.existsSync(path.join(D, 'out_v3', f)) ? path.join(D, 'out_v3', f) : fs.existsSync(path.join(D, 'out', f)) ? path.join(D, 'out', f) : path.join(D, f);
const { applyExitsPatch } = require(fs.existsSync(path.join(D, 'out/apply_exits_patch.js')) ? path.join(D, 'out/apply_exits_patch.js') : path.join(D, 'apply_exits_patch.js'));
// world dump: argv[2], else world_rich.json (full generated worlds incl. spawns/nests/critters/routes, from dump_rich.mjs), else world_full.json
const WF = process.argv[2] || [path.join(D, 'world_rich.json'), path.join(D, 'tools', 'world_rich.json'), path.join(D, 'world_full.json')].find(f => fs.existsSync(f));
const W0 = JSON.parse(fs.readFileSync(WF)).worlds;
const clone = o => JSON.parse(JSON.stringify(o));
const V2 = ['coast', 'wild', 'desert', 'mires', 'briarE', 'lut', 'sink'];
const V3 = ['wild', 'briarE', 'duneW', 'desert', 'lut'];
const warns = []; { const cw = console.warn; console.warn = (...a) => { warns.push(a.join(' ')); }; }
function build(set, opt = {}) {
  const W = clone(W0);
  for (const z of V2) if (set !== 'live') applyExitsPatch(W[z], JSON.parse(fs.readFileSync(P(`${z}_exits_patch.json`))));
  if (set === 'v3') for (const z of V3) { const w = clone(W0[z]), p = JSON.parse(fs.readFileSync(P(`${z}_exits_patch_v3.json`))); if (opt.noMoves) delete p.points_move; applyExitsPatch(w, p); applyExitsPatch(w, p); W[z] = w; }
  return W;
}
// ---- chart sim (same rules as the bundle: nearest edge of the forward exit; fallback to opposite of the return exit)
const bd = ['town', 'wild', 'briarE', 'duneW', 'desert', 'lut', 'market', 'waste', 'coast', 'bastion', 'bluffs', 'mires', 'sink', 'ridge', 'ascent', 'crypts', 'chasm', 'iron', 'flotsam', 'hollow', 'gaol', 'weald', 'isle'];
const wd = (w, h, x, y) => [{ dir: 'n', edge: y }, { dir: 's', edge: h - y }, { dir: 'e', edge: w - x }, { dir: 'w', edge: x }].sort((a, b) => a.edge - b.edge)[0];
const Td = d => ({ n: 's', s: 'n', e: 'w', w: 'e' })[d];
function Ed(occ, c, r, dir) {
  const v = { n: [0, -1], e: [1, 0], s: [0, 1], w: [-1, 0] }[dir], a = c + v[0], o = r + v[1], K = (x, y) => `${x},${y}`;
  if (!occ.has(K(a, o))) return { c: a, r: o, moved: false };
  let best = null;
  for (let i = 1; i <= 8; i++) { for (let l = -i; l <= i; l++) for (let u = -i; u <= i; u++) { if (Math.max(Math.abs(u), Math.abs(l)) !== i) continue; const d = a + u, f = o + l; if (occ.has(K(d, f))) continue;
    const p = dir === 'e' ? d - c : dir === 'w' ? c - d : dir === 's' ? f - r : r - f, m = Math.abs(u) + Math.abs(l) + (p <= 0 ? 6 : 0); if (!best || m < best.score) best = { c: d, r: f, score: m, moved: true }; }
    if (best) return best; }
  return { c: a, r: o, moved: false };
}
function chart(W) {
  const set = new Set(bd), pos = new Map([['town', { c: 0, r: 0 }]]), occ = new Set(['0,0']), q = ['town'], log = [];
  while (q.length) { const a = q.shift(), o = pos.get(a), s = W[a];
    for (const c of s.exits) { if (!set.has(c.to) || pos.has(c.to)) continue; const l = W[c.to], u = l.exits.find(e => e.to === a);
      const d = wd(s.w, s.h, c.x, c.y), f = u ? wd(l.w, l.h, u.x, u.y) : null, p = d.edge <= Math.min(s.w, s.h) * .34, m = !!f && f.edge <= Math.min(l.w, l.h) * .22;
      let h = d.dir; if (!p && f && m) h = Td(f.dir);
      const g = Ed(occ, o.c, o.r, h); occ.add(`${g.c},${g.r}`); pos.set(c.to, g); q.push(c.to);
      log.push({ from: a, to: c.to, dir: h, back: f && f.dir, consistent: !!f && f.dir === Td(h), bumped: g.moved }); } }
  return { pos, log };
}
let ok = true; const bad = m => { ok = false; console.log('FAIL', m); };
// ---- v3 checks
const W3 = build('v3'), W2 = build('v2');
for (const z of ['briarE', 'duneW', 'desert']) {
  const a = W2[z], b = W3[z], w = a.w, h = a.h; let tm = 0, sm = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { if (b.tiles[y * w + x] !== a.tiles[y * w + w - 1 - x]) tm++; if (!!b.solid[y * w + x] !== !!a.solid[y * w + w - 1 - x]) sm++; }
  if (tm || sm) bad(`${z} mirror tiles ${tm} solid ${sm}`);
  const pm = a.props.filter((p, i) => Math.abs(b.props[i].x - (w - p.x)) > 1e-3 || b.props[i].y !== p.y).length; if (pm) bad(`${z} props ${pm}`);
  if (Math.abs(b.spawn.x - (w - a.spawn.x)) > 1e-3) bad(z + ' spawn');
}
const edge = (w, x, y) => wd(w.w, w.h, x, y).dir;
function reach(w, sx, sy) { // 4-connected over non-solid tiles from the arrival; returns set of reachable indices
  const W_ = w.w, H = w.h, st = Math.floor(sy) * W_ + Math.floor(sx), seen = new Uint8Array(W_ * H); if (w.solid[st]) return null; const q = [st]; seen[st] = 1;
  while (q.length) { const i = q.pop(), x = i % W_, y = (i / W_) | 0; for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + dx, Y = y + dy; if (X < 0 || Y < 0 || X >= W_ || Y >= H) continue; const j = Y * W_ + X; if (!seen[j] && !w.solid[j]) { seen[j] = 1; q.push(j); } } }
  return seen;
}
const rows = [];
for (const z of ['wild', 'briarE', 'duneW', 'desert', 'lut']) for (const e of W3[z].exits) {
  if (!['wild', 'briarE', 'duneW', 'desert', 'lut'].includes(e.to)) continue;
  const tw = W3[e.to], back = tw.exits.find(q => q.to === z), R = reach(tw, e.sx, e.sy);
  const ein = edge(W3[z], e.x, e.y), bin = edge(tw, back.x, back.y), arrEdge = edge(tw, e.sx, e.sy);
  const toBack = R && (R[Math.floor(back.y) * tw.w + Math.floor(back.x)] || [[0,0],[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy]) => R[(Math.floor(back.y)+dy) * tw.w + Math.floor(back.x)+dx]));
  const others = tw.exits.filter(q => q.to !== z && !['den', 'town'].includes(q.to) && bd.includes(q.to)).map(q => ({ to: q.to, r: !!(R && [[0,0],[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy]) => R[(Math.floor(q.y)+dy) * tw.w + Math.floor(q.x)+dx])) }));
  const okRow = ein === Td(bin) && arrEdge === bin && R && toBack && others.every(o => o.r);
  rows.push(`${z} -> ${e.to}: leave ${z} by its ${ein.toUpperCase()} edge (${e.x},${e.y}); arrive ${e.to} (${e.sx},${e.sy}) on its ${arrEdge.toUpperCase()} side next to its return exit (${back.x},${back.y}, ${bin.toUpperCase()} edge); arrival walkable=${!!R} return-exit reachable=${!!toBack} onward ${JSON.stringify(others)} ${okRow ? 'OK' : 'MISMATCH'}`);
  if (!okRow) bad(`${z}->${e.to}`);
}
rows.forEach(r => console.log(r));
// idempotent
const t = clone(W0.briarE), pb = JSON.parse(fs.readFileSync(P('briarE_exits_patch_v3.json'))); applyExitsPatch(t, pb); const t1 = JSON.stringify(t); applyExitsPatch(t, pb); if (JSON.stringify(t) !== t1) bad('idempotent');
// ---- chart, no override
for (const s of ['live', 'v2', 'v3']) {
  const { pos, log } = chart(build(s)), wc = pos.get('wild');
  const rel = z => { const p = pos.get(z); return `${z}(${p.c - wc.c},${p.r - wc.r})`; };
  const west = ['wild', 'briarE', 'duneW', 'desert', 'lut', 'market', 'waste'];
  console.log(`chart[${s}] relative to wild:`, west.map(rel).join(' '), '| links:', log.filter(l => west.includes(l.from) && west.includes(l.to)).map(l => `${l.from}-${l.dir}->${l.to}${l.consistent ? '' : '(return ' + l.back + ' MISMATCH)'}${l.bumped ? '(BUMPED)' : ''}`).join(' '));
  if (s === 'v3' && log.some(l => west.includes(l.to) && (!l.consistent || l.bumped))) bad('v3 chart');
}

// ---- nested mirror: every point inside spawns / routes / nests / critters / lights / npcs (v3 without points_move vs v2)
const HAS_RICH = ['briarE', 'duneW', 'desert'].some(z => Array.isArray(W0[z].spawns));
const W3n = build('v3', { noMoves: true });
const TAU = Math.PI * 2, angEq = (a, b) => Math.abs(Math.atan2(Math.sin(a - b), Math.cos(a - b))) < 1e-3;
if (!HAS_RICH) console.log('(world dump has no spawns/nests/critters: nested-point and placement checks skipped; pass world_rich.json)');
for (const z of HAS_RICH ? ['briarE', 'duneW', 'desert'] : []) {
  const a = W2[z], b = W3n[z], w = a.w; let n = 0, rp = 0, fc = 0;
  const same = (p, q, what) => { n++; if (Math.abs(q.x - (w - p.x)) > 1e-3 || Math.abs(q.y - p.y) > 1e-9) bad(`${z} ${what} not mirrored (${p.x},${p.y}) -> (${q.x},${q.y})`); };
  for (const k of ['spawns', 'nests', 'critters', 'lights', 'npcs']) (a[k] || []).forEach((p, i) => {
    const q = b[k][i]; same(p, q, `${k}[${i}]`);
    if (typeof p.facing === 'number') { fc++; if (!angEq(q.facing, Math.PI - p.facing) || Math.abs(Math.cos(q.facing) + Math.cos(p.facing)) > 1e-3 || Math.abs(Math.sin(q.facing) - Math.sin(p.facing)) > 1e-3) bad(`${z} ${k}[${i}] facing ${p.facing} -> ${q.facing}`); }
    if (typeof p.vx === 'number' && q.vx !== -p.vx && !(p.vx === 0 && q.vx === 0)) bad(`${z} ${k}[${i}] vx`);
    (p.route || []).forEach((r, j) => { rp++; same(r, q.route[j], `${k}[${i}].route[${j}]`); });
  });
  console.log(`${z}: nested mirror ok for ${n} points (${rp} route points, ${fc} facings flipped PI - a)`);
}
// synthetic: the shapes the engineer listed (route/path/waypoints/patrol/points, {x,y} and [x,y], nested, shared refs)
{ const { mirrorX } = require(fs.existsSync(path.join(D, 'out/apply_exits_patch.js')) ? path.join(D, 'out/apply_exits_patch.js') : path.join(D, 'apply_exits_patch.js'));
  const sh = { x: 3, y: 1 }, sw = { w: 10, h: 2, tiles: Array(20).fill(0).map((_, i) => i), solid: Array(20).fill(0), exits: [{ x: 9.4, y: 1, to: 'q', sx: 5, sy: 5 }],
    spawns: [{ x: 2, y: 1, kind: 'snake', route: [{ x: 2, y: 1 }, { x: 4, y: 1 }], path: [[1, 1], [2, 0.5]], facing: 0, rotY: 0.5 }],
    nests: [{ x: 1, y: 1, waypoints: [sh, sh], patrol: { points: [[7, 1]] } }], npcs: [{ x: 5, y: 1, homeX: 6, homeY: 1, pos: [8, 1], meta: { target: { x: 9, y: 0 } } }],
    lights: [{ x: 1, y: 1, r: 3 }], spawn: { x: 0.5, y: 1 } };
  mirrorX(sw, { expect_w: 10, expect_h: 2 });
  const S = sw.spawns[0], exp = [[S.x, 8], [S.route[0].x, 8], [S.route[1].x, 6], [S.path[0][0], 9], [S.path[1][0], 8], [sw.nests[0].x, 9], [sh.x, 7],
    [sw.nests[0].patrol.points[0][0], 3], [sw.npcs[0].x, 5], [sw.npcs[0].homeX, 4], [sw.npcs[0].pos[0], 2], [sw.npcs[0].meta.target.x, 1], [sw.lights[0].x, 9],
    [sw.spawn.x, 9.5], [sw.exits[0].x, 0.6], [sw.exits[0].sx, 5], [sw.tiles[0], 9], [sw.lights[0].r, 3], [S.rotY, -0.5]];
  const badS = exp.filter(([g, e]) => Math.abs(g - e) > 1e-9);
  if (!angEq(S.facing, Math.PI)) badS.push(['facing', S.facing]);
  console.log(`synthetic nested mirror (route, path [x,y], waypoints, shared ref, patrol.points, npc pos/home/target, lights, rotY, facing): ${badS.length ? 'FAIL ' + JSON.stringify(badS) : 'ok'}`);
  if (badS.length) bad('synthetic mirror'); }
// ---- placement: every spawn, nest, route point and critter on an open tile reachable from the player spawn; patrol legs walkable
for (const z of HAS_RICH ? ['wild', 'briarE', 'duneW', 'desert', 'lut'] : []) {
  const w = W3[z], R = reach(w, w.spawn.x, w.spawn.y), cell = p => Math.floor(p.y) * w.w + Math.floor(p.x); let n = 0, legs = 0; const fails = [];
  const chk = (p, what) => { n++; const i = cell(p); if (w.solid[i] || !R[i]) fails.push(`${what} (${p.x},${p.y}) ${w.solid[i] ? 'solid' : 'unreachable'}`); };
  (w.spawns || []).forEach((s, i) => { chk(s, `spawns[${i}] ${s.kind}`); const r = s.route || [];
    r.forEach((p, j) => { chk(p, `spawns[${i}].route[${j}]`); const q = r[(j + 1) % r.length]; if (r.length < 2) return; legs++;
      const L = Math.hypot(q.x - p.x, q.y - p.y); for (let t = 0; t <= L; t += 0.25) { const x = p.x + (q.x - p.x) * t / L, y = p.y + (q.y - p.y) * t / L; if (w.solid[Math.floor(y) * w.w + Math.floor(x)]) { fails.push(`spawns[${i}] patrol leg ${j}->${(j + 1) % r.length} crosses a solid tile at (${x.toFixed(1)},${y.toFixed(1)})`); break; } } }); });
  (w.nests || []).forEach((p, i) => chk(p, `nests[${i}]`)); (w.critters || []).forEach((p, i) => chk(p, `critters[${i}] ${p.kind}`));
  fails.forEach(f => bad(`${z} ${f}`)); console.log(`${z}: ${n} spawn/nest/route/critter points on open reachable tiles, ${legs} patrol legs walkable: ${fails.length ? 'FAIL' : 'ok'}`);
}
// points_move rows all matched, and nests were not dropped on the road
{ const nm = warns.filter(x => /no point/.test(x)); if (nm.length) bad('points_move unmatched: ' + nm.join('; '));
  for (const z of ['wild', 'duneW', 'desert']) { const p = JSON.parse(fs.readFileSync(P(`${z}_exits_patch_v3.json`)));
    for (const m of p.points_move || []) { const t = W3[z].tiles[Math.floor(m.new.y) * W3[z].w + Math.floor(m.new.x)];
      console.log(`${z} points_move ${m.list}${m.kind ? ' ' + m.kind : ''} (${m.old.x},${m.old.y}) -> (${m.new.x},${m.new.y}) tile ${t}`);
      if (m.list === 'nests' && t === 6) bad(`${z} nest moved onto the road`); } } }
console.log(ok ? 'ALL OK' : 'FAILURES');
process.exitCode = ok ? 0 : 1;
