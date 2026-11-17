# Knell Aura v3b: animation fix

v3b replaces only `knell_aura_fx.js` from v3 (commit 2c803ae). Brian reported that v3 looked static in game.

**Cause:** the v3 ShaderMaterials sampled `map` with the raw UV and ignored `tex.offset` and `tex.repeat`. Because of that, the flame, fork and peal flipbooks (4x4) and the 2x1 mark states showed the whole atlas as one frozen sheet.

**Fix:** both shaders now sample `mapOffset + clamp(uv) * mapRepeat`, using uniforms that point at each texture's own `offset` and `repeat` vectors. The flipbook frames now advance, and the marks switch between unlit and lit.

**What stays the same:** the API, hooks, opts (scale 0.8), textures and centering are unchanged from v3. Keep loading the same textures:
- sigil and haze from `characters_art/fx_rites/knell/knell_aura_v3/`
- marks from `characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png`
- flame, embers and trail from `fx_rites/fireball/`
- fork from `fx_rites/arc_whip/arc_whip_impact_fork_4x4_v2.png`

**Engineer change:** load `knell_aura_fx.js` from `characters_art/fx_rites/knell/knell_aura_v3b/` instead of `knell_aura_v3/`.

NOT TESTED in game.
