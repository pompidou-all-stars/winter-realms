/* Banc d'essai des tours : mesure ce que chaque tour rapporte réellement par pièce d'or investie.
   Ne modifie pas le jeu : charge sim.js dans un environnement isolé (graine fixe), comme les tests.
   Outil à lancer à la main pour l'équilibrage : il ne fait pas partie de tests/tout.js ni de la vérification GitHub.

   Méthode
   - Un labyrinthe de base toujours identique : trois murs en serpentin (lignes 3, 7 et 11), ouverts à tour de rôle à droite et à gauche.
   - Une seule tour, posée dans le mur du milieu (case 6,7, deux couloirs à portée) puis dans le virage en épingle (case 1,7) ;
     on fait la moyenne des deux emplacements.
   - La tour est montée au niveau voulu (or illimité, chantiers terminés), puis une vague type traverse le terrain.
   - Les monstres sont rendus quasi immortels (PV géants) : on mesure les dégâts infligés pendant toute la traversée, sans que les morts
     ne faussent la mesure. L'armure, la vitesse, le vol, l'anti-magie et les ralentissements de la tour elle-même comptent normalement.
     Limite : la Frénésie de la Horde (cibles sous 35 % de PV) ne se déclenche jamais ici.
   - Résultat : dégâts infligés pour 100 or investis (achat et améliorations). L'indice 100 = la médiane des 50 tours au niveau 1
     dans le même scénario ; l'indice « mixte » est la moyenne des indices des scénarios.
   - Le Givre est surtout une tour de soutien : son ralentissement profite aux autres tours, ce que ce banc (une tour seule) ne compte pas.

   Rapidité : les mesures sont indépendantes et réparties sur plusieurs cœurs (worker_threads). Chaque mesure repart de sa propre graine
   (regrainer), donc le résultat est identique sur 1 cœur ou sur 20. Les mesures les plus longues (la foule) partent en premier.

   Usage : node tests/outils/banc-tours.js [--avant <réf git>] [--moteur <chemin de sim.js>] [--coeurs N] [--niveaux 1,5]
   Écrit aussi rapports/banc-tours.md (détail par faction). */
'use strict';
const fs=require('fs'),path=require('path'),os=require('os'),{execSync}=require('child_process');
const {Worker,isMainThread,parentPort,workerData}=require('worker_threads');
const {charger,RACINE,MOTEURS}=require('./moteur');

const MIN=8*60,M=1+MIN/200;/* monstres de la 8e minute : armure × 3,4 (comme leurs PV) */
/* deux emplacements : au milieu du mur (deux couloirs à portée) et dans le virage en épingle (le chemin fait demi-tour autour de la tour) */
const POSS=[{id:'mur',p:[6,7]},{id:'virage',p:[1,7]}],DT=1/60;/* pas de 1/60 s, comme le navigateur (le serveur multijoueur avance par 0,05 s) */
/* scénarios : nom, clé du monstre, nombre de groupes de 4 (ou 1 monstre seul) */
const SCEN=S=>{const k=n=>S.CR.findIndex(T=>T.n==n);return [
 {id:'sol4',nom:'Groupe au sol (4 Minotaures)',k:k('Minotaure'),g:1},
 {id:'sol1',nom:'Monstre seul (1 Minotaure)',k:k('Minotaure'),seul:1},
 {id:'vague',nom:'Grosse vague (12 Minotaures)',k:k('Minotaure'),g:3},
 {id:'air',nom:'Volants (4 Oculus abyssaux)',k:k('Oculus abyssal'),g:1},
 {id:'blinde',nom:'Blindés (4 Stégosaures, armure 41)',k:k('Stégosaure de guerre'),g:1},
 {id:'antimag',nom:"Anti-magie (4 Taureaux d'airain)",k:k("Taureau d'airain"),g:1},
 {id:'foule',nom:'Foule (40 Minotaures d\'un coup, comme une vague d\'IA)',k:k('Minotaure'),g:10,ensemble:1}]};

function terrain(S,faction,P){
 const b=new S.Board(0,'banc','#fff',0,faction);b.gold=1e9;
 for(let x=0;x<S.C;x++){if(x!=12)b.g[3][x]=1;if(x!=0&&x!=P[0])b.g[7][x]=1;if(x!=12)b.g[11][x]=1}
 b.d=b.dist();return b;
}
function finir(b){for(let i=0;i<4000&&b.t.some(t=>t.b>0);i++)b.update(.05);b.fx.length=0;b.ev.length=0}

