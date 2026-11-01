# Sanctuary: why the audio sounds choppy, crackly or clicky

Investigation date: Sun Nov 1, 2026, about 10:15 EST (America/Detroit). Read-only. Nothing on the site or in any repo was changed.
Game: https://gold-iris-zippy-bird.grok.me
Live bundle checked: **`assets/routes-DWORE8MA.js`** (+ `assets/index-rnn4x2SB.js`). This is the Stage 12B build, and it is byte-identical to `/workspace/sanctuary/live_12bf/routes-DWORE8MA.js`.
Line numbers below refer to the beautified copy `/workspace/sanctuary/audio/inv/routes.pretty.js` (prettier 3). The minified names are the same as in the A1 FACTS (`hl` = audio class, `dl` = music manager, `sl` = level table, `ul` = ramp helper, `ll` = loader).
Uncertain items are marked [?].

---

## 1. Summary

- **Stage A1 is NOT live.** No second compressor or limiter, no `peakVoices`, no `[a1]` log, no `loopStart`/seam crossfade, no `setTargetAtTime`, no `+ 0.02` lead in hit(), and voices still hard-stop. Every A1 cause is still present in the live code.
- **A1's FACTS cite a stale bundle name** (`routes-_LaUNfst.js`). The audio code is unchanged in `routes-DWORE8MA.js`, and all of A1's anchors still match, so A1 can run as written. Only the file name in FACTS is out of date.
- I rendered the live audio code offline in headless Chrome 156, using the real Web Audio DSP, the real `.ogg` files and a scripted 8-foe AoE fight with rain, wind and fire. Results:
  - **No hard clipping in Chrome.** Output peak was -0.5 dBFS with 0 samples over full scale. The pre-compressor master just touches +0.5 dBFS.
  - **The compressor pumps hard.** During a fight its gain swings about 5.5 dB (p5 to p95), moving about 1.7 dB per 20 ms on average, so the music and rain duck and swell under every hit. A1's extra limiter makes this a little *worse* (6.6 dB swing, 2.5 dB per 20 ms).
  - **There is a periodic hole in the town music:** about 80 ms at -8 dB every 44.4 s, at the loop point, caused by the generated bass hum. A1 does not touch it, and it is still there in the A1 simulation.
- The biggest new causes, which A1 does not address:
  1. **Music stems start at different times.** Each loop calls `start()` whenever its own file finishes downloading and decoding, and the hum starts even later. The layers play out of time with each other for the whole session. This is the most likely reason the *music* feels choppy or lurching [? perceptual: the size of the offset depends on network and decode timing].
  2. **The bass hum has a fade-out and fade-in baked into its loop**, so the bass bed dips to near silence for about 0.1 s every 44.4 s (measured above).
  3. **No `latencyHint`** (the default "interactive" uses the smallest buffers), plus a **~170 ms main-thread stall** when the hum is generated. Both are dropout risks on a busy WebGL frame [? device-dependent].
  4. **Compressor pumping** (fast 4 ms attack, makeup gain, music and sfx share one compressor).
  5. Smaller click sources: hit envelopes jump instantly to full level, voice files end mid-waveform (A1 only fades the start), and breath() allocates a buffer per call.

---

## 2. Is A1 live? (Task 1)

| A1 item | Searched for in live bundle | Found? |
|---|---|---|
| Limiter -3 / 0 / 20 / .001 / .1 | `createDynamicsCompressor` count, `threshold.value = -3`, `ratio.value = 20` | **No.** There is exactly 1 compressor (-16/8/2.4/.004/.18, line ~32745) |
| master 0.8, music 0.7 | `n.gain.value = +!this.muted`, `r.gain.value = 0.82` | **No.** Still 1 and .82 (32745–32750) |
| delayFeedback .35 / wet .45 / near .32 | level table `sl` (32000) | **No.** Still .48 / .66 / .462 |
| loopNoise seam crossfade | `loopStart`, `loopEnd` | **No.** 0 hits. loopNoise (33539) loops the raw 2 s buffer |
| cached gate/gasp buffers | gate (33095), gasp (32854) | **No.** Still `createBuffer` per call |
| `voices`, `peakVoices`, `track()`, 24-voice cap | `peakVoices`, `[a1]` | **No.** 0 hits |
| hit window 100 ms / cap 3 | `hitStamp > 80`, `hitN >= 4` | **No.** Still 80 / 4 |
| +0.02 lead | hit(): `let o = n.currentTime + a` | **No.** Only greet() already has +0.02 |
| mute setTargetAtTime | toggleMute (32794) | **No.** `setValueAtTime` (instant) |
| voice fade, no hard stop | speak() (32123–32135) | **No.** `this.voiceSrc?.stop()` |
| stop inactive zone loops | setZone (32108) | **No.** It ramps bus gains only, and all loops run forever |

