# models/items: item atlas masters and mobile copies

## Which file is which
- **Masters:** `items_armor.glb`, `items_belts.glb`, `items_gloves.glb`, `items_helms.glb`, `items_jewelry.glb`, `items_misc.glb` and `items_shields.glb`. These are the live files that `ITEM_MAP.json` points at. They are the source of truth. Edit these, never the `_c` copies.
- **Mobile copies:** `items_<name>_c.glb`, one next to each master. They are derived from the masters and were never hand-edited. They're regenerated from the master whenever the master changes. Since the decimation pass (below), the `_c` copies are lower-poly than the masters. The masters keep full resolution.
- `ITEM_MAP.json` still references the masters. Switching the game to the `_c` files is an engineer decision and is not part of this commit.

## Sizes
"Mid" is the first `_c` pass, which only changed textures. "Now" is the current, decimated `_c`. Tris are counted per atlas. "Worst piece" is the highest-tri item piece: an ITEM_MAP root/part node plus its child meshes.

| Master (live, untouched) | Mobile copy | MB master | MB `_c` mid | MB `_c` now | Tris mid → now | Worst piece mid | Worst piece now | Pieces decimated | Materials | Textures | ITEM_MAP nodes checked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `items_armor.glb` | `items_armor_c.glb` | 4.37 | 4.15 | 3.47 | 108,514 → 89,202 | tanners_vest 5,200 | bile_shroud 3,000 | 9 / 44 | 14 | 38 | 44 / 0 missing |
| `items_belts.glb` | `items_belts_c.glb` | 3.15 | 2.92 | 2.43 | 42,910 → 22,804 | spire_cord 7,000 | ferry_cord 2,999 | 6 / 9 | 14 | 36 | 9 / 0 missing |
| `items_gloves.glb` | `items_gloves_c.glb` | 3.97 | 3.63 | 2.84 | 57,580 → 26,870 | inquisitors_hands 8,000 | grave_claws 3,000 | 9 / 9 | 13 | 35 | 9 / 0 missing |
| `items_helms.glb` | `items_helms_c.glb` | 2.34 | 2.19 | 1.57 | 46,798 → 26,976 | spire_mask 5,200 | rite_crown 3,000 | 9 / 9 | 11 | 28 | 9 / 0 missing |
| `items_jewelry.glb` | `items_jewelry_c.glb` | 3.80 | 3.53 | 2.60 | 68,902 → 31,212 | war_band 4,500 | tin_pendant 2,500 * | 18 / 18 | 22 | 34 | 18 / 0 missing |
| `items_misc.glb` | `items_misc_c.glb` | 2.01 | 1.81 | 1.63 | 20,508 → 12,336 | scroll 6,000 | scroll 1,500 | 5 / 10 | 17 | 23 | 10 / 0 missing |
| `items_shields.glb` | `items_shields_c.glb` | 3.80 | 3.60 | 2.51 | 72,000 → 26,454 | wicker_round 8,000 | obsidian_aegis 2,998 | 9 / 9 | 14 | 32 | 9 / 0 missing |
| **Total** | | **23.44** | **21.84** | **17.05** | 417,212 → 235,854 | | | 65 / 108 | 105 | 226 | |

\* These are over the 1,500 floor-drop budget on purpose (see Exceptions).

### Budgets
- Worn pieces (armor, helms, gloves, belts, shields): 3,000 tris or fewer each. All are within budget.
- Floor-drop pieces (jewelry, misc): 1,500 tris or fewer each. All are within budget except the 7 chain amulets below.
- Pieces already within budget were left byte-identical.

### Exceptions: chain amulets
The chains are 44–51 separate links of 64 tris each, so the chain alone is about 2,800–3,300 tris. At 1,500 tris the links break into open, blobby fragments. These amulets are capped at the lowest budget that keeps every link closed:
- 2,500 tris: `amulet_ash_eye` and `amulet_tin_pendant`.
- 2,000 tris: `amulet_chapel_locket`, `amulet_grave_heart`, `amulet_obsidian_tear`, `amulet_spire_stone` and `amulet_weald_bead`.
- 1,500 tris: `amulet_bone_charm` and `amulet_war_beads`, which stay within budget.

To reach 1,500 on the chained amulets, the chain needs a lower-poly remodel in the master: for example, fewer links or 3-sided link cross-sections.

