Textures were made with Python/PIL from:
- char: Poly Haven burned_ground_01 1k (diff desaturated and darkened to 42%, nor_gl, arm), plus a crack mask from ambientCG Ice003 colour (high-pass of the cell borders, wrap-aware blur). That mask darkens the cracks to ember red in bc, and becomes char_ember.
- ice: ambientCG Ice001 1k (Color greyed and tinted blue; NormalGL; ORM = R 0.75+0.25*disp, G rough*0.6+0.05, B 0).
Everything is Lanczos-downscaled to 512, so tiling survives (a uniform downscale keeps the wrap).
Packs and licences: /workspace/free_packs/{polyhaven_burned_ground_01,ambientcg_ice}/SOURCE.txt (all CC0 1.0).
