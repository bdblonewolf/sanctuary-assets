# Bone Swordsman

Starter monster for the Sanctuary family `13_skeleton_basic`. The style target is realistic, worn gothic Diablo 1/2, with no element hue tint.

- **File:** `bone_swordsman.glb` (1.17 MB). Y up, metres, feet at y=0, single skin.
- **Height:** 1.78 m
- **Textures:** 1024 max, embedded PNG. No glTF extensions are used.
- **Validator:** Khronos gltf-validator reports `VALIDATOR errors 0 warnings 4 infos 4`. The warnings are non-blocking, for example NODE_SKINNED_MESH_NON_ROOT and unused data.

## Sources and licences

| Part | Source | Licence |
|---|---|---|
| Skeleton body mesh, skin weights, rig | danielmclogan, "Skeleton animated", https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3 | CC-BY-4.0 (credit required, see below) |
| Weapon: parish_blade | In-house Sanctuary weapon (sanctuary-assets repo, commit eb1b583 / 2b7ad63) | Project-owned |
| Rag belt with tail, bone texture | Procedural (this pipeline) | Project-owned / CC0 |
| Animations | Mixamo Sword and Shield Pack | Adobe Mixamo terms (see note) |

Animation clips: Adobe Mixamo motion data (from the project library at sanctuary/assets3d/mixamo/) retargeted onto this rig. These are Mixamo animations only, with no Mixamo characters. They are used under Adobe's Mixamo terms, which allow use in games, but they are not CC-licensed. This follows existing project precedent.

## Credit (CC-BY-4.0, must ship with the asset)

This work is based on "Skeleton animated" (https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3) by danielmclogan (https://sketchfab.com/danielmclogan) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)

Changes: re-textured, accessories added, and retargeted to new animations.

## Animation clips (30 fps, in place)

| Clip | Duration | Frames | Source |
|---|---|---|---|
| idle | 3.60 s | 109 | `Sword and Shield Pack/sword and shield idle.fbx` |
| walk | 1.10 s | 34 | `Sword and Shield Pack/sword and shield walk.fbx` |
| attack1 | 1.50 s | 46 | `Sword and Shield Pack/sword and shield slash.fbx` |
| attack2 | 3.53 s | 107 | `Sword and Shield Pack/sword and shield slash (2).fbx` |
| hit | 0.70 s | 22 | `Sword and Shield Pack/sword and shield impact.fbx` |
| death | 2.30 s | 70 | `Sword and Shield Pack/sword and shield death.fbx` |

## Bend/stretch test

This is the worst edge-length ratio against the bind pose, sampled every second frame of every clip.

```
PER {'attack1_Armature': 2.29, 'attack2_Armature': 2.4, 'death_Armature': 2.27, 'hit_Armature': 2.14, 'idle_Armature': 2.39, 'walk_Armature': 1.94}
SKIN 2.40 at attack2_Armature f20 edge(4856, 4857) z0.03
CLOTH 0.00 at 
STRETCH worst=2.40 at attack2_Armature f20 skeleton_body edge(4856, 4857) z0.03
```

## Previews

`previews/bone_swordsman_front.png`, `previews/bone_swordsman_side.png`, and `previews/bone_swordsman_attack.png` (attack1 frame 16). These are Cycles renders at 600x800.

## Known issues

- The rag belt reads as a hoop floating around the open pelvis.
- No shield, even though the clips come from the sword-and-shield pack. The off hand is empty.

## Rebuild

The scripts are in `../_pipeline/`. Skeletons use `build_skel.sh`, then `fin.sh`. Zombies use `zombie_build.py` with a spec, then `retarget2.py` with `cfg_zombie.json` and ZCFG, then `fin.sh`. Working files are in `work/`.
