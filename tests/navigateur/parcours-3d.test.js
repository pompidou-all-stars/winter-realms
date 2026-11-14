/* 2.7 : parcours mobile avec le rendu 3D (?rendu=3d), au format téléphone (portrait et paysage).
   WebGL tourne en rendu logiciel (SwiftShader) : le test ne dépend pas d'une carte graphique.
   Mêmes commandes qu'en 2D : construction en deux touchers, panneau de tour, zoom et déplacement à deux doigts. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const N=require('../outils/navigateur'),{demarrer}=require('../outils/serveur'),{RACINE}=require('../outils/moteur');

if(!N.disponible()){test('Parcours navigateur 3D',{skip:'Playwright n\'est pas installé sur cette machine : tests navigateur ignorés'},()=>{})}
else for(const format of ['portrait','paysage'])test.describe(`Parcours mobile en 3D — ${format}`,()=>{
 let srv,nav,o,p;
 test.before(async()=>{srv=await demarrer(RACINE);nav=await N.lancer({webgl:true});o=await N.ouvrir(nav,srv.url+'?rendu=3d',{format});p=o.page});
 test.after(async()=>{if(o)await o.fermer();if(nav)await nav.close();if(srv)await srv.fermer()});
 const r3d=()=>p.evaluate(()=>R3D_ETAT());

 test('Le rendu 3D se charge (WebGL, modèles) sans erreur',async()=>{
  assert.equal(await N.attendre3D(p),true,'rendu 3D prêt');
  const e=await r3d();assert.equal(e.on,true);assert.ok(e.KY<1,'rangées tassées par la caméra inclinée');
  assert.equal(await p.locator('#main3d').count(),1,'canevas WebGL présent');assert.deepEqual(o.erreurs,[]);
  assert.equal(await p.textContent('#mode3d'),'Revenir à la vue 2D');
 });
 test('Une partie démarre : le plateau, le portail et le château sont dessinés',async()=>{
  await N.toucher(p,'#go0');await N.avancer(p,600);const e=await r3d();
  assert.ok(e.scene.dessins>5,'appels de dessin : '+e.scene.dessins);assert.ok(e.scene.triangles>3000,'triangles : '+e.scene.triangles);
 });
 test('Construction : un premier toucher montre la tour fantôme et sa portée, sans rien construire',async()=>{
  await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;
  assert.deepEqual(e.tours,[]);assert.equal(e.or,100);assert.deepEqual(e.projet,{x:3,y:5,k:0});assert.equal(s.fantome,true);assert.equal(s.portee,true);
 });
 test('Construction : un second toucher sur la même case construit la tour en 3D',async()=>{
  await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;
  assert.deepEqual(e.tours,[{x:3,y:5,k:0,lv:1}]);assert.equal(e.or,80);assert.equal(s.tours,1);assert.equal(s.fantome,false);
 });
 test('Une pose impossible est refusée avec un message',async()=>{
  await N.toucherCase(p,6,0);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(await p.textContent('#toast'),'Impossible ici : le chemin serait bloqué');
 });
 test('Toucher la tour ouvre son panneau ; Améliorer fonctionne (après le chantier)',async()=>{
  await N.avancer(p,1500);await N.toucherCase(p,3,5);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);
  await N.toucher(p,'#bar button:has-text("Améliorer")');e=await N.etat(p);assert.equal(e.tours[0].lv,2);await N.toucher(p,'#bar button:has-text("Fermer")');
 });
 test('Envoyer des monstres : ils apparaissent en 3D chez l\'adversaire, animés',async()=>{
  await N.toucher(p,'#tabs button[data-t="n"]');await N.toucher(p,'#bar button:has-text("Sapeur gobelin")');await N.toucher(p,'#tabs button[data-t="t"]');
  /* les monstres apparaissent en moins de 1,4 s ; l'IA peut les tuer vite : on garde le maximum observé */
  await p.evaluate(()=>setView(1));let max=0;
  try{for(let i=0;i<12;i++){await N.avancer(p,200);max=Math.max(max,(await r3d()).scene.monstres)}}
  finally{await p.evaluate(()=>setView(0));await N.avancer(p,50)}
  assert.ok(max>=1,'monstres en 3D : '+max);
 });
 test('Deux doigts : écarter les doigts zoome, sans poser de tour',async()=>{
  const avant=await N.etat(p),c=await N.centreCase(p,6,8);
  await N.deuxDoigts(p,{de:[{x:c.x-30,y:c.y},{x:c.x+30,y:c.y}],vers:[{x:c.x-90,y:c.y},{x:c.x+90,y:c.y}]});
  const e=await N.etat(p);assert.ok(e.zoom>2.5,'zoom obtenu : '+e.zoom);assert.equal(e.tours.length,avant.tours.length);assert.equal(await p.isVisible('#zoomReset'),true);
 });
 test('Deux doigts : déplacer les deux doigts fait glisser la carte',async()=>{
  const c0=await N.centreCase(p,6,8);await N.deuxDoigts(p,{de:[{x:c0.x-40,y:c0.y},{x:c0.x+40,y:c0.y}],vers:[{x:c0.x-40,y:c0.y-60},{x:c0.x+40,y:c0.y-60}]});
  const c1=await N.centreCase(p,6,8);assert.ok(c0.y-c1.y>40,'la case (6,8) est remontée à l\'écran');
 });
 test('Zoomé : toucher une case pose la tour exactement sur cette case',async()=>{
  const b=await p.locator('#stage').boundingBox();let cible=null;
  for(let y=0;y<17&&!cible;y++)for(let x=0;x<13;x++){const c=await N.centreCase(p,x,y);if(x!=6&&!(x==3&&y==5)&&c.x>b.x+20&&c.x<b.x+b.width-20&&c.y>b.y+60&&c.y<b.y+b.height-20){cible={x,y};break}}
  assert.ok(cible,'une case visible');const avant=(await N.etat(p)).or;await N.construire(p,cible.x,cible.y);
  const e=await N.etat(p);assert.ok(e.tours.some(t=>t.x==cible.x&&t.y==cible.y),'tour posée en ('+cible.x+','+cible.y+')');assert.equal(e.or,avant-20);
 });
 test('« Vue d\'ensemble » : revient au zoom normal',async()=>{
  await N.toucher(p,'#zoomReset');assert.equal((await N.etat(p)).zoom,1);
 });
 test('Aucune erreur JavaScript pendant tout le parcours',()=>assert.deepEqual(o.erreurs,[]));
});
