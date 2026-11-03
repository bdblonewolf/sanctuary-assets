# knight_anim_v10b_c.glb (mobile copy)
- **Master and live file:** `knight_anim_v10b.glb`. It is unchanged and is still the one the game loads.
- **Mobile copy:** `knight_anim_v10b_c.glb`. It has the same 75 clips with the same frame counts at 30 fps. Keyframes went from 130,227 to 88,006, and the file from 8.39 to 6.83 MB.
- Pipeline: `/workspace/sanctuary_art/tools/mobile_compress.sh`. Steps: resample (tolerance 1e-4), prune, dedup, then drop scale tracks that never change and translation tracks except on mixamorig:Hips. No meshopt or Draco, so no decoder is needed. The largest joint drift on any frame is 2.38 mm.
- Switch to the mobile copy by changing the path in the manifest.
