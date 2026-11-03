# axeman_anim — animated axeman (full clip set)

New animated version of the existing `axeman.glb` (which is **untouched**). Same mesh, skeleton (mixamorig, 52 bones) and weapon (axeman_axe, skinned to **RightHand**).

## Files
| file | what |
|---|---|
| `axeman_anim.glb` | **mobile copy — load this in game** (1.36 MB). Made with `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions); textures unchanged. |
| `masters/axeman_anim.glb` | **uncompressed master** (2.26 MB) — edit/re-export from this, never from the mobile copy. Max bone drift mobile vs master is under 2 mm, frame counts identical. |
| `axeman_anim_clips.json` | per-clip sources, frames, duration, mode, source travel |
| `preview_axeman_anim.png` | contact sheet of key poses |
| `src/rt4.py`, `src/ax.json` | retarget script + clip config (`blender -b --python rt4.py -- axeman.glb out.glb ax.json`) |

## Specs
- **Height:** 1.68 m (body, idle pose; A-pose source ~1.75 m)
- **Orientation:** forward glTF **+Z**, Y up, feet on y=0
- **Clips:** 30 fps, **in place** (hips travel removed) except `death`, which keeps root travel
- **Walk speed at 1x:** **1.01 m/s** (source travel 1.350 m per 1.333 s cycle)
- **Run speed at 1x:** **2.46 m/s** (source travel 1.803 m per 0.733 s cycle)

## Clips (frames are 0-based)
| clip | frames | sec | loop | impact / release | source — notes |
|---|---|---|---|---|---|
| idle | 55 | 1.80 | yes | – | standing idle |
| walk | 41 | 1.33 | yes | – | standing walk forward |
| run | 23 | 0.73 | yes | – | standing run forward |
| attack1 | 73 | 2.40 | no | **31** | standing melee attack horizontal — horizontal swing, impact ~f31 |
| attack2 | 69 | 2.27 | no | **24** | standing melee attack downward — downward chop: axe raised by f18, fast down f20–24, impact ~f24 |
| hit | 45 | 1.47 | no | – | standing react large gut |
| death | 133 | 4.40 | no | – | Dying — collapses; root travel kept (~0.33 m) |

## Source / licence
- Mesh/skeleton: the existing Sanctuary `axeman.glb` (models3d).
- Animation: Mixamo "Pro Melee Axe Pack" (death = Mixamo single "Dying") from Adobe Mixamo (royalty-free for personal/commercial projects; ship baked into the game asset, do not redistribute the raw FBX files). Retargeted by world-rotation transfer with bone-direction alignment, hips height scaled to the model, multi-part clips joined with a 4-frame crossfade.
