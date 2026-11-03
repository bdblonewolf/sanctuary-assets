# fx_decals – blood / goo / lava ground decals (quick kit, v0)
Procedural, cheap, upgrade later. 512 px per map.

textures/<name>_bc.png (RGBA, alpha = decal mask), _n.png (OpenGL normal), _orm.png (R=AO G=roughness B=metal), _e.png (emissive; toxic_pool_a, lava_pool_a). lava_tile_{bc,e,n}.png = tileable 512 lava.
glb/<name>.glb: flat quad at y=+0.01 m (thin splatters 1.5 m, others 2 m), alphaMode BLEND, roughness from ORM (low = wet). lava_pool_a.glb: sunken irregular pool, 288 tris, alphaMode MASK + emissive.

Decals: blood_splatter_thin_a/b/c, blood_splatter_thick_a/b, blood_pool_a, blackblood_goo_a/b, green_goo_a/b, toxic_pool_a, lava_pool_a.

## three.js usage
Simple (flat floors): load the GLB, place, random Y rotation/scale:
```js
const g = (await loader.loadAsync('fx_decals/glb/blood_pool_a.glb')).scene;
g.traverse(o => { if (o.isMesh) { o.material.depthWrite = false; o.material.polygonOffset = true;
  o.material.polygonOffsetFactor = -4; o.renderOrder = 1; } });
g.position.copy(hit.point); g.rotation.y = Math.random()*Math.PI*2; g.scale.setScalar(0.7+Math.random()*0.6);
scene.add(g);
```
Uneven ground: reuse the GLB's material with `DecalGeometry` (three/examples/jsm/geometries/DecalGeometry.js):
`new THREE.Mesh(new DecalGeometry(groundMesh, point, new THREE.Euler(-Math.PI/2,0,rnd), new THREE.Vector3(2,2,1)), mat)`.
Lava/toxic: bump `material.emissiveIntensity` (2–4 with bloom), optionally pulse it; add a small orange PointLight for lava. Tileable lava: `lava_tile_bc.png` with `wrapS/T = RepeatWrapping`, scroll `map.offset` slowly.
Tips: share materials across instances; fade alpha over time by cloning material (opacity) for blood; cap live decals (pool of ~64).
Regenerate: `python3 src/gen_fx_decals.py && python3 src/build_glb.py && python3 src/preview.py`.
