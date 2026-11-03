# PROVENANCE: monster deaths and dismemberment (skeleton crumble, demon spew, limb sever)

Generated 2026-11-02 for Sanctuary. **Every file is original synthesis**, made from scratch in Python (numpy/scipy):
resonant noise-impulse knocks (bone), grain crackle (crunch), pitch-dropping driven sine thumps (body and ground), time-varying band-passed noise (tear, slap),
rising-pitch sine bubbles and droplet-chopped band noise (blood), and the Klatt-style formant voice from `sfxlib.voice` (the demon throat gurgle).
No recordings, samples, sample libraries or third-party audio of any kind were used, including no CC0 material. No Diablo (or other copyrighted) audio was used; the "D2 skeleton collapse" note is a feel reference only.

License: original work created for the Sanctuary project. Ownership is Brian's (the project owner). No third-party license applies.

Reproduce: `python3 /workspace/sanctuary_audio/scripts/sfx/build_deaths.py` (deterministic, seeded per file from sha1("DEATHS:name:variant")).
Code: `sfxlib.py`, `deaths_sounds.py` (designs), `build_deaths.py` (render, normalize, encode, verify), `finalize_deaths.py` (montage, provenance).

Format: Ogg Vorbis (libvorbis via libsndfile), 44.1 kHz mono. Loudness was normalized (BS.1770, whole file) and peaks limited to ≤ −1 dBTP (4× oversampled, measured on the decoded Ogg).
Each file has 1.5 ms of leading silence, a 1.5 ms fade-in, a 10 ms fade-out, and a 6 ms fade on every internal layer. Event times below include the leading silence.

| File | Method | Source / license | Design | Event times (s) | Seed | Length ms | LUFS | dBTP | SHA-256 (16) |
|---|---|---|---|---|---|---|---|---|---|
| `audio/sfx/monster/skeleton_death_crumble_01.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | dry crack, buckling clatter, pile hits ground (crunch + many hollow bone knocks), skull thunk, thinning rattles, last rolling bone | ground_impact 0.299 s, skull_thunk 0.360 s | 1188341941 | 1250.2 | -19.7 | -1.35 | 728628a4ba147251 |
| `audio/sfx/monster/skeleton_death_crumble_02.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | dry crack, buckling clatter, pile hits ground (crunch + many hollow bone knocks), skull thunk, thinning rattles, last rolling bone | ground_impact 0.351 s, skull_thunk 0.431 s | 2824666838 | 1306.4 | -20.2 | -1.56 | 474791076358a64b |
| `audio/sfx/monster/skeleton_death_crumble_03.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | dry crack, buckling clatter, pile hits ground (crunch + many hollow bone knocks), skull thunk, thinning rattles, last rolling bone | ground_impact 0.280 s, skull_thunk 0.359 s | 2309813924 | 1232.7 | -21.0 | -2.02 | 663eb192a743e751 |
| `audio/sfx/monster/demon_death_spew_01.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | gurgling throat (formant synth, heavy fry) + bubbles + wet spray and spatter, knees, heavy face-down body thud, wet squish, settle | body_thud 1.133 s, spew_end 0.746 s | 1780623394 | 1711.5 | -16.9 | -1.33 | 7528fd4bb4918f3c |
| `audio/sfx/monster/demon_death_spew_02.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | gurgling throat (formant synth, heavy fry) + bubbles + wet spray and spatter, knees, heavy face-down body thud, wet squish, settle | body_thud 1.143 s, spew_end 0.720 s | 1586026871 | 1721.3 | -17.0 | -1.11 | 2de552aee8c1197d |
| `audio/sfx/monster/demon_death_spew_03.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | gurgling throat (formant synth, heavy fry) + bubbles + wet spray and spatter, knees, heavy face-down body thud, wet squish, settle | body_thud 1.030 s, spew_end 0.604 s | 1789014327 | 1598.7 | -17.1 | -1.55 | 2be07592af7668d8 |
| `audio/sfx/impact/limb_sever_01.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | meaty chop + bone snap, wet stretching tear with bubbles, blood spray and droplets, limb lands | limb_land 0.448 s | 3679553806 | 607.3 | -17.9 | -1.69 | 8ceff87727139758 |
| `audio/sfx/impact/limb_sever_02.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | meaty chop + bone snap, wet stretching tear with bubbles, blood spray and droplets, limb lands | limb_land 0.440 s | 516961683 | 599.6 | -19.0 | -1.85 | c6c636b55473f55a |
| `audio/sfx/impact/limb_sever_03.ogg` | Synthesis (Python numpy/scipy) | Original, no third-party source | meaty chop + bone snap, wet stretching tear with bubbles, blood spray and droplets, limb lands | limb_land 0.331 s | 2422487696 | 544.6 | -17.6 | -1.5 | aa12767cfd3a29b8 |
