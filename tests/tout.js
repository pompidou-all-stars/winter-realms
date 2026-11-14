/* Lance les tests du projet, avec un affichage en français.
   node tests/tout.js               → simulation (mécaniques + 1 partie entre IA par difficulté) et navigateur
   node tests/tout.js --simulation  → simulation seulement (c'est ce que lance GitHub à chaque Pull Request)
   node tests/tout.js --complet     → ajoute les 15 parties entre IA complètes (5 factions × 3 difficultés), plusieurs minutes
   (--rapide est gardé comme synonyme de --simulation)
   Code de sortie : 0 si tout passe, 1 sinon. */
'use strict';
const {spawnSync}=require('child_process'),path=require('path'),fs=require('fs');
const ici=__dirname,args=process.argv.slice(2);
const complet=args.includes('--complet'),simulation=args.includes('--rapide')||args.includes('--simulation');
const fichiers=d=>fs.readdirSync(path.join(ici,d)).filter(f=>f.endsWith('.test.js')).sort().map(f=>path.join(ici,d,f));
const liste=[...fichiers('simulation'),...(simulation?[]:fichiers('navigateur'))];
console.log(`Tests Winter Realms — ${simulation?'simulation':'simulation + navigateur'}${complet?' (15 parties complètes)':''}\n`);
/* le rapporteur est passé sous forme d'URL file:// : sous Windows, un chemin « C:\… » est refusé par Node */
const rapporteur=require('url').pathToFileURL(path.join(ici,'outils','rapporteur.mjs')).href;
const r=spawnSync(process.execPath,['--test','--test-concurrency=1',`--test-reporter=${rapporteur}`,...liste],
 {stdio:'inherit',env:{...process.env,...(complet?{WR_COMPLET:'1'}:{})}});
process.exit(r.status===0?0:1);
