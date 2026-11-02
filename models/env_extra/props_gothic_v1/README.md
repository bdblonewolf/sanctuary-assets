# Sanctuary - Gothic Prop Pack batch 1 (`props_gothic_v1`)

Two boats, 21 gothic decoration props and 11 lootable containers (each with a closed and an opened GLB, 22 files). Everything is procedural, built in Blender 4.2 and textured with CC0 Poly Haven 1K materials that were toned dark and earthy (AO multiplied in, desaturated). The textures are embedded at 512 px to keep the files phone-friendly (the two boats use 1K albedo).

## Conventions (all files)
- **1 unit = 1 m, +Y up, front = +Z.** Origin is at the base of the prop, on the ground at its footprint centre.
- **Boats:** the origin is at the **waterline**. Put the root at the water-surface height; anything below y=0 is the submerged hull.
  - `boat_longship_ride_v1`: origin at the waterline at the hull centre. **The bow faces +Z.** Port (left when facing the bow) = **+X**, so `oars_L` is on +X and `oars_R` is on -X.
- **Wall props** (`wall_sconce`, `wall_niche_saint`, `tapestry_heraldic`, `hanging_sign`, `chains_shackles`): origin = floor level at the wall face. The back sits on the local Z=0 plane and the prop faces +Z, away from the wall.
- **Format:** plain GLB with no `extensionsUsed`, no lights and no cameras. Emissive is at most 1.0 (candle flames are emissive alpha cards, so add your own point lights in-engine). Alpha-cutout materials (`cut_*`) use MASK and are double-sided; `ds_*` materials are double-sided.
- **Colliders:** nodes named `col_*` are simple 12-tri box meshes with `extras.collider = "box"` and `extras.size_m` (given as Blender X, depth, height). Hide them at load (`obj.visible = false`) and feed them to physics or nav. Their tris are listed separately from the visible tris.
- **Rocks and mounds** are organic, with no flat faces. Only the cave-mouth cliff blobs in the preview scene, which are not shipped, are allowed to be broad.

## Previews
Current (after the fix pass):
- `preview_boats.jpg`: both boats in a scenic 3/4 view. The wreck sits at a rocky cave mouth and the longship is in the foreground. The cliffs, water and rocks are render-only scenery.
- `preview_gothic_props.jpg`: labelled contact sheet of the 21 gothic props.
- `preview_loot.jpg`: the 11 loot containers, with the closed state (left) next to the opened state (right). Orthographic camera, so the back rows are the same size as the front.

(In this repo the v2 previews are shipped as downscaled JPEGs; the original batch-1 renders and src/ are not included.)

## Changelog
**Fix pass (2026-11-01).** Node names, colliders, `col_click` volumes, origins and conventions are unchanged unless noted.
- `wall_niche_saint_v1`: re-sculpted saint (robed figure with a sculpted head and face, bowed head, clasped hands, hood and halo).
- `sarcophagus_carved_v1`: re-sculpted knight effigy (sculpted head and face, clasped hands, no circlet). `sarcophagus_small` has no effigy, so it was not changed.
- `iron_maiden_v1`: lighter, rusted iron with steel bands and rivets, plus a sorrowful relief face with eye and mouth holes. The `door` pivot and its open angle are unchanged.
- `weapon_rack_wreck` (loot): closed is a wrecked rack (snapped right trestle, slumped top beam, hanging pegboard) with a rusted notched sword, spear and axe. Opened is the rack collapsed flat and scattered, weapons taken, with only a snapped shaft and a broken blade tip left.
- `hollow_log` (loot): opened is now the log split lengthwise. The lower half-shell stays in place with the rotten core exposed, the top half lies open-side-up beside it, the split edges are splintered and the plug has rolled away.
- `boat_longship_ride_v1`: finer bow entry, plus a thinner, raked stem with planking that follows it (the dragon head sits 0.3 m further forward). The stern is slightly finer too.
- `boat_wreck_cave_v1`: about 15% larger (colliders scaled to match; `col_mast_stump` is also thinner), with a thinner mast stump, fallen mast and yard. Ribs are thicker and more numerous, with more broken ribs at the stern and the hole, and there are more and thicker loose planks.
- `tombstone_gothic_v1`: the `UNUSED_OBJECT` validator info is fixed. Skulls are more detailed (brow, teeth, jaw) on the tombstone, iron gate, altar, gibbet and the bone/skull/remains loot.

