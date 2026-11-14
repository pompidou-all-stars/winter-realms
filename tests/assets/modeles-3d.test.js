/* Modèles 3D (assets/3d/) : chaque tour et chaque monstre du jeu a son modèle, et les budgets
   « téléphone » sont respectés : ≤ 3 000 triangles et ≤ 150 Ko par modèle, ≤ 3 Mo au total.
   Les triangles sont comptés depuis l'en-tête JSON du GLB (aucun décodage nécessaire). */
'use strict';
const test=require('node:test'),assert=require('node:assert'),fs=require('fs'),path=require('path');
const {charger}=require('../outils/moteur');
const DOSSIER=path.join(__dirname,'..','..','assets','3d');
const TRI_MAX=3000,KO_MAX=150,MO_TOTAL=3;
const MONSTRES=['sapeur_gobelin','warg','brute_orc','troll_glaces','golem_runique','cyclope_cendres','chauve_souris','griffon_corrompu',
 'dragon_ancien','chaman_guerre','pretresse','gelee_mutante','tortue','briseur_runes','spectre','saboteur_gobelin','azhkhar','petit_limon'];
const FACTIONS=['alliance','horde','sylvestres','nains','ombres'];

function lireGLB(f){const b=fs.readFileSync(f);assert.strictEqual(b.readUInt32LE(0),0x46546c67,`${f} n'est pas un GLB`);
 const n=b.readUInt32LE(12);return JSON.parse(b.slice(20,20+n).toString('utf8'))}
function triangles(j){let t=0;for(const m of j.meshes||[])for(const p of m.primitives){const mode=p.mode??4;if(mode!==4)continue;
 t+=(p.indices!=null?j.accessors[p.indices].count:j.accessors[p.attributes.POSITION].count)/3}return t}

const present=fs.existsSync(DOSSIER);
test('Modèles 3D : le dossier assets/3d existe',()=>assert.ok(present,'assets/3d introuvable'));
if(present){
 const S=charger();
 test(`Un modèle par tour (${S.TW.length}) et par monstre (${S.CR.length}), dans l'ordre de sim.js`,()=>{
  assert.strictEqual(S.TW.length,FACTIONS.length*10);assert.strictEqual(S.CR.length,MONSTRES.length);
  for(const f of FACTIONS)for(let j=0;j<10;j++)assert.ok(fs.existsSync(path.join(DOSSIER,'tours',`${f}_${j}.glb`)),`tour ${f}_${j} manquante`);
  for(const m of MONSTRES)assert.ok(fs.existsSync(path.join(DOSSIER,'monstres',`${m}.glb`)),`monstre ${m} manquant`);
  for(const d of ['portail','chateau'])assert.ok(fs.existsSync(path.join(DOSSIER,'decor',`${d}.glb`)),`décor ${d} manquant`)});
 const tous=[];(function l(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);fs.statSync(p).isDirectory()?l(p):f.endsWith('.glb')&&tous.push(p)}})(DOSSIER);
 test(`Budgets : ≤ ${TRI_MAX} triangles et ≤ ${KO_MAX} Ko par modèle, ≤ ${MO_TOTAL} Mo au total`,()=>{
  let total=0;const trop=[];
  for(const f of tous){const ko=fs.statSync(f).size/1024,t=triangles(lireGLB(f));total+=ko;
   if(t>TRI_MAX||ko>KO_MAX)trop.push(`${path.relative(DOSSIER,f)} : ${t} triangles, ${ko.toFixed(0)} Ko`)}
  assert.deepStrictEqual(trop,[],'modèles hors budget');
  assert.ok(total/1024<=MO_TOTAL,`total ${(total/1024).toFixed(2)} Mo`)});
 test('Les monstres sont animés (« marche » ou « vol ») et les volants battent des ailes',()=>{
  for(const m of MONSTRES){const j=lireGLB(path.join(DOSSIER,'monstres',`${m}.glb`)),noms=(j.animations||[]).map(a=>a.name);
   const vol=S.CR[MONSTRES.indexOf(m)].fly;assert.ok(noms.includes(vol?'vol':'marche'),`${m} : animations ${noms.join(', ')||'aucune'}`)}});
 test('Les tours qui visent ont une pièce « Tourelle », compressée en meshopt',()=>{
  for(const f of FACTIONS)for(const j of [0,1,3,5,6,7,9]){const g=lireGLB(path.join(DOSSIER,'tours',`${f}_${j}.glb`));
   assert.ok(g.nodes.some(n=>n.name==='Tourelle'),`${f}_${j} sans Tourelle`);
   assert.ok((g.extensionsUsed||[]).includes('EXT_meshopt_compression'),`${f}_${j} non compressée`)}});
}
