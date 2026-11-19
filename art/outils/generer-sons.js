#!/usr/bin/env node
/* Génère la bibliothèque sonore en local, avec l'API ElevenLabs et ta clé API (variable d'environnement ELEVENLABS_API_KEY).
   Un son à la fois (2.28 : en cas d'erreur, 3 essais au plus ; 3 sons de suite en échec arrêtent tout) : génération → enregistrement → contrôle qualité (controle-sons.js) → son suivant.
   Un fichier refusé (muet, saturé…) est mis de côté puis régénéré, 2 essais au plus ; ensuite il est signalé et sauté.
   La consigne de chaque son vient de assets/audio/catalogue.json ; seuls les fichiers manquants sont produits.
   Usage : node art/outils/generer-sons.js [--max N] [--motif tir-] [--reserve 1500] [--sans-voix]
     --max N       : s'arrête après N fichiers (par défaut : tout)
     --motif X     : seulement les sons dont l'identifiant contient X
     --reserve R   : s'arrête quand il reste moins de R crédits (par défaut 1500)
     --sans-voix   : ne génère pas les répliques
   Sur Windows, pour le contrôle qualité : WR_CANAL=msedge et NODE_PATH vers Playwright (voir CLAUDE.md §12). */
'use strict';
const fs=require('fs'),path=require('path'),{execFileSync}=require('child_process');
const RAC=path.join(__dirname,'..','..'),AUD=path.join(RAC,'assets','audio'),REJ=path.join(AUD,'..','..','.sons-refuses');
const CLE=process.env.ELEVENLABS_API_KEY;
if(!CLE){console.log('ELEVENLABS_API_KEY absente : crée une clé sur elevenlabs.io (Developers → API Keys) et mets-la dans cette variable.');process.exit(1)}
const arg=(n,d)=>{const i=process.argv.indexOf(n);return i<0?d:process.argv[i+1]};
const MAX=+arg('--max',1e9),MOTIF=arg('--motif',''),RESERVE=+arg('--reserve',1500),VOIX=!process.argv.includes('--sans-voix');
const cat=JSON.parse(fs.readFileSync(path.join(AUD,'catalogue.json'),'utf8'));
const dossier=id=>id.startsWith('tir-')?'tours':/^(chantier|fini|up)-/.test(id)?'construction':/^(mort|arrivee|cri)-/.test(id)?'monstres':id.startsWith('amb-')?'ambiances':id.startsWith('voix-')?'voix/'+id.split('-')[1]:'interface';
const attendre=ms=>new Promise(r=>setTimeout(r,ms));

function presents(){const p={nums:{}};(function f(d){if(!fs.existsSync(d))return;for(const x of fs.readdirSync(d)){const q=path.join(d,x);
 if(fs.statSync(q).isDirectory())f(q);else{const m=/^(.+)-(\d+)\.mp3$/.exec(x);if(m){p[m[1]]=(p[m[1]]||0)+1;(p.nums[m[1]]=p.nums[m[1]]||new Set()).add(+m[2])}}}})(AUD);return p}
/* liste ordonnée de ce qui manque : bruitages d'abord, puis répliques */
function aFaire(){const p=presents(),l=[];
 for(const s of cat.sons)for(let i=p[s.id]||0;i<s.n;i++)l.push({id:s.id,type:'sfx',s});
 if(VOIX)for(const [f,ctx] of Object.entries(cat.repliques))for(const [c,textes] of Object.entries(ctx)){const id='voix-'+f+'-'+c;
  // la réplique n° i va toujours dans le fichier -(i+1), pour qu'une phrase refaite reste à sa place
  for(let i=0;i<textes.length;i++)if(!(p.nums[id]&&p.nums[id].has(i+1)))l.push({id,type:'tts',f,texte:textes[i],n:i+1})}
 return l.filter(x=>x.id.includes(MOTIF))}

