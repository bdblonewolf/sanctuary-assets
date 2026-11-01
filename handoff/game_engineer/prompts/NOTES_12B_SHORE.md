# NOTES 12B - isle shore: stone tiles, square edge, how to blend

Findings only. Nothing here belongs in FIX1. Source: the live bundle routes-DWORE8MA.js (pretty-printed r.js). The references are minified names plus code anchors.

## 1. Why the isle land shows blue stone tiles
- `LE.loadLib()` takes its floors from the dungeon kit (`fs.sanctuary.kit`): `Tile1_01_lambert2_0`, `Tile2_01_lambert2_0`, `Tile3_01_lambert2_0` (as `floor`, 1 m).
- In `LE.buildZone(lib, zone, px, py)`: `v = i ? e.floorsDark : e.floors`, where `i = tE.has(zone.id)` and `tE = Set(town, wild)`. floorsDark is the same kit tile darkened by `ME()` (x0.32/0.34/0.38).
- Every tile that is not water (`m === $T`, $T = 4) pushes one kit floor instance, whatever its type. Isle Grass, Grass2, Sand, Sand2, Dirt and beach all become `Tile1/2/3` dungeon stone. Isle is not in tE, so it gets the undarkened, bluer kit tiles.
- Solid outdoor tiles (not Wall) also get `lib.rock` unless a border prop stands there. This explains the grey kit rocks on beach tiles.
- Only Martsirt has a real outdoor ground: `LE.addTownGround()` uses `m_ground_blend`, textures `models/town/ground_v1/g_{grass,dirt,stone,mud}_{bc,n}.jpg` and `martsirt_splat.png`/`martsirt_ao.png`. It is a ready template for an outdoor splat ground.

## 2. Where the land/water edge is drawn
- On sea maps (`BT(id,...)` true, which includes isle) buildZone skips water tiles entirely (`s || f.push(...)`). Land is 1 m kit tiles at y=0.
- The ocean is one 520x520 m plane at y=-0.4 (`JT.placeOcean`). The coastline is therefore the hard square outline of the tile grid at y=0, with a 0.4 m vertical drop to the water and no skirt.
- Map corners look square for two reasons. The tile grid stops at the map rectangle, and the ring (backdrop_near_rect_*) is discarded inside the exact map rectangle by `edgeCut()` (`uClip`), so the ring's sea slope meets the grid along straight lines.
- Foam (`placeFoam`) and the ocean shade use the step 6 distance texture. It does not change the land.

## 3. Step 6 distance texture (reusable)
- `JT.placeOcean`: grid s = w+64 by c = h+64 (offset 32 tiles). Land/in-map non-water = 0, water seeds = 1e6, two-pass chamfer (1 / 1.414).
- The result goes into an RGBA8 DataTexture `R_`. R = clamp(d-1, 0, 12)/12 (water distance from land; land = 0). G and B are unused. Linear filtering, ClampToEdge.
- Shader uniforms are `tEdgeDist` and `uSpan`. World xz maps to uv = (xz + 32) / (w+64, h+64).

## 4. Proposal: sand / wet-shore blend band and rounded corners
A. Outdoor ground instead of kit tiles (all yE zones except town/wild, or all outdoor):
   - Replace the per-tile kit floor with one ground mesh per zone window: a subdivided plane, 2 quads per tile.
   - Give it an `m_ground_blend`-style material: a tile-type splat DataTexture (1 texel per tile, linear filter, so edges soften by themselves) that picks grass / sand / dirt / stone.
   - Dungeons keep the kit tiles.
B. Shore band from the distance texture:
   - Add a second chamfer pass in placeOcean with the seeds inverted (water = 0) and write land-to-water distance into G.
   - Then sdf = R*12 - G*12 gives a signed coast distance, positive at sea.
   - In the ground shader: wet = 1 - smoothstep(0.0, 1.5, landDist) darkens and smooths the sand (wet-sand albedo, roughness about 0.35). sand = 1 - smoothstep(1.5, 4.0, landDist) forces the sand layer over grass near water. A thin foam/wet line sits at landDist < 0.3.
C. Rounded coast and corners:
   - In the ground vertex shader, sample the bilinear sdf. For vertices with sdf > -0.5, lower y toward -0.8 (`y = -0.8 * smoothstep(-0.5, 1.0, sdf)`), so the ground shelves under the ocean (-0.4) instead of ending on a square step.
   - Bilinear filtering of the 1-texel-per-tile field rounds every 90-degree tile corner (radius about 0.7 tile).
   - Discard fragments with sdf > 1.5 to hide the underwater skirt.
   - Only visuals move. Walkability stays tile-based.
   - Map corners: also round the `edgeCut()` uClip rectangle (rounded-rect test, radius about 6 m) so the ring's sea slope and the ground meet without a straight seam.
