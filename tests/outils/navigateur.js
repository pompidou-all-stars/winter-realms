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
 return {ctx,page,erreurs,policeChargee,fermer:()=>ctx.close()};
}

/* toucher le centre d'une case du terrain */
async function toucherCase(page,x,y){const b=await page.locator('#main').boundingBox();
 await page.touchscreen.tap(b.x+(x+.5)*b.width/13,b.y+(y+.5)*b.height/17);await page.clock.runFor(50)}
async function toucher(page,selecteur){await page.locator(selecteur).first().tap();await page.clock.runFor(50)}
async function avancer(page,ms){await page.clock.runFor(ms)}
async function etat(page){return page.evaluate(()=>({or:P.gold,revenu:P.inc,vies:P.lives,tours:P.t.map(t=>({x:t.x,y:t.y,k:t.k,lv:t.lv})),temps:time,horloge:document.getElementById('clock').textContent,
 vue:view,fin:over,faction:chosenClass,panneauOuvert:!!document.querySelector('#bar .info'),boutons:[...document.querySelectorAll('#bar button')].map(b=>b.textContent)}))}

module.exports={disponible,lancer,ouvrir,toucherCase,toucher,avancer,etat,FORMATS};
