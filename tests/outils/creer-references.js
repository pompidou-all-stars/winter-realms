/* Crée les fichiers de référence à partir d'un moteur FIGÉ (jamais à partir de main).
   Usage : node tests/outils/creer-references.js v1.7
   Refuse d'écraser une référence existante : les références ne se régénèrent pas
   (voir CLAUDE.md, « Tests et validation »). */
'use strict';
const fs=require('fs'),path=require('path');
const {charger,sha256,RACINE}=require('./moteur');
const {SCENARIOS,jouer}=require('./parties');

const version=process.argv[2];
if(!version){console.error('Indique la version du moteur figé, par exemple : v1.7');process.exit(1)}
const fichierMoteur=path.join(RACINE,'tests','moteurs',version,'sim.js');
if(!fs.existsSync(fichierMoteur)){console.error('Moteur figé introuvable : '+fichierMoteur);process.exit(1)}
const dossier=path.join(RACINE,'tests','references');
const sorties={stats:path.join(dossier,`statistiques-${version}.json`),parties:path.join(dossier,`parties-${version}.json`)};
for(const f of Object.values(sorties))if(fs.existsSync(f)){console.error('Référence déjà présente, rien n\'est écrasé : '+path.relative(RACINE,f));process.exit(1)}

const S=charger(fichierMoteur),moteur={version,sha256:sha256(fichierMoteur)};
const clone=o=>JSON.parse(JSON.stringify(o));
const stats={moteur,
 constantes:{C:S.C,R:S.R,SP:S.SP,EX:S.EX,HPK:S.HPK,GRACE:S.GRACE,GROUP:S.GROUP,AURA_R:S.AURA_R},
 BASE_TW:clone(S.BASE_TW),FACTION_BALANCE:clone(S.FACTION_BALANCE),ARCH:clone(S.ARCH),ROLE:clone(S.ROLE),DIFF:clone(S.DIFF),
 tours:S.TW.map((T,k)=>({k,...clone(T),
  niveaux:[1,2,3,4,5].map(lv=>({lv,degats:S.dmg({k,lv}),portee:S.rng({k,lv}),coutPourPasserAuSuivant:lv<5?S.upCost({k,lv}):null}))})),
 monstres:S.CR.map((T,k)=>({k,...clone(T)}))};
fs.mkdirSync(dossier,{recursive:true});
fs.writeFileSync(sorties.stats,JSON.stringify(stats,null,1)+'\n');
console.log('Écrit : '+path.relative(RACINE,sorties.stats));

const parties={moteur,pas:.05,parties:[]};
for(const sc of SCENARIOS){const r=jouer(fichierMoteur,sc);parties.parties.push(r);console.log(`  ${sc.nom} : ${(r.duree/60).toFixed(1)} min, gagnant ${r.gagnant}`)}
fs.writeFileSync(sorties.parties,JSON.stringify(parties,null,1)+'\n');
console.log('Écrit : '+path.relative(RACINE,sorties.parties));
