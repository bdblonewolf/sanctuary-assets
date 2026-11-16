/**
 * Sanctuary — Knell Aura FX (v2). CC0 hook script.
 *
 * Persistent Knell aura, compact Diablo 2 Fanaticism-inspired look, built
 * as ground decals at the hero's feet for the game's isometric camera.
 * No ghost bell (dropped, Brian t497u). No bell-rune ring.
 *
 * Reused (do not copy; load from the live library paths):
 *   fireball/fireball_shockwave_ring.png     ground ring, idle pulse waves, Peal shockwave
 *   campfire_flame/campfire_flame_base_glow.png   soft pool at the feet (shader-softened)
 *   behest_banspere/swirl_wisps_4x4.png      low ground flicker (4×4, 12 fps)
 *   heavens_shrapnel/heavens_shrapnel_ground_glint.png   faint softened spark
 *   heavens_shrapnel/heavens_shrapnel_impact_burst_4x4.png   brief Peal ground flash
 *
 * New in this folder:
 *   knell_marks_2x1.png     512×256, two 256 cells: unlit | lit
 *                           R = fill mask, G = outline mask, A = coverage
 *
 * Everything is a horizontal PlaneGeometry at y ≈ 0.02–0.05 m, depthWrite
 * false, with renderOrder so the marks sit on top of the ring. No GLB.
 * The aura is centered under the character root: every ground layer sits at
 * local (0, y, 0). The 9 marks are equally spaced around that center.
 * attach() + update() copy the hero's world position only (not rotation).
 *
 * Usage:
 *   const fx = KnellAuraFX.create(THREE, scene, {
 *     shock, glow, wisps, glint, burst, marks,
 *   }, opts);
 *   fx.attach(heroObject3D);
 *   fx.setOn((player.auraOn || []).includes('knell'));
 *   fx.setCount(game.peal);       // 0–8, lights that many marks
 *   if (justTolled) fx.ninth();   // dark-blue shockwave + ground flash only
 *   fx.update(dt);
 *   fx.dispose();
 *
 * NOT TESTED: never run in three.js or in the game. Only `node --check`.
 */
