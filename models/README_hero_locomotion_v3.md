# hero_locomotion_v3.glb: knee/foot fix

- **Mobile file:** `models/hero_locomotion_v3.glb`. **Master:** `models/masters/hero_locomotion_v3.glb`. These are new files, and v2 is unchanged.
- Made from the v2 master. Only the animation changed: rotation keys on Left/Right UpLeg, Leg, Foot and ToeBase in all 12 clips.
  - **Hip adduction:** 3° in the Hips frame (thighs rotate inward). The shin counter-rotates 3° so the ankles stay put and the knees move about 1.5–2 cm toward the midline, over the feet.
  - **Foot:** world orientation is kept, so contact and planting are unchanged.
  - **Toe:** ToeBase rotation away from rest is scaled by **0.5**, which halves the toe flap.
- Unchanged: clip names, frame counts, timing, fps, bones, Hips root motion, translations and mesh (there is none in this file).
- Mobile copy made with `mobile_compress.sh` (no meshopt and no Draco).
