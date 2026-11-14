/* Parties complètes entre IA (5 factions × 3 difficultés), rejouées avec une graine fixe.
   Chaque partie doit se dérouler EXACTEMENT comme la référence 2.4 : mêmes états toutes les 30 s de jeu, même fin.
   Mode rapide (WR_RAPIDE=1) : seulement les 5 parties en difficulté Normal. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {RACINE,MOTEURS}=require('../outils/moteur');
const {SCENARIOS,jouer}=require('../outils/parties');
const REF=JSON.parse(fs.readFileSync(path.join(RACINE,'tests','references','parties-v2.4.json'),'utf8'));
const rapide=process.env.WR_RAPIDE=='1';

for(const sc of SCENARIOS){if(rapide&&sc.difficulte>0)continue;
 test(`Partie de référence — ${['Alliance','Horde','Sylvestres','Nains','Légion'][sc.faction]}, ${['Normal','Difficile','Brutal'][sc.difficulte]} (graine ${sc.graine})`,()=>{
  const r=jouer(MOTEURS.actuel,sc),ref=REF.parties.find(p=>p.graine==sc.graine);
  if(process.env.WR_PARTIES)fs.appendFileSync(process.env.WR_PARTIES,JSON.stringify(r)+'\n'); // pour le bilan gameplay
  assert.ok(ref,'référence introuvable');
  assert.equal(r.invalide,false,'valeur invalide (NaN) détectée');
  assert.equal(r.terminee,true,'la partie ne s\'est pas terminée en 30 min de jeu');
  const i=r.controles.findIndex((c,j)=>c!==ref.controles[j]);
  if(i>=0)assert.fail(`la partie diverge de la référence vers ${(i+1)*30} s de jeu`);
  assert.deepEqual({duree:r.duree,gagnant:r.gagnant,vies:r.vies,revenus:r.revenus,tours:r.tours,envois:r.envois,final:r.final},
   {duree:ref.duree,gagnant:ref.gagnant,vies:ref.vies,revenus:ref.revenus,tours:ref.tours,envois:ref.envois,final:ref.final});
 });
}