function mesurer(S,k,lv,sc,P){
 const b=terrain(S,Math.floor(k/10),P);if(!b.place(P[0],P[1],k))throw new Error('pose impossible : '+S.TW[k].n);finir(b);
 const t=b.t[0];for(let l=1;l<lv;l++){if(!b.upgrade(t))throw new Error('amélioration impossible');finir(b)}
 if(sc.seul)b.q.push({k:sc.k,m:M,t:.1});else for(let g=0;g<sc.g;g++){const n=b.q.length;b.send(sc.k,M);for(let i=n;i<b.q.length;i++)b.q[i].t+=sc.ensemble?0:g*1.5}
 const suivis=[];let temps=0;
 while(temps<240){b.update(DT);temps+=DT;b.fx.length=0;b.ev.length=0;
  for(const c of b.cr)if(!c._banc){c._banc=1;c.hp=c.max=1e9;suivis.push(c)}
  if(!b.q.length&&suivis.length&&suivis.every(c=>c.leak))break}
 const deg=suivis.reduce((s,c)=>s+(1e9-c.hp),0);
 return {deg,inv:t.inv,parOr:deg/t.inv*100};
}

/* une mesure = [version, tour, niveau, scénario, emplacement] ; graine propre à chaque mesure, indépendante de l'ordre */
function faireMesure(S,[,k,lv,si,pi]){S.regrainer(1+k*1000+lv*100+si*10+pi);return mesurer(S,k,lv,SCEN(S)[si],POSS[pi].p)}

/* travailleur : charge les moteurs une fois, puis mesure ce qu'on lui envoie */
if(!isMainThread){
 const moteurs=workerData.codes.map(code=>charger({code}));
 parentPort.on('message',j=>parentPort.postMessage({j,r:faireMesure(moteurs[j[0]],j)}));
}

/* toutes les mesures de toutes les versions, réparties sur « coeurs » fils d'exécution */
function toutMesurer(codes,niveaux,coeurs){
 const S0=charger({code:codes[0]}),nsc=SCEN(S0).length,jobs=[];
 for(let v=0;v<codes.length;v++)for(let k=0;k<S0.TW.length;k++)for(const lv of niveaux)for(let si=0;si<nsc;si++)for(let pi=0;pi<POSS.length;pi++)jobs.push([v,k,lv,si,pi]);
 /* les plus longues d'abord : foule, puis grosse vague, puis niveaux élevés */
 const poids=([,,lv,si])=>(si==nsc-1?100:si==2?10:1)*10+lv;jobs.sort((a,b)=>poids(b)-poids(a));
 const res=new Map(),cle=j=>j.join(','),tot=jobs.length;let fait=0,dernier=0;
 const progres=()=>{fait++;const p=Math.floor(fait/tot*20);if(p>dernier||fait==tot){dernier=p;process.stderr.write(`\r  ${fait} / ${tot} mesures`+(fait==tot?'\n':''))}};
 if(coeurs<=1){const moteurs=codes.map(code=>charger({code}));for(const j of jobs){res.set(cle(j),faireMesure(moteurs[j[0]],j));progres()}return Promise.resolve(res)}
 return new Promise((ok,ko)=>{let i=0,actifs=0;const ws=[];
  const donner=w=>{if(i<jobs.length){w.postMessage(jobs[i++]);actifs++}};
  for(let n=0;n<Math.min(coeurs,jobs.length);n++){const w=new Worker(__filename,{workerData:{codes}});ws.push(w);
   w.on('message',({j,r})=>{res.set(cle(j),r);actifs--;progres();donner(w);if(!actifs&&i>=jobs.length){ws.forEach(x=>x.terminate());ok(res)}});
   w.on('error',e=>{ws.forEach(x=>x.terminate());ko(e)});donner(w)}});
}

/* assemble les mesures d'une version : moyenne des emplacements, référence (médiane des 50 tours au niveau 1), indices */
function assembler(S,res,v,niveaux){
 const sc=SCEN(S),R={};
 for(let k=0;k<S.TW.length;k++)for(const lv of niveaux)sc.forEach((s,si)=>{const m=POSS.map((P,pi)=>res.get([v,k,lv,si,pi].join(',')));
  (R[k]??={})[lv+s.id]={deg:m.reduce((a,r)=>a+r.deg,0)/m.length,inv:m[0].inv,parOr:m.reduce((a,r)=>a+r.parOr,0)/m.length}});
 const med=a=>{a=[...a].sort((x,y)=>x-y);return(a[a.length-1>>1]+a[a.length>>1])/2};
 const ref={};for(const s of sc)ref[s.id]=med(S.TW.map((T,k)=>R[k]['1'+s.id].parOr));
 for(const k in R)for(const lv of niveaux){let m=0;for(const s of sc){const r=R[k][lv+s.id];r.ind=r.parOr/ref[s.id]*100;m+=r.ind}R[k][lv+'mixte']={ind:m/sc.length}}
 return {R,sc,ref,niveaux};
}

