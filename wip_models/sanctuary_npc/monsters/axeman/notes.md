# axeman — status: weights step STOPPED (stop rule), tints/previews not done
- Source: /workspace/sanctuary_art/monsters/models3d/axeman.glb copied 16:25 EDT; mtime 2026-10-31 16:22:12 EDT (already the art-bot fixed version; re-checked 16:31, identical).
- out/axeman.glb 1937152 B, 6 clips (idle, walk, attack1, attack2, hit, death; NLA), no extensions. Materials mon_skin, mon_glow (eye spheres on Head), weapon mat. Weapon node stays on mixamorig:RightHand.
- Weights: art-bot weights + scripts/fix.py local reweight loop (10 rounds). Heat skinning failed (0 verts weighted on thin skeleton mesh); limb-chain cleanup in prep.py made it worse (83-149x) -> reverted.
- Worst skin stretch 2.99x (attack2 f16, right chest/upper arm z~1.1). Per clip: atk1 2.57, atk2 2.99, death 2.93, hit 2.41, idle 2.09, walk 2.03.
