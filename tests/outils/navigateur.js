/* Pilotage du jeu dans un navigateur Chromium (Playwright), au format téléphone.
   Conditions identiques à chaque fois :
   - hasard à graine injecté AVANT le chargement du jeu (Math.random remplacé dans la page, le jeu n'est pas modifié) ;
   - horloge du navigateur figée puis avancée pas à pas (animations et partie toujours au même instant) ;
   - taille d'écran, densité de pixels, langue et fuseau horaire fixés. */
'use strict';
const {SOURCE_NAVIGATEUR}=require('./hasard');
let playwright=null;try{playwright=require('playwright')}catch(e){}

const FORMATS={
 portrait:{viewport:{width:390,height:844}},
 paysage:{viewport:{width:844,height:390}}};
const DEBUT=new Date('2026-01-01T12:00:00Z');

function disponible(){return !!playwright}

/* options de Chromium pour un rendu reproductible : rendu logiciel, pas de lissage sous-pixel ni d'optimisations variables */
const OPTIONS_STABLES=['--disable-gpu','--disable-lcd-text','--font-render-hinting=none','--force-color-profile=srgb','--disable-partial-raster','--disable-skia-runtime-opts','--disable-threaded-animation','--disable-threaded-scrolling','--disable-checker-imaging'];
/* webgl : pour le rendu 3D (2.7), WebGL en rendu logiciel SwiftShader (identique sur toutes les machines, sans carte graphique) */
const OPTIONS_WEBGL=OPTIONS_STABLES.filter(o=>o!='--disable-gpu').concat(['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);
/* WR_CANAL permet d'utiliser un navigateur déjà installé (par exemple msedge) au lieu du Chromium de Playwright */
/* WR_GPU=1 : la 3D utilise la vraie carte graphique de la machine, plus rapide et plus proche d'un téléphone (pour un PC qui en a une ;
   GitHub et le cloud n'en ont pas et gardent SwiftShader). Les captures restent comparables tant que l'avant et l'après sont pris dans la même séance. */
const OPTIONS_GPU=OPTIONS_STABLES.filter(o=>o!='--disable-gpu').concat(['--ignore-gpu-blocklist'],process.platform=='win32'?['--use-angle=d3d11']:[]);
async function lancer({webgl=false}={}){return playwright.chromium.launch({args:webgl?(process.env.WR_GPU=='1'?OPTIONS_GPU:OPTIONS_WEBGL):OPTIONS_STABLES,...(process.env.WR_CANAL?{channel:process.env.WR_CANAL}:{})})}

/* ouvre le jeu ; options : format, graine, police ('reelle' ou 'bloquee'), echelle (densité de pixels),
   bloquer (fichiers du jeu à rendre introuvables, par exemple ['rendu3d.js'] pour simuler un appareil où la 3D ne se charge pas) */
async function ouvrir(navigateur,url,{format='portrait',graine=12345,police='reelle',echelle=2,bloquer=[]}={}){
 const ctx=await navigateur.newContext({...FORMATS[format],deviceScaleFactor:echelle,isMobile:true,hasTouch:true,locale:'fr-FR',timezoneId:'Europe/Paris',reducedMotion:'no-preference'});
 const page=await ctx.newPage();
 /* 2.35 : on ignore l'icône d'onglet (/favicon.ico) que demande Edge (WR_CANAL=msedge), mais pas le Chromium de Playwright : le jeu n'en a pas */
 const erreurs=[];page.on('pageerror',e=>erreurs.push(e.message));page.on('console',m=>{if(m.type()=='error'&&!/\/favicon\.ico$/.test(m.location().url||''))erreurs.push(m.text())});
 /* aucune connexion vers l'extérieur, sauf la police si demandée (le multijoueur n'est jamais contacté) */
 const origine=new URL(url).origin+'/';
 if(bloquer.length)await page.route(u=>bloquer.some(b=>u.pathname.endsWith('/'+b)),r=>r.abort());
 await page.route(u=>!u.href.startsWith(origine),r=>{const h=new URL(r.request().url()).hostname;
  if(police=='reelle'&&(h=='fonts.googleapis.com'||h=='fonts.gstatic.com'))return r.continue();return r.abort()});
 await page.addInitScript(`window.__GRAINE__=${graine>>>0};`+SOURCE_NAVIGATEUR);
 await page.clock.install({time:DEBUT});
 /* horloge en pause : elle n'avance plus que lorsque le test le demande (sinon le temps réel s'écoule entre deux actions) */
 await page.clock.pauseAt(new Date(DEBUT.getTime()+1000));
 await page.goto(url);
 /* la police est découpée en plusieurs fichiers (graisses 500 et 700, jeux de caractères) : on les charge TOUS avant de continuer,
    sinon une capture peut montrer certaines lettres avec la mauvaise graisse */
 const policeChargee=await page.evaluate(async()=>{const fr=()=>[...document.fonts].filter(f=>/Fredoka/.test(f.family));
  await Promise.all(fr().map(f=>f.load().catch(()=>{})));await document.fonts.ready;return fr().length>0&&fr().every(f=>f.status=='loaded')});
 await page.clock.runFor(100);
 /* l'horloge simulée démarre avec 1 ou 2 ms de décalage selon les passages (temps réel écoulé pendant son installation) :
    on l'aligne sur exactement 2 000 ms pour que les animations (chemin, portail, barre de revenu, neige) soient identiques à chaque passage.
    2.29 : 2 000 ms au lieu de 200 : en 3D, le chargement est plus long et l'horloge dépassait parfois déjà 200 ms (jusqu'à 986) ;
    l'alignement était alors sauté et toute la partie décalée de quelques millisecondes d'un passage à l'autre */
 const pn=await page.evaluate(()=>performance.now());if(pn>=2000)throw new Error('horloge déjà à '+Math.round(pn)+' ms : impossible de l’aligner sur 2 000 ms');await page.clock.runFor(2000-pn);
 return {ctx,page,erreurs,policeChargee,fermer:()=>ctx.close()};
}

/* toucher le centre d'une case du terrain */
/* depuis la 2.1 le terrain peut être zoomé : la page fournit caseVersEcran ; les versions plus anciennes n'ont pas de zoom */
async function centreCase(page,x,y){return page.evaluate(([x,y])=>{if(typeof caseVersEcran=='function')return caseVersEcran(x,y);
 const r=document.getElementById('main').getBoundingClientRect();return {x:r.left+(x+.5)*r.width/13,y:r.top+(y+.5)*r.height/17}},[x,y])}
async function toucherCase(page,x,y){const c=await centreCase(page,x,y);await page.touchscreen.tap(c.x,c.y);await page.clock.runFor(50)}
/* construire une tour : deux touchers sur la même case depuis la 2.2 (aperçu puis confirmation), un seul avant */
async function construire(page,x,y){const deux=await page.evaluate(()=>typeof confirmerConstruction=='function');
 await toucherCase(page,x,y);if(deux)await toucherCase(page,x,y)}
/* glisser un doigt d'une case à une autre (sans relâcher entre les deux) */
async function glisser(page,de,vers,etapes=8){const a=await centreCase(page,de[0],de[1]),b=await centreCase(page,vers[0],vers[1]),cdp=await page.context().newCDPSession(page);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:a.x,y:a.y,id:1}]});
 for(let i=1;i<=etapes;i++){const k=i/etapes;await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:a.x+(b.x-a.x)*k,y:a.y+(b.y-a.y)*k,id:1}]})}
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await cdp.detach();await page.clock.runFor(50)}
/* geste à deux doigts (pincer / écarter / déplacer), envoyé comme de vrais événements tactiles */
async function deuxDoigts(page,{de,vers,etapes=8}){const cdp=await page.context().newCDPSession(page);const pts=(p,q)=>[{x:p.x,y:p.y,id:1},{x:q.x,y:q.y,id:2}];
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:pts(de[0],de[1])});
 for(let i=1;i<=etapes;i++){const k=i/etapes,l=(a,b)=>({x:a.x+(b.x-a.x)*k,y:a.y+(b.y-a.y)*k});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:pts(l(de[0],vers[0]),l(de[1],vers[1]))})}
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await cdp.detach();await page.clock.runFor(50)}
async function toucher(page,selecteur){await page.locator(selecteur).first().tap();await page.clock.runFor(50)}
/* En 3D, la partie avance toujours image par image (G.step à chaque image), mais la vue 3D n'est redessinée que 4 fois par seconde de jeu,
   puis une dernière fois à l'instant exact. Avant, chaque seconde de jeu dessinait 60 images en rendu logiciel, sans pause : depuis le paysage
   de la 2.26, environ 10 min pour 30 s de jeu, puis un plantage du navigateur de test (« Target crashed ») à l'arrivée des vagues, qui
   n'existe pas sur un vrai téléphone. En 2D, rien ne change. */
