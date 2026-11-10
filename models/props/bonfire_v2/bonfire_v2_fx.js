// Bonfire FX: Art-bot campfire_bundle_origfire_smokev2
// Fire: plain additive 4x4 flipbooks (no fire-shader alpha clamp).
// Smoke: smoke_shader_v2.js; falls back to a plain NORMAL flipbook if GLSL fails.
// No sparks (none in the bundle). No old fireball smoke/sparks/wisps.
import { createCampfireSmokeRig, createCampfireSmokeMaterial, SMOKE_DEFAULTS } from './smoke_shader_v2.js';

const COLS = 4, ROWS = 4;

function setFlipbookFrame(map, frame, cols = COLS, rows = ROWS) {
  const col = frame % cols;
  const row = Math.floor(frame / cols) % rows;
  map.repeat.set(1 / cols, 1 / rows);
  map.offset.set(col / cols, 1 - (row + 1) / rows);
}

function loadTex(THREE, url, colorSpace) {
  return new Promise((resolve, reject) => {
    const l = new THREE.TextureLoader();
    l.load(url, (t) => {
      t.wrapS = t.wrapT = THREE.RepeatWrapping;
      t.minFilter = THREE.LinearFilter;
      t.magFilter = THREE.LinearFilter;
      t.generateMipmaps = false;
      if (colorSpace !== undefined) t.colorSpace = colorSpace;
      resolve(t);
    }, undefined, reject);
  });
}

function makeBottomPivotPlane(THREE, w, h) {
  const geo = new THREE.PlaneGeometry(w, h);
  geo.translate(0, h * 0.5, 0); // bottom-center pivot
  return geo;
}

function makePlainFireMat(THREE, map) {
  const mat = new THREE.MeshBasicMaterial({
    map,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    depthTest: true,
    side: THREE.DoubleSide,
    toneMapped: false,
    color: 0xffffff,
  });
  return mat;
}

function shaderCompiles(THREE, renderer, camera, mat) {
  if (!renderer) return true;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(0.2, 0.2), mat);
  const s = new THREE.Scene();
  s.add(mesh);
  const cam = camera || new THREE.PerspectiveCamera(30, 1, 0.1, 20);
  const prev = renderer.debug ? renderer.debug.checkShaderErrors : undefined;
  if (renderer.debug) renderer.debug.checkShaderErrors = true;
  try {
    renderer.compile(s, cam);
    const prog = mat.program;
    if (prog && prog.program) {
      const gl = renderer.getContext();
      if (gl && gl.getProgramParameter && !gl.getProgramParameter(prog.program, gl.LINK_STATUS)) {
        return false;
      }
    }
    return true;
  } catch (e) {
    console.warn('[bonfire_v2_fx] smoke shader compile failed:', e);
    return false;
  } finally {
    if (renderer.debug && prev !== undefined) renderer.debug.checkShaderErrors = prev;
    mesh.geometry.dispose();
  }
}

function makeFallbackSmokeMat(THREE, map, maxAlpha = 0.72) {
  const mat = new THREE.MeshBasicMaterial({
    map,
    transparent: true,
    blending: THREE.NormalBlending,
    depthWrite: false,
    depthTest: true,
    side: THREE.DoubleSide,
    toneMapped: false,
    color: 0x0c0806, // rich near-black soot, never light grey
    opacity: 0,
    premultipliedAlpha: true,
  });
  mat.userData.maxAlpha = maxAlpha;
  return mat;
}

