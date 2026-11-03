# grave_old_man - dismemberment set

Source: `characters_art/monsters/grave_old_man/grave_old_man.glb (live v1 mesh; clips carried over)`. Live GLBs are untouched; these are new files.

## Files (master vs mobile)
| Mobile copy (load this) | Master (uncompressed, full rate) | What |
|---|---|---|
| `grave_old_man_dismember.glb` | `masters/grave_old_man_dismember.glb` | Full body, split into separately-hideable **skinned** parts + stump/severed gore caps (caps hidden by default) |
| `grave_old_man_half.glb` | `masters/grave_old_man_half.glb` | Half-body crawler (upper body + waist stump cap), own clip set |
| `grave_old_man_severed.glb` | `masters/grave_old_man_severed.glb` | Static severed pieces (bind pose) each with its own severed cap |

Mobile copies: `tools/mobile_compress.sh` (resample + prune + dedup + static-track strip). **No meshopt/Draco**; extensionsUsed is empty. Max drift vs master < 1.1 mm; frame counts identical.
`grave_old_man_dismember.json` = part/cut/cap table; `grave_old_man_half_clips.json` = half clip frame counts.

## Skinned parts (`grave_old_man_dismember.glb`)
All parts share one skeleton (mixamorig). Hide a part's mesh(es) and show its stump cap to "remove" it.
| Mesh | Part | Follows bone | Tris |
|---|---|---|---|
| `grave_old_man_head` | head | mixamorig:Neck | 1702 |
| `grave_old_man_arm_l` | arm_l | mixamorig:LeftArm | 904 |
| `grave_old_man_arm_r` | arm_r | mixamorig:RightArm | 910 |
| `grave_old_man_upper_torso` | upper_torso | mixamorig:Spine1 | 412 |
| `grave_old_man_lower_body` | lower_body | mixamorig:Hips | 961 |
| `grave_old_man_leg_l` | leg_l | mixamorig:LeftUpLeg | 635 |
| `grave_old_man_leg_r` | leg_r | mixamorig:RightUpLeg | 630 |

## Cuts / caps
| Cut | Stump cap (show on body) | Severed cap (on loose piece) | Radius m |
|---|---|---|---|
| head | `grave_old_man_cap_head` on mixamorig:Spine2 | `grave_old_man_sevcap_head` on mixamorig:Neck | 0.075 |
| arm_l | `grave_old_man_cap_arm_l` on mixamorig:LeftShoulder | `grave_old_man_sevcap_arm_l` on mixamorig:LeftArm | 0.0696 |
| arm_r | `grave_old_man_cap_arm_r` on mixamorig:RightShoulder | `grave_old_man_sevcap_arm_r` on mixamorig:RightArm | 0.0692 |
| leg_l | `grave_old_man_cap_leg_l` on mixamorig:Hips | `grave_old_man_sevcap_leg_l` on mixamorig:LeftUpLeg | 0.11 |
| leg_r | `grave_old_man_cap_leg_r` on mixamorig:Hips | `grave_old_man_sevcap_leg_r` on mixamorig:RightUpLeg | 0.11 |
| waist | `grave_old_man_cap_waist` on mixamorig:Spine | `grave_old_man_sevcap_waist` on mixamorig:Spine1 | 0.1478 |

## Severed pieces (`grave_old_man_severed.glb`, static, bind space)
Engine: on sever, `piece.matrix = bone.matrixWorld * skeleton.boneInverses[i]` for the bone below, then toss/ragdoll it.
| Piece | Bone at sever | Tris |
|---|---|---|
| `grave_old_man_sev_head` | mixamorig:Neck | 2021 |
| `grave_old_man_sev_arm_l` | mixamorig:LeftArm | 1217 |
| `grave_old_man_sev_arm_r` | mixamorig:RightArm | 1229 |
| `grave_old_man_sev_leg_l` | mixamorig:LeftUpLeg | 948 |
| `grave_old_man_sev_leg_r` | mixamorig:RightUpLeg | 949 |
| `grave_old_man_sev_legs` | mixamorig:Hips | 2688 |

## Half-body clips (`grave_old_man_half.glb`) - 30 fps, in place
| Clip | Frames | Loop | Events |
|---|---|---|---|
| `crawl` | 60 | yes | left hand plants f0, right f30 |
| `idle_half` | 60 | yes | - |
| `crawl_swipe` | 41 | no | wind-up f0-13, **impact f18**, recover f26-40 |
| `hit_half` | 21 | no | peak recoil f3-4 |
| `death_half` | 51 | no | rears f0-10, **face hits ground ~f30**, head turn to f40 |

- Half-body height (idle_half): **0.51 m**; tris 4390.
- Crawl speed (planted-hand slide, in place): **~0.32 m/s** - move the root at this speed while `crawl` plays.

## Sound (audio/sfx/impact/limb_sever_0[1-3].ogg)
Each file = chop at 0 s, limb hits the ground at 0.448 / 0.440 / 0.331 s.
Play at the sever frame (the killing blow's impact). Land the severed piece **13 / 13 / 10 frames** later (30 fps) to sync with the thud.
