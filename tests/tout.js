/* Lance les tests du projet, avec un affichage en français.
   node tests/tout.js               → tout : simulation (mécaniques + 15 parties) et navigateur (≈ 1 min)
   node tests/tout.js --simulation  → simulation seulement (c'est ce que lance GitHub à chaque Pull Request)
   node tests/tout.js --rapide      → simulation, avec 5 parties au lieu de 15 (≈ 15 s)
   Code de sortie : 0 si tout passe, 1 sinon. */
'use strict';
const {spawnSync}=require('child_process'),path=require('path'),fs=require('fs');
const ici=__dirname,args=process.argv.slice(2);
const rapide=args.includes('--rapide'),simulation=rapide||args.includes('--simulation');
const fichiers=d=>fs.readdirSync(path.join(ici,d)).filter(f=>f.endsWith('.test.js')).sort().map(f=>path.join(ici,d,f));
const liste=[...fichiers('simulation'),...(simulation?[]:fichiers('navigateur'))];
console.log(`Tests Winter Realms — ${simulation?'simulation'+(rapide?' (mode rapide)':''):'simulation + navigateur'}\n`);
const r=spawnSync(process.execPath,['--test','--test-concurrency=1',`--test-reporter=${path.join(ici,'outils','rapporteur.mjs')}`,...liste],
 {stdio:'inherit',env:{...process.env,...(rapide?{WR_RAPIDE:'1'}:{})}});
process.exit(r.status===0?0:1);
