/* Parcours automatisé d'un joueur dans un navigateur Chromium au format téléphone (portrait et paysage).
   Ce test vérifie que le parcours fonctionne dans CE navigateur de test : ce n'est pas une garantie
   de compatibilité avec tous les téléphones (Safari iOS, anciens Android, etc. ne sont pas testés). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const N=require('../outils/navigateur'),{demarrer}=require('../outils/serveur'),{RACINE}=require('../outils/moteur');

if(!N.disponible()){test('Parcours navigateur',{skip:'Playwright n\'est pas installé sur cette machine : tests navigateur ignorés'},()=>{})}
else for(const format of ['portrait','paysage'])test.describe(`Parcours mobile — ${format}`,()=>{
 let srv,nav,o,p;
 test.before(async()=>{srv=await demarrer(RACINE);nav=await N.lancer();o=await N.ouvrir(nav,srv.url,{format});p=o.page});
 test.after(async()=>{if(o)await o.fermer();if(nav)await nav.close();if(srv)await srv.fermer()});
 const val=f=>p.evaluate(f);

 test('La page s\'ouvre sans erreur, avec l\'écran d\'accueil',async()=>{
  assert.match(await p.title(),/Winter Realms/);assert.equal(await val(()=>document.getElementById('ov').hidden),false);
  assert.deepEqual(o.erreurs,[]);
 });
 test('À l\'ouverture, l\'Alliance est présélectionnée et les boutons de difficulté sont actifs',async()=>{
  assert.equal(await p.getAttribute('[data-faction="0"]','aria-pressed'),'true');
  for(const l of [0,1,2])assert.equal(await p.isDisabled('#go'+l),false);
 });
 test('Choisir une faction la sélectionne',async()=>{
  await N.toucher(p,'[data-faction="2"]');assert.equal(await p.getAttribute('[data-faction="2"]','aria-pressed'),'true');
  assert.equal(await p.getAttribute('[data-faction="0"]','aria-pressed'),'false');assert.match(await p.textContent('#factionStatus'),/Sylvestres/);
 });
 test('Lancer une partie en Normal : l\'accueil disparaît et l\'horloge tourne',async()=>{
  await N.toucher(p,'#go0');assert.equal(await val(()=>document.getElementById('ov').hidden),true);
  await N.avancer(p,2100);const e=await N.etat(p);assert.equal(e.horloge,'0:02');assert.deepEqual([e.or,e.revenu,e.vies,e.faction],[100,10,40,2]);
 });
 test('Construction (2.2) : un premier toucher montre un aperçu, sans rien construire',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[]);assert.equal(e.or,100);
  assert.deepEqual(e.projet,{x:3,y:5,k:20});assert.match(e.toast,/Touchez encore la case pour construire \(20 or\)/);
 });
 test('Construction (2.2) : un second toucher sur la même case construit la tour et débite son prix',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[{x:3,y:5,k:20,lv:1}]);assert.equal(e.or,80);assert.equal(e.projet,null);
 });
 test('Construction (2.2) : toucher une autre case déplace l\'aperçu, sans construire',async()=>{
  await N.toucherCase(p,8,5);await N.toucherCase(p,9,5);const e=await N.etat(p);assert.deepEqual(e.projet,{x:9,y:5,k:20});assert.equal(e.tours.length,1);assert.equal(e.or,80);
 });
 test('Construction (2.2) : glisser le doigt sur plusieurs cases ne construit rien',async()=>{
  await N.glisser(p,[1,12],[5,12]);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(e.or,80);
 });
 test('Une pose impossible est refusée avec un message',async()=>{
  await N.toucherCase(p,6,0);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(e.or,80);
  assert.equal(await p.textContent('#toast'),'Impossible ici : le chemin serait bloqué');assert.equal(await val(()=>document.getElementById('toast').hidden),false);
 });
 test('Toucher une tour ouvre son panneau ; Améliorer puis Vendre fonctionnent',async()=>{
  await N.toucherCase(p,3,5);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);
  assert.ok(e.boutons.some(b=>b.startsWith('Améliorer'))&&e.boutons.some(b=>b.startsWith('Vendre'))&&e.boutons.some(b=>b.startsWith('Fermer')));
  await N.toucher(p,'#bar button:has-text("Améliorer")');e=await N.etat(p);assert.equal(e.tours[0].lv,2);assert.equal(e.or,50);
  await N.toucher(p,'#bar button:has-text("Vendre")');e=await N.etat(p);assert.equal(e.tours.length,0);assert.equal(e.or,85);assert.equal(e.panneauOuvert,false);
 });
 test('Onglet « Sol » : envoyer un Sapeur gobelin coûte 10 or et augmente le revenu de 1',async()=>{
  await N.toucher(p,'#tabs button[data-t="n"]');await N.toucher(p,'#bar button:has-text("Sapeur gobelin")');
  const e=await N.etat(p);assert.equal(e.or,75);assert.equal(e.revenu,11);
  await N.toucher(p,'#tabs button[data-t="t"]');
 });
 test('Toucher une vignette affiche le terrain d\'une IA, puis on revient au sien',async()=>{
  await N.toucher(p,'#cartesBtn');await N.toucher(p,'#chips .chip >> nth=1');assert.equal((await N.etat(p)).vue,1);assert.equal(await val(()=>document.getElementById('banner').hidden),false);
  assert.equal(await val(()=>document.getElementById('chips').hidden),true,'le panneau se referme');await N.toucher(p,'#banner');assert.equal((await N.etat(p)).vue,0);assert.equal(await val(()=>document.getElementById('banner').hidden),true);
 });
 test('Fiche de construction (2.1) : la tour sélectionnée est décrite en clair',async()=>{
  let e=await N.etat(p);assert.match(e.fiche,/Arbre sentinelle/);assert.match(e.fiche,/Dégâts\/s/);assert.match(e.fiche,/Portée/);assert.match(e.fiche,/sol et air/);assert.match(e.fiche,/Racines/);
  await N.toucher(p,'#bar button:has-text("Gardien des racines")');e=await N.etat(p);assert.match(e.fiche,/Gardien des racines/);assert.match(e.fiche,/sol uniquement/);assert.match(e.fiche,/corps à corps/);
  await N.toucher(p,'#bar button:has-text("Arbre sentinelle")');
  assert.ok((await p.textContent('#bar button:has-text("Arbre sentinelle") em')).includes('/s'),'la carte affiche les dégâts par seconde');
 });
 test('Fiche d\'une tour posée (2.1) : niveau et gain du niveau suivant',async()=>{
  await N.construire(p,3,5);await N.toucherCase(p,3,5);const e=await N.etat(p);assert.equal(e.panneauOuvert,true);assert.match(e.fiche,/niveau 1\/5/);assert.match(e.fiche,/Niveau 2 :/);
  await N.toucher(p,'#bar button:has-text("Vendre")');
 });
 test('Onglet « Spéciaux » (2.1) : les monstres verrouillés affichent leur heure de déblocage',async()=>{
  await N.toucher(p,'#tabs button[data-t="s"]');assert.match(await p.textContent('#bar button:has-text("Tortue") em'),/🔒 dès 1:30/);
  assert.match((await N.etat(p)).fiche,/augmente ton revenu/);await N.toucher(p,'#tabs button[data-t="t"]');
 });
 test('Deux doigts (2.1) : écarter les doigts zoome, sans poser de tour',async()=>{
  const avant=await N.etat(p),c=await N.centreCase(p,6,8);
  await N.deuxDoigts(p,{de:[{x:c.x-30,y:c.y},{x:c.x+30,y:c.y}],vers:[{x:c.x-90,y:c.y},{x:c.x+90,y:c.y}]});
  const e=await N.etat(p);assert.ok(e.zoom>2.5,'zoom obtenu : '+e.zoom);assert.equal(e.tours.length,avant.tours.length,'aucune tour posée par le geste');assert.equal(e.or,avant.or);
  assert.equal(await p.isVisible('#zoomReset'),true,'le bouton « Vue d\'ensemble » apparaît');
 });
 test('Deux doigts (2.1) : déplacer les deux doigts fait glisser la carte',async()=>{
  const c0=await N.centreCase(p,6,8);await N.deuxDoigts(p,{de:[{x:c0.x-40,y:c0.y},{x:c0.x+40,y:c0.y}],vers:[{x:c0.x-40,y:c0.y-60},{x:c0.x+40,y:c0.y-60}]});
  const c1=await N.centreCase(p,6,8);assert.ok(c0.y-c1.y>40,'la case (6,8) est remontée à l\'écran');
 });
 test('Zoomé (2.1) : toucher une case pose la tour exactement sur cette case',async()=>{
  const b=await p.locator('#stage').boundingBox();let cible=null;
  for(let y=0;y<17&&!cible;y++)for(let x=0;x<13;x++){const c=await N.centreCase(p,x,y);if(x!=6&&c.x>b.x+20&&c.x<b.x+b.width-20&&c.y>b.y+50&&c.y<b.y+b.height-20){cible={x,y};break}}
  assert.ok(cible,'une case visible');const avant=(await N.etat(p)).or;await N.construire(p,cible.x,cible.y);
  const e=await N.etat(p);assert.ok(e.tours.some(t=>t.x==cible.x&&t.y==cible.y),'tour posée en ('+cible.x+','+cible.y+')');assert.equal(e.or,avant-20);
  await N.toucherCase(p,cible.x,cible.y);await N.toucher(p,'#bar button:has-text("Vendre")');
 });
 test('« Vue d\'ensemble » (2.1) : revient au zoom normal',async()=>{
  await N.toucher(p,'#zoomReset');assert.equal((await N.etat(p)).zoom,1);assert.equal(await p.isVisible('#zoomReset'),false);
 });
 test('Le revenu tombe à 10 s de jeu',async()=>{
  const avant=(await N.etat(p)).or;await N.avancer(p,10000);const e=await N.etat(p);assert.ok(e.temps>10);assert.equal(e.or,avant+11);
 });
 if(format=='paysage')test('En paysage, le HUD et les commandes passent sur le côté du terrain',async()=>{
  const s=await p.locator('#stage').boundingBox(),h=await p.locator('#hud').boundingBox(),c=await p.locator('#ctl').boundingBox();
  assert.ok(h.x>=s.x+s.width-1&&c.x>=s.x+s.width-1,'HUD et commandes à droite du terrain');
 });
 else test('En portrait, le HUD est au-dessus du terrain et les commandes en dessous',async()=>{
  const s=await p.locator('#stage').boundingBox(),h=await p.locator('#hud').boundingBox(),c=await p.locator('#ctl').boundingBox();
  assert.ok(h.y+h.height<=s.y+1&&c.y>=s.y+s.height-1);
 });
 test('Aucune erreur JavaScript pendant tout le parcours',()=>assert.deepEqual(o.erreurs,[]));
});
