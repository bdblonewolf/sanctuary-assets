# Rag Zombie (Risen Dead), v2

Starter monster for Sanctuary family `12_zombie_basic_v2`. Realistic Diablo 1/2 rot look; no element hue tint.

- **File:** `rag_zombie.glb` (2.62 MB). glTF binary, no extensions, Y up, metres, feet at y=0, height 1.78 m, mixamorig skeleton plus skirt_F / skirt_B swing bones.
- **Triangles:** 6,154 total (body 5,544 + tunic, skirt, hair cards).
- **Textures:** skin 1024, tunic 1024 (alpha), skirt 1024 (alpha), hair 256x512 (alpha). Embedded PNG. Alpha uses MASK so it works with three.js depth sorting.
- **Validator:** Khronos gltf-validator `errors 0, warnings 4, infos 2`. Warnings are all NODE_SKINNED_MESH_NON_ROOT (harmless; same as the skeletons).

## What changed from v1
- Low-poly rebind: the MPFB2 body is welded at UV seams, decimated (0.25, X-symmetric), Spine1 weights folded into Spine/Spine2, edges under 14 mm collapsed, weights Laplacian-smoothed 16 iterations with hierarchical pruning. Welding first means no seam cracks open when skinned.
- Face: eyes sunk 7 mm with shrunken eyeballs, gaunt cheeks, cheek, nose and mouth dents; baked dark sockets, nose cavity, dark gums and a dirty broken teeth band; patchy scalp and clumped dark hair cards.
- Skin: mottled grey-green with rot patches, veins, wounds, rain streaks and mud to the shins.
- Rags: a loose torn tunic shell (ragged hem, sleeves and holes) and a separate knee-length torn skirt ring on its own swing bones (skirt_F / skirt_B, parented to Hips, follow-and-damp baked into every clip), alpha-cut edges.
- Attack is now a one-arm swing (Mixamo standing melee punch) instead of the two-arm magic slam.

## Sources and licences
| Part | Source | Licence |
|---|---|---|
| Body mesh, mixamorig-compatible rig, base weights | MakeHuman / MPFB2 male_regular (https://github.com/makehumancommunity/mpfb2, LICENSE.ASSETS.md) | CC0 1.0 |
| Animations | Adobe Mixamo motion data (no Mixamo characters), from sanctuary/assets3d/mixamo/: `Pro Melee Axe Pack/unarmed idle.fbx`, `Pro Melee Axe Pack/unarmed walk forward.fbx`, `Pro Longbow Pack/standing melee punch.fbx` (one-arm attack), `Pro Melee Axe Pack/standing react large gut.fbx`, `singles/Dying.fbx`. Hunch, head and arm offsets plus slowed timing come from `_pipeline/zpost.py` | Adobe Mixamo terms (used in games; not CC). Same precedent as the skeletons |
| Burlap/rag detail | Poly Haven "Hessian 230" diffuse 1k, https://polyhaven.com/a/hessian_230 (colormass, Rico Cilliers), mixed into the procedural bake | CC0 1.0 |
| Mud and grime | Poly Haven "Brown Mud 02" diffuse 1k, https://polyhaven.com/a/brown_mud_02, box-projected below 0.6 m on skin and rags | CC0 1.0 |
| Rotted face, mottled skin, rain streaks, teeth, scalp, rag alpha and hair strands | Procedural, baked in Blender by `_pipeline/zombie_build2.py` | Project-owned / CC0 |

Rejected candidate (not used): OpenGameArt "Male City Zombie" by Rikindle3D, CC0, https://opengameart.org/content/male-city-zombie-ready-for-use-in-game-engines (modern city clothes and odd UVs; wrong look for Sanctuary).

## Clips (30 fps, in place)
idle, walk, attack, hit, death (sources above). Timing scaled by zpost (idle x1.3, walk x1.7 slower).

## Stretch test (worst edge-length ratio vs bind, every clip)
```
PER {'attack_rag_zombie': 2.79, 'death_rag_zombie': 2.72, 'hit_rag_zombie': 2.71, 'idle_rag_zombie': 1.96, 'walk_rag_zombie': 2.18}
STRETCH worst=2.79 at attack_rag_zombie f8 rag_zombie_body edge(390, 405) z1.47
```
All clips are under 3x.

## Previews
previews/rag_zombie_front.png, previews/rag_zombie_side.png, previews/rag_zombie_attack.png (attack frame 11). Lineup: ../lineup_v2.png.

## Rebuild
`_pipeline/run2.sh rag_zombie work/spec2_ragz.json work/z_ragzh2.json` then `_pipeline/fin.sh rag_zombie 11` (from _pipeline). v1 files are kept in work/v1/.

## Known limits
- Skin still has some MPFB smoothness up close; the rot is texture plus small dents, not a sculpt.
- The tunic is an offset of the body surface on the torso, so only the hem, sleeves and skirt swing.
