# ASSET_MAP.md - where every Sanctuary asset is

Single guide for Grok Build. Repo: https://github.com/bdblonewolf/sanctuary-assets (branch `main`).
Raw URL pattern for ANY file: `https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/<path>`
Example: `https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/npcs/martsirt/wolcen.glb`
Updated: Nov 1, 2026.

> ## RULES
> 1. **Game-ready 3D models are ONLY in `models/` and `characters_art/`.** Every file there is a finished glTF 2.0 `.glb` (1 unit = 1 m, +Y up) that three.js `GLTFLoader` loads directly.
> 2. **2D images (concept art, reference, previews) are ONLY in `art_2d/`.** Nothing in `art_2d/` is a model. Do not conclude a character is "2D only" because you found its art in `art_2d/`; check `characters_art/` first.
> 3. **NPC outfits are mesh NODES inside the NPC's GLB, not separate files.** `characters_art/npcs/martsirt/wolcen.glb` and `quill.glb` each hold the bare body, hair, outfit, props and animations in one file. Toggle outfit/body parts by node name.
>    The exceptions with separate piece files are the clothing sets in `characters_art/clothing/*/pieces/` and Ayla's pieces in `characters_art/npcs/ayla_phimn/pieces/`. (No monster `outfit_<set>_<slot>.glb` files exist in this repo yet; if they are added they follow that name pattern.)
> 4. `wip_models/` = unfinished (Blender sources, test bodies). Never load in the game.
> 5. `models/town/martsirt/` and `models/town/martsirt_v2/` are OLD. Use `models/town/martsirt_v2_2/`.
> 6. Dungeon pieces the live game uses (`modular_dungeon_kit.glb`, `dungeon/wall*.gltf.glb`, ...) load from `/assets3d/` inside Grok Build's own project, not from this repo.
> 7. Bone names in the files are `mixamorig:Hips` etc. three.js GLTFLoader strips the colon, so at runtime they are `mixamorigHips`.
> 8. File lists: `models/GLB_LIST.md` (all GLBs under models/), `characters_art/GLB_LIST.md`, `wip_models/WIP_LIST.md`, `art_2d/ART_LIST.md`, `audio/AUDIO_PATHS.md`.

Status key: **LIVE** = the live game loads it now. **READY** = finished, game-ready, not used live yet. **OLD** = superseded, do not use. **WIP** = unfinished. **2D** = images only.

---

## models/ - environment, weapons, hero, items (LIVE unless noted)

### Hero - LIVE
- `models/knight_anim_v10b.glb` (rigged, animated hero). `models/knight_anim.glb` is the older hero (OLD).
- Other root files (not in the verified live list): armored_guard_knight, plated_knight, plated_knight_rigged, skeleton_animated, brazier, dungeon_props, worn_banner, holster_back, holster_dagger, modular_dungeon_kit (the game uses its own /assets3d copy of the dungeon kit). `models/pieces_index.json` indexes kit pieces.

### Weapons - LIVE
- `models/weapon_*.glb` (13): weapon_arrow, weapon_axe, weapon_bow, weapon_dagger, weapon_greataxe, weapon_greatsword, weapon_mace, weapon_shield, weapon_spear, weapon_staff, weapon_sword, weapon_sword_v2, weapon_wand
- `models/weapons/` (30): weapon_ash_longbow, weapon_ash_saber, weapon_ash_staff, weapon_briar_hatchet, weapon_chapel_maul, weapon_chapel_staff, weapon_cinder_axe, weapon_ferry_pike, weapon_inquisitors_nail, weapon_kingrender, weapon_lid_glaive, weapon_mercy_hammer, weapon_mourning_spear, weapon_omen_wand, weapon_parish_blade, weapon_sable_cleaver, weapon_seam_knife, weapon_spire_falchion, weapon_spire_longbow, weapon_spite_wicker, weapon_sting_wand, weapon_stitched_blade, weapon_thorn_wand, weapon_thorn_wicker, weapon_timber_axe, weapon_war_axe, weapon_weald_staff, weapon_wicker_bow, weapon_widow_stitch, weapon_yew_longbow

