# hero_anims_m2m test pack (small)

Add-only test build from `ANIM_MAPPING.md` (cab6525). Skeleton + animation only (no meshes/textures). mixamorig bones, 30 fps, in-place (hips X/Z zeroed, Y bob kept). Clip names match game (no `_v2` suffix).

| File | Contents |
|------|----------|
| `hero_anims_m2m_m.glb` | Male sources (`m2m_walk` / `m2m_sprint`) |
| `hero_anims_m2m_f.glb` | Female sources (`m2m_walk_female` / `m2m_run_female`) |
| `hands_check.png` | Quick hand pose sheet on warrior + archer |

**Clips (22, identical names on both):** armed idles `ss_idle`, `axe_idle`, `gs_idle`, `magic_idle`; walk/run `_2` for ss/axe/gs/magic/bow/unarmed; peace/AFK `town_idle`, `town_look_around`, `town_weight_shift`, `town_idle_2`–`_4`.

**Hands (baked finger rotations from hero_locomotion_v5 closed-fist):** armed idles = weapon hand FIST (RH; LH for bow) + free hand FLAT; walks/runs = both FIST; town/AFK = both FLAT.

**Stride:** Mixamo masters are already in-place (hip X/Z ≈ 0), so cycle travel vs game assumptions (walk 1.45 m, run 4.43 m) is not measurable from these clips — no stride retarget applied.

Not a full hero pack. Load by clip name onto mixamorig characters.
