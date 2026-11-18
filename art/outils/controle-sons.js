#!/usr/bin/env node
/* Contrôle qualité des fichiers son : ouvre ecoute-sons.html dans un navigateur sans fenêtre (Playwright),
   décode chaque fichier et mesure durée, crête, niveau moyen, silences et saturation.
   Usage : node art/outils/controle-sons.js [motif]   (ex. « tir-arrow » ; sans motif : tous les sons)
   Sur Windows sans Chromium de Playwright : WR_CANAL=msedge. Sortie : une ligne par fichier, « ⚠ » si un défaut est trouvé. */
'use strict';
const path=require('path'),http=require('http'),fs=require('fs');
let pw;try{pw=require('playwright')}catch(e){console.log('Playwright absent : contrôle ignoré.');process.exit(0)}
const RAC=path.join(__dirname,'..','..'),motif=process.argv[2]||'';
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.json':'application/json','.mp3':'audio/mpeg'};
const srv=http.createServer((q,r)=>{const f=path.join(RAC,decodeURIComponent(q.url.split('?')[0]));
 if(!f.startsWith(RAC)||!fs.existsSync(f)||fs.statSync(f).isDirectory()){r.writeHead(404);r.end();return}
 r.writeHead(200,{'Content-Type':TYPES[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)});
srv.listen(0,async()=>{const port=srv.address().port;let nav;
 try{nav=await pw.chromium.launch(process.env.WR_CANAL?{channel:process.env.WR_CANAL}:{});
  const p=await nav.newPage();await p.goto('http://localhost:'+port+'/ecoute-sons.html');
  await p.waitForFunction(()=>typeof MAN!=='undefined'&&MAN!==null,null,{timeout:15000});
  /* le motif vise un son (« tir-arrow ») ou un seul fichier (« tir-arrow-alliance-3 ») */
  const res=await p.evaluate(async m=>{const ids=Object.keys(MAN.sons).filter(i=>i.includes(m)||MAN.sons[i].some(f=>f.includes(m)));
   const r=await mesurer(ids),seul=m?Object.keys(r).filter(f=>f.includes(m+'.mp3')):[];return seul.length?{[seul[0]]:r[seul[0]]}:r},motif);
  let ko=0;for(const [f,x] of Object.entries(res)){const pb=x.erreur?[x.erreur]:x.problemes;if(pb.length)ko++;
   console.log((pb.length?'⚠ ':'✓ ')+f+'  '+(x.erreur?'':x.dur+' s · crête '+x.crete+' dB · moyen '+x.rms+' dB · silence début '+x.debut+' s / fin '+x.fin+' s · saturé '+x.sature+' %')+(pb.length?'  → '+pb.join(', '):''))}
  console.log(Object.keys(res).length+' fichiers contrôlés, '+ko+' à vérifier');
 }catch(e){console.log('Erreur : '+e.message);process.exitCode=1}finally{if(nav)await nav.close();srv.close()}});
