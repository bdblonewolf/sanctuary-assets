# props_new: game-ready props (v1)

Plain GLB (no extensions), 1 unit = 1 m, Y up, front +Z, base y=0 (the well shaft, trapdoor shaft and ladder go below 0 on purpose). No lights or cameras; emissive <= 1.0.
Textures are Poly Haven CC0 (512 px, map/rug 1k). Validated with gltf-validator (0 errors; the only warnings are MESH_PRIMITIVE_GENERATED_TANGENT_SPACE) and loaded with three.js GLTFLoader (38/38 OK).
`col_*` nodes are invisible box colliders (hide or replace with physics boxes). `col_click` = pick volume. Stone and massing are rounded rubble; only crafted planks are flat.

Previews: `previews/props_new_lineup.png`, `previews/props_new_breakables_lineup.png`.

## Files
Size = W x H x D in m (glTF X, Y, Z, visual meshes only). Ymin < 0 = geometry below the floor (shafts).

| file | tris | MB | size m | Ymin | nodes (pivots/anchors) | colliders | status |
|---|---|---|---|---|---|---|---|
| `cart_broken.glb` | 1714 | 0.59 | 3.15 x 1.19 x 4.60 | -0.03 | axle, cart_body, hitch, spill, wheel_L, wheel_R | col_cart, col_click | DERIVED |
| `cart_intact.glb` | 1372 | 0.32 | 1.64 x 1.10 x 3.93 | -0.01 | axle, cart_body, hitch, wheel_L, wheel_R | col_cart, col_click | DERIVED |
| `desk.glb` | 504 | 0.55 | 1.29 x 1.06 x 0.71 | -0.00 | desk_body, fx_candle, interact | col_desk | DERIVED |
| `map_board_known_roads.glb` | 278 | 0.49 | 2.12 x 2.29 x 0.77 | +0.00 | board, interact, map_slot | col_map_board | NEW |
| `nightstand.glb` | 388 | 0.37 | 0.54 x 0.86 x 0.46 | +0.00 | drawer, fx_candle, nightstand_body | col_nightstand | NEW |
| `rowboat_ferry.glb` | 1412 | 0.29 | 5.31 x 0.84 x 4.42 | +0.00 | hull, oar_L, oar_R, player_board, seat_passenger, seat_rower, waterline | col_boat | DERIVED |
| `rug.glb` | 780 | 0.25 | 2.40 x 0.04 x 1.60 | +0.00 | rug.001 | col_rug | NEW |
| `trapdoor_ashen_coast_closed.glb` | 934 | 0.38 | 1.80 x 1.68 x 1.54 | -1.58 | hinge, lid, nav_down, surround | col_click, col_trapdoor | DERIVED |
| `trapdoor_ashen_coast_opened.glb` | 934 | 0.38 | 1.80 x 2.49 x 1.59 | -1.58 | hinge, lid, nav_down, surround | col_click, col_trapdoor_lid | DERIVED |
| `wardrobe.glb` | 548 | 0.21 | 1.36 x 2.11 x 0.71 | -0.01 | door_L, door_R, interact, wardrobe_body | col_wardrobe | NEW |
| `well_stone.glb` | 1807 | 0.78 | 2.06 x 3.84 x 1.81 | -1.20 | bucket, interact, well | col_well, col_well_posts | NEW + REUSED part |
| `well_stone_heal.glb` | 1851 | 0.82 | 2.06 x 3.84 x 1.81 | -1.20 | bucket, fx_heal_glow, interact, well | col_well, col_well_posts | DERIVED |
| `breakables/barrel_broken.glb` | 740 | 0.20 | 1.79 x 0.37 x 1.71 | -0.07 | mesh | col_click | NEW |
| `breakables/barrel_group_broken.glb` | 2196 | 0.26 | 2.32 x 0.37 x 2.31 | -0.07 | mesh | col_click | DERIVED |
| `breakables/barrel_group_intact.glb` | 2124 | 0.25 | 1.23 x 0.84 x 1.42 | +0.00 | mesh | col_barrel_group, col_click | DERIVED |
| `breakables/barrel_intact.glb` | 724 | 0.20 | 0.63 x 0.84 x 0.63 | +0.00 | mesh | col_barrel, col_click | NEW |
| `breakables/crate_broken.glb` | 334 | 0.28 | 2.03 x 0.37 x 1.62 | -0.03 | mesh | col_click | NEW |
| `breakables/crate_intact.glb` | 408 | 0.15 | 0.75 x 0.70 x 0.75 | +0.00 | mesh | col_click, col_crate | NEW |
| `breakables/crate_stack_broken.glb` | 1040 | 0.32 | 3.00 x 0.64 x 2.18 | -0.04 | mesh | col_click | DERIVED |
| `breakables/crate_stack_intact.glb` | 1176 | 0.20 | 1.57 x 1.30 x 0.87 | +0.00 | mesh | col_click, col_crate_stack | DERIVED |
| `breakables/sack_broken.glb` | 184 | 0.25 | 0.93 x 0.17 x 0.98 | +0.00 | mesh | col_click | NEW |
| `breakables/sack_intact.glb` | 188 | 0.15 | 0.50 x 0.63 x 0.38 | +0.00 | mesh | col_click, col_sack | NEW |
| `breakables/sack_pile_broken.glb` | 700 | 0.27 | 2.03 x 0.17 x 1.62 | +0.00 | mesh | col_click | DERIVED |
| `breakables/sack_pile_intact.glb` | 844 | 0.18 | 1.14 x 0.91 x 1.23 | +0.00 | mesh | col_click, col_sack_pile | DERIVED |
| `breakables/urn_a_broken.glb` | 412 | 0.21 | 1.12 x 0.36 x 1.10 | -0.04 | mesh | col_click | DERIVED |
| `breakables/urn_a_intact.glb` | 464 | 0.19 | 0.45 x 0.72 x 0.45 | +0.00 | mesh | col_click, col_urn | DERIVED |
| `breakables/urn_b_broken.glb` | 412 | 0.21 | 1.45 x 0.26 x 1.49 | -0.03 | mesh | col_click | DERIVED |
| `breakables/urn_b_intact.glb` | 432 | 0.19 | 0.59 x 0.50 x 0.59 | +0.00 | mesh | col_click, col_urn | DERIVED |
| `breakables/urn_c_broken.glb` | 438 | 0.21 | 1.03 x 0.50 x 0.83 | -0.03 | mesh | col_click | DERIVED |
| `breakables/urn_c_intact.glb` | 536 | 0.12 | 0.51 x 1.10 x 0.39 | +0.00 | mesh | col_click, col_urn | DERIVED |
| `breakables/weapon_rack_broken.glb` | 2237 | 0.51 | 2.63 x 0.87 x 3.19 | -0.03 | loot_hatchet, loot_shield, loot_spear, loot_sword, rack | col_click, col_rack | DERIVED + REUSED |
| `breakables/weapon_rack_intact.glb` | 2179 | 0.51 | 1.64 x 2.37 x 1.03 | -0.01 | loot_hatchet, loot_shield, loot_spear, loot_sword, rack | col_click, col_rack | DERIVED + REUSED |
| `lite/bookshelf_worn_lite.glb` | 2599 | 0.26 | 1.37 x 2.06 x 0.58 | -0.00 | wooden_bookshelf_worn |  | DERIVED (lite) |
| `lite/iron_chest_lite_closed.glb` | 3011 | 0.62 | 1.10 x 0.62 x 0.72 | -0.00 | body, lid, chest_root | col_chest | DERIVED (lite) |
| `lite/iron_chest_lite_opened.glb` | 3011 | 0.62 | 1.10 x 1.07 x 1.03 | -0.00 | body, lid, chest_root | col_chest | DERIVED (lite) |
| `lite/pier_lite.glb` | 8998 | 0.89 | 3.10 x 7.51 x 19.03 | -0.99 | modular_wooden_pier_poles, modular_wooden_pier_planks, modular_wooden_pier_section_01, modular_wooden_pier_section_02, modular_wooden_pier_section_03, modular_wooden_pier_section_05, modular_wooden_pier_section_04 |  | DERIVED (lite) |
| `lite/shrine_basic_lite.glb` | 4824 | 1.36 | 1.83 x 2.56 x 1.48 | -0.01 | fx_candle_00, fx_candle_01, fx_candle_02, fx_candle_03, fx_candle_04, fx_candle_05, fx_candle_06, fx_candle_07, fx_candle_08, fx_candle_09, fx_candle_10, fx_candle_11, fx_candle_12, fx_candle_13, fx_candle_14, fx_candle_15, fx_candle_16, fx_shrine_glow, interact, shrine_body, shrine_basic_root | col_shrine_niche, col_shrine_plinth | DERIVED (lite) |
| `lite/shrine_weeping_angel_lite.glb` | 4824 | 1.36 | 1.83 x 2.64 x 1.47 | -0.08 | fx_basin_shimmer, fx_candle_00, fx_candle_01, fx_candle_02, fx_candle_03, fx_candle_04, fx_heal_motes, fx_tear_drip, interact, shrine_body, water_basin, shrine_weeping_angel_root | col_shrine_niche, col_shrine_plinth | DERIVED (lite) |

