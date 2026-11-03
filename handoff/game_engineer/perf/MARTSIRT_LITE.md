# Martsirt lite pass (exterior)

Add-only. Every output is a new sibling file (`<name>_lite.glb`, `*_512.jpg`, `manifest_lite.json`). No live GLB, placements.json,
martsirt_world.json, interior JSON, collider, manifest.json, asset_version.txt, ASSET_MAP.md, GLB_LIST.md or code was touched.
Masters untouched. Full per-file data: `martsirt_lite_manifest.json` (same folder).

## Switch-over (engine, one go)
1. For the Martsirt exterior, load `files[].lite` instead of `files[].live` (61 files: 31 town_core, life/shrine/tree, gothic, characters props).
   Characters props: live is fetched from the pinned commit `2c3e35bf` path; the lite files are on **main** at `characters_art/props/<name>_lite.glb`
   (built from the pinned bytes) – point the loader at main for these.
2. Fetch `models/town/martsirt_v2_2/materials/manifest_lite.json` instead of `manifest.json` (same schema, tex_1k entries → `_512.jpg`).
3. Ground: use `textures.ground.map` in the manifest (live → `_512.jpg`, grass baseColor kept 1k). Splat/AO data maps unchanged.
4. Interiors keep loading the **live** GLBs (interior-only names `shell_`, `up_`, `stairs*`, `win_glow`, `glass`, `upper_window` live there). Expect the
   live + lite copy of a building to both be cached once a player goes inside – free the exterior lite on interior entry if memory is tight.
5. bump asset_version.txt yourself when switching (I did not).

## Results (instance-multiplied, engine visibility rules)
| Group | MB | visible tris | draw calls | shadow draws | embedded tex GPU MB |
|---|---|---|---|---|---|
| town_core | 37.81 → 16.87 | 539,261 → 189,227 | 1855 → 1322 | 1185 → 714 | 0 → 0 |
| life (trees, shrine, char props) | 19.14 → 4.6 | 156,567 → 40,368 | 16 → 16 | 5 → 5 | 397.34 → 38.67 |
| gothic | 5.69 → 4.3 | 26,314 → 14,516 | 82 → 81 | 25 → 24 | 134.85 → 100.85 |
| **ALL** | **62.65 → 25.77** | **722,142 → 244,111** | **1953 → 1419** | **1215 → 743** | |

Texture memory (GPU estimate w·h·4·4/3): material manifest 277.4 → 97.4 MB, ground 46.7 → 18.7 MB, embedded 532.2 → 139.5 MB,
**total ≈ 856 → 256 MB (−70 %)**. Texture download: manifest 11.1 → 4.9 MB, ground 3.6 → 1.6 MB.

Target check: town tris 150–200k → **189k ✔**. Texture memory: large cut ✔. Draw calls: **−29 % town core (−38 % excluding palisade) – partial miss**, see below.

### Town core per file (tris and draws × instances)
| file | inst | tris | draws | MB |
|---|---|---|---|---|
| bld_inn_salted_kettle_shared | 1 | 41,890 → 15,625 | 387 → 168 | 4.14 → 1.63 |
| bld_forge_wolchen_v2_shared | 1 | 36,479 → 11,806 | 165 → 82 | 3.04 → 1.24 |
| bld_chapel_st_noll_shared | 1 | 21,573 → 12,284 | 76 → 46 | 1.92 → 1.28 |
| bld_chapel_st_noll_tower_shared | 1 | 11,982 → 4,563 | 19 → 10 | 1.06 → 0.48 |
| bld_graveyard_st_noll_shared | 1 | 16,514 → 7,710 | 62 → 30 | 1.56 → 0.84 |
| bld_herbs_ysara_shared | 1 | 44,318 → 8,534 | 88 → 62 | 3.35 → 0.90 |
| bld_scriptorium_quill_shared | 1 | 39,677 → 11,258 | 82 → 60 | 3.55 → 1.14 |
| bld_gatehouse_south_shared | 1 | 36,760 → 13,717 | 63 → 39 | 3.32 → 1.37 |
| seg_curtain_wall_4m_shared | 2 | 2,576 → 1,158 | 16 → 10 | 0.12 → 0.06 |
| bld_mill_shared | 1 | 33,255 → 8,736 | 62 → 43 | 2.83 → 0.90 |
| bld_cottage_ness_shared | 1 | 25,718 → 7,954 | 59 → 40 | 2.27 → 0.76 |
| bld_lodge_orrin_shared | 1 | 12,923 → 4,918 | 57 → 47 | 1.23 → 0.49 |
| bld_stable_shared | 1 | 32,169 → 12,611 | 81 → 62 | 2.38 → 1.23 |
| bld_watchhouse_gibbet_shared | 1 | 14,422 → 7,936 | 49 → 35 | 1.33 → 0.79 |
| bld_square_shared | 1 | 26,392 → 9,023 | 24 → 23 | 3.65 → 2.40 |
| prop_fence_wattle_2m | 26 | 4,420 → 2,236 | 52 → 52 | 0.02 → 0.01 |
| prop_market_stall_c | 1 | 1,819 → 419 | 6 → 6 | 0.16 → 0.05 |
| prop_barrel_group | 5 | 10,020 → 3,740 | 15 → 15 | 0.17 → 0.07 |
| prop_bonfire_main | 1 | 1,554 → 1,283 | 7 → 7 | 0.18 → 0.14 |
| prop_campfire | 2 | 1,340 → 992 | 12 → 12 | 0.08 → 0.06 |
| prop_crate_stack | 4 | 1,168 → 376 | 8 → 8 | 0.03 → 0.01 |
| seg_palisade_4m_shared | 111 | 95,682 → 24,309 | 444 → 444 | 0.07 → 0.03 |
| dress_trees | 1 | 15,690 → 9,142 | 2 → 2 | 0.78 → 0.52 |
| dress_rocks | 1 | 3,360 → 1,726 | 1 → 1 | 0.13 → 0.08 |
| dress_fences | 1 | 2,148 → 1,914 | 1 → 1 | 0.13 → 0.13 |
| dress_graveyard | 1 | 460 → 385 | 1 → 1 | 0.04 → 0.03 |
| dress_clutter | 1 | 648 → 648 | 2 → 2 | 0.04 → 0.04 |
| creek | 1 | 4,068 → 4,068 | 3 → 3 | 0.21 → 0.21 |
| prop_seat_stone_bench | 5 | 180 → 130 | 10 → 10 | 0.01 → 0.00 |
| prop_seat_log | 1 | 56 → 26 | 1 → 1 | 0.01 → 0.00 |
| creek_water_col | 1 | 0 → 0 | 0 → 0 | 0.01 → 0.01 |

