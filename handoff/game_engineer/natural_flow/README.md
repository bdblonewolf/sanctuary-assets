# natural_flow (add-only)
Fixes from Brian's 11-04 screenshots.
- **Green 3D-pixel trees / green blockade**: placeDress builds trees from `this.cone()` + box/cylinder placeholders. `placeRealDress()` places real season trees/bushes (random model, yaw, scale, jitter, lean). Swap the cone instancing for it.
- **Invisible bonfire**: outdoor `bonfire` props only get a light + tiny flame. `placeBonfireModels()` adds `prop_bonfire_main.glb` (ash style uses `prop_campfire.glb`).
- **Repeated/heavy Ashen props**: `varyDecor()` (random yaw/scale/tilt, small visual offset) and `thinDecor()` (hides some crowded same-style decor). Visual only; colliders and data untouched.
- **Ashen coast border**: `layout_coast_v2_3.json` = v2_2 spread out (jitter +-1.6 m, same model within 4.5 m swapped, crowding thinned, scale x0.72-1.32, random yaw, slight tilt). 95 props, 14 models.
- Flat grey rocks in Martsirt: not changed here (cause not confirmed).
