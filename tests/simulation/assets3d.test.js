/* Assets 3D : le manifeste correspond aux scripts de art/ et chaque fichier respecte son budget.
   Ce test ne lance pas Blender (rapide, sur chaque PR) ; la régénération complète est faite par l'action « Assets 3D ». */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const {RACINE}=require('../outils/moteur');
const ART=path.join(RACINE,'art'),MANIF=path.join(RACINE,'assets','3d','manifeste.json');
const lire=f=>fs.readFileSync(f,'utf8').replace(/\r\n/g,'\n');

function scripts(){const ids=[];(function parcourir(d,rel){for(const n of fs.readdirSync(d).sort()){const p=path.join(d,n),r=rel?rel+'/'+n:n;
 if(fs.statSync(p).isDirectory()){if(!rel&&['outils','communs','sons','__pycache__'].includes(n))continue;parcourir(p,r)}
 else if(n.endsWith('.py')&&!n.startsWith('_'))ids.push(r.slice(0,-3))}})(ART,'');return ids.sort()}
/* même calcul que empreinte() dans art/outils/generer.py */
function empreinte(id){const h=crypto.createHash('sha256');h.update('script:'+lire(path.join(ART,id+'.py')),'utf8');
 const c=path.join(ART,'communs');if(fs.existsSync(c))for(const f of fs.readdirSync(c).filter(f=>f.endsWith('.py')).sort())h.update('\n--communs/'+f+'\n'+lire(path.join(c,f)),'utf8');
 return h.digest('hex')}

if(!fs.existsSync(ART))test('Assets 3D',{skip:'pas de dossier art/'},()=>{});
else{
 const M=JSON.parse(fs.readFileSync(MANIF,'utf8')),B=JSON.parse(fs.readFileSync(path.join(ART,'budgets.json'),'utf8')),ids=scripts();
 test('Chaque script de art/ a son fichier 3D dans le manifeste, et inversement',()=>{
  for(const id of ids)assert.ok(M.assets[id],`${id} : absent du manifeste (lancer art/outils/generer.py puis commiter assets/3d/)`);
  for(const id of Object.keys(M.assets))assert.ok(ids.includes(id),`${id} : présent dans le manifeste mais son script n'existe plus`);
 });
 test('Aucun fichier 3D n\'est en retard sur son script',()=>{
  for(const id of ids)if(M.assets[id])assert.ok(M.assets[id].empreinte_source===empreinte(id),`${id} : le script a changé mais le fichier 3D n'a pas été régénéré`);
 });
 test('Chaque fichier 3D existe, est un GLB valide et respecte son budget',()=>{let total=0;
  for(const [id,e] of Object.entries(M.assets)){const f=path.join(RACINE,e.fichier);assert.ok(fs.existsSync(f),`${id} : fichier ${e.fichier} manquant`);
   const buf=fs.readFileSync(f);assert.equal(buf.toString('ascii',0,4),'glTF',`${id} : ce n'est pas un fichier GLB`);assert.equal(buf.readUInt32LE(4),2,`${id} : version glTF inattendue`);
   assert.equal(buf.length,e.octets,`${id} : taille différente de celle du manifeste`);total+=buf.length;
   const lim=B[e.categorie];assert.ok(lim,`${id} : catégorie inconnue « ${e.categorie} »`);
   assert.ok(e.triangles<=lim.triangles,`${id} : ${e.triangles} triangles (budget ${lim.triangles})`);assert.ok(buf.length<=lim.octets,`${id} : ${buf.length} octets (budget ${lim.octets})`)}
  assert.ok(total<=B.total_octets,`total ${total} octets (budget ${B.total_octets})`);
 });
}
