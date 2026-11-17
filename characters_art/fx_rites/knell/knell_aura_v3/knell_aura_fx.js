/**
 * Sanctuary — Knell Aura FX (v3). CC0 hook script.
 *
 * Persistent Knell aura as a jagged gold-and-blue fire starburst sigil,
 * projected flat under the hero's feet (isometric). No smooth circles,
 * no solid rings, no ghost bell (Brian t499u / t497u).
 *
 * New in this folder:
 *   knell_sigil_starburst.png   1024 jagged starburst mask (R=fill, G=hot rim, A=coverage).
 *                               The star's alpha centroid is locked to the UV / plane center.
 *   knell_sigil_haze.png        Soft D2-style outer haze of the same star (blurred, centered).
 *
 * Reused (do not copy; load from the live library paths):
 *   fireball/fireball_explosion_flipbook.png            gold/blue fire fill (4×4, masked by the sigil)
 *   arc_whip/arc_whip_impact_fork_4x4_v2.png            crackling tendrils (4×4; center faded)
 *   fireball/fireball_sparks_embers.png                 outward ember streaks
 *   fireball/fireball_trail_strip.png                   short flame tendrils at spike tips
 *   characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png   9 count marks
 *
 * Intentionally unused: fireball_shockwave_ring.png (smooth ring).
 *
 * Everything is a horizontal PlaneGeometry at y ≈ 0.02–0.05 m, depthWrite
 * false, renderOrder so the marks sit on top. No GLB.
 * The aura is centered under the character root: every ground layer sits at
 * local (0, y, 0) except marks (evenly around the center) and tendrils
 * (radial at the spike tips). attach() + update() copy the hero's world
 * position only (not rotation).
 *
 * Usage:
 *   const fx = KnellAuraFX.create(THREE, scene, {
 *     sigil, haze, flame, fork, embers, trail, marks,
 *   }, opts);
 *   fx.attach(heroObject3D);
 *   fx.setOn((player.auraOn || []).includes('knell'));
 *   fx.setCount(game.peal);       // 0–8
 *   if (justTolled) fx.ninth();   // jagged dark-blue spike flare, no ring
 *   fx.update(dt);
 *   fx.dispose();
 *
 * NOT TESTED: never run in three.js or in the game. Only `node --check`.
 */
/* eslint-disable no-undef */
const KNELL_AURA_DEFAULTS = {
  sigilSize: 1.62,            // tip-to-tip, compact (longest spike ~0.75 m)
  flameSize: 1.62,
  forkSize: 1.85,             // tendril forks slightly past the tips
  emberSize: 1.50,
  trailLen: 0.30,
  trailWid: 0.10,
  trailRadius: 0.62,
  tendrilCount: 9,
  footY: 0.028,
  sigilY: 0.024,
  flameY: 0.028,
  forkY: 0.032,
  emberY: 0.034,
  trailY: 0.036,
  pealY: 0.040,
  markY: 0.048,
  markSize: 0.17,
  markRadius: 0.40,           // spike bases, just outside the boots
  flameFps: 12,
  forkFps: 10,
  fadeOn: 0.18,
  fadeOff: 0.25,
  pealDur: 0.45,
  // tints
  tintGold: 0xd8a040,         // #D8A040 — faint hints only
  tintGoldHi: 0xd8a040,
  tintBlue: 0x1e4c8c,         // #1E4C8C deep
  tintBlueMid: 0x3a78c0,      // #3A78C0 medium
  tintBlueHi: 0x6aa8e0,       // #6AA8E0 core cap (no paler)
  tintPeal: 0x1a3a80,         // #1A3A80
  tintMarkUnlit: 0x1a3a80,
  tintMarkLit: 0x2e5ac0,
  tintMarkOutline: 0x0c1a40,
  // peaks (keep blacks — no raw Additive, no bright wash)
  // gold is ~20% of the previous peaks (hints only)
  sigilGoldPeak: 0.07,
  sigilBluePeak: 0.62,
  flameGoldPeak: 0.145,
  flameBluePeak: 0.78,
  forkPeak: 0.34,
  emberPeak: 0.16,
  trailPeak: 0.36,
  trailGoldPeak: 0.10,
  hazePeak: 0.30,
  warpAmp: 0.20,
  softEdge: 0.018,
  hazeSize: 1.98,             // unscaled; slightly larger than the 1.62 m sigil
  hazeY: 0.020,
  // Whole-aura scale. Default 0.8 (20% smaller) so the same textures
  // sit on a tighter footprint and read denser / crisper. Size constants
  // below are the unscaled (1.0) values; attach/update apply this to the root.
  scale: 0.8,
};

