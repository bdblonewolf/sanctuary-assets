// applyAshenPatch(world, patch) -- Ashen Coast starter-area cleanup (ashen_starter_v1)
// Paste into the routes bundle source (the module that defines uc()/sc()) and call
//   l = applyAshenPatch(l, ASHEN_PATCH)
// on the coast world object returned by sc('coast',...) inside uc(), right before it is returned.
// ASHEN_PATCH = contents of ashen_starter_patch.json (import or inline).
// Pure data edit: touches world.props and world.lights only. Never touches tiles/solid (river,
// bridge and edge collision stay exactly as generated). Idempotent (patched worlds carry world.ashenPatch).
function applyAshenPatch(world, patch) {
  if (!world || world.ashenPatch === patch.patch_id) return world;
  const E = 0.01, props = world.props, lights = world.lights || (world.lights = []);
  const strip = (o) => { const r = {}; for (const k in o) if (k !== 'reason' && k !== 'id' && k !== 'match') r[k] = o[k]; return r; };
  const find = (m) => {
    const i = props.findIndex(p => p.kind === m.kind && Math.abs(p.x - m.x) < E && Math.abs(p.y - m.y) < E &&
      (m.style === undefined || p.style === m.style));
    if (i < 0) console.warn('[ashen] no match', m);
    return i;
  };
  for (const r of patch.removed || []) { const i = find(r.match); if (i >= 0) props.splice(i, 1); }
  for (const s of patch.swapped || []) {
    const i = find(s.match); if (i < 0) continue;
    const o = props[i], w = s.with, n = { kind: w.kind, x: w.x ?? o.x, y: w.y ?? o.y };
    if (o.looted) n.looted = o.looted;                       // keep loot state
    for (const k in w) if (k !== 'x' && k !== 'y') n[k] = w[k];
    if (n.kind !== 'body' && n.kind !== o.kind) delete n.looted;
    props[i] = n;
  }
  for (const m of patch.moves || []) { const i = find(m.match); if (i >= 0) Object.assign(props[i], m.to); }
  for (const f of patch.fixes || []) if (f.type === 'prop') { const i = find(f.match); if (i >= 0) Object.assign(props[i], f.set); }
  for (const c of patch.collider_adds || []) if (c.type === 'prop_box' && c.match) { const i = find(c.match); if (i >= 0) Object.assign(props[i], c.set); }
  for (const a of patch.adds || []) props.push(strip(a));
  for (const m of patch.lights_move || []) {
    const L = lights.find(l => Math.abs(l.x - m.match.x) < E && Math.abs(l.y - m.match.y) < E);
    if (L) { L.x = m.to.x; L.y = m.to.y; } else console.warn('[ashen] no light', m.match);
  }
  for (const l of patch.lights_add || []) lights.push({ x: l.x, y: l.y, r: l.r, warm: l.warm });
  world.ashenPatch = patch.patch_id;
  return world;
}
if (typeof module !== 'undefined') module.exports = { applyAshenPatch };
