# Ground blending note (v5_ground) — grass / dirt / road mixing

## Inputs
Every set in `materials/ground_manifest.json` has albedo (sRGB JPG), normal (OpenGL +Y) and ORM (R=AO, G=rough, B=metal=0).
UVs are world-space, `uv = worldXZ / tiling_m`, so every layer can use its own tiling on the same mesh with no extra UV channels.

## Weights: two options
**A. Vertex colour (cheapest, phone default).** This is for the terrain mesh at roughly 1 to 2 m vertex spacing.
- `COLOR_0.r` = dirt_mud
- `COLOR_0.g` = road
- `COLOR_0.b` = grass_dead (or ash in burnt zones)
- grass_dark = `1 - r - g - b`, the base layer. Clamp it at 0 and renormalise.
- Use COLOR_0 as **vec3**. In three.js, vec4 vertex colours also multiply alpha.

**B. Splat texture.** Use this when transitions need to be sharper than the vertex spacing.
- One RGBA8 splat per terrain chunk at 0.5 m/texel, with the same channel meaning as above. A = optional ash / scorch.
- Use linear filtering and no mips beyond 2 levels.

## Height-blended transitions (recommended, no extra textures)
Plain linear weights look like soft airbrush. To sharpen them, use each layer's "height" taken from its albedo luminance multiplied by ORM.r (AO). Cracks and gaps sit low; stones and tufts sit high.
```glsl
float hl(vec3 alb, float ao){ return dot(alb, vec3(0.3,0.59,0.11)) * ao; }
// w_i = vertex/splat weight, h_i = hl(...) of that layer
vec4 W = vec4(wGrass, wDirt, wRoad, wDead);
vec4 Hh = vec4(hG, hD, hR, hX);
vec4 x = W + Hh * 0.6;                      // 0.6 = how much height bites into the weight
float m = max(max(x.x,x.y),max(x.z,x.w)) - 0.12;  // 0.12 = transition width
vec4 b = max(x - m, 0.0); b /= (b.x+b.y+b.z+b.w);
// blend albedo / ORM linearly with b; blend normals with b then renormalise (or whiteout)
```
Mud and dirt then fill the gaps between grass, and road cobbles keep their edges when they meet mud.

## Road specifics
- `ground_road` is **directional**: U runs across the road and V runs along it. The ruts are at U = 0.28 and 0.72, the dead-grass crown at U = 0.5, and the grass verges at U = 0 and 1.
- One tile is 4 m wide. For a hand-placed road strip mesh, use `u = across_m / 4`, `v = along_m / 4`.
- On a world-XZ terrain, only roads running along world Z line up. For curved or rotated roads, use a separate road strip mesh (decal-style, +2 cm, polygonOffset) and keep the terrain splat G channel for the soft verge only.
- It also tiles across U, so a 2-lane road is `u = across_m / 4` with 8 m width.

## Hiding repetition
- Multiply albedo by a low-frequency world-space macro tint (one 256 px greyscale noise at roughly 40 m/tile, range 0.85 to 1.1). The textures were already flattened at tile scale, so this macro variation will not double up.
- The suggested tilings in the manifest are minimums. At an ARPG camera height of 12 to 20 m, use sand 8 m, coast 6 m, mud 2.5 to 4 m, grass 3 to 4 m, ash 2 to 3 m, road 4 m (fixed by the road width).
- An optional second sample at 0.37× scale for the grass and sand albedo only (`mix(a, a2, 0.35)`) breaks up patterns. It costs one texture fetch.

## Phone budget
Per pixel, 4 layers × 3 textures is 12 fetches, which is too many for low-end phones. For low quality:
- Blend only albedo + ORM for 4 layers.
- Use one shared normal map (grass or dirt), or skip normals entirely.
- Or bake the blended result into a 1–2 K chunk texture offline.
