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
async function lancer(){return playwright.chromium.launch({args:OPTIONS_STABLES})}

/* ouvre le jeu ; options : format, graine, police ('reelle' ou 'bloquee'), echelle (densité de pixels) */
async function ouvrir(navigateur,url,{format='portrait',graine=12345,police='reelle',echelle=2}={}){
 const ctx=await navigateur.newContext({...FORMATS[format],deviceScaleFactor:echelle,isMobile:true,hasTouch:true,locale:'fr-FR',timezoneId:'Europe/Paris',reducedMotion:'no-preference'});
 const page=await ctx.newPage();
 const erreurs=[];page.on('pageerror',e=>erreurs.push(e.message));page.on('console',m=>{if(m.type()=='error')erreurs.push(m.text())});
 /* aucune connexion vers l'extérieur, sauf la police si demandée (le multijoueur n'est jamais contacté) */
 await page.route(u=>!u.href.startsWith(url),r=>{const h=new URL(r.request().url()).hostname;
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
    on l'aligne sur exactement 200 ms pour que les animations (chemin, portail, barre de revenu) soient identiques à chaque passage */
 const pn=await page.evaluate(()=>performance.now());await page.clock.runFor(200-pn);
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
async function avancer(page,ms){await page.clock.runFor(ms)}
async function etat(page){return page.evaluate(()=>({or:P.gold,revenu:P.inc,vies:P.lives,tours:P.t.map(t=>({x:t.x,y:t.y,k:t.k,lv:t.lv})),temps:time,horloge:document.getElementById('clock').textContent,
 vue:view,fin:over,faction:chosenClass,panneauOuvert:!!document.querySelector('#bar .info')||document.getElementById('fiche')?.dataset.mode=='tour',fiche:document.getElementById('fiche')?.innerText||'',zoom:typeof VUE=='object'?VUE.z:1,projet:typeof projet!='undefined'&&projet?{...projet}:null,toast:document.getElementById('toast').hidden?'':document.getElementById('toast').textContent,boutons:[...document.querySelectorAll('#bar button')].map(b=>b.textContent)}))}

module.exports={disponible,lancer,ouvrir,toucherCase,construire,glisser,centreCase,deuxDoigts,toucher,avancer,etat,FORMATS};
