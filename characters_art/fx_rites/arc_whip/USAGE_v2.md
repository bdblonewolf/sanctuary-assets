# Arc Whip v2 — travelling lightning projectile

Add-only. Does **not** replace the pushed v1 pack in `characters_art/fx_rites/arc_whip/`.
Internal rite id: `arcwhip` / `arc_whip`. Original art, CC0. Mood reference: Diablo 2 lightning (feel only).

**Brian lock (v2):** the hip-swing clip is a whip motion, but the **skill itself leaves the tip of the weapon** as a **long zig-zag lightning projectile**. It must launch on the release / crack frame. It must **detach** — no latching, no tether, no snake-lasso that stays stuck to the hand after the cast. The in-hand whip mesh only flashes during the swing, then hides.

**Look:** real chaotic lightning — sharp zig-zags and branching forks, never smooth glowing curves. Approved light-blue. **Balance sharp and soft:** crisp white core + soft cyan glow. **KEEP BLACKS** (true-black alpha edges; never wash to gray).

**Runtime: NOT TESTED.** This pack was not played in the game or in three.js. Only `node --check` was run on the JS.

## Clip (already pushed — reuse, do not overwrite)

| Item | Value |
|------|--------|
| Files | `characters_art/fx_rites/arc_whip/arc_whip_swing.glb` (plus `_male` / `_female` byte-identical copies) |
| Clip name | `arc_whip_swing` |
| Duration / fps | 1.0 s @ 30 fps (31 keys) |
| **Release / crack frame** | **16** (t = **0.55 s**) — from `clip_meta.json` |
| Attach bone | `mixamorig:RightHand` |
| Whip-tip socket | local +Z from the grip, **~3.30 m** (`mesh_meta.json` `total_reach_approx_m`) |
| In-hand mesh | `arc_whip_lightning_whip.glb` — visible during the swing flash only, then **hide** |

Source of the release frame: `/workspace/sanctuary_art/handoff/from_art_bot/rites/arc_whip/clip_meta.json` and the pushed copy at `characters_art/fx_rites/arc_whip/clip_meta.json` (`crack_frame`: 16, `crack_time_s`: 0.55).

## New v2 textures (this folder)

All PNGs: 4×4, 256 px cells, 1024×1024, premultiplied alpha, RGB = 0 where alpha = 0, **Additive**, 16 fps. Material `color: 0xffffff`.

| File | Use |
|------|-----|
| `arc_whip_bolt_4x4_v2.png` | Looping travelling bolt (re-randomized jagged forks each frame). Every frame: one long forward zig-zag running LEFT->RIGHT across the cell, head (brightest, thickest) at the RIGHT, forks angle forward. No hooks, U shapes, loops or lashes; 22 px safe margin so nothing is cropped |
| `arc_whip_bolt_trail_4x4_v2.png` | Short fading zig-zag trail segments behind the bolt (same forward left->right axis, thinner) |
| `arc_whip_impact_fork_4x4_v2.png` | One-shot radial fork burst, peak at frame 0, on hit **or** at max range |

### Polish 2026-11-10
The bolt, trail and impact sheets were regenerated so no frame curls into a hook, U, loop or lash (the earlier sheet had several). Frame layout is unchanged: 4x4, 16 frames, 16 fps, row-major from top-left, bolt flies tip-right in the cell (quad local +X = flight direction). No JS changes were needed for frame assumptions.

## Projectile numbers

| Param | Value | Notes |
|-------|--------|--------|
| Speed | **18 m/s** | Fast enough to read as lightning, still visible as a projectile |
| Range | **10 m** | Flight time ≈ 0.56 s at default speed (Cast Speed % should scale speed, not the clip release frame) |
| Trail | 7 segments, 0.28 m spacing, life ~0.22 s | Fades; not a hand tether |
| Bolt quad | 2.0 × 0.55 m | Billboard / flight-aligned quad |
| Impact | 1.35 m one-shot, 16 fps, ~1.0 s | Then gone |
| Wander | ±0.12 m lateral | Visual zig only — **does not home or latch** |

## JS module

`arc_whip_projectile_v2.js`

```js
const fx = ArcWhipProjectileV2.create(THREE, scene, {
  bolt: boltTex, trail: trailTex, impact: impactTex,
}, {
  getWeaponTipWorld: (out) => { /* world pos of whip tip at release */ },
  getForward: (out) => { /* xz facing */ },
  getWhipMesh: () => whipMesh, // flashed then hidden
  onHit: (pos, target) => {},
});
// when arc_whip_swing starts:
fx.playCast();
// per frame:
fx.update(dt, { clipTime: mixer.time, targets: foes });
```

`playCast()` watches clip time and **spawns once** at the tip socket when `clipTime >= 0.55`. After `0.55 + 0.08` s the whip mesh is hidden. The bolt is then a free world-space projectile.

## Previews (not runtime)

- `previews/contact_arc_whip_bolt_4x4_v2.png`
- `previews/contact_arc_whip_bolt_trail_4x4_v2.png`
- `previews/contact_arc_whip_impact_fork_4x4_v2.png`
- `previews/arc_whip_bolt_travel_v2.gif` — bolt travelling with a fading trail (composited on black; 16 fps)

## QA

Flipbook rims: no RGB where alpha is 0 (checked at generate time). Keep blacks. Do not parent the flying bolt to the hand after release.

