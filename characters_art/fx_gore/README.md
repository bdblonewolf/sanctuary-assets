# fx_gore - stump / tear-off caps

| Mobile copy (load this) | Master |
|---|---|
| `gore_caps.glb` | `masters/gore_caps.glb` |

8 random flesh + bone tear-off caps, 313-462 tris each (jagged, tattered skin rims, bone stubs), one shared material on **one 3-map atlas** (`textures/gore_atlas_{bc,n,orm}.png`, also embedded once in the GLB):
`gore_cap_flesh` (no bone), `gore_cap_limb_a/b/c`, `gore_cap_neck`, `gore_cap_waist` (462), `gore_sev_a/b` (severed-side caps).
Cap +Z is the outward normal, unit size about radius 0.1 m - scale to the cut radius and parent to a bone.
The per-monster `*_dismember.glb` files already contain caps placed and weighted at their cuts; use this kit for anything else (e.g. new monsters).

`src/`: gore_kit.py / gore_tex.py (cap + atlas builder), dismember_build.py (`blender -b --python dismember_build.py -- in.glb outdir name`), half_build.py (`blender -b <name>_dismember.blend --python half_build.py -- outdir name`).
Preview: preview_caps.png, preview_dismember_all.png. All original work (CC0-style, no third-party assets).