const ARCHS=['Archer','Canon','Givre','Mage','Garde','Flammes'];
/* moyenne par archétype (les 5 factions, emplacements 0 à 9 de cet archétype) */
function parArchetype(S,{R,sc,niveaux}){const o={};
 for(const a of ARCHS){const ks=S.TW.map((T,k)=>k).filter(k=>S.BASE_TW[S.TW[k].skin].n==a);o[a]={};
  for(const lv of niveaux)for(const id of [...sc.map(s=>s.id),'mixte'])o[a][lv+id]=ks.reduce((s,k)=>s+R[k][lv+id].ind,0)/ks.length}
 return o;}

const pad=(s,n)=>String(s).padStart(n);
function afficher(S,res,avant){
 const A=parArchetype(S,res),B=avant&&parArchetype(avant.S,avant.res),cols=[...res.sc.map(s=>s.id),'mixte'];
 const l=[];l.push('Indice de rendement par or investi (100 = médiane des tours au niveau 1 dans ce scénario)'+(B?' — avant → après':''));
 l.push('Archétype  Niv '+cols.map(c=>pad(c,B?13:8)).join(''));
 for(const a of ARCHS){for(const lv of res.niveaux)l.push(a.padEnd(10)+pad(lv,4)+' '+cols.map(c=>{const v=Math.round(A[a][lv+c]);return B?pad(Math.round(B[a][lv+c])+'→'+v,13):pad(v,8)}).join(''));l.push('')}
 return l.join('\n');
}
function rapport(S,res,avant){
 const {R,sc,ref,niveaux}=res,l=['# Banc d\'essai des tours','',`Généré par \`node tests/outils/banc-tours.js\`. Monstres de la ${MIN/60}e minute (armure ×${M.toFixed(1)}), une tour seule dans un labyrinthe en serpentin, moyenne de deux emplacements (${POSS.map(P=>P.id+' '+P.p).join(', ')}), pas de temps 1/60 s.`,'',
  '## Scénarios et référence (dégâts pour 100 or, médiane des tours niveau 1)','',...sc.map(s=>`- **${s.id}** : ${s.nom} — référence ${Math.round(ref[s.id])}`),'',
  '## Par archétype (moyenne des factions)','','```',afficher(S,res,avant),'```','',`## Détail par tour (indice mixte par niveau)`,''];
 const dern=niveaux[niveaux.length-1];
 for(let f=0;f<S.FACTIONS.length;f++){l.push(`### ${S.FACTIONS[f].name}`,'',`| # | Tour | Type | Coût | ${niveaux.map(n=>'Niv '+n).join(' | ')} | Or total niv ${dern} |`,'|---|---|---|---|'+niveaux.map(()=>'---|').join('')+'---|');
  for(let j=0;j<10;j++){const k=f*10+j,T=S.TW[k];l.push(`| ${j} | ${T.n} | ${S.BASE_TW[T.skin].n} | ${T.c} | `+niveaux.map(lv=>Math.round(R[k][lv+'mixte'].ind)).join(' | ')+` | ${R[k][dern+'sol4'].inv} |`)}l.push('')}
 return l.join('\n');
}

if(isMainThread&&require.main===module)(async()=>{
 const arg=n=>{const i=process.argv.indexOf(n);return i>0?process.argv[i+1]:null};
 const t0=Date.now(),ref=arg('--avant');
 const niveaux=[...new Set([1,...(arg('--niveaux')||'1,2,3,4,5').split(',').map(Number).filter(n=>n>=1&&n<=5)])].sort();
 const coeurs=Math.max(1,+(arg('--coeurs')||Math.max(1,os.cpus().length-1)));
 const codes=[fs.readFileSync(arg('--moteur')?path.resolve(arg('--moteur')):MOTEURS.actuel,'utf8')];
 if(ref)codes.push(execSync(`git show ${ref}:sim.js`,{cwd:RACINE,encoding:'utf8',maxBuffer:1<<26}));
 console.error(`Banc d'essai : ${codes.length} version(s), niveaux ${niveaux.join(', ')}, ${coeurs} cœur(s)`);
 const mes=await toutMesurer(codes,niveaux,coeurs);
 const S=charger({code:codes[0]}),res=assembler(S,mes,0,niveaux);
 const avant=ref?(SA=>({S:SA,res:assembler(SA,mes,1,niveaux)}))(charger({code:codes[1]})):null;
 console.log(afficher(S,res,avant));
 const dos=path.join(RACINE,'rapports');fs.mkdirSync(dos,{recursive:true});fs.writeFileSync(path.join(dos,'banc-tours.md'),rapport(S,res,avant));
 console.log(`Détail : rapports/banc-tours.md (${((Date.now()-t0)/1000).toFixed(1)} s)`);
})().catch(e=>{console.error(e);process.exit(1)});
module.exports={mesurer,toutMesurer,assembler,parArchetype};
