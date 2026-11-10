/**
 * Sanctuary — Grave Burst GROUND BURST FX (v1). CC0, original.
 * The stone cross bursts out of the ground: cracks race out on a ground decal, a dirt spray
 * and low dust billow rise, and VERY SMALL rocks are thrown radially + upward with gravity,
 * spin, one or two bounces, then fade/sink.
 *
 * Textures (4x4, 256 px cells, PREMULTIPLIED alpha, true-black edges, keep blacks):
 *   ground_crack_decal_flipbook.png  flat decal, NORMAL premultiplied blend, plays once (16 fps), holds last frame, fades
 *   dirt_burst_spray_flipbook.png    camera-facing, NORMAL premultiplied blend, 16 fps
 *   dust_puff_flipbook.png           camera-facing, NORMAL premultiplied blend (NOT additive), 12 fps
 *   rock_debris_atlas.png            16 single sprites (0-9 rocks, 10-12 chips, 13-15 pebble clusters)
 *
 * Timing (30 fps clips):
 *   - grave_burst_slam_v2: both hands hit the ground at frame 19 (0.633 s) -> call burst({small:true}) at the hands (optional).
 *   - Stone cross emerge: game keeps its existing ~1 s delay; call burst() at the frame the cross breaks the ground.
 *
 * Usage:
 *   const fx = GraveGroundBurst.create(THREE, scene, textures, opts);
 *   fx.burst(position, {small:false});   // position = THREE.Vector3 on the ground
 *   in your loop: fx.update(dt);         // dt seconds
 *   fx.dispose();
 *
 * NOT TESTED: never run in three.js or in the game. Only `node --check` was run on this file.
 */
/* eslint-disable no-undef */
const GROUND_BURST_DEFAULTS = {
  cols: 4, rows: 4,
  decalSize: 1.6, decalFps: 16, decalHold: 2.5, decalFade: 1.2,
  sprayWidth: 1.1, sprayHeight: 1.4, sprayFps: 16,
  dustSize: 1.1, dustFps: 12, dustCount: 3,
  rockCount: 34,            // very small rocks
  rockSizeMin: 0.018,       // metres (1.8 cm)
  rockSizeMax: 0.065,       // metres (6.5 cm); a few larger "chips" via rockBigChance
  rockBigChance: 0.12, rockBigSize: 0.09,
  speedMin: 1.6, speedMax: 4.2,  // m/s
  upMin: 0.55, upMax: 0.95,      // vertical share of launch dir
  gravity: 9.8, bounce: 0.28, friction: 0.55, maxBounces: 2,
  spinMax: 14,                   // rad/s
  rockLife: 1.6, rockFade: 0.35,
  smallScale: 0.45,              // burst({small:true}) for the hand-slam
};

function _flipbookOffset(tex, frame, cols, rows) {
  const f = Math.max(0, Math.min(cols * rows - 1, frame | 0));
  const c = f % cols, r = (f / cols) | 0;
  tex.repeat.set(1 / cols, 1 / rows);
  tex.offset.set(c / cols, 1 - (r + 1) / rows); // flipY=true default for PNG in three.js
}

function _prepTex(THREE, t) {
  const c = t.clone();
  c.needsUpdate = true;
  c.wrapS = c.wrapT = THREE.ClampToEdgeWrapping;
  c.generateMipmaps = false; c.minFilter = THREE.LinearFilter;
  if ('colorSpace' in c && THREE.SRGBColorSpace) c.colorSpace = THREE.SRGBColorSpace;
  c.premultiplyAlpha = false; // PNG already premultiplied
  return c;
}

function _premulMat(THREE, map, extra) {
  return new THREE.MeshBasicMaterial(Object.assign({
    map, transparent: true, depthWrite: false, premultipliedAlpha: true,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  }, extra || {}));
}

