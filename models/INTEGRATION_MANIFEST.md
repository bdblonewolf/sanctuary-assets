# Integration manifest - environment GLBs

Generated Nov 2, 2026 from the files on `main`. 624 environment GLBs (models/outdoor, models/town, models/env_extra, models/shrines, models/props_new, plus root brazier, dungeon_props, worn_banner, modular_dungeon_kit). Weapons, items and hero models are left out. Full per-file data is in `models/INTEGRATION_MANIFEST.json`: path, category, status, MB, tris (colliders excluded), size in m (X x Y x Z), Ymin, LOD nodes, sway nodes and attribute, colliders, seasons, extensions, placement hint.

All files are 1 unit = 1 m with +Y up. Hide `col_*` nodes at load. The status column follows ASSET_MAP.md. This file does not change ASSET_MAP.md, GLB_LIST.md, placements.json or any collider.

## By folder

| Folder | GLBs | Status | Category | LODs | Sway | Seasons | Placement hint |
|---|---|---|---|---|---|---|---|
| `models/` | 4 | UNVERIFIED (root file, not in live list) | dungeon, misc, prop | - | - | - | - |
| `models/env_extra/cliffkit_v1/` | 30 | READY | cliff, fx | - | nodes | bare, dead | 2 m grid, tiers at y=-4,-8 |
| `models/env_extra/cliffkit_v2/` | 30 | READY | cliff, fx | - | nodes | bare, dead | 2 m grid, tiers at y=-4,-8 |
| `models/env_extra/hellgates/` | 3 | READY | hellgate | - | - | - | cut terrain at ground_hole_*, trigger_hellgate |
| `models/env_extra/interactables/` | 3 | READY | interactable | - | - | - | hinge pivots, see README |
| `models/env_extra/props_gothic_v1/boats/` | 2 | READY | boat | - | - | - | origin at waterline |
| `models/env_extra/props_gothic_v1/loot/` | 22 | READY | prop | - | - | - | ground at y=0; hide col_* at load |
| `models/env_extra/props_gothic_v1/props/` | 21 | READY | prop | - | - | - | ground at y=0; hide col_* at load |
| `models/outdoor/trees_gothic_v6/` | 30 | READY | tree | LOD0, LOD1, LOD2 | nodes + TEXCOORD_1 | autumn, summer, winter | instance from tree JSONs; one LOD child visible (0/35/80 m), cull ~160 m |
| `models/outdoor/v3trees/` | 6 | LIVE (superseded by trees_gothic_v6 READY) | tree | LOD0, LOD1 | nodes + COLOR_0 | autumn, bare, lush, snow | instance from tree JSONs; one LOD child visible (0/35/80 m), cull ~160 m |
| `models/outdoor/v5/` | 20 | LIVE | backdrop, fx, sky | - | - | autumn, dead, summer, winter | static, no collision, far ring |
| `models/outdoor/v5/plants/` | 9 | LIVE | plant, tree | - |  +  | dead | scatter per instance JSON |
| `models/outdoor/v5/trees/` | 5 | LIVE | tree | LOD0, LOD1, LOD2 |  + COLOR_0 | - | instance from tree JSONs; one LOD child visible (0/35/80 m), cull ~160 m |
| `models/outdoor/v5_maps/` | 49 | LIVE | backdrop, fx, shore | - | - | autumn, dead, summer, winter | static, no collision, far ring |
| `models/outdoor/v5_maps/border/` | 184 | LIVE | border | - | - | autumn, dead, summer, winter | map edge, use with existing edge colliders (do not change) |
| `models/outdoor/v5_maps/rect/` | 60 | LIVE | backdrop | - | - | autumn, dead, summer, winter | static, no collision, far ring |
| `models/outdoor/v5_maps/statues/` | 1 | LIVE | statue | - | - | - | static |
| `models/props_new/` | 12 | READY | prop | - | - | - | ground at y=0; hide col_* at load |
| `models/props_new/breakables/` | 20 | READY | breakable | - | - | - | swap _intact -> _broken on hit; hide col_* at load |
| `models/props_new/lite/` | 6 | READY | prop_lite | - | - | - | low-end/far LOD of the full prop |
| `models/shrines/` | 2 | LIVE | shrine | - | - | - | click to heal, FX via shrine_fx.json |
| `models/town/martsirt/buildings/chapel_st_noll/` | 2 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/cottage_ness/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/forge/v2/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/gatehouse_south/` | 3 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/graveyard/` | 1 | OLD | building | - | - | - | placements.json drives position |
| `models/town/martsirt/buildings/herbs_ysara/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/inn/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/lodge_orrin/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/mill/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/scriptorium_quill/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/square/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/stable/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/buildings/watchhouse_gibbet/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt/kit/glb/` | 21 | OLD | misc | - | nodes | - | - |
| `models/town/martsirt/props/` | 12 | OLD | prop, tree | - | nodes +  | dead | ground at y=0; hide col_* at load |
| `models/town/martsirt_v2/buildings/chapel_st_noll/` | 2 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/cottage_ness/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/forge/v2/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/gatehouse_south/` | 3 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/graveyard/` | 1 | OLD | building | - | - | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/herbs_ysara/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/inn/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/lodge_orrin/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/mill/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/scriptorium_quill/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/square/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/stable/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/buildings/watchhouse_gibbet/` | 1 | OLD | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2/props/` | 9 | OLD | prop, tree | - | nodes +  | dead | ground at y=0; hide col_* at load |
| `models/town/martsirt_v2_2/buildings/chapel_st_noll/` | 2 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/cottage_ness/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/forge/v2/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/gatehouse_south/` | 3 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/graveyard/` | 1 | LIVE | building | - | - | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/herbs_ysara/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/inn/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/lodge_orrin/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/mill/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/scriptorium_quill/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/square/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/stable/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/buildings/watchhouse_gibbet/` | 1 | LIVE | building | - | nodes | - | placements.json drives position |
| `models/town/martsirt_v2_2/dressing/` | 7 | LIVE | dressing, tree | - |  +  | - | placements.json drives position |
| `models/town/martsirt_v2_2/props/` | 8 | LIVE | prop | - | - | - | ground at y=0; hide col_* at load |

## Mismatches (ASSET_MAP.md / GLB_LIST.md vs disk)

- **on_disk_not_in_GLB_LIST**: 3:
  - `models/town/martsirt_v2_2/dressing/creek_water_col.glb`
  - `models/town/martsirt_v2_2/props/prop_seat_log.glb`
  - `models/town/martsirt_v2_2/props/prop_seat_stone_bench.glb`
- **props_new_not_yet_listed (expected; GLB_LIST/ASSET_MAP left untouched)**: 38:
  - all 38 files in models/props_new/ (see props_new/README.md)
- **in_GLB_LIST_missing_on_disk**: 0
- **ASSET_MAP_path_missing_on_disk**: 0
- **env_folders_not_in_ASSET_MAP**: 0

## Superseded sets

| Old | Use instead | Note |
|---|---|---|
| models/town/martsirt/ , models/town/martsirt_v2/ | models/town/martsirt_v2_2/ | ASSET_MAP rule 5 (OLD) |
| models/outdoor/v3trees/* and in-map v5 trees tree_conifer_a/b/c_v5, tree_decid_a/b_v5 | models/outdoor/trees_gothic_v6/ | READY, approved Nov 1; swap table in ASSET_MAP |
| models/knight_anim.glb | models/knight_anim_v10b.glb | hero (non-env, noted) |
| models/env_extra/cliffkit_v1/ | models/env_extra/cliffkit_v2/ | v1 kept as low-end fallback |
| models/town/martsirt_v2_2/props/prop_barrel_group, prop_crate_stack; models/town/martsirt/props/prop_cart_broken (OLD set) | models/props_new/breakables/barrel_group_*, crate_stack_*, models/props_new/cart_* | READY breakable intact/broken pairs (see props_new/README.md) |
| models/env_extra/props_gothic_v1 burial_urn, weapon_rack_wreck, sack_pile | models/props_new/breakables/urn_*, weapon_rack_*, sack_pile_* | READY breakable pairs |
| models/shrines/*, interactables chest, props_gothic_v1 bookshelf, pier | models/props_new/lite/* | lite = extra low-end LOD, NOT a replacement |

## Extensions

4 environment files use glTF extensions (mostly `EXT_texture_webp`). Browsers load them; headless Node cannot decode webp: `models/brazier.glb`, `models/dungeon_props.glb`, `models/modular_dungeon_kit.glb`, `models/worn_banner.glb`
