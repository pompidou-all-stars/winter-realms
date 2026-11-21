/* Arène des IA : fait s'affronter l'IA actuelle et celle d'une autre version (par défaut origin/main), dans le même moteur de jeu.
   Ne modifie pas le jeu : charge sim.js dans un environnement isolé (graine fixe), comme les tests.
   Outil à lancer à la main après un changement d'IA : il ne fait pas partie de tests/tout.js ni de la vérification GitHub.

   Méthode
   - Le moteur (terrains, monstres, tours) est celui de la version actuelle. La section « IA » de l'autre version (entre les lignes
     « ---------- IA ---------- » et « ---------- partie ---------- » de son sim.js) est chargée à côté, dans sa propre portée :
     chaque terrain est joué par l'une ou l'autre IA. Limite : l'IA d'avant doit rester compatible avec le moteur actuel.
   - 4 terrains, 2 joués par chaque IA, sièges alternés (N A N A), puis la même partie (même graine, mêmes factions) avec les sièges
     échangés (A N A N) : chaque IA joue chaque faction à chaque place.
   - Les 4 sièges sont « humains » pour le moteur (ni bonus de difficulté, ni fin de partie quand les humains sont éliminés), mais tous
     joués par une IA, comme le siège 0 des parties de test. La difficulté choisie règle seulement le labyrinthe (recherche, choix du plan).
   - Classement : le dernier debout gagne ; les autres sont classés par moment d'élimination ; au bout de 30 min, ceux encore en jeu
     sont départagés par leurs vies. Points : 3, 2, 1, 0 du 1er au 4e (1,5 en moyenne si les deux IA se valent).

   --vies V : vies de départ de chaque terrain (40 par défaut) ; avec beaucoup de vies, les parties durent et la fin de partie compte davantage.
   Usage : node tests/outils/arene-ia.js [--avant <réf git>] [--parties N] [--difficulte 0|1|2] [--coeurs N] [--graine G] [--vies V]
   (N : nombre de graines ; chaque graine donne 2 parties, sièges échangés.) */
'use strict';
const fs=require('fs'),path=require('path'),os=require('os'),{execSync}=require('child_process');
const {Worker,isMainThread,parentPort,workerData}=require('worker_threads');
const {charger,MOTEURS,RACINE}=require('./moteur');

/* moteur actuel + IA d'une autre version, dans sa propre portée ; renvoie les deux fonctions aiAct */
function composer(actuel,avant){
 const a=avant.indexOf('/* ---------- IA ---------- */'),b=avant.indexOf('/* ---------- partie ---------- */');
 if(a<0||b<0)throw new Error('section IA introuvable dans la version d\'avant');
 return actuel+`\n;module.exports.__IA=[aiAct,(function(){\n${avant.slice(a,b)}\n;return aiAct})()];`;
}

const DT=.05,DUREE_MAX=1800;
/* une partie : versions[i] = 0 (actuelle) ou 1 (avant) pour le siège i */
function jouer(S,graine,versions,difficulte,vies=40){
 S.regrainer(graine);const f0=graine%5;
 const G=new S.Game([0,1,2,3].map(i=>({name:'S'+i,col:'#fff',ai:0,classId:(f0+i)%5})),difficulte);
 for(const b of G.B)b.lives=vies;const aiT=[1,1.2,1.4,1.6];
 while(!G.over&&G.time<DUREE_MAX){
  for(const b of G.B)if(!b.dead){aiT[b.i]-=DT;if(aiT[b.i]<=0){aiT[b.i]=.6;b.ai=1;S.__IA[versions[b.i]](b);b.ai=0}}
  G.step(DT)}
 /* classement : vivants d'abord (par vies), puis éliminés du plus tard au plus tôt */
 const ord=[...G.B].sort((x,y)=>(x.dead-y.dead)||(x.dead?y.st.mort-x.st.mort:y.lives-x.lives));
 return G.B.map(b=>({v:versions[b.i],f:b.classId,rang:ord.indexOf(b),mort:b.dead?b.st.mort:null,tours:b.t.length,inc:b.inc,
  envOr:b.st.envOr,tue:b.st.tue}));
}

if(!isMainThread){
 const S=charger({code:workerData.code});
 parentPort.on('message',j=>parentPort.postMessage({j,r:jouer(S,j.g,j.v,workerData.difficulte,workerData.vies)}));
}

