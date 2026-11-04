# hero_locomotion_v4.glb: tighter lower legs, level feet

- **Mobile file:** `models/hero_locomotion_v4.glb` (via `mobile_compress.sh`, no meshopt or Draco). **Master:** `models/masters/hero_locomotion_v4.glb`. These are new files, and v2 and v3 are unchanged.
- Built from the v2 master. Only rotation keys changed: Left/Right UpLeg, Leg, Foot and ToeBase in all 12 clips.
  - **UpLeg:** 3° inward (same as v3). Knees sit about 2.3 cm closer to the midline.
  - **Leg (shin):** 1.4° back toward the outside, instead of v3's full 3° compensation, so each ankle ends up about 1.1 cm further in. Mean ankle width is about 2.1–2.4 cm narrower than v2 (unarmed walk 0.300 → 0.279 m, run 0.223 → 0.200 m).
  - **Foot:** sideways roll removed (soles level, 0° roll in every frame; v2 averaged 3–15° and peaked at 10–60°). Toe-out/heading reduced to 30% of v2. Foot pitch is kept.
  - **ToeBase:** flap halved (×0.5, as in v3).
- Unchanged: clip names, bones, key times, frame counts, 30 fps and Hips/root translation. No mesh or materials in this file.
