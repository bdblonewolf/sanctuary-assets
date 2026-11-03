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