function toutJouer(code,jobs,coeurs,difficulte,vies){
 const res=[];let fait=0;const progres=()=>{fait++;process.stderr.write(`\r  ${fait} / ${jobs.length} parties`+(fait==jobs.length?'\n':''))};
 if(coeurs<=1){const S=charger({code});for(const j of jobs){res.push({j,r:jouer(S,j.g,j.v,difficulte,vies)});progres()}return Promise.resolve(res)}
 return new Promise((ok,ko)=>{let i=0,actifs=0;const ws=[];
  const donner=w=>{if(i<jobs.length){w.postMessage(jobs[i++]);actifs++}};
  for(let n=0;n<Math.min(coeurs,jobs.length);n++){const w=new Worker(__filename,{workerData:{code,difficulte,vies}});ws.push(w);
   w.on('message',m=>{res.push(m);actifs--;progres();donner(w);if(!actifs&&i>=jobs.length){ws.forEach(x=>x.terminate());ok(res)}});
   w.on('error',e=>{ws.forEach(x=>x.terminate());ko(e)});donner(w)}});
}

const FN=['Alliance','Horde','Sylvestres','Nains','Légion'];
function bilan(res){
 const s=[0,1].map(()=>({pts:0,n:0,vic:0,parties:0,tours:0,inc:0,envOr:0,f:FN.map(()=>({pts:0,n:0}))}));
 for(const {r} of res)for(const x of r){const o=s[x.v],p=3-x.rang;o.pts+=p;o.n++;if(x.rang==0)o.vic++;o.tours+=x.tours;o.inc+=x.inc;o.envOr+=x.envOr;o.f[x.f].pts+=p;o.f[x.f].n++}
 /* écart par paire de parties (sièges échangés) : moyenne et erreur type, pour juger si l'écart est réel */
 const par=new Map();for(const {j,r} of res){const d=r.reduce((a,x)=>a+(x.v?-1:1)*(3-x.rang),0)/2;par.set(j.g,(par.get(j.g)||0)+d/2)}
 const ds=[...par.values()],m=ds.reduce((a,b)=>a+b,0)/ds.length,sd=Math.sqrt(ds.reduce((a,b)=>a+(b-m)**2,0)/Math.max(1,ds.length-1)),se=sd/Math.sqrt(ds.length);
 const l=[];const nom=['IA actuelle','IA d\'avant'];
 l.push(`${res.length} parties (${ds.length} graines × 2, sièges échangés)`);
 for(const v of [0,1]){const o=s[v];l.push(`${nom[v].padEnd(12)} points ${(o.pts/o.n).toFixed(2)} (1,50 = égalité) · victoires ${o.vic}/${res.length} · tours finales ${(o.tours/o.n).toFixed(0)} · revenu final ${(o.inc/o.n).toFixed(0)} · or envoyé ${(o.envOr/o.n).toFixed(0)}`)}
 l.push(`Écart de points par siège (actuelle − avant) : ${m>=0?'+':''}${m.toFixed(2)} ± ${se.toFixed(2)} (erreur type)`);
 l.push('Points par faction (actuelle / avant) : '+FN.map((n,f)=>`${n} ${(s[0].f[f].pts/Math.max(1,s[0].f[f].n)).toFixed(2)}/${(s[1].f[f].pts/Math.max(1,s[1].f[f].n)).toFixed(2)}`).join(' · '));
 return l.join('\n');
}

if(isMainThread&&require.main===module)(async()=>{
 const arg=n=>{const i=process.argv.indexOf(n);return i>0?process.argv[i+1]:null};
 const t0=Date.now(),ref=arg('--avant')||'origin/main',np=+(arg('--parties')||20),diff=+(arg('--difficulte')||0),g0=+(arg('--graine')||1),vies=+(arg('--vies')||40);
 const coeurs=Math.max(1,+(arg('--coeurs')||Math.max(1,os.cpus().length-1)));
 const actuel=fs.readFileSync(arg('--moteur')?path.resolve(arg('--moteur')):MOTEURS.actuel,'utf8');
 const avant=execSync(`git show ${ref}:sim.js`,{cwd:RACINE,encoding:'utf8',maxBuffer:1<<26});
 const code=composer(actuel,avant),jobs=[];
 for(let g=g0;g<g0+np;g++){jobs.push({g,v:[0,1,0,1]});jobs.push({g,v:[1,0,1,0]})}
 console.error(`Arène : IA actuelle contre ${ref}, ${jobs.length} parties, ${['Normal','Difficile','Brutal'][diff]}, ${coeurs} cœur(s)${vies!=40?', '+vies+' vies':''}`);
 const res=await toutJouer(code,jobs,coeurs,diff,vies);
 console.log(bilan(res));console.log(`(${((Date.now()-t0)/1000).toFixed(0)} s)`);
})().catch(e=>{console.error(e);process.exit(1)});
module.exports={composer,jouer,bilan};
