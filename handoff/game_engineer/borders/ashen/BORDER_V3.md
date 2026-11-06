# Ashen Coast border v3 (90x180, after WP1)

- Layout: `layout_coast_v3.json` (216 props, props only, no kit pieces). Proof: `layout_coast_v3_proof.png` (filled dots = v3, red rings = where the old v2 ring landed after the +24 offset).
- Generator: `../tools/gen_coast_border_v3.py`. Run it from the repo root. It is deterministic.
- Prompt: `../../world_v1_coast/PROMPT_COAST_BORDER_V3.txt` (CB3).
- `layout_coast_v2.json` is untouched. It is still the layout for the old 42x112 path.

## Edges
- **N (land, x 6–90; sea x 0–6):** a far row of crag stacks, spires, winter gtrees and sea-stack crags 6–11 m out. A middle row of gtrees, stacks and rocks 1.8–5 m out. A lip of grass, stumps and rocks 0.3–1.5 m out.
  - 8 drawable v2 north-ridge props are carried over (+24 x) and pushed off walkable row 0.
  - The Martsirt gate x=36.5 is kept clear (±6.5 m).
- **E (land, z 0–160):** the same three rows. This edge was bare after WP1. The Bastion exit z=81 is kept clear (±6.5 m).
- **E (sea, z 160–180), S and W (sea):** shore rocks 1–6 m out and sea stacks 10–26 m out, at y −0.4 on the sea plane.
- **Exclusions:** nothing inside the map, nothing on walkable tiles, no colliders, no tile changes.

## Replaces, not doubles
CB3 loads v3 instead of the v2 offset+skip ring and falls back to v2 only if v3 fails to load. The v2 pieces that WP1 kept are not placed again: the in-lagoon rocks and the trees standing in the W sea.

## Notes found while building
- The live GD loader drops every `models/outdoor/v5_maps/border/*` asset (border_peak, shelf and dune). In game it never draws:
  - 30 of the 97 coast v2 props;
  - 81 of 132 on Bastion;
  - 78 of 132 on Lut;
  - 109 of 183 on Market.
  v3 does not use them.
- The coast ground plane ends 1.7 m past the edge. Border props further out stood over nothing. CB3 step 3 extends the off-map skirt on N and E only.
- Tris: v3 ≈ 275k, against ≈ 245k for the v2 props that were actually drawn. Capped at 3 spires and 32 gtrees.
