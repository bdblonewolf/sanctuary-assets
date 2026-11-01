# Bone Axeman

Starter monster for the Sanctuary family `13_skeleton_basic`. The style target is realistic, worn gothic Diablo 1/2, with no element hue tint.

- **File:** `bone_axeman.glb` (1.25 MB). Y up, metres, feet at y=0, single skin.
- **Height:** 1.80 m
- **Textures:** 1024 max, embedded PNG. No glTF extensions are used.
- **Validator:** Khronos gltf-validator reports `VALIDATOR errors 0 warnings 9 infos 7`. The warnings are non-blocking, for example NODE_SKINNED_MESH_NON_ROOT and unused data.

## Sources and licences

| Part | Source | Licence |
|---|---|---|
| Skeleton body mesh, skin weights, rig | danielmclogan, "Skeleton animated", https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3 | CC-BY-4.0 (credit required, see below) |
| Weapon: briar_hatchet | In-house Sanctuary weapon (sanctuary-assets repo, commit eb1b583 / 2b7ad63) | Project-owned |
| Rag loincloth/back rag, bracer, bone texture | Procedurally generated in Blender by this pipeline (_pipeline/accessories.py, bonetex.py) | Project-owned / CC0 |
| Animations | Mixamo Pro Melee Axe Pack | Adobe Mixamo terms (see note) |

Animation clips: Adobe Mixamo motion data (from the project library at sanctuary/assets3d/mixamo/) retargeted onto this rig. These are Mixamo animations only, with no Mixamo characters. They are used under Adobe's Mixamo terms, which allow use in games, but they are not CC-licensed. This follows existing project precedent.

## Credit (CC-BY-4.0, must ship with the asset)

This work is based on "Skeleton animated" (https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3) by danielmclogan (https://sketchfab.com/danielmclogan) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)

Changes: re-textured, accessories added, and retargeted to new animations.

## Animation clips (30 fps, in place)

| Clip | Duration | Frames | Source |
|---|---|---|---|
| idle | 1.80 s | 55 | `Pro Melee Axe Pack/standing idle.fbx` |
| walk | 1.33 s | 41 | `Pro Melee Axe Pack/standing walk forward.fbx` |
| attack1 | 2.40 s | 73 | `Pro Melee Axe Pack/standing melee attack horizontal.fbx` |
| attack2 | 2.27 s | 69 | `Pro Melee Axe Pack/standing melee attack downward.fbx` |
| hit | 1.47 s | 45 | `Pro Melee Axe Pack/standing react large gut.fbx` |
| death | 4.40 s | 133 | `singles/Dying.fbx` |

## Bend/stretch test

This is the worst edge-length ratio against the bind pose, sampled every second frame of every clip.

```
PER {'attack1_Armature': 2.26, 'attack2_Armature': 2.26, 'death_Armature': 2.99, 'hit_Armature': 2.28, 'idle_Armature': 2.26, 'walk_Armature': 1.74}
SKIN 2.99 at death_Armature f46 edge(81, 82) z0.31
CLOTH 0.00 at 
STRETCH worst=2.99 at death_Armature f46 rag_back edge(81, 82) z0.31
```

## Previews

`previews/bone_axeman_front.png`, `previews/bone_axeman_side.png`, and `previews/bone_axeman_attack.png` (attack1 frame 26). These are Cycles renders at 600x800.

## Known issues

- Loincloth reads slightly boxy.
- Worst stretch, 2.99x, is on the rag_back cloth edge during death. All bone-skin stretch is ≤2.3x.

## Rebuild

The scripts are in `../_pipeline/`. Skeletons use `build_skel.sh`, then `fin.sh`. Zombies use `zombie_build.py` with a spec, then `retarget2.py` with `cfg_zombie.json` and ZCFG, then `fin.sh`. Working files are in `work/`.
