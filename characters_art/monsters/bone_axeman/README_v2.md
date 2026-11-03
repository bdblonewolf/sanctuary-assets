# bone_axeman_v2.glb

A copy of `bone_axeman.glb` with new clips added. The original file is unchanged, and the v2 file keeps all of its
original clips (idle, walk, attack1, attack2, hit, death) with the same frame counts. The regular `death` is kept.
30 fps, in place (no root motion), lowercase clip names.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| heavy_cleave | 61 | 2.00 | big two-handed wind-up 0–22 (weapon overhead about frames 14–22), hard chop 23–30, **impact frame 36** (damage; the weapon bites into the ground), stuck/dragging recovery 37–60 |
| death_crumble | 56 | 1.83 | standard: the skull rolls off forward-right, and the pile settles roughly in place. Shudder 0–6, skull lets go at 6, arms 8–11, spine and legs 11–13. **Ground impact / bone-crunch frame 25** (pelvis and ribcage land; the skull lands at 24). First small pieces touch the ground at 15. Bounce and settle until 37; the last frame holds the bone pile |
| death_crumble2 | 56 | 1.83 | leans and collapses forward, the skull rolls to the left, and the pile spreads wider. Shudder 0–6, skull lets go at 6, arms 8–11, spine and legs 11–13. **Ground impact / bone-crunch frame 25** (pelvis and ribcage land; the skull lands at 24). First small pieces touch the ground at 15. Bounce and settle until 36; the last frame holds the bone pile |
| death_crumble3 | 56 | 1.83 | leans and collapses backward, the skull rolls back, and the pile is tighter. Shudder 0–6, skull lets go at 6, arms 8–11, spine and legs 11–13. **Ground impact / bone-crunch frame 25** (pelvis and ribcage land; the skull lands at 24). First small pieces touch the ground at 15. Bounce and settle until 37; the last frame holds the bone pile |

Death sounds (sanctuary-assets audio/sfx/monster/, commit e355bec). Sound start frame = ground-impact frame − impact offset × 30, rounded:

| clip | sound | impact offset in sound | ground-impact frame | **sound start frame** |
|---|---|---|---|---|
| death_crumble | audio/sfx/monster/skeleton_death_crumble_01.ogg | 0.299 s (8.97 f) | 25 | **16** (16.03) |
| death_crumble2 | audio/sfx/monster/skeleton_death_crumble_02.ogg | 0.351 s (10.53 f) | 25 | **14** (14.47) |
| death_crumble3 | audio/sfx/monster/skeleton_death_crumble_03.ogg | 0.280 s (8.40 f) | 25 | **17** (16.60) |

Notes
- The death_crumble clips break the skeleton apart at the joints. Each limb segment (skull, hands with fingers, forearms,
  upper arms, clavicles, neck, ribcage, spine pieces, pelvis, thighs, shins, feet) moves as a rigid piece using bone
  translation and rotation keys on every bone. Each piece falls under gravity, bounces once or twice and settles.
  The weapon falls with its hand.
- Play a bone-crunch sound on the ground-impact frame listed for each variant. Optionally add a smaller rattle at the skull frame.
- Some skinned verts dip below the ground plane by up to about 5 cm during the crumble (blended verts at the separated joints).
- heavy_cleave: the first and last frames blend to idle frame 0. The weapon tip goes about 8 cm below the ground at the
  chop on purpose (it sticks in the ground). The hips drift up to 0.10 m forward during the chop and return.

Source / licence
- heavy_cleave: Mixamo "Great Sword Pack / great sword slash (3)", retargeted by script with a time warp (slow wind-up,
  fast chop, stuck hold, dragging recovery) and hand-keyed spine, head and hip weight layers. Used under Adobe's Mixamo terms
  (free for games; raw files not redistributed).
- death_crumble, death_crumble2, death_crumble3: procedural and keyframed by script. No free bone-crumble or collapse clip was
  found in Mixamo, Quaternius or KayKit. It is original work, free to use in this project.


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `bone_axeman_v2.glb` | `masters/bone_axeman_v2.glb` | 2.86 → 1.17 | 125,775 → 14,807 | 2.09 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
