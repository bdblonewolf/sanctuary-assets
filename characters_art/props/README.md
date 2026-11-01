# Sanctuary props: CC0 museum and Poly Haven sources, restyled

Pipeline: `src/build.sh cfg/<name>.json` runs bake.py (Blender 4.2.3: chips, pits, cracks, dents, gouges on a hi mesh, then decimate the low mesh, xatlas UVs, and bake normal, AO, cavity and source detail from hi to low) → tex.py (de-lit repaint: only the high-pass log-luminance of the source survives; base colour comes from our own palettes plus crevice dirt, stains, dust, rust, worn edges, scratches and splashes) → export.py (GLB, embedded JPEG q85, Y-up, origin at the base centre, plus one `col_*` collider) → fixtan.py → gltf-validator.
All GLBs are plain glTF 2.0 with no extensions, 1 unit = 1 m. Textures are base colour plus normal at 2048² (kylix 1024²) and ORM at half resolution.
Previews are in `previews/<asset>_{front,iso,close}.png`, rendered under a dim blue-grey ambient light plus a warm candle key.
The sources are used only as reference: every albedo is repainted, and museum labels, numbers, mounts and baked scan lighting are not carried over.

| Asset | File | Tris (visual + collider) | Size W×H×D (m) | MB | Validator |
|---|---|---|---|---|---|
| Gothic statue | polyhaven/gothic_statue_sanctuary.glb | 27,707 + 12 (box) | 1.48 × 1.74 × 1.56 | 3.02 | 0 errors, 0 warnings |
| Kite shield | polyhaven/kite_shield_sanctuary.glb | 9,499 + 12 (box) | 0.54 × 1.39 × 0.14 | 2.04 | 0 errors, 0 warnings |
| Large castle door | polyhaven/large_castle_door_sanctuary.glb | 10,999 + 12 (box) | 2.01 × 2.97 × 0.30 | 2.15 | 0 errors, 0 warnings |
| Wine barrel | polyhaven/wine_barrel_01_sanctuary.glb | 6,500 + 44 (12-side cylinder) | 0.74 × 0.87 × 0.76 | 1.58 | 0 errors, 0 warnings |
| Kneeling winged monster (demonic pillar) | museum/kneeling_winged_monster_sanctuary.glb | 23,998 + 12 (box) | 0.49 × 0.87 × 0.41 | 2.13 | 0 errors, 0 warnings |
| ↳ statue-scale variant | museum/kneeling_winged_monster_sanctuary_statue.glb | 23,998 + 12 (box) | 1.13 × 2.00 × 0.94 | 2.13 | 0 errors, 0 warnings |
| Kylix (cup) | museum/kylix_sanctuary.glb | 6,000 + 44 (12-side cylinder) | 0.22 × 0.07 × 0.18 | 0.49 | 0 errors, 0 warnings |
| Egyptian false door (Qadren tomb wall) | museum/false_door_sanctuary.glb | 10,734 + 12 (box) | 1.16 × 1.55 × 0.12 | 1.87 | 0 errors, 0 warnings |
| Goddess Sekhmet (idol, real scale) | museum/sekhmet_sanctuary.glb | 20,000 + 12 (box) | 0.033 × 0.086 × 0.039 | 1.80 | 0 errors, 0 warnings |
| ↳ shrine-idol statue variant | museum/sekhmet_sanctuary_statue.glb | 20,000 + 12 (box) | 0.77 × 2.00 × 0.91 | 1.80 | 0 errors, 0 warnings |

## Per-prop sources and licences