async function avancer(page,ms){
 const allege=await page.evaluate(()=>{if(typeof R3D=='undefined'||!R3D.api||typeof dessinerVue!='function'||window.__vueComplete)return false;
  const f=dessinerVue;window.__vueComplete=f;let d=-1e9;dessinerVue=t=>{if(t-d>=.25){d=t;f(t)}};return true});
 try{await page.clock.runFor(ms)}
 finally{if(allege)await page.evaluate(()=>{const f=window.__vueComplete;dessinerVue=f;delete window.__vueComplete;f(performance.now()/1000)}).catch(()=>{})}}
/* 2.15 : la fiche n'est visible que lorsqu'on a choisi quelque chose ; les boutons Améliorer et Vendre sont dans la fiche */
async function etat(page){return page.evaluate(()=>{const f=document.getElementById('fiche');return {or:P.gold,revenu:P.inc,vies:P.lives,tours:P.t.map(t=>({x:t.x,y:t.y,k:t.k,lv:t.lv})),temps:time,horloge:document.getElementById('clock').textContent,
 vue:view,fin:over,faction:chosenClass,panneauOuvert:f?.dataset.mode=='tour',fiche:f&&!f.hidden?f.innerText:'',choix:typeof sel!='undefined'?sel:null,monstre:typeof mon!='undefined'?mon:null,
 projet:typeof projet!='undefined'&&projet?{...projet}:null,toast:document.getElementById('toast').hidden?'':document.getElementById('toast').textContent,boutons:[...document.querySelectorAll('#fiche .actions button')].map(b=>b.textContent)}})}
/* 2.15 : toucher la carte d'une tour ou d'un monstre par son nom (les cartes n'affichent que l'icône et le prix ; le nom est dans aria-label) */
async function toucherCarte(page,nom){await toucher(page,`#bar button[aria-label^="${nom},"]`)}

/* 2.7 : attend que le rendu 3D soit prêt (module chargé et modèles préchargés). Le chargement passe par le réseau local,
   qui ne dépend pas de l'horloge figée : on attend en temps réel, puis on avance l'horloge d'une image. */
async function attendre3D(page,ms=30000){const fin=Date.now()+ms;
 while(Date.now()<fin){const e=await page.evaluate(()=>({ok:!!(window.R3D_ETAT&&R3D_ETAT().charge),echec:window.R3D_ETAT&&R3D_ETAT().echec}));
  if(e.ok){await page.clock.runFor(50);return true}if(e.echec)return false;await page.waitForTimeout(100)}return false}
module.exports={disponible,lancer,ouvrir,attendre3D,toucherCase,construire,glisser,centreCase,deuxDoigts,toucher,toucherCarte,avancer,etat,FORMATS};
