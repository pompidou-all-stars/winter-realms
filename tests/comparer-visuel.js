/* Comparaison visuelle avant / après.
   Usage : node tests/comparer-visuel.js [version-avant]     (par défaut : origin/main)
   « Avant » = la version indiquée (extraite de git dans un dossier temporaire) ; « après » = les fichiers actuels.
   Les deux sont capturées sur la même machine, dans le même navigateur, dans la même séance :
   c'est la condition pour éviter les fausses différences (voir CLAUDE.md, « Conditions de la comparaison visuelle »).
   Un « témoin » capture deux fois la version actuelle : il doit donner 0 % de différence, sinon la comparaison n'est pas fiable. */
'use strict';
const fs=require('fs'),path=require('path'),os=require('os'),{execFileSync}=require('child_process');
const N=require('./outils/navigateur'),{RACINE}=require('./outils/moteur'),{capturer}=require('./captures');

const SEUIL_CANAL=16;       // écart minimal (sur 255) pour qu'un pixel compte comme « changé » (absorbe le lissage des bords)
const SEUIL_IDENTIQUE=0.05; // en dessous de ce pourcentage de pixels changés, l'écran est considéré comme identique

function extraire(ref){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'wr-avant-'));
 const tar=execFileSync('git',['archive',ref,'index.html','sim.js'],{cwd:RACINE});execFileSync('tar',['-x','-C',dir],{input:tar});return dir}

/* compare deux images dans le navigateur ; renvoie le % de pixels changés et une image « avant | après | différences » */
async function difference(nav,fa,fb,titre,sortie){
 const page=await nav.newPage();const a='data:image/png;base64,'+fs.readFileSync(fa).toString('base64'),b='data:image/png;base64,'+fs.readFileSync(fb).toString('base64');
 const r=await page.evaluate(async({a,b,titre,SEUIL_CANAL})=>{
  const charge=s=>new Promise(ok=>{const i=new Image();i.onload=()=>ok(i);i.src=s});const A=await charge(a),B=await charge(b);
  const w=Math.max(A.width,B.width),h=Math.max(A.height,B.height),pix=i=>{const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.drawImage(i,0,0);return g.getImageData(0,0,w,h)};
  const da=pix(A),db=pix(B),dd=new ImageData(w,h);let n=0;
  for(let i=0;i<da.data.length;i+=4){const ec=Math.max(Math.abs(da.data[i]-db.data[i]),Math.abs(da.data[i+1]-db.data[i+1]),Math.abs(da.data[i+2]-db.data[i+2]));
   const gris=(db.data[i]+db.data[i+1]+db.data[i+2])/3*.35+150;
   if(ec>SEUIL_CANAL){n++;dd.data[i]=255;dd.data[i+1]=0;dd.data[i+2]=0}else{dd.data[i]=dd.data[i+1]=dd.data[i+2]=gris}dd.data[i+3]=255}
  const pc=A.width!=B.width||A.height!=B.height?100:n/(w*h)*100;
  const marge=20,haut=90,c=document.createElement('canvas');c.width=w*3+marge*4;c.height=h+haut+marge;const g=c.getContext('2d');
  g.fillStyle='#ffffff';g.fillRect(0,0,c.width,c.height);g.fillStyle='#111';g.font='bold 34px sans-serif';
  g.fillText(titre+' — '+(pc<0.005?'0':pc.toFixed(2))+' % de pixels changés',marge,40);g.font='28px sans-serif';
  ['AVANT','APRÈS','DIFFÉRENCES (en rouge)'].forEach((t,k)=>g.fillText(t,marge+k*(w+marge),78));
  g.drawImage(A,marge,haut);g.drawImage(B,w+2*marge,haut);g.putImageData(dd,2*w+3*marge,haut);
  return {pc,png:c.toDataURL('image/png')}},{a,b,titre,SEUIL_CANAL});
 await page.close();fs.writeFileSync(sortie,Buffer.from(r.png.split(',')[1],'base64'));return r.pc;
}

/* lance toute la comparaison ; renvoie un résultat détaillé (utilisé aussi par le bilan) */
async function comparer(ref='origin/main',{temoin=true}={}){
 const dossier=path.join(RACINE,'captures','comparaison');fs.rmSync(dossier,{recursive:true,force:true});fs.mkdirSync(dossier,{recursive:true});
 const avantDir=extraire(ref),nav=await N.lancer();
 const res={avant:ref,apres:'fichiers actuels',ecrans:[],remarques:[],fiable:true};
 try{
  let police='reelle';
  let A=await capturer({racine:avantDir,sortie:path.join(dossier,'avant'),police,nav});
  let B=await capturer({sortie:path.join(dossier,'apres'),police,nav});
  if(!A.policeChargee||!B.policeChargee){police='bloquee';res.remarques.push('La police Fredoka n\'a pas pu être chargée des deux côtés : la comparaison a été refaite avec la police de remplacement, pour les deux versions.');
   A=await capturer({racine:avantDir,sortie:path.join(dossier,'avant'),police,nav});B=await capturer({sortie:path.join(dossier,'apres'),police,nav})}
  res.police=police;
  for(const e of A.erreurs)res.remarques.push('Avant : '+e);for(const e of B.erreurs)res.remarques.push('Après : '+e);
  if(temoin){const T=await capturer({sortie:path.join(dossier,'temoin'),police,nav});let pire=0;
   for(const im of B.images){const t=T.images.find(x=>x.format==im.format&&x.id==im.id);if(t)pire=Math.max(pire,await difference(nav,im.fichier,t.fichier,'Témoin',path.join(dossier,'temoin',`diff-${im.format}-${im.id}.png`)))}
   res.temoin=pire;if(pire>=SEUIL_IDENTIQUE){res.fiable=false;res.remarques.push(`Le témoin n'est pas stable (${pire.toFixed(2)} %) : la comparaison n'est pas fiable sur cette machine.`)}}
  for(const im of B.images){const av=A.images.find(x=>x.format==im.format&&x.id==im.id);
   if(!av){res.ecrans.push({format:im.format,id:im.id,titre:im.titre,pc:null,apres:im.fichier});continue}
   const f=path.join(dossier,`${im.format}-${im.id}.png`),pc=await difference(nav,av.fichier,im.fichier,`${im.titre} (${im.format})`,f);
   res.ecrans.push({format:im.format,id:im.id,titre:im.titre,pc,identique:pc<SEUIL_IDENTIQUE,image:f,avant:av.fichier,apres:im.fichier})}
 }finally{await nav.close();fs.rmSync(avantDir,{recursive:true,force:true})}
 fs.writeFileSync(path.join(dossier,'resultat.json'),JSON.stringify(res,null,1));return res;
}
module.exports={comparer,SEUIL_IDENTIQUE,SEUIL_CANAL};

if(require.main===module){
 if(!N.disponible()){console.log('Playwright n\'est pas installé : comparaison visuelle impossible sur cette machine.');process.exit(0)}
 comparer(process.argv[2]||'origin/main').then(r=>{
  console.log(`Comparaison visuelle : ${r.avant} → fichiers actuels (police : ${r.police=='reelle'?'Fredoka':'remplacement'})`);
  if(r.temoin!==undefined)console.log(`Témoin (même version capturée deux fois) : ${r.temoin.toFixed(2)} %`);
  for(const e of r.ecrans)console.log(`${e.identique?'✅':'⚠️'} ${e.titre} (${e.format}) : ${e.pc==null?'pas d\'image avant':e.pc.toFixed(2)+' % de pixels changés'}`);
  for(const m of r.remarques)console.log('• '+m);console.log('Images : captures/comparaison/');
 });
}
