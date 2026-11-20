/* Banc des races (2.40) : les 5 races s'affrontent, jouées par la même IA, pour vérifier qu'aucune ne domine ni ne s'effondre.
   Ne modifie pas le jeu : charge sim.js dans un environnement isolé (graine fixe), comme les tests.
   Outil à lancer à la main après un changement d'équilibrage des races : il ne fait pas partie de tests/tout.js ni de la vérification GitHub.

   Méthode
   - 4 terrains, tous « humains » pour le moteur (pas de bonus de difficulté) mais joués par l'IA ; chaque partie met 4 races différentes,
     et une graine donne 5 parties (chaque race est absente une fois, les places tournent).
   - Classement : le dernier debout gagne ; les autres sont classés par moment d'élimination ; au bout de 30 min, ceux encore en jeu
     sont départagés par leurs vies. Points : 3, 2, 1, 0 du 1er au 4e (1,5 en moyenne si les races se valent).
   - Critère (CLAUDE.md §5.3, règle 5) : chaque race doit rester entre 1,2 et 1,8 point en moyenne.
   Usage : node tests/outils/banc-races.js [--parties N] [--coeurs N] [--graine G]
   WR_MODIF="<code>" : code exécuté sur le moteur chargé (S) avant chaque partie, pour essayer un réglage sans toucher à sim.js
   (exemple : WR_MODIF="S.TW[20].pv=.3"). */
'use strict';
const os=require('os'),{Worker,isMainThread,parentPort,workerData}=require('worker_threads');
const {charger}=require('./moteur');
const DT=.05,DUREE=1800;
const MODIF=process.env.WR_MODIF||'';
function jouer(graine,races){const S=charger('actuel',{graine});if(MODIF)new Function('S',MODIF)(S);
 const G=new S.Game(races.map((f,i)=>({name:'J'+i,col:'#fff',ai:0,classId:f})),0);const aiT=G.B.map((b,i)=>.6+i*.2);
 while(!G.over&&G.time<DUREE){for(const b of G.B)if(!b.dead){aiT[b.i]-=DT;if(aiT[b.i]<=0){aiT[b.i]=.6;b.ai=1;S.aiAct(b);b.ai=0}}G.step(DT)}
 const ordre=[...G.B].sort((a,b)=>(a.dead?a.st.mort:DUREE+a.lives)-(b.dead?b.st.mort:DUREE+b.lives)).reverse();
 return {graine,races,duree:Math.round(G.time),pts:ordre.map((b,r)=>[b.classId,3-r]),tours:G.B.map(b=>[b.classId,b.t.length])}}
if(!isMainThread){parentPort.postMessage(workerData.map(([g,r])=>jouer(g,r)));return}
const arg=(n,d)=>{const i=process.argv.indexOf(n);return i>0?Number(process.argv[i+1]):d};
const N=arg('--parties',4),G0=arg('--graine',1),CO=arg('--coeurs',Math.max(1,os.cpus().length-1));
const travaux=[];for(let g=0;g<N;g++)for(let x=0;x<5;x++){const r=[0,1,2,3,4].filter(f=>f!=x);for(let k=0;k<g%4;k++)r.push(r.shift());travaux.push([G0+g*5+x,r])}
const lots=Array.from({length:Math.min(CO,travaux.length)},()=>[]);travaux.forEach((t,i)=>lots[i%lots.length].push(t));
const t0=Date.now();Promise.all(lots.map(l=>new Promise((ok,ko)=>{const w=new Worker(__filename,{workerData:l});w.on('message',ok);w.on('error',ko)}))).then(R=>{R=R.flat();
 const {RACES}=charger('actuel');const pts=[0,0,0,0,0],n=[0,0,0,0,0],vic=[0,0,0,0,0];
 for(const r of R)for(const[f,p]of r.pts){pts[f]+=p;n[f]++;if(p==3)vic[f]++}
 console.log(`Banc des races : ${R.length} parties, durée moyenne ${Math.round(R.reduce((s,r)=>s+r.duree,0)/R.length)} s (${Math.round((Date.now()-t0)/1000)} s de calcul)`);
 for(let f=0;f<5;f++){const m=pts[f]/n[f],ok=m>=1.2&&m<=1.8;console.log(`${ok?'✅':'⚠️ '} ${RACES[f].name.padEnd(26)} ${m.toFixed(2)} point par partie · ${vic[f]} victoires sur ${n[f]}`)}});
