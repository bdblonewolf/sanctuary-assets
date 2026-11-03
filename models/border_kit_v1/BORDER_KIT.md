# Border kit v1 (world_v1/border_kit/)

Every area gets a uniform scenic ring plus a line of collidable border props, rebuilt to the zone's bounds whenever the zone changes (standing rule). The ring has no black gaps, nothing clips into the map, and it is mirrored across seams.

## Files
- `build_kit.py`: Blender build of the kit GLBs. It reuses the v5 border rocks/peaks, ashen_v1 shore rocks and v5 plants.
- `glb/bk_<style>_<season>.glb`: 6 styles (coast_land, sea, town, forest, mountain, desert) × 4 seasons (summer, autumn, winter, dead) = 24 files. Node name = piece. `kit_manifest.json` lists lengths, pivots, tris and height ranges.
- `border_styles.json`: styles, prop rules, spacing, margins, phone budget, zone entries and the seam rule.
- `gen_border.py`: the layout generator used for the proofs. It writes `out/layout_<zone>.json`.
- `proof_render.py`: before/after renders from the real game camera, with the void/gap metric.
- `camera_margin.py` with `camera_margin_table.json`, and `margin_profiles.py` with `margin_by_style.json`: the frustum margin per style.

## Pieces (per style; pivot on the edge line, piece runs along +X, border rises toward −Z, three→Blender (x, −z, y))
| piece | length | notes |
|---|---|---|
| straight12_a / _b / _c | 12 m | 3 variants; craggy (coast/mountain), treed (forest/town), dune (desert) |
| straight6 / straight3 | 6 m / 3 m | fillers; any leftover < 3 m uses scaleX on the last piece (0.75–1.25) |
| corner_outer | 0 | convex map corner; next piece is rotated −90° |
| corner_inner | 0 | concave notch; next piece is rotated +90° |
| pass12 | 12 m | seam fallback: 6 m flat road, banks rise either side |
| endcap_land_to_sea / endcap_sea_to_land | 12 m | peaked end cap where a land run meets a sea run |
| sea straight / corners | 12, 6, 3 m | sloped sea face, seabed, stacks; the engine ocean plane stays underneath |

- Kit tris per piece: land straight12 is 736 (town 768), sea 896–1100, inner corner 1058–1568, endcap 896.

## Prop spacing (lip_outer, collidable unless noted)
- Coast and mountain: crag 5–9 m (jitter 1.2), spire, grass, gtree.
- Sea: shore_rock 7–16 m and seastack (no collider, they sit on water).
- Town and forest: dead/gothic trees 9–16 m; forest density ×1.25.
- Desert: scrub 5–11 m.
- Props are never placed on road/path/bridge/plank tiles, exit ±4 m, seam spans, or within 1.2 m of a world prop. Placement is crc32-seeded, so it is stable.

## Frustum margin (hero standing ON the edge; FOV 38, pitch 50, any yaw, zoom 6–40)
| style | portrait d14 | portrait d40 | landscape d14 | landscape d40 | built depth D |
|---|---|---|---|---|---|
| coast_land | 6.3 | 18.8 | 8.9 | 22.7 | 40 |
| mountain | 6.0 | 20.2 | 8.2 | 22.8 | 40 |
| forest | 7.7 | 17.5 | 9.3 | 25.6 | 40 |
| desert | 8.7 | 18.9 | 12.9 | 25.6 | 40 |
| town (fog 30/110) | 8.2 | 16.9 | 9.9 | 28.6 | 44 |
| sea / flat | 12.6 | 29.7 | 20.8 | 52.2 | 60 (+ 520 m ocean plane) |

## Phone budget (edge fill only; far/sky layers dropped)
- Kit: ≤ ~45k tris for a 160x150 zone (~27k for coast 42x112), about 1/3 in view.
- Border props: ≤ 150 instances, instanced per asset (≤ 8 draws).
- Kit pieces merged per material after layout (≤ 5 draws for the whole ring).
- Actual: coast 25.9k tris, 49 props; Martsirt 42.6k tris, 206 props.
  - FLAG: Martsirt is over the 150-instance guide. 121 props are collidable and the rest are trees. Instancing keeps draws ≤ 8. To trim further, raise the town tree spacing to 12–20 m.
