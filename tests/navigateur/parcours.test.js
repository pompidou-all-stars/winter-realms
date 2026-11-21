/* Parcours automatisé d'un joueur dans un navigateur Chromium au format téléphone, dans le vrai jeu : la vue 3D
   (seule vue proposée depuis la 2.22). Depuis la 2.29, ce fichier réunit l'ancien parcours 2D (interface) et l'ancien parcours 3D.
   WebGL tourne en rendu logiciel SwiftShader (pas besoin de carte graphique) ; WR_GPU=1 utilise la vraie carte graphique.
   Depuis la 2.15, le jeu se joue en portrait : en paysage, on vérifie que le jeu demande de tourner le téléphone.
   La 2D ne sert plus qu'en secours (appareil où la 3D ne se charge pas) : un test court à la fin vérifie qu'on peut y jouer.
   Ce test vérifie que le parcours fonctionne dans CE navigateur de test : ce n'est pas une garantie
   de compatibilité avec tous les téléphones (Safari iOS, anciens Android, etc. ne sont pas testés). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const N=require('../outils/navigateur'),{demarrer}=require('../outils/serveur'),{RACINE}=require('../outils/moteur');

if(!N.disponible()){test('Parcours navigateur',{skip:'Playwright n\'est pas installé sur cette machine : tests navigateur ignorés'},()=>{})}
else{
test.describe('Parcours mobile en 3D — portrait',()=>{
 let srv,nav,o,p;
 test.before(async()=>{srv=await demarrer(RACINE);nav=await N.lancer({webgl:true});o=await N.ouvrir(nav,srv.url,{format:'portrait'});p=o.page});
 test.after(async()=>{if(o)await o.fermer();if(nav)await nav.close();if(srv)await srv.fermer()});
 const val=f=>p.evaluate(f),r3d=()=>p.evaluate(()=>R3D_ETAT());
 /* une case dont le centre est bien visible, entre le bandeau et le dock */
 async function caseVisible(exclues=[]){const b=await p.locator('#stage').boundingBox(),d=await p.locator('#ctl').boundingBox();
  for(let y=4;y<15;y++)for(let x=1;x<12;x++){if(x==6||exclues.some(([a,c])=>a==x&&c==y))continue;const c=await N.centreCase(p,x,y);
   if(c.x>b.x+60&&c.x<b.x+b.width-60&&c.y>b.y+140&&c.y<d.y-70)return {x,y}}return null}

 test('La page s\'ouvre sans erreur, avec l\'écran d\'accueil, sans lien vers la 2D',async()=>{
  assert.match(await p.title(),/Winter Realms/);assert.equal(await val(()=>document.getElementById('ov').hidden),false);
  assert.equal(await p.isVisible('#tourner'),false,'pas de message « tourne ton téléphone » en portrait');
  assert.equal(await p.locator('#mode3d').count(),0,'pas de lien vers la 2D sur l’accueil');
  assert.deepEqual(o.erreurs,[]);
 });
 test('Le rendu 3D se charge (WebGL, modèles) avec la caméra tactique en perspective',async()=>{
  assert.equal(await N.attendre3D(p),true,'rendu 3D prêt');
  const e=await r3d();assert.equal(e.on,true);assert.equal(e.scene.vue.perspective,true);assert.equal(e.scene.vue.az,0);
  assert.equal(await p.locator('#main3d').count(),1,'canevas WebGL présent');assert.deepEqual(o.erreurs,[]);
 });
 test('À l\'ouverture, la faction Humains est présélectionnée et les boutons de difficulté sont actifs',async()=>{
  assert.equal(await p.getAttribute('[data-faction="0"]','aria-pressed'),'true');
  for(const l of [0,1,2])assert.equal(await p.isDisabled('#go'+l),false);
 });
 test('Les cinq factions sont sélectionnables et donnent chacune accès à dix tours',async()=>{
  const factions=[[0,'Humains'],[3,'Robots'],[1,'Créatures'],[2,'Herbe'],[4,'Magique']];
  assert.deepEqual(await p.locator('#factions strong').allTextContents(),factions.map(([,nom])=>nom));
  for(const [id,nom] of factions){
   await N.toucher(p,'[data-faction="'+id+'"]');
   assert.equal(await p.locator('#factions [aria-pressed="true"]').count(),1);
   assert.equal(await p.getAttribute('[data-faction="'+id+'"]','aria-pressed'),'true');
   assert.match(await p.textContent('#factionStatus'),new RegExp(nom));
   assert.equal(await val(()=>RACES[chosenClass].tours.length),10);
  }
  await N.toucher(p,'[data-faction="2"]');
 });
 test('Lancer une partie en Normal : l\'accueil disparaît, l\'horloge tourne, une astuce s\'affiche et aucune fiche',async()=>{
  await N.toucher(p,'#go0');assert.equal(await val(()=>document.getElementById('ov').hidden),true);
  await N.avancer(p,2100);const e=await N.etat(p);assert.equal(e.horloge,'0:02');assert.deepEqual([e.or,e.revenu,e.vies,e.faction],[200,10,40,2]);
  assert.equal(await p.isVisible('#astuce'),true);assert.equal(e.fiche,'','sans choix, pas de fiche (2.15)');
 });
 test('Musique (2.16) : un des 3 thèmes démarre dès le premier toucher, puis ils s’enchaînent en boucle',async()=>{
  const m=()=>p.evaluate(()=>({src:MUSIQUE.el?MUSIQUE.el.src:'',i:MUSIQUE.i,n:MUSIQUE.pistes.length}));
  const a=await m();assert.match(a.src,/assets\/musique\/winter-realm(-1|-2)?\.mp3$/,'thème en cours : '+a.src);assert.equal(a.n,3);
  for(let k=1;k<=3;k++){await p.evaluate(()=>MUSIQUE.el.dispatchEvent(new Event('ended')));const b=await m();assert.equal(b.i,(a.i+k)%3,'thème suivant ('+k+')')}
 });
 test('Interface (2.15) : bandeau en haut, dock en bas, terrain 3D sur tout l\'écran, flèches de rotation',async()=>{
  const s=await p.locator('#stage').boundingBox(),h=await p.locator('#hud').boundingBox(),c=await p.locator('#ctl').boundingBox(),v=p.viewportSize();
  assert.ok(s.width>=v.width-1&&s.height>=v.height-1,'le terrain couvre l\'écran');assert.ok(h.y<60,'bandeau en haut');assert.ok(c.y+c.height>=v.height-1,'dock en bas');
  for(const id of ['#menuBtn','#fs','#cartesBtn','#rotG','#rotD'])assert.equal(await p.isVisible(id),true,id+' visible');
  const e=(await r3d()).scene;assert.ok(e.dessins>5,'appels de dessin : '+e.dessins);assert.ok(e.triangles>3000,'triangles : '+e.triangles);
 });
 test('Sans tour choisie, toucher une case ne construit rien et le dit',async()=>{
  await N.toucherCase(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[]);assert.equal(e.projet,null);assert.match(e.toast,/Choisis d’abord une tour/);
 });
 test('Choisir une carte de tour (2.15) : la fiche la décrit en clair, rien n\'est construit',async()=>{
  await N.toucherCarte(p,'Arbre archer');const e=await N.etat(p);assert.equal(e.choix,20);assert.equal(e.or,200);
  assert.match(e.fiche,/Arbre archer/);assert.match(e.fiche,/Dégâts\/s/);assert.match(e.fiche,/Portée/);assert.match(e.fiche,/sol et air/);assert.match(e.fiche,/Croissance/);assert.match(e.fiche,/deux fois une case/);
  assert.equal(await p.getAttribute('#bar button[aria-label^="Arbre archer,"]','class'),'sel');
  assert.match(await p.textContent('#bar button[aria-label^="Arbre archer,"]'),/^20 or$/,'la carte ne montre que le prix');
 });
 test('Construction : un premier toucher montre la tour fantôme et sa portée en 3D, sans rien construire',async()=>{
  await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;assert.deepEqual(e.tours,[]);assert.equal(e.or,200);
  assert.deepEqual(e.projet,{x:3,y:5,k:20});assert.equal(e.toast,'','2.31 : plus de bulle au milieu du terrain');
  assert.equal(await p.isVisible('#aideBat'),true,'2.34 : consigne entre les flèches');assert.match(await p.textContent('#aideBat'),/Touche encore la case pour construire/);assert.doesNotMatch(e.fiche,/Racines/,'2.31 : fiche réduite pendant l’aperçu');
  assert.equal(await val(()=>document.getElementById('fiche').classList.contains('compacte')),true);assert.equal(s.fantome,true);assert.equal(s.portee,true);
 });
 test('Construction : un second toucher sur la même case construit la tour en 3D et débite son prix',async()=>{
  await N.toucherCase(p,3,5);await N.avancer(p,50);const e=await N.etat(p),s=(await r3d()).scene;
  assert.deepEqual(e.tours,[{x:3,y:5,k:20,lv:1}]);assert.equal(e.or,180);assert.equal(await p.isVisible('#aideBat'),false,'consigne retirée après la pose');assert.equal(e.projet,null);assert.equal(s.tours,1);assert.equal(s.fantome,false);
 });
 test('Construction : toucher une autre case déplace l\'aperçu, sans construire',async()=>{
  await N.toucherCase(p,8,5);await N.toucherCase(p,9,5);assert.equal(await p.isVisible('#aideBat'),false,'consigne une seule fois par partie');assert.doesNotMatch((await N.etat(p)).fiche,/deux fois une case/);const e=await N.etat(p);assert.deepEqual(e.projet,{x:9,y:5,k:20});assert.equal(e.tours.length,1);assert.equal(e.or,180);
 });
 test('Une pose impossible est refusée avec un message',async()=>{
  await N.toucherCase(p,6,0);const e=await N.etat(p);assert.equal(e.tours.length,1);assert.equal(e.or,180);
  assert.equal(await p.textContent('#toast'),'Impossible ici : le chemin serait bloqué');assert.equal(await val(()=>document.getElementById('toast').hidden),false);
 });
 test('Toucher le pied de la tour ouvre sa fiche ; Améliorer (après le chantier) puis Vendre fonctionnent',async()=>{
  await N.avancer(p,1500);await N.toucherCase(p,3,5);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);
  assert.match(e.fiche,/niveau 1\/5/);assert.match(e.fiche,/Niveau 2 :/);
  assert.ok(e.boutons.some(b=>b.startsWith('Améliorer'))&&e.boutons.some(b=>b.startsWith('Vendre')));
  await N.toucher(p,'#fiche button:has-text("Améliorer")');e=await N.etat(p);assert.equal(e.tours[0].lv,2);assert.equal(e.or,150);
  await N.toucher(p,'#fiche button:has-text("Vendre")');e=await N.etat(p);assert.equal(e.tours.length,0);assert.equal(e.or,185);assert.equal(e.panneauOuvert,false);
  await N.avancer(p,50);assert.equal((await r3d()).scene.tours,0,'tour retirée de la scène 3D');
 });
 test('Le × de la fiche annule le choix de la tour',async()=>{
  await N.toucher(p,'#fiche .fermer');const e=await N.etat(p);assert.equal(e.choix,null);assert.equal(e.fiche,'');
 });
 test('Départ (2.30) : « Construis ! », chrono de 30 s dans le bandeau, onglets de monstres verrouillés, puis « Envoie et résiste ! »',async()=>{
  const v=()=>p.evaluate(()=>({prep:!document.getElementById('prep').hidden,n:document.getElementById('prepN').textContent,horloge:getComputedStyle(document.getElementById('clock')).display,
   verrou:[...document.querySelectorAll('#tabs button.mon')].map(b=>b.disabled),annonce:document.getElementById('annonce').hidden?'':document.getElementById('annonce').className,ph:dep.ph,tab}));
  let s=await v();assert.equal(s.prep,true,'chrono du bandeau');assert.match(s.n,/^0:[0-2]\d$/);assert.equal(s.horloge,'none');assert.deepEqual(s.verrou,[true,true,true]);assert.equal(s.ph,1,'bannière « Construis ! » montrée');
  await p.evaluate(()=>document.querySelector('#tabs button[data-t="n"]').click());assert.equal((await v()).tab,'t','onglet verrouillé');
  const or=(await N.etat(p)).or;await p.evaluate(()=>playerSend(0));await N.avancer(p,50);let e=await N.etat(p);assert.equal(e.or,or);assert.match(e.toast,/Construis d’abord/);
  await p.evaluate(()=>{G.time=GRACE-.01});await N.avancer(p,100);s=await v();
  assert.equal(s.prep,false);assert.notEqual(s.horloge,'none');assert.deepEqual(s.verrou,[false,false,false]);assert.equal(s.annonce,'envoie');assert.equal(s.ph,2);
  await N.avancer(p,3000);assert.equal((await v()).annonce,'','bannière refermée');
 });
 test('Envoyer (2.15) : le 1er toucher choisit le monstre, chaque toucher suivant envoie un groupe ; les monstres apparaissent en 3D chez l\'adversaire',async()=>{
  await N.toucher(p,'#tabs button[data-t="n"]');await N.toucherCarte(p,'Sapeur gobelin');let e=await N.etat(p);
  assert.equal(e.or,185,'le premier toucher n\'envoie rien');assert.match(e.fiche,/Sapeur gobelin/);assert.match(e.fiche,/Chaque toucher/);
  await N.toucherCarte(p,'Sapeur gobelin');e=await N.etat(p);assert.equal(e.or,175);assert.equal(e.revenu,11);
  await N.toucherCarte(p,'Sapeur gobelin');e=await N.etat(p);assert.equal(e.or,165);assert.equal(e.revenu,12);assert.match(e.toast,/^×2 · /,'compteur des envois enchaînés');
  await N.toucher(p,'#tabs button[data-t="t"]');
  /* les monstres apparaissent en moins de 1,4 s ; l'IA peut les tuer vite : on garde le maximum observé */
  await p.evaluate(()=>setView(1));let max=0;
  try{for(let i=0;i<12;i++){await N.avancer(p,200);max=Math.max(max,(await r3d()).scene.monstres)}}
  finally{await p.evaluate(()=>setView(0));await N.avancer(p,50)}
  assert.ok(max>=1,'monstres en 3D : '+max);
 });
 test('Onglet « Spéciaux » : paliers de monstres ; le palier 2 s’ouvre contre son prix et montre ses monstres',async()=>{
  await N.toucher(p,'#tabs button[data-t="s"]');assert.equal(await p.isVisible('#paliers'),true);
  assert.match(await p.textContent('#paliers button:has-text("Palier 2")'),/300 or/);
  await N.toucherCarte(p,'Ankylosaure de guerre');assert.match((await N.etat(p)).fiche,/blindée/);
  await N.toucher(p,'#paliers button:has-text("Palier 2")');assert.equal(await p.evaluate(()=>P.tier),1,'pas assez d’or : palier fermé');
  await p.evaluate(()=>{P.gold+=300});const or=await p.evaluate(()=>P.gold);await N.toucher(p,'#paliers button:has-text("Palier 2")');
  assert.equal(await p.evaluate(()=>P.tier),2);assert.equal(await p.evaluate(()=>P.gold),or-300);
  assert.equal(await p.locator('#bar button[aria-label^="Protoplasme aux mille yeux,"]').count(),1,'monstres du palier 2 affichés');
  await N.toucher(p,'#tabs button[data-t="t"]');assert.equal(await p.isVisible('#paliers'),false);
 });
 test('Bouton Adversaires : une vignette affiche le terrain d\'une IA (lecture seule), puis on revient au sien',async()=>{
  await N.toucher(p,'#cartesBtn');assert.equal(await p.isVisible('#chips'),true);await N.toucher(p,'#chips .chip >> nth=1');
  assert.equal((await N.etat(p)).vue,1);assert.equal(await val(()=>document.getElementById('banner').hidden),false);
  assert.equal(await val(()=>document.getElementById('chips').hidden),true,'le panneau se referme');assert.match(await p.textContent('#cartesBtn'),/IA 1/);
  await N.toucherCarte(p,'Arbre archer');await N.toucherCase(p,2,8);const e=await N.etat(p);assert.match(e.toast,/lecture seule/);assert.equal(e.projet,null);
  await N.toucher(p,'#banner');assert.equal((await N.etat(p)).vue,0);assert.equal(await val(()=>document.getElementById('banner').hidden),true);
  await N.toucher(p,'#fiche .fermer');
 });
 test('Le revenu tombe à 10 s de jeu',async()=>{
  const avant=(await N.etat(p)).or;await N.avancer(p,10000);const e=await N.etat(p);assert.ok(e.temps>10);assert.equal(e.or,avant+12);
 });
 test('Glisser le doigt déplace la carte (le terrain suit le doigt), sans rien construire',async()=>{
  await N.toucherCarte(p,'Arbre archer');
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
  assert.equal((await N.etat(p)).choix,20,'la tour choisie est restée');
  const cible=await caseVisible();assert.ok(cible,'une case visible');
  const avant=(await N.etat(p)).or;await N.construire(p,cible.x,cible.y);
  const e=await N.etat(p);assert.ok(e.tours.some(t=>t.x==cible.x&&t.y==cible.y),'tour posée en ('+cible.x+','+cible.y+')');assert.equal(e.or,avant-20);
 });
 test('Amélioration en lot (2.31) : toucher deux fois une tour choisit les tours pareilles, les icônes en trop rétrécissent, un bouton les améliore',async()=>{
  await p.evaluate(()=>{P.gold+=500});
  for(let i=0;i<2;i++){const ex=(await N.etat(p)).tours.map(t=>[t.x,t.y]);const c=await caseVisible(ex);assert.ok(c,'une case visible');await N.construire(p,c.x,c.y)}
  await N.avancer(p,1500);const e0=await N.etat(p),t0=e0.tours.find(t=>t.k==20&&t.lv==1),n=Math.min(10,e0.tours.filter(t=>t.k==20&&t.lv==1).length);assert.ok(n>=3,'au moins 3 tours pareilles : '+n);
  await N.toucherCase(p,t0.x,t0.y);let e=await N.etat(p);assert.equal(e.panneauOuvert,true);assert.match(e.fiche,/Touche encore la tour/);
  await N.toucherCase(p,t0.x,t0.y);e=await N.etat(p);
  assert.match(e.fiche,new RegExp(n+' × Arbre archer'));assert.equal(await p.locator('#fiche .rangee span').count(),n,'une icône par tour');
  assert.equal(await p.locator('#fiche .rangee span.non').count(),0);
  const cout=await p.evaluate(()=>lot.c);await p.evaluate(c=>{P.gold=c+1},cout);await N.avancer(p,50);
  assert.equal(await p.locator('#fiche .rangee span.non').count(),n-1,'les icônes des tours qu’on ne peut pas payer rétrécissent');
  assert.match(await p.textContent('#fiche .actions button'),new RegExp('Améliorer 1 / '+n));
  await N.toucher(p,'#fiche .actions button');e=await N.etat(p);
  assert.equal(e.tours.filter(t=>t.k==20&&t.lv==2).length,1,'une seule tour améliorée');assert.equal(e.or,1);assert.match(e.toast,/1 tour améliorée/);
  await p.evaluate(()=>{P.gold+=1000});
 });
 test('Panneau « Mes tours » (2.37) : cocher un type, choisir le niveau, la file paie ce qu’elle peut puis le reste, et s’annule',async()=>{
  await N.toucher(p,'#parcBtn');assert.equal(await p.locator('#parc').isVisible(),true,'le panneau s’ouvre');
  const n=await p.evaluate(()=>P.t.filter(t=>t.k==20&&t.lv<3).length);assert.ok(n>=3,'au moins 3 Arbre archer sous le niveau 3 : '+n);
  await p.locator('#parc .ligne',{hasText:'Arbre archer'}).click();await p.locator('#parc .niv button',{hasText:'3'}).click();
  /* juste assez d’or pour une amélioration (niveau 1 → 2) : la file la paie, le reste attend */
  await p.evaluate(()=>{P.gold=upCost({k:20,lv:1})});await N.avancer(p,50);
  assert.match(await p.textContent('#parcRes'),/Ton or en paie 1 tout de suite/);
  await p.locator('#parcGo').click();await N.avancer(p,300);
  let e=await p.evaluate(()=>({file:FILE.length,or:Math.floor(P.gold),n2:P.t.filter(t=>t.k==20&&t.lv==2).length,badge:document.getElementById('fileN').textContent}));
  assert.equal(e.file,1,'un ordre dans la file');assert.ok(e.or<30,'l’or est dépensé : '+e.or);assert.match(e.badge,/⏫ \d+/);
  assert.equal(await p.locator('#parc .ordre').count(),1,'l’ordre se voit dans le panneau');
  /* avec de l’or, chaque tour monte niveau par niveau jusqu’au 3, puis l’ordre disparaît */
  await p.evaluate(()=>{P.gold+=2000});await N.avancer(p,8000);
  e=await p.evaluate(()=>({file:FILE.length,sous3:P.t.filter(t=>t.k==20&&t.lv<3).length,chantier:P.t.filter(t=>t.b>0).length}));
  assert.equal(e.sous3,0,'toutes au niveau 3 au moins');assert.equal(e.file,0,'ordre terminé');
  /* un nouvel ordre se consulte et s’annule */
  await p.evaluate(()=>{P.gold=0});await p.locator('#parc .ligne',{hasText:'Arbre archer'}).click();await p.locator('#parc .niv button',{hasText:'5'}).click();
  await p.locator('#parcGo').click();await N.avancer(p,100);assert.equal(await p.locator('#parc .ordre').count(),1);
  await p.locator('#parc .annuler').click();await N.avancer(p,100);
  assert.equal(await p.evaluate(()=>FILE.length),0,'file annulée');assert.equal(await p.locator('#fileN').isVisible(),false);
  await N.toucher(p,'#parcBtn');assert.equal(await p.locator('#parc').isVisible(),false,'le bouton referme le panneau');
  await p.evaluate(()=>{P.gold+=1000});
 });
 test('Tour choisie toujours visible (2.35) : si la fiche la cache, la vue glisse pour la montrer au-dessus ; détails sur une ligne',async()=>{
  /* une tour sur une rangée basse (la vue ne dépasse pas les bords du terrain : une tour du haut ne peut pas finir sous la fiche) */
  const t=await p.evaluate(()=>{pick=null;lot=null;render();for(let y=R-2;y>8;y--)for(const x of [2,10,3,9])if(peutConstruire(x,y,sel)===''){doAction({type:'place',x,y,k:sel});return {x,y}}});
  assert.ok(t,'une case libre en bas du terrain');await N.avancer(p,50);
  /* plus aucune fiche (le × annule aussi le choix de la carte) : la tour se touche juste au-dessus de la console */
  await N.toucher(p,'#fiche .fermer');assert.equal((await N.etat(p)).fiche,'');
  /* la tour est amenée tout en bas de la zone libre, là où sa fiche la recouvrira */
  await p.evaluate(t=>{const r=main.getBoundingClientRect();R3D.api.amener(t.x+.5,t.y+.5,r.width/2,document.getElementById('console').getBoundingClientRect().top-r.top-25)},t);await N.avancer(p,1500);
  const y0=(await N.centreCase(p,t.x,t.y)).y;await N.toucherCase(p,t.x,t.y);assert.equal((await N.etat(p)).panneauOuvert,true);
  const haut=await p.evaluate(()=>document.getElementById('fiche').getBoundingClientRect().top);
  assert.ok(y0>haut,'au départ, la fiche cache la tour ('+Math.round(y0)+' > '+Math.round(haut)+')');
  await N.avancer(p,1500);const y1=(await N.centreCase(p,t.x,t.y)).y;
  assert.ok(y1<haut-15&&y1>haut-60,'la tour est juste au-dessus de la fiche ('+Math.round(y1)+', fiche à '+Math.round(haut)+')');
  const ex=p.locator('#fiche .ex');assert.equal(await ex.evaluate(e=>getComputedStyle(e).whiteSpace),'nowrap','détails sur une ligne');
  await ex.click();assert.equal(await ex.evaluate(e=>e.classList.contains('ouvert')),true,'un toucher déplie les détails');
  /* l'avance finale laisse render() finir son image suivante (position de la barre des cartes) avant le test d'après */
  await ex.click();await p.evaluate(()=>{pick=null;render()});await N.avancer(p,50);
 });
 test('Barre des cartes (2.31) : la molette de la souris la fait défiler',async()=>{
  await p.evaluate(()=>{bar.scrollLeft=0});const b=await p.locator('#bar').boundingBox();
  await p.mouse.move(b.x+b.width/2,b.y+b.height/2);await p.mouse.wheel(0,240);await N.avancer(p,100);
  assert.ok(await p.evaluate(()=>bar.scrollLeft)>100,'la barre a défilé');
 });
 test('Quêtes bonus (2.38) : bannière au début, pastille de suivi sous le bandeau, bannière du gagnant et or versé',async()=>{
  const v=()=>p.evaluate(()=>({annonce:document.getElementById('annonce').hidden?'':document.getElementById('annonce').className,texte:document.getElementById('annonce').innerText,
   pastille:document.getElementById('quete').hidden?'':document.getElementById('quete').innerText,or:Math.floor(P.gold)}));
  await p.evaluate(()=>{G.qu=null;G.quN=0;G.quF=QUETES.map(q=>q.id).filter(x=>x!='picsou');P.gold=1e5});await N.avancer(p,100);let s=await v();
  assert.equal(s.annonce,'quete');assert.match(s.texte,/Quête bonus/i);assert.match(s.texte,/Picsou/);assert.match(s.texte,/\+\d+ or/);
  assert.match(s.pastille,/Picsou/);assert.match(s.pastille,/1er/,'le plus riche mène');
  const or=await p.evaluate(()=>G.qu.or);await p.evaluate(()=>{G.time=G.qu.fin});await N.avancer(p,100);s=await v();
  assert.equal(s.annonce,'gagne');assert.match(s.texte,/c’est toi/);assert.ok(s.or>=1e5+or,'or de la quête versé');assert.equal(s.pastille,'','pastille retirée');
  await N.avancer(p,3500);assert.equal((await v()).annonce,'','bannière refermée');
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
 test('La scène WebGL rend les 50 tours et 50 traînées simultanément, puis retire les projectiles',async()=>{
  const compte=await p.evaluate(async()=>{
   const A=R3D.api;
   await A.precharger([0,1,2,3,4]);
   const plateau=new Board(0,'Charge','#d8b45c',0,0);
   plateau.t=TW.map((_,k)=>({x:1+k%10,y:3+Math.floor(k/10),k,lv:1,a:0}));
   plateau.pr=plateau.t.map(({x,y,k})=>({id:k,k,sx:x+.5,sy:y+.2,x:x+.8,y:y+.4,tx:x+1,ty:y+1,tot:1,a:0}));
   A.dessiner(plateau,0,{rng});
   const dense=A.etat();
   plateau.pr=[];
   A.dessiner(plateau,.1,{rng});
   const vide=A.etat();
   dessinerVue3D(.2);
   return [dense.tours,dense.projectiles,vide.projectiles,dense.dessins];
  });
  assert.deepEqual(compte.slice(0,3),[50,50,0]);
  assert.ok(compte[3]>0);
 });
 test('Aucune erreur JavaScript pendant tout le parcours',()=>assert.deepEqual(o.erreurs,[]));
});

