# Arc Whip — USAGE (Sanctuary / three.js)

Internal rite id: `arc_whip`. Original / Mesh2Motion CC0 composition. Mood reference: Diablo 2 lightning skills (feel only).
**Brian lock:** hip-swing like a real whip (Cast Speed %), small arc in front, light-blue lightning snake-lasso that tracks enemies. **KEEP BLACKS** (dark leather handle, dark backgrounds — never wash to gray).

## Files

| File | Kind | Notes |
|------|------|-------|
| `arc_whip_swing.glb` | clip | `arc_whip_swing`, 1.0 s, 30 fps, in-place, crack @ **frame 16 / 0.55 s** |
| `arc_whip_swing_male.glb` | clip | byte-identical; same mixamorig names bind to male variants |
| `arc_whip_swing_female.glb` | clip | byte-identical; same mixamorig names bind to female variants |
| `arc_whip_lightning_whip.glb` | mesh | extended lightning whip (runtime primary) |
| `arc_whip_extended.glb` | mesh | alias of extended |
| `arc_whip_idle.glb` | mesh | coiled idle / slack pose |
| `arc_whip_arc_trail.png` | FX strip 512×128 | curved swoosh; **Additive** (v1) |
| `arc_whip_arc_trail_4x4.png` | FX 4×4 / 1024 | animated arc trail; **Additive** (v1) |
| `arc_whip_arc_trail_v2.png` | FX strip 512×128 | **prefer** — saturated cyan→white core, crisp edge, no grey haze; **Additive** |
| `arc_whip_arc_trail_4x4_v2.png` | FX 4×4 / 1024 | **prefer** — animated trail v2; **Additive**, 16–20 FPS |
| `arc_whip_crack_flash_4x4.png` | FX 4×4 / 1024 | crack flash v1 (softer / bigger blob) |
| `arc_whip_crack_flash_4x4_v2.png` | FX 4×4 / 1024 | tight flash v2 (softer forks than v3) |
| `arc_whip_crack_flash_4x4_v3.png` | FX 4×4 / 1024 | **prefer** — v2 blue ring/halo + long chaotic sharp zig-zag white radial forks; peak @ frame 0; **Additive** one-shot |
| `arc_whip_snake_lasso_strip.png` | FX strip 512×64 | tileable ribbon v1 (smooth); **Additive** |
| `arc_whip_snake_lasso_4x4.png` | FX 4×4 / 1024 | lasso loop v1; **Additive** |
| `arc_whip_snake_lasso_strip_v3.png` | FX strip 512×64 | **prefer** — chaotic zig-zag white core + cyan glow; tileable; **Additive** |
| `arc_whip_snake_lasso_4x4_v3.png` | FX 4×4 / 1024 | **prefer** — re-seeded jagged crawl; **Additive**, 16–20 FPS |
| `arc_whip_sparks_4x4.png` | FX 4×4 / 512 | sparks v1 |
| `arc_whip_sparks_4x4_v3.png` | FX 4×4 / 512 | **prefer** — jagged micro-fork sparks; **Additive** |
| `clip_meta.json` / `mesh_meta.json` | meta | machine-readable attach + crack frame |
| `validation.json` | QA | sizes, tris, bounds, crack frame |
| `previews/` | PNG/GIF | prefer `effect_sequence_v3.png`, `effect_crack_hero_v3.png`, `effect_swing_v3.gif` |

All PNGs: real alpha; where alpha→0, RGB→0 (no milky halos). Do not multiply materials by gray tints.

### FX v2 / v3 (Brian fine-tune)
- **Arc trail v2 (keep):** saturated light-blue→white trail, crisp edge, no grey haze. Blue is good — leave as preferred trail.
- **Crack flash v3 (prefer):** same tight blue ring/halo as v2, but white forks are long chaotic sharp zig-zags (midpoint-displacement) with secondary/tertiary branches. Peak @ **frame 0**.
- **Snake lasso v3 (prefer):** jagged zig-zag white core (not smooth sine), cyan glow behind; 4×4 re-seeded to crawl/flicker.
- **Sparks v3 (prefer):** jagged micro-forks.
- Preview ribbon white core (v3): 2–3 re-seeded zig-zag layers per frame over the kept v2 blue glow.
- Older versions kept for rollback.

## Clip — `arc_whip_swing`

