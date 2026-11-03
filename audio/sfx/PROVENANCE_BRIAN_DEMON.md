# PROVENANCE: Brian's demon vocalizations (red demons)

**Source:** Brian D. B.'s own recording, a Samsung Notes voice memo. He performed and recorded it himself, so it is first-party audio and cleared to ship. No third-party, library or AI-generated audio is used. The demon versions are DSP transforms of the same recording.

- Container: `01M6HR1733KA1048JKKGCXH15B.sdocx` (Samsung Notes), embedded audio `raw_0.m4a`
- `raw_0.m4a`: 23.7 s, 48 kHz mono AAC, md5 `dff6161aa588587a68f986e69ef5cabd`, sha256 `916a1740dfd9da2ee21c784dadd388b45217b78d56282a82fcdb4825fa174df7`
- Owner note: "Some demon noises and demon breathing… it will have to be turned up and at the very beginning background noise to be removed… couple random noises, breathing, red demons"

## Processing chain (`scripts/sfx_brian_demon/build.py`)
1. Decode to 48 kHz float, then a 60 Hz 4th-order highpass.
2. De-plosive: dynamic gain on the band below 160 Hz only (threshold -50 dB, about 5:1). This tames breath-on-mic pops.
3. Stationary spectral NR (noisereduce). Profile: 0.32–0.68 s (noise-only opening). prop_decrease 0.8, n_std 1.5, n_fft 2048, freq smoothing 400 Hz, time smoothing 64 ms.
4. Resample to 44.1 kHz, then a gentle downward expander (ratio 2, max 10 dB) for pauses.
5. **Demon version:** rubberband -4 st, formants shifted (not preserved). Plus an octave-down layer (LP 1.2 kHz, -12 dB) and a 150–2500 Hz ring-mod (~38 Hz flutter) tanh grit layer (-14 dB). EQ: +2 dB low shelf at 130 Hz, +3 dB at 240 Hz, -4 dB high shelf at 8.5 kHz. Then HP 45 Hz, LP 11 kHz (2nd order) and peak soft-saturation.
6. Slicing: per-slice loudness normalize (growls -18 LUFS, breaths -21 LUFS), then a 4x-oversampled lookahead limiter. 1.5 ms lead silence, 1.5 ms fade-in, fade-out of min(40 ms, 15%). Ogg Vorbis q6, 44.1 kHz mono. Re-encode loop until the decoded true peak is ≤ -1.0 dBTP.
7. Start noise (0–1.04 s: silence, noise floor, record-button handling bump) is trimmed. The full takes run from 1.04 s and are normalized to -23 LUFS.

Reproduce: `/workspace/venv_demon/bin/python scripts/sfx_brian_demon/build.py`, then `qa.py`.

## Slices (times in seconds in the original m4a)

