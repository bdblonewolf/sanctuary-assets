# PROVENANCE: SFX batch B1 (loot, gold, items, menus, potions, level-up)

Generated 2026-11-01 for Sanctuary. **Every file in this batch is original synthesis**, made from scratch in Python (numpy/scipy):
sine/modal resonator banks, filtered white noise, resonant filters and pitch-swept oscillators.
No recordings, samples, sample libraries or third-party audio of any kind were used, including no CC0 material.
No Diablo (or other copyrighted) audio was used or analysed as source material. The Diablo notes in the master list are feel references only.

License: original work created for the Sanctuary project. Ownership is Brian's (the project owner). No third-party license applies.

Reproduce: `python3 /workspace/sanctuary_audio/scripts/sfx/build_b1.py` (deterministic, seeded per file).
Code: `sfxlib.py` (primitives, loudness and true-peak meters), `b1_sounds.py` (designs), `build_b1.py` (render, normalize, encode, verify), `finalize_b1.py` (montage, provenance, status).

Format: Ogg Vorbis (libvorbis via libsndfile, quality about 5), 44.1 kHz, mono. Loudness was normalized to the per-row engine target (BS.1770 K-weighted, measured over the whole sound).
Peaks were limited to a true peak of ≤ −1 dBTP (4× oversampled, measured on the decoded Ogg). There is a 1.5 ms raised-cosine fade-in, a 10 ms fade-out, and a 6 ms fade on every internal layer.