function _prepTex(THREE, t) {
  const c = t.clone();
  c.needsUpdate = true;
  c.wrapS = c.wrapT = THREE.ClampToEdgeWrapping;
  c.generateMipmaps = false;
  c.minFilter = THREE.LinearFilter;
  c.magFilter = THREE.LinearFilter;
  if ('colorSpace' in c && THREE.SRGBColorSpace) c.colorSpace = THREE.SRGBColorSpace;
  return c;
}

function _cellOffset(tex, cell, cols, rows) {
  const f = Math.max(0, Math.min(cols * rows - 1, cell | 0));
  const c = f % cols, r = (f / cols) | 0;
  tex.repeat.set(1 / cols, 1 / rows);
  tex.offset.set(c / cols, 1 - (r + 1) / rows);
}

function _commonMat(extra) {
  return Object.assign({
    transparent: true,
    depthWrite: false,
    depthTest: true,
    blending: THREE.CustomBlending,
    blendSrc: THREE.OneFactor,
    blendDst: THREE.OneMinusSrcAlphaFactor,
    toneMapped: false,
    side: THREE.DoubleSide,
    polygonOffset: true,
  }, extra || {});
}

/**
 * Luma/channel mask tint with optional:
 *   maskMap      — a second texture (the sigil) multiplied in
 *   warpAmp      — chaotic per-angle radial grow/shrink (not a ring pulse)
 *   warpPhase    — phase offset so gold/blue don't breathe in lockstep
 *   centerFade   — hide a circular core (used on the fork so only cracks show)
 *   useRim       — if the map is the sigil (R=fill, G=rim), mix tint + tintRim
 *   softEdge     — 9-tap UV blur so edges haze like a D2 aura (marks do not use this)
 *   uvDrift      — slow UV crawl on fire fill so the flame keeps moving
 */
