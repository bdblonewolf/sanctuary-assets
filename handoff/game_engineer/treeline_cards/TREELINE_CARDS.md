# Treeline cards: painted pine-canopy silhouettes replace the 3D cone trees

Date: 2026-11-06 ~01:25 America/Detroit (EST)

## What changed
I replaced every `trees_*` child in the border kit and rect backdrop GLBs. Each one is now a painted, irregular pine-canopy silhouette card mesh.
- **Scope:** all 24 `models/border_kit_v1/bk_*.glb` and all 60 `models/outdoor/v5_maps/rect/backdrop_near_rect_*.glb`.
  - **53 files changed.** That is 8 border-kit files (forest and town × 4 seasons) and 45 rect files (15 rings × summer, autumn and winter).
  - **31 files unchanged.** They have no `trees_*` nodes: the coast_land, desert, mountain and sea kits, and all 15 rect `*_dead` rings.
  - **295 `trees_*` nodes replaced** in total.
- **Same node:** each node keeps its name, its parent (`straight12_a`, `near_land_E`, ...), its TRS (none), and its local AABB. The AABB matches within 1e-3 m, and `qa/validate_report.txt` shows all 53 files ok.
- **Not touched:**
  - Parent meshes, `apron_*`, `near_sea_*`, `water_*`, and all `col_*` nodes. Their vertex data, indices, materials and textures are byte-identical by hash (checked by `tools/validate.py`).
  - The `wip_models` working-tree deletions in `/workspace/sanctuary-assets`. I committed from a separate clean worktree.
  - Game code and locked files.
- **Cost:** tree vertices went from 1,326,364 to 341,672 (−74%). Rect GLBs total ~144 MB → ~126 MB. Kit files change by −30 KB to +100 KB each because each now embeds a ~0.1–0.2 MB atlas.
- **Mesh:** cones are grouped into cells of 7 m (kit) or 15 m (rings). Each cell gets 2 vertical cards, 8 vertices in total:
  - one card faces the map, and the second is rotated ±40° (kit) or ±32° (ring) so the clump has volume when the camera orbits.
  - the top leans back 10°, so the cards still read from the pitch-50° game camera.
  - each card's bottom edge follows the cone bases (slope capped) and is buried 0.6 m or more, so there is no floating edge.
  - per-cell tile choice and UV flips break up repetition.
  - autumn cells with rust-colored cones get tiles with rust (larch-like) pines.

## Runtime contract (matches the existing 12b `prep()`/`hook()` and `placeKit()`)
- **Material per file:**
  - kit: `ms_bk_treecard_<season>`
  - ring: `ms_bd5_treecard_<season>`
  - Settings: alphaMode MASK, cutoff 0.5, doubleSided, metallic 0, roughness 0.95. The baseColor is an embedded PNG atlas: 1024², 2×2 tiles, palette-quantized, clamp-to-edge.
  - The names are new on purpose. `placeKit()` caches materials by name, so the cards can never share a material with the untextured `ms_bd5_trees` cones that still exist in `v5_maps/border/*` and the c-rings. That shared cache is a likely cause of untextured green slabs.
- **Attributes:** POSITION, NORMAL, TEXCOORD_0, and COLOR_0 (VEC4 unorm8). Both loaders force `vertexColors = true`, so COLOR_0 always exists:
  - RGB is 0.86–1.0 brightness jitter.
  - kit alpha = 1.0. The dress hook uses the stock `color_fragment`, which multiplies alpha when vertex alphas exist. Alpha 0 would alpha-test the cards away.
  - ring alpha = the cones' original fog factor (mean per cell), for `mix(rgb, fogColor, vColor.a*0.6)`.
- No new glTF extensions, no Draco and no meshopt. gltf-validator reports 0 errors on all 53 files. The only warnings are pre-existing parent tangent-space warnings.
- **Cache:** the game fetches these from raw.githubusercontent with `?v=` query strings. Bump the version (or hard-refresh) to see the new files.

## Keep blacks
- **On screen:** I rendered with three r187 GLTFLoader using the same material patching as the game, with only the trees drawn. Each card set's mean luminance is 0.62–0.97 of the cone version in every view, so none is lighter (`qa/calib_last.txt`).
- **Texture vs cone vertex colors:** p5 (5th-percentile luminance) is ≤ 0.87 of the cones for every atlas (`qa/qa_luminance.txt`).
- `ring_winter` has a texture mean of 1.08 because the snow-laden tops are painted white. On screen it is 0.87–0.92 of the old snow cones, so it is still darker.
- **Caveat:** on-screen p5 is higher than with the cones. Many cone faces render pure black (back faces and self-shadow), and a card has no self-shadowed faces. The deep palette, the dark backing canopy and the 0.55 back row keep blacks as deep as a card allows.

## Previews (`previews/`)
In each sheet, the left image is BEFORE (3D cones) and the right is AFTER (cards).
- `treecards_rect_eye_sxs.jpg`: third-person eye height, like Brian's target screenshot.
- `treecards_rect_gamecam_sxs.jpg`: high game camera.
- `treecards_kit_eye_sxs.jpg` and `treecards_kit_gamecam_sxs.jpg`: forest and town kits (summer, autumn, winter, dead).
- `treecards_atlases.jpg`: the 7 atlases (kit/ring × summer, autumn and winter, plus kit_dead).

Reference screenshots (box only): `/workspace/sanctuary_env/treeline_refs/martsirt_3d_cones_target_look.jpg` (target) and `failed_green_peaks_do_not_ship.jpg` (the failure to avoid). The new cards are textured, irregular and upright. They are not flat untextured slabs.

## Not in this pass (outside the brief, still 3D cones)
These still have `trees_*` cone meshes:
- `models/outdoor/v5_maps/backdrop_near_c{23,30,36,42,52}_{summer,autumn}.glb`
- `backdrop_mid_quads_{summer,autumn}.glb`
- `models/outdoor/v5/backdrop_mountain_ring_v5_{summer,autumn}_{mid,near}.glb`

`tools/build_cards.py` will convert them on request.

## Rebuild
- `tools/paint.py` builds the atlases. It needs `/tmp/orig_lum2.json` (written by `qa_lum.py`) and `render_gain.json`.
- `tools/build_cards.py <outdir> <glbs...>` builds the cards. `tools/gl.py` must be importable (it lives at `/tmp/gl.py` on the box).
- `tools/validate.py <orig> <new> ...` checks the results.
- `tools/calib.py` runs the render-based brightness calibration (puppeteer + three from `/workspace/m2m_test/node_modules`).
