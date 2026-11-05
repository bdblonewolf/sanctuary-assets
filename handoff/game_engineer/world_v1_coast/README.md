# world_v1_coast: Ashen Coast grow step 1 (90x180) + north-entrance fix

- `coast_v3_grow.json` is the runtime recipe (applied after the coast world is built). Encoding, offset, exits, props, spawns and POIs are documented inside it.
- `PROMPT_WP1.txt` is the single combined Grok Build prompt.
- `build_coast_v3.py` regenerates the recipe deterministically. `check_coast_v3.py` checks reachability, writes `check_result.json` and makes `coast_v3_proof.png`.
- `old_coast_recon.json` is the old 42x112 map the checks use. Rows 0-15 come from the live dump. Rows 16-111 are rebuilt from the live3.js generator, and the Sand/Sand2 noise in them is approximate.

Proof PNG legend: the white box is the old rect; yellow lines are the road; red rings are exits; yellow rings are intro/sewer/arrivals; blue rings are new spawns; magenta rings are POIs; orange rings are camps. Dots are props: dark = tree, brown = stump, grey = rock.
