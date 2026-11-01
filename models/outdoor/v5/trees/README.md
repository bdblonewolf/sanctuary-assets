# Sanctuary outdoor v5: mountain ring, sky, fog (src_v5/)
See `../outdoor_plan.md` ("v5 mountain scenery") for engine notes, and `../material_manifest_outdoor.json` key `"v5"` for materials and render states. Progress log: `PROGRESS.md`.

## Build order
1. `python3 heightgen.py <near|mid|far>`, then `python3 meshprep.py <layer>`
1b. `python3 forest_maps.py` (forest pass: tree density / deciduous stand / early-colour / tone maps)
2. `python3 bake.py <layers>` (use `SEAS=summer,autumn` to limit seasons). `python3 canopy_tex.py`, `python3 ph_tex.py`
3. `SEASONS=summer,autumn blender -b -P build_v5.py -- far`, `-- mid 48000`, `-- near 52000` (forest pass sizes; `SEASONS` limits which season GLBs are written, `FOREST=0` disables tree scatter/tone) (`PH=0` = previous v3-derived near textures)
4. `python3 fog_layout.py`, `python3 fx_tex.py`, `python3 sky_gen.py`, then `blender -b -P build_skyfx_v5.py`
5. `cd ../glb_v5 && node ../src_v5/validate_v5.js *.glb`
6. Renders: `final_renders.sh` (scenics; forest-pass re-renders via /workspace/v5work/forest_renders.sh), `python3 sheet_v5.py` (preview sheet). Game-camera renders were dropped (archived in v5/_archive/).

## Third-party assets (all CC0, Poly Haven, https://polyhaven.com, downloaded 2026-11-01 via api.polyhaven.com/files/<id>, 1K JPG)
| Asset | Authors | Maps used | Used for |
|---|---|---|---|
| rock_face_03 "Rock Face 03" | Dario Barresi (photography), Rico Cilliers (processing) | diff, nor_gl, arm | near-layer rock `ms_bd5_near_rock`. Luminance kept and colour graded to each season's v3 rock palette (summer/autumn: neutral cool grey since the forest pass) (`ph_tex.py` → `m_ph_rock_<season>_bc.jpg` 1K, `m_ph_rock_n.jpg` 512, `m_ph_rock_orm.jpg` 256) |
| snow_field_aerial "Snow Field Aerial" | Rob Tuytel | col, nor_gl, arm | near-layer snow `ms_bd5_near_snow` (lifted and cooled → `m_ph_snow_*`) |

Poly Haven `arm` = AO/Roughness/Metal, which is the same channel order as glTF ORM. `nor_gl` = OpenGL (+Y) normals, as glTF expects.
No Poly Haven HDRI is used. The sky domes are procedural (`sky_gen.py`): a CC0 HDRI is a photo of a real place with its own sun and ground, and it would not match the fixed hero layout, the alpenglow grade or the dead-season sky. Mid/far layers are baked procedurally (`bake.py`), not from Poly Haven.
Raw downloads are kept in /workspace/v5work/ph/ (not shipped).

## Trees: LOD / illusion-of-detail pass (2026-11-01)
Code: `trees_v5.py` (archetypes + LOD tiers, pure numpy), `build_v5.py` `scatter_trees()` (placement, per-instance variety, baked merge + instance JSON), `build_trees_v5.py` (archetype GLBs), `glbpost.py` (drops NORMAL on tree meshes, sets tree materials doubleSided).
- 5 shared archetypes: `conifer_a` (narrow spruce, sharp), `conifer_b` (fir, bushy), `conifer_c` (ragged pine, irregular whorls, bent leader), `decid_a` (round lumpy crown), `decid_b` (taller ovoid crown). Conifers = stacked star-shaped tiers with drooping outer tips; deciduous = merged jittered blobs in random 3D orientation.
- Per instance: height 0.7-1.4x of the layer base (near 11 m, mid 20 m, also scaled by the valley/crest tone map), width 0.8-1.25x (spruce a bit narrower, fir wider), lean up to 4 deg, random rotY, tint (season palette x value jitter 0.80-1.22 x hue jitter +-5%). Spruce is more likely higher up.
- Fake volume: AO/gradient in vertex colour (dark core and bottom, light tips and top; leader tip 1.28). No extra textures.
- Flat facets: tree primitives have no NORMAL attribute; the glTF spec makes the client compute flat normals (three.js GLTFLoader sets flatShading). This saves 12 B/vertex and reads as sharp needle tiers.
- Fog blend: COLOR_0.a = aerial fade (as for the terrain), and the AO contrast relaxes by up to 35% toward each layer's outer edge, so tier changes flatten into the haze.

### Path A, baked fallback (what the backdrop GLBs contain; works with no engine changes)
| Layer | Band (radius from ring centre) | Conifer | Deciduous |
|---|---|---|---|
| near | < 95 m | 3 tiers x 8-point star, 24 tris | 3 icosahedron blobs + trunk, 66 tris |
| near | 95-165 m | 2 tiers x 5, 10 tris | 2 octa blobs, 16 tris |
| near | > 165 m | 1 drooped 4-sided cone, 4 tris | 1 octa blob, 8 tris |
| mid | < 470 m | 2 tiers x 4, 8 tris | 1 octa blob, 8 tris |
| mid | > 470 m | 1 cone, 4 tris | 1 octa blob, 8 tris |
| far | painted crowns in the canopy texture (no geometry) | | |

### Path B, instancing (recommended; smaller and more detailed)
- `glb_v5/tree_<arch>_v5.glb` (about 8 KB each): meshes `tree_<arch>_LOD0` (262 conifer / 326 decid tris), `_LOD1` (64 / 60), `_LOD2` (12 / 16). Unit height 1 m, base at origin, Y up. COLOR_0 = AO/AOK grey (AOK = 1.35).
- `glb_v5/trees_v5_<season>_<near|mid>_instances.json`: `fields` = arch, lod, x, y, z, rotY, sx, sy, sz, leanX, leanZ, r, g, b (glTF space, metres; tint is linear and already multiplied by AOK). `lod` = the baked band index (near bands at 95/165 m, mid at 470 m).
- Engine: load the 5 GLBs once, and per (archetype, LOD) create one `THREE.InstancedMesh` (material `vertexColors: true, flatShading: true, side: DoubleSide`). Fill `setMatrixAt` with `M = T * Rz(leanZ) * Rx(leanX) * Ry(rotY) * S` and `setColorAt(r,g,b)`. Suggested LOD use: near lod0 -> LOD0, near lod1 -> LOD1, near lod2 + mid lod0 -> LOD1/LOD2, mid lod1 -> LOD2. The player stays near the ring centre, so static banding by radius = distance LOD. For a moving camera, rebucket by distance or use `THREE.LOD` per cluster or BatchedMesh. Then hide the `trees_v5_*` nodes of the backdrop GLBs (they are the fallback). The terrain and its painted canopy stay as they are.
- Cost: 5 x 8 KB of meshes + 64 B/instance matrix + 12 B colour = about 0.8 MB of GPU buffers for all near + mid trees of one season, vs about 1.6 MB of baked tree geometry.
