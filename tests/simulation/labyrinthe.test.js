/* Labyrinthe de l'IA (2.5) : plan cible généré au début de la partie, ordre de construction, rôles des tours. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
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
 assert.ok(L20>=26,`après 20 tours, chemin ${L20}`);
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
/* La découpe est vérifiée de façon certaine (nombre de tranches), la durée seulement comme garde-fou :
   les machines de GitHub sont plus ou moins chargées, d'où la meilleure de 3 mesures et une marge (révision de la 2.11). */
test('La génération est découpée en plusieurs tranches courtes (moins de 10 ms par tranche, moins de 150 ms au total ; 150 depuis la 2.18, chemin en 8 directions)',()=>{
 let meilleurMax=Infinity,meilleurTot=Infinity,tranches=0;
 for(let essai=0;essai<3;essai++){
  const S=charger('actuel',{graine:4});const G=partie(S,{ia:[0,1,1,1],difficulte:2});const b=G.B[1];let tot=0,max=0,M=null,n=0;
  S.mzStep(G.B[2],Infinity);/* échauffement du moteur JavaScript */
  while(!M){const t=process.hrtime.bigint();M=S.mzStep(b,600);const d=Number(process.hrtime.bigint()-t)/1e6;tot+=d;max=Math.max(max,d);n++}
  tranches=n;meilleurMax=Math.min(meilleurMax,max);meilleurTot=Math.min(meilleurTot,tot)}
 assert.ok(tranches>=3,`génération faite en ${tranches} tranche(s) seulement : elle n'est plus découpée`);
 assert.ok(meilleurMax<10,`tranche de ${meilleurMax.toFixed(1)} ms`);assert.ok(meilleurTot<150,`total ${meilleurTot.toFixed(1)} ms`);
});
test('En partie, l\'IA construit son plan, continue au-delà de 36 tours et n\'a pas de Mage avant la menace des Spectres',()=>{
 const S=charger('actuel',{graine:5});const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e9;const b=G.B[1];b.lives=1e9;
 avancer(G,140);assert.equal(b.t.filter(t=>S.TW[t.k].mg).length,0,'Mage avant 2:30');
 b.gold+=1e5;b.dp+=1e5;avancer(G,60);
 assert.ok(b.t.length>36,`seulement ${b.t.length} tours`);
 for(const t of b.t)assert.equal(b.mz.w[t.y*C+t.x],1,`tour hors du plan en (${t.x},${t.y})`);
});

/* depuis la 2.6 */
test('Aucun mur inutile : chaque tour qui ne touche pas le chemin est nécessaire à sa longueur',()=>{
 for(let g=1;g<=6;g++){const {S,M}=plan(g);const w=M.w.slice(),L=S.plen(w),P=S.mzPath(w);
  for(const i of M.ord){const x=i%C,y=i/C|0;if(P.some(j=>Math.abs(j%C-x)<=1&&Math.abs((j/C|0)-y)<=1))continue;
   w[i]=0;assert.ok(S.plen(w)<L,`graine ${g} : tour inutile en (${x},${y})`);w[i]=1}}
});
test('Milieu de partie : avec 40 tours du plan, le chemin dépasse 50 cases',()=>{
 for(let g=1;g<=8;g++){const {S,M}=plan(g);const w=new Uint8Array(13*17);M.ord.slice(0,40).forEach(i=>w[i]=1);
  const L=S.plen(w);assert.ok(L>=50,`graine ${g} : chemin de ${L} cases à 40 tours`);assert.equal(M.pre[2],L)}
});
