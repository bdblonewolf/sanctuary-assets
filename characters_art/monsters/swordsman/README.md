# swordsman_anim — animated swordsman (full clip set)

New animated version of the existing `swordsman.glb` (which is **untouched**). Same mesh, skeleton (mixamorig, 52 bones) and weapon (swordsman_sword, skinned to **RightHand**).

## Files
| file | what |
|---|---|
| `swordsman_anim.glb` | **mobile copy — load this in game** (1.10 MB). Made with `tools/mobile_compress.sh` (resample, prune, dedup, static tracks dropped; no meshopt/Draco, no extensions); textures unchanged. |
| `masters/swordsman_anim.glb` | **uncompressed master** (1.89 MB) — edit/re-export from this, never from the mobile copy. Max bone drift mobile vs master is under 2 mm, frame counts identical. |
| `swordsman_anim_clips.json` | per-clip sources, frames, duration, mode, source travel |
| `preview_swordsman_anim.png` | contact sheet of key poses |
| `src/rt4.py`, `src/sw.json` | retarget script + clip config (`blender -b --python rt4.py -- swordsman.glb out.glb sw.json`) |

## Specs
- **Height:** 1.64 m (body, idle pose; A-pose source ~1.75 m)
- **Orientation:** forward glTF **+Z**, Y up, feet on y=0
- **Clips:** 30 fps, **in place** (hips travel removed) except `death`, which keeps root travel
- **Walk speed at 1x:** **1.45 m/s** (source travel 1.597 m per 1.100 s cycle)
- **Run speed at 1x:** **4.01 m/s** (source travel 2.806 m per 0.700 s cycle)

## Clips (frames are 0-based)
| clip | frames | sec | loop | impact / release | source — notes |
|---|---|---|---|---|---|
| idle | 109 | 3.60 | yes | – | sword and shield idle |
| walk | 34 | 1.10 | yes | – | sword and shield walk |
| run | 22 | 0.70 | yes | – | sword and shield run |
| attack1 | 46 | 1.50 | no | **18** | sword and shield slash — overhead slash: wind-up to f15, blade impact ~f18 (tip peak 14.9 m/s) |
| attack2 | 48 | 1.57 | no | **22** | sword and shield slash (3) — low horizontal swing, impact ~f22 |
| hit | 22 | 0.70 | no | – | sword and shield impact |
| death | 70 | 2.30 | no | – | sword and shield death — falls; root travel kept, body ends ~1.22 m from origin |

## Source / licence
- Mesh/skeleton: the existing Sanctuary `swordsman.glb` (models3d).
- Animation: Mixamo "Sword and Shield Pack" (+ death "sword and shield death") from Adobe Mixamo (royalty-free for personal/commercial projects; ship baked into the game asset, do not redistribute the raw FBX files). Retargeted by world-rotation transfer with bone-direction alignment, hips height scaled to the model, multi-part clips joined with a 4-frame crossfade.
