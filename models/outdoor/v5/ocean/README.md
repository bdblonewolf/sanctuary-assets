# ocean_normal_v1.jpg

Tileable 1024x1024 tangent-space normal map (OpenGL, +Y up) for open sea water.
Made for Sanctuary from a procedural wave spectrum (two bands: swell + ripples,
wind about 26 deg off +X). No third-party source. Licence: CC0.

Use: MeshStandardMaterial normalMap, wrapS/wrapT RepeatWrapping,
repeat about 1 tile per 24 m, normalScale 0.6, scroll offset slowly (two copies at
different speeds read best).
