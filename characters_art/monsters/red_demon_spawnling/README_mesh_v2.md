# red_demon_spawnling_v2.glb (mesh upgrade)

A higher-quality rebuild of the Fallen Spawnling mesh (Grove Mauler bear quality). The v1 files are unchanged.

- Mobile copy (live): `red_demon_spawnling_v2.glb`, 21,905 tris, textures 1024 JPEG, 1.6 MB. No meshopt or Draco.
- Master (uncompressed): `masters/red_demon_spawnling_v2.glb`, same mesh with 2048 color and normal plus 1024 ORM, 4.1 MB.
- Size: 1.02 x 0.35 x 1.446 m before the tail fix (0.416 m deep after it) (same height as v1). Single skinned mesh, A-pose.
- Rig: the same 52-bone mixamorig skeleton as v1 (male_regular base). Weights were transferred from the v1 mesh, so the clips in `red_demon_spawnling_anim_v2.glb` should play on it unchanged. The file itself has no clips.
- Loincloth recolored from teal to the concept's brown.
- Preview: `previews/red_demon_spawnling_v2.png`. Made with Hunyuan3D-2.1 from the existing concept, baked and graded in Blender.

## Tail fix (Nov 3, 2026)
- The tail was fused to the outside of the left thigh and hung beside the leg, so in the back view it looked offset and floating. It is now re-rooted at the tailbone: the root sits about 3 cm inside the loincloth/back at the base of the spine, and the tail sweeps back and down and curls up on the left. The old thigh stub was removed and capped flush.
- Tail weights: 100% Hips (the rig has no tail bones). The body around the tailbone is also about 100% Hips, so the root moves rigidly with it in every clip. Checked every frame of idle, run, attack, leap_attack, hit, death, attack2, death2 and death_old in red_demon_spawnling_anim_v2.glb: the root moves at most 1.7 mm relative to the body. The tail can briefly clip the legs in run and death2 because it has no bones of its own. There is no walk clip.
- 21,890 tris (was 21,905, -15). Same 52-joint skeleton and nodes, no meshopt or Draco. Width and height are unchanged (1.02 x 1.446 m). Depth is now 0.416 m because the tail sits behind the body.
- Preview: `previews/red_demon_spawnling_v2_tailfix.png`.

## Cleanup pass: gaps, stretch, clipping (Nov 3, 2026)
Only geometry and weights changed. The skeleton, the 54 nodes and names, the 52 joints, and the clip files (`red_demon_spawnling_anim_v2.glb`, `red_demon_spawnling_walk.glb`) are unchanged. There are no new `_v2` clips. No meshopt or Draco.
- **Gaps:** 1392 open boundary edges (28 holes), 3 non-manifold edges and 6 degenerate tris went to 0 / 0 / 0. The model is now 2 closed shells: the body, and the tail, which is closed and sits about 3 cm inside the body. Nothing is see-through.
- **Tris:** 21,890 went to 22,764 (+4.0%).
- **Weights:**
  - Weights were smoothed with 40 Laplacian passes, with up to 4 influences.
  - The hands and claws were re-weighted so neighbouring fingers no longer pull each other.
  - The loincloth is weighted to Hips/Spine and blends into the thighs toward the hem (up to 85%).
- **Tail:** bent 45° down and 25° to the side, shortened to 0.8x, and weighted 75% Hips / 25% Spine. Tail-into-leg clipping is now 0 in every clip (it was 3.6 cm in run and 3.4 cm in death2).
- **Measured on every frame of every clip** (idle, walk, run, attack, attack2, leap_attack, hit, death, death2). The table gives worst stretch as max edge, p99.9 edge and p99.9 triangle area, then worst penetration.

| clip | stretch before (max/p99.9e/p99.9a) | stretch after | penetration before | penetration after |
|---|---|---|---|---|
| idle | 15.6 / 8.65 / 14.95 | 5.91 / 2.90 / 5.29 | arm 0.7 cm, cloth 0.8 | 0 |
| walk | 22.9 / 9.72 / 14.75 | 5.80 / 3.28 / 4.89 | arm 3.1, cloth 1.9 | 0 |
| run | 22.2 / 9.36 / 12.8 | 5.53 / 3.14 / 4.32 | arm 5.0, tail 3.6, cloth 3.6 | tail 0, arm 0, cloth 2.9 (15 v) |
| attack | 24.5 / 10.0 / 16.5 | 7.79 / 3.59 / 6.38 | arm 2.8, cloth 2.0 | arm 4.1 (1 v), cloth 0 |
| attack2 / leap_attack | 24.3 / 10.4 / 16.3 | 7.19 / 3.39 / 5.45 | arm 5.2, cloth 1.9, leg-leg 3.4 | arm 4.8 (6 v), cloth 1.1, leg-leg 0 |
| hit | 19.3 / 9.94 / 16.6 | 5.59 / 3.14 / 5.55 | cloth 1.0 | 0 |
| death | 22.1 / 10.7 / 15.0 | 5.50 / 3.37 / 5.08 | claw 3.9, arm 7.1, tail 2.9, cloth 5.1 | claw 4.8 (f14), arm 7.5 (f38), tail 0, cloth 3.1 |
| death2 | 25.6 / 10.9 / 17.2 | 7.99 / 3.60 / 5.33 | arm 5.8, tail 3.4, cloth 3.9, leg-leg 3.9 | arm 3.9 (2 v), tail 0, cloth 3.0, leg-leg 0 |

- **Remaining clipping comes from the poses themselves, not the weights:**
  - In death, the arm folds across the chest (7.5 cm at f38) and a claw touches the hip (4.8 cm at f14).
  - The crotch flap of the loincloth still dips about 3 cm in the deep crouches.
  - Fixing these would need `_v2` clip copies with adjusted arm keys.
- **The clip files embed the old mesh:** `red_demon_spawnling_anim_v2.glb` and `red_demon_spawnling_walk.glb` still contain the old v2 mesh, so they are kept unchanged. Play their clips on this file instead.
- **Texture:** the texture was not changed, so the hole patches use stretched existing texels.
- **Preview:** `previews/red_demon_spawnling_v2_cleanup.png`, showing before | after for gaps, the tail in run and death2, stretch heat, and the loincloth.
