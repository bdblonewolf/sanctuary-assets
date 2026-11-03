# ITEM_3D_GAPS — item bases vs 3D models

Written 2026-11-03 (ET) by Grok Bot. This was a read-only check. No game code or `ITEM_MAP.json` was changed.

## What was compared
- **Game item bases:** read from the current build `/workspace/sanctuary/live_fx2c/routes-DYqsoIet.js` (newest bundle, built Nov 2 21:43 ET). That covers the 31 `{slot, bases:[normal, exceptional, elite]}` drop tables, which give 93 bases, plus 4 class-starter weapons from `lo()`. **97 bases in total**, across 8 slots: weapon 34, armor 9, helm 9, shield 9, gloves 9, belt 9, ring 9, amulet 9. **There is no boots slot.**
- **3D map:** `sanctuary-assets/models/items/ITEM_MAP.json` (origin/main, v1). It has 64 `bases`, 34 `weapons` and 12 `kinds`, using 7 atlas GLBs and the 30 per-weapon GLBs in `models/weapons/`.
- **How the game uses the map** (same bundle):
  - Floor drops and inventory icons use `bases[]`, `weapons[]` and `kinds[]`. All of them come from the atlas node or the weapon GLB, and the icon comes from `icons/items_icons.json`.
  - Equipped visuals:
    - The in-hand weapon is the per-base weapon GLB (`_T(weaponBase)`), and the animation set comes from `weapons[].set`.
    - Helm and armor are attached to the body from `bases[].worn.knight.parts` (`syncWorn`). Only `eq.helm` and `eq.armor` are read.
    - An equipped shield is **always** the generic `models/weapon_shield.glb` (`loadProp('shield')`).
    - Gloves, belt, ring and amulet are not drawn on the body.
- **Equipment art we hold:** `sanctuary_art/equipment/` and the repo `characters_art/equipment/`.
  - `arrows/`: arrow, arrows_kit, quiver and 3 stuck-arrow variants.
  - `damaged_black/`: plate, helm, gauntlets, belt and boots, each in a base fit and 4 class fits (archer, elementalist, necromancer, warrior), plus drop versions.

## Summary
| check | result |
|---|---|
| Every game base has an ITEM_MAP entry | ✅ 97/97. The map also has `Gold`, which is a loot kind, not a base. That is harmless. |
| The entry's GLB exists in the repo | ✅ 97/97 |
| The atlas node named in the entry exists in its GLB | ✅ 63/63 node-based entries, and 12/12 `kinds` |
| The icon exists in `items_icons.json` | ✅ all of them (103 icons) |
| Unique and set items | They use their base's model, as in D2. No unique-specific meshes exist, and none are referenced. |

**There are no missing drop or floor models.** The gaps below are in how equipped items look on the character, plus some mobile and data issues.

## Gaps, in priority order
1. **Shields look the same when equipped.** All 9 shield bases (Wicker Round … Obsidian Aegis) render as the generic `weapon_shield.glb` in the off hand. Each base already has its own mesh in `items_shields.glb` (`shield_*` nodes), so this needs **fit data, not new art**:
   - Add `worn.knight.parts[{node, bone_three:'mixamorigLeftForeArm'/'LeftHand', pos, quat, scale}]` per shield, the same way as helm and armor.
   - The game would also need to read it. That is a code change, which I didn't make.
