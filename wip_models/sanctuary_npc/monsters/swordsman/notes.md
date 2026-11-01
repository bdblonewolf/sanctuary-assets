# swordsman — status: weights step STOPPED (stop rule), tints/previews not done
- Source: /workspace/sanctuary_art/monsters/models3d/swordsman.glb copied 16:25 EDT; mtime 2026-10-31 16:23:09 EDT (already the art-bot fixed version; re-checked 16:31, identical).
- out/swordsman.glb 1756628 B, 6 clips (idle, walk, attack1, attack2, hit, death; NLA), no extensions. Materials mon_skin, mon_glow (eye spheres on Head), weapon mat. Weapon node stays on mixamorig:RightHand.
- Weights: art-bot weights + scripts/fix.py local reweight loop (10 rounds). Heat skinning failed (0 verts weighted on thin skeleton mesh); limb-chain cleanup in prep.py made it worse (83-149x) -> reverted.
- Sword nudged +4 cm up (rest, world Z). Worst skin stretch 6.96x (attack2 f22, mid-jump). Per clip: atk1 5.33, atk2 6.96, death 5.93, hit 3.95, idle 2.96, walk 3.06. Hotspots: right hand/wrist where art-bot weights mix finger+forearm+UpLeg, and spine/rib z~1.2.
