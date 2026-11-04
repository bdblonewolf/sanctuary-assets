# hero_locomotion_v2.glb: clear walk vs run for the hero

- **Mobile file:** `models/hero_locomotion_v2.glb` (188 KB). **Master:** `models/masters/hero_locomotion_v2.glb` (212 KB).
- These are new files. `knight_anim_v10b(_c).glb` and the manifest are unchanged.
- **Contents:** 12 clips on the same `mixamorig:` rig as `knight_anim_v10b_c.glb` (27 joints, no mesh). All clips are 30 fps, in place (Hips x/z = 0) and loop seamlessly (last key = first key).
- **Phase:** in every clip the **left heel strikes at normalized time 0**, so walk↔run and set↔set crossfades stay in phase.
- **Upper body:** each set keeps its own weapon-hold upper body. Arms, spine, head and weapon hand come from that set's existing walk/run clip, re-timed to the new cycle. Legs and Hips are newly solved.

## Clips (measured on the knight rig, game-style playback: Hips x/z zeroed, Hips y × 0.98)

| clip | frames (keys) | sec | m / cycle | m/s | L heel-down / toe-off | R heel-down / toe-off | duty | flight frames | max foot slip | trunk lean |
|---|---|---|---|---|---|---|---|---|---|---|
| unarmed_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 0.0 mm | upright |
| ss_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 0.1 mm | as source |
| axe_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 0.0 mm | as source |
| gs_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 0.1 mm | as source |
| bow_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 0.0 mm | as source |
| magic_walk_v2 | 30 (31) | 1.000 | 1.45 | 1.45 | 0 / 19 | 15 / 4 | 0.63 | 0 | 3.5 mm (1 frame) | as source |
| unarmed_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 (2 per step) | 2.3 mm | 16° |
| ss_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 | 2.3 mm | 34° |
| axe_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 | 2.3 mm | 20° |
| gs_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 | 2.3 mm | 30° |
| bow_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 | 2.3 mm | 45° |
| magic_run_v2 | 20 (21) | 0.667 | 2.95 | 4.425 | 0 / 8 | 10 / 18 | 0.40 | 4 | 2.3 mm | 18° |

- **Walk:** about 0.72 m steps, 120 steps/min, double support, low bob, no flight.
- **Run:** about 1.48 m strides, 180 steps/min, forward lean, big arm swing (unarmed swing × 1.35), and a real flight phase (both feet off for 2 frames per step).
- **Contact:** heel-down is the first frame a foot is within 8 mm of the ground; toe-off is the first frame it is clear.

## Natural speed on each player body (same clip, body rest pose + clip rotations, as the game plays it)

Stride scales with leg proportions. Set `timeScale = moveSpeed / natural` per body, or use the knight values and accept a little slip.

| body | walk m/s | run m/s | slip per frame (walk / run) |
|---|---|---|---|
| knight rig | 1.45 | 4.43 | ≤0.1 / 2.3 mm |
| warrior | ~1.62 | ~4.92 | 2–8 / 7–8 mm |
| archer | ~1.32 | ~4.19 | 2–9 / 0.4–2 mm |
| elementalist | ~1.42 | ~4.50 | 2–11 / 0.6–2.5 mm |
| necromancer | ~1.69 | ~5.16 | 3–5 / 5–8 mm |

The body slip comes from proportion mismatch and is the same for any knight clip.

## Notes for the engineer

- `maskHero` builds the `__lo` lower-body masks only for names matching `/_run$|_walk$/`. **`*_walk_v2` / `*_run_v2` do not match.** Extend the regex (e.g. `/_(run|walk)(_v2)?$/`) or add the masks yourself.
- **The `gs_run` source clip in knight_anim_v10b plays time-reversed** (its feet moonwalk). `gs_run_v2` was built from it played backwards and is correct forward.
- Track names are `mixamorig:*`. They retarget the same way as knight_anim_v10b_c (YD rename, Hips x/z zeroed, Hips y × hipsRatio).
- Preview: `art_2d/sanctuary_art/monsters/models3d/previews/hero_locomotion_v2.png` (side view of every clip with ghosted frames).

## Master vs mobile

| | master | mobile |
|---|---|---|
| file | models/masters/hero_locomotion_v2.glb | models/hero_locomotion_v2.glb |
| size | 211,992 B | 187,972 B |
| keyframes | 8,736 | 7,066 |
| clips / frames | 12, 31 or 21 keys | identical |
| worst joint drift (verify_clips) | – | 0.32 mm |
| glTF validator | 0 errors, 0 warnings | 0 errors, 0 warnings |

## Pipeline and source

- **Source:** rotations come from the existing Mixamo-derived clips in `knight_anim_v10b.glb` and `hero_extra` (gs_walk), the same licence as those clips. No new third-party data.
- **Synthesis:** take each set's upper body (re-timed to the new cycle) and generate the legs from ss_run (runs) or the set's own walk (walks). Then:
  - plant the feet at exactly the cycle speed (contact anchors) and solve the legs with two-bone IK;
  - lock the stance-foot yaw;
  - bake Hips x/z to 0.
- **Mobile copy:** made with `tools/mobile_compress.sh`: resample 1e-4, prune, dedup, drop constant scale and non-Hips translation tracks. No meshopt or Draco.
