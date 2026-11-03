# exits_v2: re-planned zone exits (owner msg pt101u)

> "the exits and entrances can be anywhere ... whatever is more natural and flowing better"

Every outdoor zone exit was reviewed. Five zones get a real move (Martsirt, coast, wild, desert, mires). Three partner zones only get the
arrival point (sx/sy) changed. The rest stay where they are, for the reasons below. **Nothing here is applied:** the live world
JSONs, placements, colliders, asset_version, ASSET_MAP and GLB_LIST are untouched. Every file is new. The v1 files from 8b3c52f are kept as they are.

## Moved

| Zone | Exit | Old → new (tiles/m) | What changes on the ground | Why it flows better |
|---|---|---|---|---|
| **Martsirt (town)** | → coast ("ACT I") | (81,152) S-edge centre → **(49.6,152.4) SW** | The south gatehouse is still the way out. A new 4 m dirt trail runs from the gate mouth, bears west under the palisade (3+ m off the wall and the map edge), and meets the S edge at x=49.6. The arrival from the coast is now (53.8,150.9). The gate camp (campfire, crates, cart, bedroll) is a stop on the way, not in the way. A new splat (`martsirt_splat_v2.png`) paints the trail. | You leave through the gate and the road curves off toward the coast, which lies SW on the continent, instead of running dead-straight down the centre line. It lands at the same t≈0.30 as the coast side. |
| **coast (Ashen A0)** | → town | (20.2,1.2) → **(12.5,1.2)** | The A0 dirt path (x 11-13) is extended to the N edge (64 tile edits, 15 solid edits, 6 props nudged, 1 added). | The first walk from the beach camp to town becomes one natural line up the existing path, with no dog-leg east to a bare stub. |
| **wild (P1)** | → briarE | (70.4,27.2) E → **(0.6,27.5) W** | The E-W highway (rows 26-28) now runs west from the crossroads over a 3-wide Bridge causeway across the lake. The dead E branch goes back to grass and the E ring gap is closed. | The Narrow lies W on the continent, so the highway now leads somewhere. |
| **desert (P2)** | → lut | (27.4,5.6) → **(27.4,0.6)** | The road runs through a cut in the N ridge (13 tiles). | The trigger used to sit 5 tiles inside the wall. Now you visibly leave the basin. |
| **mires (P3)** | → sink | (9.2,15.2) → **(0.6,15.5) W** | A plank boardwalk runs over the black water to the W edge. | It replaces a trigger buried in a walled pocket; the Sink sits flush W. |

## Arrival-only (partner zones; tiles and props unchanged)
| Zone | Exit | Change |
|---|---|---|
| briarE | → wild | sx/sy (67.6,27.2) → (3.4,27.5) |
| lut | → desert | sx/sy (26.2,8.2) → (27.4,3.4) |
| sink | → mires | sx/sy (11.4,15.4) → (3.4,15.5) |
| coast | → town | sx/sy stays (19.8,31.6). This is a legacy 2D-town value; the live 3D Martsirt uses `arrive.coast` from the Martsirt patch. |

## Kept (reviewed, not moved)
| Zone(s) | Why it stays |
|---|---|
| Martsirt → wild (N, 76.2,1.4) | The N road already leaves through the N gate on its own line. Alternative B (a W postern at the mill-lane end) is flagged only in `martsirt_exits_patch.json` and is not the default, because it would need a palisade change. |
| coast → bastion (E 40.4,14.2) | **P4 deferred.** The E side below y≈20 is open sea on the 42x112 coast. Revisit when the coast grid grows. |
| coast ↔ flotsam, flotsam ↔ hollow, hollow, isle | Boat and dock links. They are interior or dock exits by design, so they have no edge seam. |
| bastion, bluffs, ridge, ascent, crypts, chasm, iron, gaol, weald | The mountain chain. The exits already sit where the climb roads reach the edges. **The 4 steep roads (bastion 48°, mires 38.8°, ascent 32.5°, iron 32.2°) stay deferred** (default). |
| briarE, duneW, lut, market, waste | The desert highway runs straight E-W, and each exit is where it crosses the edge. |
| sink | Its exit is the climb out of the sinkhole. Only the arrival changes (above). |