function _fireMat(THREE, map, tintHex, extra) {
  const ex = extra || {};
  const rest = Object.assign({}, ex);
  ['maskMap', 'warpAmp', 'warpPhase', 'centerFade', 'useRim', 'tintRim', 'softFalloff', 'uvRotate', 'softEdge', 'uvDrift'].forEach((k) => { delete rest[k]; });
  const mat = new THREE.ShaderMaterial(Object.assign({
    uniforms: {
      map: { value: map },
      maskMap: { value: ex.maskMap || map },
      useMask: { value: ex.maskMap ? 1 : 0 },
      tint: { value: new THREE.Color(tintHex) },
      tintRim: { value: new THREE.Color(ex.tintRim != null ? ex.tintRim : tintHex) },
      useRim: { value: ex.useRim ? 1 : 0 },
      opacity: { value: 1 },
      time: { value: 0 },
      warpAmp: { value: ex.warpAmp || 0 },
      warpPhase: { value: ex.warpPhase || 0 },
      centerFade: { value: ex.centerFade || 0 },
      uvRotate: { value: ex.uvRotate || 0 },
      softEdge: { value: ex.softEdge || 0 },
      uvDrift: { value: new THREE.Vector2((ex.uvDrift && ex.uvDrift[0]) || 0, (ex.uvDrift && ex.uvDrift[1]) || 0) },
    },
    vertexShader: [
      'varying vec2 vUv;',
      'void main(){',
      '  vUv = uv;',
      '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);',
      '}',
    ].join('\n'),
    fragmentShader: [
      'uniform sampler2D map;',
      'uniform sampler2D maskMap;',
      'uniform float useMask;',
      'uniform vec3 tint;',
      'uniform vec3 tintRim;',
      'uniform float useRim;',
      'uniform float opacity;',
      'uniform float time;',
      'uniform float warpAmp;',
      'uniform float warpPhase;',
      'uniform float centerFade;',
      'uniform float uvRotate;',
      'uniform float softEdge;',
      'uniform vec2 uvDrift;',
      'varying vec2 vUv;',
      'float mapCov(vec2 uv){',
      '  vec4 t = texture2D(map, uv);',
      '  float luma = dot(t.rgb, vec3(0.2126, 0.7152, 0.0722));',
      '  return (useRim > 0.5) ? max(t.a, max(t.r, t.g)) : max(t.a, luma);',
      '}',
      'float maskCov(vec2 uv){',
      '  vec4 ktex = texture2D(maskMap, uv);',
      '  return max(ktex.a, max(ktex.r, ktex.g));',
      '}',
      'float covAt(vec2 uvMap, vec2 uvMask){',
      '  float m = mapCov(uvMap);',
      '  if (useMask > 0.5) m *= maskCov(uvMask);',
      '  return m;',
      '}',
      'void main(){',
      '  vec2 d = vUv - vec2(0.5);',
      '  float ang = atan(d.y, d.x);',
      '  float k = 1.0 + warpAmp * (',
      '    0.16 * sin(ang * 7.0 + time * 3.05 + warpPhase) +',
      '    0.11 * sin(ang * 11.0 + time * 5.17 + warpPhase * 1.3) +',
      '    0.07 * sin(ang * 3.0 + time * 1.63 + warpPhase * 0.6)',
      '  );',
      '  vec2 uvMask = vec2(0.5) + d / max(k, 0.55);',
      '  float ca = cos(uvRotate), sa = sin(uvRotate);',
      '  vec2 rd = vec2(d.x * ca - d.y * sa, d.x * sa + d.y * ca);',
      '  vec2 uvMap = vec2(0.5) + rd / max(k, 0.55) + uvDrift * time;',
      '  float m = covAt(uvMap, uvMask);',
      '  if (softEdge > 0.0005) {',
      '    float e = softEdge;',
      '    float s = m;',
      '    s += covAt(uvMap + vec2(e, 0.0), uvMask + vec2(e, 0.0));',
      '    s += covAt(uvMap + vec2(-e, 0.0), uvMask + vec2(-e, 0.0));',
      '    s += covAt(uvMap + vec2(0.0, e), uvMask + vec2(0.0, e));',
      '    s += covAt(uvMap + vec2(0.0, -e), uvMask + vec2(0.0, -e));',
      '    s += covAt(uvMap + vec2(e, e) * 0.707, uvMask + vec2(e, e) * 0.707);',
      '    s += covAt(uvMap + vec2(-e, e) * 0.707, uvMask + vec2(-e, e) * 0.707);',
      '    s += covAt(uvMap + vec2(e, -e) * 0.707, uvMask + vec2(e, -e) * 0.707);',
      '    s += covAt(uvMap + vec2(-e, -e) * 0.707, uvMask + vec2(-e, -e) * 0.707);',
      '    m = s / 9.0;',
      '  }',
      '  float r = length(d) * 2.0;',
      '  if (centerFade > 0.001) {',
      '    m *= smoothstep(centerFade * 0.55, centerFade, r);',
      '  }',
      '  if (m < 0.001) discard;',
      '  float a = m * opacity;',
      '  vec4 t = texture2D(map, uvMap);',
      '  float fill = t.r;',
      '  float rim = t.g;',
      '  vec3 col = tint;',
      '  if (useRim > 0.5) {',
      '    float den = max(fill + rim, 1e-4);',
      '    col = (tint * fill + tintRim * rim) / den;',
      '  }',
      '  gl_FragColor = vec4(col * a, a);',
      '}',
    ].join('\n'),
  }, _commonMat(rest)));
  Object.defineProperty(mat, 'opacity', {
    get() { return this.uniforms.opacity.value; },
    set(v) { this.uniforms.opacity.value = v; },
  });
  return mat;
}

