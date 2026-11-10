# Heaven's Shrapnel — engineer fix note

Date: 2026-11-10 America/Detroit. Read-only investigation. **No game code was edited. Nothing was pushed.**
Runtime of our shard art in the live client: **NOT TESTED** (the live client never loads it).

## Cause

This is a **wiring and fallback-primitive issue**, not a missing-art issue. The pushed stained-glass shard pack is not referenced by the live 3D client. Heaven's Shrapnel (`starlash`) is drawn with a procedural almost-white emissive stand-in, then impact "glass" motes that are oversized untextured spheres.

Brian's report ("shoots out big white blobs instead of tiny pieces of fractured shrapnel") matches this fallback exactly.

## What I searched (exact)

- Path names: `*heaven*`, `*shrapnel*`, `*starlash*`, `*star_lash*` under `/workspace/sanctuary`, `/workspace/ge_handoff`, `/workspace/sanctuary_art`, `/workspace/sanctuary-assets`, `/workspace/live`, `/workspace/live11d`, `/workspace/live12`, `/workspace/live13`, `/workspace/live14`, `/workspace/live_bundle_check`, `/workspace/fxs`, `/workspace/stage_fx`, `/workspace/share_eng`, `/workspace/incoming_assets`, `/workspace/handoff`, `/tmp`.
- String `heavens_shrapnel` / `heavens-shrapnel` / `HeavenShrapnel` in `.js/.ts/.md/.json/.html/.txt` under those trees (plus `/workspace/prompts`, `/workspace/repos`, `/workspace/sanctuary-assets-staging`).
- **Result: `heavens_shrapnel` does not appear in any live game JS.** Hits are only art docs/USAGE, `ge_handoff/STAGE_RITEFX2.md`, `ge_handoff/STAGE_AIMED1.md`, and the art handoff folders.
- `fx_rites` in live JS: one hit, and it is **only** the Grave Burst stone cross (plus `fx_status/ice_shards.glb` and `char_ember.png` in the same asset table). Not Heaven's Shrapnel.
- Word `shrapnel` in live JS (without `heavens_`): tooltip/synergy copy only (`thorn shrapnel`, Grave Burst `shrapnel_ring`, "spray shrapnel") — not this rite's VFX.
- Bundles compared: `/workspace/live14/routes-C2sLE0N3.js` (mtime 2026-11-09 5:06 PM ET) is **byte-identical** to `/workspace/live_bundle_check/routes-C2sLE0N3.js`. Older copies (`/workspace/sanctuary/live_*`, `/workspace/ge_handoff/anim_debug/routes-BWHulxh-.js`) also have **zero** `heavens_shrapnel` references.
- Art on disk (pushed v1, commit `9d35b91201609dd3f51a1af640ba8300f89d4a2b`): `/workspace/sanctuary-assets/characters_art/fx_rites/heavens_shrapnel/`. Local unpushed v2: `/workspace/sanctuary_art/handoff/from_art_bot/rites/heavens_shrapnel_v2/`.

The live file is minified with very long lines, so citations are **file + line + unique search string** (column numbers run to tens of thousands).

## Evidence — what the game actually draws

### 1. The rite is `starlash`, display name Heaven's Shrapnel, shape `bolt`, color `#fff6d0`

File: `/workspace/live14/routes-C2sLE0N3.js` **line 3**. Search `starlash:{name:\`Heaven's Shrapnel\``.

```js
starlash:{name:`Heaven's Shrapnel`,school:`holy`,cost:11,
  blurb:`A holy needle. A sip of the wound comes back as life.`,
  locks:[],shape:`bolt`,elem:`magic`,mul:.95,color:`#fff6d0`}
