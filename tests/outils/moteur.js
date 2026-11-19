/* Charge un moteur de jeu (sim.js) dans un environnement isolé, sans le modifier.
   - graine : remplace Math.random par le générateur à graine, pour rejouer une partie à l'identique ;
   - expose aussi les fonctions internes (IA, constantes) dont les tests ont besoin. */
'use strict';
const vm=require('vm'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const {mulberry32}=require('./hasard');
const RACINE=path.join(__dirname,'..','..');
/* WR_MOTEUR permet de faire passer toute la suite de tests à un autre moteur (vérification, comparaison de versions) */
const MOTEURS={actuel:process.env.WR_MOTEUR?path.resolve(process.env.WR_MOTEUR):path.join(RACINE,'sim.js')};
const INTERNES=['aiAct','encaisse','trajet','expo','aiDefend','aiAttack','PLAN','pathCells','mzStep','mzPath','plen','mzKind','invest','airInv','mages','BASE_TW','FACTION_BALANCE','ARCH','ROLE','ORDER','HPK','GRACE','GROUP','AURA_R','DIRS','dmg','rng','upCost','topY','flyH','NORM','FLY','AURA','SPEC','HEAL','SPLIT','TURT','BRK','SAP','KID'];

function sha256(fichier){return crypto.createHash('sha256').update(fs.readFileSync(fichier)).digest('hex')}

/* source : 'actuel', un chemin de fichier, ou {code} (texte d'un sim.js, par exemple extrait de git).
   graine : 1 par défaut, pour que chaque test soit reproductible ; graine:null redonne le vrai hasard (Math.random). */
function charger(source='actuel',{graine=1}={}){
 const code=typeof source=='object'?source.code:fs.readFileSync(MOTEURS[source]||source,'utf8');
 const M={};for(const n of Object.getOwnPropertyNames(Math))M[n]=Math[n];M.random=graine==null?Math.random:mulberry32(graine);
 const ctx={module:{exports:{}},Math:M,console};vm.createContext(ctx);
 const expo=INTERNES.map(n=>`try{__I.${n}=${n}}catch(e){}`).join('');
 vm.runInContext(code+`\n;var __I={};${expo};this.__I=__I;`,ctx,{filename:typeof source=='string'?source:'sim.js'});
 /* regrainer(g) : repart d'une graine donnée et remet à zéro le compteur d'identifiants des monstres (UID),
    pour qu'une mesure donne le même résultat quel que soit l'ordre des mesures (banc d'essai en parallèle) */
 const regrainer=g=>{M.random=mulberry32(g);try{vm.runInContext('UID=0',ctx)}catch(e){}};
 return Object.assign({},ctx.module.exports,ctx.__I,{hasard:M.random,regrainer});
}

/* Partie de test. Par défaut : 4 sièges humains (aucune IA n'agit), utile pour monter une situation précise. */
function partie(S,{factions=[0,1,2,3],ia=[0,0,0,0],difficulte=0}={}){
 return new S.Game(factions.map((f,i)=>({name:'J'+i,col:'#fff',ai:ia[i],classId:f})),difficulte);
}

/* Fait apparaître un monstre immédiatement sur un terrain, avec le code d'apparition du moteur lui-même. */
function apparaitre(S,b,k,m=1){b.q.push({k,m,t:0});const avant=b.cr.length;b.update(0);return b.cr[avant]}

/* Avance la partie de « secondes », par pas de dt (0,05 s comme dans le navigateur au plus lent). */
function avancer(G,secondes,dt=.05){const n=Math.round(secondes/dt);for(let i=0;i<n;i++)G.step(dt)}
/* Avance un seul terrain (sans revenu ni IA). */
function avancerTerrain(b,secondes,dt=.05){const n=Math.round(secondes/dt);for(let i=0;i<n;i++)b.update(dt)}
/* Depuis la 2.4, une tour posée ou améliorée est d'abord en chantier (t.b > 0) et ne tire pas.
   Fait avancer le terrain jusqu'à la fin de tous les chantiers (sans effet sur un moteur plus ancien). */
function pret(b,dt=.05){for(let i=0;i<1000&&b.t.some(t=>t.b>0);i++)b.update(dt)}

module.exports={charger,partie,apparaitre,avancer,avancerTerrain,pret,sha256,MOTEURS,RACINE};
