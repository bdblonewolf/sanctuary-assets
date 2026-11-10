# Campfire bundle: ORIGINAL fire (pass 1) + NEW black smoke (v2)
Per Brian (2026-11-09): use the original fire, use the new black smoke. Fire v2 is not in this bundle.
- Fire: campfire_flame_flipbook.png (+ _b variation, base glow). 4x4, 16 fps, additive. UV math as in USAGE.md of the campfire_flame folder (same 4x4 math as the fireball core sheet).
- Smoke: campfire_smoke_flipbook_v2.png, normal blend (NOT additive). Script: smoke_shader_v2.js, notes: SMOKE_v2.md.
- campfire_fire_shader_v2.js / SHADER_v2.md are optional (alpha clamp, depth fade). The alpha clamp was tuned for fire v2's sheet; on the original fire it may need re-tuning of uLo/uHi, since the original edges are softer.
NOT TESTED in game. Shader GLSL NOT COMPILED. Local only, not pushed.
