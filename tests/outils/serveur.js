/* Mini serveur web local (sans dépendance), pour ouvrir le jeu dans le navigateur de test. */
'use strict';
const http=require('http'),fs=require('fs'),path=require('path');
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css','.png':'image/png','.json':'application/json','.svg':'image/svg+xml','.glb':'model/gltf-binary','.mp3':'audio/mpeg','.mjs':'text/javascript; charset=utf-8'};
/* sert le dossier « racine » sur un port libre ; renvoie {url, fermer()} */
function demarrer(racine){return new Promise(ok=>{
 const srv=http.createServer((req,res)=>{let p=decodeURIComponent(new URL(req.url,'http://x').pathname);if(p.endsWith('/'))p+='index.html';
  const f=path.join(racine,path.normalize(p).replace(/^(\.\.[\/\\])+/,''));
  if(!f.startsWith(racine)||!fs.existsSync(f)||fs.statSync(f).isDirectory()){res.writeHead(404);res.end('Introuvable');return}
  res.writeHead(200,{'Content-Type':TYPES[path.extname(f)]||'application/octet-stream','Cache-Control':'no-store'});fs.createReadStream(f).pipe(res)});
 srv.listen(0,'127.0.0.1',()=>ok({url:`http://127.0.0.1:${srv.address().port}/`,fermer:()=>new Promise(r=>srv.close(r))}))})}
module.exports={demarrer};
