# Corrupted Phimn — notes

Files: out/corrupted_phimn_caster.glb (Form A, 4.26 MB), out/corrupted_phimn_feral.glb (Form B, 3.41 MB).
Rig: Mixamo `mixamorig:` skeleton (untouched), armature "corrupted_phimn", 1.42 m adult proportions (copied from ayla_phimn_body.glb; original not edited).
Form A extra bones (children of mixamorig:Spine2): wing_{L,R}_1, wing_{L,R}_2, wing_{L,R}_f1..f4. Wing flap is baked into the clips (procedural).
Form A clips are hovering: hips are offset +0.32 m up; place the root on the ground, the feet float.

## Materials
mon_skin (base + emissive veins/runes), mon_glow (eyes), mon_fx (hand magic orbs), mon_wing, mon_hair, mon_leather, mon_bone, mon_horn.

## Element tint (one parameter: element name -> values below; see scripts/glbtool.py set_element)
| element | mon_skin baseColor | mon_wing baseColor | mon_hair baseColor | glow (emissive of mon_skin/mon_glow/mon_fx) | mon_glow strength |
|---|---|---|---|---|---|
| fire | 0.88,0.30,0.24 | 0.42,0.12,0.10 | 0.030,0.018,0.016 | 1.00,0.28,0.04 | 6 |
| ice | 0.46,0.62,1.00 | 0.20,0.27,0.42 | 0.016,0.020,0.030 | 0.30,0.68,1.00 | 6 |
| lightning | 0.80,0.70,0.86 | 0.30,0.24,0.34 | 0.022,0.018,0.026 | 0.78,0.66,1.00 | 7 |
| poison | 0.58,0.72,0.38 | 0.24,0.28,0.14 | 0.018,0.022,0.014 | 0.42,1.00,0.12 | 6 |
Apply: baseColorFactor = value+[1]; emissiveFactor = glow; KHR_materials_emissive_strength: mon_skin 1.0, mon_glow per table, mon_fx 4.0.
In three.js: set material.color / material.emissive / material.emissiveIntensity on the same material names.

## Clips
A: idle, move (idle + procedural hover glide), attack_cast (Standing 2H Magic Attack 01), attack_cast_1h (Standing 1H Magic Attack 01), hit (Standing React Small From Front), death (Standing React Death Backward). All Mixamo, retargeted via retarget_test.py method.
B: idle, run, sniff, attack_claw, attack_pounce (in place, ~0.5 m lunge then settles back — move the root in game), hit, death. All procedural (IK rig baked to FK).

## QA
Max 4 influences, weights normalized (all meshes). Stretch worst: A 3.15x, B 3.08x (target 2.5x) — only on mm-length edges (hair roots at shoulders, armpit of top, palm, boot toes).

## v2 (2026-10-31)
- Pipeline: build.py -> anim.py/animB.py -> **reweight.py** (new post-anim hand/thumb/foot/crotch/top reweight) -> export.py -> stretch.py
- render.py: action `bind` = true bind pose (used for A rest previews); B rest previews = idle @0.3
- New meshes: mon_runes (constant red emissive decal, NOT element-tinted), mon_fangs, mon_mouth, mon_straps (A halter), mon_spear_strap, mon_wrap_rags (B)
- B hair weighted 100% Head (crouch spine is ~117deg; spine-weighted hair flew off the back). B spear rests on the back surface, Spine2 rigid.
- Fire skin tint now (1.0,0.26,0.18). Hair strands A=400, B=620.
- Sizes: caster 3,966,548 B; feral 3,681,588 B. Worst stretch: A 2.62 (mon_runes, death), B 2.76 (body foot/toe, death).