- **Source:** Mesh2Motion CC0 `m2m_one_hand_slash_combo` (first slash window), retimed to a whip crack. Hip/spine/shoulder motion gently amplified. **Hand / finger / wrist quaternion values are NOT edited** (time-resampled only).
- **Skeleton:** mixamorig joints cloned from `m2m_human_anims_mixamo.glb` (same 27 skin joints as hero / `knight_anim_v10b_clips.glb`).
- **Duration:** 1.0 s @ 30 fps (31 keys, 0…1.0 inclusive).
- **Crack frame:** **16** (t = **0.55 s**) — fire damage / lasso attach / crack flash here.
- **In-place:** hips XZ translation locked (no root motion).
- **Windup:** 0.00–0.55 s (ease-in back-hip / shoulder).
- **Recover:** 0.55–1.00 s (ease-out to stance).
- **Male / female:** use the same clip; joint names match `anim_variant_male` / `anim_variant_female` / `hero_anims_m2m_m` / `hero_anims_m2m_f`.

```js
// Playback sketch (Cast Speed % scales timeScale)
actions.arc_whip_swing.reset().setEffectiveTimeScale(castSpeed).play();
// at mixer.time === crackTime / castSpeed → spawn crack FX + start lasso
```

## Mesh — lightning whip

- **Origin:** grip / right-hand attach (butt of dark leather handle).
- **Axis:** Y-up meters; whip extends along **+Z** (~3.30 m tip).
- **Handle:** ~0.30 m dark braided leather (non-emissive, keep blacks).
- **Body:** segmented light-blue lightning ribbon + pale cyan/white emissive core; tapers to crack tip.
- **Tris:** 957 (extended) / 1045 (idle) — under 3k budget.
- **Attach bone:** `mixamorig:RightHand`
- **Suggested offset (m):** `[0.0, -0.02, 0.04]`
- **Suggested euler (deg):** `[90, 0, 0]` then fine-tune so local +Z aims along the hand’s forward/grip axis.
- **Idle:** swap to `arc_whip_idle.glb` (coiled) when not casting, or hide mesh and rely on FX ribbon only.

## FX — colors & blend

| Asset | Blend | Color feel |
|-------|-------|------------|
| arc trail / crack / lasso / sparks | **AdditiveBlending**, depthWrite:false | pale cyan `(0.85,0.95,1)` core, light-blue `(0.45,0.85,1)` glow |
| leather handle | opaque PBR | `(0.04, 0.025, 0.018)` — do not lift |

Flipbook UV helper (4×4):

```js
function setFrame(mat, frame, cols=4, rows=4) {
  const col = frame % cols, row = Math.floor(frame / cols) % rows;
  mat.map.repeat.set(1/cols, 1/rows);
  mat.map.offset.set(col/cols, 1 - (row+1)/rows);
}
```

## Driving the snake-lasso (three.js)

The lasso is a **ribbon / CatmullRom curve** from the right hand (or whip tip) to the tracked enemy, textured with the tileable strip (scroll U) or the 4×4 crackle flipbook.

```js
// Pseudocode
const curve = new THREE.CatmullRomCurve3([
  handWorldPos,
  handWorldPos.clone().lerp(targetWorldPos, 0.35).add(sideOffset),
  targetWorldPos,
]);
const ribbonGeo = new THREE.TubeGeometry(curve, 32, 0.03, 5, false);
// or THREE.Mesh with a custom RibbonBufferGeometry spanning hand→target
const mat = new THREE.MeshBasicMaterial({
  map: lassoStripTex, // wrapS = RepeatWrapping; offset.x -= dt * 4
  blending: THREE.AdditiveBlending,
  transparent: true, depthWrite: false, color: 0xffffff,
});
// On crack frame: play crack_flash_4x4 one-shot at tip; spray sparks_4x4
// Arc trail: billboard/swoosh along the swing arc for ~0.25–0.4s
```

### Timing (Cast Speed 100%)

| Phase | Time | Assets |
|-------|------|--------|
| Windup | 0.00–0.55 s | clip windup; optional faint hand glow |
| Crack | **0.55 s** | prefer `crack_flash_4x4_v3` (frame 0 peak) + `sparks_4x4_v3`; start lasso to target |
| Arc trail | 0.45–0.85 s | prefer `arc_trail_v2` strip / `arc_trail_4x4_v2`; lasso prefer `snake_lasso_*_v3` |
| Lasso track | 0.55 s → hit end | `snake_lasso_strip` scroll or 4×4 loop |
| Recover | 0.55–1.00 s | clip recover; fade trail |

## QA / keep-blacks
- Handle and preview backgrounds must stay rich black/dark brown — never milky gray.
- Additive FX: material `color = 0xffffff`; let the PNG carry the cyan.
- Do not replace this with a procedural red/blue line stand-in when these assets are available.
