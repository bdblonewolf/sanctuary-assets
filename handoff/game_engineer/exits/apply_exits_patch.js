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
  world.exitsPatch = patch.patch_id;
  return world;
}
if (typeof module !== 'undefined') module.exports = { applyExitsPatch };