### Items - LIVE
- `models/items/` : items_armor, items_belts, items_gloves, items_helms, items_jewelry, items_misc, items_shields. Index of atlases, icons and item meshes: `models/items/ITEM_MAP.json`.

### Shrines - LIVE
- `models/shrines/` : shrine_basic.glb, shrine_weeping_angel.glb (final v4). FX data for them: `models/env_extra/interactables/shrine_fx.json` + `heal_motes_8x8.png`.

### Outdoor - LIVE
- `models/outdoor/v5/` : mountain backdrop rings (backdrop_mountain_ring_v5_<summer|autumn|winter|dead>_<near|mid|far>), sky domes (day, dusk, overcast, dead), sky_cloud_layers_v5, fog_valley_banks_v5, fx_crow_flock_v5, fx_godrays_v5, `manifest_v5.json`. Subfolders `trees/` (tree_conifer_a_v5, tree_conifer_b_v5, tree_conifer_c_v5, tree_decid_a_v5, tree_decid_b_v5 + instance JSONs), `plants/` (plant_agave_a_v5, plant_cactus_cluster_b_v5, plant_cactus_column_a_v5, plant_palm_date_a_v5, plant_palm_date_b_v5, plant_palm_date_c_v5, plant_scrub_bush_a_v5, tree_dead_a_v5, tree_dead_b_v5), `ocean/` (ocean_normal_v1.jpg).
- `models/outdoor/v5_maps/` : per-map backdrops (backdrop_near_c23/c30/c36/c42/c52_<season>, backdrop_islands_isle/mires(_v2)_<season>), shore_rock_kit_v5, shore_foam_strips_v5, tree instance JSONs, `maps_backdrop_v5.json`, README.md. Subfolders `border/` (148: beach_sand/shingle, seacliff_* pieces, border_kit), `rect/` (60: backdrop_near_rect_*), `statues/` (statue_angel_hero_bust).
- `models/outdoor/v5_ground/` : ground PBR textures in `materials/<ash|dirt_mud|grass_dark|grass_dead|road|sand_coast|sand_desert>/` + `ground_manifest.json`, GROUND_BLEND_NOTE.md.
- `models/outdoor/v3trees/` : tree_oak_gnarled_autumn, tree_oak_gnarled_b_lush, tree_oak_gnarled_bare, tree_oak_gnarled_lush, tree_pine_dark, tree_pine_dark_snow.

### Town (Martsirt) - LIVE: `models/town/martsirt_v2_2/`
- `props/` : prop_barrel_group, prop_bonfire_main, prop_campfire, prop_crate_stack, prop_fence_wattle_2m, prop_market_stall_c
- `dressing/` : creek, dress_clutter, dress_fences, dress_graveyard, dress_rocks, dress_trees
- `buildings/<name>/` : chapel_st_noll, cottage_ness, forge (`forge/v2/bld_forge_wolchen_v2_shared.glb`), gatehouse_south (+ curtain wall / palisade segments), graveyard, herbs_ysara, inn, lodge_orrin, mill, scriptorium_quill, square, stable, watchhouse_gibbet (files `bld_*_shared.glb`).
- `placements.json` (where everything goes), `martsirt_world.json`, `materials/` (manifest.json, tex_1k, tex_2k).
- `models/town/ground_v1/` : town ground textures + splat/AO maps (not in the verified live list).
- **OLD, do not use:** `models/town/martsirt/`, `models/town/martsirt_v2/`.

### Env extra - READY (not used live yet): `models/env_extra/`
All plain GLB, textures embedded (no external files), no extensions, 1 u = 1 m, +Y up. Each file was load-checked. Tris = visible (colliders `col_*` excluded; hide `col_*` at load). Height = bounding box height in m. Full notes: `models/env_extra/README.md` and each folder's README.

