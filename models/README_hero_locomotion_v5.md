# hero_locomotion_v5.glb: tight arms, closed fists

- **Mobile file:** `models/hero_locomotion_v5.glb` (via `mobile_compress.sh`, no meshopt or Draco). **Master:** `models/masters/hero_locomotion_v5.glb`. These are new files, and v2, v3 and v4 are unchanged.
- Built from the v4 master. All v4 leg and foot changes are kept. Only rotation keys changed.
- **Fists:** added 30 finger nodes (Left/Right HandIndex/Middle/Ring/Pinky/Thumb 1-3, rest offsets from the warrior body) with constant closed-fist rotation keys at each clip's Hand key times. Curl is about 75/95/60° on segments 1/2/3, and the thumb is wrapped across at 25/35/30°. Applied to all 12 clips.
- **Unarmed walk/run:**
  - Arm: lateral and twist wobble damped to ×0.3 and forward/back swing to ×0.8 around the clip mean, then adducted so the elbows sit about 0.17–0.22 m from the body centre line (v4: 0.26–0.31 m).
  - Elbow bend: run about 83° and walk about 42°. Forearm wobble ×0.5.
  - Wrist: Hand rotation deviation ×0.2 (nearly locked).
  - Forward/back wrist travel: walk 0.51/0.38 → 0.33/0.28 m, run 0.36/0.38 → 0.21/0.17 m.
- **Weapon sets:** arm adducted 6°, arm wobble ×0.6 and swing ×0.85. Forearm and hand are unchanged relative to the arm, so the grip pose is kept. Elbows come in about 1–2.5 cm.
- Unchanged: clip names, existing bone names, key times, frame counts, 30 fps and Hips translation.