## Method (scripts kept on the box in /workspace/mlite, glTF-Transform 4 + meshoptimizer 1.3)
1. **Dump & classify** every node: code-looked-up names (col_, nav_, npc_spot_, fx_, sway_*, interact, creek_banks, WANTS_EXTRA incl. shutter/gutter, door/gate/hatch/wheel/sign_/lantern/bell = moving) are never merged, renamed, reparented or moved.
2. **Cull** hidden/interior/bottom faces: per-triangle ray-cast visibility (embree) from the D2 camera cone at every placement rotation, with the ground plane as occluder; a face is kept if any sample is camera-visible or it can cast a shadow onto something visible. Floor undersides, faces inside walls, buried bark and the buried shrine plinth go. Col_/code-named/moving prims are never culled, and any cull that changes a bbox-relevant prim's bbox by > 1 cm is reverted.
3. **Decimate**: meshopt simplify with lock-border; boxy seam-heavy building meshes use Permissive+Prune at error 0.03 (palisade 0.10, props 0.025, gothic 0.015, trees 0.02) – silhouettes checked from the 50° D2 camera.
4. **Attribute diet**: dropped TANGENT (three.js derives them), unused TEXCOORD_n, all-white COLOR_0, and stray JOINTS/WEIGHTS on unskinned files; then weld. Positions/normals stay float32 (no quantisation, no meshopt/Draco/KTX).
5. **Merge per material per block**: static, non-code-named meshes are joined per material into their host block node (never across blocks, never touching col_/sway_/fx_ nodes). Materials are **not** deduped by content – the engine paints by material name.
6. **Dedupe** accessors and textures. 7. **Textures** to 512 (embedded and manifest), small gothic props to 256.
8. **Validate**: glTF validator 0 errors on all 61 files (only GENERATED_TANGENT_SPACE info/warnings where tangents were dropped).
9. **Verify**: root names + transforms identical, every preserved node present with identical transform, every col_ bbox identical; for no-col files
   (dress_graveyard, dress_clutter, creek, tree) every per-mesh bbox identical because the engine builds colliders from them.

Preserved names: 1,569 across 61 files (854 col_, 166 fx_, 118 sway_, 84 shutter, 54 nav_, 34 npc_spot_, 24 gutter, 23 interact, 12 door, creek_banks, + 199 other named roots/anchors such as chimney_*, ground_mud). Full list per file in the manifest.

## Hero 1k textures (justified)
- `m_stone_ashlar_limestone` baseColor – chapel + tower facade, the biggest lit vertical surface on screen; at 512 the ashlar coursing aliases into noise from the D2 camera. Its normal map is 512.
- `ground_v1/g_grass_bc` – the main ground, covers most of every frame.
Everything else is 512 (256 for small gothic props).