**`models/env_extra/props_gothic_v1/`** - gothic props, loot containers (closed/opened pairs), boats. Also `README.md`, `preview_boats.jpg`, `preview_gothic_props.jpg`, `preview_loot.jpg`, `props_gothic_v1.json`.
| File | Size | Tris | Height m |
|---|---|---|---|
| `boats/boat_longship_ride_v1.glb` | 2.16 MB | 14,672 | 9.84 |
| `boats/boat_wreck_cave_v1.glb` | 2.09 MB | 11,595 | 8.69 |
| `loot/bone_pile_closed.glb` | 0.27 MB | 1,360 | 0.47 |
| `loot/bone_pile_opened.glb` | 0.27 MB | 1,360 | 0.24 |
| `loot/burial_urn_closed.glb` | 0.27 MB | 742 | 0.87 |
| `loot/burial_urn_opened.glb` | 0.37 MB | 826 | 0.39 |
| `loot/hollow_log_closed.glb` | 0.23 MB | 508 | 0.62 |
| `loot/hollow_log_opened.glb` | 0.26 MB | 1,098 | 0.61 |
| `loot/remains_heap_closed.glb` | 0.38 MB | 1,100 | 0.31 |
| `loot/remains_heap_opened.glb` | 0.40 MB | 1,232 | 0.23 |
| `loot/rock_pile_closed.glb` | 0.34 MB | 720 | 0.83 |
| `loot/rock_pile_opened.glb` | 0.35 MB | 1,060 | 0.47 |
| `loot/rotten_stump_closed.glb` | 0.25 MB | 840 | 0.79 |
| `loot/rotten_stump_opened.glb` | 0.36 MB | 916 | 1.03 |
| `loot/rubble_cache_closed.glb` | 0.37 MB | 1,156 | 0.73 |
| `loot/rubble_cache_opened.glb` | 0.40 MB | 1,912 | 0.64 |
| `loot/sack_pile_closed.glb` | 0.16 MB | 500 | 0.6 |
| `loot/sack_pile_opened.glb` | 0.28 MB | 1,024 | 0.14 |
| `loot/sarcophagus_small_closed.glb` | 0.13 MB | 324 | 0.67 |
| `loot/sarcophagus_small_opened.glb` | 0.37 MB | 1,276 | 0.65 |
| `loot/skull_heap_closed.glb` | 0.29 MB | 1,732 | 0.61 |
| `loot/skull_heap_opened.glb` | 0.29 MB | 1,732 | 0.29 |
| `loot/weapon_rack_wreck_closed.glb` | 0.27 MB | 320 | 1.77 |
| `loot/weapon_rack_wreck_opened.glb` | 0.18 MB | 218 | 0.11 |
| `props/altar_cloth_v1.glb` | 0.46 MB | 1,526 | 1.7 |
| `props/anvil_stump_v1.glb` | 0.21 MB | 516 | 1.01 |
| `props/candelabra_tall_v1.glb` | 0.20 MB | 1,520 | 2.16 |
| `props/cauldron_tripod_v1.glb` | 0.33 MB | 1,438 | 1.81 |
| `props/chains_shackles_v1.glb` | 0.16 MB | 2,440 | 1.36 |
| `props/church_pew_v1.glb` | 0.08 MB | 296 | 1.22 |
| `props/cobweb_cards_v1.glb` | 0.02 MB | 6 | 2.0 |
| `props/gargoyle_perched_v1.glb` | 0.33 MB | 1,290 | 2.38 |
| `props/gibbet_cage_v1.glb` | 0.47 MB | 2,362 | 3.68 |
| `props/grave_celtic_cross_v1.glb` | 0.29 MB | 844 | 2.11 |
| `props/hanging_sign_v1.glb` | 0.17 MB | 652 | 0.83 |
| `props/iron_fence_gothic_v1.glb` | 0.26 MB | 1,112 | 1.82 |
| `props/iron_gate_gothic_v1.glb` | 0.46 MB | 2,084 | 2.98 |
| `props/iron_maiden_v1.glb` | 0.39 MB | 1,944 | 2.09 |
| `props/lectern_book_v1.glb` | 0.38 MB | 488 | 1.41 |
| `props/sarcophagus_carved_v1.glb` | 0.37 MB | 3,020 | 1.27 |
| `props/tapestry_heraldic_v1.glb` | 0.18 MB | 404 | 2.79 |
| `props/tombstone_gothic_v1.glb` | 0.54 MB | 786 | 1.38 |
| `props/urn_plinth_v1.glb` | 0.14 MB | 768 | 1.83 |
| `props/wall_niche_saint_v1.glb` | 0.49 MB | 2,966 | 2.7 |
| `props/wall_sconce_v1.glb` | 0.15 MB | 342 | 0.56 |

