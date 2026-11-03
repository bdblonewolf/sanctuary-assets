# grave_risen_v2.glb (mesh upgrade)

A higher-quality rebuild of the Grave Risen zombie mesh (Grove Mauler bear quality). The v1 files are unchanged.

- Mobile copy (live): `grave_risen_v2.glb`, 20,349 tris, textures 1024 JPEG, 1.3 MB. No meshopt or Draco.
- Master (uncompressed): `masters/grave_risen_v2.glb`, same mesh with 2048 color and normal plus 1024 ORM, 3.1 MB.
- Size: 1.334 x 0.446 x 1.75 m. Single skinned mesh, A-pose.
- Rig: the same 52-bone mixamorig skeleton as v1 (male_regular base). Weights were transferred from the v1 mesh, so the existing grave_risen clips (including `dismember/grave_risen_full.glb`) should play on it unchanged. The file itself has no clips. The dismember pieces are still built from the v1 mesh.
- Preview: `previews/grave_risen_v2.png`. Made with Hunyuan3D-2.1 from the existing concept, baked and graded in Blender.

## Cleanup pass: gaps, stretch, clipping (Nov 3, 2026)
Only geometry and weights changed. The skeleton, the 54 nodes and names, the 52 joints, and the clips in `dismember/grave_risen_full.glb` are unchanged. There are no new `_v2` clips. No meshopt or Draco.
- **Gaps:** 1193 open boundary edges (14 holes) plus a 1-tri floating shell went to 0 boundary and 0 non-manifold. The model is now 1 closed shell, and nothing is see-through.
- **Tris:** 20,349 went to 21,162 (+4.0%).
- **Weights:**
  - Weights were smoothed with 40 Laplacian passes, with up to 4 influences.
  - The hands were re-weighted.
  - The robe is weighted to Hips/Spine and blends into the legs toward the hem (up to 80%), so the hem follows the knees instead of the legs pushing through it.
- **Measured on every frame of idle, walk, attack, hit and death.** The table gives worst stretch as max edge, p99.9 edge and p99.9 triangle area, then worst penetration.

| clip | stretch before (max/p99.9e/p99.9a) | stretch after | penetration before | penetration after |
|---|---|---|---|---|
| idle | 14.7 / 7.06 / 8.33 | 3.71 / 2.40 / 3.02 | arm 7.9 cm, cloth 3.0, legs through robe 1.0, leg-leg 2.5 | arm 3.2, cloth 1.3, legs through 3.1 (2 v), leg-leg 0 |
| walk | 18.5 / 8.51 / 9.70 | 4.36 / 2.70 / 4.49 | arm 7.8, cloth 5.0, legs through 5.5, leg-leg 6.9 | arm 7.5, cloth 4.1 (5 v), legs through 4.5 (2 v), leg-leg 0 |
| attack | 17.0 / 9.15 / 11.0 | 5.49 / 3.43 / 4.97 | arm 7.8, legs through 3.9 | arm 7.4, cloth 6.1 (4 v), legs through 0 |
| hit | 15.4 / 9.44 / 12.9 | 6.91 / 3.41 / 6.39 | claw 0.8, arm 5.3, legs through 3.7 | claw 0, arm 7.7, cloth 3.0 (5 v), legs through 0 |
| death | 20.5 / 9.76 / 10.7 | 5.32 / 3.05 / 3.82 | arm 7.8, cloth 7.7 (342 v), legs through 5.1, leg-leg 7.8 | arm 8.0 (7 v), cloth 6.8 (244 v), legs through 2.0, leg-leg 0 |

- **Remaining clipping:**
  - The upper arm sits under the shoulder collar/cape in every pose (about 7.5 cm, hidden under the cloth).
  - In death, the robe folds into the knees during the collapse.
  - Both come from the poses. Fixing them would need `_v2` clip copies.
- **Texture:** the texture was not changed, so the hole patches use stretched existing texels.
- **Preview:** `previews/grave_risen_v2_cleanup.png`.