## Caveats / misses
- **Draw calls (partial miss)**: the palisade is 111 instances × 4 materials = 444 draws, wattle fence 52 – this needs engine `InstancedMesh` (one per material), which would take town core from 1,322 to ≈ 880 draws. Remaining building draws are mostly shutters/sway/wantsExtra and door nodes deliberately kept separate (code animates or swaps them). Inn 387 → 168.
- Bbox changes > 1 cm (all collider-safe): forge 0.03 m, graveyard 0.097 m (small pieces merged), market stall 0.025, palisade 0.015, dress_trees 0.39 m and shrine 0.67 m (buried geometry culled – bottom only, not visible).
- Tree, hanging sign and iron gate were mostly protected (sway/moving names), so their reduction is small.
- Gothic small props are 256 (deviation from the 512 rule, they are < 1.5 m on screen).
- Renders are Cycles approximations (no engine shaders/lights); the black squares are untextured decal/notice planes in both versions.

## castShadow = false candidates (279 nodes, ≈ 22,877 tris; full list in the manifest)
| file | node | material | tris | why |
|---|---|---|---|---|
| `bld_stable_shared_lite.glb` | `straw_yard_strands` | `m_straw_strand` | 5083 | flat (<0.35 m tall) |
| `kite_shield_sanctuary_lite.glb` | `kite_shield_sanctuary` | `M_kite_shield_sanctuary` | 2536 | small prop under 1.6 m |
| `bld_watchhouse_gibbet_shared_lite.glb` | `notice_travel` | `m_ink_tar` | 2300 | small (<0.8 m tall, <1 m wide) |
| `chains_shackles_v1_lite.glb` | `chains` | `m_iron` | 1094 | small prop under 1.6 m |
| `gargoyle_perched_v1_lite.glb` | `gargoyle_pedestal` | `m_gargoyle_stone` | 1032 | small prop under 1.6 m |
| `bld_scriptorium_quill_shared_lite.glb` | `door_note` | `m_ink` | 960 | flat (<0.35 m tall) |
| `bld_herbs_ysara_shared_lite.glb` | `interior` | `m_glass_stained` | 594 | emissive/decal/glass material |
| `gibbet_cage_v1_lite.glb` | `cage` | `m_bone` | 474 | small prop under 1.6 m |
| `bld_inn_salted_kettle_shared_lite.glb` | `props_inn` | `m_glass_stained` | 380 | emissive/decal/glass material |
| `bld_square_shared_lite.glb` | `statue_plinth` | `m_ink_tar` | 350 | flat (<0.35 m tall) |
| `wall_niche_saint_v1_lite.glb` | `niche` | `m_saint_stone` | 344 | small prop under 1.6 m |
| `bld_forge_wolchen_v2_shared_lite.glb` | `hearth_coals` | `m_coal_glow` | 244 | flat (<0.35 m tall) |
| `lectern_book_v1_lite.glb` | `lectern` | `m_wood_dark` | 236 | small prop under 1.6 m |
| `bld_stable_shared_lite.glb` | `straw_yard_mound` | `m_roof_thatch` | 208 | flat (<0.35 m tall) |
| `bld_inn_salted_kettle_shared_lite.glb` | `hearth_coals` | `m_coal_glow` | 188 | flat (<0.35 m tall) |
| `bld_inn_salted_kettle_shared_lite.glb` | `decals_inn` | `m_decal_atlas` | 174 | emissive/decal/glass material |
| `bld_gatehouse_south_shared_lite.glb` | `guard_props` | `m_coal_glow` | 170 | flat (<0.35 m tall) |
| `bld_square_shared_lite.glb` | `well` | `m_stone_ashlar_limestone` | 161 | flat (<0.35 m tall) |
| `bld_watchhouse_gibbet_shared_lite.glb` | `gibbet_frame` | `m_stone_rubble_soot` | 147 | small (<0.8 m tall, <1 m wide) |
| `bld_herbs_ysara_shared_lite.glb` | `interior` | `m_coal_glow` | 144 | flat (<0.35 m tall) |
| `bld_stable_shared_lite.glb` | `straw_stalls_strands` | `m_straw_strand` | 127 | flat (<0.35 m tall) |
| `bld_chapel_st_noll_shared_lite.glb` | `decals_chapel` | `m_decal_atlas` | 116 | emissive/decal/glass material |
| `tombstone_gothic_v1_lite.glb` | `stone` | `m_stone_mossy` | 104 | small prop under 1.6 m |
| `bld_watchhouse_gibbet_shared_lite.glb` | `braziers` | `m_brazier_coals` | 101 | emissive/decal/glass material |
| `bld_mill_shared_lite.glb` | `sign_mill` | `m_metal_wrought_rust` | 100 | small (<0.8 m tall, <1 m wide) |

Also turn shadows off for every material matching `glass`, `coal_glow`, `decal`, `fire_`, `ember`, and for flat ground pieces (`ground_*`, `plaza`).

## Renders (`renders/`, D2 50° camera, no tilt)
`town_overview_compare.jpg` (ortho), `inn_compare.jpg`, `forge_compare.jpg`, `chapel_compare.jpg`, `gatehouse_compare.jpg`; single `*_before.jpg` / `*_after.jpg` beside them.