function _markMat(THREE, map, fillHex, outlineHex, extra) {
  const mat = new THREE.ShaderMaterial(Object.assign({
    uniforms: {
      map: { value: map },
      tintFill: { value: new THREE.Color(fillHex) },
      tintOutline: { value: new THREE.Color(outlineHex) },
      opacity: { value: 1 },
    },
    vertexShader: [
      'varying vec2 vUv;',
      'void main(){',
      '  vUv = uv;',
      '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);',
      '}',
    ].join('\n'),
    fragmentShader: [
      'uniform sampler2D map;',
      'uniform vec3 tintFill;',
      'uniform vec3 tintOutline;',
      'uniform float opacity;',
      'varying vec2 vUv;',
      'void main(){',
      '  vec4 t = texture2D(map, vUv);',
      '  float fill = t.r;',
      '  float outline = t.g;',
      '  float cov = max(t.a, max(fill, outline));',
      '  float a = cov * opacity;',
      '  float den = max(fill + outline, 1e-4);',
      '  vec3 col = (tintOutline * outline + tintFill * fill) / den;',
      '  gl_FragColor = vec4(col * a, a);',
      '}',
    ].join('\n'),
  }, _commonMat(extra || {})));
  Object.defineProperty(mat, 'opacity', {
    get() { return this.uniforms.opacity.value; },
    set(v) { this.uniforms.opacity.value = v; },
  });
  return mat;
}

function _pulse(t) {
  const v = 0.74
    + 0.12 * Math.sin(t * 2.05)
    + 0.08 * Math.sin(t * 3.61 + 1.15)
    + 0.05 * Math.sin(t * 5.17 + 2.60)
    + 0.04 * Math.sin(t * 1.13 + 0.40);
  return Math.max(0.52, Math.min(1.0, v));
}

