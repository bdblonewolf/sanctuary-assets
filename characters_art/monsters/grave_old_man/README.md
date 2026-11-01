# Grave Old Man, v2

Starter monster for Sanctuary family `12_zombie_basic_v2`. Near-bare emaciated old corpse with a narrow loin rag; no element hue tint.

- **File:** `grave_old_man.glb` (1.33 MB). glTF binary, no extensions, Y up, metres, feet at y=0, height 1.78 m, mixamorig skeleton plus loin_F / loin_B swing bones.
- **Triangles:** 7,288 total (body 5,544 + loin cord and flaps, hair cards).
- **Textures:** skin 1024, loin 512 (alpha), hair 256x512 (alpha). Embedded PNG.
- **Validator:** Khronos gltf-validator `errors 0, warnings 3, infos 2` (all warnings NODE_SKINNED_MESH_NON_ROOT).

## What changed from v1
- Same low-poly rebind as the Rag Zombie (seam weld, decimate 0.25, 14 mm short-edge collapse, smoothed weights).
- Thinned toward the bones (arms ~80%, shins ~84%, chest ~90%) rather than using the MPFB skinny body; the skinny shape transfer failed the stretch test (death 3.2–3.5x).
- Pale grey-green skin with age spots, rot, veins, mud and rain grime; sunken eyes, gaunt cheeks, broken teeth; balding scalp with thin grey hair cards.
- The modesty undergarment is gone: only a waist band and a narrow crotch strip remain under a real loin rag (waist cord, a 16 x 36 cm front flap and a 30 cm back flap with torn alpha edges), on swing bones.
- Attack is the one-arm Mixamo punch.

## Sources and licences
| Part | Source | Licence |
|---|---|---|
| Body mesh, rig, base weights | MakeHuman / MPFB2 male_regular (https://github.com/makehumancommunity/mpfb2, LICENSE.ASSETS.md) | CC0 1.0 |
| Animations | Adobe Mixamo motion data (no Mixamo characters), from sanctuary/assets3d/mixamo/: `Pro Melee Axe Pack/unarmed idle.fbx`, `Pro Melee Axe Pack/unarmed walk forward.fbx`, `Pro Longbow Pack/standing melee punch.fbx` (one-arm attack), `Pro Melee Axe Pack/standing react large gut.fbx`, `singles/Dying.fbx`. Hunch, head and arm offsets plus slowed timing come from `_pipeline/zpost.py` | Adobe Mixamo terms (used in games; not CC). Same precedent as the skeletons |
| Burlap/rag detail | Poly Haven "Hessian 230" diffuse 1k, https://polyhaven.com/a/hessian_230 (colormass, Rico Cilliers), mixed into the procedural bake | CC0 1.0 |
| Mud and grime | Poly Haven "Brown Mud 02" diffuse 1k, https://polyhaven.com/a/brown_mud_02, box-projected below 0.6 m on skin and rags | CC0 1.0 |
| Rotted face, mottled skin, rain streaks, teeth, scalp, rag alpha and hair strands | Procedural, baked in Blender by `_pipeline/zombie_build2.py` | Project-owned / CC0 |

## Stretch test
```
PER {'attack_grave_old_man': 2.95, 'death_grave_old_man': 2.75, 'hit_grave_old_man': 2.72, 'idle_grave_old_man': 1.96, 'walk_grave_old_man': 1.98}
STRETCH worst=2.95 at attack_grave_old_man f10 grave_old_man_body edge(378, 389) z1.45
```
All clips are under 3x.

## Previews
previews/grave_old_man_front.png, previews/grave_old_man_side.png, previews/grave_old_man_attack.png (attack frame 11). Lineup: ../lineup_v2.png.

## Rebuild
`_pipeline/run2.sh grave_old_man work/spec2_oldman.json work/z_oldman2h2.json` then `_pipeline/fin.sh grave_old_man 11`. v1 files are in work/v1/.
