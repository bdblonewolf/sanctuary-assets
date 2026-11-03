# Damaged Black — starter armor set

This is the starter armor set for every class. It is cut from `models/knight_anim_v10b.glb` with the knight's look kept as is (same meshes and textures, no restyle). It was built headless in Blender 4.2.3, and the scripts live in the working dir (`sanctuary_art/equipment/damaged_black/work/`).

## Pieces / slots

| Slot | File | Contents |
|---|---|---|
| Helm | `damaged_black_helm.glb` | great helm |
| **Plate** | `damaged_black_plate.glb` | **torso + legs**: cuirass, pauldrons, faulds/tassets, skirt and cape, cuisses, knee cops, greave tops |
| Gauntlets | `damaged_black_gauntlets.glb` | gauntlets, vambraces, couters |
| **Boots** | `damaged_black_boots.glb` | **just the boots** (foot + boot shaft) |
| Belt | `damaged_black_belt.glb` | waist belt, buckle, straps |

> **Slot rule (Brian's correction):** Plate (chest) covers the torso **plus** the leggings/skirt and leg armor below the belt. Boots are only the boots, and Belt is only the belt. The Plate and Boots icons and floor drops follow this split. The knight's sword and scabbard (material 11) are left out, since weapons are separate items.

Knight material → slot: 06 helm · 07/08/12 plate · 09 knee parts → plate, the rest → gauntlets · 10 split by bone (hand/forearm → gauntlets, hip band → belt, foot → boots, the rest → plate) · 13 boots, with the floating knee guards (island centre above 0.41 m) → plate.

## Rig

Every piece is a separate, swappable skinned mesh on the shared **mixamorig 52-bone rig** (`characters_art/bodies/`). Each piece has at most 4 influences, and no animations, morphs or body mesh are included. Load the matching body, then attach the pieces to its armature.

## Per-class variants

`pieces/damaged_black_<piece>.glb` is fitted to **male_regular**. `pieces/damaged_black_<piece>_<class>.glb` is fitted per class:

| Class | Test body used |
|---|---|
| warrior | male_regular scaled 1.08/1.08/1.05 (slightly bigger), 1.87 m |
| necromancer | male_regular thinner (0.90/0.92) and tallest, 1.97 m |
| archer | female_skinny, Ayla slate skin tone, 1.60 m (5'3") |
| elementalist | 50/50 vertex blend of female_medium and female_curvy, 1.68 m (5'6") |

**These are test bodies.** No final class bodies exist yet, so the variants must be refit when they do (run `work/fit.py -- <class>` after updating `work/classbodies.py`).

### Fit approach
1. **Retarget** the knight to male_regular. This uses FK-chained minimal-rotation bone alignment with length scaling, then LBS of the armor with the knight's own skin weights.
2. **Body→class field.** male_regular and the class bodies share MPFB topology, matched through the UV layout. Each armor vertex follows the smooth (IDW, k=16) displacement of nearby body vertices. Near the skin it also gets the normal-direction part of a surface-attached offset, so cuirasses follow chest shape.
3. **Helm.** Rigid scale and offset so it encloses the head.
4. **Push-out (shrinkwrap/offset).** Armor vertices and face samples inside the skin or the linen undergarment are pushed out to a 7 mm margin. Requirements are gathered on armor vertices and spatially blurred (3 cm) to keep plate shapes, then outlier vertices are de-spiked.
5. **Weights.** Gauntlets keep the knight's weights. The other pieces use barycentric transfer from the body plus smoothing, top 4 influences.

### Body masks
`<piece>[_<class>].mask.json` (same format in `pieces/` and `masters/`) lists the body vertices the piece covers, so the game can hide them to stop skin poking through. Indices refer to the class body as imported in Blender, the same convention as `characters_art/clothing/`.

## Icons / drops / renders
- `icons/damaged_black_<piece>.png`: 256 px Eevee render on a dark gothic slot frame. `icons/contact_sheet.png` shows all five.
- `drops/damaged_black_<piece>_drop.glb`: static, unrigged, decimated (about 0.9k–4k tris) floor loot, lying on the ground (z = 0, the plate on its back).
- `renders/damaged_black_<class>.png`: each class wearing the full set. `renders/damaged_black_classes_sheet.png` shows all four.

## Mobile pass (final): master vs mobile copy

| Folder | What it is |
|---|---|
| `masters/damaged_black_<piece>[_<class>].glb` + `.mask.json` | **MASTER**: uncompressed, full-detail originals (the af8dacf/f4f520d pieces, about 67.6k tris per set) with their **original embedded knight textures**. Edit and refit from these. |
| `pieces/damaged_black_<piece>[_<class>].glb` + `.mask.json` | **MOBILE copy** that the game loads. Same filenames and paths as before. |
| `textures/damaged_black_atlas_{basecolor,metallicroughness,normal}.webp` | ONE shared 1024² WebP atlas (348 KB in total). Every mobile piece references it by URI (`../textures/...`, `EXT_texture_webp`, required). |

How the mobile copy is built (`sanctuary_art/equipment/damaged_black/work/final/`: build.py, post.py):
- It is decimated to the phone budget: plate ≤9k tris, gauntlets/boots/helm ≤4k, belt ≤2k, set ≤25k tris and ≤1.5 MB. All the knight materials are baked into the single `damaged_black_atlas` material.
- **Compression: none.** There is no meshopt, no Draco and no `KHR_mesh_quantization` in any GLB. The files run through `gltf-transform prune` (keep attributes/leaves) and `dedup` only, plus core-glTF packing: WEIGHTS_0 is normalized u8 (each vertex sums to exactly 255) and TEXCOORD_0 is normalized u16. POSITION and NORMAL stay float.
- The rig is unchanged: the same 52 mixamorig joints in the same order, identical inverse bind matrices, metres, and no scale or offset. Node names match the masters.
- **Piece separation:** the plate's material `10_-_Default` hip band was a duplicate of the belt, so 852 duplicate belt tris were deleted from the plate. 4282 harness-strap tris stay on the plate, and no plate tris moved to the boots. The belt textures inside the gauntlets were separated, with 0 tris moved (18 for the archer).
- **Liners:** thin dark under-liners close the cuffs, boot tops and helm neck: gauntlets 995 tris, boots 894 and helm 416. All of these are included in the budget numbers.
- **Masks** (same running-index format): they are recomputed per class from coverage, so the boot masks now include the whole ankle and foot. The helm mask keeps the face visible through the visor slit (272 verts for the warrior).

### Budget (mobile `pieces/`, tris / MB per piece)
| Class | plate | gauntlets | boots | helm | belt | set tris | set MB (geom + atlas) | masters MB |
|---|---|---|---|---|---|---|---|---|
| base (male_regular) | 8923 / 0.282 | 3949 / 0.230 | 3949 / 0.206 | 3814 / 0.158 | 1959 / 0.076 | 22594 | 1.300 | 5.694 |
| warrior | 8923 / 0.282 | 3950 / 0.230 | 3947 / 0.205 | 3814 / 0.158 | 1960 / 0.076 | 22594 | 1.300 | 5.694 |
| necromancer | 8924 / 0.282 | 3949 / 0.230 | 3948 / 0.206 | 3815 / 0.158 | 1960 / 0.076 | 22596 | 1.300 | 5.694 |
| archer | 8923 / 0.282 | 3949 / 0.230 | 3948 / 0.206 | 3815 / 0.158 | 1959 / 0.077 | 22594 | 1.301 | 5.694 |
| elementalist | 8924 / 0.283 | 3949 / 0.230 | 3947 / 0.206 | 3814 / 0.158 | 1959 / 0.076 | 22593 | 1.301 | 5.693 |

Before (masters), every class: plate 28322 / 2.715, gauntlets 17209 / 1.252, boots 7724 / 0.690, helm 3398 / 0.466, belt 10940 / 0.570. The set was **67593 tris / 5.694 MB**; it is now **~22.6k tris / 1.30 MB including the atlas**. Nothing is over budget.

## Clipping / gap check (final)
Method: `work/final/check.py`. Clips are retargeted onto each class body with a world-delta rotation retarget, and the hips translation is dropped. The poses are idle, run, ss_attack_heavy, bow_draw and magic_cast (`knight_anim_v10b`), plus rest, walk_a, walk_b, sit and stand_up (anim_v2). The table shows the worst frame per seam.
- **skin_gap:** an unmasked skin vertex whose outward 12 cm ray hits no armor (visible skin at the seam).
- **hole:** a masked vertex whose skin faces are all hidden and which no armor covers (from +1 mm or from 5 mm inside), so you would see through the body.
- **clip:** an armor vertex more than 3 mm behind a *visible* body triangle.
- Face verts seen through the visor slit are intended and are not counted.

`[skin_gap, hole, clip]`, before (masters) → after (mobile):

| Class | boots / hem | cuffs / sleeves | helm neck / collar | belt / waist |
|---|---|---|---|---|
| warrior | [60,729,9] → [0,35,0] | [0,2363,0] → [0,172,0] | [24,94,2] → [3,4,4] | [3,13,0] → [2,16,0] |
| necromancer | [61,700,11] → [0,31,0] | [0,2307,0] → [0,142,0] | [25,81,16] → [1,2,0] | [1,2,0] → [4,0,0] |
| archer | [48,718,7] → [0,19,0] | [0,2183,0] → [0,160,0] | [20,87,3] → [0,1,0] | [36,1,12] → [15,4,6] |
| elementalist | [50,717,12] → [0,28,0] | [0,2186,0] → [0,170,0] | [26,122,0] → [0,4,0] | [13,19,1] → [19,12,1] (stand_up) |
| base (male_regular) | [60,720,11] → [0,29,0] | [0,2346,0] → [0,151,0] | [25,99,1] → [2,2,3] | [2,12,0] → [4,14,0] |

- **Boots:** there are **0 skin-gap verts** between the plate hem and the boot for every class in every pose.
- The remaining "holes" are fingertip and toe tips where the decimated liner sits just inside the hidden skin. They are tiny and covered by the gauntlet and boot shells in the renders.
- The archer's belt/waist skin_gap verts are inner-thigh/crotch verts (z≈0.69 m) that the tassets hide, so no skin is visible in the renders.
- Raw results are in `checks/<class>_{before,after}.json`.

## Renders (final pass)
- `renders/damaged_black_feet_sheet.png`: feet and ankle close-ups per class. The columns are before front, before 3/4, after front and after 3/4. The single images are in `renders/feet/<class>_{ffront,fq34}_{before,after}.png`.
- `renders/damaged_black_seams_<class>.png`: seam close-ups. The rows are idle, run, ss_attack_heavy, bow_draw and magic_cast; the columns are boots/hem, cuff/sleeve, helm neck/collar and belt/waist.
- The player renders with the mobile set are in `characters_art/players/renders/`: `player_<class>_damaged_black_{front,q34}.png`, the per-class sheets and `players_lineup_sheet.png`.
- The older `renders/damaged_black_<class>.png` and `damaged_black_classes_sheet.png` show the pre-mobile masters on the test bodies.

## Bodies / skin textures
- The player bodies are **unchanged**: they are not decimated or compressed, and the vertex order is the same. So there is no `characters_art/players/masters/` folder.
- The optional skin-texture pass was **skipped**. The bodies must not change, and no suitable, budget-fitting skin textures were verified. The necromancer stays pale.

## Starter weapons (unchanged)
Ironvow (warrior) `models/weapons/weapon_parish_blade.glb` · Longmark (archer) `models/weapons/weapon_wicker_bow.glb` · Cinderwake (elementalist) `models/weapons/weapon_thorn_wand.glb` · Gravewell (necromancer) `models/weapons/weapon_seam_knife.glb` (all from Weapons v10a, current).
Stale: the ITEM_MAP sword fallback `models/weapon_sword.glb` is older than `weapon_sword_v2.glb`, which the sword prop uses.
