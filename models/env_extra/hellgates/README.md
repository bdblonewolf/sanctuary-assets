# Sanctuary — Hell Gates (upgrade of the stone-plate gates)

Three drop-in GLB props: graveyard entrances where you go down creepy steps into the Hell-only areas.
Plain glTF 2.0 GLB: no Draco, no meshopt, **no extensions** (KHR_* none), no lights, no cameras.
1 unit = 1 m, +Y up (exported from Blender Z-up). Origin = centre of the surface footprint, at ground level (Y=0).
Embedded PBR: baseColor (JPEG, sRGB, multiplied by COLOR_0 grime), normal, metallicRoughness (ORM-packed: G=rough, B=metal), 512–1024 px.
Textures: Poly Haven CC0 scans (mossy_stone_wall, castle_wall_slates, rock_pitted_mossy, mossy_cobblestone, rusty_metal_02, brown_mud_leaves_01, old_stone_wall, rock_wall_08), graded dark/desaturated.
Statues: CC0 "gothic_statue" (Poly Haven, Benny Weimer), decimated; the four draft statues in sanctuary/assets3d/statues were not used.

| file | footprint (surface, 2 m grid) | depth | size | tris | verts | validator |
|---|---|---|---|---|---|---|
| hellgate_crypt_a.glb | 6 × 8 m (x ±3, z ±4) | stair to −3.0 m, tunnel to −3.1 | 3.69 MB | 35.3k | 40.2k | 0 errors, 0 ext |
| hellgate_monolith_b.glb | 8 × 8 m (x ±4, z ±4) | spiral to −3.8 m | 3.59 MB | 27.7k | 31.3k | 0 errors, 0 ext |
| hellgate_mausoleum_c.glb | 6 × 8 m (x ±3, z ±4) | stair to −2.85 m; bottom door/tunnel goes ~0.5 m past +Z edge underground | 3.53 MB | 32.1k | 36.9k | 0 errors, 0 ext |

Only warnings: MESH_PRIMITIVE_GENERATED_TANGENT_SPACE (three.js computes tangents itself; fine).
Steps: A rise 0.1875 / tread 0.28 (16 risers); B 18 wedge steps × 18°, rise 0.20; C rise 0.19 / tread 0.28 (15 risers). Doorways ≥ 2.0 m clear (hero 1.8 m).
Entrance faces −Z in glTF (Blender −Y) for A and C; B's spiral starts on the −Z side.

## Node conventions (same in all three; suffix _a / _b / _c)
- **Meshes** grouped by part (stairs, pit_wall_l, iron, monoliths, maus_roof, statue_*, ground…). `ground` is a ragged dirt apron with a hole; it blends into your terrain.
- `fx_void_*` — black unlit-ish quad(s) at the bottom doorway (material hg_void). Keep as pure black / add depth-fade.
- `fx_fog_*` — alpha-blended quads (hg_fog, radial alpha texture). Animate UV/opacity, or replace with your fog sprite system. Set `depthWrite=false`.
- `fx_glow_hell_*` — red emissive alpha quad at the stair bottom (hg_glow; emissive factor ≈ (1,.09,.02), strength 1 since no KHR_emissive_strength). Put a PointLight (red, low intensity, ~4 m range) here at runtime and pulse it.
- `fx_embers_rise_*` — empties (arrow up): spawn rising ember particles.
- `fx_candle_*` — empties at each wick tip: flame sprite + tiny flicker light (optional).
- `fx_crow_perch_*` — empties for crows (fence finials, wings/monolith tops, ridge).
- B only: `runes` mesh uses hg_ember (dim red emissive) — pulse emissiveIntensity for a breathing glow.
- `col_*` — empties, display CUBE; **scale = half extents**, position = box centre, rotation as given. Use as box colliders, then hide.
- `trigger_hellgate` — same cube convention; at the top of the stairs / the doorway. Fire the Hell-gate interaction (load area / portalTap) on enter.
- `ground_hole_*` — empty describing the opening to cut in the terrain: A/C a CUBE (scale = half extents x/z), B a SPHERE (radius = scale.x = 2.32 m). If your ground is a flat plane, cut/hide terrain inside this region or the pit is covered.

## Findings about the existing gates (live build sanctuary/live_s8e/routes-*.js + docs)
- There is no dedicated "hellgate" object. The "stone plates" are the 2D-drawn props `{kind:'arch', style:'sealed', label:'SEALED'}` (e.g. nave map x 13.2/15.4, y 3.15): drawn by `qd()` as two flat stone blocks `dd(... 0.7×0.7, h 78, #5c584e/#524e46)` with iron bars; message "The doors are massive, and sealed from the other side...".
- Related: `{kind:'stairs', style:'deep', label:'DEEPER'}` in the sewer ("A second stair delves deeper… locked, for now"); other stairs styles hatch/ladder/trap; hit-test via portalTap. In 3D, arch/stairs props only get torch markers at y≈0.55.
- Lore/docs: killing Nightmare Ysmer opens The Margins (Hell-only portal at Quill's lectern, quest margins1); Margins areas (Tide-Clock 121 … Last Page 185) open only on Hell difficulty.
- Placement: props use tile coords (x, y) where game y = 3D z. To swap: at each sealed arch / DEEPER stairs prop, instance one of these GLBs at (x, 0, y), rotate so −Z faces the walkway, scale 1, add colliders from col_*, and wire trigger_hellgate to the existing portal/lock logic (show "sealed" message until Hell is unlocked). Footprints are 2 m-grid snapped, so they fit the tile grid when the prop centre is on an even metre.

## Renders
renders/{a,b,c}_iso_front.png, *_iso_back.png (night, ~35° iso, opposite sides), *_cutaway.png (section showing stairs to the void). Combined: hellgate_preview_sheet.jpg (renders/ and src/ not in this repo).
Render-only helpers (larger terrain plane, moon, red pit lights, candle lights) are not exported.

## Rebuild
`blender -b -P src/build_a.py -- 32` (same for b/c; last arg = Cycles samples). src/dl.py fetches CC0 sources, src/prep_tex.py builds tex/, src/hg.py = geometry/material helpers, src/rx.py = export/render.

## Known compromises
- Underground outer faces of pit walls are plain (hidden by terrain); you need to cut the terrain using ground_hole_*.
- Glow/fog are simple alpha quads, meant to be driven by your FX code; no baked lightmaps/AO beyond vertex-colour grime.
- Statues are one CC0 sculpt (veiled/crowned robed figure) reused: A as the "weeping angel" with added stone wings, C as the two hooded mourners. Not a true weeping angel pose.
- B's cutaway reads the pit/door/column but the spiral steps are hard to see in it; the iso renders show the spiral.
- Fixed 3 seeds; textures at 512–1024 to stay under 4 MB.
