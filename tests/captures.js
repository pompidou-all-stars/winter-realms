/* Captures d'écran du jeu, format téléphone : 5 écrans en portrait, et l'accueil en paysage
   (depuis la 2.15, le jeu se joue en portrait ; en paysage, un téléphone affiche « Tourne ton téléphone »).
   Usage : node tests/captures.js            → images du vrai jeu (vue 3D, depuis la 2.29) dans captures/actuel/
           node tests/captures.js --2d       → la même chose avec la 2D de secours, dans captures/2d/
   (--3d, l'ancienne option, est gardé : c'est désormais le choix par défaut)
   Le scénario est toujours le même (graine fixe, horloge figée) : deux lancements donnent les mêmes images
   sur une même machine. Il fonctionne aussi avec les versions d'avant la 2.15 (comparaison visuelle avec main).
   Voir CLAUDE.md, « Conditions de la comparaison visuelle ». */
'use strict';
const fs=require('fs'),path=require('path');
const N=require('./outils/navigateur'),{demarrer}=require('./outils/serveur'),{RACINE}=require('./outils/moteur');

const ECRANS=[
 {id:'1-accueil',titre:'Écran d\'accueil'},
 {id:'2-debut',titre:'Début de partie (4 tours posées)'},
 {id:'3-partie',titre:'Partie en cours (35 s de jeu, monstres en route)'},
 {id:'4-panneau',titre:'Fiche d\'une tour posée'},
 {id:'5-adversaires',titre:'Terrains des adversaires (panneau des vignettes)'}];
const FORMATS=['portrait','paysage'];
/* écrans capturés pour chaque format (portrait seulement depuis la 2.15, sauf l'accueil) */
const ECRANS_DU_FORMAT={portrait:ECRANS.map(e=>e.id),paysage:['1-accueil']};

/* joue le scénario et enregistre les images ; renvoie la liste des captures et l'état de la police */
/* rendu : '3d' (par défaut depuis la 2.29 : le vrai jeu, WebGL logiciel ou carte graphique avec WR_GPU=1) ou '2d' (secours, ?rendu=2d) */
async function capturer({racine=RACINE,sortie,police='reelle',echelle=2,graine=12345,nav=null,rendu='3d'}={}){
 fs.mkdirSync(sortie,{recursive:true});
 const srv=await demarrer(racine),proprio=!nav;if(!nav)nav=await N.lancer({webgl:rendu=='3d'});
 const res={police,policeChargee:true,images:[],erreurs:[]};
 try{for(const format of FORMATS){const o=await N.ouvrir(nav,srv.url+(rendu=='3d'?'?rendu=3d':'?rendu=2d'),{format,graine,police,echelle}),p=o.page;
  if(!o.policeChargee)res.policeChargee=false;
  const prendre=async e=>{const f=path.join(sortie,`${format}-${e.id}.png`);await p.screenshot({path:f,animations:'allow'});res.images.push({format,...e,fichier:f})};
  try{
   if(rendu=='3d'&&!await N.attendre3D(p))throw new Error('le rendu 3D ne s\'est pas chargé');
   await prendre(ECRANS[0]);
   if(ECRANS_DU_FORMAT[format].length>1){
    await N.toucher(p,'#go0');await N.avancer(p,500);
    /* 2.15 : on choisit d'abord une tour (avant, la première était déjà choisie : ce toucher ne change rien) */
    await N.toucher(p,'#bar button >> nth=0');
    for(const [x,y] of [[5,6],[7,6],[5,10],[7,10]])await N.construire(p,x,y);
    await N.avancer(p,500);await prendre(ECRANS[1]);
    await N.avancer(p,34000);await prendre(ECRANS[2]);
    await N.toucherCase(p,5,6);await N.avancer(p,200);await prendre(ECRANS[3]);
    /* fermer la fiche : bouton × depuis la 2.15, bouton « Fermer » de la barre avant */
    if(await p.locator('#fiche .fermer').count())await N.toucher(p,'#fiche .fermer');else await N.toucher(p,'#bar button:has-text("Fermer")');
    await N.toucher(p,'#cartesBtn');await N.avancer(p,200);await prendre(ECRANS[4])}
  }catch(err){res.erreurs.push(`${format} : ${err.message.split('\n')[0]}`)}
  for(const e of o.erreurs)res.erreurs.push(`${format} : erreur JavaScript : ${e}`);
  await o.fermer()}}
 finally{if(proprio)await nav.close();await srv.fermer()}
 return res;
}
module.exports={capturer,ECRANS,FORMATS,ECRANS_DU_FORMAT};

if(require.main===module){
 if(!N.disponible()){console.log('Playwright n\'est pas installé : captures impossibles sur cette machine.');process.exit(0)}
 const rendu=process.argv.includes('--2d')?'2d':'3d',sortie=path.join(RACINE,'captures',rendu=='2d'?'2d':'actuel');
 capturer({sortie,rendu}).then(r=>{
  console.log(`${r.images.length} captures enregistrées dans ${path.relative(RACINE,sortie)}/`);
  if(!r.policeChargee)console.log('⚠️ La police Fredoka n\'a pas pu être chargée : le texte utilise une police de remplacement.');
  for(const e of r.erreurs)console.log('❌ '+e);process.exit(r.erreurs.length?1:0)});
}
