/**
 * Sanctuary — Arc Whip v2 travelling lightning projectile. CC0, original.
 *
 * Brian lock: the skill leaves the weapon tip as a long zig-zag lightning
 * PROJECTILE (a whip motion on the clip, but the bolt itself detaches).
 * No latching, no tether, no lasso-to-target after the cast.
 * Look: chaotic sharp zig-zags + branching forks, light-blue, crisp white
 * core with a soft cyan glow (balance sharp and soft). KEEP BLACKS.
 *
 * Textures (4x4, 256 px cells, PREMULTIPLIED alpha, true-black edges, Additive):
 *   arc_whip_bolt_4x4_v2.png         looping bolt, 16 fps
 *   arc_whip_bolt_trail_4x4_v2.png   short fading zig-zag trail, 16 fps
 *   arc_whip_impact_fork_4x4_v2.png  one-shot impact burst, peak frame 0, 16 fps
 *
 * Clip (already pushed — do not overwrite):
 *   characters_art/fx_rites/arc_whip/arc_whip_swing.glb
 *   Release / crack frame 16 @ 0.55 s  (clip_meta.json)
 *
 * Usage:
 *   const fx = ArcWhipProjectileV2.create(THREE, scene, textures, opts);
 *   fx.playCast();                 // call when the swing clip starts
 *   fx.update(dt, { clipTime, targets });
 *   fx.dispose();
 *
 * Or spawn directly:
 *   fx.spawnBolt(originVec3, forwardVec3);
 *
 * opts.getWeaponTipWorld(out)  world position of the whip-tip socket
 * opts.getForward(out)         cast / facing direction (xz)
 * opts.getWhipMesh()           optional in-hand whip mesh; flashed then hidden
 *
 * NOT TESTED: never run in three.js or in the game. Only `node --check` was run.
 */
/* eslint-disable no-undef */

const ARC_WHIP_V2_DEFAULTS = {
  clipName: 'arc_whip_swing',
  releaseFrame: 16,
  releaseTimeS: 0.55,
  clipFps: 30,
  speedMps: 18,
  rangeM: 10,
  boltFps: 16,
  trailFps: 16,
  impactFps: 16,
  cols: 4,
  rows: 4,
  boltLength: 2.0,
  boltWidth: 0.55,
  trailSegs: 7,
  trailGap: 0.28,
  trailLifeS: 0.22,
  trailWidth: 0.38,
  trailLength: 0.55,
  impactSize: 1.35,
  impactLifeS: 1.0, // 16 frames at 16 fps
  flashHoldS: 0.08, // whip mesh stays visible this long after release, then hides
  tipSocketLocal: [0, 0, 3.3], // whip local +Z tip, metres (mesh_meta total reach)
  attachBone: 'mixamorig:RightHand',
  wanderAmp: 0.12, // slight lateral zig, not a seeking lasso
};

function _flipbookOffset(tex, frame, cols, rows) {
  const f = Math.max(0, Math.min(cols * rows - 1, frame | 0));
  const c = f % cols, r = (f / cols) | 0;
  tex.repeat.set(1 / cols, 1 / rows);
  tex.offset.set(c / cols, 1 - (r + 1) / rows);
}

function _prepTex(THREE, t) {
  const c = t.clone();
  c.needsUpdate = true;
  c.wrapS = c.wrapT = THREE.ClampToEdgeWrapping;
  c.generateMipmaps = false;
  c.minFilter = THREE.LinearFilter;
  if ('colorSpace' in c && THREE.SRGBColorSpace) c.colorSpace = THREE.SRGBColorSpace;
  c.premultiplyAlpha = false; // PNG is already premultiplied
  return c;
}

function _addMat(THREE, map) {
  return new THREE.MeshBasicMaterial({
    map,
    color: 0xffffff,
    transparent: true,
    depthWrite: false,
    premultipliedAlpha: true,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
  });
}

