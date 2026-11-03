# archer_anim — animated archer (full clip set)

New animated version of the existing `archer.glb` (which is **untouched**). Same mesh, skeleton (mixamorig, 52 bones) and weapon (archer_bow, skinned to **LeftHand** (spawn the arrow at LeftHand)).

## Files
| file | what |
|---|---|
| `archer_anim.glb` | **mobile copy — load this in game** (1.56 MB). Made with `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions); 2048² textures in the master, resized to 1024² in the mobile copy. |
| `masters/archer_anim.glb` | **uncompressed master** (4.54 MB) — edit/re-export from this, never from the mobile copy. Max bone drift mobile vs master is under 2 mm, frame counts identical. |
| `archer_anim_clips.json` | per-clip sources, frames, duration, mode, source travel |
| `preview_archer_anim.png` | contact sheet of key poses |
| `src/rt4.py`, `src/ar.json` | retarget script + clip config (`blender -b --python rt4.py -- archer.glb out.glb ar.json`) |

## Specs
- **Height:** 1.73 m (body, idle pose; A-pose source ~1.75 m)
- **Orientation:** forward glTF **+Z**, Y up, feet on y=0
- **Clips:** 30 fps, **in place** (hips travel removed) except `death`, which keeps root travel
- **Walk speed at 1x:** **1.12 m/s** (source travel 1.342 m per 1.200 s cycle)
- **Run speed at 1x:** **3.51 m/s** (source travel 3.044 m per 0.867 s cycle)

## Clips (frames are 0-based)
| clip | frames | sec | loop | impact / release | source — notes |
|---|---|---|---|---|---|
| idle | 154 | 5.10 | yes | – | standing idle 01 |
| walk | 37 | 1.20 | yes | – | standing walk forward |
| run | 27 | 0.87 | yes | – | standing run forward |
| attack1 | 49 | 1.60 | no | **33** (release) | standing draw arrow, standing aim recoil — quick shot: draw arrow, nock ~f17, full draw f31, **release f33**, recoil |
| attack2 | 82 | 2.70 | no | **66** (release) | standing draw arrow, standing aim overdraw, standing aim recoil — power shot: draw, full draw f30, overdraw hold to f62, **release f66**, recoil |
| hit | 39 | 1.27 | no | – | standing react small from front |
| death | 93 | 3.07 | no | – | standing death backward 01 — falls backward; root travel kept (~1.09 m) |

## Source / licence
- Mesh/skeleton: the existing Sanctuary `archer.glb` (models3d).
- Animation: Mixamo "Pro Longbow Pack" from Adobe Mixamo (royalty-free for personal/commercial projects; ship baked into the game asset, do not redistribute the raw FBX files). Retargeted by world-rotation transfer with bone-direction alignment, hips height scaled to the model, multi-part clips joined with a 4-frame crossfade.
