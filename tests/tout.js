/* Lance les tests du projet, avec un affichage en français.
   node tests/tout.js               → simulation (mécaniques + 1 partie entre IA par difficulté) et navigateur
   node tests/tout.js --simulation  → simulation seulement (c'est ce que lance GitHub à chaque Pull Request)
   node tests/tout.js --complet     → ajoute les 15 parties entre IA complètes (5 factions × 3 difficultés)
   node tests/tout.js --un-par-un   → un fichier de test après l'autre (fonctionnement d'avant la 2.34)
   (--rapide est gardé comme synonyme de --simulation)
   2.34 : les fichiers de test tournent en parallèle (un processus par fichier, autant que de cœurs moins un),
   les plus longs en premier ; les parties entre IA sont elles aussi jouées en parallèle (tests/outils/parties.js).
   Code de sortie : 0 si tout passe, 1 sinon. */
'use strict';
const {spawnSync}=require('child_process'),path=require('path'),fs=require('fs'),os=require('os');
const ici=__dirname,args=process.argv.slice(2);
const complet=args.includes('--complet'),simulation=args.includes('--rapide')||args.includes('--simulation');
const fichiers=d=>fs.readdirSync(path.join(ici,d)).filter(f=>f.endsWith('.test.js')).sort().map(f=>path.join(ici,d,f));
/* les plus longs d'abord, pour qu'ils ne restent pas seuls à la fin */
const LONGS=['parcours.test.js','parties-ia.test.js','labyrinthe-partie.test.js','labyrinthe.test.js'],rang=f=>{const i=LONGS.indexOf(path.basename(f));return i<0?LONGS.length:i};
const liste=[...fichiers('simulation'),...(simulation?[]:fichiers('navigateur'))].sort((a,b)=>rang(a)-rang(b));
const coeurs=os.availableParallelism?os.availableParallelism():os.cpus().length,paralleles=args.includes('--un-par-un')?1:Math.max(1,coeurs-1);
console.log(`Tests Winter Realms — ${simulation?'simulation':'simulation + navigateur'}${complet?' (15 parties complètes)':''} · ${paralleles} fichier(s) à la fois\n`);
/* le rapporteur est passé sous forme d'URL file:// : sous Windows, un chemin « C:\… » est refusé par Node */
const rapporteur=require('url').pathToFileURL(path.join(ici,'outils','rapporteur.mjs')).href;
const r=spawnSync(process.execPath,['--test',`--test-concurrency=${paralleles}`,`--test-reporter=${rapporteur}`,...liste],
 {stdio:'inherit',env:{...process.env,...(complet?{WR_COMPLET:'1'}:{})}});
process.exit(r.status===0?0:1);