function _spriteMat(THREE, map) {
  return new THREE.SpriteMaterial({
    map, transparent: true, depthWrite: false, premultipliedAlpha: true,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
}

function create(THREE, scene, textures, opts) {
  const o = Object.assign({}, GROUND_BURST_DEFAULTS, opts || {});
  const live = [];

  function burst(pos, bopts) {
    const small = !!(bopts && bopts.small);
    const k = small ? o.smallScale : 1;
    const group = new THREE.Group(); group.position.copy(pos); scene.add(group);
    const b = { group, t: 0, items: [] };

    // decal (flat on ground, slight lift to avoid z-fight)
    const dTex = _prepTex(THREE, textures.crack);
    const decal = new THREE.Mesh(new THREE.PlaneGeometry(o.decalSize * k, o.decalSize * k), _premulMat(THREE, dTex, { polygonOffset: true, polygonOffsetFactor: -2 }));
    decal.rotation.x = -Math.PI / 2; decal.rotation.z = Math.random() * Math.PI * 2; decal.position.y = 0.01;
    group.add(decal);
    b.items.push({ kind: 'decal', obj: decal, tex: dTex });

    // dirt spray billboard
    const sTex = _prepTex(THREE, textures.spray);
    const spray = new THREE.Sprite(_spriteMat(THREE, sTex));
    spray.center.set(0.5, 0.04); spray.scale.set(o.sprayWidth * k, o.sprayHeight * k, 1);
    group.add(spray); b.items.push({ kind: 'spray', obj: spray, tex: sTex });

    // dust puffs
    for (let i = 0; i < (small ? 1 : o.dustCount); i++) {
      const tx = _prepTex(THREE, textures.dust);
      const s = new THREE.Sprite(_spriteMat(THREE, tx));
      s.center.set(0.5, 0.12);
      const a = Math.random() * Math.PI * 2, r = i === 0 ? 0 : 0.25 * k;
      s.position.set(Math.cos(a) * r, 0, Math.sin(a) * r);
      const sz = o.dustSize * k * (0.8 + Math.random() * 0.4); s.scale.set(sz, sz, 1);
      s.material.rotation = (Math.random() - 0.5) * 0.4;
      group.add(s); b.items.push({ kind: 'dust', obj: s, tex: tx, delay: i * 0.06 });
    }

    // very small rocks (sprites from the atlas, each with its own cell)
    const n = Math.round(o.rockCount * (small ? 0.4 : 1));
    for (let i = 0; i < n; i++) {
      const tx = _prepTex(THREE, textures.rocks);
      const cell = Math.random() < 0.2 ? 13 + ((Math.random() * 3) | 0) : ((Math.random() * 13) | 0);
      _flipbookOffset(tx, cell, o.cols, o.rows);
      const sp = new THREE.Sprite(_spriteMat(THREE, tx));
      const big = Math.random() < o.rockBigChance;
      const size = (big ? o.rockBigSize : o.rockSizeMin + Math.random() * (o.rockSizeMax - o.rockSizeMin)) * (small ? 0.8 : 1);
      sp.scale.set(size, size, 1);
      const ang = Math.random() * Math.PI * 2;
      const up = o.upMin + Math.random() * (o.upMax - o.upMin);
      const spd = (o.speedMin + Math.random() * (o.speedMax - o.speedMin)) * (big ? 0.6 : 1) * Math.sqrt(k);
      const h = Math.sqrt(1 - up * up);
      const r0 = Math.random() * 0.12 * k;
      sp.position.set(Math.cos(ang) * r0, 0.02, Math.sin(ang) * r0);
      group.add(sp);
      b.items.push({ kind: 'rock', obj: sp, tex: tx, size,
        v: new THREE.Vector3(Math.cos(ang) * h * spd, up * spd, Math.sin(ang) * h * spd),
        spin: (Math.random() * 2 - 1) * o.spinMax, bounces: 0, delay: Math.random() * 0.05, rest: false });
    }
    live.push(b);
    return b;
  }

  function update(dt) {
    for (let li = live.length - 1; li >= 0; li--) {
      const b = live[li]; b.t += dt; let alive = false;
      for (const it of b.items) {
        const t = b.t - (it.delay || 0); if (t < 0) { it.obj.visible = false; alive = true; continue; }
        it.obj.visible = true;
        if (it.kind === 'decal') {
          _flipbookOffset(it.tex, t * o.decalFps, o.cols, o.rows);
          const end = 16 / o.decalFps + o.decalHold;
          const fade = 1 - Math.min(1, Math.max(0, (t - end) / o.decalFade));
          it.obj.material.opacity = fade; if (fade > 0) alive = true;
        } else if (it.kind === 'spray' || it.kind === 'dust') {
          const fps = it.kind === 'spray' ? o.sprayFps : o.dustFps;
          const f = t * fps; _flipbookOffset(it.tex, f, o.cols, o.rows);
          it.obj.visible = f < 16; if (f < 16) alive = true;
        } else if (it.kind === 'rock') {
          if (!it.rest) {
            it.v.y -= o.gravity * dt;
            it.obj.position.addScaledVector(it.v, dt);
            it.obj.material.rotation += it.spin * dt;
            if (it.obj.position.y < it.size * 0.4) {
              it.obj.position.y = it.size * 0.4;
              if (it.bounces < o.maxBounces && Math.abs(it.v.y) > 0.6) {
                it.v.y = -it.v.y * o.bounce; it.v.x *= o.friction; it.v.z *= o.friction; it.spin *= 0.5; it.bounces++;
              } else { it.rest = true; it.v.set(0, 0, 0); }
            }
          }
          const fadeStart = o.rockLife - o.rockFade;
          const a = 1 - Math.min(1, Math.max(0, (t - fadeStart) / o.rockFade));
          it.obj.material.opacity = a; // premultiplied: opacity scales colour + alpha together
          if (a > 0) alive = true;
        }
      }
      if (!alive) { _disposeBurst(b); live.splice(li, 1); }
    }
  }

  function _disposeBurst(b) {
    scene.remove(b.group);
    for (const it of b.items) { it.tex.dispose(); it.obj.material.dispose(); if (it.obj.geometry && it.kind === 'decal') it.obj.geometry.dispose(); }
  }

  function dispose() { while (live.length) _disposeBurst(live.pop()); }

  return { burst, update, dispose, options: o };
}

const GraveGroundBurst = { GROUND_BURST_DEFAULTS, create,
  TIMING: { clip: 'grave_burst_slam_v2', fps: 30, handImpactFrame: 19, handImpactTime: 0.633, crossEmerge: 'engine-defined (existing ~1 s delay)' } };

if (typeof module !== 'undefined' && module.exports) module.exports = GraveGroundBurst;
if (typeof window !== 'undefined') window.GraveGroundBurst = GraveGroundBurst;
