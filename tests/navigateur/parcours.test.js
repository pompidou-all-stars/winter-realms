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
 test('Toucher une case pose la tour sélectionnée et débite son prix',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[{x:3,y:5,k:20,lv:1}]);assert.equal(e.or,80);
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
  await N.toucher(p,'#chips .chip >> nth=1');assert.equal((await N.etat(p)).vue,1);assert.equal(await val(()=>document.getElementById('banner').hidden),false);
  await N.toucher(p,'#chips .chip >> nth=0');assert.equal((await N.etat(p)).vue,0);assert.equal(await val(()=>document.getElementById('banner').hidden),true);
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
