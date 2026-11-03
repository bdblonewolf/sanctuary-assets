// exits_v2 apply test. Applies each patch twice (idempotency) to the live generated worlds and, where the reviewed
// after_<zone>.json exists (work dir), compares tiles/solid/exits/props. Also checks that every file path in the
// patches (martsirt splat) resolves from the repo root.
// Usage: node test_apply.js [world_full.json]   (patches: ./out/ if present, else this file's dir)
const fs = require('fs'), path = require('path');
const D = __dirname, PD = fs.existsSync(path.join(D, 'out')) ? path.join(D, 'out') : D;
const { applyExitsPatch } = require(path.join(PD, 'apply_exits_patch.js'));
let fail = 0;
// repo root = first ancestor of the handoff/game_engineer/exits copy that has handoff/; in the work dir use the repo checkout
function repoRoot() { for (let d = D; d !== path.dirname(d); d = path.dirname(d)) if (fs.existsSync(path.join(d, 'handoff/game_engineer'))) return d;
  return fs.existsSync('/workspace/sanctuary-assets/handoff') ? '/workspace/sanctuary-assets' : null; }
const R = repoRoot();
{ const m = JSON.parse(fs.readFileSync(path.join(PD, 'martsirt_exits_patch.json'))), f = m.splat && m.splat.file;
  const ok = !!(R && f && fs.existsSync(path.join(R, f)));
  const textOk = !/exits\/martsirt\//.test(JSON.stringify(m));
  console.log(`martsirt splat ${f} resolves from repo root: ${ok}; no stale exits/martsirt/ path: ${textOk}`); if (!ok || !textOk) fail++; }
const WF = process.argv[2] || path.join(D, 'world_full.json');
if (!fs.existsSync(WF)) { console.log(`(no world dump at ${WF}; pass a dump of the live worlds as argv[2] to run the apply checks)`); process.exit(fail ? 1 : 0); }
const W = JSON.parse(fs.readFileSync(WF)).worlds;
for (const z of ['coast', 'wild', 'desert', 'mires', 'briarE', 'lut', 'sink']) {
  const w = JSON.parse(JSON.stringify(W[z])), p = JSON.parse(fs.readFileSync(path.join(PD, `${z}_exits_patch.json`)));
  applyExitsPatch(w, p); const once = JSON.stringify(w); applyExitsPatch(w, p);
  let msg = z + ` idempotent=${JSON.stringify(w) === once}`; if (JSON.stringify(w) !== once) fail++;
  const AF = path.join(D, `after_${z}.json`);
  if (fs.existsSync(AF)) { const A = JSON.parse(fs.readFileSync(AF));
    const key = q => q.kind + ':' + q.x.toFixed(2) + ',' + q.y.toFixed(2), s = a => a.map(key).sort().join('|');
    const r = { tiles: JSON.stringify(w.tiles) === JSON.stringify(A.tiles), solid: JSON.stringify(w.solid.map(Number)) === JSON.stringify(A.solid.map(Number)),
      exits: JSON.stringify(w.exits) === JSON.stringify(A.exits), props: s(w.props) === s(A.props) };
    for (const k in r) { msg += ` ${k}=${r[k]}`; if (!r[k]) fail++; } msg += ` n=${w.props.length}/${A.props.length}`;
    if (fs.existsSync(path.join(D, 'v2in'))) fs.writeFileSync(path.join(D, `v2in/after_${z}_js.json`), JSON.stringify(w)); }
  else msg += ' ' + JSON.stringify(w.exits);
  console.log(msg); }
console.log(fail ? `FAIL (${fail})` : 'ALL OK'); process.exit(fail ? 1 : 0);
