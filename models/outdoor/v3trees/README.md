# v3trees - close-range green trees (Stage 12F)
Source: sanctuary_env/outdoor/glb_v3 (Oct 31). Each GLB: node sway_<name> with meshes <mesh>_LOD0 / <mesh>_LOD1,
2 primitives each: m_out_bark (bc/n/orm 1024) + leaf/needle cards (alphaMode MASK, doubleSided, 512 tex).
COLOR_0 = sway weight, NOT a colour: set material.vertexColors=false.
| file | mesh | LOD0 / LOD1 tris | height | size |
|---|---|---|---|---|
| tree_oak_gnarled_lush.glb | tree_oak_gnarled | 3632 / 470 | 8.5 m | 961 KB |
| tree_oak_gnarled_b_lush.glb | tree_oak_gnarled_b | 6248 / 638 | 8.0 m | 1142 KB |
| tree_oak_gnarled_autumn.glb | tree_oak_gnarled | 3632 / 470 | 8.5 m | 961 KB |
| tree_oak_gnarled_bare.glb | tree_oak_gnarled_bare | 2702 / 250 | 7.4 m | 837 KB |
| tree_pine_dark.glb | tree_pine_dark | 844 / 628 | 14.0 m | 805 KB |
| tree_pine_dark_snow.glb | tree_pine_dark | 844 / 628 | 14.0 m | 833 KB |
Seasons: summer lush+pine_dark, autumn autumn+pine_dark, winter bare+pine_dark_snow. Cache tag ?v=12f.
