# evil_rat — plague rat (swarm)

`evil_rat.glb` is a single skinned mesh with one PBR material (baked baseColor, roughness, normal and emissive at 1024²). Backface culling is on.

**Look:** near-black greasy fur with mangy bald patches and sores, sickly green-tinged corruption veins (disease), raw pink tail/feet and glowing red eyes.

## Files
| file | what |
|---|---|
| `evil_rat.glb` | **mobile copy — load this in game** (1.20 MB). `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions) + textures re-encoded to JPEG q88 (still 1024², one material, no duplicate textures). Max bone drift vs master < 2 mm, identical frame counts. |
| `masters/evil_rat.glb` | **uncompressed master** (3.29 MB, PNG textures) — edit/re-export from this, never from the mobile copy. |
| `evil_rat_info.json` | machine-readable specs: tris, size, speeds, clip frames, impact frames |
| `preview_evil_rat.png` | contact sheet (3/4 view + key frames of walk/attack/attack2/hit/death) |
| `src/` | build config + Blender scripts (`blender -b --python wb_build*.py -- <config>.json`) |

## Specs
- **Tris:** 4,204
- **Size:** 0.32 m tall, about 0.97 m long including tail (giant rat)
- **Orientation:** forward is glTF **+Z**, Y is up, feet sit on y=0
- **Clips:** 30 fps, **in place** (no root motion)
- **Walk speed at 1x:** **0.1 m/s**
- **Run speed at 1x:** **0.49 m/s**
- Speeds are foot stride ÷ cycle time; raise the playback rate if the game moves it faster.

## Clips (frames 0-based)
| clip | frames | loop | impact frame | notes |
|---|---|---|---|---|
| idle | 72 | yes | – |  |
| walk | 41 | yes | – |  |
| run | 16 | yes | – |  |
| attack | 21 | no | **13** | bite |
| attack2 | 31 | no | **24** | lunge disease bite: jump forward blending into the bite |
| hit | 16 | no | – | head/neck jerk back |
| death | 33 | no | – | rolls over |

Impact = frame where the head reaches furthest forward (bite/gore contact).

## Source / licence
- **Base mesh and animation:** Quaternius "Rat" via Poly Pizza (https://poly.pizza/m/iltq5bVNaV), CC0 1.0.
- **Changes made here (original work):** smooth-shaded and quad-merged (no subdivision), added glowing eye spheres skinned to Head, new baked corrupted textures, clips retimed 24→30 fps; hit is a new keyed flinch; attack2 (lunge) blends the jump into the bite.
