# rag_zombie - dismemberment set

Source: `characters_art/monsters/rag_zombie/rag_zombie.glb (live v1 mesh; clips attack/death/hit/idle/walk carried over)`. Live GLBs are untouched; these are new files.

## Files (master vs mobile)
| Mobile copy (load this) | Master (uncompressed, full rate) | What |
|---|---|---|
| `rag_zombie_dismember.glb` | `masters/rag_zombie_dismember.glb` | Full body, split into separately-hideable **skinned** parts + stump/severed gore caps (caps hidden by default) |
| `rag_zombie_half.glb` | `masters/rag_zombie_half.glb` | Half-body crawler (upper body + waist stump cap), own clip set |
| `rag_zombie_severed.glb` | `masters/rag_zombie_severed.glb` | Static severed pieces (bind pose) each with its own severed cap |

Mobile copies: `tools/mobile_compress.sh` (resample + prune + dedup + static-track strip). **No meshopt/Draco**; extensionsUsed is empty. Max drift vs master < 1.1 mm; frame counts identical.
`rag_zombie_dismember.json` = part/cut/cap table; `rag_zombie_half_clips.json` = half clip frame counts.

## Skinned parts (`rag_zombie_dismember.glb`)
All parts share one skeleton (mixamorig). Hide a part's mesh(es) and show its stump cap to "remove" it.
| Mesh | Part | Follows bone | Tris |
|---|---|---|---|
| `rag_zombie_head` | head | mixamorig:Neck | 1854 |
| `rag_zombie_arm_l` | arm_l | mixamorig:LeftArm | 1039 |
| `rag_zombie_arm_r` | arm_r | mixamorig:RightArm | 1064 |
| `rag_zombie_upper_torso` | upper_torso | mixamorig:Spine1 | 789 |
| `rag_zombie_lower_body` | lower_body | mixamorig:Hips | 1271 |
| `rag_zombie_leg_l` | leg_l | mixamorig:LeftUpLeg | 637 |
| `rag_zombie_leg_r` | leg_r | mixamorig:RightUpLeg | 634 |

## Cuts / caps
| Cut | Stump cap (show on body) | Severed cap (on loose piece) | Radius m |
|---|---|---|---|
| head | `rag_zombie_cap_head` on mixamorig:Spine2 | `rag_zombie_sevcap_head` on mixamorig:Neck | 0.075 |
| arm_l | `rag_zombie_cap_arm_l` on mixamorig:LeftShoulder | `rag_zombie_sevcap_arm_l` on mixamorig:LeftArm | 0.08 |
| arm_r | `rag_zombie_cap_arm_r` on mixamorig:RightShoulder | `rag_zombie_sevcap_arm_r` on mixamorig:RightArm | 0.08 |
| leg_l | `rag_zombie_cap_leg_l` on mixamorig:Hips | `rag_zombie_sevcap_leg_l` on mixamorig:LeftUpLeg | 0.105 |
| leg_r | `rag_zombie_cap_leg_r` on mixamorig:Hips | `rag_zombie_sevcap_leg_r` on mixamorig:RightUpLeg | 0.11 |
| waist | `rag_zombie_cap_waist` on mixamorig:Spine | `rag_zombie_sevcap_waist` on mixamorig:Spine1 | 0.1528 |

## Severed pieces (`rag_zombie_severed.glb`, static, bind space)
Engine: on sever, `piece.matrix = bone.matrixWorld * skeleton.boneInverses[i]` for the bone below, then toss/ragdoll it.
| Piece | Bone at sever | Tris |
|---|---|---|
| `rag_zombie_sev_head` | mixamorig:Neck | 2173 |
| `rag_zombie_sev_arm_l` | mixamorig:LeftArm | 1352 |
| `rag_zombie_sev_arm_r` | mixamorig:RightArm | 1383 |
| `rag_zombie_sev_leg_l` | mixamorig:LeftUpLeg | 950 |
| `rag_zombie_sev_leg_r` | mixamorig:RightUpLeg | 953 |
| `rag_zombie_sev_legs` | mixamorig:Hips | 3004 |

## Half-body clips (`rag_zombie_half.glb`) - 30 fps, in place
| Clip | Frames | Loop | Events |
|---|---|---|---|
| `crawl` | 60 | yes | left hand plants f0, right f30 |
| `idle_half` | 60 | yes | - |
| `crawl_swipe` | 41 | no | wind-up f0-13, **impact f18**, recover f26-40 |
| `hit_half` | 21 | no | peak recoil f3-4 |
| `death_half` | 51 | no | rears f0-10, **face hits ground ~f30**, head turn to f40 |

- Half-body height (idle_half): **0.549 m**; tris 5208.
- Crawl speed (planted-hand slide, in place): **~0.32 m/s** - move the root at this speed while `crawl` plays.

## Sound (audio/sfx/impact/limb_sever_0[1-3].ogg)
Each file = chop at 0 s, limb hits the ground at 0.448 / 0.440 / 0.331 s.
Play at the sever frame (the killing blow's impact). Land the severed piece **13 / 13 / 10 frames** later (30 fps) to sync with the thud.

## v2 clips (2026-11-04, add-only)
`rag_zombie_dismember_v2.glb` = the dismember parts with the live `rag_zombie_v2.glb` clips at 30 fps: idle 2.333, walk 2.300, attack 1.000, hit 1.467, death 2.700, death2 2.667 s. Bind pose unchanged.
`rag_zombie_full_v2.glb` = the live v2 model with the same six clips (spit and death_old left out). Masters in `masters/`.