| file | src | description | gain dB | LUFS | dBTP | est. noise floor dBFS | sha256 |
|---|---|---|---|---|---|---|---|
| `full/brian_demon_take_clean_natural.ogg` | 1.04–end | full cleaned take | +28.6 | -24.2 | -1.45 | -61.7 | `1b2fdb68b857795a` |
| `full/brian_demon_take_demon.ogg` | 1.04–end | full cleaned take | +30.9 | -24.8 | -1.38 | -62.8 | `fc3b14f5299447d5` |
| `audio/sfx/monster_natural/demon_growl_01.ogg` | 1.20–2.46 | raspy breathy "hhrraah" (formants ~1k/2k/4k) into a hissing tail, breath pop at 2.1 s | +27.4 | -19.6 | -1.55 | -62.9 | `f650b47b86afe9b9` |
| `audio/sfx/monster/demon_growl_01.ogg` | 1.20–2.46 | raspy breathy "hhrraah" (formants ~1k/2k/4k) into a hissing tail, breath pop at 2.1 s | +29.5 | -20.0 | -1.44 | -64.2 | `63b6c6281826933d` |
| `audio/sfx/monster_natural/demon_growl_02.ogg` | 4.56–5.78 | long breathy roar-rasp "hhhaaah", clear vowel formants (~0.8/1.5/2.5/4 kHz), decaying | +34.0 | -18.3 | -1.99 | -56.3 | `5097b50c220bdf01` |
| `audio/sfx/monster/demon_growl_02.ogg` | 4.56–5.78 | long breathy roar-rasp "hhhaaah", clear vowel formants (~0.8/1.5/2.5/4 kHz), decaying | +38.1 | -18.3 | -1.61 | -55.6 | `6c3fd6af33e798d3` |
| `audio/sfx/monster_natural/demon_growl_03.ogg` | 7.02–7.52 | short sharp snort/hiss burst "HAH!" (snarl hit) | +30.9 | -18.5 | -1.96 | -59.4 | `96cc563ddd62d620` |
| `audio/sfx/monster/demon_growl_03.ogg` | 7.02–7.52 | short sharp snort/hiss burst "HAH!" (snarl hit) | +35.9 | -18.7 | -1.12 | -57.8 | `1e9ae1fd55bee440` |
| `audio/sfx/monster_natural/demon_growl_04.ogg` | 7.54–9.14 | longest phrase: pulsed rattling rasp 7.95-8.6 s (most growl-like), then breathy tail | +33.4 | -18.5 | -1.18 | -56.9 | `a09d7d36ac8458f4` |
| `audio/sfx/monster/demon_growl_04.ogg` | 7.54–9.14 | longest phrase: pulsed rattling rasp 7.95-8.6 s (most growl-like), then breathy tail | +39.8 | -21.1 | -1.45 | -53.9 | `23cdf406e0e7c030` |
| `audio/sfx/monster_natural/demon_breath_01.ogg` | 5.80–6.28 | quick hissing inhale, pure high band (no vowel) | +38.1 | -21.1 | -6.3 | -52.2 | `fce83b5ff38eeca8` |
| `audio/sfx/monster/demon_breath_01.ogg` | 5.80–6.28 | quick hissing inhale, pure high band (no vowel) | +53.0 | -21.2 | -7.83 | -40.7 | `1237780b125a1258` |
| `audio/sfx/monster_natural/demon_breath_02.ogg` | 9.20–9.54 | short hiss breath, high band only | +40.8 | -21.3 | -8.67 | -49.5 | `cf3b468112e7aa0a` |
| `audio/sfx/monster/demon_breath_02.ogg` | 9.20–9.54 | short hiss breath, high band only | +55.5 | -21.3 | -5.47 | -38.2 | `dbd2494bd90b8cbb` |
| `audio/sfx/monster_natural/demon_breath_03.ogg` | 10.30–10.90 | heavy exhale "HHAH" with a vowel flash at 10.72 s and a small breath pop | +30.9 | -21.2 | -3.52 | -59.4 | `01cd60614bc1d8da` |
| `audio/sfx/monster/demon_breath_03.ogg` | 10.30–10.90 | heavy exhale "HHAH" with a vowel flash at 10.72 s and a small breath pop | +35.9 | -21.2 | -1.75 | -57.8 | `7ef964778533c9b6` |
| `audio/sfx/monster_natural/demon_breath_04.ogg` | 11.36–11.68 | small quiet inhale hiss | +45.4 | -21.3 | -5.48 | -44.9 | `7aa9c1d8529a6002` |
| `audio/sfx/monster/demon_breath_04.ogg` | 11.36–11.68 | small quiet inhale hiss | +58.6 | -21.2 | -6.36 | -35.1 | `4e8a7314f820f164` |
| `audio/sfx/monster_natural/demon_breath_05.ogg` | 11.78–12.95 | exhale "hhhaa" (high hiss into vowel), soft grumbling tail | +38.2 | -21.7 | -2.21 | -52.1 | `c0ad4ff82726aab9` |
| `audio/sfx/monster/demon_breath_05.ogg` | 11.78–12.95 | exhale "hhhaa" (high hiss into vowel), soft grumbling tail | +44.2 | -21.4 | -1.62 | -49.5 | `35d8d56e63b9fae0` |

Rejected regions (mic and handling noise, no usable voice): 0.70–0.86 (handling bump), 2.46–3.34 (breath rumble and thump), 13.3–21.0 (silence and ticks), 21.05–21.72 (rumble and thump), 21.98–22.27 (faint hiss), 22.93–23.15 (stop handling bump).

## Quality notes
- Raw level is very low, so slices needed +27 to +51 dB of gain. After NR, the pause floor is about -90 dBFS before gain. The estimated floor after gain is in the table.
- The material is mostly unvoiced (about 10% voiced frames). The 'growls' are formanted rasps, not pitched growls. They are best layered under a pitched or synthetic roar for big hits.
- breath_01/02/04 are mostly a 12–19 kHz breath fizz with little body. They are marginal, especially the demon versions (floor SNR about 14–20 dB). Use them quietly or as layers only.
- A mouth-click transient at about 1.8 s (growl_01) and 8.4 s (growl_04) survives pitch shifting. It is softened by the 11 kHz LP but is still faintly audible.

## Shipped to repo (2026-11-03)
Approved by Brian. Demonized versions only. Repo name <- source slice:
- demon_growl_01..04.ogg <- demon_growl_01..04
- demon_breath_01.ogg <- demon_breath_03 (heavy exhale)
- demon_breath_02.ogg <- demon_breath_05 (exhale w/ grumble)
Dropped: source breath_01, 02, 04 (thin, low SNR).
