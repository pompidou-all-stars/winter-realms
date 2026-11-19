/* Parties complètes entre IA, avec une graine fixe chacune.
   Par défaut : une partie par difficulté (3 parties). Mode complet (WR_COMPLET=1, node tests/tout.js --complet) : les 15 (5 factions × 3 difficultés).
   Chaque partie doit se terminer en moins de 30 min de jeu, sans valeur invalide (NaN), avec un vainqueur cohérent.
   Pas de comparaison à une partie enregistrée : un changement d'équilibrage ou d'IA ne fait pas échouer ces tests.
   2.34 : toutes les parties sont lancées dès le chargement, en parallèle (une par cœur, jouerEnParallele) ; chaque test attend la sienne. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs');
const {MOTEURS}=require('../outils/moteur');
const {SCENARIOS,COURTS,jouerEnParallele}=require('../outils/parties');
const liste=process.env.WR_COMPLET=='1'?SCENARIOS:COURTS;
/* 2 minutes de jeu suffisent pour la reproductibilité : l'IA a déjà construit et attaqué */
const deux={dureeMax:120},R=jouerEnParallele(MOTEURS.actuel,[...liste.map(sc=>({sc})),{sc:SCENARIOS[0],opts:deux},{sc:SCENARIOS[0],opts:deux}]);

liste.forEach((sc,i)=>{
 test(`Partie entre IA — ${['Alliance','Horde','Sylvestres','Nains','Légion'][sc.faction]}, ${['Normal','Difficile','Brutal'][sc.difficulte]} (graine ${sc.graine})`,async()=>{
  const r=await R[i];
  if(process.env.WR_PARTIES)fs.appendFileSync(process.env.WR_PARTIES,JSON.stringify(r)+'\n'); // pour le bilan gameplay
  assert.equal(r.invalide,false,'valeur invalide (NaN) détectée');
  assert.equal(r.terminee,true,'la partie ne s\'est pas terminée en 30 min de jeu');
  assert.ok(r.gagnant>=-1&&r.gagnant<4,'vainqueur incohérent');
  assert.ok(r.tours.some(n=>n>0),'aucune tour construite');
  assert.ok(r.envois.slice(1).some(n=>n>0),'aucune IA n\'a attaqué');
 });
});

test('Une même graine rejoue exactement la même partie (2 premières minutes)',async()=>{
 const [a,b]=await Promise.all(R.slice(-2));
 assert.deepEqual(a.controles,b.controles);assert.equal(a.final,b.final);
});
