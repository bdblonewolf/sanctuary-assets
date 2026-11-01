# Bone Archer

Starter monster for the Sanctuary family `13_skeleton_basic`. The style target is realistic, worn gothic Diablo 1/2, with no element hue tint.

- **File:** `bone_archer.glb` (1.26 MB). Y up, metres, feet at y=0, single skin.
- **Height:** 1.84 m overall including the helmet (the skull is about 1.79 m)
- **Textures:** 1024 max, embedded PNG. No glTF extensions are used.
- **Validator:** Khronos gltf-validator reports `VALIDATOR errors 0 warnings 10 infos 8`. The warnings are non-blocking, for example NODE_SKINNED_MESH_NON_ROOT and unused data.

## Sources and licences

| Part | Source | Licence |
|---|---|---|
| Skeleton body mesh, skin weights, rig | danielmclogan, "Skeleton animated", https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3 | CC-BY-4.0 (credit required, see below) |
| Weapon: bow | In-house Sanctuary weapon_bow.glb (sanctuary-assets repo) | Project-owned |
| Helmet with nasal, belt, bracer, bone texture | Procedural (this pipeline) | Project-owned / CC0 |
| Animations | Mixamo Pro Longbow Pack | Adobe Mixamo terms (see note) |

Animation clips: Adobe Mixamo motion data (from the project library at sanctuary/assets3d/mixamo/) retargeted onto this rig. These are Mixamo animations only, with no Mixamo characters. They are used under Adobe's Mixamo terms, which allow use in games, but they are not CC-licensed. This follows existing project precedent.

## Credit (CC-BY-4.0, must ship with the asset)

This work is based on "Skeleton animated" (https://sketchfab.com/3d-models/skeleton-animated-9210377c7a514cf6b48a31b9d3991ff3) by danielmclogan (https://sketchfab.com/danielmclogan) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)

Changes: re-textured, accessories added, and retargeted to new animations.

## Animation clips (30 fps, in place)

| Clip | Duration | Frames | Source |
|---|---|---|---|
| idle | 5.10 s | 154 | `Pro Longbow Pack/standing idle 01.fbx` |
| walk | 1.20 s | 37 | `Pro Longbow Pack/standing walk forward.fbx` |
| attack1 | 1.00 s | 31 | `Pro Longbow Pack/standing draw arrow.fbx` |
| attack2 | 0.70 s | 22 | `Pro Longbow Pack/standing aim recoil.fbx` |
| hit | 1.27 s | 39 | `Pro Longbow Pack/standing react small from front.fbx` |
| death | 3.07 s | 93 | `Pro Longbow Pack/standing death backward 01.fbx` |

## Bend/stretch test

This is the worst edge-length ratio against the bind pose, sampled every second frame of every clip.

```
PER {'attack1_Armature': 1.93, 'attack2_Armature': 2.03, 'death_Armature': 2.45, 'hit_Armature': 1.98, 'idle_Armature': 1.91, 'walk_Armature': 1.97}
SKIN 2.45 at death_Armature f58 edge(489, 504) z0.42
CLOTH 0.00 at 
STRETCH worst=2.45 at death_Armature f58 skeleton_body edge(489, 504) z0.42
```

## Previews

`previews/bone_archer_front.png`, `previews/bone_archer_side.png`, and `previews/bone_archer_attack.png` (attack1 frame 20). These are Cycles renders at 600x800.

## Known issues

- In the idle side view the bow passes through the leg.
- The Longbow pack clips stand side-on to the target, so the game should face the archer accordingly.
- No arrow mesh or quiver is included. Spawn the projectile in game.

## Rebuild

The scripts are in `../_pipeline/`. Skeletons use `build_skel.sh`, then `fin.sh`. Zombies use `zombie_build.py` with a spec, then `retarget2.py` with `cfg_zombie.json` and ZCFG, then `fin.sh`. Working files are in `work/`.