D. Border kit 12I coast pieces (see section 5). Use them along long straight coast runs and at map corners, on top of A-C.

## 5. Border kit 12I (use this kit, not backup_pre12H)
Path: `/workspace/sanctuary_env/outdoor/glb_v5_maps/border/`, index `border_kit_v5.json` (stage 12I), 184 GLBs (46 pieces x 4 seasons).
- Path convention: each coast piece starts at the origin heading +X, land on the LEFT (-Z) and sea on the RIGHT (+Z), the same as shore_foam_strips_v2. One slot is 6 m.
  - straight6 / straight6b / straight6c end at (6,0,0).
  - outer (convex land corner, R=6) ends at (6,0,-6) heading -Z; rotate the next piece +90 degrees.
  - inner (concave, R=6) ends at (6,0,+6); rotate the next piece -90 degrees.
- Beaches `beach_{sand,shingle}_{straight6,outer,inner}_v5_{season}`: land edge on the path line, tucked 0.4 m inland below ground, shelving to y=-0.8 at 4 m seaward, waterline about 2.8 m out. Shingle has a storm berm about 1.2 m out. Winter has snow above the high-water line. These are the isle beach pieces: they sit under walkable land and run seaward, so they never block tiles.
- Sea cliffs `seacliff_{straight6,straight6b,straight6c,outer,inner}_h{3,5,8}_v5_{season}`:
  - lip on the path at y=h; battered sea face (about 70-73 degrees);
  - toe at y=-1.4, reaching 2.2 / 3.0 / 4.2 m seaward at h3/h5/h8 (up to about 4.6 m with lumps);
  - 1.2 m top, then a back slope reaching y=0 at 1.2+0.5h m inland (2.7 / 3.7 / 5.2 m). Those inland metres must be solid/non-walkable tiles, so use cliffs only on non-walkable headlands, the border band, or off-map.
- Endcaps `seacliff_endcap_{left,right}_h{3,5,8}_{a,b}_v5_{season}`, one 6 m slot each:
  - RIGHT closes the END of a run. Place it where the next piece would go, same heading. Nothing chains after it.
  - LEFT closes the START. Place it one slot before the first piece, so its (6,0,0) end sits on the run start. Nothing chains before it.
  - a/b are spire variants.
- Steps `seacliff_step_{h3h5,h5h3,h5h8,h8h5}_v5_{season}`: one 6 m slot between runs of different height. For h3<->h8, chain two steps (h3h5+h5h8 or h8h5+h5h3).
- Rule 12I: every free end of a cliff run gets an endcap of the matching height (left at the start, right at the end), and every height change gets a step. Endcaps and steps join straights of the same height (corners share the end section, so they can join outer/inner directly). No cliff run may end on a bare end wall.
- Border mounds `border_{peak,shelf,dune}_{a,b,c}`: unit footprint (max X/Z = 1 m), scale x8-x40, rotate freely. 12I removed flat tops.
- Placement sketch for isle:
  - trace the land/water boundary on a 6 m macro grid (a macro cell is land if 50% or more of its tiles are land) into closed loops of 6 m edges;
  - emit straight6 / outer / inner beach pieces along walkable shore;
  - switch to seacliff runs only where the macro edge's inland tiles are solid, and close each cliff run with endcaps, or a step where the next run has a different height;
  - keep the tile-level sdf shelf (4C) underneath, so gaps between the 6 m pieces and the 1 m tile coast never show a square step.

## 6. Needed from the env bot
1. Upload the 12I border kit to the asset repo. `.../models/outdoor/v5_maps/border/*` and `border_kit_v5.json` currently return 404 on raw.githubusercontent (checked 2026-11-01), so no stage can load them yet.
2. Outdoor ground texture set, tileable, 2-4 m repeat, albedo + normal (+ roughness in alpha): grass (4 seasons), dry sand, wet sand, shingle/pebble, dirt/path, mud (mires). The Martsirt ground_v1 grass/dirt/mud can cover the first pass, but there is no sand or wet sand.
3. Short beach variants for tight isle coves, because the 1 m tile coast is jagged against 6 m slots: `beach_{sand,shingle}_{straight3,outer3,inner3}` (R=3), plus a beach run end/taper piece (the beach equivalent of an endcap).
4. Beach-to-cliff transition pieces `seacliff_to_beach_{left,right}_h3`, so a cliff run can end into sand without an endcap spire every time.
5. Optional: a wet-sand/foam-line decal strip that follows the path convention, for the waterline at landDist < 0.3.

## 7. Other things seen (report only)
- Shot 2 (07:58, fog): the hero stands on blue kit stone running straight into the sea. Same cause as section 1.
- The dark spiky shapes are in-map 12B conifers, the pale-green blob in shot 1 is a 12B decid tree, and both are 6.5-9.5 m tall. FIX1 scales these trees down.
