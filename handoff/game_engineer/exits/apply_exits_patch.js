// applyExitsPatch(world, patch) -- exits_v2 (exits move to where the roads naturally lead)
// One patch per zone: handoff/game_engineer/exits/<zone>_exits_patch.json (tile zones + sx/sy-only partners).
// Martsirt is NOT applied with this function (its world is the authored martsirt_world.json + placements):
// see martsirt_exits_patch.json "apply".
// Call on the generated world object (sc(zone)) after it is built (coast: after applyAshenPatch), before caching.
// Pure data edit on world.tiles / world.solid / world.exits / world.props. Old-value checks: a row whose current
// value differs from "old" is skipped with a warning (never overwrites unexpected data). Idempotent via world.exitsPatch.
function applyExitsPatch(world, patch) {
  if (!world || world.exitsPatch === patch.patch_id) return world;
  const E = 0.01, w = world.w, props = world.props || (world.props = []);
  const I = (x, y) => y * w + x;
  for (const [x, y, o, n] of patch.tiles_set || []) {
    const i = I(x, y); if (world.tiles[i] !== o) { console.warn('[exits] tile mismatch', x, y, world.tiles[i], o); continue; } world.tiles[i] = n;
  }
  for (const [x, y, o, n] of patch.solid_set || []) {
    const i = I(x, y); if ((world.solid[i] ? 1 : 0) !== o) { console.warn('[exits] solid mismatch', x, y); continue; } world.solid[i] = n;
  }
  for (const s of patch.exits_set || []) {
    const e = (world.exits || []).find(q => q.to === s.match.to); if (!e) { console.warn('[exits] no exit', s.match); continue; }
    for (const k of ['x', 'y', 'sx', 'sy']) if (s.new[k] !== undefined) e[k] = s.new[k];
  }
  for (const m of patch.props_move || []) {
    const p = props.find(q => q.kind === m.match.kind && Math.abs(q.x - m.match.x) < E && Math.abs(q.y - m.match.y) < E &&
      (m.match.style === undefined || q.style === m.match.style));
    if (!p) { console.warn('[exits] no prop', m.match); continue; }
    for (const k in m.to) p[k] = m.to[k];
  }
  for (const a of patch.props_add || []) props.push(Object.assign({}, a));
  // exits_v3: mirror the whole zone left<->right (x -> w - x), then set the final exits. Used for the west-road
  // wilderness zones (briarE, duneW, desert) so the in-game chart (unrotated, north up) reads wild <- briarE <- duneW <- desert.
  if (patch.mirror_x) mirrorX(world, patch.mirror_x);
  for (const s of patch.exits_final || []) {
    const e = (world.exits || []).find(q => q.to === s.to); if (!e) { console.warn('[exits] no exit', s.to); continue; }
    for (const k of ['x', 'y', 'sx', 'sy']) if (s[k] !== undefined) e[k] = s[k];
  }
  if (patch.points_move) movePoints(world, patch.points_move);
  world.exitsPatch = patch.patch_id;
  return world;
}
// Mirror a generated world left<->right in place (exits_v3). Tiles/solid and any other per-tile array (length w*h)
// have each row reversed. Then it RECURSES through every other field of the world (spawns, nests, npcs, critters,
// lights, props, spawn, and anything nested in them: route / path / waypoints / patrol / points / home ...):
//  - every object with numeric x and y is a point: x -> w - x (also homeX, gx, tx, x0, x1 if present), vx -> -vx,
//    heading angles facing/heading -> PI - a (2D heading, (cos a, sin a) in tile x/y; normalised to [0, 2PI)),
//    rotY -> -rotY (three.js yaw; tile x/y map to X/Z), style face-e <-> face-w;
//  - every [x, y] pair (array of exactly 2 numbers) inside a path-like field (route, path, waypoints, patrol, points,
//    pos, at, home, target, goal) or inside an array of such pairs: x -> w - x.
// Shared objects are flipped once. exits get x -> w - x only; their sx/sy point into OTHER zones (set by exits_final).
const MIRROR_PATH_KEYS = new Set(['route', 'path', 'waypoints', 'patrol', 'points', 'pos', 'at', 'home', 'target', 'goal']);
function mirrorX(world, opt) {
  const w = world.w, h = world.h, N = w * h, done = new Set();
  if (opt && opt.expect_w && (opt.expect_w !== w || opt.expect_h !== h)) { console.warn('[exits] mirror size mismatch', w, h); return; }
  const r4 = v => +v.toFixed(4), TAU = Math.PI * 2;
  const ang = a => r4(((Math.PI - a) % TAU + TAU) % TAU);
  const isPair = v => Array.isArray(v) && v.length === 2 && typeof v[0] === 'number' && typeof v[1] === 'number';
  const flipPair = v => { if (!done.has(v)) { done.add(v); v[0] = r4(w - v[0]); } };
  const visit = (o, key, depth) => {
    if (!o || typeof o !== 'object' || depth > 12 || ArrayBuffer.isView(o)) return;
    if (Array.isArray(o)) {
      if (MIRROR_PATH_KEYS.has(key) && isPair(o)) return flipPair(o);
      const pairs = o.length > 0 && o.every(isPair);
      for (const v of o) { if (pairs && MIRROR_PATH_KEYS.has(key)) flipPair(v); else visit(v, key, depth + 1); }
      return;
    }
    if (done.has(o)) return; done.add(o);
    if (typeof o.x === 'number' && typeof o.y === 'number') {
      o.x = r4(w - o.x);
      for (const k of ['homeX', 'gx', 'tx', 'x0', 'x1']) if (typeof o[k] === 'number') o[k] = r4(w - o[k]);
      if (typeof o.vx === 'number') o.vx = -o.vx;
      for (const k of ['facing', 'heading']) if (typeof o[k] === 'number') o[k] = ang(o[k]);
      if (typeof o.rotY === 'number') o.rotY = -o.rotY;
      if (o.style === 'face-e') o.style = 'face-w'; else if (o.style === 'face-w') o.style = 'face-e';
    }
    for (const k of Object.keys(o)) { const v = o[k]; if (v && typeof v === 'object') visit(v, k, depth + 1); }
  };
  for (const k of Object.keys(world)) {
    const v = world[k];
    if (k === 'exits') { for (const e of v || []) { e.x = r4(w - e.x); done.add(e); } continue; }
    if ((Array.isArray(v) || ArrayBuffer.isView(v)) && v.length === N && (typeof v[0] === 'number' || typeof v[0] === 'boolean')) {
      for (let y = 0; y < h; y++) for (let a = y * w, b = a + w - 1; a < b; a++, b--) { const t = v[a]; v[a] = v[b]; v[b] = t; }
    } else visit(v, k, 0);
  }
}
// exits_v3 points_move: move a spawn / nest / critter / route point (matched by list + kind + old x,y within 0.05,
// in the FINAL, post-mirror frame). Rows: {list, kind?, index?, route_i?, old:{x,y}, new:{x,y}, why}. A route point
// is addressed as list 'spawns' + route_i (index into that spawn's route). Old-value check as everywhere else.
function movePoints(world, rows) {
  const E = 0.05, near = (p, o) => !!p && typeof p.x === 'number' && Math.abs(p.x - o.x) < E && Math.abs(p.y - o.y) < E;
  for (const m of rows || []) {
    const L = world[m.list], list = Array.isArray(L) ? L : L ? [L] : []; let p = null, owner = null;
    for (const q of list) {
      if (!q) continue;
      if (m.route_i !== undefined) { if (Array.isArray(q.route) && near(q.route[m.route_i], m.old)) { p = q.route[m.route_i]; owner = q; break; } }
      else if ((m.kind === undefined || q.kind === m.kind) && near(q, m.old)) { p = owner = q; break; }
    }
    if (!p) { console.warn('[exits] no point', m.list, m.kind, m.old); continue; }
    p.x = m.new.x; p.y = m.new.y;
    // a patrol starts where its enemy spawns: keep the spawn and route[0] together when either one moves
    const r0 = Array.isArray(owner.route) ? owner.route[0] : null;
    if (r0 && r0 !== p && near(r0, m.old)) { r0.x = m.new.x; r0.y = m.new.y; }
    if (owner !== p && r0 === p && near(owner, m.old)) { owner.x = m.new.x; owner.y = m.new.y; }
  }
}
if (typeof module !== 'undefined') module.exports = { applyExitsPatch, mirrorX, movePoints };
