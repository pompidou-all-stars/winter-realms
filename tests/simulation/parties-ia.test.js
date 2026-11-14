/* Parties complètes entre IA (5 factions × 3 difficultés), avec une graine fixe chacune.
   Chaque partie doit se terminer en moins de 30 min de jeu, sans valeur invalide (NaN), avec un vainqueur cohérent.
   Pas de comparaison à une partie enregistrée : un changement d'équilibrage ou d'IA ne fait pas échouer ces tests.
   Mode rapide (WR_RAPIDE=1) : seulement les 5 parties en difficulté Normal. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs');
const {MOTEURS}=require('../outils/moteur');
const {SCENARIOS,jouer}=require('../outils/parties');
const rapide=process.env.WR_RAPIDE=='1';

for(const sc of SCENARIOS){if(rapide&&sc.difficulte>0)continue;
 test(`Partie entre IA — ${['Alliance','Horde','Sylvestres','Nains','Légion'][sc.faction]}, ${['Normal','Difficile','Brutal'][sc.difficulte]} (graine ${sc.graine})`,()=>{
  const r=jouer(MOTEURS.actuel,sc);
  if(process.env.WR_PARTIES)fs.appendFileSync(process.env.WR_PARTIES,JSON.stringify(r)+'\n'); // pour le bilan gameplay
  assert.equal(r.invalide,false,'valeur invalide (NaN) détectée');
  assert.equal(r.terminee,true,'la partie ne s\'est pas terminée en 30 min de jeu');
  assert.ok(r.gagnant>=-1&&r.gagnant<4,'vainqueur incohérent');
  assert.ok(r.tours.some(n=>n>0),'aucune tour construite');
  assert.ok(r.envois.slice(1).some(n=>n>0),'aucune IA n\'a attaqué');
 });
}

test('Une même graine rejoue exactement la même partie',()=>{
 const sc=SCENARIOS[0],a=jouer(MOTEURS.actuel,sc),b=jouer(MOTEURS.actuel,sc);
 assert.deepEqual(a.controles,b.controles);assert.equal(a.final,b.final);
});
