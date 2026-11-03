# models/items: item atlas masters and mobile copies

## Which file is which
- **Masters:** `items_armor.glb`, `items_belts.glb`, `items_gloves.glb`, `items_helms.glb`, `items_jewelry.glb`, `items_misc.glb` and `items_shields.glb`. These are the live files that `ITEM_MAP.json` points at. They are the source of truth. Edit these, never the `_c` copies.
- **Mobile copies:** `items_<name>_c.glb`, one next to each master. They are derived from the masters and add-only. They were never hand-edited, and they're regenerated from the master whenever the master changes.
- `ITEM_MAP.json` still references the masters. Switching the game to the `_c` files is an engineer decision and is not part of this commit.

## Sizes
| Master (live, untouched) | Mobile copy | MB before | MB after | Materials | Textures | Images (before → after) | ITEM_MAP nodes checked |
|---|---|---|---|---|---|---|---|
| `items_armor.glb` | `items_armor_c.glb` | 4.37 | 4.15 | 14 → 14 | 38 → 38 | 38 (38 jpeg) → 38 webp | 44 / 0 missing |
| `items_belts.glb` | `items_belts_c.glb` | 3.15 | 2.92 | 14 → 14 | 42 → 36 | 36 (11 jpeg, 25 webp) → 36 webp | 9 / 0 missing |
| `items_gloves.glb` | `items_gloves_c.glb` | 3.97 | 3.63 | 13 → 13 | 39 → 35 | 35 (11 jpeg, 24 webp) → 35 webp | 9 / 0 missing |
| `items_helms.glb` | `items_helms_c.glb` | 2.34 | 2.19 | 11 → 11 | 28 → 28 | 28 (28 jpeg) → 28 webp | 9 / 0 missing |
| `items_jewelry.glb` | `items_jewelry_c.glb` | 3.80 | 3.53 | 22 → 22 | 36 → 34 | 34 (11 jpeg, 23 webp) → 34 webp | 18 / 0 missing |
| `items_misc.glb` | `items_misc_c.glb` | 2.01 | 1.81 | 17 → 17 | 27 → 23 | 23 (7 jpeg, 16 webp) → 23 webp | 10 / 0 missing |
| `items_shields.glb` | `items_shields_c.glb` | 3.80 | 3.60 | 14 → 14 | 42 → 32 | 32 (9 jpeg, 23 webp) → 32 webp | 9 / 0 missing |
| **Total** | | **23.44** | **21.84** | 105 → 105 | 252 → 226 | | |

Total saving: 1.60 MB (6.8%). Geometry makes up most of every file, about 12.7 MB of the 23.4 MB total, and armor alone is about 3.6 MB of geometry. That size can only come down through decimation or quantization. Quantization is excluded on purpose, so no geometry was changed.

## Pipeline (gltf-transform 4.5.1)
1. `gltf-transform prune MASTER p.glb --keep-leaves true --keep-attributes true`. This keeps every empty or leaf node, so all ITEM_MAP nodes and children survive.
2. `gltf-transform dedup p.glb d.glb`. This collapses duplicate texture objects (belts 42→36, gloves 39→35, jewelry 36→34, misc 27→23, shields 42→32). Images were already unique, so no image was dropped.
3. `gltf-transform webp d.glb items_<name>_c.glb --formats jpeg --quality 85`. JPEGs are re-encoded as WebP. WebP images already in the masters are kept byte-for-byte, because re-encoding them made the files larger.
4. Resize was not applied. Every image in the masters is already 512 px or smaller, so the 1024 cap is a no-op. `gltf-transform resize` would also have re-encoded the images for nothing.
5. No materials were merged. Each material has its own baseColor, metallic/roughness factors and texture set, and the UVs are tiled well outside 0–1 (ranges such as -5…2 and up to about 16). Merging would mean re-baking into a new atlas and would change how the items look. Node, mesh and material names, and the node hierarchy, are identical to the master.
6. Extensions: every copy declares `EXT_texture_webp` in `extensionsUsed` (and in `extensionsRequired`). `items_misc_c.glb` also keeps `KHR_materials_emissive_strength`, the same as its master. No `EXT_meshopt_compression`, `KHR_draco_mesh_compression` or `KHR_mesh_quantization`, and the index buffers are uint16.

## Checks
- **gltf-validator 2.0.0-dev.3.10:** 0 errors on all 7 copies. The only warnings are `MESH_PRIMITIVE_GENERATED_TANGENT_SPACE`, which the masters have too.
- For comparison, 5 of the masters fail validation: they embed `image/webp` without declaring `EXT_texture_webp` (`IMAGE_NON_ENABLED_MIME_TYPE` and `TEXTURE_INVALID_IMAGE_MIME_TYPE`). The `_c` copies fix that.
- **ITEM_MAP:** every `bases[].node`, `children[]`, `worn.*.parts[].node` and `kinds[].node` served by each atlas exists in its `_c` copy. 0 are missing.
- **Spot render** (Blender Cycles, master vs `_c`, same camera): Obsidian Cuirass + children, Wick Coat + children, Rite Crown, Obsidian Aegis, War Gauntlets, Weald Belt, Inquisitor's Seal, Obsidian Tear and potion. The mean absolute pixel difference is 0.11/255 or less, and the 99th percentile is 6/255 or less. The copies are visually identical.
