/* Winter Realms — rendu 3D (par défaut depuis la 2.8). Chargé à la demande par index.html.
   Lit l'état d'un terrain (Board de sim.js) comme draw() en 2D, et le dessine avec three.js.

   Caméra « vue tactique » (2.15) : PERSPECTIVE, à hauteur fixe (élévation ELEV), qui regarde un point du sol (V.fx, V.fz).
   Une case (x, y) du jeu est en (x, 0, y) dans le monde (X vers la droite, Z vers le château, Y vers le haut).
   - le joueur la déplace en glissant le doigt (glisser : le sol reste sous le doigt), avec un peu d'élan au lâcher (lancer) ;
   - elle pivote autour du point regardé par huitièmes de tour (pivoter), en douceur ;
   - à la largeur du point regardé, on voit COLONNES cases ; le point regardé est au centre de la zone libre entre le bandeau
     du haut et le dock du bas (cadre).
   index.html passe par projeter (monde → pixels), echelle (pixels par case) et sol (pixels → case) pour la surcouche 2D,
   le toucher d'une case et les tests.

   Modèles : assets/3d/ (fabriqués par les scripts Blender de art/, voir CLAUDE.md §15). */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';

/* caméra tactique (2.15) : champ vertical, élévation, nombre de cases visibles en largeur au point regardé */
/* 2.26 : champ plus étroit (moins de déformation), caméra un peu plus redressée, et 20 % plus près (8,4 cases au lieu de 10,5) */
export const FOV = 34, ELEV = 44 * Math.PI / 180, COLONNES = 8.4;
/* les monstres sont agrandis en jeu pour rester lisibles sur téléphone (les rapports de taille entre eux sont gardés) */
const ECH_MONSTRES = 1.4;
/* 2.32 : les volants sont plus compacts (ailes déployées, ils masquaient le terrain et les autres monstres) ; 2.35 : deux fois moins grands (×0,65 → ×0,5) */
const ECH_VOLANTS = .5;
const echMonstre = k => ECH_MONSTRES * (CR[k].fly ? ECH_VOLANTS : 1);
const FAC = ['alliance', 'horde', 'sylvestres', 'nains', 'ombres'];
/* couleurs du terrain : mêmes valeurs que art/communs/factions.py (SOL, BIOME) */
/* thème hiver (2.9) : terrain enneigé (NEIGE ; TEINTE n'est plus utilisée depuis le paysage continu de la 2.26),
   bord en roche givrée, décor d'hiver (sapins enneigés, rochers, cristaux de glace). */
