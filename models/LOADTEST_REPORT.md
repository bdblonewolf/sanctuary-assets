# Headless three.js load test - Nov 2, 2026

GLTFLoader in Node with no WebGL: parse plus scene build, run against every `.glb` under `models/` and `characters_art/` on `main` (after 3d1b318).

- **800 GLBs: 722 OK, 78 flagged. None of the flagged files are real failures for the game.**
- 63 x `Image is not defined`: these files use `EXT_texture_webp`. Headless Node can't decode webp, but browsers load them. Root files under models/: armored_guard_knight, brazier, dungeon_props, knight_anim(_v10b), modular_dungeon_kit, plated_knight(_rigged), skeleton_animated, weapon_*, worn_banner. The rest are under characters_art/ (clothing pieces, NPCs).
- 15 x `no meshes`: animation-clip or empty-FX containers, which is expected. That is `characters_art/anim_v2/*` (14 clip files) and `models/outdoor/v5/fx_crow_flock_v5.glb` (no mesh; it is driven at runtime).
- `models/props_new/`: 38/38 OK (plain GLB, gltf-validator 0 errors; the only warnings are generated-tangent ones).