function _aimQuad(obj, origin, dir, up) {
  // Quad lies in a plane with local +X along dir (bolt flies tip-right in the sheet; polish 2026-11-10:
  // every bolt frame is a forward left->right zig-zag, head at the right, so +X alignment is unchanged).
  obj.position.copy(origin);
  const x = dir.clone().normalize();
  let y = up.clone().cross(x);
  if (y.lengthSq() < 1e-8) y = new (up.constructor)(0, 0, 1).cross(x);
  y.normalize();
  const z = x.clone().cross(y).normalize();
  obj.up.copy(z);
  const look = origin.clone().add(z);
  obj.lookAt(look);
  // after lookAt, +Z faces camera-ish; rotate so +X follows flight
  obj.rotateY(Math.PI / 2);
}

function create(THREE, scene, textures, opts) {
  const o = Object.assign({}, ARC_WHIP_V2_DEFAULTS, opts || {});
  const up = new THREE.Vector3(0, 1, 0);
  const tmpO = new THREE.Vector3();
  const tmpF = new THREE.Vector3();
  const tmpS = new THREE.Vector3();
  const live = [];
  let armed = false;
  let spawned = false;
  let clipT = 0;

  function hideWhip() {
    const m = o.getWhipMesh && o.getWhipMesh();
    if (m) m.visible = false;
  }
  function showWhip() {
    const m = o.getWhipMesh && o.getWhipMesh();
    if (m) m.visible = true;
  }

  function playCast() {
    armed = true;
    spawned = false;
    clipT = 0;
    showWhip();
  }

  function cancel() {
    armed = false;
    spawned = false;
    hideWhip();
  }

  function spawnBolt(origin, forward) {
    const dir = forward.clone();
    dir.y = 0;
    if (dir.lengthSq() < 1e-8) dir.set(0, 0, 1);
    dir.normalize();
    const side = new THREE.Vector3().crossVectors(up, dir).normalize();

    const group = new THREE.Group();
    scene.add(group);

    const boltTex = _prepTex(THREE, textures.bolt);
    const bolt = new THREE.Mesh(new THREE.PlaneGeometry(o.boltLength, o.boltWidth), _addMat(THREE, boltTex));
    group.add(bolt);

    const trails = [];
    for (let i = 0; i < o.trailSegs; i++) {
      const tx = _prepTex(THREE, textures.trail);
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(o.trailLength, o.trailWidth), _addMat(THREE, tx));
      mesh.visible = false;
      group.add(mesh);
      trails.push({ mesh, tex: tx, age: 999 });
    }

    const b = {
      group, bolt, boltTex, trails,
      origin: origin.clone(),
      pos: origin.clone(),
      dir, side,
      dist: 0,
      t: 0,
      seed: Math.random() * 100,
      dead: false,
      impact: null,
    };
    live.push(b);
    return b;
  }

  function _startImpact(b, pos) {
    b.dead = true;
    const tx = _prepTex(THREE, textures.impact);
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(o.impactSize, o.impactSize), _addMat(THREE, tx));
    mesh.position.copy(pos);
    scene.add(mesh);
    b.impact = { mesh, tex: tx, t: 0 };
    if (b.bolt) b.bolt.visible = false;
    for (const tr of b.trails) tr.mesh.visible = false;
  }

  function _hitTest(b, targets) {
    if (!targets || !targets.length) return null;
    const prev = b.pos;
    const next = tmpO.copy(b.origin).addScaledVector(b.dir, b.dist);
    // slight wander is applied after; use the actual pos
    const a = prev, c = b.pos;
    for (let i = 0; i < targets.length; i++) {
      const tgt = targets[i];
      if (!tgt || tgt.dead) continue;
      const p = tgt.position || tgt;
      const rad = tgt.radius != null ? tgt.radius : 0.45;
      const dx = p.x - c.x, dy = (p.y || 0) - c.y, dz = p.z - c.z;
      if (dx * dx + dy * dy + dz * dz <= rad * rad) return tgt;
      // segment-sphere rough test
      const vx = c.x - a.x, vz = c.z - a.z;
      const wx = p.x - a.x, wz = p.z - a.z;
      const denom = vx * vx + vz * vz || 1;
      let u = (wx * vx + wz * vz) / denom;
      if (u < 0) u = 0; else if (u > 1) u = 1;
      const hx = a.x + vx * u - p.x, hz = a.z + vz * u - p.z;
      if (hx * hx + hz * hz <= rad * rad) return tgt;
    }
    return null;
  }

  function update(dt, state) {
    const st = state || {};
    if (typeof st.clipTime === 'number') clipT = st.clipTime;

    if (armed && !spawned && clipT + 1e-4 >= o.releaseTimeS) {
      spawned = true;
      if (o.getWeaponTipWorld) o.getWeaponTipWorld(tmpO);
      else tmpO.set(0, 1.2, 0);
      if (o.getForward) o.getForward(tmpF);
      else tmpF.set(0, 0, 1);
      spawnBolt(tmpO.clone(), tmpF.clone());
    }
    if (armed && spawned && clipT >= o.releaseTimeS + o.flashHoldS) {
      hideWhip();
    }

    for (let i = live.length - 1; i >= 0; i--) {
      const b = live[i];
      if (b.impact) {
        b.impact.t += dt;
        const fr = Math.min(15, (b.impact.t * o.impactFps) | 0);
        _flipbookOffset(b.impact.tex, fr, o.cols, o.rows);
        const fade = 1 - Math.min(1, b.impact.t / o.impactLifeS);
        b.impact.mesh.material.opacity = fade;
        if (b.impact.t >= o.impactLifeS) {
          b.impact.mesh.removeFromParent();
          b.impact.mesh.geometry.dispose();
          b.impact.mesh.material.dispose();
          b.group.removeFromParent();
          live.splice(i, 1);
        }
        continue;
      }

      b.t += dt;
      b.dist += o.speedMps * dt;
      const wander = Math.sin(b.dist * 5.5 + b.seed) * o.wanderAmp
        + Math.sin(b.dist * 13.0 + b.seed * 2.1) * o.wanderAmp * 0.45;
      b.pos.copy(b.origin).addScaledVector(b.dir, b.dist).addScaledVector(b.side, wander);

      const fr = (b.t * o.boltFps) | 0;
      _flipbookOffset(b.boltTex, fr, o.cols, o.rows);
      _aimQuad(b.bolt, b.pos, b.dir, up);

      // trail: drop a segment every trailGap metres, fade by age
      for (const tr of b.trails) tr.age += dt;
      const want = Math.min(o.trailSegs, Math.floor(b.dist / o.trailGap));
      for (let k = 0; k < o.trailSegs; k++) {
        const tr = b.trails[k];
        if (k >= want) { tr.mesh.visible = false; continue; }
        const behind = (k + 1) * o.trailGap;
        const td = Math.max(0, b.dist - behind);
        const tw = Math.sin(td * 5.5 + b.seed) * o.wanderAmp * 0.8;
        tmpO.copy(b.origin).addScaledVector(b.dir, td).addScaledVector(b.side, tw);
        _aimQuad(tr.mesh, tmpO, b.dir, up);
        _flipbookOffset(tr.tex, ((b.t * o.trailFps) + k) | 0, o.cols, o.rows);
        const fade = Math.max(0, 1 - (behind / (o.trailSegs * o.trailGap)) - tr.age * 0.15);
        tr.mesh.visible = fade > 0.04;
        tr.mesh.material.opacity = fade * 0.7;
      }

      const hit = _hitTest(b, st.targets);
      if (hit) {
        _startImpact(b, b.pos);
        if (o.onHit) o.onHit(b.pos.clone(), hit);
        continue;
      }
      if (b.dist >= o.rangeM) {
        _startImpact(b, b.pos);
        if (o.onMaxRange) o.onMaxRange(b.pos.clone());
      }
    }
  }

  function dispose() {
    for (const b of live) {
      if (b.impact) {
        b.impact.mesh.removeFromParent();
        b.impact.mesh.geometry.dispose();
        b.impact.mesh.material.dispose();
      }
      b.group.removeFromParent();
    }
    live.length = 0;
    armed = false;
  }

  return { playCast, cancel, spawnBolt, update, dispose, defaults: o };
}

const ArcWhipProjectileV2 = {
  DEFAULTS: ARC_WHIP_V2_DEFAULTS,
  create,
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ArcWhipProjectileV2, ARC_WHIP_V2_DEFAULTS };
}