async function api(url,corps,essais=3){
 for(let e=0;;e++){const r=await fetch('https://api.elevenlabs.io'+url,{method:corps?'POST':'GET',headers:{'xi-api-key':CLE,'Content-Type':'application/json'},body:corps?JSON.stringify(corps):undefined});
  if(r.ok)return r;const t=await r.text();
  if((r.status==429||r.status>=500)&&e<essais){const d=15000*(e+1);console.log('  occupé ('+r.status+'), nouvel essai dans '+d/1000+' s');await attendre(d);continue}
  throw new Error(r.status+' '+t.slice(0,300))}}
async function credits(){const j=await (await api('/v1/user/subscription')).json();return {reste:j.character_limit-j.character_count,limite:j.character_limit}}

async function generer(x){
 if(x.type=='sfx'){const s=x.s,c={text:s.p,model_id:'eleven_text_to_sound_v2',duration_seconds:s.dur,prompt_influence:.5};if(s.loop)c.loop=true;
  return Buffer.from(await (await api('/v1/sound-generation?output_format=mp3_44100_128',c)).arrayBuffer())}
 const v=cat.voix[x.f];
 return Buffer.from(await (await api('/v1/text-to-speech/'+v.voice_id+'?output_format=mp3_44100_128',{text:v.ton+' '+x.texte,model_id:cat.modele_voix||'eleven_v3'})).arrayBuffer())}

function enregistrer(id,buf,num){const d=path.join(AUD,dossier(id));fs.mkdirSync(d,{recursive:true});let n=num||1;while(!num&&fs.existsSync(path.join(d,id+'-'+n+'.mp3')))n++;
 const f=path.join(d,id+'-'+n+'.mp3');fs.writeFileSync(f,buf);return f}
function manifeste(){execFileSync(process.execPath,[path.join(__dirname,'manifeste-audio.js')],{stdio:'ignore'})}
function controle(f){try{const o=execFileSync(process.execPath,[path.join(__dirname,'controle-sons.js'),path.basename(f,'.mp3')],{encoding:'utf8',env:process.env});
  const l=o.split('\n')[0];return {ok:!l.startsWith('⚠'),ligne:l}}catch(e){return {ok:true,ligne:'(contrôle indisponible : '+e.message.split('\n')[0]+')'}}}

(async()=>{let c=await credits();console.log('Crédits restants : '+c.reste+' / '+c.limite);
 let faits=0,refus=0,echecs=0;const sautes=new Set();
 while(faits<MAX){const l=aFaire().filter(x=>!sautes.has(x.id));if(!l.length){console.log('Rien à générer.');break}
  if(c.reste<RESERVE){console.log('Réserve atteinte ('+c.reste+' crédits) : arrêt.');break}
  const x=l[0];let essai=0,ok=false;
  while(essai<3&&!ok){essai++;
   try{const f=enregistrer(x.id,await generer(x),x.n);manifeste();const q=controle(f);console.log((q.ok?'✓ ':'⚠ ')+q.ligne.replace(/^[✓⚠] /,''));
    if(q.ok)ok=true;else{fs.mkdirSync(REJ,{recursive:true});fs.renameSync(f,path.join(REJ,path.basename(f,'.mp3')+'-refus'+Date.now()+'.mp3'));manifeste();refus++}}
   catch(e){console.log('✗ '+x.id+' : '+e.message);if(/40[0-4]/.test(e.message))break;await attendre(20000)}}
  if(ok){faits++;echecs=0}else{sautes.add(x.id);console.log('  → '+x.id+' sauté, à revoir');if(++echecs>=3){console.log('3 sons de suite en échec : arrêt.');break}}
  c=await credits();await attendre(1500)}
 console.log(faits+' fichiers produits, '+refus+' refusés au contrôle'+(sautes.size?', sautés : '+[...sautes].join(', '):'')+'. Crédits restants : '+c.reste+'. Reste '+aFaire().length+' fichiers.')})();
