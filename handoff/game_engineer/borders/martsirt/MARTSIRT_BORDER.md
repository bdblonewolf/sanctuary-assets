# Martsirt (martsirt_v2_2) border to true bounds 162x154 (PROPOSAL, not live)

No placements, world JSON, colliders or live code were touched. **World props moved: 0.**

## Layout
- `border_kit/out/layout_martsirt.json`: 62 kit pieces (town + forest style), 206 border props (121 collidable), 42,572 kit tris. Within the phone budget of ≤45k.
- Frame: tile metres. Placements in `placements.json` are relative to origin [81, 76]; the layout uses tile coords (add the origin to placements).
- Seam spans: N 70.2–82.2 ↔ Briarwood (exit 76.2, 1.4) and S 75–87 ↔ Ashen Coast (exit 81, 152).
- Props avoid roads (`header.v2.roads`), exits ±4 m, and anything within 1.2 m of existing placements.

## Loader changes (engineer)
1. In the town loader (after the palisade/placements), add the kit pieces and props from `layout_martsirt.json`, using the same clone/instance/merge rules as the coast.
2. In moodTown, set the clear colour to the fog colour 0x10131A (now 0x07080C), so whatever sits beyond fog-far reads as fog, not black.
3. On the N and S seams, copy neighbour scenery per `seams/martsirt__wild.json` and `seams/coast__martsirt.json`.

## Proof (same camera rig, 8 views x d14/d40 x portrait/landscape)
- Files: `proof/before_*.png` and `proof/after_*.png`, contact sheets `proof/contact_*_d40.png`, numbers in `proof/proof_results.json`.

| | views | mean black void | max |
|---|---|---|---|
| before (no ring) | 32 | 55.5 % | 83.9 % (corners, landscape) |
| after | 32 | 0.003 % | 0.06 % (N d14, looking through the open pass12 seam; the neighbour copy fills it) |

## Terrain
`terrain/martsirt.json`: Martsirt stays flat at 0 m, so no building y-offsets are needed. Briarwood does the climb (0 → 6 m base) and the coast stays at 0.