## Boats
| File | Size | Tris | Size m (X x Y x Z) | Colliders | Placement notes |
|---|---|---|---|---|---|
| `boats/boat_longship_ride_v1.glb` | 2.06 MB | 14,672 (+36 col) | 9.79 x 9.84 x 15.72 | `col_deck_walk`, `col_hull`, `col_mast` | Rideable longship. Bow faces +Z, port/left = +X. Origin = waterline at hull centre; hull draft ~0.6 m below y=0. Deck y=0.15. Animate sail (pivot yard centre), oars_L/oars_R children oar_* (pivot at oar port). |
| `boats/boat_wreck_cave_v1.glb` | 2.00 MB | 11,595 (+48 col) | 8.06 x 8.7 x 10.87 | `col_hull_bow`, `col_hull_mid`, `col_mast_stump`, `col_stern_mound` | Static set piece. Origin = waterline; parts below y=0 are underwater/buried. Place in shallows or on shore at a cave mouth, bow (+Z) pointing out of the cave. |

**`boat_longship_ride_v1` nodes**
- `player_stand`: where the player rides, on the deck centre aft of the mast, at y=0.15.
- `player_board`: boarding point at the waterline beside the port (+X) hull. Lerp or teleport the player from here to `player_stand`.
- `npc_seat_1..6`: rower seats, 3 per side, with `extras.facing = "inboard"`.
- `sail`: pivots at the yard centre. Its children are `yard` and `sail_cloth`; scale or rotate it to furl or trim.
- `oars_L` / `oars_R`: groups of `oar_L_1..6` / `oar_R_1..6`. Each oar pivots at its oar port, so rotate it about local Y and X to row.
- `col_hull`: hull volume, used to block the player in the water.
- `col_deck_walk`: thin walkable deck box (`extras.walkable = true`), with its top at about deck height.
- `col_mast`: mast blocker.

**`boat_wreck_cave_v1`:** a static set piece (`wreck_hull`, plus `silt_mound` and `barnacles_weed`). It has separate box colliders for the bow, midships, mast stump and the stern mound.

