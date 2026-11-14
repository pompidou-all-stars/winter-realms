/* Winter Realms — rendu 3D (prototype, activé par ?rendu=3d). Chargé à la demande par index.html.
   Lit l'état d'un terrain (Board de sim.js) comme draw() en 2D, et le dessine avec three.js.

   Projection : caméra ORTHOGRAPHIQUE inclinée (élévation E). Une case (x, y) du jeu est en (x, 0, y) dans le monde
   (X vers la droite, Z vers le bas de l'écran, Y vers le haut). À l'écran, un point du sol (gx, gz) à la hauteur h est en
     sx = ox + gx·s,   sy = oy + (gz·KY − h·KH)·s     avec s = taille d'une case en pixels, KY = sin E, KH = cos E.
   C'est la même formule que la 2D avec un tassement vertical KY : zoom, déplacement à deux doigts et toucher d'une case
   gardent la logique d'index.html (VUE.z, VUE.ox, VUE.oy).

   Modèles : assets/3d/ (fabriqués par les scripts Blender de art/, voir CLAUDE.md §15). */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';

export const E = 42 * Math.PI / 180, KY = Math.sin(E), KH = Math.cos(E), TOPM = 1.2;
/* les monstres sont agrandis en jeu pour rester lisibles sur téléphone (les rapports de taille entre eux sont gardés) */
const ECH_MONSTRES = 1.4;
const FAC = ['alliance', 'horde', 'sylvestres', 'nains', 'ombres'];
/* couleurs du terrain : mêmes valeurs que art/communs/factions.py (SOL, BIOME) */
const SOL = [['#5a9a45', '#66a64f'], ['#52683b', '#647b43'], ['#356d4b', '#407d58'], ['#68604d', '#77705b'], ['#493858', '#594568']];
const BIOME = [{bord: '#6b6253', terre: '#5a4632', detail: '#c8e08a', fleur: '#f4e27a'}, {bord: '#303b25', terre: '#4b3a2a', detail: '#c9a36a', fleur: '#e07a3a'},
  {bord: '#244a39', terre: '#3a3326', detail: '#d6e8a2', fleur: '#c79bff'}, {bord: '#4b4538', terre: '#4a4036', detail: '#d9c9a5', fleur: '#e0a34d'},
  {bord: '#382d4a', terre: '#2a2236', detail: '#a78cdb', fleur: '#7ff3ff'}];
const VOL = .5; // hauteur de vol des volants (cases)