```

`boltKind('starlash')` returns `'holy'` because `school === 'holy'` (same file, search `boltKind(e){`).

### 2. The default bolt sphere is explicitly hidden for starlash — and our shard GLBs are never loaded

File: same, **line 4561**. Search `r.skill===\`starlash\`)n.visible=!1`.

```js
} else if (r.kind === `acid` || r.skill === `bonespear` || r.skill === `javelin` || r.skill === `starlash`) {
  n.visible = !1;  // hides this.boltGeo sphere
  i && (i.visible = !1); // hides arrow mesh
}
```

`askRiteMeshes()` (**line 4562**, search `askRiteMeshes(){`) loads only:

- `models/weapon_spear.glb`
- `characters_art/fx_status/ice_shards.glb`
- `characters_art/fx_rites/grave_burst/grave_burst_stone_cross.glb`

Asset table (**line 4307**), search `graveCrossUrl:` / `iceShardsUrl:`:

```js
iceShardsUrl: `https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_status/ice_shards.glb`,
graveCrossUrl: `https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/grave_burst/grave_burst_stone_cross.glb`,
```

No `heavens_shrapnel_shard_*.glb`, no shatter/trail/impact PNGs.

### 3. Travel visual is `makeGlass()` — four untextured almost-white boxes, not our shards

File: **line 4562**. Search `makeGlass(){` and `i.skill===\`starlash\``.

```js
makeGlass() {
  this.glassGeo ||= new THREE.BoxGeometry(.03, .2, .01); // ng is BoxGeometry (line ~997, this.type=`BoxGeometry`)
  this.glassMat ||= new THREE.MeshStandardMaterial({
    color: 0xFFF8E8,          // 16775400 — almost white
    emissive: 0xFFE29A,       // 16769690 — pale gold
    emissiveIntensity: 1.6,
    transparent: true, opacity: .62, roughness: .04, metalness: .02, depthWrite: false
  });
  const root = new THREE.Group();
  for (let t = 0; t < 4; t++) {
    const mesh = new THREE.Mesh(this.glassGeo, this.glassMat);
    mesh.position.set((t - 1.5) * .045, (t - 1.5) * .03, t % 2 * .02);
    mesh.rotation.set(t * .4, t * .2, t * .55);
    root.add(mesh);
  }
  return root;
}

// in syncSpearGlass:
if (i.skill === `starlash`) {
  n.visible = false;          // spear hidden
  r.visible = true;           // show the makeGlass() group
  r.position.set(i.x, 0.85, i.y);
  r.lookAt(/* flight dir */);
  r.rotation.z = this.time * 6; // spins — four pale emissive boxes read as a white blob
  continue;
}
```

Each box is 3 × 20 × 1 cm, but four of them overlap, spin, and bloom at emissive 1.6 / color `#FFF8E8`. There is no stained-glass texture and no shard sheet / GLB.

### 4. Impact is `puffFx(..., 'glass', 10, 0.95)` — ten oversized untextured spheres

Combat hook, **line 4573**. Search `r.skill===\`starlash\`&&l>0){a=!0,this.puffFx` (hit) and `r.skill===\`starlash\`&&this.puffFx` (expire / miss).

```js
this.puffFx(e.x, e.y, `glass`, 10, .95);
```

`puffFx` (**line 4573**, search `puffFx(e,t,n,r,i=.45)`): `i` is the **start height in metres**, not a scale. Count = 10. Kind = `'glass'`. Launch speed 0.7–2.8 m/s, life ~0.32–0.70 s.

`syncMotes` / `moteMat` (**line 4562**), search `r.kind===\`glass\`?n.scale.setScalar(.18/.28)` and `o=e===\`gold\`||e===\`glass\``:

```js
this.globGeo = new THREE.SphereGeometry(0.28, 10, 8); // line 4523, search this.globGeo=new ug(.28,10,8)
// glass/gold color 16773828 = #FFF2C4, emissiveIntensity 1.5
// glass mote world scale:
n.scale.setScalar(.18 / .28);  // radius 0.18 m → diameter **0.36 m**
// other motes use .05 / .28 → radius 0.05 m
```

Those 36 cm pale-white glowing spheres are the "big white blobs" on impact. They do **not** sample `heavens_shrapnel_shatter_fragments.png`.

## Our shard art

Pushed v1 is stylistically what Brian asked for (stained-glass crimson / cobalt / amber, gold-white trails). It is simply not loaded.

Size note (honest): v1 mesh length is **0.36–0.50 m** at scale `(1,1,1)` per `USAGE.md`. That is already larger than "tiny pieces." Local v2 (unpushed, not approved for push here) is even chunkier (0.55–0.78 m). For tiny shrapnel, apply a **spawn scale** so the long axis lands in **0.05–0.15 m**.

## Fix for the engineer (do not use the white boxes)

1. Load the pushed pack (raw base `https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/characters_art/fx_rites/heavens_shrapnel/`):
   - `heavens_shrapnel_shard_a.glb` (crimson), `_b.glb` (cobalt), `_c.glb` (amber)
   - `heavens_shrapnel_trail.png` or `heavens_shrapnel_trail_4x4.png` (Additive)
   - `heavens_shrapnel_glint_sparkle.png` (Additive)
   - `heavens_shrapnel_impact_burst_4x4.png` (Additive, one-shot)
   - `heavens_shrapnel_shatter_fragments.png` (Normal or soft Additive)
   - `heavens_shrapnel_ground_glint.png` (Additive decal for the tick)
2. In `syncSpearGlass`, when `skill === 'starlash'`, **stop** using `makeGlass()`. Clone a mix of shard_a/b/c. Axes: Y-up, origin center, tip +Z (same as USAGE).
3. **Scale:** `0.20–0.35` on v1 meshes, so long axis ≈ **0.07–0.15 m** (target 0.05–0.15 m). Do not leave scale `(1,1,1)` if the brief is "tiny pieces."
4. **Count (flight):** 4–6 shards, mixed colors, slight spread / arc. Each gets a razor-thin Additive gold/white trail (`color: 0xffffff`, `depthWrite: false`).
5. **Impact:** play `impact_burst_4x4` once (~1.0–1.8 m, 16–20 fps). Emit **8–16** fragments from `shatter_fragments.png` (random atlas cells) at **0.05–0.10 m**. Remove or shrink the `puffFx(..., 'glass', 10, .95)` spheres (if kept, use scale `.05/.28` like other motes, not `.18/.28`, and do not use `#FFF2C4` untextured).
6. Do not fall back to `boltGeo` (`SphereGeometry(0.10)`) or `makeGlass()` if the GLB load fails — log and skip rather than spawning white boxes.
7. Local v2 (handoff only, not on main) is optional later; wire **v1 on main** first.

Read `characters_art/fx_rites/heavens_shrapnel/USAGE.md` for materials (transparent glass, lead stays dark, `emissiveIntensity` ~1.5–2.5 on the panes only). **KEEP BLACKS.**
