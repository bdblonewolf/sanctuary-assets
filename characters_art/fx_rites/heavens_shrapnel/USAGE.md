# Heaven's Shrapnel (star_lash) — USAGE

Original procedural art, CC0. Mood reference: Diablo 2 skills/effects (feel only).
**Brian lock:** Divine / Holy Glass — transparent diamond-hard shards like fractured celestial cathedral stained glass; razor-thin **gold / white fire** trails; bright splash on impact; tick damage after initial hit.
**Colors:** stained-glass deep **crimson / cobalt / amber**, dark lead-came, gold+white trails. **KEEP BLACKS** — lead lines and dark backgrounds stay dark; never wash to gray.

## Mesh shards (GLB)

| File | Color | Length | Tris | Notes |
|------|-------|--------|------|-------|
| `heavens_shrapnel_shard_a.glb` | deep crimson | ~0.44 m | 152 | variant A |
| `heavens_shrapnel_shard_b.glb` | cobalt | ~0.36 m | 152 | variant B |
| `heavens_shrapnel_shard_c.glb` | amber | ~0.50 m | 152 | variant C |

- **Axes:** glTF **Y-up**, origin at **shard center**, long axis **+Z** (tip toward +Z).
- **Scale:** `(1,1,1)` world meters. Spawn 4–6 mixed variants.
- **Material (embedded):** baseColor RGBA (straight alpha, stained panes + dark lead) + emissive (soft glass glow + bright refracted rim). Approximates transmission for web — use `transparent: true`, `alphaTest` ~0.08 or alpha-hashed, `depthWrite: false` for overlapping shards, `emissiveIntensity` ~1.5–2.5.
- Source `.blend` files are in this folder for revision only (not runtime).

```js
// tip points +Z; orient shard.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1), dir)
shard.position.copy(pos);
```

## FX textures

| File | Layout | Blend | FPS / use |
|------|--------|-------|-----------|
| `heavens_shrapnel_trail.png` | 512×128 strip, tileable on U | **Additive** | ribbon behind shard; scroll U 1.5–3/s; length ~0.8–1.6 m; razor-thin |
| `heavens_shrapnel_trail_4x4.png` | 1024×256, 4×4 cells 256×64 | **Additive** | 12–16 FPS animated trail (optional) |
| `heavens_shrapnel_glint_sparkle.png` | 512×512, 4×4 cells 128×128 | **Additive** | 10–14 FPS cathedral 4-point gold/white glints on shard edges |
| `heavens_shrapnel_impact_burst_4x4.png` | 1024×1024, 4×4 cells 256×256 | **Additive** | 16–20 FPS one-shot: white-gold flash → colored glass burst → fade |
| `heavens_shrapnel_shatter_fragments.png` | 512×512, 4×4 atlas 128×128 | **Normal** (alpha) or Additive soft | spawn 8–16 tiny colored fragments at impact |
| `heavens_shrapnel_ground_glint.png` | 256×256 | **Additive** | tick-damage area decal; pulse opacity ~0.3–0.7 |

All FX PNGs: real alpha; RGB→0 where alpha→0 (no milky halos). Material `color: 0xffffff` — do not multiply by gray.

## Recommended sequence

| Phase | Time | Assets |
|-------|------|--------|
| Cast / release | 0–0.2s | optional glint on hand |
| Flight | until hit | 4–6 shards (mix a/b/c) arcing; each with trail strip + occasional glint |
| Impact flash | 0–0.15s | impact burst frames 0–3; spawn shatter fragments |
| Splash / shards out | 0.1–0.55s | impact mid frames + fragments outward 2–5 m/s |
| Tick zone | 0.4–2.0s+ | ground glint decal under impact; low tick DPS as locked |

### Trail placement
Attach a ribbon/beam from shard center toward **-flight direction** (behind the tip). Trail head at shard, fading tail opposite +Z tip. AdditiveBlending, depthWrite:false.

### Impact
1. Play `heavens_shrapnel_impact_burst_4x4.png` once at hit point, scale ~1.0→1.8.
2. Emit 8–16 quads from `heavens_shrapnel_shatter_fragments.png` (random cells), outward velocity, life 0.4–0.8s, tumble.
3. Place `heavens_shrapnel_ground_glint.png` on XZ at impact for tick-damage telegraph.

## Colors (approx linear 0–1)

- Crimson glass: `(0.72–0.85, 0.06–0.10, 0.08–0.12)`
- Cobalt glass: `(0.08–0.12, 0.18–0.22, 0.72–0.85)`
- Amber glass: `(0.78–0.90, 0.42–0.50, 0.05–0.08)`
- Lead came: `(0.04, 0.035, 0.032)`
- Trail / fire: gold `(1.00, 0.82, 0.28)` → white-hot `(1.00, 0.98, 0.92)`

## QA / keep-blacks
- Lead lines must stay near-black on `#050505`.
- Do not additive-blend the shard mesh itself in a way that lifts lead to gray — emissive is for panes/rims only.
- Smoke not used; this rite is glass + gold/white fire only.
