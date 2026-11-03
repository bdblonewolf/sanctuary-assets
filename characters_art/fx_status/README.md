# fx_status: char (burn) and ice (freeze) overlays plus the ice shard kit

## Files
| File | What |
|---|---|
| `textures/char_{bc,n,orm}.png` + `char_ember.png` | Charred-flesh material, 512, **tileable**. `char_ember` is a grey mask of glowing cracks |
| `textures/ice_{bc,n,orm}.png` | Frost/ice material, 512, **tileable** |
| `textures/jpg/*.jpg` | **Mobile copies** (q90) of the same 7 maps. Ship these; the PNGs are masters |
| `ice_shards.glb` (mobile) / `masters/ice_shards.glb` (master) | 8 shards `ice_shard_01..08` + `ice_cluster_a`, 1 material `fx_ice`, textures embedded once (JPEG) |
| `preview_fx_status.png` | char / char+ember / ice spheres plus the shards |

ORM = R occlusion, G roughness, B metal (glTF order, so `aoMap` = `roughnessMap` = `metalnessMap` = the same texture). Normals are OpenGL (+Y), which is the three.js default.
Sources: Poly Haven burned_ground_01 and ambientCG Ice001/Ice003, all CC0 (see `src/make_textures.md`).

## Shards (glTF, Y up, metres)
Base at the origin, growing along +Y. Heights 0.08 to 0.37 m, 14 to 26 tris each (cluster 90 tris, 0.32 m). Flat-shaded, with a faint blue emission (strength 0.12) so they read in dark dungeons.
| node | height m | tris |
|---|---|---|
| ice_shard_01 | 0.327 | 22 |
| ice_shard_02 | 0.247 | 18 |
| ice_shard_03 | 0.185 | 22 |
| ice_shard_04 | 0.144 | 14 |
| ice_shard_05 | 0.114 | 18 |
| ice_shard_06 | 0.369 | 26 |
| ice_shard_07 | 0.083 | 14 |
| ice_shard_08 | 0.217 | 18 |
| ice_cluster_a | 0.322 | 90 |

## How to use the overlays (three.js)
Monster UVs aren't laid out for tiling, so **blend the overlay in triplanar object space** on the monster's existing material, driven by one uniform `uStatus` (0 to 1). Don't swap materials. Load the 3 or 4 textures once, share them across all monsters, and set `wrapS = wrapT = RepeatWrapping`.

```js
// once
const T = n => { const t = loader.load(`fx_status/textures/jpg/${n}.jpg`); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
const FX = { char_bc:T('char_bc'), char_ember:T('char_ember'), ice_bc:T('ice_bc') };
// T() loads everything as linear; set .colorSpace = THREE.SRGBColorSpace on char_bc and ice_bc only.

function addStatusOverlay(mat) {           // call once per monster material (MeshStandardMaterial)
  mat.userData.fx = { uChar:{value:0}, uIce:{value:0}, uTime:{value:0}, uScale:{value:3.0},
                      tChar:{value:FX.char_bc}, tEmber:{value:FX.char_ember}, tIce:{value:FX.ice_bc} };
  mat.onBeforeCompile = s => {
    Object.assign(s.uniforms, mat.userData.fx);
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vObjP; varying vec3 vObjN;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvObjP = position; vObjN = normal;');   // bind-pose space, so it sticks to the skin
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>
      varying vec3 vObjP; varying vec3 vObjN; uniform float uChar,uIce,uTime,uScale; uniform sampler2D tChar,tEmber,tIce;
      vec4 tri(sampler2D t){ vec3 w=pow(abs(normalize(vObjN)),vec3(4.)); w/=w.x+w.y+w.z; vec3 p=vObjP*uScale;
        return texture2D(t,p.yz)*w.x+texture2D(t,p.xz)*w.y+texture2D(t,p.xy)*w.z; }`)
      .replace('#include <map_fragment>', `#include <map_fragment>
      float n = tri(tChar).r;                                    // char albedo doubles as a noisy reveal mask
      float cm = clamp(uChar*1.4 - 0.4 + n*1.5, 0., 1.) * step(0.001, uChar);
      diffuseColor.rgb = mix(diffuseColor.rgb, tri(tChar).rgb, cm);
      float im = clamp(uIce*1.2 - n*0.2, 0., 1.);
      diffuseColor.rgb = mix(diffuseColor.rgb, tri(tIce).rgb*1.1, im);`)
      .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
      totalEmissiveRadiance += vec3(1.0,0.32,0.06) * tri(tEmber).r * cm * (0.6+0.4*sin(uTime*6.0)) * 2.0;`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
      roughnessFactor = mix(roughnessFactor, 0.95, cm); roughnessFactor = mix(roughnessFactor, 0.15, im);`);
  };
  mat.customProgramCacheKey = () => 'fxstatus';
}
// per frame: mat.userData.fx.uChar.value = burn 0..1 (ramp up over ~0.4 s on fire hit and hold on death); uIce.value = freeze 0..1; uTime.value = t
```
- **Burn:** ramp `uChar` 0 to 1 over about 0.4 s, and pulse the embers with `uTime`. For a burning death, hold `uChar = 1` and fade the ember term out over 2 s.
- **Freeze:** ramp `uIce` to 1 over 0.25 s and slow the mixer (`action.timeScale = 0.15`; use 0 for a full freeze). Then spawn 4 to 8 shards (see below). On thaw, ramp it back.
- `uScale` sets texture repeats per metre. 3 suits humanoids; use 1.5 to 2 for big monsters.
- One `customProgramCacheKey` means a single extra shader variant shared by every monster.

**Ice shards on a frozen monster:** clone random `ice_shard_*` nodes from the one loaded `ice_shards.glb`, so they share the geometry and material. Parent each to a random bone among Spine, Spine2, Shoulder, Arm, ForeArm, UpLeg and Leg, with a local offset of about 0.05 to 0.10 m out along the bone's side. Point +Y away from the body (use the nearest surface normal, or the vector from the bone towards the mesh bbox centre, negated). Scale 0.6 to 1.4, and use `ice_cluster_a` on the ground at the feet. Shatter: hide them and spawn the same nodes as debris with gravity. For draw calls, use an `InstancedMesh` per shard type, since there are 8 geometries.
