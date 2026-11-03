# evil_rabbit — corrupted hare

`evil_rabbit.glb` is a single skinned mesh with one PBR material (baked baseColor, roughness, normal and emissive at 1024²). Backface culling is on.

**Look:** dark brown matted fur with raw mange patches and sores, dark-red corruption veins and glowing red eyes.

## Files
| file | what |
|---|---|
| `evil_rabbit.glb` | **mobile copy — load this in game** (1.19 MB). `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions) + textures re-encoded to JPEG q88 (still 1024², one material, no duplicate textures). Max bone drift vs master < 2 mm, identical frame counts. |
| `masters/evil_rabbit.glb` | **uncompressed master** (3.29 MB, PNG textures) — edit/re-export from this, never from the mobile copy. |
| `evil_rabbit_info.json` | machine-readable specs: tris, size, speeds, clip frames, impact frames |
| `preview_evil_rabbit.png` | contact sheet (3/4 view + key frames of walk/attack/attack2/hit/death) |
| `src/` | build config + Blender scripts (`blender -b --python wb_build*.py -- <config>.json`) |

## Specs
- **Tris:** 5,456
- **Size:** 0.54 m tall in rest pose with ears up (lower when sitting), about 0.68 m long
- **Orientation:** forward is glTF **+Z**, Y is up, feet sit on y=0
- **Clips:** 30 fps, **in place** (no root motion)
- **Walk speed at 1x:** **0.62 m/s**
- **Run speed at 1x:** **0.95 m/s**
- Speeds are foot stride ÷ cycle time; raise the playback rate if the game moves it faster.

## Clips (frames 0-based)
| clip | frames | loop | impact frame | notes |
|---|---|---|---|---|
| idle | 81 | yes | – | sitting, breathing/ear twitch |
| walk | 33 | yes | – | slow bound |
| run | 21 | yes | – | bound |
| attack | 22 | no | **8** | bite: neck darts forward and down (low, ankle height) |
| attack2 | 36 | no | **20** | leap bite: leap (f0–17) blending into the bite |
| hit | 16 | no | – | head jerks back |
| death | 26 | no | – | falls onto its side (Dying.001) |

Impact = frame where the head reaches furthest forward (bite/gore contact).

## Source / licence
- **Base mesh and animation:** "Rabbit" by CDmir (collab. TinyWorlds), OpenGameArt (https://opengameart.org/content/rabbit-0), CC0.
- **Changes made here (original work):** IK rig baked to the 22 deform bones, fur-shell/whisker card mesh dropped, subdivided then decimated, glowing eye spheres added, new baked corrupted textures, clips retimed 24→30 fps; walk is the bounding run slowed 1.6x, idle is a seamless loop cut from Sitting (src f196–260); attack and hit are new keyed clips; attack2 (leap bite) blends the jump into the bite.
