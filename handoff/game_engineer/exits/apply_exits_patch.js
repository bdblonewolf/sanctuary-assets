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
  world.exitsPatch = patch.patch_id;
  return world;
}
// Mirror a generated world left<->right in place. Tiles/solid and any other per-tile array (length w*h) have each row
// reversed; every point-like object (has numeric x and y) found directly on the world or in a top-level array
// (props, npcs, spawn, lights, nests, spawns, loreSpots, ...) gets x -> w - x (homeX too), rotY -> -rotY and
// face-e <-> face-w. exits get x -> w - x; their sx/sy point into OTHER zones and are set by exits_final.
function mirrorX(world, opt) {
  const w = world.w, h = world.h, N = w * h, done = new Set();
  if (opt && opt.expect_w && (opt.expect_w !== w || opt.expect_h !== h)) { console.warn('[exits] mirror size mismatch', w, h); return; }
  const pt = o => {
    if (!o || typeof o !== 'object' || done.has(o) || typeof o.x !== 'number' || typeof o.y !== 'number') return; done.add(o);
    o.x = +(w - o.x).toFixed(4); if (typeof o.homeX === 'number') o.homeX = +(w - o.homeX).toFixed(4);
    if (typeof o.rotY === 'number') o.rotY = -o.rotY;
    if (o.style === 'face-e') o.style = 'face-w'; else if (o.style === 'face-w') o.style = 'face-e';
  };
  for (const k of Object.keys(world)) {
    const v = world[k];
    if (k === 'exits') { for (const e of v || []) { e.x = +(w - e.x).toFixed(4); done.add(e); } continue; }
    if ((Array.isArray(v) || ArrayBuffer.isView(v)) && v.length === N && (typeof v[0] === 'number' || typeof v[0] === 'boolean')) {
      for (let y = 0; y < h; y++) for (let a = y * w, b = a + w - 1; a < b; a++, b--) { const t = v[a]; v[a] = v[b]; v[b] = t; }
    } else if (Array.isArray(v)) v.forEach(pt); else pt(v);
  }
}
if (typeof module !== 'undefined') module.exports = { applyExitsPatch, mirrorX };