| File | Master ID | Method | Source / license | Design | Seed | Length ms | LUFS | dBTP | SHA-256 (16) |
|---|---|---|---|---|---|---|---|---|---|
| `audio/sfx/loot/drop_common_01.ogg` | LT-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull floor thunk + settle bounce | 3689376878 | 330.0 | -19.9 | -4.68 | 9f43ebd40c3bd983 |
| `audio/sfx/loot/drop_common_02.ogg` | LT-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull floor thunk + settle bounce | 2888703925 | 330.0 | -19.9 | -5.61 | dcee5df9a33c560f |
| `audio/sfx/loot/drop_common_03.ogg` | LT-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull floor thunk + settle bounce | 4136154414 | 330.0 | -20.0 | -5.6 | d4bbb352ebf40658 |
| `audio/sfx/loot/drop_uncommon_01.ogg` | LT-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + faint iron tick | 2397619251 | 365.7 | -20.0 | -4.68 | e61cae8d8591ebf9 |
| `audio/sfx/loot/drop_uncommon_02.ogg` | LT-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + faint iron tick | 2454040324 | 368.0 | -19.9 | -4.72 | 2096e1674bb8fc15 |
| `audio/sfx/loot/drop_uncommon_03.ogg` | LT-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + faint iron tick | 1012260027 | 364.8 | -20.0 | -4.43 | 861d87d8a1d5e0f6 |
| `audio/sfx/loot/drop_rare_01.ogg` | LT-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + pitched iron ring (D5 area) + faint fifth | 1971064757 | 680.0 | -17.6 | -1.48 | 01bf081e6c67ca0d |
| `audio/sfx/loot/drop_rare_02.ogg` | LT-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + pitched iron ring (D5 area) + faint fifth | 3937364998 | 680.0 | -16.6 | -1.38 | 6ec8b3bab28115c8 |
| `audio/sfx/loot/drop_rare_03.ogg` | LT-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + pitched iron ring (D5 area) + faint fifth | 1075113590 | 680.0 | -16.4 | -1.39 | 14ae2180d44c1c6e |
| `audio/sfx/loot/drop_epic_01.ogg` | LT-04 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + low bell bloom (G3 area) | 3047693797 | 1150.0 | -14.2 | -1.45 | edea5cf242c4d4a8 |
| `audio/sfx/loot/drop_epic_02.ogg` | LT-04 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + low bell bloom (G3 area) | 3132226789 | 1150.0 | -14.6 | -1.41 | 005f64f5fcc34ee5 |
| `audio/sfx/loot/drop_epic_03.ogg` | LT-04 | Synthesis (Python numpy/scipy) | Original, no third-party source | thunk + low bell bloom (G3 area) | 225839943 | 1150.0 | -14.7 | -1.45 | 02568ad1e95aa91a |
| `audio/sfx/loot/drop_legendary_01.ogg` | LT-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | sub boom + heavy thunk + dark tolled bell (C3 area) | 1738748236 | 1480.0 | -15.1 | -1.32 | 0eda0b58e16bd9a5 |
| `audio/sfx/loot/drop_legendary_02.ogg` | LT-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | sub boom + heavy thunk + dark tolled bell (C3 area) | 2732055281 | 1480.0 | -15.8 | -1.34 | 91674ad988d37c44 |
| `audio/sfx/loot/drop_legendary_03.ogg` | LT-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | sub boom + heavy thunk + dark tolled bell (C3 area) | 3129123654 | 1480.0 | -15.0 | -1.38 | fd37a1290bb3f4f0 |
| `audio/sfx/loot/drop_potion_01.ogg` | LT-09 | Synthesis (Python numpy/scipy) | Original, no third-party source | two glass clinks on stone | 3298581305 | 378.7 | -20.0 | -7.94 | 98bc556710911cb7 |
| `audio/sfx/loot/drop_potion_02.ogg` | LT-09 | Synthesis (Python numpy/scipy) | Original, no third-party source | two glass clinks on stone | 770152449 | 400.0 | -20.0 | -7.63 | 7beaa5b174453688 |
| `audio/sfx/loot/drop_potion_03.ogg` | LT-09 | Synthesis (Python numpy/scipy) | Original, no third-party source | two glass clinks on stone | 3484731160 | 400.0 | -20.0 | -7.53 | e0d30c07d2a86b70 |
| `audio/sfx/gold/spill_01.ogg` | LT-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | coin cascade onto stone | 2012470968 | 388.0 | -20.1 | -6.02 | e93c8a93449921d4 |
| `audio/sfx/gold/spill_02.ogg` | LT-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | coin cascade onto stone | 2091844248 | 500.0 | -20.1 | -7.2 | b21e4abf97fa5cf7 |
| `audio/sfx/gold/spill_03.ogg` | LT-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | coin cascade onto stone | 1079102669 | 457.8 | -20.1 | -6.86 | 38f297056a1fafe4 |
| `audio/sfx/gold/pickup_01.ogg` | LT-07 | Synthesis (Python numpy/scipy) | Original, no third-party source | short coin gather into hand | 3981695540 | 235.1 | -22.0 | -9.44 | 7a8bd0966a0051b6 |
| `audio/sfx/gold/pickup_02.ogg` | LT-07 | Synthesis (Python numpy/scipy) | Original, no third-party source | short coin gather into hand | 4184581093 | 285.2 | -22.1 | -10.2 | be50151dd3f8bbaa |
| `audio/sfx/gold/pickup_03.ogg` | LT-07 | Synthesis (Python numpy/scipy) | Original, no third-party source | short coin gather into hand | 360605136 | 278.5 | -22.0 | -11.14 | 9a38eafc0287c3b6 |
| `audio/sfx/gold/pickup_04.ogg` | LT-07 | Synthesis (Python numpy/scipy) | Original, no third-party source | short coin gather into hand | 1752815827 | 264.7 | -22.0 | -10.57 | 2f23491911174983 |
| `audio/sfx/item/pickup_light_01.ogg` | LT-08 | Synthesis (Python numpy/scipy) | Original, no third-party source | light item stowed in pack | 208881901 | 111.4 | -22.4 | -10.11 | 9b1a89735638354d |
| `audio/sfx/item/pickup_armor_01.ogg` | LT-08 | Synthesis (Python numpy/scipy) | Original, no third-party source | armor item stowed in pack | 4057508910 | 285.0 | -22.2 | -8.52 | e10b98011f7ad1b8 |
| `audio/sfx/item/pickup_weapon_01.ogg` | LT-08 | Synthesis (Python numpy/scipy) | Original, no third-party source | weapon item stowed in pack | 3047656642 | 267.4 | -22.2 | -5.66 | 271ef368c9be27e2 |
| `audio/sfx/item/equip_weapon_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip weapon | 3340185008 | 451.0 | -20.2 | -3.14 | c620204f8afaed19 |
| `audio/sfx/item/unequip_weapon_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip weapon | 3630995122 | 260.6 | -20.3 | -6.74 | dbae99fc0a9b081f |
| `audio/sfx/item/equip_armor_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip armor | 593460947 | 442.3 | -20.1 | -7.45 | 078d0c7e02774614 |
| `audio/sfx/item/unequip_armor_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip armor | 3704936493 | 260.5 | -20.1 | -7.63 | 1614b404abb298bf |
| `audio/sfx/item/equip_helm_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip helm | 901745706 | 461.4 | -20.0 | -3.4 | 4b6769f16b9751cb |
| `audio/sfx/item/unequip_helm_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip helm | 1802086815 | 361.4 | -20.0 | -6.75 | 9fa88b30feeeced6 |
| `audio/sfx/item/equip_shield_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip shield | 2401085539 | 401.7 | -20.0 | -4.9 | 7238615b808d8f98 |
| `audio/sfx/item/unequip_shield_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip shield | 2441925575 | 311.3 | -20.0 | -5.16 | 0d3cb57570f7e3bc |
| `audio/sfx/item/equip_jewelry_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip jewelry | 796102248 | 480.0 | -20.0 | -8.8 | acfd160c2c5f92ae |
| `audio/sfx/item/unequip_jewelry_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip jewelry | 3811655205 | 411.6 | -20.0 | -11.87 | 60b3c717b425f37b |
| `audio/sfx/item/equip_belt_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | equip belt | 2734192328 | 351.3 | -20.1 | -3.76 | 5154f1893c4a667e |
| `audio/sfx/item/unequip_belt_01.ogg` | UI-01 | Synthesis (Python numpy/scipy) | Original, no third-party source | unequip belt | 2100067022 | 260.9 | -20.1 | -5.69 | 57f5a9c5e287efa9 |
| `audio/sfx/vendor/buy_01.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins counted into a leather purse | 4088232319 | 368.5 | -20.0 | -7.77 | 3e9ba6ce928230b8 |
| `audio/sfx/vendor/buy_02.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins counted into a leather purse | 3850048515 | 368.4 | -20.0 | -7.74 | 64b08e8adbe695aa |
| `audio/sfx/vendor/buy_03.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins counted into a leather purse | 1239721772 | 368.4 | -20.1 | -6.1 | 5317beff5002171e |
| `audio/sfx/vendor/sell_01.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins set on a wooden counter | 267251817 | 355.9 | -19.9 | -6.65 | eea70594ed85a3ef |
| `audio/sfx/vendor/sell_02.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins set on a wooden counter | 4122913910 | 368.5 | -20.0 | -8.46 | 7d25bd9fdfb27f43 |
| `audio/sfx/vendor/sell_03.ogg` | LT-10 | Synthesis (Python numpy/scipy) | Original, no third-party source | coins set on a wooden counter | 2862194694 | 358.3 | -20.1 | -7.96 | c1be5ffa62c58cb6 |
| `audio/sfx/ui/open_01.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel open | 1616083135 | 184.7 | -24.0 | -8.57 | baf2339a887a3962 |
| `audio/sfx/ui/open_02.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel open | 3811214582 | 184.3 | -24.0 | -6.85 | c7c36149a4099f54 |
| `audio/sfx/ui/open_03.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel open | 414619384 | 184.4 | -24.1 | -7.97 | ef98ee737b2b6394 |
| `audio/sfx/ui/close_01.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel shut | 919545486 | 200.0 | -23.9 | -7.13 | 704253408bda32eb |
| `audio/sfx/ui/close_02.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel shut | 1608766770 | 200.0 | -24.0 | -9.3 | ee8a6c5e713baece |
| `audio/sfx/ui/close_03.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | leather book panel shut | 3874638519 | 200.0 | -23.9 | -9.89 | 16ad59a05ba3bd49 |
| `audio/sfx/ui/click_01.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | bone/wood button tick | 1202174602 | 59.6 | -26.1 | -10.53 | f745c9594da11368 |
| `audio/sfx/ui/click_02.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | bone/wood button tick | 1808173206 | 59.6 | -26.1 | -10.19 | 844436b91e1bcf39 |
| `audio/sfx/ui/click_03.ogg` | UI-03 | Synthesis (Python numpy/scipy) | Original, no third-party source | bone/wood button tick | 3849409831 | 59.6 | -26.0 | -9.33 | a48a6c032dc92523 |
| `audio/sfx/ui/deny_01.ogg` | UI-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull descending click-thud pair | 474736939 | 240.0 | -23.9 | -10.47 | cda0e50c51ec0fa0 |
| `audio/sfx/ui/deny_02.ogg` | UI-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull descending click-thud pair | 4127899004 | 240.0 | -24.0 | -11.13 | 2821b86c6a5c28ef |
| `audio/sfx/ui/deny_03.ogg` | UI-02 | Synthesis (Python numpy/scipy) | Original, no third-party source | dull descending click-thud pair | 432314925 | 240.0 | -24.0 | -10.08 | 349e59bcc3bb65d8 |
| `audio/sfx/potion/health_01.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + deep gulps | 114715234 | 780.0 | -18.0 | -4.19 | 7dce156b68298bbe |
| `audio/sfx/potion/health_02.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + deep gulps | 3582472041 | 751.0 | -18.1 | -1.46 | 3c0b77576b605cef |
| `audio/sfx/potion/health_03.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + deep gulps | 189250734 | 780.0 | -18.0 | -3.16 | b8f647661527cdd1 |
| `audio/sfx/potion/mana_01.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + thinner gulps + low cold glow | 850279789 | 780.0 | -18.0 | -3.76 | 725eafccf64833a9 |
| `audio/sfx/potion/mana_02.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + thinner gulps + low cold glow | 291225639 | 768.5 | -18.1 | -2.67 | 9b93fd226e15e481 |
| `audio/sfx/potion/mana_03.ogg` | UI-05 | Synthesis (Python numpy/scipy) | Original, no third-party source | cork + thinner gulps + low cold glow | 408312902 | 780.0 | -18.1 | -2.53 | 3ba221ec5af14579 |
| `audio/sfx/player/level_up_01.ogg` | UI-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | rush + drone fifth + one dark bell strike | 3785016345 | 2450.0 | -15.8 | -1.45 | 236df2242c5b21ed |
| `audio/sfx/player/level_up_02.ogg` | UI-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | rush + drone fifth + one dark bell strike | 1160494489 | 2450.0 | -16.6 | -2.07 | e2a453abee699721 |
| `audio/sfx/player/level_up_03.ogg` | UI-06 | Synthesis (Python numpy/scipy) | Original, no third-party source | rush + drone fifth + one dark bell strike | 3867982847 | 2450.0 | -15.1 | -1.49 | 8e76f0761bbba770 |
