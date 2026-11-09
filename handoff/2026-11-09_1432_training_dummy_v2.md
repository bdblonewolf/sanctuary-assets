# Gothic training dummy v2 look pass

See `2026-11-09_1417_training_dummy.md` (v2 section) for full details.


---

## v2 — 2026-11-09 ~14:32 EST (look pass)

Addressed weak silhouette vs reference. **v1 kept.** New files under `handoff/dummy_gothic_v2/`.

### Fixes vs v1
1. **Arms:** Continuous weathered timber crossbar (~1.10 m) through the torso at shoulder height; short burlap sleeve cuffs + rope wraps at ends; straw tuft clusters at wrists (no ball sleeves).
2. **Torso/head:** Lathed tapered sack with pinched hem (double rope cinch + gathers); wrinkle deform; head with squarer gathered crown + straw tuft; front-mapped X eyes + stitched mouth; triple neck rope.
3. **Target:** Concentric muted red/blue/cream rings **painted onto front torso faces** (subdivided, radial UVs) — conforming, no floating/clipped disc.
4. **Straw:** Fan clusters (`cut_straw` alpha cards) at hem, wrists, and crown — not floating rings.
5. **Post/base:** Post clear below hem; planked 0.46 m base; iron side bands, corner brackets, rivets, post collar.

### Files
| File | Bytes | Tris |
|------|------:|-----:|
| `dummy_gothic_v2/dummy_gothic_v2.glb` | 2567688 | 5838 (+12 col) |
| `dummy_gothic_v2/dummy_gothic_v2_lite.glb` | 1368928 | 4546 (+12 col) |
| `dummy_gothic_v2/dummy_hit_physics.js` | — | same spring as v1 |
| `dummy_gothic_v2/preview.html` | — | click-to-hit |
| `dummy_gothic_v2/preview_front.png` | — | front, collider hidden |
| `dummy_gothic_v2/preview_q34.png` | — | 3/4 view |
| `dummy_gothic_v2/preview_dummy_gothic_v2.png` | — | same as q34 |

### Hierarchy (unchanged contract)
`dummy_root` → `dummy`, `hit_center` @ `[0,1.25,0]`, `col_dummy` box `size_m≈[0.55,0.50,1.55]`.

Materials: `m_sack_burlap`, `m_sack_face`, `m_wood_plank`, `m_wood_beam`, `m_iron_band` (metal 0.32, darkened), `m_rope_hemp`, `m_target_paint`, `cut_straw`, plus arrow mats.

**Note:** Original reference attachment hash was not present on disk during this pass; built against the written brief + iterative front/¾ QA. Prefer **v2** for immersion.