**`models/env_extra/hellgates/`** - 3 Hell-gate graveyard entrances (stairs down into Hell-only areas; origin at ground level, the pit goes below y=0; cut terrain at `ground_hole_*`, use `trigger_hellgate`). Also `README.md`, `hellgate_preview_sheet.jpg`.
| File | Size | Tris | Height m |
|---|---|---|---|
| `hellgate_crypt_a.glb` | 3.69 MB | 35,259 | 5.95 |
| `hellgate_mausoleum_c.glb` | 3.53 MB | 32,084 | 7.41 |
| `hellgate_monolith_b.glb` | 3.59 MB | 27,672 | 7.47 |

**`models/env_extra/cliffkit_v2/`** - modular cliff kit v2 (prefer this one; 2 m grid, 4 m tiers stacking at y = -4, -8, ...). Also `cliff_kit_manifest.json`, `cliff_kit_v2_preview_sheet.jpg`.
| File | Size | Tris | Height m |
|---|---|---|---|
| `cliff_edge_broken_lip_4m.glb` | 2.38 MB | 7,202 | 4.63 |
| `cliff_edge_corner_inner.glb` | 2.47 MB | 9,718 | 4.64 |
| `cliff_edge_corner_outer.glb` | 2.46 MB | 9,696 | 4.61 |
| `cliff_edge_overhang_4m.glb` | 2.34 MB | 6,182 | 4.64 |
| `cliff_edge_straight_4m.glb` | 2.34 MB | 6,152 | 4.63 |
| `cliff_edge_straight_8m.glb` | 2.54 MB | 11,930 | 4.63 |
| `cliff_edge_waterfall_notch_8m.glb` | 2.53 MB | 11,752 | 4.62 |
| `cliff_wall_4m_deep.glb` | 1.30 MB | 3,360 | 4.2 |
| `cliff_wall_4m_ledge_roots.glb` | 2.30 MB | 4,324 | 4.2 |
| `cliff_wall_4m_mid.glb` | 1.30 MB | 3,360 | 4.2 |
| `cliff_wall_4m_upper.glb` | 1.30 MB | 3,360 | 4.2 |
| `cliff_wall_8m_deep.glb` | 1.41 MB | 6,720 | 4.2 |
| `cliff_wall_8m_mid.glb` | 1.41 MB | 6,720 | 4.2 |
| `cliff_wall_8m_upper.glb` | 1.41 MB | 6,720 | 4.2 |
| `cliff_wall_corner_inner_deep.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_corner_inner_mid.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_corner_inner_upper.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_corner_outer_deep.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_corner_outer_mid.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_corner_outer_upper.glb` | 1.38 MB | 5,964 | 4.2 |
| `cliff_wall_notch_8m_deep.glb` | 1.41 MB | 6,720 | 4.2 |
| `cliff_wall_notch_8m_mid.glb` | 1.41 MB | 6,720 | 4.2 |
| `cliff_wall_notch_8m_upper.glb` | 1.41 MB | 6,720 | 4.2 |
| `dead_stump_blighted.glb` | 0.74 MB | 442 | 2.59 |
| `dead_stump_blighted_dead.glb` | 0.66 MB | 442 | 2.59 |
| `dress_cliff_rope_remnant.glb` | 0.46 MB | 1,748 | 8.01 |
| `fx_waterfall_notch_ribbon_16m.glb` | 0.77 MB | 812 | 18.3 |
| `rock_spire_bare_16m.glb` | 1.93 MB | 22,524 | 22.35 |
| `rock_spire_bare_16m_dead.glb` | 2.06 MB | 22,524 | 22.35 |
| `sway_dead_grass_patch_2m.glb` | 0.14 MB | 78 | 0.58 |

