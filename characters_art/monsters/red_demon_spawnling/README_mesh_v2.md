# red_demon_spawnling_v2.glb (mesh upgrade)

A higher-quality rebuild of the Fallen Spawnling mesh (Grove Mauler bear quality). The v1 files are unchanged.

- Mobile copy (live): `red_demon_spawnling_v2.glb`, 21,905 tris, textures 1024 JPEG, 1.6 MB. No meshopt or Draco.
- Master (uncompressed): `masters/red_demon_spawnling_v2.glb`, same mesh with 2048 color and normal plus 1024 ORM, 4.1 MB.
- Size: 1.02 x 0.35 x 1.446 m before the tail fix (0.416 m deep after it) (same height as v1). Single skinned mesh, A-pose.
- Rig: the same 52-bone mixamorig skeleton as v1 (male_regular base). Weights were transferred from the v1 mesh, so the clips in `red_demon_spawnling_anim_v2.glb` should play on it unchanged. The file itself has no clips.
- Loincloth recolored from teal to the concept's brown.
- Preview: `previews/red_demon_spawnling_v2.png`. Made with Hunyuan3D-2.1 from the existing concept, baked and graded in Blender.

## Tail fix (Nov 3, 2026)
- The tail was fused to the outside of the left thigh and hung beside the leg, so in the back view it looked offset and floating. It is now re-rooted at the tailbone: the root sits about 3 cm inside the loincloth/back at the base of the spine, and the tail sweeps back and down and curls up on the left. The old thigh stub was removed and capped flush.
- Tail weights: 100% Hips (the rig has no tail bones). The body around the tailbone is also about 100% Hips, so the root moves rigidly with it in every clip. Checked every frame of idle, run, attack, leap_attack, hit, death, attack2, death2 and death_old in red_demon_spawnling_anim_v2.glb: the root moves at most 1.7 mm relative to the body. The tail can briefly clip the legs in run and death2 because it has no bones of its own. There is no walk clip.
- 21,890 tris (was 21,905, -15). Same 52-joint skeleton and nodes, no meshopt or Draco. Width and height are unchanged (1.02 x 1.446 m). Depth is now 0.416 m because the tail sits behind the body.
- Preview: `previews/red_demon_spawnling_v2_tailfix.png`.
