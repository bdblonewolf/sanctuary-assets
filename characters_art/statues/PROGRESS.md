# Angel statues - PROGRESS
(resume point: read this first)

## Plan
- src/sdf_lib.py   : sparse SDF engine (numpy, per-primitive AABB slices) + primitives (feather, wings, plate, cloth)
- src/<name>_sdf.py: sculpt -> src/<name>_hi.npz (statue, 3mm) + plinth
- src/bake.py      : Blender: hi npz -> decimated game mesh, UV, bake base/normal/rough/metal/AO, colliders, fx empties, GLB
- src/render.py    : previews front/iso/close
- validation: node gltf-validator

## Status
- [ ] female_bust (HERO)
- [ ] knight_kneeling (HERO)
- [ ] sword_shield (02)
- [ ] archangel_black_gold (03)
- [ ] spear_serpent (04)
- [ ] mourner_bronze (01)
- [ ] seraph_six_wing (05)
- [ ] draped_maiden (06)
- [ ] reclining_muse (07, weathered marble, broken stone block)
- [ ] veiled_maiden (08, weathered marble)

## READY FOR REVIEW
(none yet)

## Log
- 00:50 started; read refs + v4 pipeline
- 00:51 steering: added 07/08 to queue; log each finished statue under READY FOR REVIEW and keep going
- 00:52 art direction: D2 mood ('Epic Angels and Sad Souls') for all but 07/08: grave faces, weathered/chipped/rain-stained, lichen plinths, larger ragged wings, gothic austere armour (filigree, pitting, worn edge), dulled gilt on raised edges only, deep verdigris, grave-monument plinths with inscription band. No pristine white or bright gold.

## PAUSED 01:05 (Brian: statues to be done last) — exact resume point
**Status: HERO female bust in progress, nothing exported yet. No GLBs, no READY FOR REVIEW items.**

### Done so far (all saved)
- `src/sdf_lib.py`: SDF engine + feather/wing builder. NEW: `feather(..., incl, shing)` shingle tilt (tips/one vane edge raised so rows read); `GROOVE=[flight,covert]` barb-groove strength (0.45, 0.15).
- `src/figure.py`: procedural SDF head. **Superseded for faces**: it looked doll-like, keep only `lock()` for hair.
- **NEW key decision:** bodies/faces/hands now come from MakeHuman (MPFB2, CC0, installed Blender extension) via `src/human.py`
  (`blender -b --python human.py -- spec.json`). It does phenotype + targets, expression units (eye closure, inner-brow-up, mouth depression → grave closed-eye face),
  world-space bone pose deltas `[bone, axis, deg]` (+x = bow forward, +y on LeftArm = lower arm), arm-limited `limb_cuts`, global plane `cuts` with hole fill, subdiv,
  and writes npz (v,f) + `_bones.json` (posed world bone head/tail). Read only from /workspace/sanctuary_npc (nothing modified there).
- `src/fb_human.json` → `work/fb_human.npz` (104k verts, 209k tris, height 1.95 = 1.2× life, cut at z=1.02, arms cut at 0.85 of the upper arm, head bowed and tilted). Face checked: good, sorrowful, eyes closed.
- `src/test_wing2.py`: hero wing (R 4.5 mm, ~45 s). Silhouette OK, feathers individual. Last change (6 rows of smaller coverts + 34 marginals) **was written but its render was interrupted; not yet checked**.

### Next steps on resume
1. Run `/workspace/venv/bin/python src/test_wing2.py 0.0045` then `src/look.sh /tmp/w2.png -90,0,3.2,0.5,0,-0.2 -50,15,3.2,0.5,0,-0.2 -90,0,1.0,0.35,-0.1,0.35 -- /tmp/wing2.npz`. Check that the covert rows read as scalloped rows. Make the wing taller/less dome-like (ref: apex well above the head, long drooping primaries with tips curling out, sides cupped forward).
2. Body SDF field from fb_human.npz (cKDTree Hoppe plane distance, ~4 mm grid, blurred) → drape shell (off-shoulder over her right shoulder/upper arm, radiating folds, torn hem + holes at the waist, skirt block with vertical folds down to the base), hair cap + `lock()` locks (centre part, wavy, over the shoulders), rough broken arm-stump caps.
3. Place: shift human dz=-0.12 so the bust base sits on the plinth top at z=0.9; wings rooted at the shoulder blades (±0.1,+0.08 local); plinth ~0.9 m grave pedestal with inscription band, chips, darker base.
4. Hi = human mesh + SDF meshes (separate overlapping meshes are OK). Low = Blender voxel remesh of the joined meshes (union) → decimate to ~45k → Smart UV → bake (adapt build_v4.py mkmat/bake_set) → GLB → validate → previews → READY FOR REVIEW.
5. Then knight (MakeHuman male base + SDF plate armour), 02, 03, 04, 01, 05, 06, 07, 08, sheet, README.

