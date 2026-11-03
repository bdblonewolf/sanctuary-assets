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
`<piece>[_<class>].mask.json` lists the body vertices the piece covers, so the game can hide them to stop skin poking through. Indices refer to the class body as imported in Blender, the same convention as `characters_art/clothing/`.

## Icons / drops / renders
- `icons/damaged_black_<piece>.png`: 256 px Eevee render on a dark gothic slot frame. `icons/contact_sheet.png` shows all five.
- `drops/damaged_black_<piece>_drop.glb`: static, unrigged, decimated (about 0.9k–4k tris) floor loot, lying on the ground (z = 0, the plate on its back).
- `renders/damaged_black_<class>.png`: each class wearing the full set. `renders/damaged_black_classes_sheet.png` shows all four.

## Known remaining clipping
These counts are armor vertices more than 3 mm inside *visible* (unmasked) skin, measured with the anim_v2 clips. They are small and come mostly from the greave/boot top at the knee and the cape panel in seated poses.

| Class | Rest | Walk | Sit | Stand up |
|---|---|---|---|---|
| warrior | knee 28 | shoulder ≤6, knee 27 | knee 38 | knee 36 |
| necromancer | knee 39 | shoulder ≤11, knee 40 | knee 46 | knee 47 |
| archer | hip 10, knee 40 | shoulder ≤4, hip 10, knee 40 | **hip 149**, knee 44 | **hip 113**, knee 59 |
| elementalist | knee 44 | shoulder ≤2, knee 56 | hip 11, knee 51 | knee 67 |

The archer's seated hip clipping comes from the stiff skirt and cape panel against the thighs.

## Starter weapons (unchanged)
Ironvow (warrior) `models/weapons/weapon_parish_blade.glb` · Longmark (archer) `models/weapons/weapon_wicker_bow.glb` · Cinderwake (elementalist) `models/weapons/weapon_thorn_wand.glb` · Gravewell (necromancer) `models/weapons/weapon_seam_knife.glb` (all from Weapons v10a, current).
Stale: the ITEM_MAP sword fallback `models/weapon_sword.glb` is older than `weapon_sword_v2.glb`, which the sword prop uses.