function create(THREE, scene, textures, opts) {
  const o = Object.assign({}, KNELL_AURA_DEFAULTS, opts || {});
  const S = (o.scale != null && o.scale > 0) ? o.scale : 1;
  const root = new THREE.Group();
  root.name = 'KnellAuraFX';
  root.visible = false;
  root.scale.set(S, S, S);
  scene.add(root);

  const _tmp = new THREE.Vector3();
  let hero = null;
  let on = false;
  let count = 0;
  let t = 0;
  let fade = 0;
  let pealT = -1;
  const owned = [];
  const markSlots = [];
  const trailSlots = [];
  const ticking = []; // materials whose time uniform we advance

  function _ground(map, tint, poly, size, y, order, matExtra, w, h) {
    const tex = _prepTex(THREE, map);
    const mat = _fireMat(THREE, tex, tint, Object.assign({ polygonOffsetFactor: poly }, matExtra || {}));
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w || size, h || size), mat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.set(0, y, 0);
    mesh.renderOrder = order;
    mesh.frustumCulled = false;
    root.add(mesh);
    owned.push(tex, mat, mesh.geometry);
    ticking.push(mat);
    return { mesh, tex, mat };
  }

  const sigilTex = textures.sigil ? _prepTex(THREE, textures.sigil) : null;
  if (sigilTex) owned.push(sigilTex);

  const hazeSrc = textures.haze || textures.sigil;
  const haze = hazeSrc
    ? _ground(hazeSrc, o.tintBlue, 0, o.hazeSize, o.hazeY, 1, {
      warpAmp: o.warpAmp * 0.35, warpPhase: 0.8, softEdge: 0.03,
    })
    : null;

  const sigilGold = textures.sigil
    ? _ground(textures.sigil, o.tintGold, -1, o.sigilSize, o.sigilY, 2, {
      useRim: true, tintRim: o.tintBlueMid, warpAmp: o.warpAmp, warpPhase: 0.0,
      softEdge: o.softEdge,
    })
    : null;
  const sigilBlue = textures.sigil
    ? _ground(textures.sigil, o.tintBlue, -1, o.sigilSize, o.sigilY + 0.002, 3, {
      useRim: true, tintRim: o.tintBlueMid, warpAmp: o.warpAmp * 0.85, warpPhase: 1.7,
      softEdge: o.softEdge,
    })
    : null;

  const flameGold = (textures.flame && sigilTex)
    ? _ground(textures.flame, o.tintGold, -2, o.flameSize, o.flameY, 4, {
      maskMap: sigilTex, warpAmp: o.warpAmp * 0.7, warpPhase: 0.4,
      softEdge: o.softEdge, uvDrift: [0.018, 0.010],
    })
    : null;
  if (flameGold) _cellOffset(flameGold.tex, 0, 4, 4);
  const flameBlue = (textures.flame && sigilTex)
    ? _ground(textures.flame, o.tintBlueMid, -2, o.flameSize, o.flameY + 0.002, 5, {
      maskMap: sigilTex, warpAmp: o.warpAmp * 0.7, warpPhase: 2.1, uvRotate: 0.7,
      softEdge: o.softEdge, uvDrift: [-0.012, 0.016],
    })
    : null;
  if (flameBlue) _cellOffset(flameBlue.tex, 5, 4, 4);

  const fork = textures.fork
    ? _ground(textures.fork, o.tintBlueMid, -3, o.forkSize, o.forkY, 6, {
      tintRim: o.tintBlueHi, warpAmp: o.warpAmp * 0.35, warpPhase: 0.9,
      centerFade: 0.30, softEdge: 0.014,
    })
    : null;
  if (fork) _cellOffset(fork.tex, 0, 4, 4);

  const embers = textures.embers
    ? _ground(textures.embers, o.tintBlueMid, -3, o.emberSize, o.emberY, 7, {
      warpAmp: 0.08, warpPhase: 0.2, softEdge: 0.016,
    })
    : null;

  if (textures.trail) {
    for (let i = 0; i < o.tendrilCount; i++) {
      const ang = (i / o.tendrilCount) * Math.PI * 2;
      const tex = _prepTex(THREE, textures.trail);
      // gold hints on two tips only; the rest stay dark blue
      const goldHint = (i === 1 || i === 5);
      const mat = _fireMat(THREE, tex, goldHint ? o.tintGold : o.tintBlueMid, {
        polygonOffsetFactor: -4, warpAmp: 0, tintRim: goldHint ? o.tintGold : o.tintBlueHi,
        softEdge: 0.022,
      });
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(o.trailLen, o.trailWid), mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.rotation.z = Math.PI / 2 - ang;
      mesh.position.set(Math.sin(ang) * o.trailRadius, o.trailY, Math.cos(ang) * o.trailRadius);
      mesh.renderOrder = 8;
      mesh.frustumCulled = false;
      root.add(mesh);
      owned.push(tex, mat, mesh.geometry);
      ticking.push(mat);
      trailSlots.push({ mesh, tex, mat, ang, goldHint });
    }
  }

  const pealSigil = textures.sigil
    ? _ground(textures.sigil, o.tintPeal, -4, o.sigilSize, o.pealY, 9, {
      useRim: true, tintRim: o.tintBlueMid, warpAmp: o.warpAmp * 1.15, warpPhase: 0.0,
      softEdge: o.softEdge * 1.2,
    })
    : null;
  if (pealSigil) pealSigil.mesh.visible = false;
  const pealHaze = hazeSrc
    ? _ground(hazeSrc, o.tintPeal, -4, o.hazeSize, o.pealY - 0.002, 8, {
      warpAmp: o.warpAmp * 0.5, warpPhase: 0.3, softEdge: 0.03,
    })
    : null;
  if (pealHaze) pealHaze.mesh.visible = false;
  const pealFork = textures.fork
    ? _ground(textures.fork, o.tintPeal, -4, o.forkSize, o.pealY + 0.002, 9, {
      centerFade: 0.22, warpAmp: 0.12, softEdge: 0.016,
    })
    : null;
  if (pealFork) { pealFork.mesh.visible = false; _cellOffset(pealFork.tex, 0, 4, 4); }

  if (textures.marks) {
    for (let i = 0; i < 9; i++) {
      const ang = (i / 9) * Math.PI * 2;
      const tex = _prepTex(THREE, textures.marks);
      const mat = _markMat(THREE, tex, o.tintMarkUnlit, o.tintMarkOutline, { polygonOffsetFactor: -6 });
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(o.markSize, o.markSize), mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.set(Math.sin(ang) * o.markRadius, o.markY, Math.cos(ang) * o.markRadius);
      mesh.renderOrder = 12;
      mesh.frustumCulled = false;
      root.add(mesh);
      owned.push(tex, mat, mesh.geometry);
      _cellOffset(tex, 0, 2, 1);
      markSlots.push({ mesh, tex, mat });
    }
  }

  function _applyMarks(nLit) {
    const litN = Math.max(0, Math.min(9, nLit | 0));
    const litCol = new THREE.Color(o.tintMarkLit);
    const unlitCol = new THREE.Color(o.tintMarkUnlit);
    for (let i = 0; i < markSlots.length; i++) {
      const lit = i < litN;
      _cellOffset(markSlots[i].tex, lit ? 1 : 0, 2, 1);
      markSlots[i].mat.uniforms.tintFill.value.copy(lit ? litCol : unlitCol);
    }
  }

  function setOn(v) { on = !!v; if (on) root.visible = true; }
  function setCount(n) {
    count = Math.max(0, Math.min(8, n | 0));
    if (pealT < 0) _applyMarks(count);
  }
  function ninth() {
    pealT = 0;
    if (pealSigil) pealSigil.mesh.visible = true;
    if (pealHaze) pealHaze.mesh.visible = true;
    if (pealFork) pealFork.mesh.visible = true;
    _applyMarks(9);
  }
  function attach(heroObj) { hero = heroObj || null; }

  function update(dt) {
    if (dt < 0) dt = 0;
    if (dt > 0.1) dt = 0.1;
    t += dt;
    if (hero) {
      hero.updateWorldMatrix(true, false);
      _tmp.setFromMatrixPosition(hero.matrixWorld);
      root.position.set(_tmp.x, _tmp.y, _tmp.z);
      root.quaternion.identity();
      root.scale.set(S, S, S);
    }
    const target = on ? 1 : 0;
    const fadeRate = on ? 1 / o.fadeOn : 1 / o.fadeOff;
    if (fade < target) fade = Math.min(target, fade + dt * fadeRate);
    else if (fade > target) fade = Math.max(target, fade - dt * fadeRate);
    if (fade <= 0 && !on && pealT < 0) { root.visible = false; return; }
    root.visible = true;

    const pul = _pulse(t);
    for (let i = 0; i < ticking.length; i++) {
      if (ticking[i].uniforms && ticking[i].uniforms.time) ticking[i].uniforms.time.value = t;
    }

    if (haze) {
      haze.mat.opacity = fade * o.hazePeak * (0.80 + 0.20 * pul);
      haze.mesh.rotation.z = t * 0.07;
    }
    if (sigilGold) sigilGold.mat.opacity = fade * o.sigilGoldPeak * (0.70 + 0.30 * pul);
    if (sigilBlue) {
      sigilBlue.mat.opacity = fade * o.sigilBluePeak * (0.78 + 0.22 * (1 - pul));
    }
    if (flameGold) {
      _cellOffset(flameGold.tex, (((t * o.flameFps) % 16) + 16) % 16, 4, 4);
      flameGold.mat.opacity = fade * o.flameGoldPeak * (0.65 + 0.35 * pul);
    }
    if (flameBlue) {
      _cellOffset(flameBlue.tex, (((t * o.flameFps * 0.87 + 7) % 16) + 16) % 16, 4, 4);
      flameBlue.mat.opacity = fade * o.flameBluePeak * (0.75 + 0.25 * (1 - pul));
    }
    if (fork) {
      _cellOffset(fork.tex, (((t * o.forkFps) % 16) + 16) % 16, 4, 4);
      fork.mat.opacity = fade * o.forkPeak * (0.70 + 0.30 * pul);
      fork.mesh.rotation.z = t * 0.10;
    }
    if (embers) {
      embers.mat.opacity = fade * o.emberPeak * (0.60 + 0.40 * pul);
      embers.mesh.rotation.z = -t * 0.18;
    }
    for (let i = 0; i < trailSlots.length; i++) {
      const tr = trailSlots[i];
      const flicker = 0.50 + 0.50 * Math.sin(t * (7.1 + i * 0.73) + i * 1.2);
      const grow = 1.0 + 0.28 * Math.sin(t * (3.4 + i * 0.5) + i);
      const peak = tr.goldHint ? o.trailGoldPeak : o.trailPeak;
      tr.mat.opacity = fade * peak * flicker;
      tr.mesh.scale.set(grow, 1, 1);
    }
    for (let i = 0; i < markSlots.length; i++) {
      const lit = pealT >= 0 ? true : i < count;
      markSlots[i].mat.opacity = fade * (lit ? 1.0 : 0.92);
    }

    if (pealT >= 0) {
      pealT += dt;
      const u = Math.min(1, pealT / o.pealDur);
      const op = (1 - u) * 0.95;
      const sc = 1.0 + 0.55 * u;
      if (pealHaze) {
        pealHaze.mat.opacity = op * 0.80;
        pealHaze.mesh.scale.set(sc * 1.08, sc * 1.08, 1);
        pealHaze.mesh.visible = u < 1;
      }
      if (pealSigil) {
        pealSigil.mat.opacity = op;
        pealSigil.mesh.scale.set(sc, sc, 1);
        pealSigil.mesh.visible = u < 1;
      }
      if (pealFork) {
        _cellOffset(pealFork.tex, Math.min(15, (u * 16) | 0), 4, 4);
        pealFork.mat.opacity = op * 0.85;
        pealFork.mesh.scale.set(sc * 1.05, sc * 1.05, 1);
        pealFork.mesh.visible = u < 1;
      }
      if (pealT >= o.pealDur) {
        pealT = -1;
        if (pealSigil) pealSigil.mesh.visible = false;
        if (pealHaze) pealHaze.mesh.visible = false;
        if (pealFork) pealFork.mesh.visible = false;
        _applyMarks(count);
      }
    }
  }

  function dispose() {
    hero = null;
    for (const x of owned) if (x && x.dispose) x.dispose();
    owned.length = 0;
    markSlots.length = 0;
    trailSlots.length = 0;
    ticking.length = 0;
    if (root.parent) root.parent.remove(root);
  }

  return { attach, setOn, setCount, ninth, update, dispose, options: o, root, getCount: () => count };
}

