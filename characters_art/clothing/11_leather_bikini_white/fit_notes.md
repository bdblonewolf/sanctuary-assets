# 11_leather_bikini_white — fit notes
- Files: npc_f_leather_<set>_hourglass_a.glb / _hourglass_b.glb (one fit per body; the same mesh does NOT fit both, because waist/hip/thigh hull shapes differ). Each ~2.6 MB, embedded WEBP 2K basecolor/normal/ORM (alpha-clip on the tattered cloth). Source PNGs are in textures/.
- Nodes: npc_f_leather_<set>_chest, _belt (belt+tassets+loincloth), _vambrace_L, _vambrace_R, _boots (boots+thigh/knee plates), _pauldron (left). 52-bone mixamorig skin, ≤4 influences, normalized; nothing weighted to the hands.
- Bodies: built on the trimmed copies bodies_fit/female_medium_hourglass_{a,b}.glb (linen undergarment band at the midriff turned into skin, shorts trimmed to briefs). approved/ was not touched.
- Weights: transferred from the body by nearest face, limited to the allowed bones per piece (chest: Spine*; belt: Hips/Spine; tassets/loincloth: Hips plus a ramp to the thighs; vambraces: 100% forearm; boots: leg chain), then smoothed. Solidify is applied AFTER weighting, so the inner and outer shells share weights.
- Stretch (Idle, Looking Around, Walking; every 2nd frame; edges <1 mm ignored): chest 1.41, belt 1.5, pauldron ≤2.1, vambraces 1.0. Boots 4.1 on a / 8.5 on b, but only on ~20 micro-edges (1–2 mm) at the front of the knee left over from the voxel remesh. That moves things by less than 1 cm and doesn't show in renders. Fix this with a cleaner boot topology later.
- Poke counts (stretch_poke_*.json) are mostly false positives: hand verts passing the tassets as the arms swing, skin at the armpit rim of the bandeau, and the front deltoid under the pauldron during Looking Around. Use body_mask_*.json, which lists the body triangles fully covered at all times, to hide the skin under the garments in game.
- Known gaps vs the sheet: the pauldron is simpler/flatter, the boots have no raised heel, and the lacing is texture-only.

## Equip/unequip (added)
The loincloth is now its own node. Each piece is exported separately in pieces/ as <node>_<body>.glb, with a <node>_<body>.mask.json listing the body vertex indices it covers plus the bone regions. All pieces are listed in ../manifest.json.

## 15:28 pass (boots / belt / chest)
- Boots: shaft weights come from the body's lower-leg weights with UpLeg removed. Body b uses lighter smoothing (1). Calf clearance is 8 mm. Max stretch is 2.11 on body a and 2.32 on body b.
- Belt: shrinkwrapped to 3 mm. Chest: shrinkwrapped to 2.5 mm over the bust, blending to the loose hull above z 1.13 at the strap.
- The poke test now ignores arm and hand verts for non-arm pieces.
- Still open: the calf clip (237 frames) and the chest clip at the strap/underarm (237 frames). Both are under 2 mm or within the strap zone; see stretch_poke_*.json.
