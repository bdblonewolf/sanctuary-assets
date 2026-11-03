# evil_deer — corrupted stag

`evil_deer.glb` is a single skinned mesh with one PBR material (baked baseColor, roughness, normal and emissive at 1024²). Backface culling is on.

**Look:** dark, matted hide with mange patches and open sores, faint dark-red corruption veins, blood-stained antlers and ember-red eyes.

## Files
| file | what |
|---|---|
| `evil_deer.glb` | **mobile copy — load this in game** (1.32 MB). `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions) + textures re-encoded to JPEG q88 (still 1024², one material, no duplicate textures). Max bone drift vs master < 2 mm, identical frame counts. |
| `masters/evil_deer.glb` | **uncompressed master** (3.08 MB, PNG textures) — edit/re-export from this, never from the mobile copy. |
| `evil_deer_info.json` | machine-readable specs: tris, size, speeds, clip frames, impact frames |
| `preview_evil_deer.png` | contact sheet (3/4 view + key frames of walk/attack/attack2/hit/death) |
| `src/` | build config + Blender scripts (`blender -b --python wb_build*.py -- <config>.json`) |

## Specs
- **Tris:** 11,428
- **Size:** 1.87 m tall including antlers, about 1.66 m long
- **Orientation:** forward is glTF **+Z**, Y is up, feet sit on y=0
- **Clips:** 30 fps, **in place** (no root motion)
- **Walk speed at 1x:** **0.48 m/s**
- **Run speed at 1x:** **1.8 m/s**
- Speeds are foot stride ÷ cycle time; raise the playback rate if the game moves it faster.

## Clips (frames 0-based)
| clip | frames | loop | impact frame | notes |
|---|---|---|---|---|
| idle | 101 | yes | – |  |
| walk | 36 | yes | – |  |
| run | 16 | yes | – | gallop |
| attack | 24 | no | **11** | antler gore: head drops and hooks forward |
| attack2 | 50 | no | **36** | charge: 2 gallop cycles blending into the gore (gore lands at the impact frame) |
| hit | 14 | no | – | flinch (Idle_HitReact_Left) |
| death | 33 | no | – | collapses onto its side |

Impact = frame where the head reaches furthest forward (bite/gore contact).

## Source / licence
- **Base mesh and animation:** Quaternius, *Ultimate Animated Animal Pack*, "Stag" (CC0 1.0, https://quaternius.com/packs/ultimateanimatedanimals.html).
- **Changes made here (original work):** slimmed torso and head, subdivided then decimated, antlers re-skinned to the head bone, new baked corrupted textures, clips retimed 24→30 fps and renamed; attack2 (charge) blends 2 gallop cycles into the antler gore.