## ART BOT TAKEOVER
- 2026-11-01 01:25 EST — art bot took over the statue project. READY FOR REVIEW: hero female bust only (`statue_angel_hero_bust.glb`); knight and others NOT started, waiting for Brian's review.
  - GLB: plain glTF 2.0 binary, no extensions, 3.41 MB, 1 unit = 1 m, Y up, origin at the base centre, 2.04 m tall (wing tips 2.04, plinth top 0.85). 38,554 tris game mesh + `col_base` box (12 tris). One material, maps baked from ~2.0M-tri hi sculpt: base colour 2K JPEG, normal 2K JPEG, ORM 1K JPEG (R=AO, G=rough, B=metal 0). gltf-validator: 0 errors / 0 warnings / 0 infos / 0 hints.
  - Previews (Cycles, dim blue-grey ambient + faint cold key): previews/hero_bust_front.png, hero_bust_iso.png (13.5 m, 35° iso, 90 mm), hero_bust_close.png.
  - Pipeline: src/hb_wings.py, hb_body.py, hb_plinth.py (SDF hi sculpt) -> src/hb_bake.py (Blender: low mesh, xatlas UVs, normal/AO/cavity bake) -> src/hb_tex.py (numpy triplanar texturing) -> src/hb_export.py -> src/hb_render.py.
  - Asset sources (all CC0):
    - Poly Haven `concrete_wall_008` (https://polyhaven.com/a/concrete_wall_008, 2K diffuse): fine mottling of the rain-worn marble.
    - Poly Haven `dirty_concrete` (https://polyhaven.com/a/dirty_concrete, 2K diffuse): grime and stain layer.
    - Poly Haven `mossy_rock` (https://polyhaven.com/a/mossy_rock, 2K diffuse): lichen and moss colour on the plinth, a few patches up top.
    - Downloaded through api.polyhaven.com/files/<id> into work/ph/; sampled triplanar and baked into the 2K base map. Rough/normal/AO maps from Poly Haven were downloaded but not used.
    - Body base: the MakeHuman bust already in work/fb_human.npz (from the earlier builder session). No Smithsonian 3D assets used.

### HERO BUST v2 — fine-tune pass (READY FOR REVIEW, 2026-11-01)
Backups of v1: `statue_angel_hero_bust_v1.glb`, `previews/hero_bust_{front,iso,close}_v1.png` (v1 hi meshes in `work/hb_v1/`, scripts `src/hb_wings_v1.py`, `src/hb_body_v2.py` = pre-v2 body script).
- **Stats:** `statue_angel_hero_bust.glb` 3,601,968 B (3.44 MiB); 38,976 tris statue + 12 tris `col_base`; validator 0 errors / 0 warnings / 0 infos / 0 hints; no extensions, cameras, lights. Base 2048² JPEG (1.00 MB), normal 2048² (734 KB), ORM 1024² (164 KB). Bounds (Y up): x −1.352…1.415, y 0…2.291, z −0.311…0.480. Height 2.29 m (< 2.4 m), wingspan ≈2.77 m. col_base unchanged (0.714 × 0.846 × 0.620 m).
- **Wings** (`src/hb_wings.py`): wrist raised and pushed out (arm bezier apex 0.86→1.05 m above the root, tip 0.73 m out), less back-sweep (yaw 0.38→0.30 rad) so it reads as a raised, spread silhouette from the front; 14 primaries fanning 4–40° outward (L 0.98–1.16), 17 secondaries, 6 covert rows with more feathers + 42 marginals; covert row step 11→16 mm for deeper stacked layering; ragging 1.25→0.72 and notch splits ×0.6 so the long feathers are worn, not dagger-spiky. `sdf_lib.wing_feathers` gained optional `row_step` / `flight_split` (defaults keep old behaviour). Low mesh 9.8k tris per wing (body 15k, plinth 4.6k).
- **Waist** (`src/hb_body.py`): MakeHuman torso cinched (−15 % x, −8 % y, Gaussian at z 1.09, arms masked out); cloth now uses a torso-only distance field (arms excluded); belly mass shrunk; cloth offset/folds pulled snug at the waist sides. Drape half-width at the waist 0.153→≈0.13 m (pre-scale); still fully covered/modest.
- **Fixes:** horizontal seam = formwork panel lines baked into the concrete_wall_008 photo-scan → cleaned copy `work/ph/concrete_wall_008_clean.png` (seam bands replaced by offset texture), plus single soft cloth sag (no step). Navel pit filled under the cloth (wide-blur belly field). Arm edge of the drape now a curved, torn line wrapping slightly round the front instead of a straight vertical cut. Marble whiter: base albedo 0.80→0.875, grime weights −15–25 % (texture mean 0.58→0.68).
- **Export fixes:** loose <20-face fragments dropped (224 faces); `src/hb_fixtan.py` post-export replaces 1 mikktspace zero tangent (validator error) with an orthogonal unit tangent.
- Pipeline: hb_wings (L/R, R 0.0045) → hb_body (0.003) → `NB=15000 NW=9800 blender -b -P hb_bake.py` → hb_tex.py → hb_export.py → hb_fixtan.py → hb_render.py (front: `-90 6 4.7 0 0 1.15 50 128 1000`; iso: `-45 35.26 13.5 0 0 1.1 90 128 1000`; close unchanged).
- Asset sources unchanged: Poly Haven CC0 concrete_wall_008 (seam-cleaned derivative), dirty_concrete, mossy_rock (2K diffuse); MakeHuman base mesh; no Smithsonian assets.
