# ENV_ADDED: environment GLBs added on Nov 1, 2026

This commit adds **47 GLBs (42,800,652 B, 40.8 MB)**. All of them were missing from the repo, and none overwrites an existing file. The source is the environment artist's working tree (`sanctuary_env/outdoor/glb_v5_maps`). Every other environment GLB was compared by git blob hash against the whole repo; see the skipped list below.

The gothic v6 trees were pushed in an earlier commit, under `models/outdoor/trees_gothic_v6/`.

## Border kit: `models/outdoor/v5_maps/border/` (36 new files)

How these relate to the live pieces:
- They are **not** end caps, height steps or newer revisions of anything live. All 48 `seacliff_endcap_*` and 16 `seacliff_step_*` files are already live.
- They are the **standalone backdrop mound pieces**: `border_{peak,shelf,dune}_{a,b,c}_v5_{season}`. Each has a 1.0 m normalised footprint, its base at y=0 and a 3 cm skirt, and is meant to be scaled uniformly x8 to x40 and rotated freely about Y.
- The live `border/border_kit_v5.json`, which is byte-identical to ours, already describes them under `border_pieces`, but the GLBs were never in the folder.
- They are the latest revision (12I, Nov 1). Shelves have crowned, multi-summit tops and no open side; dune_b has a sinuous crest; peaks were re-gridded. Each is 4.5k tris or fewer.

Same-named live files: all **148** existing `border/` files (beaches, seacliff straights, corners, end caps, steps and `border_kit_v5.json`) are **byte-identical** to ours. Nothing differs, so nothing was overwritten.

| File | Size (B) | Piece |
|---|---:|---|
| `models/outdoor/v5_maps/border/border_dune_a_v5_autumn.glb` | 328,304 | dune_a (barchan crescent), autumn |
| `models/outdoor/v5_maps/border/border_dune_a_v5_dead.glb` | 328,300 | dune_a (barchan crescent), dead |
| `models/outdoor/v5_maps/border/border_dune_a_v5_summer.glb` | 328,304 | dune_a (barchan crescent), summer |
| `models/outdoor/v5_maps/border/border_dune_a_v5_winter.glb` | 468,304 | dune_a (barchan crescent), winter |
| `models/outdoor/v5_maps/border/border_dune_b_v5_autumn.glb` | 276,372 | dune_b (long transverse ridge), autumn |
| `models/outdoor/v5_maps/border/border_dune_b_v5_dead.glb` | 276,368 | dune_b (long transverse ridge), dead |
| `models/outdoor/v5_maps/border/border_dune_b_v5_summer.glb` | 276,372 | dune_b (long transverse ridge), summer |
| `models/outdoor/v5_maps/border/border_dune_b_v5_winter.glb` | 407,160 | dune_b (long transverse ridge), winter |
| `models/outdoor/v5_maps/border/border_dune_c_v5_autumn.glb` | 343,568 | dune_c (rippled dome), autumn |
| `models/outdoor/v5_maps/border/border_dune_c_v5_dead.glb` | 343,564 | dune_c (rippled dome), dead |
| `models/outdoor/v5_maps/border/border_dune_c_v5_summer.glb` | 343,568 | dune_c (rippled dome), summer |
| `models/outdoor/v5_maps/border/border_dune_c_v5_winter.glb` | 484,612 | dune_c (rippled dome), winter |
| `models/outdoor/v5_maps/border/border_peak_a_v5_autumn.glb` | 432,816 | peak_a (single summit), autumn |
| `models/outdoor/v5_maps/border/border_peak_a_v5_dead.glb` | 397,640 | peak_a (single summit), dead |
| `models/outdoor/v5_maps/border/border_peak_a_v5_summer.glb` | 397,336 | peak_a (single summit), summer |
| `models/outdoor/v5_maps/border/border_peak_a_v5_winter.glb` | 390,256 | peak_a (single summit), winter |
| `models/outdoor/v5_maps/border/border_peak_b_v5_autumn.glb` | 469,488 | peak_b (twin-summit ridge), autumn |
| `models/outdoor/v5_maps/border/border_peak_b_v5_dead.glb` | 432,728 | peak_b (twin-summit ridge), dead |
| `models/outdoor/v5_maps/border/border_peak_b_v5_summer.glb` | 434,008 | peak_b (twin-summit ridge), summer |
| `models/outdoor/v5_maps/border/border_peak_b_v5_winter.glb` | 438,176 | peak_b (twin-summit ridge), winter |
| `models/outdoor/v5_maps/border/border_peak_c_v5_autumn.glb` | 444,776 | peak_c (broad jagged crag), autumn |
| `models/outdoor/v5_maps/border/border_peak_c_v5_dead.glb` | 409,952 | peak_c (broad jagged crag), dead |
| `models/outdoor/v5_maps/border/border_peak_c_v5_summer.glb` | 409,296 | peak_c (broad jagged crag), summer |
| `models/outdoor/v5_maps/border/border_peak_c_v5_winter.glb` | 434,180 | peak_c (broad jagged crag), winter |
| `models/outdoor/v5_maps/border/border_shelf_a_v5_autumn.glb` | 461,188 | shelf_a (one-step ledge), autumn |
| `models/outdoor/v5_maps/border/border_shelf_a_v5_dead.glb` | 426,668 | shelf_a (one-step ledge), dead |
| `models/outdoor/v5_maps/border/border_shelf_a_v5_summer.glb` | 425,708 | shelf_a (one-step ledge), summer |
| `models/outdoor/v5_maps/border/border_shelf_a_v5_winter.glb` | 406,452 | shelf_a (one-step ledge), winter |
| `models/outdoor/v5_maps/border/border_shelf_b_v5_autumn.glb` | 446,660 | shelf_b (two-tier ledge), autumn |
| `models/outdoor/v5_maps/border/border_shelf_b_v5_dead.glb` | 411,636 | shelf_b (two-tier ledge), dead |
| `models/outdoor/v5_maps/border/border_shelf_b_v5_summer.glb` | 411,180 | shelf_b (two-tier ledge), summer |
| `models/outdoor/v5_maps/border/border_shelf_b_v5_winter.glb` | 399,464 | shelf_b (two-tier ledge), winter |
| `models/outdoor/v5_maps/border/border_shelf_c_v5_autumn.glb` | 460,464 | shelf_c (low slab), autumn |
| `models/outdoor/v5_maps/border/border_shelf_c_v5_dead.glb` | 426,212 | shelf_c (low slab), dead |
| `models/outdoor/v5_maps/border/border_shelf_c_v5_summer.glb` | 424,984 | shelf_c (low slab), summer |
| `models/outdoor/v5_maps/border/border_shelf_c_v5_winter.glb` | 407,896 | shelf_c (low slab), winter |

