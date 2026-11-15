# Grove Mauler Bear v3b (add-only; v3 files untouched) - NOT TESTED IN GAME

Load: `grove_mauler_bear_v3b.glb` (one glb, base colour).
Dark Brown: swap the baseColor image of material `grove_mauler_bear_v3b_mat` with
`grove_mauler_bear_v3b_darkbrown_col.webp` (2048x2048, same UVs). The loader must decode WebP.

Changes vs v3
- Mouth: real opening cut on the lip line and driven by the existing `jaw` bone (no new bones). Adds a dark mouth interior, 26 low-poly teeth (canines included), and a tongue.
- `bear_attack_bite`: same timing (1.0 s, impact f15, bleed). The jaw opens to 31 deg on the lunge and snaps shut at impact.
- The other 10 clips have keyframes identical to v3. Note: the old clips already rotated the jaw (attack/attack2/hit/death 12-16 deg, run 7 deg, idle 0.8-3 deg), so the mouth now visibly opens in them too.
- Feet: hind toes lifted, plus 8 mesh claws on the hind toes. Hind-foot texture repainted as fur (the glossy black toes, the grey heel smear, and the misplaced painted claws are gone). Green/pink tint removed from the front claws.
- Fur: 12 broken stick/arrow-shaft stubs that were part of the body mesh are flattened into the surface, and their texture is refilled.
- Dark Brown is darker (mean luminance 0.094 -> 0.078; blacks kept).

16,408 tris (v3: 15,000). 5 materials (body textured + 4 factor-only).

Wiring
- `monsters_3d.json` entry `bear` currently points to `corrupted_phimn_feral_lod15k_walk.glb`. The engineer must wire this file in. Do NOT edit `monsters_3d.json`.

Attack clips
- `bear_attack_heavy_claw_left`: 1.40 s, impact f20
- `bear_attack_light_claw_right`: 0.70 s, impact f9
- `bear_attack_bite`: 1.00 s, impact f15, bleed flag; jaw opens 31 degrees

Notes
- The old clips now show teeth when the jaw moves.
- Idle shows a thin tooth line.
- NOT TESTED in game.