test('Paysage (2.15) : sur un téléphone tenu en paysage, le jeu demande de le tourner',async()=>{
 const srv=await demarrer(RACINE),nav=await N.lancer({webgl:true});
 try{const o=await N.ouvrir(nav,srv.url,{format:'paysage'});
  assert.equal(await o.page.isVisible('#tourner'),true);assert.match(await o.page.textContent('#tourner'),/Tourne ton téléphone/);
  assert.deepEqual(o.erreurs,[]);await o.fermer()}
 finally{await nav.close();await srv.fermer()}});

/* secours : si la 3D ne se charge pas (appareil sans WebGL 2, module introuvable), le jeu passe en 2D et reste jouable ;
   ?rendu=2d force la même 2D (dépannage et anciens outils) */
test('Secours 2D : si la 3D ne se charge pas, le jeu le dit, passe en 2D et on peut construire',async()=>{
 const srv=await demarrer(RACINE),nav=await N.lancer();
 try{const o=await N.ouvrir(nav,srv.url,{bloquer:['rendu3d.js']}),p=o.page;
  assert.equal(await N.attendre3D(p,15000),false,'la 3D échoue');const r=await p.evaluate(()=>R3D_ETAT());assert.equal(r.on,false);assert.equal(r.echec,true);
  assert.match(await p.textContent('#toast'),/3D indisponible sur cet appareil/);assert.equal(await p.locator('#main3d').count(),0);
  await N.toucher(p,'#go0');await N.avancer(p,600);assert.equal(await p.isVisible('#rotG'),false,'pas de flèches de rotation en 2D');
  await N.toucherCarte(p,'Archer royal');await N.construire(p,3,5);const e=await N.etat(p);assert.deepEqual(e.tours,[{x:3,y:5,k:0,lv:1}]);assert.equal(e.or,180);
  assert.deepEqual(o.erreurs.filter(m=>!/rendu3d|Failed to load|ERR_FAILED|module script/i.test(m)),[]);await o.fermer();
  const o2=await N.ouvrir(nav,srv.url+'?rendu=2d');assert.equal((await o2.page.evaluate(()=>R3D_ETAT())).on,false,'?rendu=2d force la 2D');assert.deepEqual(o2.erreurs,[]);await o2.fermer()}
 finally{await nav.close();await srv.fermer()}});
}