**`models/env_extra/cliffkit_v1/`** - cliff kit v1, same file names as v2, lighter textures (fallback for low-end devices). Also `cliff_kit_manifest.json`, `cliff_kit_preview_sheet.png`.
| File | Size | Tris | Height m |
|---|---|---|---|
| `cliff_edge_broken_lip_4m.glb` | 0.97 MB | 1,348 | 4.27 |
| `cliff_edge_corner_inner.glb` | 0.96 MB | 1,558 | 4.26 |
| `cliff_edge_corner_outer.glb` | 0.96 MB | 1,556 | 4.26 |
| `cliff_edge_overhang_4m.glb` | 0.93 MB | 861 | 4.28 |
| `cliff_edge_straight_4m.glb` | 0.94 MB | 881 | 4.27 |
| `cliff_edge_straight_8m.glb` | 0.97 MB | 1,761 | 4.26 |
| `cliff_edge_waterfall_notch_8m.glb` | 0.99 MB | 2,314 | 4.3 |
| `cliff_wall_4m_deep.glb` | 0.48 MB | 800 | 4.0 |
| `cliff_wall_4m_ledge_roots.glb` | 1.12 MB | 1,770 | 4.0 |
| `cliff_wall_4m_mid.glb` | 0.48 MB | 800 | 4.0 |
| `cliff_wall_4m_upper.glb` | 0.48 MB | 800 | 4.0 |
| `cliff_wall_8m_deep.glb` | 0.51 MB | 1,600 | 4.0 |
| `cliff_wall_8m_mid.glb` | 0.51 MB | 1,600 | 4.0 |
| `cliff_wall_8m_upper.glb` | 0.51 MB | 1,600 | 4.0 |
| `cliff_wall_corner_inner_deep.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_corner_inner_mid.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_corner_inner_upper.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_corner_outer_deep.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_corner_outer_mid.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_corner_outer_upper.glb` | 0.50 MB | 1,440 | 4.0 |
| `cliff_wall_notch_8m_deep.glb` | 0.52 MB | 2,120 | 4.0 |
| `cliff_wall_notch_8m_mid.glb` | 0.52 MB | 2,120 | 4.0 |
| `cliff_wall_notch_8m_upper.glb` | 0.52 MB | 2,120 | 4.0 |
| `dead_stump_blighted.glb` | 0.58 MB | 442 | 2.59 |
| `dead_stump_blighted_dead.glb` | 0.50 MB | 442 | 2.59 |
| `dress_cliff_rope_remnant.glb` | 0.28 MB | 528 | 8.01 |
| `fx_waterfall_notch_ribbon_16m.glb` | 0.22 MB | 192 | 16.0 |
| `rock_spire_bare_16m.glb` | 0.51 MB | 1,620 | 16.8 |
| `rock_spire_bare_16m_dead.glb` | 0.46 MB | 1,620 | 16.8 |
| `sway_dead_grass_patch_2m.glb` | 0.14 MB | 66 | 0.47 |

**`models/env_extra/interactables/`** - final chest and doors (lid / door leaf pivot on hinge, see README). Also `README.md`, `heal_motes_8x8.png`, `preview_chest_doors.jpg`, `shrine_fx.json`.
| File | Size | Tris | Height m |
|---|---|---|---|
| `chest.glb` | 1.84 MB | 24,050 | 0.63 |
| `door.glb` | 1.98 MB | 25,658 | 2.99 |
| `door_gothic.glb` | 2.21 MB | 27,468 | 2.92 |

---

## characters_art/ - characters, NPCs, monsters, props (READY except NPCs)