## Pipeline (gltf-transform 4.5.1 + meshoptimizer 1.3.0)
1. `gltf-transform prune MASTER p.glb --keep-leaves true --keep-attributes true`. This keeps every empty or leaf node, so all ITEM_MAP nodes and children survive.
2. `gltf-transform dedup p.glb d.glb`. This collapses duplicate texture objects (belts 42→36, gloves 39→35, jewelry 36→34, misc 27→23, shields 42→32). Images were already unique, so no image was dropped.
3. `gltf-transform webp d.glb items_<name>_c.glb --formats jpeg --quality 85`. JPEGs are re-encoded as WebP. WebP images already in the masters are kept byte-for-byte, because re-encoding them made the files larger.
4. Resize was not applied. Every image in the masters is already 512 px or smaller, so the 1024 cap is a no-op. `gltf-transform resize` would also have re-encoded the images for nothing.
5. No materials were merged. Each material has its own baseColor, metallic/roughness factors and texture set, and the UVs are tiled well outside 0–1 (ranges such as -5…2 and up to about 16). Merging would mean re-baking into a new atlas and would change how the items look. Node, mesh and material names, and the node hierarchy, are identical to the master.
6. **Decimation**, applied to the `_c` copies only. It uses meshoptimizer `simplifyWithAttributes` and works per piece (an ITEM_MAP root/part node plus its child meshes), one primitive at a time.
   - Normals and UVs are passed as attributes, so attribute seams are preserved.
   - Each piece uses one of four modes, chosen by the best silhouette score within budget:
     - `LockBorder` (open boundaries are kept), or
     - "UV-seam lock": every vertex that sits on a UV seam (same position, different UV) is locked, and `Permissive` lets hard-normal-only seams collapse.
     - In either case, tris are spread by the same ratio for every primitive, or by one absolute error threshold for the whole piece.
   - Accessors that dedup had shared between meshes are cloned before they are simplified, so no other item changes. Vertices are compacted per shared-POSITION group.
   - No weld, no quantization, no meshopt/Draco compression. Positions, normals and UVs stay float32, and indices are uint16.
   - None of the atlases has skins or JOINTS/WEIGHTS, so there are no skin weights to preserve.
   - Node, mesh and material names, primitive→material assignment, node transforms and hierarchy, and the texture and image bytes are identical to the previous `_c` copies.
7. Extensions: every copy declares `EXT_texture_webp` in `extensionsUsed` (and in `extensionsRequired`). `items_misc_c.glb` also keeps `KHR_materials_emissive_strength`, the same as its master. No `EXT_meshopt_compression`, `KHR_draco_mesh_compression` or `KHR_mesh_quantization`, and the index buffers are uint16.

## Checks
- **gltf-validator 2.0.0-dev.3.10:** 0 errors on all 7 copies. The only warnings are `MESH_PRIMITIVE_GENERATED_TANGENT_SPACE`, which the masters have too.
- For comparison, 5 of the masters fail validation: they embed `image/webp` without declaring `EXT_texture_webp` (`IMAGE_NON_ENABLED_MIME_TYPE` and `TEXTURE_INVALID_IMAGE_MIME_TYPE`). The `_c` copies fix that.
- **ITEM_MAP:** every `bases[].node`, `children[]`, `worn.*.parts[].node` and `kinds[].node` served by each atlas exists in its `_c` copy. 0 are missing.
- **Geometry vs master, per piece:**
  - Measures: symmetric Hausdorff distance as a fraction of the piece's bbox diagonal, and rasterized silhouette IoU from 3 axis views.
  - Worst piece per atlas:

    | Atlas | Max Hausdorff | Min IoU | Lowest-IoU piece |
    |---|---|---|---|
    | armor | 0.013 | 0.955 | |
    | belts | 0.025 | 0.868 | spire_cord; thin belt rims seen edge-on |
    | gloves | 0.011 | 0.978 | |
    | helms | 0.016 | 0.976 | |
    | jewelry | 0.017 | 0.894 | war_beads |
    | misc | 0.015 | 0.937 | |
    | shields | 0.027 | 0.966 | |

  - Bounding boxes are unchanged (≤0.3% drift).
- **Spot render** (Blender, previous `_c` vs decimated `_c`):
  - Views: the 50° top-down game camera angle and a 15° low angle, plus 40 px game-scale thumbnails.
  - The same 9 items: Obsidian Cuirass, Wick Coat, Rite Crown, Obsidian Aegis, War Gauntlets, Weald Belt, Inquisitor's Seal, Obsidian Tear and potion.
  - Plus 6 more: Ash Eye, Obsidian Belt, War Tower, Spire Mask, Portal and Ash Brigandine.
  - Mean foreground pixel difference: 0–5/255 (Ash Eye 9.6/255).
  - All read the same from the game camera. Up close, the Rite Crown thorns are slightly thinner and the amulet chain links are more angular.