## Gothic decoration props
| File | Size | Tris | Size m (X x Y x Z) | Colliders | Placement notes |
|---|---|---|---|---|---|
| `props/church_pew_v1.glb` | 78 KB | 296 (+12 col) | 2.47 x 1.22 x 0.8 | `col_pew` | Seat height 0.46 m; faces +Z (sitters look toward +Z). Rows ~1.0 m apart. |
| `props/altar_cloth_v1.glb` | 449 KB | 1,526 (+12 col) | 2.24 x 1.7 x 1.13 | `col_altar` | Front faces +Z. Two lit candles (emissive flame cards); add a small warm point light in-engine if desired. |
| `props/lectern_book_v1.glb` | 368 KB | 488 (+12 col) | 0.71 x 1.41 x 0.64 | `col_lectern` | Desk slopes down toward +Z; the reader stands on the +Z side. Small lit reading candle. |
| `props/candelabra_tall_v1.glb` | 194 KB | 1,520 (+12 col) | 0.7 x 2.16 x 0.7 | `col_candelabra` | 2.05 m tall, 5 lit candles (emissive flame cards). Pair with a warm point light ~1.9 m up. |
| `props/wall_sconce_v1.glb` | 144 KB | 342 (+12 col) | 0.2 x 0.56 x 0.41 | `col_sconce` | Wall prop: origin = floor at wall face; back sits on local Z=0 plane, faces +Z (out of wall). Candle flame ~1.95 m above origin. |
| `props/gargoyle_perched_v1.glb` | 326 KB | 1,290 (+12 col) | 1.41 x 2.38 x 0.93 | `col_gargoyle` | Crouched gargoyle on 1.1 m pedestal, faces +Z, wings half-spread. 2.4 m tall. |
| `props/wall_niche_saint_v1.glb` | 482 KB | 2,966 (+12 col) | 1.46 x 2.7 x 0.82 | `col_niche` | Wall prop: origin = floor at wall face; back sits on local Z=0 plane, faces +Z (out of wall). Block 1.4 x 2.7 m, 0.55 m deep; flush against or inset into a wall. Votive candles lit. |
| `props/grave_celtic_cross_v1.glb` | 282 KB | 844 (+24 col) | 1.44 x 2.11 x 2.33 | `col_cross`, `col_mound` | Celtic ring cross on plinth with a sunken soil mound in front (+Z side). Mound is organic (no flat faces). |
| `props/tombstone_gothic_v1.glb` | 528 KB | 786 (+12 col) | 0.74 x 1.38 x 0.55 | `col_tomb` | Leaning pointed-arch headstone with skull and crossbones relief; ~0.2 m sunk below origin. Face toward +Z. |
| `props/urn_plinth_v1.glb` | 138 KB | 768 (+12 col) | 0.64 x 1.83 x 0.62 | `col_urn` | Funerary urn on gothic-panelled plinth, 1.83 m. Symmetric; any facing. |
| `props/iron_fence_gothic_v1.glb` | 258 KB | 1,112 (+12 col) | 2 x 1.82 x 0.32 | `col_fence` | Tiling segment 2.0 m along X (snap ends at x=+-1.0). Pairs with iron_gate_gothic_v1 (same height & curb). |
| `props/iron_gate_gothic_v1.glb` | 446 KB | 2,084 (+36 col) | 3.32 x 2.98 x 0.62 | `col_gate_closed`, `col_pier_L`, `col_pier_R` | 2.2 m opening between stone piers (overall 3.2 m). Leaves gate_leaf_L/R pivot at their hinge; col_gate_closed should be disabled when opened. |
| `props/tapestry_heraldic_v1.glb` | 177 KB | 404 (+12 col) | 1.67 x 2.79 x 0.12 | `col_tapestry` | Wall prop: origin = floor at wall face; back sits on local Z=0 plane, faces +Z (out of wall). Rod at 3.0 m, cloth hangs to ~0.5 m. Double-sided material. |
| `props/anvil_stump_v1.glb` | 206 KB | 516 (+12 col) | 0.95 x 1.01 x 0.94 | `col_anvil` | Anvil (horn toward +X) on a rooted stump with hammer and tongs. Work height 0.96 m. |
| `props/cauldron_tripod_v1.glb` | 322 KB | 1,438 (+48 col) | 1.37 x 1.81 x 1.37 | `col_cauldron`, `col_leg0`, `col_leg1`, `col_leg2` | Cauldron on chain under an iron tripod over a cold stone fire ring. Add a fire VFX / point light if lit. |
| `props/hanging_sign_v1.glb` | 166 KB | 652 (+12 col) | 0.14 x 0.83 x 0.96 | `col_sign` | Wall prop: origin = floor at wall face; back sits on local Z=0 plane, faces +Z (out of wall). Bracket at 2.7 m, board bottom ~1.95 m. Node sign_board pivots at bracket for wind swing. Tavern tankard emblem. |
| `props/chains_shackles_v1.glb` | 158 KB | 2,440 (+12 col) | 1.15 x 1.36 x 0.24 | `col_chains` | Wall prop: origin = floor at wall face; back sits on local Z=0 plane, faces +Z (out of wall). Two wall eye-plates at 2.1 m with hanging chains, manacles and a swag chain with collar. |
| `props/gibbet_cage_v1.glb` | 456 KB | 2,362 (+24 col) | 1.97 x 3.68 x 0.67 | `col_cage`, `col_post` | Gallows post with hanging body-shaped gibbet cage and remains. Node cage pivots at the chain end for sway. Footprint ~1.7 x 0.6 m. |
| `props/sarcophagus_carved_v1.glb` | 365 KB | 3,020 (+12 col) | 2.42 x 1.27 x 1.12 | `col_sarcophagus` | Long axis X (head at -X). Carved effigy on lid, blind gothic arcades. Not lootable (see loot/ for small cracked one). |
| `props/iron_maiden_v1.glb` | 383 KB | 1,944 (+12 col) | 1.14 x 2.09 x 1.06 | `col_maiden` | Iron maiden (rusted iron, worn steel bands/rims, sorrowful relief face on door), exported with door node open ~115 deg (set door rotation 0 to close). Faces +Z. |
| `props/cobweb_cards_v1.glb` | 18 KB | 6 (+12 col) | 3.9 x 2 x 0.9 | `col_none` | Three alpha-cutout web cards as separate nodes (web_corner, web_hang, web_low), each with its own origin at its attach point; detach and place individually. Non-blocking. |

