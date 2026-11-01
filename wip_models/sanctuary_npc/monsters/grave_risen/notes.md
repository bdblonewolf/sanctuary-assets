# grave_risen (zombie) — status: WIP, stretch target NOT met
- out/grave_risen.glb 3.11 MB (5 clips: idle, walk, attack, hit, death; NLA, no extensions), out/grave_risen_rig.glb 2.68 MB
- Weights: heat skin + 4 rounds local reweight (scripts/heat.py, loop.sh). No triangles deleted.
- Worst stretch 6.79x (attack f24, tunic/hip z~0.94). Per clip: attack 6.79, death 5.94, hit 5.37, walk 3.94, idle 2.61. Target 2.5x failed after many attempts -> stopped per stop rule.
- Hotspots: tunic skirt spanning legs, back of hips, clavicle.
- Not done: element tint, previews, Mixamo wishlist finalization.

## 2026-10-31 16:25 EDT — skirt panel pass: FAILED (stopped per stop rule)
- scripts/cloth.py (seam split F/B, skirt_F/skirt_B bones under Hips, panel weights) + bake_cloth() in retarget.py (damped follow) + stretch.py skin/cloth split (cloth limit 3.0).
- Attempts (worst skin / cloth): 11.4/16.3, 28.7/16.3, 34.3/13.0, 92/21, 32/21 -> loop 12/53, 44.8/26.6. All worse than baseline 6.79.
- Root causes found: forearms/hands still welded to tunic at hip (z~0.9), back hem (z~0.44) carries cross-leg weights; panel weights clash with surrounding heat weights.
- Restored baseline (heat + reweight, 6.79x). cloth cfg parked as "cloth_wip" in cfg.json.