const KnellAuraFX = {
  KNELL_AURA_DEFAULTS, create,
  REUSE: {
    flame: 'characters_art/fx_rites/fireball/fireball_explosion_flipbook.png',
    fork: 'characters_art/fx_rites/arc_whip/arc_whip_impact_fork_4x4_v2.png',
    embers: 'characters_art/fx_rites/fireball/fireball_sparks_embers.png',
    trail: 'characters_art/fx_rites/fireball/fireball_trail_strip.png',
    marks: 'characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png',
  },
  NEW: {
    sigil: 'characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_starburst.png',
    haze: 'characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_haze.png',
  },
  CREDITS: {
    sigil: 'Original jagged starburst sigil mask (Sanctuary art).',
    marks: 'v2 count-mark atlas, reused in place (one copy).',
  },
  TIMING: {
    use: 'persistent jagged gold+blue fire starburst at the feet + 9 count marks + Ninth Peal (dark-blue spike flare, no ring)',
    flame: '12 fps 4×4 fireball explosion, masked by the sigil so only the star shows fire',
    fork: '10 fps 4×4, center faded so only cracks show',
    marks: '9 pips, 0.17 m, radius 0.30 m (inner star / spike bases), setCount 0–8; all 9 light during ninth()',
    ninth: '0.45s soft jagged sigil+haze+fork flare, scales 1.0→1.55, dark blue, no ring',
    scale: 'opts.scale default 0.8 (20% smaller); same textures, tighter footprint',
    look: 'darker blue fire (#1E4C8C/#3A78C0, cores cap #6AA8E0), gold only as faint hints, hazy D2 edges',
    motion: 'always on: flipbook fire, UV drift, per-spike warp, pulse, slow haze/fork/ember spin, flickering tendrils',
    call: 'setOn(auraOn includes knell), setCount(peal 0-8), ninth() on the toll',
  },
};

if (typeof module !== 'undefined' && module.exports) module.exports = KnellAuraFX;
if (typeof window !== 'undefined') window.KnellAuraFX = KnellAuraFX;