## Loot containers (`loot/`) - `interactable: "loot_low"`
Each container comes as a pair, `<name>_closed.glb` and `<name>_opened.glb`. Both files share the same origin and footprint and the same collider names, so you can swap the closed one for the opened one in place. Each root node carries `extras: {loot_state, loot_pair}`. `interactable: "loot_low"` and `environments` are recorded in `props_gothic_v1.json`.
- `col_click` is the mouse or tap pick volume. It has `extras.pick = "loot"` and is a little larger than the visible prop, for touch use.
- The other `col_*` node is the physical blocker.

| Container | Category | Environments | Closed (size / tris) | Opened (size / tris) | Notes |
|---|---|---|---|---|---|
| `bone_pile` | loot_dungeon | dungeon, crypt, catacombs, cave, torture_chamber | 261 KB / 1,360 | 259 KB / 1,360 | Heap of old bones with two skulls on a dirt mound. Opened: bones kicked flat and scattered, skull rolled off. |
| `skull_heap` | loot_dungeon | dungeon, crypt, catacombs, ossuary | 280 KB / 1,732 | 279 KB / 1,732 | Stacked pyramid of seven skulls on a plinth of bones. Opened: heap knocked over, skulls tumbled across the floor. |
| `burial_urn` | loot_dungeon | dungeon, crypt, catacombs, tomb, desert_tomb | 266 KB / 742 | 364 KB / 826 | Clay burial urn with lid and rope band. Opened: urn smashed - jagged lower half, shards, lid on its side, spilled ash and a finger bone. |
| `sarcophagus_small` | loot_dungeon | crypt, catacombs, tomb, cathedral_undercroft | 127 KB / 324 | 358 KB / 1,276 | Small cracked stone sarcophagus (1.3 m, child/reliquary size) with crossed lid. Opened: lid broken in two and shoved off, dusty interior with bones visible. |
| `sack_pile` | loot_dungeon | dungeon, cellar, storeroom, camp, sewer | 159 KB / 500 | 275 KB / 1,024 | Pile of rotting hessian sacks. Opened: sacks slit and slumped flat, grain/rot spilled across the floor. |
| `remains_heap` | loot_dungeon | dungeon, crypt, battlefield, torture_chamber, cave | 375 KB / 1,100 | 390 KB / 1,232 | Shrouded corpse lying on a dirt bed, skull and bony hand poking from a rotten shroud. Opened: shroud dragged aside, ribcage/skeleton exposed and picked over. |
| `rubble_cache` | loot_dungeon | dungeon, crypt, mine, cave, ruins | 366 KB / 1,156 | 393 KB / 1,912 | Collapsed rubble with a broken beam burying a cache. Opened: rubble dug aside, smashed strongbox lid open, empty. |
| `rock_pile` | loot_outdoor | wilderness, forest, highlands, riverbank, cave_entrance, graveyard | 333 KB / 720 | 344 KB / 1,060 | Cairn-like heap of loose rocks. Opened: rocks rolled aside, shallow dug hollow revealed. |
| `hollow_log` | loot_outdoor | forest, swamp, wilderness, riverbank | 228 KB / 508 | 251 KB / 1,098 | Fallen hollow dead log, end plugged with a mossy stone. Opened: plug rolled away and the top split off, rotten hollow exposed. |
| `rotten_stump` | loot_outdoor | forest, swamp, graveyard, wilderness | 240 KB / 840 | 349 KB / 916 | Rotten hollow tree stump with roots and fungus, top sealed by a rotten crust. Opened: one side burst open and the crust broken, rotten hollow exposed. |
| `weapon_rack_wreck` | loot_outdoor | battlefield, barracks, camp, ruins, wilderness | 259 KB / 320 | 171 KB / 218 | Wrecked weapon rack: right trestle snapped, top beam slumped to the ground, still holding a rusted notched sword, a leaning spear and an axe. Opened: rack collapsed flat and scattered, weapons taken - only a snapped spear shaft and a broken blade tip left. |

