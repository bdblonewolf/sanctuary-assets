# exits_v2: re-planned zone exits (owner msg pt101u)

> "the exits and entrances can be anywhere ... whatever is more natural and flowing better"

Every outdoor zone exit was reviewed. Five zones get a real move (Martsirt, coast, wild, desert, mires). Three partner zones only get the
arrival point (sx/sy) changed. The rest stay where they are, for the reasons below. **Nothing here is applied:** the live world
JSONs, placements, colliders, asset_version, ASSET_MAP and GLB_LIST are untouched. Every file is new. The v1 files from 8b3c52f are kept as they are.

## exits_v3 fix: briarE is WEST of wild, no chart override (engineer feedback on 5e55a62)

**What was wrong in v2.** v2 moved wild's briarE exit to wild's W edge but left briarE untouched. Its return exit was still on briarE's
**W** edge, so you left wild westward and walked in on briarE's west side (the seam needed a 180° turn). On the in-game chart
("The known roads", BFS over the zone list, each link from the nearest edge of the forward exit) that gives
`wild-w->briarE` with a mismatched return, and `briarE-e->duneW` is **bumped** to the cell north of wild. The X1 `chartDir` override that keeps
briarE east papered over this. The override is not the plan: `continent_layout_core_v2.json` already puts briarE (x 1945) **west** of
wild (x 2325), with the whole west road at rot 2 (180°), which the game cannot express.

**Fix.** Mirror left↔right the three wilderness zones on the west road: **briarE, duneW and desert**. They have no buildings or doors, so a
mirror is safe. A 180° rotation would have dragged in the towns lut, market and waste. lut, market and waste are **not** changed.
desert's lut exit stays on its N edge (x 27.4 → 8.6) and lut's S gate still faces it.

| Zone | Exit to | Edge | Exit x,y | You arrive at (sx,sy) |
|---|---|---|---|---|
| wild | briarE | **W** (unchanged from v2) | 0.6, 27.5 | 48.6, 20.4 (briarE E side) |
| briarE | wild | **E** | 50.6, 20.2 | 3.4, 27.5 (wild W side) |
| briarE | duneW | **W** | 2.6, 20.2 | 25.4, 8.2 (duneW E side) |
| duneW | briarE | **E** | 26.8, 8.2 | 5.5, 20.2 |
| duneW | desert | **W** | 1.8, 8.2 | 31.8, 14.2 (desert E side) |
| desert | duneW | **E** | 34.8, 14.2 | 3.8, 8.4 |
| desert | lut | **N** | 8.6, 0.6 | 14, 18.5 (lut S gate) |
| lut | desert | **S** (unchanged) | 14.2, 22.4 | 8.6, 3.4 |