export function creer(J) {
  /* J : tables et constantes du jeu (C, R, SP, EX, INF, DIRS, TW, CR, AURA_R, topY, rng) */
  const {C, R, SP, EX, INF, DIRS, TW, CR, AURA_R} = J;
  const canvas = document.createElement('canvas');
  canvas.id = 'main3d';
  canvas.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none';
  const renderer = new THREE.WebGLRenderer({canvas, antialias: true, powerPreference: 'high-performance'});
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#18251c');
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, .1, 200);
  cam.position.set(0, 60 * Math.sin(E), 60 * Math.cos(E)); cam.lookAt(0, 0, 0);

  /* lumières : ciel et sol (ambiance), soleil chaud avec ombres, contre-jour */
  scene.add(new THREE.HemisphereLight('#dfeaff', '#5a4632', 1.25));
  const soleil = new THREE.DirectionalLight('#fff1db', 2.3);
  soleil.position.set(C / 2 - 7, 14, R / 2 + 5); soleil.target.position.set(C / 2, 0, R / 2);
  soleil.castShadow = true;
  const sc = soleil.shadow.camera; sc.left = -12; sc.right = 12; sc.top = 13; sc.bottom = -13; sc.near = 1; sc.far = 40;
  soleil.shadow.mapSize.set(2048, 2048); soleil.shadow.bias = -.0006; soleil.shadow.normalBias = .02;
  scene.add(soleil, soleil.target);
  const contre = new THREE.DirectionalLight('#ffe2b8', .9); contre.position.set(C / 2 + 3, 8, -6); contre.target.position.set(C / 2, 0, R / 2);
  scene.add(contre, contre.target);

  /* ---------- modèles ---------- */
  const loader = new GLTFLoader(); loader.setMeshoptDecoder(MeshoptDecoder);
  const cache = new Map(), prets = new Map();
  function charger(url) {
    if (!cache.has(url)) cache.set(url, loader.loadAsync(url).then(g => {
      g.scene.traverse(o => {
        if (!o.isMesh) return;
        o.castShadow = true; o.receiveShadow = true;
        const m = o.material;
        if (m && m.name && m.name.startsWith('Lueur')) { m.emissiveIntensity = 1.6; o.castShadow = false }
        if (m) m.roughness = Math.max(.55, m.roughness);
      });
      prets.set(url, g); return g;
    }).catch(e => { console.warn('Modèle 3D introuvable : ' + url, e); prets.set(url, null); return null }));
    return cache.get(url);
  }
  /* noms des fichiers : voir art/LISEZMOI.md (tours/<faction>-<j>, monstres/<clé g de CR>) */
  const urlTour = k => `assets/3d/tours/${FAC[TW[k].faction]}-${k % 10}.glb`;
  const urlMonstre = k => `assets/3d/monstres/${CR[k].g}.glb`;
  /* plusieurs monstres peuvent partager un modèle (le Petit limon et la Gelée mutante) : le jeu le met à l'échelle de z */
  const echelleModele = k => { const ref = CR.find(c => c.g === CR[k].g); return Math.pow(CR[k].z / ref.z, 1.8) };
  /* undefined : en cours de chargement ; null : introuvable (le jeu affiche alors une forme de repli) */
  const modele = url => { if (!prets.has(url)) { charger(url); return undefined } return prets.get(url) };
  function precharger(factions) {
    const l = [charger('assets/3d/decor/portail.glb'), charger('assets/3d/decor/chateau.glb')];
    for (let k = 0; k < CR.length; k++) l.push(charger(urlMonstre(k)));
    for (const f of factions) for (let j = 0; j < 10; j++) l.push(charger(urlTour(f * 10 + j)));
    return Promise.all(l);
  }

  /* ---------- géométries et matériaux partagés ---------- */
  const G = {
    boite: new THREE.BoxGeometry(1, 1, 1), sphere: new THREE.SphereGeometry(1, 12, 8), ico: new THREE.IcosahedronGeometry(1, 0),
    anneau: new THREE.RingGeometry(.94, 1, 64).rotateX(-Math.PI / 2), disque: new THREE.CircleGeometry(1, 48).rotateX(-Math.PI / 2),
    cone: new THREE.ConeGeometry(1, 1, 5).translate(0, .5, 0), octa: new THREE.OctahedronGeometry(1, 0),
    fleche: new THREE.CylinderGeometry(.015, .015, .34, 5).rotateX(Math.PI / 2), pointe: new THREE.ConeGeometry(.035, .09, 5).rotateX(Math.PI / 2).translate(0, 0, .2),
    tranche: new THREE.TorusGeometry(.34, .04, 4, 16, 2.4).rotateX(-Math.PI / 2),
    dalle: new THREE.BoxGeometry(.97, .08, .97).translate(0, -.04, 0), tiret: new THREE.BoxGeometry(.2, .02, .09),
  };
  const mat = (col, o = {}) => new THREE.MeshStandardMaterial({color: col, roughness: .75, ...o});
  const transp = (col, op = .5) => new THREE.MeshBasicMaterial({color: col, transparent: true, opacity: op, depthWrite: false});
  const M = {or: mat('#ffd34a', {emissive: '#6a4a00'}), blanc: mat('#ffffff'), bois: mat('#6b4423'), fer: mat('#2b2b30', {metalness: .5, roughness: .4}),
    plume: mat('#f4efe0'), givre: mat('#bfe8ff', {emissive: '#3d8fd0', emissiveIntensity: .8}), arcane: mat('#e3b8ff', {emissive: '#9b4ad0', emissiveIntensity: 1}),
    etoile: mat('#ffe45e', {emissive: '#806000'})};

  /* ---------- plateau-diorama (refait quand la faction du terrain affiché change) ---------- */
  let plateau = null, plateauFaction = -1;
  const decorSeed = (x, y, f) => (x * 92821 + y * 68917 + f * 31337) % 997;
  function construirePlateau(f) {
    if (plateau) scene.remove(plateau);
    plateau = new THREE.Group(); plateauFaction = f;
    const bio = BIOME[f] || BIOME[0], sol = SOL[f] || SOL[0];
    const terre = new THREE.Mesh(G.boite, mat(bio.terre)); terre.scale.set(C + .1, .3, R + .1); terre.position.set(C / 2, -.2, R / 2); terre.receiveShadow = true;
    const falaise = new THREE.Mesh(G.boite, mat(bio.bord)); falaise.scale.set(C + .34, .4, R + .34); falaise.position.set(C / 2, -.5, R / 2);
    plateau.add(terre, falaise);
    const dalles = new THREE.InstancedMesh(G.dalle, mat('#ffffff', {roughness: .9}), C * R);
    dalles.receiveShadow = true;
    const m4 = new THREE.Matrix4(), col = new THREE.Color();
    let i = 0;
    for (let y = 0; y < R; y++) for (let x = 0; x < C; x++) {
      m4.makeTranslation(x + .5, 0, y + .5); dalles.setMatrixAt(i, m4);
      const s = decorSeed(x, y, f); col.set(sol[(x + y) % 2]).multiplyScalar(.93 + (s % 13) / 100); dalles.setColorAt(i++, col);
    }
    plateau.add(dalles);
    /* décor déterministe (aucun scintillement), comme en 2D : cailloux, herbes, fleurs */
    const pos = {caillou: [], herbe: [], fleur: []};
    for (let y = 0; y < R; y++) for (let x = 0; x < C; x++) {
      const s = decorSeed(x, y, f), fx = x + .2 + (s % 61) / 100, fy = y + .2 + ((s * 7) % 45) / 100;
      if (s % 11 === 0) pos.caillou.push([fx, fy, s]); else if (s % 7 === 0) pos.herbe.push([fx, fy, s]); else if (s % 5 === 0) pos.fleur.push([fx, fy, s]);
    }
    const inst = (geo, m, liste, fn) => {
      if (!liste.length) return; const im = new THREE.InstancedMesh(geo, m, liste.length); im.castShadow = true;
      liste.forEach((p, n) => { fn(m4, p); im.setMatrixAt(n, m4) }); plateau.add(im);
    };
    const q = new THREE.Quaternion(), v = new THREE.Vector3(), e = new THREE.Euler();
    inst(G.ico, mat('#b8b2a2'), pos.caillou, (m, [x, y, s]) => m.compose(v.set(x, .02, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.08, .05, .07)));
    const herbes = []; for (const p of pos.herbe) for (let k = -1; k <= 1; k++) herbes.push([p[0] + k * .045, p[1], k]);
    inst(G.cone, mat(bio.detail), herbes, (m, [x, y, k]) => m.compose(v.set(x, 0, y), q.setFromEuler(e.set(0, 0, k * .4)), new THREE.Vector3(.022, .12, .022)));
    const fleurs = []; for (const p of pos.fleur) for (let k = 0; k < 3; k++) fleurs.push([p[0] + k * .06, p[1] + (k % 2) * .05, k]);
    inst(G.sphere, mat(bio.fleur, {emissive: bio.fleur, emissiveIntensity: .15}), fleurs, (m, [x, y]) => m.compose(v.set(x, .03, y), q.identity(), new THREE.Vector3(.025, .018, .025)));
    scene.add(plateau);
  }

  /* portail et château */
  const decor = {portail: null, chateau: null, drapeau: null, col: ''};
  function placerDecor(b) {
    if (!decor.portail) { const g = modele('assets/3d/decor/portail.glb'); if (g) { decor.portail = g.scene.clone(true); decor.portail.position.set(SP[0] + .5, 0, SP[1] + .5); scene.add(decor.portail) } }
    if (!decor.chateau) {
      const g = modele('assets/3d/decor/chateau.glb');
      if (g) {
        decor.chateau = g.scene.clone(true); decor.chateau.position.set(EX[0] + .5, 0, EX[1] + .5); scene.add(decor.chateau);
        decor.chateau.traverse(o => { if (o.isMesh && o.material && o.material.name === 'Drapeau') { o.material = o.material.clone(); decor.drapeau = o.material } });
      }
    }
    if (decor.drapeau && decor.col !== b.col) { decor.col = b.col; decor.drapeau.color.set(b.col) }
  }

  /* ---------- chemin en pointillés animés ---------- */
  const NTIR = 240;
  const tirets = new THREE.InstancedMesh(G.tiret, transp('#ffffff', .42), NTIR); tirets.frustumCulled = false; scene.add(tirets);
  let cheminD = null, chemin = [], longueur = 0;
  function calculerChemin(b) {
    if (b.d === cheminD) return; cheminD = b.d; chemin = []; longueur = 0;
    let x = SP[0], y = SP[1]; chemin.push([x + .5, y + .5]);
    for (let n = 0; n < 200 && b.d[y][x] > 0 && b.d[y][x] < INF; n++) {
      for (const [dx, dy] of DIRS) { const a = x + dx, c = y + dy; if (a >= 0 && c >= 0 && a < C && c < R && b.d[c][a] == b.d[y][x] - 1) { x = a; y = c; break } }
      chemin.push([x + .5, y + .5]);
    }
    longueur = chemin.length - 1;
  }
  function dessinerChemin(t) {
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), un = new THREE.Vector3(1, 1, 1), e = new THREE.Euler();
    let n = 0; const pas = .46, dec = (t * .9) % pas;
    for (let d = dec; d < longueur && n < NTIR; d += pas) {
      const i = Math.floor(d), f = d - i, a = chemin[i], b = chemin[i + 1];
      m4.compose(v.set(a[0] + (b[0] - a[0]) * f, .015, a[1] + (b[1] - a[1]) * f), q.setFromEuler(e.set(0, b[0] !== a[0] ? 0 : Math.PI / 2, 0)), un);
      tirets.setMatrixAt(n++, m4);
    }
    tirets.count = n; tirets.instanceMatrix.needsUpdate = true;
  }

  /* ---------- tours ---------- */
  const tours = new Map();
  const pipGeo = new THREE.SphereGeometry(.035, 8, 6);
  /* formes de repli quand un modèle manque (règle d'art/LISEZMOI.md : le jeu fonctionne sans le fichier 3D) */
  function repliTour(k) {
    const g = new THREE.Group(), m = mat(TW[k].col);
    const socle = new THREE.Mesh(new THREE.CylinderGeometry(.38, .4, .1, 12), mat('#8a8f99')); socle.position.y = .05;
    const fut = new THREE.Mesh(new THREE.CylinderGeometry(.18, .24, .6, 10), m); fut.position.y = .4;
    for (const o of [socle, fut]) { o.castShadow = o.receiveShadow = true; g.add(o) }
    return g;
  }
  function repliMonstre(k) {
    const T = CR[k], h = .4 * Math.pow(T.z, 1.8), o = new THREE.Mesh(G.sphere, mat(T.col));
    o.scale.set(h * .45, h * .5, h * .45); o.position.y = h * .5; o.castShadow = true;
    const g = new THREE.Group(); g.add(o); return g;
  }
  /* échafaudage d'un chantier (construction ou amélioration, depuis la 2.4) */
  function echafaudage() {
    const g = new THREE.Group();
    for (const [x, z] of [[-.34, -.34], [.34, -.34], [-.34, .34], [.34, .34]]) { const p = new THREE.Mesh(G.boite, M.bois); p.scale.set(.04, 1.0, .04); p.position.set(x, .5, z); g.add(p) }
    for (const y of [.35, .75]) for (const [x, z, sx, sz] of [[0, -.34, .72, .03], [0, .34, .72, .03], [-.34, 0, .03, .72], [.34, 0, .03, .72]]) {
      const p = new THREE.Mesh(G.boite, M.bois); p.scale.set(sx, .03, sz); p.position.set(x, y, z); g.add(p);
    }
    const marteau = new THREE.Group(), manche = new THREE.Mesh(G.boite, M.bois), tete = new THREE.Mesh(G.boite, M.fer);
    manche.scale.set(.03, .22, .03); manche.position.y = .11; tete.scale.set(.12, .06, .06); tete.position.y = .22;
    marteau.add(manche, tete); marteau.position.set(.3, .78, .3); g.add(marteau); g.userData.marteau = marteau;
    g.traverse(o => { if (o.isMesh) o.castShadow = true });
    return g;
  }
  function creerTour(t, fantome) {
    const g = modele(urlTour(t.k)); if (g === undefined) return null;
    const o = g ? g.scene.clone(true) : repliTour(t.k);
    if (fantome) o.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; m.material.opacity = .55; m.material.depthWrite = false; m.castShadow = false } });
    const r = new THREE.Group(); r.add(o);
    const anim = {};
    for (const n of ['Tourelle', 'Cristal', 'Eclats', 'Flamme', 'Anneaux', 'Orbe', 'AnneauFlottant']) anim[n] = o.getObjectByName(n) || null;
    if (anim.Orbe) anim.orbeY = anim.Orbe.position.y;
    const pips = new THREE.Group(); r.add(pips);
    const etoiles = new THREE.Group(); for (let i = 0; i < 3; i++) etoiles.add(new THREE.Mesh(pipGeo, M.etoile)); etoiles.visible = false; r.add(etoiles);
    const chantier = fantome ? null : echafaudage(); if (chantier) { chantier.visible = false; r.add(chantier) }
    return {r, o, anim, pips, etoiles, chantier, k: t.k, lv: 0, ech: 1, ph: (t.x * 7 + t.y * 13) % 6};
  }
  function majTour(T, t, temps) {
    if (T.lv !== t.lv) {
      T.lv = t.lv; T.ech = 1 + .07 * (t.lv - 1);
      T.pips.clear(); for (let q = 0; q < t.lv; q++) { const p = new THREE.Mesh(pipGeo, M.or); p.position.set((q - (t.lv - 1) / 2) * .1, .03, .44); T.pips.add(p) }
    }
    /* chantier : échafaudage et marteau qui frappe ; à la construction, la tour sort de terre */
    const enChantier = t.b > 0, p = enChantier ? Math.max(0, Math.min(1, 1 - t.b / (t.bt || 1))) : 1;
    if (T.chantier) {
      T.chantier.visible = enChantier;
      if (enChantier) T.chantier.userData.marteau.rotation.z = -.4 + Math.abs(Math.sin(temps * 7)) * 1.1;
    }
    T.o.scale.set(T.ech, T.ech * (enChantier && t.lv === 1 ? .15 + .85 * p : 1), T.ech);
    const A = T.anim;
    if (A.Tourelle && t.a !== undefined) {
      A.Tourelle.rotation.y = Math.atan2(Math.cos(t.a), Math.sin(t.a));
      A.Tourelle.rotation.x = t.sw > 0 ? -t.sw * 1.5 : 0;
    }
    if (A.Cristal) A.Cristal.rotation.y = temps * 1.4 + T.ph;
    if (A.Eclats) A.Eclats.rotation.y = -temps * 1.1 + T.ph;
    if (A.Anneaux) A.Anneaux.rotation.y = temps * .8 + T.ph;
    if (A.AnneauFlottant) A.AnneauFlottant.rotation.y = temps * .6 + T.ph;
    if (A.Orbe) A.Orbe.position.y = A.orbeY + Math.sin(temps * 2.4 + T.ph) * .03;
    if (A.Flamme) { const f = Math.sin(temps * 13 + T.ph) * .5 + Math.sin(temps * 21 + T.ph) * .5; A.Flamme.scale.set(1 + f * .06, 1 + f * .16, 1 + f * .06) }
    T.etoiles.visible = t.stun > 0;
    if (t.stun > 0) T.etoiles.children.forEach((m, i) => { const a = temps * 6 + i * 2.1; m.position.set(Math.cos(a) * .25, 1.45, Math.sin(a) * .25) });
  }

  /* repères de sélection : cercle de portée, case dorée, tour fantôme */
  const portee = new THREE.Group();
  const porteeFond = new THREE.Mesh(G.disque, transp('#ffffff', .1)), porteeBord = new THREE.Mesh(G.anneau, transp('#ffffff', .75));
  porteeFond.renderOrder = porteeBord.renderOrder = 2; portee.add(porteeFond, porteeBord); portee.visible = false; scene.add(portee);
  const cadreCase = new THREE.Group(), cadreMat = transp('#ffd95e', .95);
  for (const [x, z, sx, sz] of [[0, -.48, 1, .05], [0, .48, 1, .05], [-.48, 0, .05, 1], [.48, 0, .05, 1]]) {
    const m = new THREE.Mesh(G.boite, cadreMat); m.scale.set(sx, .03, sz); m.position.set(x, .02, z); cadreCase.add(m);
  }
  cadreCase.visible = false; scene.add(cadreCase);
  const fantomes = new Map(); let fantome = null;

  /* ---------- monstres ---------- */
  const monstres = new Map();
  function creerMonstre(c) {
    const g = modele(urlMonstre(c.k)); if (g === undefined) return null;
    const T = CR[c.k];
    const o = g ? g.scene.clone(true) : repliMonstre(c.k); o.scale.setScalar(ECH_MONSTRES * (g ? echelleModele(c.k) : 1));
    if (T.inv) o.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true } });
    const r = new THREE.Group(); r.add(o);
    let mixer = null;
    if (g && g.animations.length) { mixer = new THREE.AnimationMixer(o); const a = mixer.clipAction(g.animations[0]); a.play(); a.time = (c.ph || 0) % g.animations[0].duration }
    /* halo au sol : ralenti (bleu), hâté (jaune), soigné (vert) */
    const halo = new THREE.Mesh(G.disque, transp('#8fdcff', .45)); halo.scale.setScalar(.22 * (T.z || 1)); halo.position.y = .01; halo.visible = false; r.add(halo);
    let aura = null;
    if (T.aura || T.heal) { aura = new THREE.Mesh(G.anneau, transp(T.aura ? '#ffe45e' : '#6fcf97', .55)); aura.scale.setScalar(AURA_R); aura.position.y = .02; r.add(aura) }
    r.position.set(c.x + .5 + (c.ox || 0), T.fly ? VOL : 0, c.y + .5 + (c.oy || 0));
    return {r, o, mixer, halo, aura, k: c.k, px: r.position.x, pz: r.position.z, yaw: 0, inv: !!T.inv};
  }
  function majMonstre(Mo, c, dt, temps) {
    const T = CR[c.k], x = c.x + .5 + (c.ox || 0), z = c.y + .5 + (c.oy || 0);
    const dx = x - Mo.px, dz = z - Mo.pz;
    if (dx * dx + dz * dz > 1e-6) {
      const cible = Math.atan2(dx, dz); let d = cible - Mo.yaw; d = Math.atan2(Math.sin(d), Math.cos(d));
      Mo.yaw += d * Math.min(1, dt * 10);
    }
    Mo.px = x; Mo.pz = z;
    Mo.r.position.set(x, T.fly ? VOL + Math.sin(temps * 3 + (c.ph || 0)) * .03 : 0, z);
    Mo.o.rotation.y = Mo.yaw;
    if (Mo.mixer) Mo.mixer.update(dt * (c.sl > 0 ? .55 : 1) * (T.s / 1.4));
    const glow = c.sl > 0 ? '#8fdcff' : c.h ? '#ffe45e' : c.hl ? '#6fcf97' : '';
    Mo.halo.visible = !!glow; if (glow) Mo.halo.material.color.set(glow);
    if (Mo.aura) Mo.aura.material.opacity = .35 + Math.sin(temps * 5) * .15;
    if (Mo.inv) { const op = c.hid ? .3 : .85; Mo.o.traverse(m => { if (m.isMesh) m.material.opacity = op }) }
  }
  const HAUT = k => (CR[k].fly ? VOL : 0) + .4 * Math.pow(CR[k].z, 1.8) * ECH_MONSTRES + .08;

  /* ---------- projectiles ---------- */
  const projs = new Map();
  function creerProj(p) {
    const skin = TW[p.k].skin, r = new THREE.Group();
    if (skin == 0) { r.add(new THREE.Mesh(G.fleche, M.bois), new THREE.Mesh(G.pointe, M.blanc)) }
    else if (skin == 1) { const m = new THREE.Mesh(G.sphere, M.fer); m.scale.setScalar(.08); m.castShadow = true; r.add(m) }
    else { const m = new THREE.Mesh(G.octa, skin == 2 ? M.givre : M.arcane); m.scale.set(.07, .07, .12); r.add(m) }
    scene.add(r); return {r, skin};
  }
  function majProj(Pj, p) {
    const q = Math.max(0, Math.min(1, 1 - Math.hypot(p.tx - p.x, p.ty - p.y) / (p.tot || 1)));
    let h = 1.0 + (.3 - 1.0) * q; if (Pj.skin == 1) h += Math.sin(q * Math.PI) * .8;
    Pj.r.position.set(p.x, h, p.y + .3 * (1 - q));
    Pj.r.rotation.y = Math.atan2(p.tx - p.x, p.ty - p.y);
    if (Pj.skin >= 2) Pj.r.rotation.z += .2;
  }

  /* ---------- effets ---------- */
  const effets = new Map();
  function creerEffet(f) {
    let o = null;
    switch (f.type) {
      case 'boom': o = new THREE.Mesh(G.sphere, transp(f.col, .55)); break;
      case 'ring': o = new THREE.Mesh(G.anneau, transp(f.col, 1)); break;
      case 'range': { o = new THREE.Group(); o.add(new THREE.Mesh(G.disque, transp(f.col, .12)), new THREE.Mesh(G.anneau, transp('#ffffff', .7))); break }
      case 'puff': { o = new THREE.Group(); for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(G.sphere, transp(f.col, .8)); m.userData.a = i * 1.05; o.add(m) } break }
      case 'flame': o = new THREE.Mesh(G.sphere, transp('#ffb347', .85)); break;
      case 'slash': o = new THREE.Mesh(G.tranche, transp('#ffffff', .9)); break;
      case 'bad': { o = new THREE.Mesh(G.boite, transp('#ff4d3d', .6)); o.scale.set(1, .02, 1); break }
      case 'zap': {
        const pts = []; const a = new THREE.Vector3(f.x, .3, f.y), b = new THREE.Vector3(f.x2, 1.1, f.y2 + .4);
        for (let i = 0; i <= 5; i++) { const p = a.clone().lerp(b, i / 5); if (i && i < 5) { p.x += (i % 2 ? 1 : -1) * .1; p.z += (i % 2 ? -.06 : .06) } pts.push(p) }
        o = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({color: '#ffe45e', transparent: true})); break;
      }
      default: return null;
    }
    o.renderOrder = 3; scene.add(o); return o;
  }
  function majEffet(o, f) {
    const p = 1 - f.t / f.d, fade = Math.max(0, 1 - p);
    const op = (m, v) => { if (m.material) m.material.opacity = v };
    switch (f.type) {
      case 'boom': o.position.set(f.x, .12, f.y); o.scale.set(f.r * (.25 + .75 * p), f.r * (.25 + .75 * p) * .45, f.r * (.25 + .75 * p)); op(o, fade * .55); break;
      case 'ring': o.position.set(f.x, .35, f.y); o.scale.setScalar(f.r * (.3 + .7 * p)); op(o, fade); break;
      case 'range': o.position.set(f.x, .03, f.y); o.scale.setScalar(f.r); op(o.children[0], fade * .12); op(o.children[1], fade * .7); break;
      case 'puff': o.position.set(f.x, .3, f.y); for (const m of o.children) { const a = m.userData.a; m.position.set(Math.cos(a) * p * .4, p * .2, Math.sin(a) * p * .4); m.scale.setScalar((1 - p) * .08 + .01); op(m, fade * .8) } break;
      case 'flame': o.position.set(f.x, .25 + (1 - p) * .4, f.y + (1 - p) * .3); o.scale.setScalar(.06 + .15 * p); o.material.color.set(p < .3 ? '#fff3a8' : p < .65 ? '#ffb347' : '#e4572e'); op(o, fade * .85); break;
      case 'slash': o.position.set(f.x, .35, f.y); o.rotation.y = -f.a - 2 + 2.6 * p; op(o, fade); break;
      case 'bad': o.position.set(f.x, .03, f.y); op(o, fade * .6); break;
      case 'zap': op(o, fade); break;
    }
  }

  /* ---------- synchronisation d'une collection d'objets du jeu avec leurs objets 3D ---------- */
  function synchro(map, liste, cle, creer, maj, retirer) {
    const vus = new Set();
    for (const it of liste) {
      const k = cle(it); vus.add(k);
      let o = map.get(k);
      if (o === undefined || o === null) { o = creer(it); if (!o) continue; map.set(k, o) }
      maj(o, it);
    }
    for (const [k, o] of map) if (!vus.has(k)) { retirer(o); map.delete(k) }
  }
  const retirerGroupe = o => scene.remove(o.r || o);

  /* ---------- image ---------- */
  let terrain = null, dernier = 0;
  function vider() {
    for (const m of [tours, monstres, projs, effets]) { for (const o of m.values()) retirerGroupe(o); m.clear() }
  }
  function dessiner(b, temps, VUE, cell, etat) {
    const dt = dernier ? Math.min(.1, Math.max(0, temps - dernier)) : 0; dernier = temps;
    if (b !== terrain) { vider(); terrain = b; cheminD = null }
    if (b.classId !== plateauFaction) construirePlateau(b.classId);
    placerDecor(b);
    if (decor.portail) decor.portail.traverse(o => { const m = /^Anneau(\d)$/.exec(o.name); if (m) o.rotation.y = temps * (2 + +m[1] * .6) * (m[1] % 2 ? 1 : -1) });
    calculerChemin(b); dessinerChemin(temps);

    synchro(tours, b.t, t => t.x + ',' + t.y + ',' + t.k, t => { const T = creerTour(t); if (T) { T.r.position.set(t.x + .5, 0, t.y + .5); scene.add(T.r) } return T },
      (T, t) => majTour(T, t, temps), retirerGroupe);
    synchro(monstres, b.cr, c => c.id, c => { const Mo = creerMonstre(c); if (Mo) scene.add(Mo.r); return Mo }, (Mo, c) => majMonstre(Mo, c, dt, temps), retirerGroupe);
    synchro(projs, b.pr, p => p.id, creerProj, majProj, retirerGroupe);
    synchro(effets, b.fx, f => f, creerEffet, majEffet, o => scene.remove(o));

    /* sélection : tour touchée ou projet de construction */
    const sel = etat.projet || etat.pick;
    portee.visible = cadreCase.visible = !!sel;
    if (sel) {
      const r = etat.projet ? TW[sel.k].r : etat.rng(sel);
      portee.position.set(sel.x + .5, .03, sel.y + .5); portee.scale.setScalar(r);
      porteeFond.material.color.set(etat.projet && !etat.ok ? '#ff4d3d' : '#ffffff');
      cadreCase.position.set(sel.x + .5, 0, sel.y + .5); cadreMat.color.set(etat.projet && !etat.ok ? '#ff6b5a' : '#ffd95e');
      cadreMat.opacity = etat.projet ? .7 + .25 * Math.sin(temps * 6) : .95;
    }
    const pk = etat.projet ? etat.projet.k : -1;
    if (fantome && (pk < 0 || fantome.k !== pk)) { scene.remove(fantome.r); fantome = null }
    if (pk >= 0) {
      if (!fantome) { fantome = fantomes.get(pk) || creerTour({k: pk, x: 0, y: 0}, true); if (fantome) { fantomes.set(pk, fantome); majTour(fantome, {lv: 1, a: .7}, temps); scene.add(fantome.r) } }
      if (fantome) fantome.r.position.set(etat.projet.x + .5, 0, etat.projet.y + .5);
    }

    /* caméra : mêmes zoom et décalage que la 2D (voir l'en-tête) */
    const s = cell * VUE.z;
    cam.left = -VUE.ox / s; cam.right = (VUE.w - VUE.ox) / s; cam.top = VUE.oy / s; cam.bottom = -(VUE.h - VUE.oy) / s;
    cam.updateProjectionMatrix();
    renderer.render(scene, cam);
  }
  function taille(w, h, dpr) { renderer.setPixelRatio(Math.min(2, dpr)); renderer.setSize(w, h, true) }
  /* point du monde (gx, gz au sol, hauteur h) → pixels du canevas */
  function versEcran(gx, gz, h, VUE, cell) { const s = cell * VUE.z; return {x: VUE.ox + gx * s, y: VUE.oy + (gz * KY - h * KH) * s} }

  /* compteurs pour les tests : objets 3D présents et appels de dessin de la dernière image */
  const etat = () => ({tours: tours.size, monstres: monstres.size, projectiles: projs.size, effets: effets.size, fantome: !!(fantome && fantome.r.parent),
    portee: portee.visible, dessins: renderer.info.render.calls, triangles: renderer.info.render.triangles});
  return {canvas, dessiner, taille, versEcran, precharger, hauteurMonstre: HAUT, KY, TOPM, renderer, etat};
}
