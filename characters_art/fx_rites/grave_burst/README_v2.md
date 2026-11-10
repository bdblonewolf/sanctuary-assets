# Grave Burst v2: foot-plant fix + ground-burst FX. NOT TESTED in game

## Which "skeleton" was fixed
I searched for a Grave Burst skeleton, emerge or rise clip under `grave_burst*`, commit 728e822, `*skel*`, `*rise*`, `*raise*`, `*emerge*` and `*summon*`, in the repo and the local handoff. None exists. Commit 728e822 is the stone cross only, and Grave Burst is the hero's `grave_burst_slam` (both hands slam the ground) plus the stone cross rising. So the fix is on the hero's slam clip (hero mixamorig skeleton).

## Clip: grave_burst_slam_v2 (30 fps, 55 frames, 1.80 s, in place)
- Files: `grave_burst_slam_v2.glb`, `grave_burst_slam_male_v2.glb`, `grave_burst_slam_female_v2.glb` (byte-identical, the same convention as v1).
- **Impact is still frame 19 (0.633 s).** Frames 0–28 are v1 for the body.
- The right foot steps out for the slam, lifts at f34, and **plants exactly on its frame-0 spot at f44**. f42–f54 settle, and the **last frame equals frame 0** (all 23 channels are bit-identical), so it hands back to idle.
- The legs are re-solved with 2-bone IK (UpLeg, Leg and Foot rotations only). The left foot's ball is pinned for the whole clip; v1 slid it about 19 cm back during the rise.
- Hands, fingers and wrists: copied from v1 frame-for-frame for f0–f42. **In the f42–f54 settle they blend back to their own frame-0 values. That is the only change to the wrist tracks, and it was needed so the clip loops back.** Brian should know.

| foot (authoring rig, m) | frame 0 | v2 last f54 | v2 error | v1 last f42 error |
|---|---|---|---|---|
| LeftFoot | (0.2897, 0.1009, 0.0310) | same | 0.000 cm / 0.00° | 16.7 cm / 17.6° |
| RightFoot | (-0.1934, 0.0907, -0.1056) | same | 0.000 cm / 0.00° | 50.5 cm / 10.8° (in the air) |

On the live hero mesh (player_necromancer, with the loader's hips-Y scale ×1.144): last vs frame 0 is 0.0 cm for both feet (v1: 19.8 cm and 58.9 cm). The left ball drifts up to ~3 cm during the squat because the hero's legs are a different length from the M2M rig (v1: up to 21 cm). Toes ≥ 0 and knees never bend backward. Bone lengths do not change. The RightHand 54°/frame spike at f11 is inherited from v1 (the slam drop).

Previews (clay on player_necromancer, numpy skinning, not the game renderer): `previews/v2_contact_sheet.png`, `previews/v2_frame0_vs_last_feet.png`, `previews/v2_vs_v1.gif` and `.mp4`. Data: `clip_meta_v2.json`, `validation_v2.json`, `previews/hero_rig_check.json`. Scripts: `build_clip_v2.py`, `render_preview_v2.py` and `validate_clip.py` (they refuse to overwrite).

## Ground-burst FX pack (`ground_burst/`): CC0, procedural, original
All are 4×4 sheets with 256 px cells, PREMULTIPLIED alpha, rgb = 0 where alpha = 0, true-black 2 px cell borders, and no black lift.
- `ground_crack_decal_flipbook.png`: flat ground decal. Cracks race out, the soil heaves into chunks, and it ends in a dark crater. NORMAL premultiplied blend, 16 fps, holds the last frame and then fades.
- `dirt_burst_spray_flipbook.png`: camera-facing dirt clods (crisp) and a light soil mist (soft). NORMAL blend, 16 fps.
- `dust_puff_flipbook.png`: low, dark soot-brown dust in thin soft wisps (polished 2026-11-10: darker and thinner than the first pale billow, keep-blacks; whole plume sits inside the cell). NORMAL blend (not additive), 12 fps.
- `rock_debris_atlas.png`: 16 sprites. Cells 0–9 are rocks, 10–12 flat chips, 13–15 pebble clusters. Dark grey-brown stone, crisp 1 px anti-aliased silhouettes, chipped fracture faces.
- `ground_burst_fx.js`: `GraveGroundBurst.create(THREE, scene, {crack, spray, dust, rocks}, opts)` → `burst(pos, {small})`, `update(dt)`, `dispose()`. It throws 34 very small rocks (1.8–6.5 cm, a few 9 cm chips) radially and upward at 1.6–4.2 m/s, with gravity 9.8, spin up to 14 rad/s, up to 2 bounces (0.28 restitution), and a fade at 1.25–1.6 s. Timing: `burst({small:true})` at slam frame 19 (0.633 s) and `burst()` when the stone cross breaks the ground (the engine's existing ~1 s delay).
- **NOT TESTED:** the JS has had `node --check` only. It has never run in three.js or the game. There is no custom GLSL.
- Previews (a Python re-implementation of the JS physics, not three.js): `ground_burst/previews/ground_burst_composite.png`, `ground_burst.gif`, `ground_burst.mp4`.
- Rebuild: `gen_ground_burst_textures.py` and `preview_ground_burst.py`.