Total: 45 GLBs, 16.0 MB.

## Validation
All 45 GLBs pass `gltf-validator` (`validateBytes`) with **0 errors**. Run `node src/validate.js boats/*.glb props/*.glb loot/*.glb` to check them again.
- The warnings are almost all `MESH_PRIMITIVE_GENERATED_TANGENT_SPACE`: the normal-mapped materials ship without tangents. three.js generates tangents at runtime, so this is harmless and was kept to save bytes.
- Some files also carry an `UNUSED_OBJECT` info (not a warning): an unused texture-coordinate set on a flat, untextured material. It is harmless.

## Source
- Build scripts are in `src/`: `build_boats.py`, `build_gothic.py`, `build_loot.py`, `lib.py`, `glib.py`, `hull.py` and `prep_tex.py`.
- Previews are rendered with `src/render.py`, and `src/gen_docs.py` writes this README and `props_gothic_v1.json`.

## Texture credits (all CC0, polyhaven.com)

- Weathered Planks (`weathered_planks`) by Dario Barresi, Dimitrios Savva: https://polyhaven.com/a/weathered_planks
- Rough Wood (`rough_wood`) by Rob Tuytel: https://polyhaven.com/a/rough_wood
- Moss Wood (`moss_wood`) by Rob Tuytel: https://polyhaven.com/a/moss_wood
- Dark Wooden Planks (`dark_wooden_planks`) by Amal Kumar: https://polyhaven.com/a/dark_wooden_planks
- Weathered Peeling Timber (`weathered_peeling_timber`) by Dimitrios Savva: https://polyhaven.com/a/weathered_peeling_timber
- Worn Rock Natural 01 (`worn_rock_natural_01`) by Rob Tuytel, Dimitrios Savva: https://polyhaven.com/a/worn_rock_natural_01
- Rock Pitted Mossy (`rock_pitted_mossy`) by Dimitrios Savva, Rico Cilliers: https://polyhaven.com/a/rock_pitted_mossy
- Castle Wall Slates (`castle_wall_slates`) by Rob Tuytel: https://polyhaven.com/a/castle_wall_slates
- Rock Face (`rock_face`) by Greg Zaal, Dario Barresi: https://polyhaven.com/a/rock_face
- Dark Rock (`dark_rock`) by Amal Kumar: https://polyhaven.com/a/dark_rock
- Rust Coarse 01 (`rust_coarse_01`) by Dimitrios Savva, Rico Cilliers: https://polyhaven.com/a/rust_coarse_01
- Metal Plate (`metal_plate`) by Rob Tuytel: https://polyhaven.com/a/metal_plate
- Hessian 230 (`hessian_230`) by colormass, Rico Cilliers: https://polyhaven.com/a/hessian_230
- Rough Linen (`rough_linen`) by colormass, Rico Cilliers: https://polyhaven.com/a/rough_linen
- Velour Velvet (`velour_velvet`) by colormass, Rico Cilliers: https://polyhaven.com/a/velour_velvet
- Brown Leather (`brown_leather`) by Rob Tuytel: https://polyhaven.com/a/brown_leather
- Grey Plaster (`grey_plaster`) by Rob Tuytel: https://polyhaven.com/a/grey_plaster
- Cliff Side (`cliff_side`) by James Ray Cock, Jenelle van Heerden, Dario Barresi: https://polyhaven.com/a/cliff_side
- Lichen Rock (`lichen_rock`) by Rico Cilliers: https://polyhaven.com/a/lichen_rock

The toning, the sail stripes, the tapestry heraldry and the book pages are derived from the textures above. The flame and cobweb alpha cards are procedural.
