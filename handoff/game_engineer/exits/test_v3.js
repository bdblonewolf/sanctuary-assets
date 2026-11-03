// exits_v3 checks: apply v2/v3 patches to the live generated worlds (world_full.json), verify the mirror, edges,
// arrivals and idempotency, and simulate the in-game chart (port of Od/wd/Td/Ed from the routes bundle) with NO override.
const fs = require('fs'), path = require('path');
const D = __dirname, P = f => fs.existsSync(path.join(D, 'out_v3', f)) ? path.join(D, 'out_v3', f) : fs.existsSync(path.join(D, 'out', f)) ? path.join(D, 'out', f) : path.join(D, f);
const { applyExitsPatch } = require(fs.existsSync(path.join(D, 'out/apply_exits_patch.js')) ? path.join(D, 'out/apply_exits_patch.js') : path.join(D, 'apply_exits_patch.js'));
const WF = process.argv[2] || path.join(D, 'world_full.json');
const W0 = JSON.parse(fs.readFileSync(WF)).worlds;
const clone = o => JSON.parse(JSON.stringify(o));
const V2 = ['coast', 'wild', 'desert', 'mires', 'briarE', 'lut', 'sink'];
const V3 = ['wild', 'briarE', 'duneW', 'desert', 'lut'];
function build(set) {
  const W = clone(W0);
  for (const z of V2) if (set !== 'live') applyExitsPatch(W[z], JSON.parse(fs.readFileSync(P(`${z}_exits_patch.json`))));
  if (set === 'v3') for (const z of V3) { const w = clone(W0[z]), p = JSON.parse(fs.readFileSync(P(`${z}_exits_patch_v3.json`))); applyExitsPatch(w, p); applyExitsPatch(w, p); W[z] = w; }
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
console.log(ok ? 'ALL OK' : 'FAILURES');
process.exitCode = ok ? 0 : 1;