Also absent from both bundles: `ScriptProcessor`, `AudioWorklet`, `latencyHint`, `suspend(`, `HTMLAudioElement`/`new Audio(`. There is one `AudioContext`, created in unlock() (32735) as `new e()` with no options.

---

## 3. A1 causes, verified against the live code (Task 2)

| A1 cause | Live code | Verdict |
|---|---|---|
| No limiter, levels sum past full scale | 1 soft compressor; master 1, music .82 | **Present.** In my Chrome simulation the pre-compressor sum reached +0.47 dBFS in an 8-foe AoE fight. The compressor's output stayed at -0.5 dBFS with 0 overs, so in Chrome this is *near*-clipping, not constant clipping. With more foes, louder rites or other browsers it can go over [?]. |
| loopNoise step every 2 s | 2 s random-walk buffer, `loop = true`, no fade | **Present.** This is a periodic tick in rain and wind. |
| gate/gasp allocate per call | `createBuffer` + `Math.random` per call | **Present.** It creates GC pressure, so it counts as jank, not a direct click. **A1 misses breath() (33496), which does the same.** |
| No global voice cap | only per-type windows | **Present.** My simulation peaked at about 19 one-shot voices plus about 12 loop sources [? the `ended` counting is approximate]. |
| One-shots at `currentTime` | hit, swish, rite, beast, ching… | **Present.** When the main thread is late, the attack gets cut (a click or flam). |
| Instant mute / hard voice stop | setValueAtTime, `voiceSrc.stop()` | **Present.** Clicks. |
| Inactive-zone loops always running | setZone ramps buses only; town + wild + dread all decoded and playing | **Present.** About 110 MB of decoded PCM at 48 kHz [?], plus constant mixing cost. |
| Delay feedback/wet too high | .48 / .66 / .462 vs guitarDry .28 | **Present.** See N5: the wet signal is louder than the dry. |

---

## 4. Measurements

### 4a. Audio files (all 22 live files re-downloaded, byte-identical to `../live_files`, served as `audio/ogg`, all Vorbis)