## Pivots and anchors
- **trapdoor_ashen_coast**: node `lid` origin = hinge on the back edge (glTF -Z side). Open = rotate about local X by -112° (the `_opened` file is exactly that pose). Also `hinge` and `nav_down` (`dest=ashen_coast`) empties. Place the root on the inn node `cellar_hatch` (5.2, 0.06, 4.3); it covers the same 1.2 x 1.0 m as `col_cellar_hatch`. The inn has no hatch mesh, so this is the visual.
- **cart**: `wheel_L` (+X) and `wheel_R` (-X) origins = axle centre (y 0.5); spin about local X. `axle` and `hitch` (shaft tips) empties. Broken: `wheel_L` is detached and lying flat.
- **well_stone / well_stone_heal**: node `bucket` origin = rope top under the winch (y 1.68). Lower it by translating -Y (up to ~1.6 m into the shaft). Heal: the `fx_heal_glow` empty is for a point light or particles (#40d9b3).
- **rowboat_ferry**: `oar_L` and `oar_R` pivot at the oarlocks. `waterline` empty (y 0.2): sink the boat so it sits at the water surface. Also `seat_rower`, `seat_passenger` and `player_board`. Bow faces -Z.
- **map_board_known_roads**: `map_slot` is a separate 1.5 x 1.0 m quad with its own material `m_map_slot` (UV 0..1), so you can swap its texture at runtime. `interact` stand point.
- **wardrobe**: `door_L` and `door_R` origins on the outer hinge edges; rotate about Y. **nightstand**: `drawer` slides +Z. `fx_candle` on the nightstand and the desk.
- **weapon_rack**: each weapon is its own `loot_*` node (spear, hatchet, sword, shield), so you can hide it on pickup.
- **Breakables**: swap `_intact` for `_broken` at the same transform. `_broken` has no blocking collider, only `col_click`. glTF extras on the root: `state`, `pair`, `replaces`.

## Player room (inn north upstairs hall, upper floor y=3.5, about 15.4 x 5.3 m, ~2.8 m headroom)
wardrobe 1.26 x 2.11 x 0.71 | nightstand 0.54 x 0.6 (0.86 with candle) x 0.46 | desk 1.29 x 0.76 x 0.71 | rug 2.4 x 1.6 | plus the existing bed and `iron_chest_lite` as the stash. Everything fits between the north windows (z -6.42) and the corridor partition (z -1.0).

## Breakable replacements (originals untouched)
| pair | replaces |
|---|---|
| breakables/barrel_* | `models/modular_dungeon_kit.glb` BarrelClosed_01/02/03 + BarrelBroken_01/02; single uses of `characters_art/props/wine_barrel_01_sanctuary.glb` (inn.json) |
| breakables/barrel_group_* | `models/town/martsirt_v2_2/props/prop_barrel_group.glb` (+ martsirt, martsirt_v2 copies); placements market_barrels, inn_barrels |
| breakables/crate_* | crate stand-ins (dungeons draw kit barrels as crates) |
| breakables/crate_stack_* | `models/town/martsirt_v2_2/props/prop_crate_stack.glb`; placement forge_crates, inn.json |
| breakables/sack_* | new single sack |
| breakables/sack_pile_* | `models/env_extra/props_gothic_v1/loot/sack_pile_closed/opened.glb` |
| breakables/urn_a/b/c_* | new (method from loot/burial_urn) |
| breakables/weapon_rack_* | new (layout from loot/weapon_rack_wreck) |

## Reuse status (searched repo models/, characters_art/props/, wip_models/, /workspace/sanctuary_env, /workspace/sanctuary_art, local Poly Haven/KayKit)
- **map_board_known_roads**: NEW: nothing suitable existed (hanging_sign_v1 is a wall sign); textures painted from repo map names
- **rowboat_ferry**: DERIVED: props_gothic_v1 longship: same hull.py clinker generator + m_hull_tarred/wood materials, scaled to a 4 m rowboat
- **well_stone**: NEW + REUSED part: no well existed; bucket = decimated Poly Haven wooden_bucket_01 (CC0, local assets3d)
- **well_stone_heal**: DERIVED: from well_stone + runes_e emissive band, glowing water
- **trapdoor_ashen_coast**: DERIVED: inn bld_inn_salted_kettle_shared cellar_hatch footprint (col_cellar_hatch 1.2 x 1.0 m; inn has no hatch mesh) + inn soot stone
- **cart**: DERIVED: footprint/scale from models/town/martsirt/props/prop_cart_broken.glb (bed ~2.0 x 1.4 m); rebuilt so both states match and wheels are pivot nodes
- **wardrobe**: NEW: no wardrobe/cabinet in repo or workspace (KayKit only cartoon)
- **nightstand**: NEW: none existed
- **desk**: DERIVED: Poly Haven wooden_table_02 (CC0) rescaled + drawer/papers/ink/candle
- **rug**: NEW: none existed; texture from Poly Haven fabric + painted medallion
- **urn_a**: DERIVED: break method from props_gothic_v1 loot/burial_urn (jagged lathe, shards, ash)
- **urn_b**: DERIVED: as urn_a
- **urn_c**: DERIVED: as urn_a (amphora with handles)
- **weapon_rack**: DERIVED + REUSED: layout from props_gothic_v1 weapon_rack_wreck; weapons = decimated copies of models/weapons/weapon_mourning_spear, weapon_briar_hatchet, characters_art/monsters/swordsman sword, characters_art/props/kite_shield_sanctuary (originals untouched)
- **barrel**: NEW: replaces modular_dungeon_kit BarrelClosed_01/02/03 + BarrelBroken_01/02, and single uses of characters_art/props/wine_barrel_01_sanctuary.glb
- **barrel_group**: DERIVED: layout of models/town/martsirt_v2_2/props/prop_barrel_group.glb (3 barrels, placements market_barrels, inn_barrels) -> replaces it
- **crate**: NEW: single breakable crate (dungeons currently draw kit barrels as crates)
- **crate_stack**: DERIVED: size of models/town/martsirt_v2_2/props/prop_crate_stack.glb (placement forge_crates, inn.json) -> replaces it
- **sack**: NEW: single sack
- **sack_pile**: DERIVED: props_gothic_v1 loot/sack_pile_closed/opened -> replaces them as a breakable pair
- **iron_chest_lite**: DERIVED (lite): decimated from props_gothic_v1 iron chest (24k -> 3k), opened = lid node rotated
- **bookshelf_worn_lite**: DERIVED (lite): decimated from props_gothic_v1 bookshelf_worn
- **shrine_basic_lite**: DERIVED (lite): decimated from batch1_interactables/v4/shrine_basic
- **shrine_weeping_angel_lite**: DERIVED (lite): decimated from batch1_interactables/v4/shrine_weeping_angel
- **pier_lite**: DERIVED (lite): decimated from local Poly Haven pier (not a repo file); modular sections kept in source layout

KayKit Dungeon had barrels, crates, tables and shelves, but it is a cartoon style, so it was not used.
Build scripts: `src/build_new.py`, `src/build_lite.py` (Blender 4.2). Not wired into the game: no placements or JSONs were edited.
