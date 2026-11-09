# Behest Bānspere — usage (final)

## Mesh
- File: `behest_banspere_lance.glb`
- Length ≈ 2.485 m; head width ≈ 0.415 m; tris = 7800
- **Tip = +Z** (glTF Y-up; Blender source tip was local −Y). Origin at butt (grip end).
- Scale (1,1,1). Hurl as a projectile along local +Z.

## Embedded PBR
- Base Color: aged ivory bone (weathered / stained). Crevices + cord wraps stay near-black.
- Normal: cortical grain + cracks + pores
- Roughness: dry-matte bone
- Emission: dark crimson runes in carved grooves only (subtle — no orange wash)

## Particle FX (additive / alpha)
| File | Role | Anchor |
|------|------|--------|
| `bow_wave.png` (+ `bow_wave_4x4.png`) | V chevron cutting **ahead** of tip | Apex at tip **+0.05 m along +Z**. Sprite left = forward. Apex at u≈0.14 from left. Arms sweep back symmetrically around the head. Quad world width ≈ 0.87 m. |
| `trail_v.png` (+ `trail_v_4x4.png`) | V wake **trailing** behind tip | Apex at tip **−0.08 m along +Z** (just behind tip). Sprite left = forward / attachment. Apex at u≈0.08 from left. Smooth alpha falloff → fully transparent at far end (no hard cut, no laser bar). Quad world length ≈ 1.68 m. |
| `swirl_wisps_4x4.png` | Swirling crimson wisps | Mid-trail / along shaft |
| `sparks_4x4.png` | Embers / sparks | Near tip + mid-trail, thinning rearward |
| `impact_flare.png` | Tip impact flare (4×4 sheet) | Tip / just ahead |
| `handle_aura.png` | Faint grip aura (4×4 sheet) | Butt / grip |

### Placement notes (runtime)
1. Orient FX quads so sprite **left** aligns with flight **+Z** (apex leads).
2. Bow wave: place so the V apex sits at/just beyond the blade tip; arms wrap the head, not a solid plate covering it.
3. Trail: attach just behind the tip; arms open rearward with wisps/embers; alpha must reach ~0 at the far end.
4. Additive blend, dark crimson — do **not** brighten sprites. Keep blacks.

### Raw URLs (main)
```
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/behest_banspere_lance.glb
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/bow_wave.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/bow_wave_4x4.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/trail_v.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/trail_v_4x4.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/swirl_wisps_4x4.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/sparks_4x4.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/impact_flare.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/handle_aura.png
https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/behest_banspere/USAGE.md
```

## Color lock
Dark crimson only on emission / FX. No orange / yellow shift. Keep blacks in crevices and wraps.