/* eslint-disable no-undef */
const KNELL_AURA_DEFAULTS = {
  // metres — compact, at the feet (D2 aura, isometric). Hero GLB is ~1.87 m tall.
  ringDiameter: 1.40,
  glowSize: 1.28,             // wide ground pool, not a tight ball
  wispSize: 0.72,             // low ground flicker, not a rising column
  wispFps: 12,
  glintSize: 0.55,            // spread out; was a sharp 0.22 m star
  footY: 0.030,               // ring height
  glowY: 0.022,
  wispY: 0.026,
  glintY: 0.024,
  waveY: 0.032,
  shockY: 0.036,
  flashY: 0.038,
  flashSize: 0.90,
  ringSpin: 18,               // seconds per revolution, slow
  // idle pulse waves (same shock texture, expanding)
  pulseD0: 0.50,
  pulseD1: 1.56,
  pulseDur: 0.85,
  pulseEvery: 1.00,
  // 9 count marks ON the bright band of the 1.40 m ring (peak at ~0.71 of the plane radius)
  markSize: 0.17,
  markRadius: 0.50,
  markY: 0.048,               // above the ring so they read on top in iso
  // Ninth Peal (no bell)
  shockD0: 0.56,
  shockD1: 2.10,
  shockDur: 0.40,
  flashDur: 0.35,
  fadeOn: 0.18,
  fadeOff: 0.25,
  // tints (hex). Shader uses luma/channel masks. Premultiplied tint * a.
  tintAura: 0x4a9ad0,         // #4A9AD0 light-blue mid
  tintAuraHi: 0x8ec8f0,       // #8EC8F0 light-blue core (glow)
  tintPeal: 0x1a3a80,         // #1A3A80 dark blue (shock, flash)
  tintMarkUnlit: 0x1a3a80,    // #1A3A80 unlit fill (outline uses tintMarkOutline)
  tintMarkLit: 0x2e5ac0,      // #2E5AC0 brighter dark-blue fill
  tintMarkOutline: 0x0c1a40,  // #0C1A40 darker navy outline
  // glow / glint softness (1 = wide gaussian falloff, lower peak)
  glowSoft: 1.0,
  glowPeak: 0.28,             // was 0.45–0.80; stops the solid ball
  glintSoft: 1.0,
  glintPeak: 0.12,            // was 0.25–0.60; was a sharp center dot
  wispPeak: 0.22,
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

/** Luma+alpha mask tint, optional wide radial falloff to stop a solid core from balling up. */
function _tintMat(THREE, map, tintHex, extra) {
  const soft = (extra && extra.softFalloff) || 0;
  const rest = Object.assign({}, extra || {});
  delete rest.softFalloff;
  const mat = new THREE.ShaderMaterial(Object.assign({
    uniforms: {
      map: { value: map },
      tint: { value: new THREE.Color(tintHex) },
      opacity: { value: 1 },
      softFalloff: { value: soft },
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
      'uniform vec3 tint;',
      'uniform float opacity;',
      'uniform float softFalloff;',
      'varying vec2 vUv;',
      'void main(){',
      '  vec4 t = texture2D(map, vUv);',
      '  float luma = dot(t.rgb, vec3(0.2126, 0.7152, 0.0722));',
      '  float m = max(t.a, luma);',
      '  float r = length(vUv - vec2(0.5)) * 2.0;',
      // Wide gaussian + a smooth outer cutoff. softFalloff 0 = off, 1 = full.
      '  float soft = exp(-r * r / (2.0 * 0.52 * 0.52)) * (1.0 - smoothstep(0.82, 1.05, r));',
      '  float a = m * opacity * mix(1.0, soft, softFalloff);',
      '  gl_FragColor = vec4(tint * a, a);',
      '}',
    ].join('\n'),
  }, _commonMat(rest)));
  Object.defineProperty(mat, 'opacity', {
    get() { return this.uniforms.opacity.value; },
    set(v) { this.uniforms.opacity.value = v; },
  });
  return mat;
}

/** Mark atlas: R = fill, G = outline, A = coverage. Two tints so the outline stays darker. */
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
  const root = new THREE.Group();
  root.name = 'KnellAuraFX';
  root.visible = false;
  scene.add(root);

  const _tmp = new THREE.Vector3();
  let hero = null;
  let on = false;
  let count = 0;
  let t = 0;
  let fade = 0;
  let pulseAcc = 0.35;
  let pealT = -1;
  const waves = [];
  const owned = [];
  const markSlots = [];

  function _ground(map, tint, poly, size, y, order, matExtra) {
    const tex = _prepTex(THREE, map);
    const mat = _tintMat(THREE, tex, tint, Object.assign({ polygonOffsetFactor: poly }, matExtra || {}));
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(size, size), mat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.set(0, y, 0); // centered on the character root; no x/z offset
    mesh.renderOrder = order;
    mesh.frustumCulled = false;
    root.add(mesh);
    owned.push(tex, mat, mesh.geometry);
    return { mesh, tex, mat };
  }

  const glow = textures.glow
    ? _ground(textures.glow, o.tintAuraHi, -1, o.glowSize, o.glowY, 1, { softFalloff: o.glowSoft })
    : null;
  const glint = textures.glint
    ? _ground(textures.glint, o.tintAuraHi, -2, o.glintSize, o.glintY, 2, { softFalloff: o.glintSoft })
    : null;
  const wisps = textures.wisps
    ? _ground(textures.wisps, o.tintAura, -2, o.wispSize, o.wispY, 3)
    : null;
  if (wisps) _cellOffset(wisps.tex, 0, 4, 4);
  const ring = textures.shock
    ? _ground(textures.shock, o.tintAura, -3, 1, o.footY, 5)
    : null;
  const shock = textures.shock
    ? _ground(textures.shock, o.tintPeal, -4, 1, o.shockY, 6)
    : null;
  if (shock) shock.mesh.visible = false;
  const flash = textures.burst
    ? _ground(textures.burst, o.tintPeal, -4, o.flashSize, o.flashY, 7)
    : null;
  if (flash) { flash.mesh.visible = false; _cellOffset(flash.tex, 0, 4, 4); }

  if (textures.marks) {
    for (let i = 0; i < 9; i++) {
      const ang = (i / 9) * Math.PI * 2; // i=0 at +Z
      const tex = _prepTex(THREE, textures.marks);
      const mat = _markMat(THREE, tex, o.tintMarkUnlit, o.tintMarkOutline, { polygonOffsetFactor: -6 });
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(o.markSize, o.markSize), mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.x = Math.sin(ang) * o.markRadius;
      mesh.position.z = Math.cos(ang) * o.markRadius;
      mesh.position.y = o.markY;
      mesh.renderOrder = 10;
      mesh.frustumCulled = false;
      root.add(mesh);
      owned.push(tex, mat, mesh.geometry);
      _cellOffset(tex, 0, 2, 1);
      markSlots.push({ mesh, tex, mat });
    }
  }

  function _spawnWave() {
    if (!textures.shock) return;
    const w = _ground(textures.shock, o.tintAura, -3, 1, o.waveY, 4);
    w.mesh.rotation.z = Math.random() * Math.PI * 2;
    waves.push({ ...w, t: 0 });
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
    if (shock) shock.mesh.visible = true;
    if (flash) flash.mesh.visible = true;
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
      // Centered under the hero root. Copy world x, y, z so the ring stays
      // under the character on raised ground. Do not copy rotation or scale:
      // the ground planes stay world-flat when he turns or tilts.
      root.position.set(_tmp.x, _tmp.y, _tmp.z);
      root.quaternion.identity();
      root.scale.set(1, 1, 1);
    }
    const target = on ? 1 : 0;
    const fadeRate = on ? 1 / o.fadeOn : 1 / o.fadeOff;
    if (fade < target) fade = Math.min(target, fade + dt * fadeRate);
    else if (fade > target) fade = Math.max(target, fade - dt * fadeRate);
    if (fade <= 0 && !on && pealT < 0) { root.visible = false; return; }
    root.visible = true;

    const pul = _pulse(t);
    if (ring) {
      const d = o.ringDiameter * (0.985 + 0.025 * pul);
      ring.mesh.scale.set(d, d, 1);
      ring.mesh.rotation.z = t * (Math.PI * 2 / o.ringSpin);
      ring.mat.opacity = fade * (0.70 + 0.30 * pul);
    }
    if (glow) {
      glow.mat.opacity = fade * o.glowPeak * (0.85 + 0.15 * pul);
    }
    if (wisps) {
      const frame = (((t * o.wispFps) % 16) + 16) % 16;
      _cellOffset(wisps.tex, frame, 4, 4);
      wisps.mat.opacity = fade * o.wispPeak * (0.80 + 0.20 * pul);
    }
    if (glint) {
      glint.mat.opacity = fade * o.glintPeak * (0.80 + 0.20 * pul);
      glint.mesh.rotation.z = -t * (Math.PI * 2 / (o.ringSpin * 0.6));
    }
    for (let i = 0; i < markSlots.length; i++) {
      const lit = pealT >= 0 ? true : i < count;
      markSlots[i].mat.opacity = fade * (lit ? 1.0 : 0.92);
    }

    if (on && fade > 0.6 && textures.shock) {
      pulseAcc += dt;
      const period = o.pulseEvery * (0.85 + 0.22 * Math.sin(t * 0.73 + 0.5));
      if (pulseAcc >= period && waves.length < 3) { pulseAcc = 0; _spawnWave(); }
    }
    for (let i = waves.length - 1; i >= 0; i--) {
      const w = waves[i];
      w.t += dt;
      const u = w.t / o.pulseDur;
      if (u >= 1) {
        root.remove(w.mesh);
        w.tex.dispose(); w.mat.dispose(); w.mesh.geometry.dispose();
        waves.splice(i, 1);
        continue;
      }
      const d = o.pulseD0 + (o.pulseD1 - o.pulseD0) * u;
      w.mesh.scale.set(d, d, 1);
      w.mat.opacity = fade * (1 - u) * (0.50 + 0.25 * pul);
    }

    if (pealT >= 0) {
      pealT += dt;
      if (shock) {
        const su = Math.min(1, pealT / o.shockDur);
        const sd = o.shockD0 + (o.shockD1 - o.shockD0) * su;
        shock.mesh.scale.set(sd, sd, 1);
        shock.mat.opacity = (1 - su) * 0.95;
        shock.mesh.visible = su < 1;
      }
      if (flash) {
        const fu = Math.min(1, pealT / o.flashDur);
        _cellOffset(flash.tex, Math.min(15, (fu * 16) | 0), 4, 4);
        flash.mat.opacity = (1 - fu) * 0.70;
        const fs = 0.90 + 0.35 * fu;
        flash.mesh.scale.set(fs, fs, 1);
        flash.mesh.visible = fu < 1;
      }
      const doneAt = Math.max(o.shockDur, o.flashDur);
      if (pealT >= doneAt) {
        pealT = -1;
        if (shock) shock.mesh.visible = false;
        if (flash) flash.mesh.visible = false;
        _applyMarks(count);
      }
    }
  }

  function dispose() {
    hero = null;
    while (waves.length) {
      const w = waves.pop();
      root.remove(w.mesh);
      w.tex.dispose(); w.mat.dispose(); w.mesh.geometry.dispose();
    }
    for (const x of owned) if (x && x.dispose) x.dispose();
    owned.length = 0;
    markSlots.length = 0;
    if (root.parent) root.parent.remove(root);
  }

  return { attach, setOn, setCount, ninth, update, dispose, options: o, root, getCount: () => count };
}