export async function createBonfireFX(THREE, group, opts = {}) {
  const root = new THREE.Group();
  root.name = 'bonfire_v2_fx';
  group.add(root);

  const flameUrl = opts.flameUrl || './campfire_flame_flipbook.png';
  const flameUrlB = opts.flameUrlB || './campfire_flame_flipbook_b.png';
  const glowUrl = opts.glowUrl || './campfire_flame_base_glow.png';
  const smokeUrl = opts.smokeUrl || './campfire_smoke_flipbook_v2.png';
  const renderer = opts.renderer || null;
  const camera = opts.camera || null;

  const [mapA, mapB, mapGlow, mapSmoke] = await Promise.all([
    loadTex(THREE, flameUrl, THREE.SRGBColorSpace),
    loadTex(THREE, flameUrlB, THREE.SRGBColorSpace),
    loadTex(THREE, glowUrl, THREE.SRGBColorSpace),
    loadTex(THREE, smokeUrl, THREE.SRGBColorSpace),
  ]);
  // each fire card needs its own texture instance so offsets can differ
  const mapA2 = mapA.clone(); mapA2.needsUpdate = true;
  const mapB2 = mapB.clone(); mapB2.needsUpdate = true;

  const fw = opts.flameWidth || 1.44;
  const fh = opts.flameHeight || 1.56;
  const flameY = opts.flameY != null ? opts.flameY : 0.06; // bottom-center at log base, inside the teepee
  const fpsFire = opts.flameFps || 16;

  const geoA = makeBottomPivotPlane(THREE, fw, fh);
  const geoB = makeBottomPivotPlane(THREE, fw, fh);
  const matA = makePlainFireMat(THREE, mapA2);
  const matB = makePlainFireMat(THREE, mapB2);
  const cardA = new THREE.Mesh(geoA, matA);
  const cardB = new THREE.Mesh(geoB, matB);
  cardA.position.set(0, flameY, 0);
  cardB.position.set(0, flameY, 0);
  cardB.rotation.y = Math.PI * 0.5;
  cardA.castShadow = cardB.castShadow = false;
  cardA.receiveShadow = cardB.receiveShadow = false;
  root.add(cardA);
  root.add(cardB);

  const frameA0 = Math.floor(Math.random() * 16);
  const frameB0 = Math.floor(Math.random() * 16);
  setFlipbookFrame(mapA2, frameA0);
  setFlipbookFrame(mapB2, frameB0);

  // base glow at the log base
  const glow = new THREE.Mesh(
    makeBottomPivotPlane(THREE, 1.02, 0.54),
    new THREE.MeshBasicMaterial({
      map: mapGlow,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      side: THREE.DoubleSide,
      toneMapped: false,
      color: 0xffffff,
    })
  );
  glow.position.set(0, 0.02, 0);
  glow.rotation.x = -Math.PI * 0.5;
  glow.castShadow = glow.receiveShadow = false;
  root.add(glow);

  // fire lights (cards are unlit additive; scene still needs a warm key)
  const p1 = new THREE.PointLight(0xff6a28, 2.4, 7.0, 2.0);
  p1.position.set(0.02, 0.55, 0.03);
  p1.castShadow = true;
  p1.shadow.mapSize.set(512, 512);
  p1.shadow.camera.near = 0.05;
  p1.shadow.camera.far = 6;
  p1.shadow.bias = -0.005;
  const p2 = new THREE.PointLight(0xff9a40, 0.7, 3.5, 2.0);
  p2.position.set(-0.05, 0.22, 0.04);
  root.add(p1);
  root.add(p2);

  // --- smoke ---
  let smokeMode = 'shader_v2';
  let smokeRig = null;
  let smokeFallback = [];
  const smokeOpts = {
    map: mapSmoke,
    count: opts.smokeCount || 6,
    fps: 12,
    width: 1.1,
    height: 1.6,
    life: 2.8,
    rise: 2.2,
    spawnY: 1.25,
    spawnJitter: 0.18,
    windAmp: 0.16,
    windFreq: 0.35,
    invisibleUntil: 0.25,
    sootStart: 0.50,
    sootEnd: 0.75,
    dissolveStart: 0.78,
    maxAlpha: 0.72,
    heatTint: [0.16, 0.07, 0.03],
    sootColor: [0.025, 0.016, 0.012],
  };

  try {
    // probe compile with one material before building the rig
    const probeMap = mapSmoke.clone(); probeMap.needsUpdate = true;
    const probe = createCampfireSmokeMaterial(THREE, probeMap, smokeOpts);
    if (renderer && !shaderCompiles(THREE, renderer, camera, probe)) {
      throw new Error('GLSL link/compile failed');
    }
    smokeRig = createCampfireSmokeRig(THREE, smokeOpts);
    root.add(smokeRig.group);
  } catch (e) {
    console.warn('[bonfire_v2_fx] falling back to plain smoke material:', e);
    smokeMode = 'plain_fallback';
    smokeRig = null;
    const count = smokeOpts.count;
    for (let i = 0; i < count; i++) {
      const tm = mapSmoke.clone(); tm.needsUpdate = true;
      const mat = makeFallbackSmokeMat(THREE, tm, smokeOpts.maxAlpha);
      const mesh = new THREE.Mesh(
        makeBottomPivotPlane(THREE, smokeOpts.width, smokeOpts.height),
        mat
      );
      mesh.castShadow = mesh.receiveShadow = false;
      const seed = Math.random();
      root.add(mesh);
      smokeFallback.push({
        mesh, mat, map: tm, seed,
        life: smokeOpts.life * (0.85 + 0.3 * seed),
        age: (i / count), // stagger
        offset: Math.floor(Math.random() * 16),
        x0: (Math.random() * 2 - 1) * smokeOpts.spawnJitter,
        z0: (Math.random() * 2 - 1) * smokeOpts.spawnJitter,
      });
    }
  }

  let t = 0;
  function update(dt) {
    t += dt;
    const fA = Math.floor(t * fpsFire + frameA0) % 16;
    const fB = Math.floor(t * fpsFire + frameB0) % 16;
    setFlipbookFrame(mapA2, fA);
    setFlipbookFrame(mapB2, fB);
    const flick = 1.0 + 0.12 * Math.sin(t * 9.1) + 0.07 * Math.sin(t * 17.3);
    p1.intensity = 2.4 * flick;
    p2.intensity = 0.7 * flick;
    glow.material.opacity = 0.7 + 0.2 * Math.sin(t * 7.5);

    if (smokeRig) {
      smokeRig.update(dt);
    } else {
      for (const p of smokeFallback) {
        p.age += dt / p.life;
        if (p.age >= 1) {
          p.age -= 1;
          p.x0 = (Math.random() * 2 - 1) * smokeOpts.spawnJitter;
          p.z0 = (Math.random() * 2 - 1) * smokeOpts.spawnJitter;
        }
        const age = p.age;
        const y = smokeOpts.spawnY + age * smokeOpts.rise;
        const wind = smokeOpts.windAmp * Math.sin((age + p.seed) * smokeOpts.windFreq * Math.PI * 2);
        const wind2 = smokeOpts.windAmp * 0.6 * Math.sin((age * 1.7 + p.seed * 6.0) * (smokeOpts.windFreq * 1.4) * Math.PI * 2 + 1.3);
        p.mesh.position.set(p.x0 + wind, y, p.z0 + wind2);
        const sc = 0.72 + 0.45 * age;
        p.mesh.scale.set(sc, 0.9 + 0.25 * age, 1);
        // 25% birth ease, soot/dark stay, dissolve late — no light-grey tint
        let a = 0;
        if (age < smokeOpts.invisibleUntil) a = 0;
        else if (age < 0.5) a = smokeOpts.maxAlpha * (age - smokeOpts.invisibleUntil) / (0.5 - smokeOpts.invisibleUntil);
        else if (age < smokeOpts.dissolveStart) a = smokeOpts.maxAlpha;
        else a = smokeOpts.maxAlpha * (1 - (age - smokeOpts.dissolveStart) / (1 - smokeOpts.dissolveStart));
        p.mat.opacity = Math.max(0, a);
        const soot = age > smokeOpts.sootStart ? Math.min(1, (age - smokeOpts.sootStart) / (smokeOpts.sootEnd - smokeOpts.sootStart)) : 0;
        // stay rich black/brown
        p.mat.color.setRGB(
          0.16 * (1 - soot) + 0.025 * soot,
          0.07 * (1 - soot) + 0.016 * soot,
          0.03 * (1 - soot) + 0.012 * soot
        );
        const frame = Math.floor(age * p.life * smokeOpts.fps + p.offset) % 16;
        setFlipbookFrame(p.map, frame);
      }
    }
  }

  return { update, group: root, smokeMode };
}
