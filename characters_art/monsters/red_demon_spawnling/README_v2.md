# red_demon_spawnling_anim_v2.glb

A copy of `red_demon_spawnling_anim.glb` with new clips added. The original file is unchanged, and the v2 file keeps
all of its original clips (idle, run, attack, hit, death) with the same frame counts.
30 fps, in place (no root motion), lowercase clip names. Same mesh, materials and 52-bone mixamorig skeleton.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| leap_attack | 43 | 1.40 | crouch wind-up 0–12, takeoff 13, apex 15 (hips +0.44 m), land crouched 19, double-claw slam impact **23** (damage frame), recover to idle pose 36–42 |

Notes
- leap_attack is in place: the hips move only up and down (0.0 m horizontal drift). The game should move the actor if it wants a lunge.
- The first and last frames blend to idle frame 0, so it crossfades cleanly.
- The claws dip about 7 cm below the ground plane at the impact frame (23); this is the slam.

Source / licence
- Jump: Mixamo "Pro Melee Axe Pack / unarmed jump" (in place, frames 9–55, time-compressed).
- Claw swipe: Mixamo "Magic Spell Pack / Standing 2H Magic Attack 02" (frames 13–45).
- Both are retargeted onto this rig by script (world-rotation retarget), with hand-keyed spine, head, arm and hip layers on top.
- Mixamo animations are used under Adobe's Mixamo terms (free for use in games, royalty free; the raw files must not be redistributed on their own).

## Update 2026-11-03: spew deaths (face-down)
The file now has 9 clips at 30 fps: death_old 70, hit 22, attack 46, run 22, idle 109, leap_attack 43, attack2 43, death 52, death2 51.
- **leap_attack**: impact f23. **attack2** is the same motion as leap_attack, added so the full set has an attack2 name.
- **death** (52 f): spew f6-22, chest down f34, **face-down impact f36**, hold to f51. Base: Mixamo "two handed sword death (2)", time-warped, plus a hand-keyed spew layer (head and jaw thrust).
- **death2** (51 f): spew f12-30, **face-down impact f38**. Base: Mixamo "standing death forward 01" plus the spew layer.
- **death_old**: the previous death, kept for reference.
- An empty node named `mouth` sits under mixamorig:Head. Attach the spew particle emitter there during the spew frames.
- Sounds: start demon_death_spew_01..03.ogg (thuds at 1.133/1.143/1.030 s) at about frame 36-34=2 for death and 38-34=4 for death2. That is the impact frame minus round(thud×30).
- Previews (Cycles): previews_v2/death_side.png, death2_side.png, death_end_top.png


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `red_demon_spawnling_anim_v2.glb` | `masters/red_demon_spawnling_anim_v2.glb` | 5.29 → 4.30 | 71,448 → 12,989 | 0.43 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.

## Update 2026-11-03: walk clip (new file `red_demon_spawnling_walk.glb`)
The walk is in its **own file**, so nothing live is touched: `red_demon_spawnling_anim_v2.glb`, `red_demon_spawnling_v2.glb` and the other GLBs are unchanged.
The file holds the v1 mesh (`red_demon_spawnling.glb`) and the same 52-bone mixamorig skeleton (same joint names and rest as `red_demon_spawnling_anim_v2.glb`), plus one clip.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| walk | 41 keys (0–40; frame 40 = frame 0, a 40-frame loop) | 1.333 | **left** heel-down f11, toe-off f31; **right** heel-down f31, toe-off f11 (f51) |

- A hunched, predatory prowl: a crouched torso and the claws held forward to match the run. It is **in place**: the hips only bob (0.67–0.73 m) and sway; there is no root motion.
- **Loop distance**, measured from the foot plants (the planted ankle moves back at a constant 0.0338 m per frame): **1.353 m per cycle = 1.01 m/s** on this rig (v1 and anim_v2). On `red_demon_spawnling_v2.glb` the legs are shorter, so the same clip covers **1.292 m per cycle = 0.97 m/s**. Use the value for the mesh in use (at native scale; multiply by any model scale). Moving at that speed gives no foot slide.
- Feet: the planted foot is pinned (heel, then a toe roll from f24/f44), and the swing foot clears the floor. On v2 the stance feet sit 0–2 cm above y = 0. On v1 they sit 1–4 cm into it, the same v1/v2 offset as the existing idle and run.
- Plays on both meshes: the channels are rotations for all bones plus the Hips translation only (no other bone translations), so it binds to `red_demon_spawnling_v2.glb` as well. This was checked by grafting it onto the v2 file.
- Hips are centred at the idle/run position (mean z 0.08), so run ⇄ walk crossfades don't jump.
- Preview: `previews/red_demon_spawnling_walk.png` (v1 and v2, side and 3/4 views, with foot-height and ankle-track plots).

Source / licence: Mixamo "Pro Magic Pack / Crouch Walk Forward" (root motion, 34-frame cycle), retargeted onto this rig by script (world-rotation retarget). It was then made in place, re-timed to 40 frames, stride ×0.85, foot-pinned with two-bone leg IK, and given hand-set spine, head and arm layers. Used under Adobe's Mixamo terms (free for use in games; the raw files must not be redistributed).

Master vs mobile: `masters/red_demon_spawnling_walk.glb` is the uncompressed master. `red_demon_spawnling_walk.glb` is the mobile copy, made by `mobile_compress.sh` (2,173 → 1,666 keyframes, max joint drift 0.32 mm, plant frames f11/f31 within 0.03 mm). **No meshopt or Draco.** The two files are about the same size (4.06 MB) because the mesh dominates and the clip is short.
