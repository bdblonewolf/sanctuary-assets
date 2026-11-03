# grove_mauler_bear_anim_v2.glb: fixed death

`grove_mauler_bear_anim.glb` (live) is untouched. v2 uses the same mesh (15k tris), the same 29-bone rig, 30 fps, in place.
The only change is a new `death`. The old death rolled the bear onto its back with the front legs folded across the chest, so it read as a melted lump. That clip is kept as `death_old`.

| clip | frames | s | notes |
|---|---|---|---|
| idle | 91 | 3.0 | loop (unchanged) |
| walk | 37 | 1.2 | loop (unchanged) |
| run | 17 | 0.53 | loop (unchanged) |
| attack | 37 | 1.2 | unchanged |
| attack2 | 55 | 1.8 | unchanged |
| hit | 19 | 0.6 | unchanged |
| **death** | 73 | 2.4 | NEW: belly-down collapse (see below). Holds the last pose from f58. |
| death_old | 79 | 2.6 | the previous death, for reference or fallback |

## New death timing (30 fps)
- f0-6: recoil from the killing blow (head jerks up, jaw opens).
- f6-16: stagger forward and down.
- f16-26: front legs buckle. **Chest impact about f26 (0.87 s).**
- f26-38: hindquarters drop and the legs splay back. **Full-body impact f38 (1.27 s)**, a small settle at f41, then the head comes to rest turned slightly to one side.
- f58-72: static hold (the corpse pose).
- The mesh never goes below the ground (min z 0.0). The bear ends lying on its belly with the head down, reading as a dark mound with splayed paws from the top-down camera.
- Sound: a heavy thud at f26, a second body thud at f38. Sound start = impact frame − round(thud offset × 30).

Previews (Cycles): previews_v2/death_v2_side.png (f0-72), previews_v2/death_v2_topdown_game.png (58° elevation, 13 m), previews_v2/death_old_eevee.png (the old death, for comparison).
Built with tools_v2/bear_anim_v2.py (rigwork bear_anim.py plus clip_death_sprawl). Original work.
