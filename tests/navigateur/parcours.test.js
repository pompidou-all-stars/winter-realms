/* Parcours automatisé d'un joueur dans un navigateur Chromium au format téléphone, en 2D (?rendu=2d).
   Depuis la 2.15, le jeu se joue en portrait seulement : le parcours complet est en portrait, et en paysage on vérifie
   que le jeu demande de tourner le téléphone.
   Ce test vérifie que le parcours fonctionne dans CE navigateur de test : ce n'est pas une garantie
   de compatibilité avec tous les téléphones (Safari iOS, anciens Android, etc. ne sont pas testés). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const N=require('../outils/navigateur'),{demarrer}=require('../outils/serveur'),{RACINE}=require('../outils/moteur');

if(!N.disponible()){test('Parcours navigateur',{skip:'Playwright n\'est pas installé sur cette machine : tests navigateur ignorés'},()=>{})}
else{
test.describe('Parcours mobile — portrait',()=>{
 let srv,nav,o,p;
 test.before(async()=>{srv=await demarrer(RACINE);nav=await N.lancer();o=await N.ouvrir(nav,srv.url+'?rendu=2d',{format:'portrait'});p=o.page});
 test.after(async()=>{if(o)await o.fermer();if(nav)await nav.close();if(srv)await srv.fermer()});
 const val=f=>p.evaluate(f);

 test('La page s\'ouvre sans erreur, avec l\'écran d\'accueil',async()=>{
  assert.match(await p.title(),/Winter Realms/);assert.equal(await val(()=>document.getElementById('ov').hidden),false);
  assert.equal(await p.isVisible('#tourner'),false,'pas de message « tourne ton téléphone » en portrait');
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
 test('Lancer une partie en Normal : l\'accueil disparaît, l\'horloge tourne, une astuce s\'affiche et aucune fiche',async()=>{
  await N.toucher(p,'#go0');assert.equal(await val(()=>document.getElementById('ov').hidden),true);
  await N.avancer(p,2100);const e=await N.etat(p);assert.equal(e.horloge,'0:02');assert.deepEqual([e.or,e.revenu,e.vies,e.faction],[100,10,40,2]);
  assert.equal(await p.isVisible('#astuce'),true);assert.equal(e.fiche,'','sans choix, pas de fiche (2.15)');
 });
 test('Musique (2.16) : un des 3 thèmes démarre dès le premier toucher, puis ils s’enchaînent en boucle',async()=>{
  const m=()=>p.evaluate(()=>({src:MUSIQUE.el?MUSIQUE.el.src:'',i:MUSIQUE.i,n:MUSIQUE.pistes.length}));
  const a=await m();assert.match(a.src,/assets\/musique\/winter-realm(-1|-2)?\.mp3$/,'thème en cours : '+a.src);assert.equal(a.n,3);
  for(let k=1;k<=3;k++){await p.evaluate(()=>MUSIQUE.el.dispatchEvent(new Event('ended')));const b=await m();assert.equal(b.i,(a.i+k)%3,'thème suivant ('+k+')')}
 });
 test('Interface (2.15) : bandeau en haut, dock en bas, terrain sur tout l\'écran ; pas de flèches de rotation en 2D',async()=>{
  const s=await p.locator('#stage').boundingBox(),h=await p.locator('#hud').boundingBox(),c=await p.locator('#ctl').boundingBox(),v=p.viewportSize();
  assert.ok(s.width>=v.width-1&&s.height>=v.height-1,'le terrain couvre l\'écran');assert.ok(h.y<60,'bandeau en haut');assert.ok(c.y+c.height>=v.height-1,'dock en bas');
  for(const id of ['#menuBtn','#fs','#cartesBtn'])assert.equal(await p.isVisible(id),true,id+' visible');
  assert.equal(await p.isVisible('#rotG'),false);assert.equal(await p.isVisible('#rotD'),false);
 });
 test('Sans tour choisie, toucher une case ne construit rien et le dit',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[]);assert.equal(e.projet,null);assert.match(e.toast,/Choisis d’abord une tour/);
 });
 test('Choisir une carte de tour (2.15) : la fiche la décrit en clair, rien n\'est construit',async()=>{
  await N.toucherCarte(p,'Arbre sentinelle');const e=await N.etat(p);assert.equal(e.choix,20);assert.equal(e.or,100);
  assert.match(e.fiche,/Arbre sentinelle/);assert.match(e.fiche,/Dégâts\/s/);assert.match(e.fiche,/Portée/);assert.match(e.fiche,/sol et air/);assert.match(e.fiche,/Racines/);assert.match(e.fiche,/deux fois une case/);
  assert.equal(await p.getAttribute('#bar button[aria-label^="Arbre sentinelle,"]','class'),'sel');
  assert.match(await p.textContent('#bar button[aria-label^="Arbre sentinelle,"]'),/^20 or$/,'la carte ne montre que le prix');
 });
 test('Construction : un premier toucher montre un aperçu, sans rien construire',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[]);assert.equal(e.or,100);
  assert.deepEqual(e.projet,{x:3,y:5,k:20});assert.match(e.toast,/Touchez encore la case pour construire \(20 or/);
 });
 test('Construction : un second toucher sur la même case construit la tour et débite son prix',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[{x:3,y:5,k:20,lv:1}]);assert.equal(e.or,80);assert.equal(e.projet,null);
 });
 test('Construction : toucher une autre case déplace l\'aperçu, sans construire',async()=>{
  await N.toucherCase(p,8,5);await N.toucherCase(p,9,5);const e=await N.etat(p);assert.deepEqual(e.projet,{x:9,y:5,k:20});assert.equal(e.tours.length,1);assert.equal(e.or,80);
 });
 test('Construction : glisser le doigt sur plusieurs cases ne construit rien',async()=>{
  await N.glisser(p,[1,12],[5,12]);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(e.or,80);
 });
 test('Une pose impossible est refusée avec un message',async()=>{
  await N.toucherCase(p,6,0);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(e.or,80);
  assert.equal(await p.textContent('#toast'),'Impossible ici : le chemin serait bloqué');assert.equal(await val(()=>document.getElementById('toast').hidden),false);
 });
 test('Toucher une tour ouvre sa fiche ; Améliorer (après le chantier) puis Vendre fonctionnent',async()=>{
  await N.avancer(p,1500);await N.toucherCase(p,3,5);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);
  assert.match(e.fiche,/niveau 1\/5/);assert.match(e.fiche,/Niveau 2 :/);
  assert.ok(e.boutons.some(b=>b.startsWith('Améliorer'))&&e.boutons.some(b=>b.startsWith('Vendre')));
  await N.toucher(p,'#fiche button:has-text("Améliorer")');e=await N.etat(p);assert.equal(e.tours[0].lv,2);assert.equal(e.or,50);
  await N.toucher(p,'#fiche button:has-text("Vendre")');e=await N.etat(p);assert.equal(e.tours.length,0);assert.equal(e.or,85);assert.equal(e.panneauOuvert,false);
 });
 test('Le × de la fiche annule le choix de la tour',async()=>{
  await N.toucher(p,'#fiche .fermer');const e=await N.etat(p);assert.equal(e.choix,null);assert.equal(e.fiche,'');
 });
 test('Envoyer (2.15) : le 1er toucher choisit le monstre, chaque toucher suivant envoie un groupe',async()=>{
  await N.toucher(p,'#tabs button[data-t="n"]');await N.toucherCarte(p,'Sapeur gobelin');let e=await N.etat(p);
  assert.equal(e.or,85,'le premier toucher n\'envoie rien');assert.match(e.fiche,/Sapeur gobelin/);assert.match(e.fiche,/Chaque toucher/);
  await N.toucherCarte(p,'Sapeur gobelin');e=await N.etat(p);assert.equal(e.or,75);assert.equal(e.revenu,11);
  await N.toucherCarte(p,'Sapeur gobelin');e=await N.etat(p);assert.equal(e.or,65);assert.equal(e.revenu,12);assert.match(e.toast,/^×2 · /,'compteur des envois enchaînés');
  await N.toucher(p,'#tabs button[data-t="t"]');
 });
 test('Onglet « Spéciaux » : paliers de monstres ; le palier 2 s’ouvre contre son prix et montre ses monstres',async()=>{
  await N.toucher(p,'#tabs button[data-t="s"]');assert.equal(await p.isVisible('#paliers'),true);
  assert.match(await p.textContent('#paliers button:has-text("Palier 2")'),/300 or/);
  await N.toucherCarte(p,'Tortue');assert.match((await N.etat(p)).fiche,/blindée/);
  await N.toucher(p,'#paliers button:has-text("Palier 2")');assert.equal(await p.evaluate(()=>P.tier),1,'pas assez d’or : palier fermé');
  await p.evaluate(()=>{P.gold+=300});const or=await p.evaluate(()=>P.gold);await N.toucher(p,'#paliers button:has-text("Palier 2")');
  assert.equal(await p.evaluate(()=>P.tier),2);assert.equal(await p.evaluate(()=>P.gold),or-300);
  assert.equal(await p.locator('#bar button[aria-label^="Golem de boue,"]').count(),1,'monstres du palier 2 affichés');
  await N.toucher(p,'#tabs button[data-t="t"]');assert.equal(await p.isVisible('#paliers'),false);
 });
 test('Bouton Adversaires : une vignette affiche le terrain d\'une IA (lecture seule), puis on revient au sien',async()=>{
  await N.toucher(p,'#cartesBtn');assert.equal(await p.isVisible('#chips'),true);await N.toucher(p,'#chips .chip >> nth=1');
  assert.equal((await N.etat(p)).vue,1);assert.equal(await val(()=>document.getElementById('banner').hidden),false);
  assert.equal(await val(()=>document.getElementById('chips').hidden),true,'le panneau se referme');assert.match(await p.textContent('#cartesBtn'),/IA 1/);
  await N.toucherCarte(p,'Arbre sentinelle');await N.toucherCase(p,2,8);const e=await N.etat(p);assert.match(e.toast,/lecture seule/);assert.equal(e.projet,null);
  await N.toucher(p,'#banner');assert.equal((await N.etat(p)).vue,0);assert.equal(await val(()=>document.getElementById('banner').hidden),true);
  await N.toucher(p,'#fiche .fermer');
 });
 test('Le revenu tombe à 10 s de jeu',async()=>{
  const avant=(await N.etat(p)).or;await N.avancer(p,10000);const e=await N.etat(p);assert.ok(e.temps>10);assert.equal(e.or,avant+12);
 });
 test('Menu (2.15) : son, rappel des gestes, reprendre ; quitter demande une confirmation',async()=>{
  await N.toucher(p,'#menuBtn');assert.equal(await p.isVisible('#menu'),true);
  await N.toucher(p,'#snd');assert.equal(await p.textContent('#snd'),'Son : coupé');await N.toucher(p,'#snd');
  await N.toucher(p,'#mMusique');assert.equal(await p.textContent('#mMusique'),'Musique : coupée');assert.equal(await p.evaluate(()=>MUSIQUE.el.paused),true,'musique en pause');await N.toucher(p,'#mMusique');assert.equal(await p.evaluate(()=>MUSIQUE.on),true);
  await N.toucher(p,'#mGestes');assert.equal(await p.isVisible('#mListe'),true);
  await N.toucher(p,'#mReprendre');assert.equal(await p.isVisible('#menu'),false);
  await N.toucher(p,'#menuBtn');await N.toucher(p,'#mQuitter');assert.equal(await val(()=>document.getElementById('ov').hidden),true,'un seul toucher ne quitte pas');
  await N.toucher(p,'#mQuitter');assert.equal(await val(()=>document.getElementById('ov').hidden),false,'retour à l\'accueil');assert.equal((await N.etat(p)).fin,true);
 });
 test('Aucune erreur JavaScript pendant tout le parcours',()=>assert.deepEqual(o.erreurs,[]));
});

test('Paysage (2.15) : sur un téléphone tenu en paysage, le jeu demande de le tourner',async()=>{
 const srv=await demarrer(RACINE),nav=await N.lancer();
 try{const o=await N.ouvrir(nav,srv.url+'?rendu=2d',{format:'paysage'});
  assert.equal(await o.page.isVisible('#tourner'),true);assert.match(await o.page.textContent('#tourner'),/Tourne ton téléphone/);
  assert.deepEqual(o.erreurs,[]);await o.fermer()}
 finally{await nav.close();await srv.fermer()}});
}
