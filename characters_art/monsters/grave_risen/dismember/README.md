# grave_risen - dismemberment set

Source: `characters_art/monsters/grave_risen/grave_risen.glb` (mesh only, no clips in source; 52-joint mixamorig rig). Live GLBs are untouched.
Full-body clips (idle/walk/attack/hit/death) are retargeted from `characters_art/monsters/rag_zombie/masters/rag_zombie_v2.glb` (same mixamorig bone names) and baked into both `grave_risen_dismember.glb` and `grave_risen_full.glb`.

## Files (master vs mobile)
| Mobile copy (load this) | Master (uncompressed, full rate) | What |
|---|---|---|
| `grave_risen_dismember.glb` | `masters/grave_risen_dismember.glb` | Full body, split into separately-hideable **skinned** parts + stump/severed gore caps (caps hidden by default), with the full-body clips below |
| `grave_risen_full.glb` | `masters/grave_risen_full.glb` | Full body, single unsplit mesh (same mesh + rig as live `grave_risen.glb`) with the full-body clips below |
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

## Full-body clips (`grave_risen_dismember.glb` and `grave_risen_full.glb`) - 30 fps, in place
The 5 clips have the same frame counts and event frames in both files. Node names, meshes and the half-body clips are unchanged.
| Clip | Frames | Loop | Events |
|---|---|---|---|
| `idle` | 71 (f0-70) | yes | - |
| `walk` | 70 (f0-69) | yes | left foot plants f20 (planted to ~f48), right foot plants f48 (planted to ~f21) |
| `attack` | 31 (f0-30) | no | wind-up f0-4, left-arm swing, **impact f9** (hand at full reach and top speed), follow-through f10-14, recover f15-30 (near idle pose by f22) |
| `hit` | 45 (f0-44) | no | **contact f5** (fastest head snap), doubled-over **peak recoil f14**, recover f15-44 |
| `death` | 82 (f0-81) | no | stagger sway f0-30, drops to the knees at about f30, pitches forward, **body impact f54** (head and chest land f53-54), lies still to f81 |

- Sources (rag_zombie_v2 master): idle/walk/attack/hit = the zombie set (attack = Mixamo one-arm melee swing, hit = "standing react large gut"); death = the f225983 slow death (README_v2 `death`, impact f54). `death2`, `death_old` and `spit` are not included.
- Retarget: world-space bone rotations copied by mixamorig name, every frame (linear keys). Only `mixamorig:Hips` has translation (scaled by hip height 0.9831).
- Grounding: the hips height is offset so the lowest vertex sits on y=0. It is constant per clip for idle/attack/hit (+0.107/+0.105/+0.106 m) and per frame for walk and death, so the feet and the fallen body stay on the floor.
- In place: hips XZ drift is sway only (walk ~0.10 m side / 0.08 m fore-aft; death leans 0.50 m forward as the body falls, same as the source). Move the root yourself while `walk` plays.
- Mobile copies: `tools/mobile_compress.sh` (no meshopt/Draco, extensionsUsed empty). `verify_clips.mjs` master vs mobile: frame counts identical, worst drift 0.70 mm, 0 mm at attack f9, hit f5/f14 and death f30/f54.
- Preview: `previews/full_clips.png` (key frames per clip, 3/4 and side views).
- Sound: knee thud at death f30 and body thud at f54 (start the sound at the impact frame minus round(thud_s*30)); swing whoosh landing on attack f9.

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
