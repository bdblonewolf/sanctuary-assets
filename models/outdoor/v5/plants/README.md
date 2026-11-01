# Act II plants and dead trees (v5)
## Textures and the shared atlas (fix pass, Nov 1)
Every plant GLB is self-contained. It embeds one compact 1024² **palette PNG** (256 colours, binary alpha) laid out exactly like the shared atlas. Cells the plant never samples are blanked, which keeps each GLB between 179 and 245 KB.
All 7 plant GLBs use **one material with the same name: `mat_plant_atlas_v5`**. It is MASK with cutoff 0.5, double-sided, roughness 0.88, metal 0, and multiplied by `COLOR_0`. Every UV points into the same 1024 layout, so the shared atlas can replace the embedded texture with no UV change.

Shared atlas set in `textures/` (load once):

| file | bytes | use |
|---|---|---|---|
| `plant_atlas_v5_color.jpg` | 276,766 | sRGB colour, q90 (transparent texels are dilated colour) |
| `plant_atlas_v5_alpha.png` | 132,800 | 8-bit grey alpha (cut at 0.5) |
| `plant_atlas_v5_rgba.png` | 1,745,136 | optional single-file RGBA master (lossless, also the embed source) |

**To load the plant texture once** in three.js:
```js
const color = texLoader.load('plants/textures/plant_atlas_v5_color.jpg'); color.colorSpace = THREE.SRGBColorSpace; color.flipY = false;
const alpha = texLoader.load('plants/textures/plant_atlas_v5_alpha.png'); alpha.flipY = false;
const shared = new THREE.MeshStandardMaterial({ map: color, alphaMap: alpha, alphaTest: 0.5, side: THREE.DoubleSide,
  vertexColors: true, roughness: 0.88, metalness: 0 });
gltf.scene.traverse(o => { if (o.isMesh && o.material.name === 'mat_plant_atlas_v5') { o.material.dispose(); o.material.map?.dispose(); o.material = shared; } });
```
The texture flags matter: set `flipY = false` because glTF UVs have a top-left origin. `alphaMap` reads the green channel, and a grey PNG works for that. If you swap the material, the embedded PNG never goes to the GPU, though it is still downloaded inside the GLB. Cell rects are in `../src/atlas_layout.json`.
Dead trees use their own small `../trees/t_deadwood_v5.jpg` (256×1024) and their own material. They are not part of this swap.

## Conventions
- Units: metres, Y up, origin at the base centre. The base sits about 5 cm below y=0 so it stays grounded on slopes. Dead-tree roots dip to about −0.12 m.
- `COLOR_0` (vec3): baked AO gradient multiplied by the tint, matching the v5 archetypes. Multiply it with the albedo (three.js `vertexColors:true`).
- Material: a single `mat_plant_atlas_v5` per plant file (see above), with metal 0 and no emission. Trunks and cacti sit in opaque texels, so MASK has no effect on them.
- **Sway** uses `TEXCOORD_1`:
  - `x` = trunk bend weight, from 0 at the base to 1 at the top (quadratic).
  - `y` = leaf flutter weight, from 0 at the leaf root to 1 at the tip.
  - Amplitudes and frequencies are in node `extras.sway`. The phase is a hash of the instance's world XZ.
  - Palms also carry `extras.crown_pivot_m`.
  - Suggested vertex shader: `pos.xz += windDir * (sin(t*f1+ph)*a1*uv1.x) ; pos += normal * sin(t*f2+ph+pos.x*3.)*a2*uv1.y`.

| file | tris | bytes | notes |
|---|---|---|---|
| plant_palm_date_a_v5 | 926 | 244,704 | about 9.8 m with crown, slight bend, 22 live and 9 dead hanging fronds |
| plant_palm_date_b_v5 | 902 | 243,468 | about 8.5 m, strong bend, 20 live and 10 dead fronds |
| plant_palm_date_c_v5 | 878 | 242,236 | about 7.0 m, dying: 13 live fronds and a heavy brown skirt of 16 dead fronds |
| plant_cactus_column_a_v5 | 800 | 197,184 | 3.2 m, 8-rib column with 2 arms |
| plant_cactus_cluster_b_v5 | 864 | 207,552 | 2.6 m organ-pipe cluster of 6 stems, 6 ribs each |
| plant_agave_a_v5 | 593 | 244,160 | rosette of 24 leaves (outer ones dry) plus a dead 3.4 m flower stalk |
| plant_scrub_bush_a_v5 | 116 | 178,540 | 7 crossed cards and 5 stems, about 1 m tall and 2 m wide |
| ../trees/tree_dead_a_v5 | 984 | 219,676 | 7.2 m gnarled, twisted fluted trunk, root flare |
| ../trees/tree_dead_b_v5 | 984 | 219,676 | 6.2 m, leaning, broken top |

## CC0 credits (Poly Haven)
- Palm Bark (Charlotte Baglioni)
- Bark Brown 02 (Rob Tuytel)
- Quiver Tree 01 (James Ray Cock, Dario Barresi, Rico Cilliers): agave leaf strip
- Wild Rooibos Bush (James Ray Cock, Jenelle van Heerden): scrub twig/tuft sprites

Palm fronds were reworked in the fix pass: darker, more saturated olive with 78 leaflets per card, cards 0.68 m wide, and 2 to 4 more live fronds per palm. The dead skirt stays brown.
The frond, palm fibre and cactus skin cells are procedural and painted in `src/atlas.py`.
