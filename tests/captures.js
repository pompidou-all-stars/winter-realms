/* Captures d'écran du jeu, format téléphone, portrait et paysage (5 écrans).
   Usage : node tests/captures.js            → images dans captures/actuel/
           node tests/captures.js --3d       → la même chose avec le rendu 3D (2.6), dans captures/3d/
   Le scénario est toujours le même (graine fixe, horloge figée) : deux lancements donnent les mêmes images
   sur une même machine. Voir CLAUDE.md, « Conditions de la comparaison visuelle ». */
'use strict';
const fs=require('fs'),path=require('path');
const N=require('./outils/navigateur'),{demarrer}=require('./outils/serveur'),{RACINE}=require('./outils/moteur');

const ECRANS=[
 {id:'1-accueil',titre:'Écran d\'accueil'},
 {id:'2-debut',titre:'Début de partie (4 tours posées)'},
 {id:'3-partie',titre:'Partie en cours (35 s de jeu, monstres en route)'},
 {id:'4-panneau',titre:'Panneau d\'une tour sélectionnée'},
 {id:'5-zoom',titre:'Terrain zoomé à deux doigts'}];
const FORMATS=['portrait','paysage'];

/* joue le scénario et enregistre les images ; renvoie la liste des captures et l'état de la police */
/* rendu : '2d' (par défaut) ou '3d' (2.6, ?rendu=3d, WebGL logiciel) */
async function capturer({racine=RACINE,sortie,police='reelle',echelle=2,graine=12345,nav=null,rendu='2d'}={}){
 fs.mkdirSync(sortie,{recursive:true});
 const srv=await demarrer(racine),proprio=!nav;if(!nav)nav=await N.lancer({webgl:rendu=='3d'});
 const res={police,policeChargee:true,images:[],erreurs:[]};
 try{for(const format of FORMATS){const o=await N.ouvrir(nav,srv.url+(rendu=='3d'?'?rendu=3d':''),{format,graine,police,echelle}),p=o.page;
  if(!o.policeChargee)res.policeChargee=false;
  const prendre=async e=>{const f=path.join(sortie,`${format}-${e.id}.png`);await p.screenshot({path:f,animations:'allow'});res.images.push({format,...e,fichier:f})};
  try{
   if(rendu=='3d'&&!await N.attendre3D(p))throw new Error('le rendu 3D ne s\'est pas chargé');
   await prendre(ECRANS[0]);
   await N.toucher(p,'#go0');await N.avancer(p,500);
   for(const [x,y] of [[5,6],[7,6],[5,10],[7,10]])await N.construire(p,x,y);
   await N.avancer(p,500);await prendre(ECRANS[1]);
   await N.avancer(p,34000);await prendre(ECRANS[2]);
   await N.toucherCase(p,5,6);await N.avancer(p,200);await prendre(ECRANS[3]);
   await N.toucher(p,'#bar button:has-text("Fermer")');const c=await N.centreCase(p,6,7);
   await N.deuxDoigts(p,{de:[{x:c.x-25,y:c.y},{x:c.x+25,y:c.y}],vers:[{x:c.x-60,y:c.y},{x:c.x+60,y:c.y}]});await N.avancer(p,200);await prendre(ECRANS[4]);
  }catch(err){res.erreurs.push(`${format} : ${err.message.split('\n')[0]}`)}
  for(const e of o.erreurs)res.erreurs.push(`${format} : erreur JavaScript : ${e}`);
  await o.fermer()}}
 finally{if(proprio)await nav.close();await srv.fermer()}
 return res;
}
module.exports={capturer,ECRANS,FORMATS};

if(require.main===module){
 if(!N.disponible()){console.log('Playwright n\'est pas installé : captures impossibles sur cette machine.');process.exit(0)}
 const rendu=process.argv.includes('--3d')?'3d':'2d',sortie=path.join(RACINE,'captures',rendu=='3d'?'3d':'actuel');
 capturer({sortie,rendu}).then(r=>{
  console.log(`${r.images.length} captures enregistrées dans ${path.relative(RACINE,sortie)}/`);
  if(!r.policeChargee)console.log('⚠️ La police Fredoka n\'a pas pu être chargée : le texte utilise une police de remplacement.');
  for(const e of r.erreurs)console.log('❌ '+e);process.exit(r.erreurs.length?1:0)});
}