| File | Format | Notes |
|---|---|---|
| town/guitar, nylon, woodwind | 22.05 kHz mono, 40 kbps nominal | exactly 44.4 s; start and end on exact zeros; **2.2 s / 2.2 s / 5.05 s of leading silence, 1.39 / 1.14 / 2.47 s trailing**; seam clean |
| town/cimbalom | 22.05 kHz mono | zeros, 2.2 s lead, 5.4 s trail; **never loaded by the code** |
| town/pad | 22.05 kHz mono | edges about -0.07 (DC-ish), seam step ratio 2.7 vs median (inaudible) |
| town/clockwork | 22.05 kHz mono | seam ratio 1.6 (fine) |
| wild/drone | 22.05 kHz mono, 60 s | seam step 0.004 (≈ -48 dBFS) vs median step 0.0006: tiny, inaudible after bus gains [?] |
| wild/hollow, metal | 60 s | seams clean |
| dread/overworld | 16 kHz stereo, 66.0172 s | starts and ends mid-signal, but the seam prediction error is 0.001 vs a median step of 0.005 (clean). -20.4 LUFS, -8.0 dBTP |
| voice/* (12 files) | short | **many start or end mid-waveform:** f/hello first sample -0.145, f/hey -0.140, f/hm -0.255 (ends -0.271), m/hey -0.237, m/hello -0.173, m/hm -0.269 (ends -0.145), m/news ends -0.088, m/speak ends -0.098, f/yes ends -0.017. DC offset is small (≤ 0.007). |

- Lengths are exact multiples (2,131,200 / 2,880,000 samples at 48 kHz), so **there is no Vorbis padding gap at any seam.**
- **No file clips.** Peaks are -8 to -13.8 dBFS.
- The sample rates (16 / 22.05 kHz) are resampled once by decodeAudioData, so there is no runtime resampling cost and no rate-mismatch artifact. They only sound dull, with no content above 8–11 kHz. **Not a crackle cause.**

### 4b. Offline render of the live audio code (headless Chrome 156, OfflineAudioContext 48 kHz)

Harness: `/workspace/sanctuary/audio/inv/harness/` and `inv/run_harness.js`. The live `sl`…`hl` code (lines 32000–33560) runs *verbatim*. `performance.now` is mapped to the audio clock so the rate limits behave as they do in real time. The fight script fires an AoE rite every 0.6 s hitting 8 foes (hit + beast each), a player swish every 0.35 s and enemy hits every 0.5–0.9 s, with rain .34, wind .22 and the fire on. The "A1" rows apply A1 steps 1 and 4 (limiter, levels, delay, hit window) to the same code.
Results: `inv/sim_results*.json`.

| Scenario | Output peak | Samples > 1.0 | Pre-comp peak | Comp gain swing (p5–p95) | Mean gain change per 20 ms |
|---|---|---|---|---|---|
| Town idle (music + rain + wind + fire) | -6.2 dBFS | 0 | -9.2 | n/a (net **+4.1 dB** makeup) | n/a |
| Town fight, live | **-0.5 dBFS** | 0 | **+0.47** | **5.5 dB** | **1.7 dB** |
| Town fight, A1 | -1.2 dBFS | 0 | -2.6 | 6.6 dB | 2.5 dB |
| Dread fight, live | -1.2 dBFS | 0 | +0.02 | n/a | n/a |
| Dread fight, A1 | -0.9 dBFS | 0 | -1.9 | n/a | n/a |

**Town music seam (music only, 20 ms RMS around t = 44.4 s), live:**

```
-20 -18 -17 -19 -17 -18 -20 -15 [-23 -27 -23 -25] -18 -18 -20 ...   (median -18 dB)
```

With A1 it is still `-21 [-26 -24 -28 -26] -17`.

- Almost all of the town mix energy is below 200 Hz, so the hum/bass dominates it and also drives the compressor.
- humUnder generation timing, same JS loop in Node on this box: **~170 ms** for 2.13 M samples (48 kHz). That is a one-off main-thread block, likely 300–600 ms on a phone [?].
- At the end of the buffer, the hum oscillator's phase is 0.30 rad (fundamental) and 0.15 rad (sub) away from a whole cycle, so simply removing the fades would leave a click. It needs a crossfade.

---

## 5. Other things I checked (Task 3)

| Suspect | Finding | Verdict |
|---|---|---|
| All loops at gain 0 | Yes: town (5 stems + hum + 2 delay lines), wild (3), dread (1) all run forever | A1 step 7 covers it. **But A1 step 7 must also cache the hum AudioBuffer**, otherwise every return to town re-runs the 170 ms generation, **and it must restart a group's stems with one shared start time** (see N1). |
| Main-thread jank | Per-frame: setMood, setFire, pump, setWeather (0.03 threshold), tickGasp (80573–80585). These are cheap. The real spikes are the humUnder generation (170 ms) and per-call `createBuffer` in gate, gasp and breath (GC). | New: N3 and N8 |
| ScriptProcessor / AudioWorklet | none | not a cause |
| Compressor pumping/distortion | 4 ms attack, 180 ms release, about +5.6 dB auto-makeup [?Blink formula], music and sfx share it; measured 5.5 dB swing | New: N4. A 4 ms attack is shorter than one cycle of 65–117 Hz bass, so it can distort the bass [?]. |
| `.value` jumps (zipper) | toggleMute (A1 covers it). applyGale() is called **every frame during the intro** (80585 → 32828/32848): cancel + setValueAtTime(current) + 0.9 s ramp, re-issued per frame; setWeather also ramps windGain | Minor [?]: N9 |
| Oscillators without envelopes | Every one-shot has a decay. **Attacks are instant** (`setValueAtTime(peak)`) in flesh tri .08·t (33218), cling tri .12·t (33235), heavy sine .42·t (33251), slash tri .16·t, crunch sine .5·t + noise .32·t (33299/33310), contact sine .28·t + noise .18·t (t ≤ 1.3) | New: N6. Clicks on hits, up to about 50 per second (4 per 80 ms) |
| exponentialRamp to 0 | none (floors are 1e-4 or 2e-4) | not a cause |
| Sample-rate mismatch | decode resamples once, and the hum uses ctx.sampleRate | not a cause |
| Ogg seam padding | exact lengths, seams clean (4a) | not a cause (drone step negligible [?]) |
| latencyHint | not set, so the default "interactive" (smallest buffer) | New: N3 [?] |
| iOS/Safari Ogg | Ogg Vorbis decodeAudioData is unsupported on older iOS/Safari [? version, brief says 18.4]. The loader returns null and that layer is just **silent**, not choppy | N10, needs a device check |
| Feedback delay build-up | Each delay feeds back only into itself (not true ping-pong). The loop gain .48 with a 1200 Hz lowpass is stable (DC gain 1/(1-.48) ≈ 1.92×). Wet .66 ×2 vs dry .28 | No runaway, but it is a smeary, muddy wash. A1 step 1 reduces it, and N5 goes further |
| Voice count | about 19 one-shots + 12 loops at peak in the simulation [?] | A1 step 4 |
| **Stem start sync** | `loop()` (32141) and wireTown (32172) call `src.start()` with no time **inside each file's own fetch/decode `.then`**; humUnder starts after the guitar and after 170 ms of generation | **New: N1** |

---

## 6. New causes, ranked by impact

Impact classes: **[S]** stutter, dropouts or out-of-time feel · **[C]** crackle, distortion or pumping · **[K]** clicks.

| # | Class | Cause | Evidence | Confidence |
|---|---|---|---|---|
| N1 | S | Music stems and hum start at unrelated times (per-file decode completion), so the layers stay out of time all session | 32141–32152, 32172–32196, humUnder start at 32248 | Code: certain. Audibility: likely, the offset varies [?] |
| N2 | S | Hum loop has 50 ms fade-in/out baked in, causing an ~80–100 ms bass hole every 44.4 s | 32235–32239; measured -8 dB dip at 44.36–44.44 s; A1 does not fix | certain |
| N3 | S | latencyHint default "interactive" with heavy WebGL load, causing audio underruns; plus the 170 ms humUnder main-thread stall; 20 ms lead is short for frame hitches | 32735; measured 170 ms | device-dependent [?] |
| N4 | C | Shared compressor with 4 ms attack and auto-makeup pumps the music and rain under every hit (5.5 dB swing); A1's limiter adds to it | sim table 4b | measured (Chrome) |
| N5 | C | Delay wet (.66 L + .66 R) well above guitar dry (.28), long feedback tail: a muddy, "crackly" smear on the guitar | sl table 32000, delaySend 32154 | certain (code); taste [?] |
| N6 | K | Instant attacks on hit oscillators and noise | lines in §5 | certain |
| N7 | K | Voice files end mid-waveform; A1 only fades the start | 4a | certain |
| N8 | S (minor) | breath() allocates a noise buffer per call (A1 only fixes gate and gasp); the hum buffer needs caching if A1 step 7 recreates the town group | 33496 | certain |
| N9 | K (minor) | applyGale re-issued every intro frame (cancel + set + ramp) | 80585, 32848 | [?] |
| N10 | silence | Ogg decode failure on older iOS/Safari leaves layers missing | loader 32061 | [?] |

**Not causes:** ScriptProcessor, exponential ramp to 0, sample-rate mismatch, Vorbis padding, file clipping, delay runaway.

---

## 7. Proposed STAGE A2 addendum

The A2 text below can be pasted as-is. Run it **after A1** is built and published; it assumes A1's changes are already in.

```
STAGE A2 - Audio de-chop: stem sync, hum seam, latency, gentler dynamics, attack ramps

Goal: Remove the remaining choppy and lurching music, the periodic bass dropout, the hit and voice clicks and the pumping that A1 does not cover. Start every music group's stems together on one shared clock. Make the generated hum loop seamless. Ask for a larger audio buffer. Stop the music ducking under every hit. Add 2-3 ms attack ramps to hit tones. Fade voice-file endings. Sound design, music choice and which sounds play when stay as they are.

RULES
- New features are 3D only. Do not touch any 2D drawing code.
- Audio code is not drawing code; this stage edits only the audio class and its music manager.
- If a step fails twice, stop and report. No retry loops. Build once, check the console, publish.
- Be strict: change only what is listed.
- Keep a single AudioContext. No new audio files, no new dependencies.
- A1 must already be live. If the `[a1]` log is missing, stop and report.

FACTS (verified in live bundle routes-DWORE8MA.js, pre-A1; minified names may differ in source, so find them by the anchors)
- Audio class (minified hl). unlock() creates the context with `new e()` (no options), where `let e = window.AudioContext || window.webkitAudioContext`. Compressor: `l.threshold.value = -16, l.knee.value = 8, l.ratio.value = 2.4, l.attack.value = .004, l.release.value = .18`. The music bus feeds master, which feeds the compressor.
- Music manager (minified dl), anchored by `delayWet = []`, `voices = new Map`.
  - loop(path, bus, gain) creates a GainNode, then inside `ll(ctx, path).then(buf => ...)` creates a looping BufferSource and calls `start()` with no time. Each stem therefore starts whenever its own file finishes decoding.
  - wireTown(): the guitar source starts inside its own `.then` (with `a.start(), this.humUnder(n.duration)`). nylon, pad, woodwind and clockwork use loop(). wireWild(): drone, hollow, metal use loop(). All stems in a group have the same length (town 44.4 s, wild 60 s).
  - humUnder(len) builds a mono buffer of len*sampleRate samples in a JS loop (~170 ms on desktop) with `l = Math.floor(.05 * n)` and `t < l ? f = t / l : t > r - l && (f = (r - t) / l)`. That is a 50 ms fade-in AND fade-out at the buffer edges, so the bass drops out for ~0.1 s every loop. The phase at the end is not a whole cycle (0.30 rad off), so the fades cannot simply be removed. It then goes through a lowpass at 170 Hz and a gain of .3 into the town bus, and starts with `f.start()`.
- One-shot hit helpers start tones at full level: `gain.setValueAtTime(PEAK, e)` then `exponentialRampToValueAtTime(1e-4, ...)` in flesh (`.08 * t`), cling (`.12 * t`), heavy (`.42 * t`), slash (`.16 * t`), crunch (`.5 * t` sine and `.32 * t` noise), contact (`.28 * t` sine and `.18 * t` noise).
- Voice files (voice/female/*.ogg, voice/male/*.ogg) end mid-waveform (e.g. male/hm ends at -0.145, male/speak at -0.098, female/hm at -0.271).
- breath(e, t) allocates a new noise buffer each call, like gate and gasp did before A1.
- applyGale() is called every frame during the intro via `this.intro && this.audio.setGale(this.introGale())`. Each call cancels and re-ramps windGain.

STEPS
1. Bigger audio buffer. In unlock(), create the context with `new e({ latencyHint: 'playback' })`. If that throws, fall back to `new e()`. Log once: `[a2] sampleRate=<n> baseLatency=<s> outputLatency=<s>`.
2. Stems start together. In the music manager, load each group's buffers with Promise.all (town: guitar, nylon, pad, woodwind, clockwork; wild: drone, hollow, metal). When all are decoded (skip any that return null), build the hum buffer (town only), then compute ONE `when = ctx.currentTime + 0.1` and call `start(when)` on every source of that group, the hum included. Keep loop() creating its GainNode synchronously as today, so that callers that keep the returned gain (nylonGain) still work. Use the same shared-`when` start whenever A1 step 7 recreates a group.
3. Seamless hum. In humUnder(): remove the edge-fade factor (f = 1 always). Generate N = floor(0.05*sampleRate) extra samples past the end (len + N total, same formula, continuing the phase). Then for i in 0..N-1: a[i] = a[i]*sin(x) + a[len+i]*cos(x), with x = (i/N)*PI/2, and keep only the first len samples in the buffer. Build the buffer once and keep it on the manager (this.humBuf). A1 step 7 must reuse it instead of regenerating it.
4. Gentler dynamics. Compressor: attack .004 → 0.012, release .18 → 0.25, threshold -16 → -14. Route the music bus straight into A1's limiter instead of into master → compressor (music = 0.7 → limiter), so hits no longer duck the music. Sfx and rain/wind stay on master → compressor → limiter. Mute must still silence music: apply the A1 mute fade to the music bus as well. Because the music no longer gets the compressor's ~+4 dB makeup gain, raise the music bus 0.7 → 1.0 [? adjust by ear].
5. Attack ramps on hits. In flesh, cling, heavy, slash, crunch and contact, replace each `gain.setValueAtTime(PEAK, e)` with `gain.setValueAtTime(1e-4, e)` + `gain.exponentialRampToValueAtTime(PEAK, e + 0.003)`. Keep the existing decay ramp after it, and move its start so that it begins after the attack ends (e + 0.003). Peaks and decay end times stay unchanged.
6. Voice end fade. In speak(), on the per-voice GainNode A1 added, also schedule `setValueAtTime(1, when + dur - 0.015)` and `linearRampToValueAtTime(0, when + dur)`, where dur = buffer.duration.
7. Cached breath noise. Build breath()'s noise buffer once on first use (the longest length it needs) and reuse it. Same content and gains.
8. Intro wind. In setGale()/applyGale(), skip the re-ramp when |newTarget - lastTarget| < 0.01 (store lastTarget).
9. Build once, check the console, publish.
10. TEST (live, 3D view on, real device + headphones; one desktop Chrome run and one phone run, iOS Safari if available):
   - Load into Martsirt and stand by the bonfire for 90 s. Expect the guitar, nylon, woodwind and hum to sit in time, and no bass dropout at ~44 s or ~89 s.
   - Fight a group with an AoE skill for 60 s. Expect the music level to stay steady (no ducking per hit) and no clicks at hit onsets.
   - Trigger 3 NPC greetings. Expect no click at the start or end.
   - Leave town and come back. Expect the town stems to restart in time with each other and no hitch.
   - Report the `[a2]` log line, the highest `[a1] peakVoices`, and any audio decode errors (null buffers).

REPORT
One line per step: STEP n - done / failed (reason). Then console errors (if any) and files changed.
```

---

## 8. Needs Brian's input

1. **Real-device listening test.** Headless rendering can measure levels but cannot hear dropouts or underruns. N3 (latencyHint) is a trade-off: "playback" can add roughly 20–40 ms+ of input-to-sound delay [?], which is fine for this game but noticeable on hit sounds.
2. **Which browser and device the choppiness happens on.** If it is iOS Safari: are some layers silent (Ogg decode failure, N10)? That may need m4a/AAC fallbacks, which would mean new files and break the "no new audio files" rule.
3. **Has A1 been sent to Grok Build yet?** It is not live. A2 assumes A1 lands first. A1's FACTS cite `routes-_LaUNfst.js`; the current build is `routes-DWORE8MA.js`, but the anchors still match.
4. **Music taste calls:** is the 2.2 s of leading silence in the guitar and nylon stems (and 5 s in woodwind) intentional phrasing? Should the guitar delay wash stay as heavy as it is (N5)? Also, `town/cimbalom.ogg` is shipped but never used.
5. Reconcile with the "Tristram song feel" music request: A2 does not change the composition, only the timing and mixing.
