# Sanctuary starter monsters (batch 1)

| Monster | Status | File | Size | Height | Clips | Worst stretch | Base licence |
|---|---|---|---|---|---|---|---|
| Bone Axeman | done | bone_axeman/bone_axeman.glb | 1.25 MB | 1.80 m | idle, walk, attack1, attack2, hit, death | 2.99x | CC-BY-4.0 (danielmclogan), with credit |
| Bone Swordsman | done | bone_swordsman/bone_swordsman.glb | 1.17 MB | 1.78 m | idle, walk, attack1, attack2, hit, death | 2.40x | CC-BY-4.0 (danielmclogan), with credit |
| Bone Archer | done | bone_archer/bone_archer.glb | 1.26 MB | 1.84 m incl. helmet | idle, walk, attack1, attack2, hit, death | 2.45x | CC-BY-4.0 (danielmclogan), with credit |
| Rag Zombie (v2) | done | rag_zombie/rag_zombie.glb | 2.62 MB | 1.78 m | idle, walk, attack, hit, death | 2.79x | CC0 (MPFB2, Poly Haven) |
| Grave Old Man (v2) | done | grave_old_man/grave_old_man.glb | 1.33 MB | 1.78 m | idle, walk, attack, hit, death | 2.95x | CC0 (MPFB2, Poly Haven) |
| Mummified Crawler | MISSING | - | | | | | No crawl or prone locomotion clip in the library, and no licence-safe rigged source |
| Fallen Spawnling | MISSING | - | | | | | No licence-safe, realistic, rigged ~1 m imp/demon source without a login. A scaled human body would read wrong |
| Spawn Shaman | MISSING | - | | | | | Same as Fallen Spawnling |
| Grove Mauler (bear) | MISSING | - | | | | | No licence-safe, realistic, rigged quadruped bear without a login. Sketchfab downloads need sign-in, which was not used. No quadruped animation set |

Animations on every model are Adobe Mixamo motion data (no Mixamo characters). Each per-monster README lists sources, clips, stretch, validator results and known issues. All glTF validator runs report 0 errors and no extensions.


Lineup (v2): lineup_v2.png (bone_axeman, bone_swordsman, bone_archer, rag_zombie, grave_old_man).

Pipeline note: `_pipeline/retarget2.py` bone-direction now prefers `mixamorig:` children, so extra cloth bones under Hips no longer twist the Hips retarget. The skeleton monsters were built before this change; it does not affect them (no extra bones).
