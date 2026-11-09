# Fireball FX — USAGE (Sanctuary / three.js)

Original procedural art, CC0. Mood reference: Diablo 2 Fireball (shape/feel only).
**Brian lock:** darker deep red-orange fire, hotter orange-yellow core, heavy black smoke, gothic, **KEEP BLACKS** (edges fade to rich black/alpha — never washed gray).

## Files

| File | Size | Frames / layout | Blend | Notes |
|------|------|-----------------|-------|-------|
| `fireball_core_flipbook.png` | 1024×1024 | 4×4 = 16 frames, 256×256 cells | **Additive** | Looping flaming ball with tongues |
| `fireball_trail_strip.png` | 512×128 | tileable on X | **Additive** | Streaky flame tail |
| `fireball_trail_flipbook.png` | 1024×256 | 4×2 = 8 frames, 256×128 cells | **Additive** | Animated trail (optional) |
| `fireball_explosion_flipbook.png` | 1024×1024 | 4×4 = 16 frames, 256×256 cells | **Additive** | Flash → bloom → char → clear |
| `fireball_shockwave_ring.png` | 512×512 | single ring | **Additive** | Scale ring mesh/sprite ~0.35s |
| `fireball_smoke_flipbook.png` | 1024×1024 | 4×4 = 16 frames, 256×256 cells | **Normal (transparent)** | Heavy charcoal — NOT additive |
| `fireball_sparks_embers.png` | 512×512 | 4×4 atlas, 128×128 cells | **Additive** | Streaks + ember dots |
| `fireball_windup_glow.png` | 256×256 | single | **Additive** | Hand charge glow |

All PNGs: real alpha, RGB premultiplied by alpha (no edge halos). Where alpha→0, RGB→0 (true black).

## Colors used (approx linear 0–1)

- Hot core: `(1.00, 0.95, 0.55)`
- Warm orange: `(1.00, 0.58, 0.10)`
- Mid deep red-orange: `(0.98, 0.28, 0.04)`
- Edge ember: `(0.55, 0.08, 0.015)`
- Smoke dark: `(0.055, 0.045, 0.040)` / mid charcoal `(0.14, 0.11, 0.09)` (hard-capped ≤0.22)

Do **not** multiply by a light gray tint in engine — keep blacks.

## Recommended playback

### Wind-up (hand)
- Sprite: `fireball_windup_glow.png` on hand/weapon tip bone
- Scale: 0.25 → 0.55 world units over ~0.35–0.5s
- Opacity: 0 → 1 → hold; optional ±8% scale pulse at ~6 Hz

### Flight (projectile)
- Core: `fireball_core_flipbook.png`, **16–20 FPS**, loop
- UV flipbook 4×4: `col = frame % 4`, `row = floor(frame/4)`; `repeat=(1/4,1/4)`, `offset=(col/4, 1-(row+1)/4)`
- Scale: ~0.55–0.75
- Trail: ribbon with `fireball_trail_strip.png` (scroll U 2–4/s) **or** trail flipbook 12–16 FPS
- Trail length ~1.2–2.0 m; AdditiveBlending, depthWrite:false

### Impact
1. Explosion — `fireball_explosion_flipbook.png`, **16–20 FPS**, one-shot, scale 1.2→2.2, life ~0.75–0.9s
2. Shockwave — `fireball_shockwave_ring.png` on XZ ring/quad; scale 0.4→2.5 over ~0.35s, fade alpha
3. Sparks — 12–24 particles from sparks atlas; outward 3–8 m/s, life 0.4–0.8s, additive
4. Smoke — `fireball_smoke_flipbook.png`, **10–12 FPS**, one-shot; **NormalBlending**; scale 1.0→2.5; life ~1.2–1.8s; material color `0xffffff` so dark RGB stays dark

## three.js sketch

```js
const fireMat = new THREE.SpriteMaterial({
  map: coreTex, blending: THREE.AdditiveBlending,
  depthWrite: false, transparent: true, color: 0xffffff,
});
const smokeMat = new THREE.SpriteMaterial({
  map: smokeTex, blending: THREE.NormalBlending,
  depthWrite: false, transparent: true, color: 0xffffff,
});
function setFrame(mat, frame, cols=4, rows=4) {
  const col = frame % cols, row = Math.floor(frame/cols)%rows;
  mat.map.repeat.set(1/cols, 1/rows);
  mat.map.offset.set(col/cols, 1 - (row+1)/rows);
}
```

## Sequence timing

| Phase | Time | Assets |
|-------|------|--------|
| Wind-up | 0.0–0.45s | windup glow |
| Flight | 0.45s–impact | core loop + trail + sparks |
| Impact flash | 0–0.15s | explosion 0–2 + shockwave start |
| Fire bloom | 0.15–0.55s | explosion mid + sparks burst |
| Smoke / char | 0.4–1.8s | smoke flipbook + residual embers |

## QA / keep-blacks
- Smoke and fire edges must read as rich black on `#050505`, not milky gray.
- No additive smoke. Bloom fire sheets only if needed — never smoke.
