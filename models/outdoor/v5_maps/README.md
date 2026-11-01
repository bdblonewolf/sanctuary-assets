# Sanctuary Stage 12B: map-pinned backdrops (glb_v5_maps)

These are new files only. `glb_v5/` is read and never written. The machine-readable source of truth is `maps_backdrop_v5.json`.

## Conventions
- 1 unit = 1 m, glTF Y-up. The origin is the ring centre, which is also the map centre. Plain glTF 2.0 GLB with no extensions, no lights, no cameras, and emissive ≤ 1.0. Every file is ≤ 4,000,000 B.
- Map placement: tile (x, y) maps to world (x − w/2, 0, y − h/2). Tile x runs along +X (east) and tile y along +Z (south), so north is −Z. All maps are axis-aligned, so **rotationY = 0 for every map**.
- **Yaw / bearing**: bearing = atan2(−z, x) in degrees. 0 = E (+X), 90 = N (−Z), 180 = W (−X), 270 = S (+Z).
- **Quadrants**: q = floor(((bearing + 45) mod 360) / 90), giving 0=E (315..45), 1=N (45..135), 2=W (135..225), 3=S (225..315). The boundaries sit on the diagonals, i.e. the map corners.
- **Inner edge**: there is a lip at y = 0 on radius = class (23/30/36/42/52 m). This is ≥ map corner distance + ~6 m (actual clearances 6.3–10.2 m). The near outer edge at 288 m meets the glb_v5 mid ring (~280 m).
- Sea level is y = −0.4 (water_Q) and the apron is at y = −0.1.
- COLOR_0.a is the aerial-fade weight ss(60, 2000, r), the same as glb_v5. COLOR_0.rgb is linear.

## Files
| file | what |
|---|---|
| `backdrop_near_c{23,30,36,42,52}_{summer,autumn,winter,dead}.glb` | Near ring per radius class and season, inner edge = class, out to 288 m. Nodes: `near_land_{Q}` (+child `trees_land_{Q}_n`) and `apron_{Q}`. Classes 30, 42 and 52 also have `near_sea_{Q}` (+`trees_sea_{Q}_n`; the terrain sinks below the sea away from the diagonals, keeps headlands on them, and has 4 m skirts on the radial edges) and `water_{Q}`. Trees exist only in summer and autumn (as in v5). |
| `trees_near_c{R}_{summer,autumn}_instances.json` | Tree instances (pos, set, quad, LOD band) so the engine can instance or hide them by quadrant. LOD bands: LOD0 < R+59 m, LOD1 < R+129 m, LOD2 beyond. Thinning weight 1/(1+((r−R)/55)^1.5), so detail stays nearest and drops off into the fog. |
| `backdrop_mid_quads_{S}.glb`, `backdrop_far_quads_{S}.glb` | glb_v5 mid/far rings re-packed by face centroid into `mid_{Q}` (+`trees_mid_{Q}`) / `far_{Q}`, with extras {quadrant, bearing_deg}. |
| `fog_valley_banks_v5_quads.glb` | glb_v5 valley fog banks split into `fog_{E,N,W,S}`. Use this instead of the glb_v5 file so sea quadrants can drop their fog. |
| `backdrop_islands_{isle,mires}_{S}.glb` | Open sea all round. Node `islands` (16 or 22 islets at 420–1500 m, vertex colour only) plus `water_E/N/W/S`. |
| `shore_foam_strips_v5.glb` | `shore_foam_strip_16m`, `_8m`, `shore_foam_corner_out_r6`, `_in_r6`. 3 m wide, 8 m texture tile. Each piece runs along local X with the land edge at local z = 0 (V = 0) and extends seaward to +Z (local). Place it at the waterline (y = −0.37) and yaw it so local +Z points out to sea (table below). |
| `shore_rock_kit_v5.glb` | 5 rocks: `shore_rock_a_boulder`, `b_slab`, `c_stack`, `d_cluster`, `e_seastack` (576–864 tris). They share material `ms_shore_rock_v5` and a 2x2 atlas (wet basalt / granite / lichen / salt crust), with a wet-line vertex colour. **Origin = waterline**; each base sinks to −0.6 m, so place at y = −0.4. Each has a child `col_*` convex hull (58–113 tris, no material) to use as a collider and never render. |
| `maps_backdrop_v5.json` | Per-map entries: kind, radius_class, clearance, quadrants, sea_segments, near/mid/far/fog file per season, `near_show_nodes`, `hide_mid_far_nodes`, `hide_fog_nodes`, islands. |

Foam yaw (rotation about +Y that turns local +Z, the seaward side, outward): S edge 0°, E edge +90°, N edge 180°, W edge −90° (+Z rotated by θ about Y → (sin θ, 0, cos θ)).

## Show/hide rule (one rule per quadrant)
- **Land quadrant**: show `near_land_Q`, `apron_Q`, `mid_Q`, `far_Q`, `fog_Q`.
- **Sea quadrant**: show `near_sea_Q` and `water_Q`; hide `mid_Q`, `far_Q`, `apron_Q`, `fog_Q`.
- `water_Q` appears only on sea quadrants. Land near rings contain gorges below sea level that would otherwise flood.
- Islands maps (isle, mires): load only the islands file plus the sky. Hide all fog nodes.
- Hiding a parent hides its child trees. Engines that flatten the hierarchy must hide `trees_*_{Q}*` together with their parent.

## Foam scroll / render state (node extras)
`fx = shore_foam`, `scrollV_per_s = 0.045` (wash toward land), `scrollU_per_s = 0.006`, `uvPulse: v += 0.06*sin(t*0.9)`. Render state: BLEND, depthWrite false, polygonOffset −1, y = water level + 0.03. Texture `t_shore_foam_v5` (1024×256 RGBA) tiles in U; V = 0 is the land edge, and alpha fades seaward.

## Class assignments
| class | maps |
|---|---|
| 23 | tollarch, spireroots, ashcamps, duneW |
| 30 | desert, ascent, iron, flotsam (sea N) |
| 36 | weald |
| 42 | briarE, waste, bluffs, ridge, coast (sea E/W/S) |
| 52 | wild (sea W) |
| islands | isle, mires |

## Scripts (`../src_v5_maps/`) in pipeline order
heightgen/meshprep → `build_maps.py` (near rings, one Blender run per class) → `repack_quads.py` (mid/far) → `repack_fog.py` → `gen_shore_tex.py` → `build_shore.py` (foam, rocks, islands) → `fix_water.py` (water winding fix, idempotent) → `fix_island_vcol.py` (islet sRGB→linear, idempotent) → `build_json.py` → `render_maps.py` (previews). Validation log: `validation_maps.txt`.

## Known weak spots
- Near files give 8–20 `MESH_PRIMITIVE_GENERATED_TANGENT_SPACE` validator warnings (0 errors), because normal-mapped prims ship without tangents. Exporting tangents would add ~0.7 MB per file and push some files over 4 MB.
- Mid/far quads split on existing faces, so the cut is ragged by ~1–3° around the diagonals. On sea maps the hidden quadrant leaves a vertical silhouette edge on the mountain ring at the diagonal.
- Tree counts are lower than v5 to meet the 4 MB budget. The nearest trees are low-poly cones/blobs.
- There are no trees in winter or dead (same as v5).
- Islets are vertex colour only, low and soft at distance.
- The water is a flat, low-roughness plane. Waves and glint come from the engine shader.
- The foam texture streaks are slightly blocky up close.
- The previews use a flat stand-in map ground, not the real tiles.