### gothic_statue_sanctuary
- Source: https://polyhaven.com/a/gothic_statue. Author: Benny Weimer (Poly Haven).
- Licence: CC0 (https://polyhaven.com/license). Credit "Poly Haven / Benny Weimer" as a courtesy.
- Restyle: repainted as soot-darkened grey stone instead of the source's bronze look. Added edge chips, cracks, pitting, grime at the foot and dust on top. No decimation was needed (source 27.7k tris); normals were baked from a subdivided, displaced hi mesh.

### kite_shield_sanctuary
- Source: https://polyhaven.com/a/kite_shield. Author: Ulan Cabanilla (Poly Haven).
- Licence: CC0. Credit "Poly Haven / Ulan Cabanilla" as a courtesy.
- Restyle: dark oak with a faded bone-and-blood-red heraldic field, heavily worn. Added dents, sword gouges and scratches (battle scars), plus rusted iron trim and dark splashes.

### large_castle_door_sanctuary
- Source: https://polyhaven.com/a/large_castle_door. Author: Tina (Poly Haven).
- Licence: CC0. Credit "Poly Haven / Tina" as a courtesy.
- Restyle: grimy dark oak and black iron. Added dents, axe gouges, scratches, rot near the foot and splashes. Origin is at the bottom centre of the frame.

### wine_barrel_01_sanctuary
- Source: https://polyhaven.com/a/wine_barrel_01. Author: James Ray Cock (Poly Haven).
- Licence: CC0. Credit "Poly Haven / James Ray Cock" as a courtesy.
- Restyle: dark stained oak with rusted hoops, dents, chips, cracks and floor grime.

### kneeling_winged_monster_sanctuary (+ _statue)
- Source: Smithsonian National Museum of Asian Art F1916.345, "Kneeling winged monster", China, Northern Qi dynasty, 550–577, gift of Charles Lang Freer.
  - 3D: https://3d-api.si.edu/voyager/3d_package:0dc68216-3651-44c7-99cf-18e5d4d1eb9f
  - Record: https://asia.si.edu/object/F1916.345/
  - EDAN id: ld1-1643390182193-1643390189497-0
- Licence: CC0, verified through api.si.edu Open Access (metadata_usage.access = CC0; the 3d_package media usage.access = CC0). Credit "Smithsonian National Museum of Asian Art" as a courtesy.
- Raw: the Download3D GLB "150k-4096" (mm). No labels or numbers were visible in the texture atlas; the albedo is fully repainted in any case.
- Restyle: dark soot-stained limestone with chips, cracks, pitting, crevice grime and foot dirt. Used as a demonic pillar statue. The `_statue` variant is uniformly scaled to 2.0 m tall.

### kylix_sanctuary
- Source: Cooper Hewitt, Smithsonian Design Museum 1971-48-12, "Kylix", Greece, ca. 800 BC, painted earthenware, gift of Ruth Vollmer.
  - 3D: https://3d-api.si.edu/voyager/3d_package:547c78d1-620b-40c4-982e-01928870fef4
  - EDAN id: ld1-1643399887910-1643399942523-0
- Licence: CC0, verified through api.si.edu (objectRights = CC0; the 3d_package usage.access = CC0). Credit "Cooper Hewitt, Smithsonian Design Museum" as a courtesy.
- Raw: the "150k-4096-high" Web3D GLB (Draco; there is no Download3D GLB for this package). Mm units, converted to m.
- Restyle: grimy dark earthenware with soot-black geometric paint (repainted from a hue/saturation mask), chips, rim wear and dust.

### false_door_sanctuary
- Source: Minneapolis Institute of Art (Mia) 52.22, "False door", Ancient Egyptian, about 2400 BCE, limestone, 154.9 × 115.8 × 11.4 cm. The Christina N. and Swan J. Turnblad Memorial Fund.
  - Mia record: https://collections.artsmia.org/art/1230/false-door-ancient-egyptian (rights: Public Domain)
  - Original 3D: Mia on Sketchfab, https://sketchfab.com/3d-models/ffe4b699e75849d59d8efe47d3538f03
  - Obtained via the Artheon Museum mirror (approved by Brian): https://www.artheonmuseum.org/artwork/egyptian-false-door-about-2400-bce-ffe4b6, GLB https://images.artheonmuseum.org/ugc/sketchfab/ffe4b699e75849d59d8efe47d3538f03.glb (HEAD 200, model/gltf-binary, 5,391,588 B)
- Licence: CC0 1.0. Verified on the Artheon page (license "cc0", creativecommons.org/publicdomain/zero/1.0, "Minneapolis Institute of Art (CC0)") and in the GLB asset.extras (license "CC0-1.0", author "Minneapolis Institute of Art"). The Mia record says Public Domain. Credit "Minneapolis Institute of Art (Mia), via the Artheon Museum mirror" as a courtesy.
- Check: the internal texture name 180108_mia348_001230 carries the Mia object id 1230. The proportions match the record (scaled ×0.8534 to 1.549 m tall), and the relief matches Mia's photo.
- Restyle: a Qadren tomb-wall piece at real scale. Repainted as soot-darkened, grimy limestone with no scan lighting. Added edge chips, fine cracks, pitting, impact dents, crevice grime, dark splashes and foot dirt. The carved relief is kept from the baked normals. Decimated 65k → 10.7k tris. No labels or numbers were found on the source.

### sekhmet_sanctuary (+ _statue)
- Source: Minneapolis Institute of Art (Mia) 16.51, "Goddess Sekhmet", Ancient Egyptian, 1320–656 BCE, glazed faience, 8.57 × 3.33 cm. The William Hood Dunwoody Fund.
  - Mia record: https://collections.artsmia.org/art/101/goddess-sekhmet-ancient-egyptian (rights: Public Domain; Mia has no photo online, so it was checked against the Artheon thumbnail)
  - Original 3D: Mia on Sketchfab, https://sketchfab.com/3d-models/160b5a18fa994fcdb4bef96e5c1f1c4a
  - Obtained via the Artheon Museum mirror (approved by Brian): https://www.artheonmuseum.org/artwork/goddess-sekhmet-1320-656-bce-160b5a, GLB https://images.artheonmuseum.org/ugc/sketchfab/160b5a18fa994fcdb4bef96e5c1f1c4a.glb (HEAD 200, model/gltf-binary, 4,871,768 B)
- Licence: CC0 1.0. Verified on the Artheon page and in the GLB asset.extras (license "CC0-1.0", author "Minneapolis Institute of Art"). The Mia record says Public Domain. Credit "Minneapolis Institute of Art (Mia), via the Artheon Museum mirror" as a courtesy.
- Check: the internal name 180808_mia348_000101 carries the Mia object id 101. The height/width ratio matches the record. Scaled to the real 8.57 cm.
- Markings: the painted accession numbers ("16.51", "839", "16") were removed from the source texture with `src/clean_ink.py` (in-painted) before baking.
- Restyle: a shrine idol in darkened, weathered blue-green glaze, worn through to brown body at the edges and recesses. Repainted with no scan lighting, plus chips, cracks, pits, grime and dust. Decimated 62k → 20k tris. The `_statue` variant is uniformly scaled to 2.0 m tall for a shrine idol. Because the wear was authored at amulet scale, it reads as coarse weathering at statue size.
