# wip_models: unfinished, superseded, test and source files

Unfinished, superseded and test models plus Blender (.blend) and Blender-Python sources for the finished models, committed Nov 1, 2026 so the game engineer can open them in Blender and carry on. The finished, game-ready GLBs are in `characters_art/`.
Source folder structure is kept. Files were saved with Blender 4.2, so open them in 4.2 or newer. Paths inside .blend files point to the original `/workspace/...` layout, so relink textures if any show as missing.

Skipped: base iterations byte-identical to approved bodies (female_medium_v1, v8b, v9b), the ossuary/razor src GLBs in sanctuary_npc (identical copies of the models3d files), stage1/walk test .blend scenes, Blender install files, and raw third-party downloads.

| Path | Type | MB | State | What it is |
|---|---|---|---|---|
| `wip_models/sanctuary_art/monsters/models3d/ossuary_footman.glb` | glb | 2.20 | Unfinished | Art-bot monster model, never rigged/animated (NPC rig pass produced no output) |
| `wip_models/sanctuary_art/monsters/models3d/razor_tollman.glb` | glb | 2.61 | Unfinished | Art-bot monster model, never rigged/animated (NPC rig pass produced no output) |
| `wip_models/sanctuary_art/props/museum/work/mourner/low.blend` | blend | 2.11 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/museum/work/reliquary/low.blend` | blend | 1.53 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/mia_false_door/low.blend` | blend | 3.80 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/mia_sekhmet/low.blend` | blend | 4.71 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/ph_gothic_statue/low.blend` | blend | 13.03 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/ph_kite_shield/low.blend` | blend | 15.40 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/ph_large_castle_door/low.blend` | blend | 12.58 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/ph_wine_barrel_01/low.blend` | blend | 2.93 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/si_kneeling_winged_monster/low.blend` | blend | 8.91 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_art/props/work/si_kylix/low.blend` | blend | 2.65 | Source (finished) | Blender source (low-poly bake scene) of the finished prop in characters_art/props/ |
| `wip_models/sanctuary_env/statues_angels/statue_angel_hero_bust_v1.glb` | glb | 3.41 | Superseded | Statue hero bust v1 backup, replaced by v2 in characters_art/statues/ |
| `wip_models/sanctuary_env/statues_angels/work/bake/low.blend` | blend | 3.50 | Source (finished) | Blender bake scene for the angel statue hero bust |
| `wip_models/sanctuary_npc/bases/female_medium_v2_cone.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v3.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v4.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v5.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v6.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v7.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v8.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_medium_v9.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/female_tiny_v1.glb` | glb | 0.96 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/male_brute_heavy_v1.glb` | glb | 0.95 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/bases/male_brute_heavy_v2.glb` | glb | 0.95 | Superseded | Body base iteration, replaced by the approved bodies in characters_art/bodies/ |
| `wip_models/sanctuary_npc/martsirt/src/anim.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/fbx2glb.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_bl.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_boot.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_detail.py` | py | 0.01 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_fin.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_fit.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_head.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_mat.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/lib_props.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/manifest.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/namefix.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/npc_quill.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/npc_wolcen.py` | py | 0.02 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/pipeline.sh` | sh | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/pose.py` | py | 0.01 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/preview.py` | py | 0.01 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/sheet.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/strands_tex.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/martsirt/src/swatch_prep.py` | py | 0.00 | Source (first pass) | Martsirt NPC build script (Blender Python); see characters_art/npcs/martsirt/README.md and MANIFEST.json for the pipeline |
| `wip_models/sanctuary_npc/monsters/axeman/notes.md` | md | 0.00 | Notes | axeman rig-pass notes (status: stopped) |
| `wip_models/sanctuary_npc/monsters/axeman/out/axeman.glb` | glb | 1.94 | Superseded / unfinished | Oct 31 axeman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/axeman/ replaces it |
| `wip_models/sanctuary_npc/monsters/axeman/out/axeman.glb.bad.json` | json | 0.00 | Superseded / unfinished | Oct 31 axeman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/axeman/ replaces it |
| `wip_models/sanctuary_npc/monsters/axeman/out/axeman_rig.blend` | blend | 4.28 | Superseded / unfinished | Oct 31 axeman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/axeman/ replaces it |
| `wip_models/sanctuary_npc/monsters/axeman/out/axeman_rig.glb` | glb | 1.49 | Superseded / unfinished | Oct 31 axeman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/axeman/ replaces it |
| `wip_models/sanctuary_npc/monsters/axeman/out/clips.json` | json | 0.00 | Superseded / unfinished | Oct 31 axeman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/axeman/ replaces it |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/notes.md` | md | 0.00 | Notes | Corrupted Phimn build notes |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/anim_A.blend` | blend | 21.49 | Source (finished) | Blender animation scene for the final Corrupted Phimn caster (A) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/anim_B.blend` | blend | 24.37 | Source (finished) | Blender animation scene for the final Corrupted Phimn feral (B) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/rest_A.blend` | blend | 13.44 | Test | Corrupted Phimn rest-pose build (Blender scene) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/rest_A.glb` | glb | 3.27 | Test | Corrupted Phimn rest-pose build (glb) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/rest_B.blend` | blend | 12.40 | Test | Corrupted Phimn rest-pose build (Blender scene) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/rest_B.glb` | glb | 3.33 | Test | Corrupted Phimn rest-pose build (glb) |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/test_A.glb` | glb | 4.79 | Test | Early Corrupted Phimn test export |
| `wip_models/sanctuary_npc/monsters/corrupted_phimn/out/test_B.glb` | glb | 4.01 | Test | Early Corrupted Phimn test export |
| `wip_models/sanctuary_npc/monsters/grave_risen/notes.md` | md | 0.00 | Notes | grave_risen rig-pass notes (status: stopped) |
| `wip_models/sanctuary_npc/monsters/grave_risen/out/clips.json` | json | 0.00 | Superseded / unfinished | Oct 31 grave_risen rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/grave_risen/ replaces it |
| `wip_models/sanctuary_npc/monsters/grave_risen/out/grave_risen.glb` | glb | 3.11 | Superseded / unfinished | Oct 31 grave_risen rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/grave_risen/ replaces it |
| `wip_models/sanctuary_npc/monsters/grave_risen/out/grave_risen.glb.bad.json` | json | 0.03 | Superseded / unfinished | Oct 31 grave_risen rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/grave_risen/ replaces it |
| `wip_models/sanctuary_npc/monsters/grave_risen/out/grave_risen_rig.blend` | blend | 4.13 | Superseded / unfinished | Oct 31 grave_risen rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/grave_risen/ replaces it |
| `wip_models/sanctuary_npc/monsters/grave_risen/out/grave_risen_rig.glb` | glb | 2.68 | Superseded / unfinished | Oct 31 grave_risen rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/grave_risen/ replaces it |
| `wip_models/sanctuary_npc/monsters/ossuary_footman/scripts/pick_shield.json` | json | 0.02 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/ossuary_footman/scripts/thin.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/ossuary_footman/scripts/vis.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/boxpick.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/comp.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/pick_cleaver.json` | json | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/pick_hook.json` | json | 0.01 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/thin.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/razor_tollman/scripts/vis.py` | py | 0.00 | Unfinished | Helper script/data from the abandoned rig pass for this monster |
| `wip_models/sanctuary_npc/monsters/starter/bone_archer/work/bone_archer.blend` | blend | 4.44 | Source (finished) | Blender source of the finished starter monster in characters_art/monsters/ |
| `wip_models/sanctuary_npc/monsters/starter/bone_axeman/work/bone_axeman.blend` | blend | 4.41 | Source (finished) | Blender source of the finished starter monster in characters_art/monsters/ |
| `wip_models/sanctuary_npc/monsters/starter/bone_swordsman/work/bone_swordsman.blend` | blend | 4.17 | Source (finished) | Blender source of the finished starter monster in characters_art/monsters/ |
| `wip_models/sanctuary_npc/monsters/starter/grave_old_man/work/grave_old_man.blend` | blend | 4.90 | Source (finished) | Blender source of the finished starter monster in characters_art/monsters/ |
| `wip_models/sanctuary_npc/monsters/starter/rag_zombie/work/rag_zombie.blend` | blend | 5.57 | Source (finished) | Blender source of the finished starter monster in characters_art/monsters/ |
| `wip_models/sanctuary_npc/monsters/swordsman/notes.md` | md | 0.00 | Notes | swordsman rig-pass notes (status: stopped) |
| `wip_models/sanctuary_npc/monsters/swordsman/out/clips.json` | json | 0.00 | Superseded / unfinished | Oct 31 swordsman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/swordsman/ replaces it |
| `wip_models/sanctuary_npc/monsters/swordsman/out/swordsman.glb` | glb | 1.76 | Superseded / unfinished | Oct 31 swordsman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/swordsman/ replaces it |
| `wip_models/sanctuary_npc/monsters/swordsman/out/swordsman.glb.bad.json` | json | 0.01 | Superseded / unfinished | Oct 31 swordsman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/swordsman/ replaces it |
| `wip_models/sanctuary_npc/monsters/swordsman/out/swordsman_rig.blend` | blend | 4.09 | Superseded / unfinished | Oct 31 swordsman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/swordsman/ replaces it |
| `wip_models/sanctuary_npc/monsters/swordsman/out/swordsman_rig.glb` | glb | 1.36 | Superseded / unfinished | Oct 31 swordsman rig/animation attempt (stretch target not met); the Nov 1 art-bot model in characters_art/monsters/swordsman/ replaces it |
| `wip_models/sanctuary_npc/work_cl/w_a_red/stage2.blend` | blend | 10.58 | Source (finished) | Blender stage-2 build scene for the finished outfit w_a_red (w_ayla = Ayla of the Phimn; w_a/w_b = hourglass A/B, white/red leather) |
| `wip_models/sanctuary_npc/work_cl/w_a_white/stage2.blend` | blend | 10.24 | Source (finished) | Blender stage-2 build scene for the finished outfit w_a_white (w_ayla = Ayla of the Phimn; w_a/w_b = hourglass A/B, white/red leather) |
| `wip_models/sanctuary_npc/work_cl/w_ayla/stage2.blend` | blend | 7.51 | Source (finished) | Blender stage-2 build scene for the finished outfit w_ayla (w_ayla = Ayla of the Phimn; w_a/w_b = hourglass A/B, white/red leather) |
| `wip_models/sanctuary_npc/work_cl/w_b_red/stage2.blend` | blend | 10.45 | Source (finished) | Blender stage-2 build scene for the finished outfit w_b_red (w_ayla = Ayla of the Phimn; w_a/w_b = hourglass A/B, white/red leather) |
| `wip_models/sanctuary_npc/work_cl/w_b_white/stage2.blend` | blend | 10.11 | Source (finished) | Blender stage-2 build scene for the finished outfit w_b_white (w_ayla = Ayla of the Phimn; w_a/w_b = hourglass A/B, white/red leather) |
