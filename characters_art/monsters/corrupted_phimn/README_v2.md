# corrupted_phimn_feral_lod15k_v2.glb

This is a copy of `corrupted_phimn_feral_lod15k.glb` (used by the brute, bear and melakir kinds) with one new clip added. The original file and `notes.md` are unchanged.
The 7 original clips (attack_claw, attack_pounce, death, hit, idle, run, sniff) are copied **byte-for-byte** from the live
file. They are still keyed at 24 fps, with the same keyframes and durations, so their loops stay exact. The new clip is keyed at 30 fps and is in place.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| attack2 | 39 | 1.267 | **frenzy swipe**: rears up from the crouch 0–9 (right claw raised by 9), **hit 1: right swipe at frame 12**, left claw winds up 14–16, **hit 2: left swipe at frame 18**, right claw winds up 20–22, **hit 3: right swipe at frame 25**, holds 26–30, then drops back to the all-fours idle pose 31–38 |

- Use the hit frames 12 / 18 / 25 for damage ticks and claw-whoosh SFX. A good fit is the 3-hit secondary attack, or `attack2` in monsters_3d.json (not edited here).
- Frame 0 matches attack_claw frame 0, and the last frame matches attack_claw's last frame, which is the crouched idle stance.
- The hips lunge forward about 9 cm by hit 3 and return to 0 at the end. The lowest skinned vertex is −0.08 m during the swipes (claw tips).

Source / licence
- This is derived from the monster's **own live `attack_claw`** clip: source frames 0–15, then an X-mirrored copy of 7–15 (the left-hand swipe), then 7–15 again, then 16–end.
  These are joined with 3-frame crossfades, with a Spine2 twist and hip-lunge layer added by script. No outside animation was used, so this is original project work.
- Searched first: there is no unarmed claw-flurry clip in the Mixamo library on the box, and the Quaternius CC0 monster packs use different rigs.
