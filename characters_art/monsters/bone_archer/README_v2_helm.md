# bone_archer_v2_helm.glb: skeleton archer with a top-down-readable helm

This is a copy of `bone_archer_v2.glb`. The skeleton body, bow, belt, bracers and **all 9 v2 clips** are unchanged (same frame counts):
idle 154, walk 37, attack1 31, attack2 22, hit 39, death 93, death_crumble / death_crumble2 / death_crumble3 56 each (30 fps).
`bone_archer.glb` and `bone_archer_v2.glb` are untouched.

## What changed
- The old small dark skull-cap (`helmet`, `helmet_band`, `helmet_nasal`, about 0.21 m across) is removed.
- New mesh `skeleton_helm` is a **kettle-hat** (chapel-de-fer) with a deep dome, a **wide brim 0.48 x 0.54 m** (about 2.3x the old helmet), a slight
  downturned lip, a riveted collar and a **0.12 m top spike**, plus a low front-to-back comb. It is 1068 tris, skinned 100% to `mixamorig:Head`, so it follows every clip.
- Material `mon_rust_light` uses a 512 px texture (`tools_helm/helm_rust_light_c.jpg`, derived from the archer's own rust_c): **lighter**
  grey iron with orange rust patches, metallic 0.5, roughness 0.6. From the top-down camera it reads as a bright round disc with a spike dot, clearly
  separate from the ivory bones and the dark ground.
- Total file tris: about 10.5k (body 6791, bow 1540, helm 1068, belt and bracers 892).

## skeleton_helm.glb (helm alone)
- This is the same mesh and material, unskinned, stored in **bone_archer's `mixamorig:Head` joint-local space**. In three.js, `headBone.add(helm)` with an identity
  transform puts it on the head exactly as in bone_archer_v2_helm (the joint rest position is glTF (0, 1.5907, -0.013) and its rotation is identity).
- For other mixamorig skeletons, add it under their Head bone and adjust the position if their head size differs.
- Source: built from scratch in Blender (`tools_helm/build_helm.py`). I checked items_helms.glb, env/props and the free packs first; none had a kettle-hat or brimmed helm, and the item helms are knightly. Original work, free to use in this project.

## Previews (Cycles; old bone_archer_v2 on the left, the new helm on the right)
- previews_helm/preview_topdown_game.png: game-distance top-down (60° elevation, 14 m, 50 mm), walk f10
- previews_helm/preview_topdown_game_crop3x.png: the same image cropped and scaled 3x with nearest-neighbour (phone-pixel look)
- previews_helm/preview_topdown_ortho_close.png: straight down, close, attack1 f12
- previews_helm/preview_threequarter.png: 3/4 close view, idle

Note: EEVEE Next shows false black patches on the bones in this file (a render-engine artifact). The GLB data is identical to v2, so use Cycles or the game for previews.