const KnellAuraFX = {
  KNELL_AURA_DEFAULTS, create,
  REUSE: {
    shock: 'characters_art/fx_rites/fireball/fireball_shockwave_ring.png',
    glow: 'characters_art/fx_rites/campfire_flame/campfire_flame_base_glow.png',
    wisps: 'characters_art/fx_rites/behest_banspere/swirl_wisps_4x4.png',
    glint: 'characters_art/fx_rites/heavens_shrapnel/heavens_shrapnel_ground_glint.png',
    burst: 'characters_art/fx_rites/heavens_shrapnel/heavens_shrapnel_impact_burst_4x4.png',
  },
  NEW: {
    marks: 'characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png',
  },
  CREDITS: {
    marks: 'Original small rigid pips (Sanctuary art).',
  },
  TIMING: {
    use: 'persistent Knell aura at the feet (Fanaticism-inspired, light blue, isometric ground decals) + 9 count marks on the ring + Ninth Peal (dark-blue shockwave + ground flash). No bell.',
    ringSpin: '18s/rev',
    pulseWave: '0.85s, every ~1.0s jittered, 0.50→1.56 m, light blue',
    marks: '9 pips, 0.17 m, radius 0.50 m (on the bright ring band), one lights per hit (setCount 0–8); all 9 light during ninth()',
    ninthShock: '0.40s, 0.56→2.10 m, dark blue',
    ninthFlash: '0.35s, ground decal at the feet',
    call: 'setOn(auraOn includes knell), setCount(peal 0-8), ninth() on the toll',
  },
};

if (typeof module !== 'undefined' && module.exports) module.exports = KnellAuraFX;
if (typeof window !== 'undefined') window.KnellAuraFX = KnellAuraFX;
