/* 2.7 puis 2.15 : parcours mobile avec le rendu 3D (?rendu=3d), au format téléphone (portrait : depuis la 2.15, le jeu se joue en portrait).
   WebGL tourne en rendu logiciel (SwiftShader) : le test ne dépend pas d'une carte graphique.
   Vue tactique (2.15) : caméra en perspective, glisser le doigt déplace la carte, deux flèches la font pivoter d'un huitième de tour. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const N=require('../outils/navigateur'),{demarrer}=require('../outils/serveur'),{RACINE}=require('../outils/moteur');

if(!N.disponible()){test('Parcours navigateur 3D',{skip:'Playwright n\'est pas installé sur cette machine : tests navigateur ignorés'},()=>{})}
else test.describe('Parcours mobile en 3D — portrait',()=>{
 let srv,nav,o,p;
 test.before(async()=>{srv=await demarrer(RACINE);nav=await N.lancer({webgl:true});o=await N.ouvrir(nav,srv.url+'?rendu=3d',{format:'portrait'});p=o.page});
 test.after(async()=>{if(o)await o.fermer();if(nav)await nav.close();if(srv)await srv.fermer()});
 const r3d=()=>p.evaluate(()=>R3D_ETAT());
 /* une case dont le centre est bien visible, entre le bandeau et le dock */
 async function caseVisible(exclues=[]){const b=await p.locator('#stage').boundingBox(),d=await p.locator('#ctl').boundingBox();
  for(let y=4;y<15;y++)for(let x=1;x<12;x++){if(x==6||exclues.some(([a,c])=>a==x&&c==y))continue;const c=await N.centreCase(p,x,y);
   if(c.x>b.x+60&&c.x<b.x+b.width-60&&c.y>b.y+140&&c.y<d.y-70)return {x,y}}return null}

 test('Le rendu 3D se charge (WebGL, modèles) sans erreur, avec la caméra tactique en perspective',async()=>{
  assert.equal(await N.attendre3D(p),true,'rendu 3D prêt');
  const e=await r3d();assert.equal(e.on,true);assert.equal(e.scene.vue.perspective,true);assert.equal(e.scene.vue.az,0);
  assert.equal(await p.locator('#main3d').count(),1,'canevas WebGL présent');assert.deepEqual(o.erreurs,[]);
 });
 test('Une partie démarre : le plateau, le portail et le château sont dessinés ; les flèches de rotation sont là',async()=>{
  await N.toucher(p,'#go0');await N.avancer(p,600);const e=await r3d();
  assert.ok(e.scene.dessins>5,'appels de dessin : '+e.scene.dessins);assert.ok(e.scene.triangles>3000,'triangles : '+e.scene.triangles);
  assert.equal(await p.isVisible('#rotG'),true);assert.equal(await p.isVisible('#rotD'),true);
 });
 test('Construction : après le choix d\'une tour, un premier toucher montre la tour fantôme et sa portée, sans rien construire',async()=>{
  await N.toucherCarte(p,'Tour des archers');await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;
  assert.deepEqual(e.tours,[]);assert.equal(e.or,200);assert.deepEqual(e.projet,{x:3,y:5,k:0});assert.equal(s.fantome,true);assert.equal(s.portee,true);
 });
 test('Construction : un second toucher sur la même case construit la tour en 3D',async()=>{
  await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;
  assert.deepEqual(e.tours,[{x:3,y:5,k:0,lv:1}]);assert.equal(e.or,180);assert.equal(s.tours,1);assert.equal(s.fantome,false);
 });
 test('Une pose impossible est refusée avec un message',async()=>{
  await N.toucherCase(p,6,0);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(await p.textContent('#toast'),'Impossible ici : le chemin serait bloqué');
 });
 test('Toucher la tour ouvre sa fiche ; Améliorer fonctionne (après le chantier)',async()=>{
  await N.avancer(p,1500);await N.toucherCase(p,3,5);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);
  await N.toucher(p,'#fiche button:has-text("Améliorer")');e=await N.etat(p);assert.equal(e.tours[0].lv,2);await N.toucher(p,'#fiche .fermer');
 });
 test('Envoyer des monstres : ils apparaissent en 3D chez l\'adversaire, animés',async()=>{
  await p.evaluate(()=>{G.time=GRACE});await N.avancer(p,100); // 2.30 : fin de la phase « Construis »
  await N.toucher(p,'#tabs button[data-t="n"]');await N.toucherCarte(p,'Sapeur gobelin');await N.toucherCarte(p,'Sapeur gobelin');await N.toucher(p,'#tabs button[data-t="t"]');
  /* les monstres apparaissent en moins de 1,4 s ; l'IA peut les tuer vite : on garde le maximum observé */
  await p.evaluate(()=>setView(1));let max=0;
  try{for(let i=0;i<12;i++){await N.avancer(p,200);max=Math.max(max,(await r3d()).scene.monstres)}}
  finally{await p.evaluate(()=>setView(0));await N.avancer(p,50)}
  assert.ok(max>=1,'monstres en 3D : '+max);
 });
 test('Glisser le doigt déplace la carte (le terrain suit le doigt), sans rien construire',async()=>{
  const avant=await N.etat(p),c0=await N.centreCase(p,6,9);await N.glisser(p,[6,9],[6,6]);await N.avancer(p,600);
  const c1=await N.centreCase(p,6,9),e=await N.etat(p);assert.ok(c0.y-c1.y>40,'la case (6,9) est remontée à l\'écran : '+Math.round(c0.y)+' → '+Math.round(c1.y));
  assert.equal(e.tours.length,avant.tours.length);assert.equal(e.or,avant.or);assert.equal(e.projet,null);
 });
 test('Les flèches font pivoter la vue d\'un huitième de tour, dans un sens puis dans l\'autre',async()=>{
  const c0=await N.centreCase(p,3,5);await N.toucher(p,'#rotD');await N.avancer(p,800);assert.equal((await r3d()).scene.vue.az,1);
  const c1=await N.centreCase(p,3,5);assert.ok(Math.hypot(c1.x-c0.x,c1.y-c0.y)>20,'la case (3,5) a bougé à l\'écran');
  await N.toucher(p,'#rotG');await N.toucher(p,'#rotG');await N.avancer(p,800);assert.equal((await r3d()).scene.vue.az,-1);
 });
 test('Vue pivotée : toucher une case pose la tour exactement sur cette case',async()=>{
  await N.toucher(p,'#bar button >> nth=0');const cible=await caseVisible([[3,5]]);assert.ok(cible,'une case visible');
  const avant=(await N.etat(p)).or;await N.construire(p,cible.x,cible.y);
  const e=await N.etat(p);assert.ok(e.tours.some(t=>t.x==cible.x&&t.y==cible.y),'tour posée en ('+cible.x+','+cible.y+')');assert.equal(e.or,avant-20);
 });
 test('Aucune erreur JavaScript pendant tout le parcours',()=>assert.deepEqual(o.erreurs,[]));
});

/* 2.8 : la 3D est le rendu par défaut ; ?rendu=2d garde la 2D classique (2.22 : plus de lien sur l'accueil, la 2D sert de secours et aux tests) */
if(N.disponible())test('Adresse par défaut : la 3D ; avec ?rendu=2d : la 2D',async()=>{
 const srv=await demarrer(RACINE),nav=await N.lancer({webgl:true});
 try{let o=await N.ouvrir(nav,srv.url);assert.equal(await N.attendre3D(o.page),true,'3D chargée sans paramètre');
  assert.equal(await o.page.locator('#mode3d').count(),0,'pas de lien vers la 2D sur l’accueil');assert.deepEqual(o.erreurs,[]);await o.fermer();
  o=await N.ouvrir(nav,srv.url+'?rendu=2d');const e=await o.page.evaluate(()=>R3D_ETAT());assert.equal(e.on,false);assert.equal(await o.page.locator('#main3d').count(),0);
  assert.deepEqual(o.erreurs,[]);await o.fermer()}
 finally{await nav.close();await srv.fermer()}});
