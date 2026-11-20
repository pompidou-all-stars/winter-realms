/* Labyrinthe de l'IA (2.5) : plan cible généré au début de la partie, ordre de construction, rôles des tours. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie}=require('../outils/moteur');
const C=13,SPI=6;
const plan=(graine,lv=0,siege=1)=>{const S=charger('actuel',{graine});const G=partie(S,{ia:[0,1,1,1],difficulte:lv});return {S,G,b:G.B[siege],M:S.mzStep(G.B[siege],Infinity)}};

test('Le plan complet laisse toujours un chemin, bien plus long que la ligne droite (16)',()=>{
 for(let g=1;g<=8;g++)for(let lv=0;lv<3;lv++){const {S,M}=plan(g,lv);const L=S.plen(M.w);
  assert.ok(L>0,`graine ${g}, difficulté ${lv} : chemin bloqué`);assert.ok(L>=60,`graine ${g} : chemin ${L} < 60`);
  assert.equal(M.w[SPI],0);assert.equal(M.w[16*C+6],0)}
});
test('Chaque début de l\'ordre de construction laisse le chemin ouvert, et le chemin s\'allonge avec les tours',()=>{
 const {S,M}=plan(3);const w=new Uint8Array(13*17);let L20=0;
 M.ord.forEach((i,n)=>{w[i]=1;const L=S.plen(w);assert.ok(L>0,`bloqué après ${n+1} tours`);if(n==19)L20=L});
 assert.ok(L20>=24,`après 20 tours, chemin ${L20}`);/* 24 depuis la 2.33 (ordre selon l'exposition, 25,6 pour cette graine) ; 26 avant */
});
test('Deux graines différentes donnent deux labyrinthes différents ; la même graine donne le même',()=>{
 const a=plan(1).M.w.join(''),b=plan(2).M.w.join(''),a2=plan(1).M.w.join('');
 assert.notEqual(a,b);assert.equal(a,a2);
});
test('Givre : 2 à 6 emplacements, répartis tout le long du chemin final',()=>{
 for(let g=1;g<=5;g++){const {S,M}=plan(g);const P=S.mzPath(M.w),gi=[];M.role.forEach((r,i)=>{if(r==2)gi.push(i)});
  assert.ok(gi.length>=2&&gi.length<=6,`graine ${g} : ${gi.length} Givre`);
  /* chaque tiers du chemin a au moins un Givre à portée (2,5 cases) */
  for(let t=0;t<3;t++){const part=P.slice(Math.floor(P.length*t/3),Math.floor(P.length*(t+1)/3));
   assert.ok(gi.some(i=>part.some(j=>Math.hypot(i%C-j%C,(i/C|0)-(j/C|0))<=2.5)),`graine ${g} : tiers ${t} sans Givre`)}}
});
/* 2.36 : le test de durée de la génération est dans labyrinthe-duree.test.js, lancé seul par tout.js. */
/* depuis la 2.6 */
test('Aucun mur inutile : chaque tour qui ne touche pas le chemin est nécessaire à sa longueur',()=>{
 for(let g=1;g<=6;g++){const {S,M}=plan(g);const w=M.w.slice(),L=S.plen(w),P=S.mzPath(w);
  for(const i of M.ord){const x=i%C,y=i/C|0;if(P.some(j=>Math.abs(j%C-x)<=1&&Math.abs((j/C|0)-y)<=1))continue;
   w[i]=0;assert.ok(S.plen(w)<L,`graine ${g} : tour inutile en (${x},${y})`);w[i]=1}}
});
/* depuis la 2.33 : ordre de construction selon l'exposition (cases du chemin vues par chaque tour) ; avant : chemin d'au moins 50 cases à 40 tours */
test('Milieu de partie : à 15, 25 et 40 tours du plan, les tours voient le chemin du moment (exposition) et le chemin dépasse 35 cases à 40 tours',()=>{
 const voit=(i,P)=>P.filter(j=>Math.hypot(j%C-i%C,(j/C|0)-(i/C|0))<=2.5).length,expo={15:4,25:5,40:6};
 for(const n of [15,25,40]){let loin=0,cov=0;
  for(let g=1;g<=8;g++){const {S,M}=plan(g);const w=new Uint8Array(13*17),ts=M.ord.slice(0,n);ts.forEach(i=>w[i]=1);const P=S.mzPath(w);
   for(const i of ts){const v=voit(i,P);cov+=v/n/8;if(!v)loin++}
   if(n==40){const L=S.plen(w);assert.ok(L>=35,`graine ${g} : chemin de ${L} cases à 40 tours`);assert.equal(M.pre[2],L)}}
  assert.ok(loin<=.2*n*8,`${n} tours : ${loin} tours sur ${n*8} hors de portée du chemin`);
  assert.ok(cov>=expo[n],`${n} tours : chaque tour voit ${cov.toFixed(1)} cases du chemin en moyenne (au moins ${expo[n]} attendu)`)}
});
/* depuis la 2.33 : type des tours ordinaires selon la menace reçue */
test('Répartition : sans menace connue, l\'IA garde le type prévu par son plan ; face à des blindés, un Archer vaut moins par or que face à des monstres ordinaires',()=>{
 /* 2.39 : Hautroc (sans poison, qui ignore l'armure) */
 const S=charger('actuel',{graine:2}),G=partie(S,{ia:[0,1,1,1],factions:[0,3,1,2]}),b=G.B[1],M=S.mzStep(b,Infinity);const i=M.ord.find(i=>Math.abs(i%C-6)>2&&M.role[i]==0);assert.ok(i!==undefined);
 assert.equal(S.choixType(b,i,0,10),0,'menace inconnue : type du plan');
 const base=b.classId*10,x=i%C,y=i/C|0;G.time=300;b.gold=1e7;for(const j of M.ord)b.place(j%C,j/C|0,base);
 S.observer(b);b.menace.fill(0);b.menace[S.NORM[5]]=1000;const ord=S.contreMenace(b,base,x,y);
 b.menace.fill(0);b.menace[S.CR.findIndex(T=>T.n.startsWith('Scarab'))]=1000;const bl=S.contreMenace(b,base,x,y);
 assert.ok(bl<ord/2,`Archer : ${bl.toFixed(3)} contre des blindés, ${ord.toFixed(3)} contre des monstres ordinaires`);
 assert.notEqual(S.choixType(b,i,0,10),0,'face à des blindés, autre chose qu\'un Archer');
});