## Apply order (when the engineer builds it)
1. `applyAshenPatch` (A0) first. The coast patch expects the post-Ashen coast.
2. **Martsirt and coast together, in the same release** (each `requires` the other). Martsirt is applied by hand: set `exits[to=coast]` and `arrive.coast`, append `roads_add` to `placements.header.v2.roads`, and swap the splat.
3. wild + briarE, desert + lut, mires + sink: apply each pair together using `apply_exits_patch.js` (`applyExitsPatch(world, patch)`). This is idempotent through `world.exitsPatch` and checks the old values before writing.
4. When the zones are rebuilt, use the `_v2` border layouts, seams and terrain. They are inert until then.

## Checks (all pass)
- **Martsirt:**
  - The trail's clearance is 1.32 m to solid (0.65 m in the gate mouth) and 3.63 m to the gate-camp props.
  - No trail samples are blocked.
  - The spawn reaches the new exit, the arrival, every exit and every NPC (Wolchen, Ysara, Ilyra, Quill, Bram).
- **coast (A0):**
  - The 56 new road tiles are clear and reachable.
  - The A0 spawn reaches every exit.
  - All 74 of 75 Ashen props that were reachable before are still reachable, with 0 lost (1 was already unreachable before).
  - Wynn is reachable, and 0 intro-line samples are blocked.
- **wild, desert, mires:**
  - All exits, NPCs and key props are reachable before and after.
  - No new road tile is blocked or unreachable.
  - The partner arrival point is clear and reachable.
- **`test_apply.js`:** applying each patch to the live world reproduces the reviewed after-state exactly (tiles, solid, exits, props).
- **Borders v2** (ring skip at the new exits):
  - coast: N props 8→5, pass12 at walk_t 6.5, NW endcap scaled 0.54.
  - Martsirt: S props 52→49, pass12 at walk_t 106.4-118.4.
  - **Proof renders after v2:**
    - coast: 44 views, void 0.00 %, dark gap ≤0.10 % (same as v1).
    - Martsirt: 36 views, void ≤0.15 %. The 0.15 % is a horizon sliver seen straight through the open pass at the new EXIT view, where the neighbour zone is not rendered. Gap is 0.00 %.
- **Seams v2:**
  - Regenerated: coast__martsirt, briarE__wild, desert__lut and mires__sink (these two were `interior_exit` in v1 and are now `edge_seam`), plus bastion__coast (scenery copy changed with the coast ring).
  - Seam heights are consistent.
  - The other 16 pairs are byte-identical to v1.
- **Continent:** `gen_layout_v2` with only P4 still a proposal gives 0 overlaps. The coast branch shifts −13.5 m (later grid) and the desert chain +1.8 m.

## Files
- **`handoff/game_engineer/exits/`:**
  - `*_exits_patch.json` for martsirt, coast, wild, desert, mires, briarE, lut and sink;
  - `apply_exits_patch.js` and `test_apply.js`;
  - `martsirt_splat_v2.png`;
  - `topdown/*_exits_before_after.png`;
  - `continent_delta_v2.json`;
  - `tools/` with the v2 generator copies.
- **`handoff/game_engineer/seams/`:** `*_v2.json` and `seams_index_v2.json`.
- **`handoff/game_engineer/borders/`:**
  - `ashen/layout_coast_v2.json` and `martsirt/layout_martsirt_v2.json`;
  - `*/proof_v2/` with the contact sheets and proof_results;
  - `tools/gen_border_v2.py`, `tools/border_styles_v2.json` and `tools/proof_render_v2.py`.
- **`handoff/game_engineer/terrain/`:** `{coast,martsirt,wild,desert,mires}_v2.json`. The partner zones' terrain is unchanged.
