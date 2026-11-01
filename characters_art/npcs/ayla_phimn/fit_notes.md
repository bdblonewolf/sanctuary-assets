# Ayla of the Phimn – outfit fit notes
Body: bodies_fit/ayla_phimn_body.glb. Custom MPFB2 build, 1.42 m (4'8"), petite proportions, same 52-bone mixamorig skeleton, grey-blue skin with a 2K red rune layer baked into the basecolor (stomach sigil, glyphs down both sides of the waist, shoulders, shoulder blades, spine, lower back). Dark linen briefs for decency. Source: work_ayla/ (ayla_build.py, runes.py, skin.py). No hair modelled (the sheet shows long black hair).
Race rule: Phimn = human in code, always grey-blue skin, always 1.42 m.
Combined GLB: npc_f_ayla_phimn_ayla_phimn_body.glb (2.1 MB). Separate pieces + body masks: pieces/ (see ../manifest.json).
Nodes: halter_top, halter_strings (tied behind the neck, knot + tie ends), charm_silver, charm_crystal (pale-blue emissive), belt, loincloth (front/back panels match, ±40°, 0.27 m, both use the plain panel texture), vambrace_L/R, boots (flat, no heel, mid-calf, laced in texture).
Stretch (Idle / Looking Around / Walking): everything ≤1.32 except the boots, at 3.1 on 8 micro-edges of 1–2 mm (the same voxel-remesh artifact as on the leather sets). Pokes: loincloth over the thighs during the walk stride (expected, it's loose cloth), crystal 3 frames, boots minor. Report: stretch_poke_ayla_phimn_body.json.
Gaps vs the sheet: the top is a fitted band with halter strings, not separate triangle cups; lacing is texture-only; the face is MPFB targets only (no sculpt pass); no hair.

## Pass 3 (Oct 31 2026)
- Body copy (bodies_fit/ayla_phimn_body.glb) slimmed: waist -12%, legs +7%, arms +6% to match the sheet silhouette (see previews/ayla_phimn_overlay.jpg).
- Loincloth split into 4 overlapping halves (front/back x L/R), each weighted to its own thigh: walk stretch 1.96, max 3 poked verts (was 14).
- New separate hair piece pieces/npc_f_ayla_hair.glb (slot head/hair): 180 alpha strand cards with bangs; minor shoulder poke (~11 verts) on walk.
- Boots: 25 sole/heel body verts flagged under the ground plane only (masked).

## 15:04 rebuild (EDT)
- Body (bodies_fit copy only): pear-hourglass. Narrow, sloped shoulders, smaller bust, fuller hips and thighs, waist -12%. All linen undergarment polys are now skin, so the dark hip, thigh and chest patches are gone.
- Skin: slate grey-blue with pores, a normal map, roughness variation and AO-darkened creases. Red runes: stomach sigil, waist and rib rows, upper arms and shoulders, shoulder blades, spine.
- Halter top: worn pale leather, sweetheart cups resampled per column (clean curved edges) with crossed lacing down the centre gap. Cup straps run up into halter strings over the neck, knotted behind it. Back band ties.
- Charm: a short silver chain from the top's centre to a bail, 4-point star, ring and emissive pale-blue crystal. The stray silver spikes were hair cards crossing the chest; fixed in hair.py.
- Hair: 4 layers of strand cards, temple strands stop at the hairline, bangs to the brow.
- Anim (Idle, Looking Around, Walking): max stretch 2.04 (loincloth), hair 2.20. All under 2.5. See stretch_poke_ayla_phimn_body.json.

## 15:13 rebuild (3:04 PM review pass)
- Skin: slate (sRGB ~0.36/0.38/0.44) and subtle texture; dark-red continuous stave runes on stomach, arms, thighs and back.
- Hair: long, straight and glossy black, with a centre part framing the face. Bangs were removed because they rendered as dark streaks across the eyes.
- Top: smaller and laced, with the bust reduced (slim pull 0.55). Loincloth: wider (±50°), ragged and woven, mid-thigh. Panel offset raised to 30/33 mm.
- Belt: brown-tan, studded, with a buckle. The hip gaussian was moved, so no hand poke shows. Vambraces and boots are studded and stitched, with a dark sole.
- Anim (Idle, Looking Around, Walking): stretch max 2.14 on the loincloth and 2.15 on the hair, all ≤2.5. Remaining pokes are covered by the per-piece masks: belt 4 verts on the belly, loincloth 11 verts on the walking thigh, boots 13.

## 15:2x Brian fixes
- Halter top is shrinkwrapped onto the current pear-hourglass body at +2.5 mm, so there is no sag or gap. Stretch is 2.36.
- Loincloth is back to the first style: skinny ±13° front and back flaps with ragged ends, held by a thin cord belt in place of the buckled belt. The node name stays npc_f_ayla_belt.
- Poke test now excludes arm and hand verts from the belt and chest coverage, which were false hits from the hanging hands.
- Results: belt 68 frames / 2 verts, boots 6/13, strings 20/1, everything else 0. All stretch is ≤2.36.
