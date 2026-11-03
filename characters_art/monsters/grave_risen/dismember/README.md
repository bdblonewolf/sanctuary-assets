# grave_risen - dismemberment set

Source: `characters_art/monsters/grave_risen/grave_risen.glb (mesh only, no clips in source; 52-joint mixamorig rig - drive with any mixamorig clip set by bone name)`. Live GLBs are untouched; these are new files.

## Files (master vs mobile)
| Mobile copy (load this) | Master (uncompressed, full rate) | What |
|---|---|---|
| `grave_risen_dismember.glb` | `masters/grave_risen_dismember.glb` | Full body, split into separately-hideable **skinned** parts + stump/severed gore caps (caps hidden by default) |
| `grave_risen_half.glb` | `masters/grave_risen_half.glb` | Half-body crawler (upper body + waist stump cap), own clip set |
| `grave_risen_severed.glb` | `masters/grave_risen_severed.glb` | Static severed pieces (bind pose) each with its own severed cap |

Mobile copies: `tools/mobile_compress.sh` (resample + prune + dedup + static-track strip). **No meshopt/Draco**; extensionsUsed is empty. Max drift vs master < 1.1 mm; frame counts identical.
`grave_risen_dismember.json` = part/cut/cap table; `grave_risen_half_clips.json` = half clip frame counts.

## Skinned parts (`grave_risen_dismember.glb`)
All parts share one skeleton (mixamorig). Hide a part's mesh(es) and show its stump cap to "remove" it.
| Mesh | Part | Follows bone | Tris |
|---|---|---|---|
| `grave_risen_head` | head | mixamorig:Neck | 1226 |
| `grave_risen_arm_l` | arm_l | mixamorig:LeftArm | 1137 |
| `grave_risen_arm_r` | arm_r | mixamorig:RightArm | 1109 |
| `grave_risen_upper_torso` | upper_torso | mixamorig:Spine1 | 2290 |
| `grave_risen_lower_body` | lower_body | mixamorig:Hips | 3103 |
| `grave_risen_leg_l` | leg_l | mixamorig:LeftUpLeg | 1690 |
| `grave_risen_leg_r` | leg_r | mixamorig:RightUpLeg | 1408 |

## Cuts / caps
| Cut | Stump cap (show on body) | Severed cap (on loose piece) | Radius m |
|---|---|---|---|
| head | `grave_risen_cap_head` on mixamorig:Spine2 | `grave_risen_sevcap_head` on mixamorig:Neck | 0.075 |
| arm_l | `grave_risen_cap_arm_l` on mixamorig:LeftShoulder | `grave_risen_sevcap_arm_l` on mixamorig:LeftArm | 0.08 |
| arm_r | `grave_risen_cap_arm_r` on mixamorig:RightShoulder | `grave_risen_sevcap_arm_r` on mixamorig:RightArm | 0.08 |
| leg_l | `grave_risen_cap_leg_l` on mixamorig:Hips | `grave_risen_sevcap_leg_l` on mixamorig:LeftUpLeg | 0.11 |
| leg_r | `grave_risen_cap_leg_r` on mixamorig:Hips | `grave_risen_sevcap_leg_r` on mixamorig:RightUpLeg | 0.11 |
| waist | `grave_risen_cap_waist` on mixamorig:Spine | `grave_risen_sevcap_waist` on mixamorig:Spine1 | 0.17 |

## Severed pieces (`grave_risen_severed.glb`, static, bind space)
Engine: on sever, `piece.matrix = bone.matrixWorld * skeleton.boneInverses[i]` for the bone below, then toss/ragdoll it.
| Piece | Bone at sever | Tris |
|---|---|---|
| `grave_risen_sev_head` | mixamorig:Neck | 1545 |
| `grave_risen_sev_arm_l` | mixamorig:LeftArm | 1450 |
| `grave_risen_sev_arm_r` | mixamorig:RightArm | 1428 |
| `grave_risen_sev_leg_l` | mixamorig:LeftUpLeg | 2003 |
| `grave_risen_sev_leg_r` | mixamorig:RightUpLeg | 1727 |
| `grave_risen_sev_legs` | mixamorig:Hips | 6663 |

## Half-body clips (`grave_risen_half.glb`) - 30 fps, in place
| Clip | Frames | Loop | Events |
|---|---|---|---|
| `crawl` | 60 | yes | left hand plants f0, right f30 |
| `idle_half` | 60 | yes | - |
| `crawl_swipe` | 41 | no | wind-up f0-13, **impact f18**, recover f26-40 |
| `hit_half` | 21 | no | peak recoil f3-4 |
| `death_half` | 51 | no | rears f0-10, **face hits ground ~f30**, head turn to f40 |

- Half-body height (idle_half): **0.54 m**; tris 6224.
- Crawl speed (planted-hand slide, in place): **~0.29 m/s** - move the root at this speed while `crawl` plays.

## Sound (audio/sfx/impact/limb_sever_0[1-3].ogg)
Each file = chop at 0 s, limb hits the ground at 0.448 / 0.440 / 0.331 s.
Play at the sever frame (the killing blow's impact). Land the severed piece **13 / 13 / 10 frames** later (30 fps) to sync with the thud.