const NEIGE = ['#eef3f9', '#e2eaf3'];
const TEINTE = ['#5a9a45', '#a8652f', '#356d4b', '#8a7a5a', '#7a5a9a'];
const BIOME = [{bord: '#5b6b80', terre: '#8a9bb0', glace: '#bfe6ff'}, {bord: '#5f5a58', terre: '#958a86', glace: '#cfe9ff'},
  {bord: '#4f6670', terre: '#8aa3a8', glace: '#c8f2e6'}, {bord: '#625d58', terre: '#9a948c', glace: '#ffe2b8'},
  {bord: '#4e4660', terre: '#8e86a3', glace: '#d9c4ff'}];
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
  /* 2.26 : le terrain est entouré d'un paysage d'hiver (construirePlateau) qui se fond au loin dans la brume ;
     ciel en dégradé (nuit en haut, bleu gris à l'horizon) et montagnes lointaines, hors de la brume */
  const HORIZON = '#4a6385';
  scene.background = new THREE.Color('#16243a'); scene.fog = new THREE.Fog(HORIZON, 34, 85);
  {
    const geo = new THREE.SphereGeometry(300, 32, 16), p = geo.attributes.position, cols = [], haut = new THREE.Color('#0a1426'), bas = new THREE.Color(HORIZON), c = new THREE.Color();
    for (let i = 0; i < p.count; i++) { const t = Math.max(0, p.getY(i) / 300); c.copy(bas).lerp(haut, Math.pow(t, .55)); cols.push(c.r, c.g, c.b) }
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
    const ciel = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false}));
    ciel.position.set(C / 2, 0, R / 2); ciel.renderOrder = -1; scene.add(ciel);
    /* chaîne de montagnes tout autour, en silhouettes bleutées coiffées de neige */
    const cone = new THREE.ConeGeometry(1, 1, 7).translate(0, .5, 0), N = 40;
    const roc = new THREE.InstancedMesh(cone, new THREE.MeshBasicMaterial({color: '#2b3d5a', fog: false}), N), cime = new THREE.InstancedMesh(cone, new THREE.MeshBasicMaterial({color: '#aebcd0', fog: false}), N);
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), s = new THREE.Vector3();
    for (let i = 0; i < N; i++) {
      const a = i / N * Math.PI * 2 + ((i * 37) % 11) / 30, r = 120 + ((i * 53) % 29), h = 22 + ((i * 71) % 31), l = h * (.9 + ((i * 13) % 7) / 10);
      v.set(C / 2 + Math.cos(a) * r, -2, R / 2 + Math.sin(a) * r); q.setFromAxisAngle(s.set(0, 1, 0), i);
      m4.compose(v, q, s.set(l, h, l)); roc.setMatrixAt(i, m4);
      m4.compose(v.set(v.x, -2 + h * .62, v.z), q, s.set(l * .38, h * .38, l * .38)); cime.setMatrixAt(i, m4);
    }
    scene.add(roc, cime);
  }

  /* ---------- caméra tactique (2.15) ---------- */
  const cam = new THREE.PerspectiveCamera(FOV, 1, .5, 400);
  /* fx, fz : point regardé ; az : angle actuel (azC : visé, par huitièmes de tour) ; vx, vz : élan ; w, h : taille du canevas ;
     haut, bas : bandes couvertes par le bandeau et le dock (le point regardé est au centre de ce qui reste) */
  const V = {fx: C / 2, fz: R / 2 + 1.5, az: 0, azC: 0, vx: 0, vz: 0, w: 1, h: 1, haut: 0, bas: 0, cx: null, cz: null};
  /* 2.26 : le point regardé reste à au moins MARGE cases des bords du terrain : on ne voit jamais plus d'environ une case et demie
     de paysage sur le côté (avant : jusqu'à la moitié de l'écran) */
  const MARGE = Math.min(C / 2, Math.max(1, COLONNES / 2 - 1.2));
  const borner = () => { V.fx = Math.min(C - MARGE, Math.max(MARGE, V.fx)); V.fz = Math.min(R - MARGE, Math.max(MARGE, V.fz)) };
  function placerCamera() {
    const asp = V.w / V.h, D = COLONNES / (2 * Math.tan(FOV * Math.PI / 360) * asp), ch = D * Math.cos(ELEV);
    scene.fog.near = D + 8; scene.fog.far = D + 60;
    cam.aspect = asp; cam.setViewOffset(V.w, V.h, 0, V.h / 2 - (V.haut + (V.h - V.haut - V.bas) / 2), V.w, V.h);
    cam.position.set(V.fx + ch * Math.sin(V.az), D * Math.sin(ELEV), V.fz + ch * Math.cos(V.az)); cam.up.set(0, 1, 0); cam.lookAt(V.fx, 0, V.fz);
    cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  }
  placerCamera();
  /* taille du canevas et bandes couvertes par l'interface */
  function cadre(o) { Object.assign(V, o); placerCamera() }
  /* point du monde → pixels du canevas (z > 1 : derrière la caméra) */
  const vp = new THREE.Vector3(), droite = new THREE.Vector3();
  function projeter(x, y, z) { vp.set(x, y, z).project(cam); return {x: (vp.x + 1) / 2 * V.w, y: (1 - vp.y) / 2 * V.h, z: vp.z} }
  /* taille à l'écran (pixels) d'une case posée au point (x, z) du sol, à la hauteur y */
  function echelle(x, z, y = 0) { droite.setFromMatrixColumn(cam.matrixWorld, 0); const a = projeter(x, y, z), b = projeter(x + droite.x, y + droite.y, z + droite.z); return Math.hypot(b.x - a.x, b.y - a.y) }
  /* pixels du canevas → point du sol {x, z} (null au-dessus de l'horizon ; avec loin, un point lointain dans cette direction) */
  const rayon = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function sol(px, py, loin) {
    ndc.set(px / V.w * 2 - 1, 1 - py / V.h * 2); rayon.setFromCamera(ndc, cam); const o = rayon.ray.origin, d = rayon.ray.direction;
    if (d.y > -.02) { if (!loin) return null; const n = Math.hypot(d.x, d.z) || 1; return {x: o.x + d.x / n * 90, z: o.z + d.z / n * 90} }
    const t = -o.y / d.y; return {x: o.x + d.x * t, z: o.z + d.z * t};
  }
  /* le doigt passe de (x0, y0) à (x1, y1) : la caméra suit pour garder le même point du sol sous le doigt. Renvoie le déplacement. */
  function glisser(x0, y0, x1, y1) {
    V.cx = null; const a = sol(x0, y0), b = sol(x1, y1), ax = V.fx, az = V.fz; let dx, dz;
    if (a && b && Math.hypot(a.x - V.fx, a.z - V.fz) < 40) { dx = a.x - b.x; dz = a.z - b.z }
    else { const k = echelle(V.fx, V.fz) || 30, k2 = k * Math.sin(ELEV), c = Math.cos(V.az), s = Math.sin(V.az), du = (x1 - x0) / k, dv = (y1 - y0) / k2;
      dx = -du * c - dv * s; dz = du * s - dv * c }
    const n = Math.hypot(dx, dz); if (n > 1.5) { dx *= 1.5 / n; dz *= 1.5 / n }
    V.fx += dx; V.fz += dz; borner(); placerCamera(); return [V.fx - ax, V.fz - az];
  }
  /* un huitième de tour à gauche (-1) ou à droite (+1), animé dans dessiner */
  function pivoter(sens) { V.azC += sens * Math.PI / 4 }
  /* élan au lâcher (cases par seconde), amorti dans dessiner */
  function lancer(vx, vz) { const n = Math.hypot(vx, vz), m = n > 14 ? 14 / n : 1; V.vx = vx * m; V.vz = vz * m; V.cx = null }
  function viser(x, z) { V.fx = x; V.fz = z; V.vx = V.vz = 0; V.cx = null; borner(); placerCamera() }
  /* 2.35 : fait glisser la vue, en douceur, pour que le point (x, z) du sol arrive au pixel (px, py) du canevas
     (par exemple une tour choisie qui serait cachée par la fiche). Glisser le doigt ou viser annule le mouvement. */
  function amener(x, z, px, py) {
    const g = sol(px, py); if (!g) return;
    V.cx = Math.min(C - MARGE, Math.max(MARGE, V.fx + x - g.x)); V.cz = Math.min(R - MARGE, Math.max(MARGE, V.fz + z - g.z)); V.vx = V.vz = 0;
  }
  /* coins de la zone libre, au sol (pour le cadre de la vignette) */
  const empreinte = () => [[0, V.haut], [V.w, V.haut], [V.w, V.h - V.bas], [0, V.h - V.bas]].map(([x, y]) => sol(x, y, true));
  function bougerCamera(dt) {
    V.az = Math.abs(V.azC - V.az) > 1e-3 ? V.az + (V.azC - V.az) * Math.min(1, dt * 8) : V.azC;
    if (V.cx != null) { const f = Math.min(1, dt * 7); V.fx += (V.cx - V.fx) * f; V.fz += (V.cz - V.fz) * f; if (Math.hypot(V.cx - V.fx, V.cz - V.fz) < .01) { V.fx = V.cx; V.fz = V.cz; V.cx = null } }
    else if (Math.hypot(V.vx, V.vz) > .05) { V.fx += V.vx * dt; V.fz += V.vz * dt; borner(); const f = Math.exp(-dt * 4); V.vx *= f; V.vz *= f } else V.vx = V.vz = 0;
    placerCamera();
  }

  /* lumières : ciel et sol (ambiance), soleil chaud avec ombres, contre-jour */
  scene.add(new THREE.HemisphereLight('#e4efff', '#6a7890', 1.15));
  const soleil = new THREE.DirectionalLight('#fff6ea', 2.2);
  soleil.position.set(C / 2 - 6, 24, R / 2 + 6); /* 2.26 : plus haut, pour que l'ombre des sapins ne couvre pas le terrain */ soleil.target.position.set(C / 2, 0, R / 2);
  soleil.castShadow = true;
  /* les ombres couvrent le terrain et la forêt proche (2.26) */
  const sc = soleil.shadow.camera; sc.left = -19; sc.right = 19; sc.top = 20; sc.bottom = -20; sc.near = 1; sc.far = 60;
  soleil.shadow.mapSize.set(2048, 2048); soleil.shadow.bias = -.0006; soleil.shadow.normalBias = .02;
  scene.add(soleil, soleil.target);
  const contre = new THREE.DirectionalLight('#cfe0ff', .8); contre.position.set(C / 2 + 3, 8, -6); contre.target.position.set(C / 2, 0, R / 2);
  scene.add(contre, contre.target);

  /* ---------- style « peint » commun à tous les modèles (2.39) ----------
     1. ombres en paliers (matériau « toon ») : la lumière du soleil passe par 4 paliers au lieu d'un dégradé ;
     2. liseré de lumière froide sur les bords tournés à l'opposé de la caméra (rim light) : la silhouette se détache de la neige ;
     3. contour sombre d'épaisseur constante à l'écran (coque inversée, en pixels) : lisible même à 30 pixels par case.
     Désactivable avec ?style=0 (comparaison, ou téléphone trop lent). Les pièces lumineuses (« Lueur… ») ne sont pas touchées. */
  const STYLE = !/[?&]style=0\b/.test(location.search);
  const PALIERS = (() => { const d = new Uint8Array([90, 160, 215, 255]); const t = new THREE.DataTexture(d, d.length, 1, THREE.RedFormat);
    t.minFilter = t.magFilter = THREE.NearestFilter; t.generateMipmaps = false; t.needsUpdate = true; return t })();
  const RIM = {value: new THREE.Color('#d8e9ff').multiplyScalar(.42)};
  const RESOL = {value: new THREE.Vector2(1, 1)}, LARGEUR = {value: 1.15};   // épaisseur du contour, en pixels CSS
  const contourMat = new THREE.ShaderMaterial({
    uniforms: {uRes: RESOL, uLargeur: LARGEUR, uCouleur: {value: new THREE.Color('#1a2233')}},
    vertexShader: `#include <common>
#include <skinning_pars_vertex>
uniform vec2 uRes; uniform float uLargeur;
void main() {
#include <beginnormal_vertex>
#include <skinbase_vertex>
#include <skinnormal_vertex>
#include <begin_vertex>
#include <skinning_vertex>
#include <project_vertex>
  vec4 cn = projectionMatrix * vec4(normalize(normalMatrix * objectNormal), 0.0);
  vec2 d = cn.xy; float l = length(d); if (l > 1e-5) gl_Position.xy += d / l * uLargeur * gl_Position.w * 2.0 / uRes;
}`,
    fragmentShader: `uniform vec3 uCouleur; void main() { gl_FragColor = vec4(uCouleur, 1.0); }`,
    side: THREE.BackSide});
  const versToon = new Map();
  function toon(m) {
    if (versToon.has(m)) return versToon.get(m);
    const t = new THREE.MeshToonMaterial({name: m.name, color: m.color, map: m.map, normalMap: m.normalMap, normalScale: m.normalScale,
      vertexColors: m.vertexColors, emissive: m.emissive, emissiveMap: m.emissiveMap, emissiveIntensity: m.emissiveIntensity,
      transparent: m.transparent, opacity: m.opacity, alphaTest: m.alphaTest, side: m.side, gradientMap: PALIERS});
    t.onBeforeCompile = s => {
      s.uniforms.uRim = RIM;
      s.fragmentShader = 'uniform vec3 uRim;\n' + s.fragmentShader.replace('#include <opaque_fragment>', `{
  vec3 vd = isOrthographic ? vec3(0.0, 0.0, 1.0) : normalize(vViewPosition);
  float r = smoothstep(0.55, 0.95, 1.0 - saturate(dot(normal, vd)));
  outgoingLight += uRim * r * (0.4 + 0.6 * diffuseColor.rgb);
}
#include <opaque_fragment>`);
    };
    versToon.set(m, t); return t;
  }
  function styliser(racine) {
    const l = []; racine.traverse(o => { if (o.isMesh && !o.userData.contour) l.push(o) });
    for (const o of l) {
      if (!o.material || (o.material.name || '').startsWith('Lueur')) continue;
      o.material = toon(o.material);
      let c;
      if (o.isSkinnedMesh) { c = new THREE.SkinnedMesh(o.geometry, contourMat); c.bind(o.skeleton, o.bindMatrix) } else c = new THREE.Mesh(o.geometry, contourMat);
      c.userData.contour = true; c.castShadow = c.receiveShadow = false; c.frustumCulled = o.frustumCulled; o.add(c);
    }
  }
  /* avant chaque rendu : taille réelle du canevas (en pixels CSS) pour l'épaisseur du contour */
  const tailleTmp = new THREE.Vector2();
  function majContour(r) { r.getSize(tailleTmp); RESOL.value.copy(tailleTmp) }

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
      if (STYLE) styliser(g.scene);
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
    /* 2.40 : morts relevés, seulement si la Cour des Ossements (race 4) est en jeu */
    if (factions.includes(4)) l.push(charger('assets/3d/decor/mort-squelette.glb'), charger('assets/3d/decor/mort-colosse.glb'));
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

  /* ---------- terrain et paysage ----------
     2.26 : plus de « diorama » posé dans le vide. Le terrain de jeu est une partie d'un grand paysage d'hiver continu, que seule
     sa grille distingue : sol enneigé avec du relief tout autour (le terrain de jeu reste plat, sans effet sur le jeu), plaques
     d'herbe et de neige fondue, grands sapins, rochers. Tout est calculé à partir des coordonnées (bruit déterministe) :
     même paysage à chaque partie, aucun scintillement. Le paysage est construit une seule fois ; seul le petit décor posé sur
     le terrain de jeu dépend de la faction (construirePlateau). */
  let plateau = null, plateauFaction = -1, paysage = null;
  const decorSeed = (x, y, f) => (x * 92821 + y * 68917 + f * 31337) % 997;
  const hacher = (i, j) => { let h = (i * 374761393 + j * 668265263) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296 };
  function bruit(x, z) { const i = Math.floor(x), j = Math.floor(z), fx = x - i, fz = z - j, u = fx * fx * (3 - 2 * fx), w = fz * fz * (3 - 2 * fz);
    const a = hacher(i, j), b = hacher(i + 1, j), c = hacher(i, j + 1), d = hacher(i + 1, j + 1); return a + (b - a) * u + (c - a) * w + (a - b - c + d) * u * w }
  const fbm = (x, z) => bruit(x, z) * .55 + bruit(x * 2.1 + 5.3, z * 2.1 + 1.7) * .3 + bruit(x * 4.3 + 9.1, z * 4.3 + 3.3) * .15;
  const lisse = (a, b, t) => { t = Math.min(1, Math.max(0, (t - a) / (b - a))); return t * t * (3 - 2 * t) };
  /* distance au terrain de jeu (0 dessus) et hauteur du sol : plat sur le terrain, collines de plus en plus hautes en s'éloignant */
  const horsTerrain = (x, z) => Math.hypot(Math.max(0, -x, x - C), Math.max(0, -z, z - R));
  function hauteur(x, z) { const d = horsTerrain(x, z); if (d <= 0) return 0;
    return lisse(.8, 10, d) * (.5 + 3.4 * fbm(x * .07, z * .07)) + lisse(.3, 3, d) * .45 * (fbm(x * .4 + 20, z * .4) - .35) }
  /* plaques d'herbe (bords déchirés, neige qui reste par endroits) : 0 (neige) à 1 (herbe) ; plus rares et plus pâles sur le terrain de jeu */
  function herbeEn(x, z) { const sur = horsTerrain(x, z) <= 0, n1 = fbm(x * .16 + 3, z * .16 + 9), brise = lisse(.3, .7, bruit(x * 2.3 + 50, z * 2.3 + 50));
    return lisse(sur ? .68 : .62, sur ? .72 : .665, n1) * (.3 + .7 * brise) * (sur ? .5 : 1) }
  const TAILLE = 100, RES = 1024;
  /* couleurs du sol peintes dans une image (11 pixels par case) : neige, neige grise, herbe, terre, flaques de neige fondue */
  function texturePaysage() {
    const cv = document.createElement('canvas'); cv.width = cv.height = RES; const g = cv.getContext('2d'), im = g.createImageData(RES, RES), px = im.data;
    const neige = new THREE.Color(NEIGE[0]), neige2 = new THREE.Color('#d3dde9'), herbe = new THREE.Color('#4c6136'), herbe2 = new THREE.Color('#7d7b45'),
      fondue = new THREE.Color('#90a3ba'), bordF = new THREE.Color('#7f93ab'), terreC = new THREE.Color('#6f604f'), c = new THREE.Color(), h2 = new THREE.Color();
    for (let j = 0; j < RES; j++) for (let i = 0; i < RES; i++) {
      const x = C / 2 - TAILLE / 2 + (i + .5) / RES * TAILLE, z = R / 2 - TAILLE / 2 + (j + .5) / RES * TAILLE, sur = horsTerrain(x, z) <= 0;
      const n2 = fbm(x * .21 + 17, z * .21 + 2), n3 = bruit(x * 1.3, z * 1.3), n4 = bruit(x * 6.1, z * 6.1), vH = herbeEn(x, z);
      /* neige fondue : flaque gris bleu, au bord un peu plus sombre (neige mouillée) */
      const sf = sur ? .65 : .6, vF = lisse(sf, sf + .05, n2) * (sur ? .35 : .8), bord = lisse(sf - .04, sf, n2) * (1 - lisse(sf + .02, sf + .05, n2)) * (sur ? .2 : .5);
      c.copy(neige).lerp(neige2, n3 * .5 + n4 * .15).lerp(bordF, bord).lerp(fondue, vF * .8);
      c.lerp(h2.copy(herbe).lerp(herbe2, n3 * .7 + n4 * .3), vH);
      if (!sur && vH > .7) c.lerp(terreC, (vH - .7) * .9 * bruit(x * 2.7, z * 2.7));
      const o = (j * RES + i) * 4; px[o] = c.r * 255; px[o + 1] = c.g * 255; px[o + 2] = c.b * 255; px[o + 3] = 255;
    }
    g.putImageData(im, 0, 0);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  }
  /* grain de la neige : petite texture répétée, en relief (bumpMap) : cristaux, traces, petites bosses */
  function textureGrain() {
    const cv = document.createElement('canvas'); cv.width = cv.height = 256; const g = cv.getContext('2d');
    g.fillStyle = '#c8c8c8'; g.fillRect(0, 0, 256, 256);
    for (let n = 0; n < 3200; n++) { const x = hacher(n, 1) * 256, y = hacher(n, 2) * 256, r = .5 + hacher(n, 3) * 2.2, l = Math.floor(120 + hacher(n, 4) * 135);
      g.fillStyle = `rgba(${l},${l},${l},${.3 + hacher(n, 5) * .4})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill() }
    const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(TAILLE / 2.5, TAILLE / 2.5); return t;
  }
  function construirePaysage() {
    paysage = new THREE.Group();
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), e = new THREE.Euler();
    const inst = (geo, m, liste, fn) => {
      if (!liste.length) return; const im = new THREE.InstancedMesh(geo, m, liste.length); im.castShadow = true;
      liste.forEach((p, n) => { fn(m4, p); im.setMatrixAt(n, m4) }); paysage.add(im);
    };
    /* sol : une seule grande surface avec du relief autour du terrain, peinte (texturePaysage) et granuleuse (textureGrain) */
    const geo = new THREE.PlaneGeometry(TAILLE, TAILLE, 160, 160).rotateX(-Math.PI / 2).translate(C / 2, 0, R / 2), p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) p.setY(i, hauteur(p.getX(i), p.getZ(i)));
    geo.computeVertexNormals();
    const sol3d = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({map: texturePaysage(), bumpMap: textureGrain(), bumpScale: 1.6, roughness: .88}));
    sol3d.receiveShadow = true; paysage.add(sol3d);
    /* grille du terrain de jeu : c'est elle qui montre où l'on joue ; bord un peu plus marqué */
    const lignes = [];
    for (let x = 0; x <= C; x++) lignes.push(x, .012, 0, x, .012, R);
    for (let z = 0; z <= R; z++) lignes.push(0, .012, z, C, .012, z);
    const gl = new THREE.BufferGeometry(); gl.setAttribute('position', new THREE.Float32BufferAttribute(lignes, 3));
    paysage.add(new THREE.LineSegments(gl, new THREE.LineBasicMaterial({color: '#48638a', transparent: true, opacity: .42, depthWrite: false})));
    const bordM = transp('#2f4d76', .7);
    for (const [x, z, sx, sz] of [[C / 2, 0, C + .08, .08], [C / 2, R, C + .08, .08], [0, R / 2, .08, R], [C, R / 2, .08, R]]) {
      const b = new THREE.Mesh(G.boite, bordM); b.scale.set(sx, .01, sz); b.position.set(x, .014, z); paysage.add(b) }
    /* forêt de grands sapins enneigés autour du terrain, par bosquets avec des clairières ;
       petits près du bord (ils ne cachent jamais le jeu), de plus en plus grands en s'éloignant */
    const h = (a, b) => hacher(Math.round(a * 10), Math.round(b * 10)), arbres = [];
    for (let gz = -24; gz <= R + 24; gz += 1.6) for (let gx = -24; gx <= C + 24; gx += 1.6) {
      const x = gx + (h(gx, gz) - .5) * 1.3, z = gz + (h(gz + 3, gx) - .5) * 1.3, d = horsTerrain(x, z);
      if (d < 1.6 || d > 25 || fbm(x * .09 + 40, z * .09 + 11) < .47 || h(x + 7, z) < .3 || herbeEn(x, z) > .5) continue;
      arbres.push([x, hauteur(x, z) - .05, z, (.45 + .55 * lisse(1.6, 8, d)) * (1.4 + h(z, x + 5) * 1.7), h(x, z + 9) * 6]);
    }
    if (arbres.length) {
      const sapin = new THREE.ConeGeometry(1, 1, 9).translate(0, .5, 0), tronc = new THREE.CylinderGeometry(.5, .65, 1, 6).translate(0, .5, 0);
      const fut = new THREE.InstancedMesh(tronc, mat('#4f3726'), arbres.length), vert = new THREE.InstancedMesh(sapin, mat('#ffffff', {roughness: .85}), arbres.length * 3),
        neigeA = new THREE.InstancedMesh(sapin, mat('#f3f7fc', {roughness: .95}), arbres.length * 3), VERTS = ['#2b5240', '#244636', '#32604b', '#2a4a45'].map(x => new THREE.Color(x));
      const etages = [[.2, .62, .56], [.45, .47, .5], [.68, .32, .44]]; let k = 0;
      arbres.forEach(([x, y, z, t, a], n) => {
        q.setFromEuler(e.set(0, a, 0)); fut.setMatrixAt(n, m4.compose(v.set(x, y, z), q, new THREE.Vector3(.1 * t, .4 * t, .1 * t)));
        for (const [b, r, hh] of etages) {
          vert.setMatrixAt(k, m4.compose(v.set(x, y + b * t, z), q, new THREE.Vector3(r * t, hh * t, r * t))); vert.setColorAt(k, VERTS[(n + k) % 4]);
          neigeA.setMatrixAt(k++, m4.compose(v.set(x, y + (b + hh * .48) * t, z), q, new THREE.Vector3(r * .58 * t, hh * .54 * t, r * .58 * t)));
        }
      });
      for (const o of [fut, vert, neigeA]) { o.castShadow = true; paysage.add(o) }
    }
    /* rochers enneigés et touffes d'herbe sèche dans les plaques d'herbe, autour du terrain */
    const rocs = [], touffes = [];
    for (let n = 0; n < 150; n++) { const x = -20 + hacher(n, 31) * (C + 40), z = -20 + hacher(n, 47) * (R + 40), d = horsTerrain(x, z);
      if (d >= 1.2 && d <= 22) rocs.push([x, hauteur(x, z), z, .25 + hacher(n, 59) * .75, hacher(n, 61) * 6]) }
    inst(G.ico, mat('#7a8492', {flatShading: true}), rocs, (m, [x, y, z, s, a]) => m.compose(v.set(x, y + s * .2, z), q.setFromEuler(e.set(a, a * 2, 0)), new THREE.Vector3(s, s * .7, s * .9)));
    inst(G.ico, mat('#f2f6fb'), rocs, (m, [x, y, z, s, a]) => m.compose(v.set(x, y + s * .58, z), q.setFromEuler(e.set(0, a, 0)), new THREE.Vector3(s * .78, s * .26, s * .7)));
    for (let n = 0; n < 5000; n++) { const x = -14 + hacher(n, 71) * (C + 28), z = -14 + hacher(n, 73) * (R + 28);
      if (horsTerrain(x, z) >= .3 && herbeEn(x, z) > .45) touffes.push([x, hauteur(x, z), z, .7 + hacher(n, 79), hacher(n, 83) * 6, n % 3]) }
    for (const [ton, coul] of [[0, '#6f7a42'], [1, '#8a8a4e'], [2, '#56683c']])
      inst(G.cone, mat(coul), touffes.filter(t => t[5] === ton), (m, [x, y, z, s, a]) => m.compose(v.set(x, y - .02, z), q.setFromEuler(e.set(0, a, .25)), new THREE.Vector3(.05 * s, .22 * s, .05 * s)));
    scene.add(paysage);
  }
  /* petit décor posé sur le terrain de jeu (il ne gêne pas la lecture), propre à la faction du terrain affiché */
  function construirePlateau(f) {
    if (!paysage) construirePaysage();
    if (plateau) scene.remove(plateau);
    plateau = new THREE.Group(); plateauFaction = f;
    const bio = BIOME[f] || BIOME[0], m4 = new THREE.Matrix4();
    /* décor déterministe (aucun scintillement) : rochers enneigés, sapins, congères, cristaux de glace */
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
    // rochers gris givrés, coiffés de neige
    inst(G.ico, mat('#8c939e'), pos.caillou, (m, [x, y, s]) => m.compose(v.set(x, .02, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.09, .06, .08)));
    inst(G.ico, mat('#f4f8fc'), pos.caillou, (m, [x, y, s]) => m.compose(v.set(x, .055, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.07, .025, .06)));
    // petits sapins : tronc, feuillage vert sombre, pointe de neige (plus grands depuis la 2.26)
    inst(G.boite, mat('#5a3d26'), pos.herbe, (m, [x, y]) => m.compose(v.set(x, .045, y), q.identity(), new THREE.Vector3(.035, .09, .035)));
    inst(G.cone, mat('#2f5a45'), pos.herbe, (m, [x, y, s]) => m.compose(v.set(x, .07, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.15, .32, .15)));
    inst(G.cone, mat('#f4f8fc'), pos.herbe, (m, [x, y, s]) => m.compose(v.set(x, .25, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.08, .16, .08)));
    // congères (bosses de neige) et cristaux de glace
    inst(G.sphere, mat('#f6f9fd', {roughness: .95}), pos.fleur, (m, [x, y, s]) => m.compose(v.set(x, 0, y), q.setFromEuler(e.set(0, s, 0)), new THREE.Vector3(.14, .045, .09)));
    const cristaux = pos.fleur.filter(p => p[2] % 3 === 0);
    inst(G.octa, mat(bio.glace, {emissive: bio.glace, emissiveIntensity: .25, roughness: .2}), cristaux, (m, [x, y, s]) => m.compose(v.set(x + .12, .06, y), q.setFromEuler(e.set(.3, s, .2)), new THREE.Vector3(.03, .07, .03)));
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

  /* ---------- flocons (thème hiver, 2.9) : 260 points qui tombent en boucle au-dessus du plateau ---------- */
  /* 2.30 : la position de chaque flocon ne dépend que du temps (x0, y0 : position de départ), plus de l'enchaînement des images :
     même mouvement à l'écran, mais deux captures au même instant sont identiques (comparaison visuelle des tests) */
  const NF = 260, flocons = new Float32Array(NF * 3), vitesses = new Float32Array(NF), x0 = new Float32Array(NF), y0 = new Float32Array(NF);
  for (let i = 0; i < NF; i++) { const h = (i * 2654435761 >>> 0) / 4294967296, h2 = (i * 40503 % 997) / 997, h3 = (i * 7919 % 389) / 389;
    x0[i] = flocons[i * 3] = -1 + h * (C + 2); y0[i] = flocons[i * 3 + 1] = h2 * 6; flocons[i * 3 + 2] = -1 + h3 * (R + 2); vitesses[i] = .35 + h2 * .35 }
  const geoF = new THREE.BufferGeometry(); geoF.setAttribute('position', new THREE.BufferAttribute(flocons, 3));
  const neige = new THREE.Points(geoF, new THREE.PointsMaterial({color: '#ffffff', size: .07, transparent: true, opacity: .85, depthWrite: false}));
  neige.frustumCulled = false; neige.renderOrder = 4; scene.add(neige);
  /* chute à vitesse constante en boucle sur 6 unités de hauteur ; balancement latéral = intégrale de sin(0,8 t + i) × 0,08 */
  function fairePleuvoir(temps) {
    for (let i = 0; i < NF; i++) {
      let y = (y0[i] - vitesses[i] * temps) % 6; if (y < 0) y += 6;
      flocons[i * 3 + 1] = y; flocons[i * 3] = x0[i] - .1 * Math.cos(temps * .8 + i);
    }
    geoF.attributes.position.needsUpdate = true;
  }

  /* ---------- chemin en pointillés animés ---------- */
  const NTIR = 240;
  const tirets = new THREE.InstancedMesh(G.tiret, transp('#3d5f8a', .5), NTIR); tirets.frustumCulled = false; scene.add(tirets);
  /* points de passage en ligne droite (diagonales comprises, depuis la 2.25) et distance cumulée à chacun */
  let cheminD = null, chemin = [], cumul = [0], longueur = 0;
  function calculerChemin(b) {
    if (b.d === cheminD) return; cheminD = b.d;
    chemin = J.chemin(b).map(([x, y]) => [x + .5, y + .5]); cumul = [0];
    for (let i = 1; i < chemin.length; i++) cumul.push(cumul[i - 1] + Math.hypot(chemin[i][0] - chemin[i - 1][0], chemin[i][1] - chemin[i - 1][1]));
    longueur = cumul[cumul.length - 1];
  }
  function dessinerChemin(t) {
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), un = new THREE.Vector3(1, 1, 1), e = new THREE.Euler();
    let n = 0, i = 0; const pas = .46, dec = (t * .9) % pas;
    for (let d = dec; d < longueur && n < NTIR; d += pas) {
      while (cumul[i + 1] < d) i++;
      const a = chemin[i], b = chemin[i + 1], f = (d - cumul[i]) / ((cumul[i + 1] - cumul[i]) || 1);
      m4.compose(v.set(a[0] + (b[0] - a[0]) * f, .015, a[1] + (b[1] - a[1]) * f), q.setFromEuler(e.set(0, -Math.atan2(b[1] - a[1], b[0] - a[0]), 0)), un);
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
    if (fantome) o.traverse(m => { if (m.userData.contour) m.visible = false; else if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; m.material.opacity = .55; m.material.depthWrite = false; m.castShadow = false } });
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
  const porteeFond = new THREE.Mesh(G.disque, transp('#3d6fb0', .12)), porteeBord = new THREE.Mesh(G.anneau, transp('#25486f', .8));
  porteeFond.renderOrder = porteeBord.renderOrder = 2; portee.add(porteeFond, porteeBord); portee.visible = false; scene.add(portee);
  const cadreCase = new THREE.Group(), cadreMat = transp('#ffd95e', .95);
  for (const [x, z, sx, sz] of [[0, -.48, 1, .05], [0, .48, 1, .05], [-.48, 0, .05, 1], [.48, 0, .05, 1]]) {
    const m = new THREE.Mesh(G.boite, cadreMat); m.scale.set(sx, .03, sz); m.position.set(x, .02, z); cadreCase.add(m);
  }
  cadreCase.visible = false; scene.add(cadreCase);
  /* 2.31 : cadres des tours choisies pour une amélioration en lot (un par tour, jusqu'à 10) */
  const cadresLot = [], lotMat = transp('#ffd95e', .8);
  function cadreLot(i) {
    while (cadresLot.length <= i) { const c = cadreCase.clone(true); c.traverse(m => { if (m.isMesh) m.material = lotMat }); c.visible = false; scene.add(c); cadresLot.push(c) }
    return cadresLot[i];
  }
  const fantomes = new Map(); let fantome = null;

  /* ---------- monstres ---------- */
  const monstres = new Map();
  function creerMonstre(c) {
    const g = modele(urlMonstre(c.k)); if (g === undefined) return null;
    const T = CR[c.k];
    const o = g ? g.scene.clone(true) : repliMonstre(c.k); o.scale.setScalar(echMonstre(c.k) * (g ? echelleModele(c.k) : 1));
    if (T.inv) o.traverse(m => { if (m.userData.contour) m.visible = false; else if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true } });
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
  const HAUT = k => (CR[k].fly ? VOL : 0) + .4 * Math.pow(CR[k].z, 1.8) * echMonstre(k) + .08;

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
      case 'range': { o = new THREE.Group(); o.add(new THREE.Mesh(G.disque, transp(f.col, .12)), new THREE.Mesh(G.anneau, transp('#25486f', .7))); break }
      case 'puff': { o = new THREE.Group(); for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(G.sphere, transp(f.col, .8)); m.userData.a = i * 1.05; o.add(m) } break }
      case 'flame': o = new THREE.Mesh(G.sphere, transp('#ffb347', .85)); break;
      case 'slash': o = new THREE.Mesh(G.tranche, transp('#ffffff', .9)); break;
      case 'bad': { o = new THREE.Mesh(G.boite, transp('#ff4d3d', .6)); o.scale.set(1, .02, 1); break }
      case 'zap': {
        /* 2.40 : couleur (f.col), trait droit (f.ln : tir en ligne, rayon), éclair tombé du ciel (f.ciel) */
        const pts = []; const a = f.ciel ? new THREE.Vector3(f.x2, 3.2, f.y2) : new THREE.Vector3(f.x, f.ln ? .7 : .3, f.y), b = new THREE.Vector3(f.x2, f.ciel ? .3 : f.ln ? .45 : 1.1, f.y2 + (f.ln || f.ciel ? 0 : .4));
        for (let i = 0; i <= 5; i++) { const p = a.clone().lerp(b, i / 5); if (i && i < 5 && !f.ln) { p.x += (i % 2 ? 1 : -1) * .1; p.z += (i % 2 ? -.06 : .06) } pts.push(p) }
        o = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({color: f.col || '#ffe45e', transparent: true})); break;
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
  /* 2.40 : morts relevés par la Cour des Ossements (squelette en armure, colosse d'os) et mines de Hautroc */
  const allies = new Map(), mines = new Map(), matMine = transp('#ff9a3d', .85);
  /* 2.40 : modèles à part (decor/mort-squelette, decor/mort-colosse), indépendants des monstres de CR */
  const URL_MORT = {sq: 'assets/3d/decor/mort-squelette.glb', co: 'assets/3d/decor/mort-colosse.glb'};
  function creerMort(c) {
    const g = modele(URL_MORT[c.m]); if (g === undefined) return null;
    let o;
    if (g) o = g.scene.clone(true);
    else { o = new THREE.Mesh(new THREE.CylinderGeometry(.06, .08, c.m === 'co' ? .6 : .4, 8), mat('#d8cfb6')); o.position.y = c.m === 'co' ? .3 : .2 }
    const r = new THREE.Group(); r.add(o); r.position.set(c.x + .5, 0, c.y + .5); scene.add(r);
    return {r, o, px: r.position.x, pz: r.position.z, yaw: 0, ph: (c.x * 7 + c.y * 13) % 6, y0: o.position.y};
  }
  function majMort(Mo, c, dt, temps) {
    const x = c.x + .5, z = c.y + .5, dx = x - Mo.px, dz = z - Mo.pz;
    if (dx * dx + dz * dz > 1e-6) { let d = Math.atan2(dx, dz) - Mo.yaw; d = Math.atan2(Math.sin(d), Math.cos(d)); Mo.yaw += d * Math.min(1, dt * 10) }
    Mo.px = x; Mo.pz = z; Mo.r.position.set(x, 0, z); Mo.o.rotation.y = Mo.yaw;
    /* démarche saccadée de mort-vivant : petits bonds et roulis */
    Mo.o.position.y = Mo.y0 + Math.abs(Math.sin(temps * 7 + Mo.ph)) * .015; Mo.o.rotation.z = Math.sin(temps * 7 + Mo.ph) * .06;
  }
  function creerMine() { const r = new THREE.Group(), d = new THREE.Mesh(G.disque, matMine); d.scale.setScalar(.22); r.add(d); const c = new THREE.Mesh(G.octa, mat('#ffb347', {emissive: '#ff6a1a', emissiveIntensity: .8})); c.scale.setScalar(.07); c.position.y = .08; r.add(c); r.renderOrder = 2; scene.add(r); return {r, c} }
  function vider() {
    for (const m of [tours, monstres, projs, effets, allies, mines]) { for (const o of m.values()) retirerGroupe(o); m.clear() }
  }
  function dessiner(b, temps, etat) {
    const dt = dernier ? Math.min(.1, Math.max(0, temps - dernier)) : 0; dernier = temps;
    if (b !== terrain) { vider(); terrain = b; cheminD = null }
    if (b.classId !== plateauFaction) construirePlateau(b.classId);
    placerDecor(b);
    if (decor.portail) decor.portail.traverse(o => { const m = /^Anneau(\d)$/.exec(o.name); if (m) o.rotation.y = temps * (2 + +m[1] * .6) * (m[1] % 2 ? 1 : -1) });
    calculerChemin(b); dessinerChemin(temps); fairePleuvoir(temps);

    synchro(tours, b.t, t => t.x + ',' + t.y + ',' + t.k, t => { const T = creerTour(t); if (T) { T.r.position.set(t.x + .5, 0, t.y + .5); scene.add(T.r) } return T },
      (T, t) => majTour(T, t, temps), retirerGroupe);
    synchro(monstres, b.cr, c => c.id, c => { const Mo = creerMonstre(c); if (Mo) scene.add(Mo.r); return Mo }, (Mo, c) => majMonstre(Mo, c, dt, temps), retirerGroupe);
    synchro(projs, b.pr, p => p.id, creerProj, majProj, retirerGroupe);
    synchro(allies, (b.al || []).map((a, i) => ({id: 'a' + (a.id ?? i) + (a.g ? 'g' : ''), m: a.g ? 'co' : 'sq', x: a.x, y: a.y})), c => c.id,
      creerMort, (Mo, c) => majMort(Mo, c, dt, temps), retirerGroupe);
    synchro(mines, b.mi || [], m => m.id ?? (m.x + ',' + m.y), creerMine, (o, m) => { o.r.position.set(m.x + .5, .03, m.y + .5); o.c.rotation.y = temps * 2; o.c.position.y = .08 + Math.sin(temps * 4) * .02 }, retirerGroupe);
    synchro(effets, b.fx, f => f, creerEffet, majEffet, o => scene.remove(o));

    /* sélection : tour touchée ou projet de construction */
    const sel = etat.projet || etat.pick;
    portee.visible = cadreCase.visible = !!sel;
    if (sel) {
      const r = etat.projet ? TW[sel.k].r : etat.rng(sel);
      portee.position.set(sel.x + .5, .03, sel.y + .5); portee.scale.setScalar(r);
      porteeFond.material.color.set(etat.projet && !etat.ok ? '#ff4d3d' : '#3d6fb0');
      cadreCase.position.set(sel.x + .5, 0, sel.y + .5); cadreMat.color.set(etat.projet && !etat.ok ? '#ff6b5a' : '#ffd95e');
      cadreMat.opacity = etat.projet ? .7 + .25 * Math.sin(temps * 6) : .95;
    }
    const lt = etat.lot || [];
    for (let i = 0; i < Math.max(lt.length, cadresLot.length); i++) {
      const c = cadreLot(i); c.visible = i < lt.length; if (c.visible) c.position.set(lt[i].x + .5, 0, lt[i].y + .5);
    }
    lotMat.opacity = .55 + .35 * Math.sin(temps * 5);
    const pk = etat.projet ? etat.projet.k : -1;
    if (fantome && (pk < 0 || fantome.k !== pk)) { scene.remove(fantome.r); fantome = null }
    if (pk >= 0) {
      if (!fantome) { fantome = fantomes.get(pk) || creerTour({k: pk, x: 0, y: 0}, true); if (fantome) { fantomes.set(pk, fantome); majTour(fantome, {lv: 1, a: .7}, temps); scene.add(fantome.r) } }
      if (fantome) fantome.r.position.set(etat.projet.x + .5, 0, etat.projet.y + .5);
    }

    /* caméra : rotation et élan (voir l'en-tête) */
    bougerCamera(dt);
    majContour(renderer); renderer.render(scene, cam);
  }
  function taille(w, h, dpr) { renderer.setPixelRatio(Math.min(2, dpr)); renderer.setSize(w, h, true) }
  /* point du monde (gx, gz au sol, hauteur h) → pixels du canevas */
  function versEcran(gx, gz, h) { return projeter(gx, h, gz) }

  /* 2.12 : vignettes des boutons (tours et monstres) rendues à partir des modèles 3D, vue de trois quarts,
     avec un petit moteur de rendu à part (fond transparent). Renvoie l'image en data URL, ou null si le modèle manque. */
  let rv = null; const vignettes = new Map();
  function vignette(type, k, w, h) {
    const cle = type + k + '|' + w + 'x' + h; if (vignettes.has(cle)) return vignettes.get(cle);
    const p = charger(type === 'tour' ? urlTour(k) : urlMonstre(k)).then(g => {
      if (!g) return null;
      if (!rv) {
        rv = {r: new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: true}), s: new THREE.Scene(), c: new THREE.PerspectiveCamera(26, 1, .05, 60)};
        rv.r.outputColorSpace = THREE.SRGBColorSpace; rv.r.setClearColor(0, 0);
        rv.s.add(new THREE.HemisphereLight('#eef5ff', '#56627c', 1.7));
        const d = new THREE.DirectionalLight('#fff4e0', 2.6); d.position.set(-2, 4, 3); rv.s.add(d);
        const b = new THREE.DirectionalLight('#9fd0ff', 1.3); b.position.set(3, 2, -3); rv.s.add(b);
      }
      const o = g.scene.clone(true), piv = new THREE.Group(); piv.add(o); piv.rotation.y = type === 'tour' ? -.55 : -.7;
      const box = new THREE.Box3().setFromObject(piv), ct = box.getCenter(new THREE.Vector3()), rad = Math.max(.05, box.getSize(new THREE.Vector3()).length() / 2);
      o.position.sub(ct.applyAxisAngle(new THREE.Vector3(0, 1, 0), -piv.rotation.y)); rv.s.add(piv);
      const dist = rad / Math.sin(rv.c.fov * Math.PI / 360) * (type === 'tour' ? .78 : .72);
      rv.c.aspect = w / h; rv.c.position.set(0, dist * .38, dist * .92); rv.c.lookAt(0, type === 'tour' ? -rad * .05 : 0, 0); rv.c.updateProjectionMatrix();
      rv.r.setPixelRatio(2); rv.r.setSize(w, h, false); majContour(rv.r); rv.r.render(rv.s, rv.c);
      const url = rv.r.domElement.toDataURL('image/png'); rv.s.remove(piv); return url;
    }).catch(e => { console.warn(e); return null });
    vignettes.set(cle, p); return p;
  }

  /* compteurs pour les tests : objets 3D présents et appels de dessin de la dernière image */
  const etat = () => ({tours: tours.size, monstres: monstres.size, projectiles: projs.size, effets: effets.size, fantome: !!(fantome && fantome.r.parent),
    portee: portee.visible, dessins: renderer.info.render.calls, triangles: renderer.info.render.triangles,
    vue: {fx: V.fx, fz: V.fz, az: Math.round(V.azC / (Math.PI / 4)), perspective: cam.isPerspectiveCamera}});
  return {canvas, dessiner, taille, versEcran, precharger, hauteurMonstre: HAUT, vignette, renderer, etat,
    cadre, projeter, echelle, sol, glisser, pivoter, lancer, viser, amener, empreinte};
}
