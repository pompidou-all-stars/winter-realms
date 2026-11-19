/* Durée de la génération du labyrinthe de l'IA (sorti de labyrinthe.test.js en 2.36).
   C'est une mesure de temps réel : tests/tout.js lance ce fichier seul, après les autres (liste SEULS),
   pour que les tests qui tournent en parallèle ne faussent pas la mesure. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie}=require('../outils/moteur');

/* La découpe est vérifiée de façon certaine (nombre de tranches), la durée seulement comme garde-fou :
   les machines de GitHub sont plus ou moins chargées, d'où la meilleure de 3 mesures et une marge (révision de la 2.11). */
test('La génération est découpée en plusieurs tranches courtes (moins de 10 ms par tranche, moins de 150 ms au total ; 150 depuis la 2.25, chemin en 8 directions)',()=>{
 let meilleurMax=Infinity,meilleurTot=Infinity,tranches=0;
 for(let essai=0;essai<3;essai++){
  const S=charger('actuel',{graine:4});const G=partie(S,{ia:[0,1,1,1],difficulte:2});const b=G.B[1];let tot=0,max=0,M=null,n=0;
  S.mzStep(G.B[2],Infinity);/* échauffement du moteur JavaScript */
  while(!M){const t=process.hrtime.bigint();M=S.mzStep(b,600);const d=Number(process.hrtime.bigint()-t)/1e6;tot+=d;max=Math.max(max,d);n++}
  tranches=n;meilleurMax=Math.min(meilleurMax,max);meilleurTot=Math.min(meilleurTot,tot)}
 assert.ok(tranches>=3,`génération faite en ${tranches} tranche(s) seulement : elle n'est plus découpée`);
 assert.ok(meilleurMax<10,`tranche de ${meilleurMax.toFixed(1)} ms`);assert.ok(meilleurTot<150,`total ${meilleurTot.toFixed(1)} ms`);
});