**Chart direction (no override; remove the X1 `chartDir` entry).** The stock nearest-edge rule now gives the correct layout, relative to wild:
wild (0,0) · briarE (−1,0) · duneW (−2,0) · desert (−3,0) · lut (−3,−1) · market (−2,−1) · waste (−1,−1).
- wild **W** edge ↔ briarE **E** edge: briarE is **west** of wild.
- briarE W ↔ duneW E; duneW W ↔ desert E (the road keeps going west).
- desert N ↔ lut S (lut is north of desert).
- lut E ↔ market W; market E ↔ waste W (unchanged live town exits, so this row runs back east, north of the west road).
Every link pairs opposite edges and nothing is bumped (`test_v3.js` simulates the bundle's chart for live, v2 and v3).

**Files (use INSTEAD of the v2 patches for these zones; each v3 patch already contains its zone's v2 ops):**
- `briarE_exits_patch_v3.json`, `duneW_exits_patch_v3.json`, `desert_exits_patch_v3.json`: v2 ops (in the original frame), then `mirror_x`, then `exits_final`.
- `wild_exits_patch_v3.json`, `lut_exits_patch_v3.json`: v2 ops plus the new arrival points only (no mirror).
- `apply_exits_patch.js` is updated with `mirror_x` and `exits_final` support. It still applies the v2 patches unchanged; `test_apply.js` passes on it.
- `mirror_x` does this: tile/solid rows reversed (every per-tile array of length w·h); every point object x → w − x (props, npcs, spawn, lights, nests, `homeX`); `rotY` → −`rotY`; `face-e` ↔ `face-w`. It checks `expect_w`/`expect_h` first.
- Seams: `seams/{briarE__wild,briarE__duneW,desert__duneW,desert__lut}_v3.json` and `seams/seams_index_v3.json`. All four now pair opposite edges at rot 0, with no orientation mismatch. briarE__wild was W|W at 180° in v2 and is now W|E at 0°.
- Terrain: `terrain/{briarE,duneW,desert}_v3.json` (regenerated from the mirrored worlds; the other zones are byte-identical to v2).
- Top-downs: `topdown/{briarE,duneW,desert}_exits_v2_v3.png`.
- `continent_delta_v3.json`; tools `build_v3.py`, `build_v3in.py`, `gen_{terrain,seams,layout}_v3.py`, `finish_seams_v3.py`, `make_topdowns_v3.py`, `delta_v3.py`.
- `test_v3.js` (`node test_v3.js <world dump>`) checks the mirror (tiles, solid, props, spawn), every edge pairing, that arrivals are walkable and next to the return exit, that return and onward exits are reachable, idempotency, and the chart. **ALL OK.**

**Caveats.**
- **Saves:** fog-of-war ("seen" tiles) and saved player positions inside briarE, duneW or desert are in the old frame. Reset them, or mirror them (x → w − x) once on load.
- Any coordinates for these three zones kept outside the world object (quest markers, hard-coded spawns, the X1 chart override) need the same mirror or should be removed.
- **Continent plan (HOLD) divergence:** the west road now matches the plan with rot 0. The Qadren branch does not. In-game, market and waste are east of lut; the plan had them west. At later-grid sizes `gen_layout_v3` reports 7 overlaps (see `continent_delta_v3.json`). The fix is a plan decision and was not made here: re-place the branch and planned nodes, or move the town exits west (which contradicts Hesta's "East of the lamps, the Barrens begin").

## Moved

| Zone | Exit | Old → new (tiles/m) | What changes on the ground | Why it flows better |
|---|---|---|---|---|
| **Martsirt (town)** | → coast ("ACT I") | (81,152) S-edge centre → **(49.6,152.4) SW** | The south gatehouse is still the way out. A new 4 m dirt trail runs from the gate mouth, bears west under the palisade (3+ m off the wall and the map edge), and meets the S edge at x=49.6. The arrival from the coast is now (53.8,150.9). The gate camp (campfire, crates, cart, bedroll) is a stop on the way, not in the way. A new splat (`handoff/game_engineer/exits/martsirt_splat_v2.png`) paints the trail. | You leave through the gate and the road curves off toward the coast, which lies SW on the continent, instead of running dead-straight down the centre line. It lands at the same t≈0.30 as the coast side. |
| **coast (Ashen A0)** | → town | (20.2,1.2) → **(12.5,1.2)** | The A0 dirt path (x 11-13) is extended to the N edge (64 tile edits, 15 solid edits, 6 props nudged, 1 added). | The first walk from the beach camp to town becomes one natural line up the existing path, with no dog-leg east to a bare stub. |
| **wild (P1)** | → briarE | (70.4,27.2) E → **(0.6,27.5) W** | The E-W highway (rows 26-28) now runs west from the crossroads over a 3-wide Bridge causeway across the lake. The dead E branch goes back to grass and the E ring gap is closed. | The Narrow lies W on the continent, so the highway now leads somewhere. |
| **desert (P2)** | → lut | (27.4,5.6) → **(27.4,0.6)** | The road runs through a cut in the N ridge (13 tiles). | The trigger used to sit 5 tiles inside the wall. Now you visibly leave the basin. |
| **mires (P3)** | → sink | (9.2,15.2) → **(0.6,15.5) W** | A plank boardwalk runs over the black water to the W edge. | It replaces a trigger buried in a walled pocket; the Sink sits flush W. |

## Arrival-only (partner zones; tiles and props unchanged)
| Zone | Exit | Change |
|---|---|---|
| briarE | → wild | sx/sy (67.6,27.2) → (3.4,27.5). **Superseded by exits_v3 (section above)** (v2 left briarE's return exit on its W edge). |
| lut | → desert | sx/sy (26.2,8.2) → (27.4,3.4). **Superseded by exits_v3:** (8.6,3.4). |
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
- **`test_apply.js`** (`node test_apply.js <world dump>`): checks that the Martsirt splat path resolves from the repo root, then that applying each patch to the live world reproduces the reviewed after-state exactly (tiles, solid, exits, props).
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
  - `handoff/game_engineer/exits/martsirt_splat_v2.png` (the splat the Martsirt patch points at; it replaces `models/town/ground_v1/martsirt_splat.png`);
  - `topdown/*_exits_before_after.png`;
  - `continent_delta_v2.json`;
  - `tools/` with the v2 generator copies.
- **`handoff/game_engineer/seams/`:** `*_v2.json` and `seams_index_v2.json`.
- **`handoff/game_engineer/borders/`:**
  - `ashen/layout_coast_v2.json` and `martsirt/layout_martsirt_v2.json`;
  - `*/proof_v2/` with the contact sheets and proof_results;
  - `tools/gen_border_v2.py`, `tools/border_styles_v2.json` and `tools/proof_render_v2.py`.
- **`handoff/game_engineer/terrain/`:** `{coast,martsirt,wild,desert,mires}_v2.json`. The partner zones' terrain is unchanged.
