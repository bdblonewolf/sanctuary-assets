# red_demon_spawnling_anim_v3.glb (clip copies with clipping fixes)

New file only. `red_demon_spawnling_v2.glb`, `red_demon_spawnling_anim_v2.glb`, `red_demon_spawnling_walk.glb` and their READMEs are unchanged.

- Mobile: `red_demon_spawnling_anim_v3.glb` (2.1 MB, 1024 JPEG textures, no meshopt/Draco). Master: `masters/red_demon_spawnling_anim_v3.glb` (5.5 MB).
- Contains the cleaned v2 mesh (with the mouth node, 55 nodes, 52 joints) and all clips, so it can be loaded on its own.
- Clips (30 fps, in place, same names and frame counts as before): death_old 70, hit 22, attack 46, run 22, idle 109, leap_attack 43, attack2 43, death 52, death2 51, walk 41. leap_attack = attack2 (same fixes).
- Event frames unchanged: leap_attack/attack2 f23, death f36, death2 f38, walk foot plants f11/f31.
- Walk: the rotations are identical to `red_demon_spawnling_walk.glb`. Walk also gets the same constant bone-length translation tracks as the anim_v2 clips. Without them, walk played with the v2 mesh's own rest lengths (left upper arm 0.483 m vs 0.244 m in every other clip), so the left arm changed length between walk and the other clips.
- Changes: only arm (and a few leg) rotation keys were re-keyed, per frame, to pull limbs out of the body. Re-keyed bones: run/attack/attack2/death/death2/death_old arms; death, death2, death_old some leg keys. hit, idle, walk untouched (no clipping).
- No weight change: a cloth-only weight tweak was tried and made clipping worse, so it was dropped. The mesh weights are identical to `red_demon_spawnling_v2.glb`.

## Clipping, worst depth in cm (before -> after)
VISIBLE = can be seen by a player. HIDDEN = crease/seam that already touches in the bind pose (under 2 cm apart at rest: armpit, loincloth fold).

| clip | pair | visible | hidden |
|---|---|---|---|
| attack | arm into torso | 7.8 (f24) -> 1.5 | 0.9 -> 0.9 |
| attack2 / leap_attack | arm into torso | 5.8 (f26) -> 0.8 | 2.0 -> 1.0 |
| attack2 / leap_attack | leg into leg | 1.3 -> 1.0 | |
| attack2 / leap_attack | loincloth into legs | 0 | 0.7 -> 0.4 |
| run | arm into torso | 5.8 (f10) -> 1.8 | 0 |
| run | loincloth into legs | 3.0 (f19) -> 3.0 | 2.1 -> 2.1 |
| death | arm across chest | 7.7 (f32) -> 5.9 (f33); f37-51 about 3 | 1.5 -> 1.4 |
| death | claw into hip (f14-16) | 0.7 -> 0.0 | |
| death | loincloth into legs | 3.1 (f49) -> 3.1 | 2.1 -> 2.1 |
| death | tail into legs | 2.1 (f43) -> 2.1 | |
| death2 | arm into torso | 4.6 (f11) -> 1.0 | 1.3 -> 1.0 |
| death2 | loincloth into legs | 3.0 (f20) -> 2.7 | 1.8 -> 1.8 |
| death_old | arm into torso | 7.7 (f58) -> 1.4 | 1.5 -> 1.1 |
| death_old | loincloth into legs | 2.5 (f45) -> 0.1 | 1.8 -> 1.0 |
| hit, idle, walk | all | 0 | 0 |

## Left over
- death f33-36: the right arm still crosses the chest/neck by about 6 cm (about 3 cm for f37-51). No rotation up to 50 degrees on the arm and shoulder fixed it without breaking the pose.
- Loincloth into legs about 3 cm in run, death and death2 deep crouches. Fixing it would need cloth bones or weight work; leg keys would make the feet slide.
- Hand drift from re-keying (cm, max): run 9.7, attack 12.3 (7.0 at f23), attack2 9.4, death 24 (right hand, while falling), death2 13 (0.2 at the f38 event), death_old 19. Feet stay planted in walk and run.

Preview: `previews/red_demon_spawnling_v2_cleanup2.png` (before | after, 0 / 60 / 300 degrees, worst frames).
