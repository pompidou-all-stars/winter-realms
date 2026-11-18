/* Banc d'essai des tours : mesure ce que chaque tour rapporte réellement par pièce d'or investie.
   Ne modifie pas le jeu : charge sim.js dans un environnement isolé (graine fixe), comme les tests.

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

   Usage : node tests/outils/banc-tours.js [--avant <réf git>] [--moteur <chemin de sim.js>]
   Écrit aussi rapports/banc-tours.md (détail par faction). */
'use strict';
const fs=require('fs'),path=require('path'),{execSync}=require('child_process');
const {charger,RACINE}=require('./moteur');

const MIN=8*60,M=1+MIN/200;/* monstres de la 8e minute : armure × 3,4 (comme leurs PV) */
/* deux emplacements : au milieu du mur (deux couloirs à portée) et dans le virage en épingle (le chemin fait demi-tour autour de la tour) */
const POSS=[{id:'mur',p:[6,7]},{id:'virage',p:[1,7]}],DT=1/60;/* pas de 1/60 s, comme le navigateur (le serveur multijoueur avance par 0,05 s) */
/* scénarios : nom, clé du monstre, nombre de groupes de 4 (ou 1 monstre seul) */
const SCEN=S=>{const k=n=>S.CR.findIndex(T=>T.n==n);return [
 {id:'sol4',nom:'Groupe au sol (4 Ogres)',k:k('Ogre'),g:1},
 {id:'sol1',nom:'Monstre seul (1 Ogre)',k:k('Ogre'),seul:1},
 {id:'vague',nom:'Grosse vague (12 Ogres)',k:k('Ogre'),g:3},
 {id:'air',nom:'Volants (4 Vouivres)',k:k('Vouivre'),g:1},
 {id:'blinde',nom:'Blindés (4 Scarabées, armure 41)',k:k('Scarabée cuirassé'),g:1},
 {id:'antimag',nom:'Anti-magie (4 Inquisiteurs)',k:k('Inquisiteur'),g:1},
 {id:'foule',nom:'Foule (40 Ogres d\'un coup, comme une vague d\'IA)',k:k('Ogre'),g:10,ensemble:1}]};

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

function banc(S){
 const sc=SCEN(S),R={};
 for(let k=0;k<S.TW.length;k++)for(let lv=1;lv<=5;lv++)for(const s of sc){const m=POSS.map(P=>mesurer(S,k,lv,s,P.p));
  (R[k]??={})[lv+s.id]={deg:m.reduce((a,r)=>a+r.deg,0)/m.length,inv:m[0].inv,parOr:m.reduce((a,r)=>a+r.parOr,0)/m.length}}
 /* référence : médiane des 50 tours au niveau 1 */
 const med=a=>{a=[...a].sort((x,y)=>x-y);return(a[a.length-1>>1]+a[a.length>>1])/2};
 const ref={};for(const s of sc)ref[s.id]=med(S.TW.map((T,k)=>R[k]['1'+s.id].parOr));
 for(const k in R)for(let lv=1;lv<=5;lv++){let m=0;for(const s of sc){const r=R[k][lv+s.id];r.ind=r.parOr/ref[s.id]*100;m+=r.ind}R[k][lv+'mixte']={ind:m/sc.length}}
 return {R,sc,ref};
}

const ARCHS=['Archer','Canon','Givre','Mage','Garde','Flammes'];
/* moyenne par archétype (les 5 factions, emplacements 0 à 9 de cet archétype) */
function parArchetype(S,{R,sc}){const o={};
 for(const a of ARCHS){const ks=S.TW.map((T,k)=>k).filter(k=>S.TW[k].n&&S.BASE_TW[S.TW[k].skin].n==a);o[a]={};
  for(let lv=1;lv<=5;lv++)for(const id of [...sc.map(s=>s.id),'mixte'])o[a][lv+id]=ks.reduce((s,k)=>s+R[k][lv+id].ind,0)/ks.length}
 return o;}

const pad=(s,n)=>String(s).padStart(n);
function afficher(S,res,avant){
 const A=parArchetype(S,res),B=avant&&parArchetype(avant.S,avant.res),cols=[...res.sc.map(s=>s.id),'mixte'];
 const l=[];l.push('Indice de rendement par or investi (100 = médiane des tours au niveau 1 dans ce scénario)'+(B?' — avant → après':''));
 l.push('Archétype  Niv '+cols.map(c=>pad(c,B?13:8)).join(''));
 for(const a of ARCHS){for(let lv=1;lv<=5;lv++)l.push(a.padEnd(10)+pad(lv,4)+' '+cols.map(c=>{const v=Math.round(A[a][lv+c]);return B?pad(Math.round(B[a][lv+c])+'→'+v,13):pad(v,8)}).join(''));l.push('')}
 return l.join('\n');
}
function rapport(S,res,avant){
 const {R,sc,ref}=res,l=['# Banc d\'essai des tours','',`Généré par \`node tests/outils/banc-tours.js\`. Monstres de la ${MIN/60}e minute (armure ×${M.toFixed(1)}), une tour seule dans un labyrinthe en serpentin, moyenne de deux emplacements (${POSS.map(P=>P.id+' '+P.p).join(', ')}), pas de temps 1/60 s.`,'',
  '## Scénarios et référence (dégâts pour 100 or, médiane des tours niveau 1)','',...sc.map(s=>`- **${s.id}** : ${s.nom} — référence ${Math.round(ref[s.id])}`),'',
  '## Par archétype (moyenne des factions)','','```',afficher(S,res,avant),'```','','## Détail par tour (indice mixte, niveaux 1 → 5 ; dégâts/s affichés au niveau 1)',''];
 for(let f=0;f<S.FACTIONS.length;f++){l.push(`### ${S.FACTIONS[f].name}`,'','| # | Tour | Type | Coût | Niv 1 | Niv 2 | Niv 3 | Niv 4 | Niv 5 | Or total niv 5 |','|---|---|---|---|---|---|---|---|---|---|');
  for(let j=0;j<10;j++){const k=f*10+j,T=S.TW[k];l.push(`| ${j} | ${T.n} | ${S.BASE_TW[T.skin].n} | ${T.c} | `+[1,2,3,4,5].map(lv=>Math.round(R[k][lv+'mixte'].ind)).join(' | ')+` | ${R[k]['5sol4'].inv} |`)}l.push('')}
 return l.join('\n');
}

if(require.main===module){
 const arg=n=>{const i=process.argv.indexOf(n);return i>0?process.argv[i+1]:null};
 const t0=Date.now(),S=charger(arg('--moteur')||'actuel'),res=banc(S);
 let avant=null;const ref=arg('--avant');
 if(ref){const code=execSync(`git show ${ref}:sim.js`,{cwd:RACINE,encoding:'utf8',maxBuffer:1<<26});const SA=charger({code});avant={S:SA,res:banc(SA)}}
 console.log(afficher(S,res,avant));
 const dos=path.join(RACINE,'rapports');fs.mkdirSync(dos,{recursive:true});fs.writeFileSync(path.join(dos,'banc-tours.md'),rapport(S,res,avant));
 console.log(`Détail : rapports/banc-tours.md (${((Date.now()-t0)/1000).toFixed(1)} s)`);
}
module.exports={banc,parArchetype,mesurer};
