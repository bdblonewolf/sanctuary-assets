# Sanctuary museum props: Mourner and Arm Reliquary

Restyled game props for Sanctuary, built from Cleveland Museum of Art 3D scans. The scans were used only as **reference**: the base colour was de-lit and repainted darker and grittier in Sanctuary's own style, all markings were removed, and chips, cracks and wear were added. The silhouettes stay faithful to the originals.

| File | Tris (visual) | Size W×D×H (m) | File size | Validator |
|---|---|---|---|---|
| `mourner.glb` | 21,998 | 0.144 × 0.120 × 0.409 | 2.09 MB (2,094,188 B) | 0 errors, 0 warnings, no extensions |
| `mourner_statue.glb` (×4.402) | 21,998 | 0.635 × 0.527 × 1.800 | 2.09 MB (2,094,224 B) | 0 errors, 0 warnings, no extensions |
| `reliquary.glb` | 13,980 | 0.126 × 0.094 × 0.515 | 2.42 MB (2,423,008 B) | 0 errors, 0 warnings, no extensions |

Validated with `gltf-validator` (`/tmp/gv/node_modules/gltf-validator`).

## Format
- Plain GLB with no extensions. 1 unit = 1 m, Y up, origin at the base centre (bottom at y = 0), and the front faces +Z.
- Nodes: the visual mesh plus one `col_<name>` box collider: 90% of the footprint, full height, starting at y = 0. Hide or skip it in rendering.
- Embedded JPEG PBR textures (one material per model):
  - 2K base colour (sRGB).
  - 2K tangent-space normal map, baked from the high-res chipped mesh plus a detail height pass.
  - 1K ORM: R = AO (baked), G = roughness, B = metallic. AO is wired as glTF occlusion.

## Restyle notes
- **Mourner** (alabaster, about 1404–1410):
  - De-lit scan colour (baked museum shading regressed out against AO and cavity), repainted as aged, dirty alabaster or stone.
  - Crevice grime, dust on the upper surfaces, streaks, hairline cracks, and about 9 faceted edge chips in the geometry.
  - Red accession ink ("58") and underside mount holes and markings scrubbed out; the underside is repainted plain dark stone. Metallic 0.
- **Arm Reliquary** (silver-gilt, about 1340s):
  - Re-materialed as old gold and tarnished silver with heavy black tarnish in recesses, verdigris in silver crevices, polished wear on convex edges, scratches, dents and about 7 chips.
  - The underside iron ring, wax and label blobs were removed; the base is repainted as a dark, non-metal oak/iron base plate.
- Pipeline (scripts in `src/`): voxel remesh, chip displacement, decimate, xatlas UVs, Cycles bakes (normal, AO, cavity, colour reference), numpy restyle (`tex.py`), export (`export.py`), tangent check (`fixtan.py`).

## Previews (`previews/`)
Crypt lighting: dim blue-grey ambient, a faint cold moonlight and one warm candle key.
- `mourner_front|iso|close.png`
- `mourner_statue_front|iso|close.png`
- `reliquary_front|iso|close.png`

## Source and licence
- **Mourner from the Tomb of Philip the Bold**: Claus de Werve, Cleveland Museum of Art, accession **1958.66**.
  - Museum page: https://www.clevelandart.org/art/1958.66
  - Sketchfab model: https://sketchfab.com/3d-models/0d89139b17024e378f2882e575531e08
  - Downloaded from the Artheon Museum mirror: https://images.artheonmuseum.org/ugc/sketchfab/0d89139b17024e378f2882e575531e08.glb
  - Raw copy: `raw/mourner_1958.66_artheon.glb`, sha256 `1a7e56ce…48ea2`, 84,996 tris.
- **Arm Reliquary of the Apostles**: Cleveland Museum of Art, accession **1930.739**.
  - Museum page: https://www.clevelandart.org/art/1930.739
  - Sketchfab model: https://sketchfab.com/3d-models/df98bbcd1c3b46f0a9d640e925490f4a
  - Downloaded from the Artheon Museum mirror: https://images.artheonmuseum.org/ugc/sketchfab/df98bbcd1c3b46f0a9d640e925490f4a.glb
  - Raw copy: `raw/reliquary_1930.739_artheon.glb`, sha256 `d170099b…d894`, 89,852 tris.
- **Licence: CC0 1.0 (public domain dedication).**
  - The CMA Open Access API lists `share_license_status: CC0` for both objects (API ids 135538 and 112316).
  - The mirrored GLBs carry CMA / CC0-1.0 credit in `asset.extras`.
  - Both scans were checked against the CMA photos (`raw/cma_*_print.jpg`) and the museum's published dimensions.
- No attribution is required. As a courtesy: *"Based on 3D scans courtesy of The Cleveland Museum of Art (CC0)."*
