/* 2.7 : les modèles 3D couvrent tout le jeu et ont ce qu'il faut au rendu 3D (rendu3d.js).
   Complète assets3d.test.js (manifeste, empreintes, budgets) : ici, la correspondance avec sim.js et le contenu des GLB.
   Lit seulement l'en-tête JSON des GLB (aucun décodage, pas de Blender). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {RACINE,charger}=require('../outils/moteur');
const D=path.join(RACINE,'assets','3d'),FAC=['alliance','horde','sylvestres','nains','ombres'];
const lireGLB=f=>{const b=fs.readFileSync(f);return JSON.parse(b.slice(20,20+b.readUInt32LE(12)).toString('utf8'))};
const S=charger();

test('Un modèle 3D pour chaque tour (tours/<faction>-<j>) et chaque clé de monstre (monstres/<g>), plus le portail et le château',()=>{
 assert.equal(S.TW.length,FAC.length*10);
 for(const [f,F] of FAC.entries())for(let j=0;j<10;j++)assert.ok(fs.existsSync(path.join(D,'tours',`${F}-${j}.glb`)),`tour ${F}-${j} (${S.TW[f*10+j].n}) sans modèle`);
 for(const g of new Set(S.CR.map(c=>c.g)))assert.ok(fs.existsSync(path.join(D,'monstres',`${g}.glb`)),`monstre « ${g} » sans modèle`);
 for(const d of ['portail','chateau'])assert.ok(fs.existsSync(path.join(D,'decor',`${d}.glb`)),`décor ${d} manquant`);
});
test('Les monstres sont animés : « vol » pour les volants, « marche » pour les autres',()=>{
 for(const g of new Set(S.CR.map(c=>c.g))){const T=S.CR.find(c=>c.g==g),noms=(lireGLB(path.join(D,'monstres',`${g}.glb`)).animations||[]).map(a=>a.name);
  assert.ok(noms.includes(T.fly?'vol':'marche'),`${g} : animations ${noms.join(', ')||'aucune'}`)}
});
test('Les tours qui visent (archer, garde, canon, mage) ont une pièce « Tourelle »',()=>{
 for(const F of FAC)for(const j of [0,1,3,5,6,7,9])assert.ok(lireGLB(path.join(D,'tours',`${F}-${j}.glb`)).nodes.some(n=>n.name==='Tourelle'),`${F}-${j} sans Tourelle`);
});
test('Les modèles du jeu sont compressés (meshopt) et leurs couleurs sont dans les sommets (matériau « Peint »)',()=>{
 for(const sous of ['tours','monstres','decor'])for(const f of fs.readdirSync(path.join(D,sous)).filter(f=>f.endsWith('.glb'))){const g=lireGLB(path.join(D,sous,f));
  assert.ok((g.extensionsUsed||[]).includes('EXT_meshopt_compression'),`${sous}/${f} non compressé`);
  assert.ok(g.materials.some(m=>m.name==='Peint'),`${sous}/${f} sans matériau Peint`)}
});
test('Le château a un drapeau recolorable (matériau « Drapeau »)',()=>{
 assert.ok(lireGLB(path.join(D,'decor','chateau.glb')).materials.some(m=>m.name==='Drapeau'));
});