2. **Gloves and belts are invisible when equipped.** 18 bases (Wick Wraps … Inquisitor's Hands; Ferry Cord … Obsidian Belt) have drop meshes but no `worn` fits, and the game ignores `eq.gloves` and `eq.belt` for visuals.
   - Gloves need a skinned or bone-attached left/right pair per base, or a hand-tint fallback.
   - Belts can be rigid on `mixamorigHips`, like the armor fauld.
   - Reuse first: `damaged_black_gauntlets` and `damaged_black_belt` already have knight-style fits and per-class fits, and could become worn variants.
3. **Worn helm and armor fits exist only for `knight` and `npc_male_regular`.** The code reads `worn.knight` only. If the players' class bodies in `characters_art/players/` (archer, elementalist, necromancer, warrior) or female NPCs ever wear gear, each needs its own `worn[bodyKey]` fit for all 18 helm and armor bases. `damaged_black` shows the per-class refit approach.
4. **Some weapon types lack an animation set.** `hT` only has sword, dagger, greataxe, bow, staff and wand, so:

   | weapons | count | animation set used | gap |
   |---|---|---|---|
   | maces (Chapel Maul, Mercy Hammer, Inquisitor's Nail) | 3 | `sword` | The scabbard is hidden for these, but the swing is a sword slash. A blunt overhead set is missing. |
   | 1-handed axes (Briar Hatchet, Cinder Axe, Sable Cleaver) | 3 | `greataxe` | They are two-handed swings with a one-handed weapon. A 1H axe set is missing. |
   | spears and polearms (Ferry Pike, Mourning Spear, Lid Glaive) | 3 | `staff` | They animate like a staff. A thrust set is missing. |

   The animations made today for swordsman and axeman, `characters_art/monsters/{swordsman,axeman}/*_anim.glb` (mixamorig), could be sources for a 1H axe set or a mace set.
5. **The starter weapons have no meshes of their own.** Each of the 4 reuses a drop base's mesh and icon:

   | starter weapon | reuses |
   |---|---|
   | Rusted Iron Sword | Parish Blade |
   | Chipped Bone Dagger | Seam Knife |
   | Gnarled Yew Wand | Thorn Wand |
   | Ashwood Short Bow | Wicker Bow |

   Because of that, a starter and a Parish Blade look identical in inventory. This is low priority. A cheap fix is a rusted or chipped texture variant of the same mesh.
6. **The quest ring has no mesh of its own.** `kinds.quest_ring` reuses `ring_spire_circle`, so a quest ring looks like a Spire Circle drop. Low priority. A distinct emissive or tinted variant would do.
7. **Boots are art with no slot.** `damaged_black_boots` (5 fits plus a drop) exist, but the game has no boots slot. Keep them for later, or fold them into the armor visuals.
8. **Phone budget.** These are not missing models, but they cost download and memory:
   - The 7 atlases total **23.4 MB** and contain 11–22 materials each, with about 3 textures per material at 256–512 px. They are separate materials, not one shared atlas, so there are many draw calls when several drops are on screen.
   - `items_armor.glb` alone is 108k tris and 4.4 MB.
   - 5 atlases embed **WebP** images (`image/webp`) without declaring `EXT_texture_webp`. Browsers load them, but this is not valid glTF. Validators and some tools will reject it, and iOS 13 and older can't decode WebP. It should either declare the extension or use JPEG/PNG.
   - Suggested fix (not done, to avoid live overwrites):
     1. Run `mobile_compress.sh` on each atlas.
     2. Merge to 1–2 materials per atlas with one 1024–2048 texture set.
     3. Ship as `_c` copies alongside the current files, and move the originals to `masters/`.
   - The per-weapon GLBs (0.1–0.3 MB, 2–5k tris) are fine.

## Not gaps (checked)
- Potions, mana potions, portal scrolls, scrolls, books, jewels, runes, keys, boss stones and gold all have `kinds` nodes present in `items_misc.glb`.
- Arrows, the quiver and stuck arrows exist in `characters_art/equipment/arrows/`. The game currently uses `models/weapon_arrow.glb` for the bow arrow.

## Per-base table
| base | slot | tier / qlvl | 3D model (glb → node) | drop / icon | equipped visual |
|---|---|---|---|---|---|
| Parish Blade | weapon | normal q1 | `weapon_parish_blade.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Ash Saber | weapon | exceptional q16 | `weapon_ash_saber.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Spire Falchion | weapon | elite q32 | `weapon_spire_falchion.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Briar Hatchet | weapon | normal q4 | `weapon_briar_hatchet.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| Cinder Axe | weapon | exceptional q19 | `weapon_cinder_axe.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| Sable Cleaver | weapon | elite q36 | `weapon_sable_cleaver.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| Ferry Pike | weapon | normal q6 | `weapon_ferry_pike.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Mourning Spear | weapon | exceptional q21 | `weapon_mourning_spear.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Lid Glaive | weapon | elite q38 | `weapon_lid_glaive.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Chapel Maul | weapon | normal q8 | `weapon_chapel_maul.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Mercy Hammer | weapon | exceptional q24 | `weapon_mercy_hammer.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Inquisitor's Nail | weapon | elite q42 | `weapon_inquisitors_nail.glb` | ✅ | in hand, own mesh (anim set `sword`) |
| Timber Axe | weapon | normal q6 | `weapon_timber_axe.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| War Axe | weapon | exceptional q22 | `weapon_war_axe.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| Kingrender | weapon | elite q40 | `weapon_kingrender.glb` | ✅ | in hand, own mesh (anim set `greataxe`) |
| Stitched Blade | weapon | normal q2 | `weapon_stitched_blade.glb` | ✅ | in hand, own mesh (anim set `dagger`) |
| Seam Knife | weapon | exceptional q16 | `weapon_seam_knife.glb` | ✅ | in hand, own mesh (anim set `dagger`) |
| Widow Stitch | weapon | elite q32 | `weapon_widow_stitch.glb` | ✅ | in hand, own mesh (anim set `dagger`) |
| Yew Longbow | weapon | normal q4 | `weapon_yew_longbow.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Ash Longbow | weapon | exceptional q18 | `weapon_ash_longbow.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Spire Longbow | weapon | elite q36 | `weapon_spire_longbow.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Wicker Bow | weapon | normal q1 | `weapon_wicker_bow.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Thorn Wicker | weapon | exceptional q14 | `weapon_thorn_wicker.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Spite Wicker | weapon | elite q30 | `weapon_spite_wicker.glb` | ✅ | in hand, own mesh (anim set `bow`) |
| Ash Staff | weapon | normal q3 | `weapon_ash_staff.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Chapel Staff | weapon | exceptional q18 | `weapon_chapel_staff.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Weald Staff | weapon | elite q34 | `weapon_weald_staff.glb` | ✅ | in hand, own mesh (anim set `staff`) |
| Sting Wand | weapon | normal q2 | `weapon_sting_wand.glb` | ✅ | in hand, own mesh (anim set `wand`) |
| Thorn Wand | weapon | exceptional q16 | `weapon_thorn_wand.glb` | ✅ | in hand, own mesh (anim set `wand`) |
| Omen Wand | weapon | elite q32 | `weapon_omen_wand.glb` | ✅ | in hand, own mesh (anim set `wand`) |
| Ashwood Short Bow | weapon | starter q1 | `weapon_wicker_bow.glb` (reuses Wicker Bow mesh) | ✅ | in hand, own mesh (anim set `bow`) |
| Chipped Bone Dagger | weapon | starter q1 | `weapon_seam_knife.glb` (reuses Seam Knife mesh) | ✅ | in hand, own mesh (anim set `dagger`) |
| Gnarled Yew Wand | weapon | starter q1 | `weapon_thorn_wand.glb` (reuses Thorn Wand mesh) | ✅ | in hand, own mesh (anim set `wand`) |
| Rusted Iron Sword | weapon | starter q1 | `weapon_parish_blade.glb` (reuses Parish Blade mesh) | ✅ | in hand, own mesh (anim set `sword`) |
| Wick Coat | armor | normal q1 | `items_armor.glb` → `armor_wick_coat` | ✅ | knight + npc_male_regular fits |
| Silt Hauberk | armor | exceptional q15 | `items_armor.glb` → `armor_silt_hauberk` | ✅ | knight + npc_male_regular fits |
| Bile Shroud | armor | elite q30 | `items_armor.glb` → `armor_bile_shroud` | ✅ | knight + npc_male_regular fits |
| Tanner's Vest | armor | normal q5 | `items_armor.glb` → `armor_tanners_vest` | ✅ | knight + npc_male_regular fits |
| Ash Brigandine | armor | exceptional q18 | `items_armor.glb` → `armor_ash_brigandine` | ✅ | knight + npc_male_regular fits |
| Spire Harness | armor | elite q34 | `items_armor.glb` → `armor_spire_harness` | ✅ | knight + npc_male_regular fits |
| Parish Plate | armor | normal q9 | `items_armor.glb` → `armor_parish_plate` | ✅ | knight + npc_male_regular fits |
| Grave Plate | armor | exceptional q23 | `items_armor.glb` → `armor_grave_plate` | ✅ | knight + npc_male_regular fits |
| Obsidian Cuirass | armor | elite q40 | `items_armor.glb` → `armor_obsidian_cuirass` | ✅ | knight + npc_male_regular fits |
| Bent Brow | helm | normal q1 | `items_helms.glb` → `helm_bent_brow` | ✅ | knight + npc_male_regular fits |
| Ash Sallet | helm | exceptional q16 | `items_helms.glb` → `helm_ash_sallet` | ✅ | knight + npc_male_regular fits |
| Rite Crown | helm | elite q33 | `items_helms.glb` → `helm_rite_crown` | ✅ | knight + npc_male_regular fits |
| Mourner Hood | helm | normal q1 | `items_helms.glb` → `helm_mourner_hood` | ✅ | knight + npc_male_regular fits |
| Grave Visor | helm | exceptional q19 | `items_helms.glb` → `helm_grave_visor` | ✅ | knight + npc_male_regular fits |
| Weald Cowl | helm | elite q36 | `items_helms.glb` → `helm_weald_cowl` | ✅ | knight + npc_male_regular fits |
| Iron Skull | helm | normal q2 | `items_helms.glb` → `helm_iron_skull` | ✅ | knight + npc_male_regular fits |
| Bone Casque | helm | exceptional q22 | `items_helms.glb` → `helm_bone_casque` | ✅ | knight + npc_male_regular fits |
| Spire Mask | helm | elite q40 | `items_helms.glb` → `helm_spire_mask` | ✅ | knight + npc_male_regular fits |
| Wicker Round | shield | normal q1 | `items_shields.glb` → `shield_wicker_round` | ✅ | **generic `models/weapon_shield.glb`** |
| Ash Guard | shield | exceptional q15 | `items_shields.glb` → `shield_ash_guard` | ✅ | **generic `models/weapon_shield.glb`** |
| Crypt Round | shield | elite q31 | `items_shields.glb` → `shield_crypt_round` | ✅ | **generic `models/weapon_shield.glb`** |
| Briar Targe | shield | normal q5 | `items_shields.glb` → `shield_briar_targe` | ✅ | **generic `models/weapon_shield.glb`** |
| Grave Wall | shield | exceptional q19 | `items_shields.glb` → `shield_grave_wall` | ✅ | **generic `models/weapon_shield.glb`** |
| Spire Targe | shield | elite q35 | `items_shields.glb` → `shield_spire_targe` | ✅ | **generic `models/weapon_shield.glb`** |
| Parish Kite | shield | normal q9 | `items_shields.glb` → `shield_parish_kite` | ✅ | **generic `models/weapon_shield.glb`** |
| War Tower | shield | exceptional q24 | `items_shields.glb` → `shield_war_tower` | ✅ | **generic `models/weapon_shield.glb`** |
| Obsidian Aegis | shield | elite q41 | `items_shields.glb` → `shield_obsidian_aegis` | ✅ | **generic `models/weapon_shield.glb`** |
| Wick Wraps | gloves | normal q2 | `items_gloves.glb` → `gloves_wick_wraps` | ✅ | **not shown on body** |
| Ash Grips | gloves | exceptional q16 | `items_gloves.glb` → `gloves_ash_grips` | ✅ | **not shown on body** |
| Spire Hands | gloves | elite q32 | `items_gloves.glb` → `gloves_spire_hands` | ✅ | **not shown on body** |
| Tanner Mitts | gloves | normal q6 | `items_gloves.glb` → `gloves_tanner_mitts` | ✅ | **not shown on body** |
| Grave Claws | gloves | exceptional q20 | `items_gloves.glb` → `gloves_grave_claws` | ✅ | **not shown on body** |
| Bile Grasp | gloves | elite q36 | `items_gloves.glb` → `gloves_bile_grasp` | ✅ | **not shown on body** |
| Chapel Gloves | gloves | normal q10 | `items_gloves.glb` → `gloves_chapel_gloves` | ✅ | **not shown on body** |
| War Gauntlets | gloves | exceptional q24 | `items_gloves.glb` → `gloves_war_gauntlets` | ✅ | **not shown on body** |
| Inquisitor's Hands | gloves | elite q42 | `items_gloves.glb` → `gloves_inquisitors_hands` | ✅ | **not shown on body** |
| Ferry Cord | belt | normal q1 | `items_belts.glb` → `belt_ferry_cord` | ✅ | **not shown on body** |
| Ash Sash | belt | exceptional q15 | `items_belts.glb` → `belt_ash_sash` | ✅ | **not shown on body** |
| Spire Cord | belt | elite q30 | `items_belts.glb` → `belt_spire_cord` | ✅ | **not shown on body** |
| Tanner Sash | belt | normal q5 | `items_belts.glb` → `belt_tanner_sash` | ✅ | **not shown on body** |
| Grave Cinch | belt | exceptional q19 | `items_belts.glb` → `belt_grave_cinch` | ✅ | **not shown on body** |
| Weald Belt | belt | elite q35 | `items_belts.glb` → `belt_weald_belt` | ✅ | **not shown on body** |
| Chapel Girdle | belt | normal q9 | `items_belts.glb` → `belt_chapel_girdle` | ✅ | **not shown on body** |
| War Girdle | belt | exceptional q23 | `items_belts.glb` → `belt_war_girdle` | ✅ | **not shown on body** |
| Obsidian Belt | belt | elite q40 | `items_belts.glb` → `belt_obsidian_belt` | ✅ | **not shown on body** |
| Copper Band | ring | normal q3 | `items_jewelry.glb` → `ring_copper_band` | ✅ | not shown (by design) |
| Ash Signet | ring | exceptional q17 | `items_jewelry.glb` → `ring_ash_signet` | ✅ | not shown (by design) |
| Spire Circle | ring | elite q33 | `items_jewelry.glb` → `ring_spire_circle` | ✅ | not shown (by design) |
| Tin Loop | ring | normal q7 | `items_jewelry.glb` → `ring_tin_loop` | ✅ | not shown (by design) |
| Grave Loop | ring | exceptional q21 | `items_jewelry.glb` → `ring_grave_loop` | ✅ | not shown (by design) |
| Weald Loop | ring | elite q37 | `items_jewelry.glb` → `ring_weald_loop` | ✅ | not shown (by design) |
| Chapel Ring | ring | normal q11 | `items_jewelry.glb` → `ring_chapel_ring` | ✅ | not shown (by design) |
| War Band | ring | exceptional q25 | `items_jewelry.glb` → `ring_war_band` | ✅ | not shown (by design) |
| Inquisitor's Seal | ring | elite q43 | `items_jewelry.glb` → `ring_inquisitors_seal` | ✅ | not shown (by design) |
| Bone Charm | amulet | normal q2 | `items_jewelry.glb` → `amulet_bone_charm` | ✅ | not shown (by design) |
| Ash Eye | amulet | exceptional q16 | `items_jewelry.glb` → `amulet_ash_eye` | ✅ | not shown (by design) |
| Spire Stone | amulet | elite q32 | `items_jewelry.glb` → `amulet_spire_stone` | ✅ | not shown (by design) |
| Chapel Locket | amulet | normal q6 | `items_jewelry.glb` → `amulet_chapel_locket` | ✅ | not shown (by design) |
| Grave Heart | amulet | exceptional q20 | `items_jewelry.glb` → `amulet_grave_heart` | ✅ | not shown (by design) |
| Weald Bead | amulet | elite q36 | `items_jewelry.glb` → `amulet_weald_bead` | ✅ | not shown (by design) |
| Tin Pendant | amulet | normal q10 | `items_jewelry.glb` → `amulet_tin_pendant` | ✅ | not shown (by design) |
| War Beads | amulet | exceptional q24 | `items_jewelry.glb` → `amulet_war_beads` | ✅ | not shown (by design) |
| Obsidian Tear | amulet | elite q41 | `items_jewelry.glb` → `amulet_obsidian_tear` | ✅ | not shown (by design) |
