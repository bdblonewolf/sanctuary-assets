# grave_risen_full_v2.glb (clip copies with clipping fixes)

New file only. `grave_risen_full.glb`, `grave_risen_v2.glb` and their READMEs are unchanged.

- Mobile: `dismember/grave_risen_full_v2.glb` (1.7 MB, 1024 JPEG textures, no meshopt/Draco). Master: `dismember/masters/grave_risen_full_v2.glb` (3.6 MB).
- Contains the cleaned v2 mesh (`grave_risen_v2.glb`, 52 joints) and the five clips from `grave_risen_full.glb`.
- Clips (30 fps, in place, same names and frame counts): idle 71, walk 70, attack 31, hit 45, death 82.
- Event frames unchanged: attack f9, hit f5/f14, death f54, walk foot plants f20/f48.
- Changes: arm rotation keys were re-keyed per frame in idle, walk, attack, hit and death. Some leg keys were also re-keyed in death. Leg keys in attack and hit were tried and dropped because they made the feet slide (18 cm).
- No weight change: a robe-only weight tweak was tried and made clipping worse, so it was dropped. The weights are identical to `grave_risen_v2.glb`.

## Clipping, worst depth in cm (before -> after)
VISIBLE = can be seen by a player (all legs-through-robe counts as visible). HIDDEN = crease that already touches in the bind pose (under 2 cm apart at rest).

| clip | pair | visible | hidden |
|---|---|---|---|
| attack | arm into torso | 7.4 (f7) -> 0.0 | |
| attack | robe into legs | 6.1 (f8) -> 6.1 | |
| hit | arm into torso | 7.7 (f4) -> 0.0 | |
| hit | robe into legs | 3.0 (f33) -> 3.0 | |
| walk | arm into torso | 7.5 (f53) -> 0.9 | |
| walk | robe into legs | 4.1 (f41) -> 4.1 | 0.8 -> 0.8 |
| walk | legs through robe | 4.5 (f6) -> 4.5 (2 hem vertices at the right knee) | |
| idle | arm into torso | 3.2 (f32) -> 2.6 | |
| idle | robe into legs | 1.3 -> 1.3 | |
| idle | legs through robe | 3.1 (f53) -> 3.1 | |
| death | arm into torso | 8.0 (f39) -> 3.2 | |
| death | robe into knees | 6.8 (f34) -> 3.8 | 1.5 -> 1.7 |
| death | legs through robe | 2.0 (f52) -> 1.3 | |

## Left over
- The robe still folds into the legs (attack 6 cm, walk 4 cm, hit 3 cm), and the knee pokes through the hem in walk f6 (2 vertices). Fixing these needs robe bones or a new robe weight approach. Re-keying the legs made the feet slide.
- Hand drift from re-keying (cm, max): idle 6.6, walk 13.8, attack 16.6, hit 4.2 (2.7 at f5, 1.5 at f14), death foot 22.6 while falling (1.1 at f54).

Preview: `../previews/grave_risen_v2_cleanup2.png` (before | after, 0 / 60 / 300 degrees, worst frames).
