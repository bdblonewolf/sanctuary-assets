# npc_ilyra_body_hair_v2.glb: skin-colour fix

This is a recoloured copy of `npc_ilyra_body_hair.glb`, which is left untouched. The fix is colour only.

- The `linen_undergarment` material covers the strapless chest band and the shorts (mesh `base`, primitive 1, 2,254 tris). It now uses her skin material's values:
  - the same base-colour texture (texture 0)
  - base-colour factor 1,1,1,1
  - metallic 0
  - roughness 0.501 (skin is 0.5; the extra 0.001 only stops the mobile dedup step from merging the two materials)
- Every texel this primitive's UVs land on is pure white in the skin texture. That makes it an exact match for the body skin, and no off-colour patch can show through gaps in armour.
- Unchanged:
  - geometry, vertex order and accessors (byte-identical mesh)
  - skin and rig, with all 55 nodes the same
  - hair, face and eyes
  - textures (byte-identical images)
  - material count (4) and material names. The material keeps the name `linen_undergarment`.
- Tris: 43,660 total (base 24,502 + 2,254 + 280; ilyra_locks 16,624).
- `masters/npc_ilyra_body_hair_v2.glb` is the master. The root file is the `mobile_compress.sh` output, with no meshopt or Draco. Both pass glTF validation with 0 errors.
- Preview: `previews/npc_ilyra_body_hair_v2_before_after.png` shows front and back, before and after.
