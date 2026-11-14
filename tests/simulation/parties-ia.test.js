/* Parties complètes entre IA, avec une graine fixe chacune.
   Par défaut : une partie par difficulté (3 parties). Mode complet (WR_COMPLET=1, node tests/tout.js --complet) : les 15 (5 factions × 3 difficultés).
   Chaque partie doit se terminer en moins de 30 min de jeu, sans valeur invalide (NaN), avec un vainqueur cohérent.
   Pas de comparaison à une partie enregistrée : un changement d'équilibrage ou d'IA ne fait pas échouer ces tests. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs');
const {MOTEURS}=require('../outils/moteur');
const {SCENARIOS,COURTS,jouer}=require('../outils/parties');
const liste=process.env.WR_COMPLET=='1'?SCENARIOS:COURTS;

for(const sc of liste){
 test(`Partie entre IA — ${['Humains','Créatures','Végétaux','Robots','Magiques'][sc.faction]}, ${['Normal','Difficile','Brutal'][sc.difficulte]} (graine ${sc.graine})`,()=>{
  const r=jouer(MOTEURS.actuel,sc);
  if(process.env.WR_PARTIES)fs.appendFileSync(process.env.WR_PARTIES,JSON.stringify(r)+'\n'); // pour le bilan gameplay
  assert.equal(r.invalide,false,'valeur invalide (NaN) détectée');
  assert.equal(r.terminee,true,'la partie ne s\'est pas terminée en 30 min de jeu');
  assert.ok(r.gagnant>=-1&&r.gagnant<4,'vainqueur incohérent');
  assert.ok(r.tours.some(n=>n>0),'aucune tour construite');
  assert.ok(r.envois.slice(1).some(n=>n>0),'aucune IA n\'a attaqué');
 });
}

/* 2 minutes de jeu suffisent : l'IA a déjà construit et attaqué */
test('Une même graine rejoue exactement la même partie (2 premières minutes)',()=>{
 const sc=SCENARIOS[0],a=jouer(MOTEURS.actuel,sc,{dureeMax:120}),b=jouer(MOTEURS.actuel,sc,{dureeMax:120});
 assert.deepEqual(a.controles,b.controles);assert.equal(a.final,b.final);
});
