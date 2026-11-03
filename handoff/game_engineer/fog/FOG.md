# Ground haze per zone (cheap height fog)

Files: `fog_zones.json` (data), `wisp_512.png` (512², tileable, greyscale + alpha, for the optional High-only wisp planes).
Nothing else changed. The existing scene distance fog (`Fog(0x07080C, 16, 46)`) stays as it is; this haze is an extra, very
thin, light grey-blue layer that only lives in the first 1–2 m above the ground.

## Look
- Thin and transparent. `density` is the **maximum** blend at ground level at full view distance (0.025 town … 0.22 mires);
  everything is clamped by `model.max_alpha = 0.35`. It should read as damp air on the ground, never as a white-out.
- Darkness-preserving: the colours are light grey-blue but the blend is tiny, and `night_mul 0.8` lowers it at night so
  the haze never lifts the blacks. If it ever looks milky at night, reduce density, do not darken the colour.
- Thickest: **mires**, the **cemetery** pocket in Martsirt, **briarE**. Then sink, coast, flotsam, wild, isle, bluffs.
  Nearly none: Martsirt (town), Qadren (lut), desert. Interiors and caves: none.

## Keys
Zone keys are the live area ids (`world.id`, from the area-level map / name map in `routes-DYqsoIet.js`): town, lut, market,
bastion, wild, briarE, weald, coast, flotsam, isle, bluffs, mires, sink, duneW, desert, waste, ridge, ascent, iron.
Interior/cave ids (cottage, taproom, inn, house, nave, sewer, church1/2, castle1–4, vault, den, root, crypts, chasm, hollow,
gaol, hull, undercroft) are `{"inherit":"interior"}` → density 0. Any id not listed uses `default`.
Note `sink` is in the code's cave set but gets a low foul vapour on purpose.

Cemetery is a **sub-zone of `town`**: rect centred on the graveyard placement (48, −12), 24 × 18 m, rotY 0.1047, with an 8 m
feather. Blend `density`/`color` from town → cemetery by `1 - smoothstep(0, feather, distanceOutsideRect)` (per fragment from
world XZ is cheapest; or per frame from the player position if a single uniform is wanted).

## Engine model (no depth pass)
Patch `fog_fragment` with `onBeforeCompile` on the shared materials (or a small ShaderChunk override). Needs world position
in the fragment (`vWorldPos`, add it in `worldpos_vertex`).

```glsl
uniform vec3  uHazeColor;   // zone.color (linear)
uniform float uHazeDensity; // zone.density * weatherMul * (night ? night_mul : 1)
uniform float uHazeBase, uHazeTop, uHazeFall, uHazeRange; // height.base/top/falloff_exp, model.range_m
// ... after the stock fog:
float h = pow(clamp((uHazeTop - vWorldPos.y) / (uHazeTop - uHazeBase), 0.0, 1.0), uHazeFall);
float d = 1.0 - exp(-length(vWorldPos - cameraPosition) / uHazeRange);
float a = min(uHazeDensity * h * d, 0.35);
gl_FragColor.rgb = mix(gl_FragColor.rgb, uHazeColor, a);
```
Cost: a handful of ALU per fragment, no extra pass, no extra target. Mobile-safe. Skip it entirely when density == 0
(interiors) via a define. On zone change, lerp the uniforms over `transition_s` (2.5 s).
`weatherMul = 1 + 1.5·clamp(game.fog, 0, 1)` hooks the existing weather fog value.

## Wisps (High quality only)
`wisps.enabled_on_high` → spawn `count` horizontal planes (`plane_size_m`, at `y_m` above ground) around the camera target,
`MeshBasicMaterial({ map: wisp_512, transparent: true, depthWrite: false, opacity: wisps.density, color: zone.color })`,
scroll the UV offset at `drift_speed_mps / plane_size_m` along `drift_dir_deg`, and fade each plane's opacity in/out over its
life so the repetition is not visible. `castShadow/receiveShadow = false`, `renderOrder` after opaque. Off on Low/Medium.
The PNG is luminance 200–240 with soft alpha (peak ≈ 0.7, about 30 % empty) so it tints rather than whitens.
