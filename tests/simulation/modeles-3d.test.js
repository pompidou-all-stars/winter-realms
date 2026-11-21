/* 2.7 : les modèles 3D couvrent tout le jeu et ont ce qu'il faut au rendu 3D (rendu3d.js).
   Complète assets3d.test.js (manifeste, empreintes, budgets) : ici, la correspondance avec sim.js et le contenu des GLB.
   Lit seulement l'en-tête JSON des GLB (aucun décodage, pas de Blender). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {RACINE,charger}=require('../outils/moteur');
const D=path.join(RACINE,'assets','3d'),FAC=['alliance','horde','sylvestres','nains','ombres'];
const lireGLB=f=>{const b=fs.readFileSync(f);return JSON.parse(b.slice(20,20+b.readUInt32LE(12)).toString('utf8'))};
const S=charger();

/* 2.44 : les 5 premières races ont des modèles 3D ; les 5 races de Thibaut (sil) sont dessinées par silhouettes.js */
test('Un modèle 3D pour chaque tour des races à modèles (tours/<faction>-<j>), chaque clé de monstre (monstres/<g>), le portail et le château',()=>{
 assert.equal(S.RACES.filter(F=>!F.sil).length,FAC.length);
 for(const [f,F] of FAC.entries())for(let j=0;j<10;j++)assert.ok(fs.existsSync(path.join(D,'tours',`${F}-${j}.glb`)),`tour ${F}-${j} (${S.TW[f*10+j].n}) sans modèle`);
 for(const g of new Set(S.CR.map(c=>c.g)))assert.ok(fs.existsSync(path.join(D,'monstres',`${g}.glb`)),`monstre « ${g} » sans modèle`);
 for(const d of ['portail','chateau','mort-squelette','mort-colosse'])assert.ok(fs.existsSync(path.join(D,'decor',`${d}.glb`)),`décor ${d} manquant`);
});
test('Les monstres sont animés : « vol » pour les volants, « marche » pour les autres',()=>{
 for(const g of new Set(S.CR.map(c=>c.g))){const T=S.CR.find(c=>c.g==g),noms=(lireGLB(path.join(D,'monstres',`${g}.glb`)).animations||[]).map(a=>a.name);
  assert.ok(noms.includes(T.fly?'vol':'marche'),`${g} : animations ${noms.join(', ')||'aucune'}`)}
});
/* 2.40 : les tours qui tirent sur une cible (ni soutien « no », ni impulsion « pu », ni mines « mn ») ont une pièce qui la suit */
test('Les tours qui visent une cible ont une pièce « Tourelle »',()=>{
 S.TW.forEach((T,i)=>{if(T.no||T.pu===0||T.mn||S.RACES[T.faction].sil)return;const F=FAC[Math.floor(i/10)],j=i%10;
  assert.ok(lireGLB(path.join(D,'tours',`${F}-${j}.glb`)).nodes.some(n=>n.name==='Tourelle'),`${F}-${j} sans Tourelle`)});
});
test('Les modèles du jeu sont compressés (meshopt) et leurs couleurs sont dans les sommets (« Peint ») ou dans une texture peinte (« Peau », 2.30)',()=>{
 for(const sous of ['tours','monstres','decor'])for(const f of fs.readdirSync(path.join(D,sous)).filter(f=>f.endsWith('.glb'))){const g=lireGLB(path.join(D,sous,f));
  assert.ok((g.extensionsUsed||[]).includes('EXT_meshopt_compression'),`${sous}/${f} non compressé`);
  assert.ok(g.materials.some(m=>m.name==='Peint'||m.name==='Peau'),`${sous}/${f} sans matériau Peint ni Peau`)}
});
test('Bestiaire épique (2.41) : chaque monstre est sur squelette, avec texture peinte WebP et clips marche (ou vol), touche et mort',()=>{
 for(const g of new Set(S.CR.map(c=>c.g))){const T=S.CR.find(c=>c.g==g),m=lireGLB(path.join(D,'monstres',`${g}.glb`)),noms=(m.animations||[]).map(a=>a.name);
  assert.ok(m.skins&&m.skins.length>=1&&m.skins[0].joints.length>=12,`${g} : squelette attendu`);
  assert.ok((m.extensionsUsed||[]).includes('EXT_texture_webp')&&[1,2].includes((m.images||[]).length),`${g} : texture WebP attendue (peinture et carte de relief)`);
  for(const c of [T.fly?'vol':'marche','touche','mort'])assert.ok(noms.includes(c),`${g} : clip ${c} manquant (${noms.join(', ')})`)}
});
test('Le château a un drapeau recolorable (matériau « Drapeau »)',()=>{
 assert.ok(lireGLB(path.join(D,'decor','chateau.glb')).materials.some(m=>m.name==='Drapeau'));
});