## v5 maps root: `models/outdoor/v5_maps/` (11 new files)

| File | Size (B) | What it is |
|---|---:|---|
| `models/outdoor/v5_maps/backdrop_far_quads_autumn.glb` | 3,173,336 | far backdrop ring re-packed into quadrant nodes `far_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_far_quads_dead.glb` | 2,815,828 | far backdrop ring re-packed into quadrant nodes `far_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_far_quads_summer.glb` | 2,866,772 | far backdrop ring re-packed into quadrant nodes `far_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_far_quads_winter.glb` | 3,792,772 | far backdrop ring re-packed into quadrant nodes `far_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_mid_quads_autumn.glb` | 3,850,088 | mid backdrop ring re-packed into quadrant nodes `mid_{Q}` and `trees_mid_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_mid_quads_dead.glb` | 2,602,264 | mid backdrop ring re-packed into quadrant nodes `mid_{Q}` and `trees_mid_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_mid_quads_summer.glb` | 3,409,260 | mid backdrop ring re-packed into quadrant nodes `mid_{Q}` and `trees_mid_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/backdrop_mid_quads_winter.glb` | 3,429,576 | mid backdrop ring re-packed into quadrant nodes `mid_{Q}` and `trees_mid_{Q}`. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/fog_valley_banks_v5_quads.glb` | 1,062,444 | valley fog banks split into `fog_{E,N,W,S}`, so sea quadrants can drop their fog. Documented in the live README, but the file was missing. |
| `models/outdoor/v5_maps/shore_foam_strips_v2.glb` | 394,616 | Stage 12E foam strips v2. Released alongside the islands v2 and coast kit. A companion to the live `shore_foam_strips_v5`, which stays unchanged. |
| `models/outdoor/v5_maps/shore_rock_kit_v2.glb` | 999,736 | Stage 12E shore rock kit v2. Rock stacks that hide a cliff height change. A companion to the live `shore_rock_kit_v5` (which stays unchanged), not a replacement. |

Note: the live `models/outdoor/v5_maps/README.md` was not edited. It stops before Stage 12C, while the artist's copy also documents 12C rect, 12D winter fix, 12E islands v2 and border kit, and 12F to 12I border revisions. Ask the artist for the newer README if you want it.

## Skipped: already in the repo (byte-identical)

- `batch1_interactables`: 5 GLBs, already at `models/env_extra/interactables/` (3), `models/shrines/` (2)
- `hellgates`: 3 GLBs, already at `models/env_extra/hellgates/` (3)
- `kit`: 21 GLBs, already at `models/town/martsirt/kit/glb/` (21)
- `martsirt_v2_2`: 49 GLBs, already at `models/town/martsirt/kit/glb/` (21), `models/town/martsirt_v2_2/buildings/chapel_st_noll/` (2), `models/town/martsirt_v2_2/buildings/cottage_ness/` (1), `models/town/martsirt_v2_2/buildings/forge/v2/` (1), `models/town/martsirt_v2_2/buildings/gatehouse_south/` (3), `models/town/martsirt_v2_2/buildings/graveyard/` (1), `models/town/martsirt_v2_2/buildings/herbs_ysara/` (1), `models/town/martsirt_v2_2/buildings/inn/` (1), `models/town/martsirt_v2_2/buildings/lodge_orrin/` (1), `models/town/martsirt_v2_2/buildings/mill/` (1), `models/town/martsirt_v2_2/buildings/scriptorium_quill/` (1), `models/town/martsirt_v2_2/buildings/square/` (1), `models/town/martsirt_v2_2/buildings/stable/` (1), `models/town/martsirt_v2_2/buildings/watchhouse_gibbet/` (1), `models/town/martsirt_v2_2/dressing/` (6), `models/town/martsirt_v2_2/props/` (6)
- `outdoor/glb_v3`: 6 GLBs, already at `models/outdoor/v3trees/` (6)
- `outdoor/glb_v5`: 21 GLBs, already at `models/outdoor/v5/` (16), `models/outdoor/v5/trees/` (5)
- `outdoor/glb_v5_maps`: 38 GLBs, already at `models/outdoor/v5_maps/` (38)
- `outdoor/glb_v5_maps/border`: 148 GLBs, already at `models/outdoor/v5_maps/border/` (148)
- `outdoor/glb_v5_maps/rect`: 60 GLBs, already at `models/outdoor/v5_maps/rect/` (60)
- `outdoor/v5_ground/plants`: 7 GLBs, already at `models/outdoor/v5/plants/` (7)
- `outdoor/v5_ground/trees`: 2 GLBs, already at `models/outdoor/v5/plants/` (2)
- `props_gothic_v1`: 45 GLBs, already at `models/env_extra/props_gothic_v1/boats/` (2), `models/env_extra/props_gothic_v1/loot/` (22), `models/env_extra/props_gothic_v1/props/` (21)

## Skipped: superseded older working copies (not added)

- `buildings/` (17 GLBs): an older working copy of the Martsirt buildings. Newer versions are live in `models/town/martsirt_v2_2/buildings/`, byte-identical to the artist's v2.2. This includes the original `bld_forge_wolchen.glb`, which `forge/v2` superseded.
- `props/` (13 GLBs): the v1 Martsirt props. Newer versions are live in `models/town/martsirt*/props/`. `prop_fence_rail_2m.glb` is in no repo version and is not referenced by any Martsirt placement, so it was left out.
- `batch1_interactables/` v1 `chest.glb` and `door.glb`: the v2 versions are live in `models/env_extra/interactables/`. The `shrine.glb` iterations v1, v2 and v3 were also skipped: v4 is live (`models/shrines/`).
- `props_gothic_v1`, `hellgates` and `kit` are byte-identical to the live copies listed above. Per the engineer, the cliff kits (`models/env_extra/cliffkit_v1`, `cliffkit_v2`) are live too and were not touched.