### Martsirt NPCs - LIVE (live game pins commit 51d94e0; newest is pass 3, commit e4db7f2): `characters_art/npcs/martsirt/`
- `wolcen.glb`, `quill.glb` : **3D, full outfits included.** One skinned GLB per NPC, with mesh nodes:
  - `<id>_body_<region>` (arms, feet, hands, head, legs, torso) - bare body split by region
  - `<id>_hair`
  - `<id>_outfit_<slot>` (torso, legs, feet, hands) - the outfit meshes
  - `<id>_prop_*` (wolcen: hammer, tongs; quill: quill) and `<id>_keepsake` - rigid, parented to bones
  - Animation clips: idle, walk, talk, sit, sit_talk, work_* (wolcen work_hammer, quill work_write), sleep
- `MANIFEST.json` : per NPC `slots`, `slot_hides` (which body regions an outfit slot hides), `default_hidden_regions`, `props`, `clips`. `README.md` explains usage.
- The other 7 Martsirt NPCs have no 3D outfits yet (bare bodies using Wolcen's clips).

### Ayla of the Phimn - READY: `characters_art/npcs/ayla_phimn/`
- `ayla_phimn_body.glb`, `npc_f_ayla_phimn_ayla_phimn_body.glb`, `fit_notes.md`; `pieces/` = separate clothing piece GLBs (belt, boots, charms, hair, halter, loincloth, vambraces) each with a `.mask.json` (body regions to hide).

### Bodies - READY: `characters_art/bodies/` (12 bare bodies, mixamorig 52-bone)
- female_curvy, female_medium, female_medium_hourglass_a, female_medium_hourglass_b, female_skinny, female_thick, female_tiny, male_brute_heavy, male_brute_muscular, male_regular, male_skinny, male_vshape

### Clothing - READY: `characters_art/clothing/`
- `11_leather_bikini_white/`, `12_leather_bikini_redbrown/` : full fitted sets (`npc_f_leather_<color>_hourglass_a|b.glb`) + `pieces/` (one GLB per piece + `.mask.json`). `bodies_fit/` : the hourglass_a/b fit bodies. `manifest.json`, `fit_notes.md`.

### Monsters - READY: `characters_art/monsters/<name>/` (13 folders, one GLB each unless noted)
- archer, axeman, bone_archer, bone_axeman, bone_swordsman, corrupted_phimn (corrupted_phimn_caster + corrupted_phimn_feral), crawler, grave_old_man, grave_risen, rag_zombie, red_demon_spawnling, shambler, swordsman. Path: `characters_art/monsters/<name>/<name>.glb`. Notes: README_starter_batch1.md and per-folder READMEs (bone_* use a CC-BY-4.0 base, credit required).

### Props - READY: `characters_art/props/` (realistic, finished)
- false_door_sanctuary, gothic_statue_sanctuary, kite_shield_sanctuary, kneeling_winged_monster_sanctuary, kneeling_winged_monster_sanctuary_statue, kylix_sanctuary, large_castle_door_sanctuary, mourner, mourner_statue, reliquary, sekhmet_sanctuary, sekhmet_sanctuary_statue, wine_barrel_01_sanctuary. Credits: README.md, README_museum_mourner_reliquary.md.

### Statues - READY: `characters_art/statues/`
- statue_angel_hero_bust.glb (angel hero bust).

---

## Not models

| Folder | What | Status |
|---|---|---|
| `art_2d/` | concept art, reference images, preview renders (npc_concepts, refs_brian, sanctuary_art, sanctuary_env, sanctuary_npc). List: ART_LIST.md | **2D only** - not models |
| `wip_models/` | unfinished Blender sources (.blend), test body versions, WIP monsters (ossuary_footman, razor_tollman), statue v1. List: WIP_LIST.md | **WIP** - not game-ready |
| `audio/` | music (town, desert, dread, dungeon) + sfx (gold, impact, item, loot, player, potion, ui, vendor, weapon). Paths: AUDIO_PATHS.md | LIVE / ready |
| `hud/`, `icons/` | HUD frame + orbs; item icon atlas (items_icons.png + .json) | 2D UI |
| `handoff/game_engineer/` | HANDOFF.md, design docs (`design/`), stage prompts (`prompts/`), audio notes | docs |
