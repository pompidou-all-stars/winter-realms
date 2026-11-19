/* Winter Realms — bibliothèque sonore (2.13). Lit assets/audio/manifeste.json et joue les fichiers générés avec ElevenLabs.
   Indépendant de la simulation : la page appelle SON.joue(id) ; si le fichier n'est pas (encore) chargé, la fonction rend false
   et la page joue le son synthétisé d'origine. Rien ne bloque le jeu : chargements et décodages sont asynchrones.
   Désactivable avec ?son=synth dans l'adresse (retour aux seuls sons synthétisés). */
(function(){
'use strict';
const ACTIF=!/[?&]son=synth\b/.test(location.search);
const MAX_VOIES=10;          // sons simultanés au plus (hors voix et ambiances)
const ECART_MIN=60;          // ms minimum entre deux lectures du même son
const VOL={effets:.9,voix:1,ambiance:.5};
let AC=null,sortie=null,bus={},manif=null,etat='rien';
const tampons={},enCours={},dernier={},derniereVariante={};
let voies=[],voixEnCours=null;

function init(ctx,dest){
 if(!ACTIF||AC||!ctx)return;AC=ctx;sortie=dest||ctx.destination;
 for(const k of ['effets','voix','ambiance']){const g=AC.createGain();g.gain.value=VOL[k];g.connect(sortie);bus[k]=g}
 if(etat=='rien'){etat='charge';
  fetch('assets/audio/manifeste.json').then(r=>r.ok?r.json():null).then(m=>{manif=m&&m.sons?m:null;etat=manif?'pret':'absent'}).catch(()=>{etat='absent'})}}

/* mise à niveau au chargement : crête ramenée à -3 dB (gain plafonné à ×2 depuis la 2.28 : au-delà, le souffle remontait), silences du début (10 ms gardées)
   et de la fin (50 ms gardées) coupés, pour qu'un son parte au moment de l'action.
   Les ambiances en boucle ne sont pas touchées (la boucle doit rester exacte). */
function nettoyer(buf,id){if(!buf||id.startsWith('amb-'))return buf;
 const n=buf.length,ch=buf.numberOfChannels,sr=buf.sampleRate;let pk=0,a=n,z=0;const seuil=Math.pow(10,-45/20);
 for(let c=0;c<ch;c++){const d=buf.getChannelData(c);for(let i=0;i<n;i++){const v=Math.abs(d[i]);if(v>pk)pk=v;if(v>seuil){if(i<a)a=i;if(i>z)z=i}}}
 if(pk<1e-4||a>=n)return null;const g=Math.min(2,Math.pow(10,-3/20)/pk),deb=Math.max(0,a-Math.round(sr*.01)),fin=Math.min(n,z+Math.round(sr*.05)+1);
 const b=AC.createBuffer(ch,fin-deb,sr);
 for(let c=0;c<ch;c++){const s=buf.getChannelData(c),d=b.getChannelData(c);for(let i=deb;i<fin;i++)d[i-deb]=s[i]*g}
 return b}

/* charge (une fois) toutes les variantes d'un son ; ne rejette jamais */
function charger(id){
 if(!manif||!AC||tampons[id]||enCours[id])return enCours[id]||Promise.resolve(tampons[id]);
 const fichiers=manif.sons[id];if(!fichiers||!fichiers.length)return Promise.resolve(null);
 enCours[id]=Promise.all(fichiers.map(f=>fetch('assets/audio/'+f).then(r=>r.ok?r.arrayBuffer():null)
  .then(b=>b?new Promise(ok=>{try{const p=AC.decodeAudioData(b,ok,()=>ok(null));if(p&&p.catch)p.catch(()=>ok(null))}catch(e){ok(null)}}):null).catch(()=>null)))
  .then(l=>{l=l.map(b=>nettoyer(b,id)).filter(Boolean);if(l.length)tampons[id]=l;delete enCours[id];return tampons[id]||null});
 return enCours[id]}

/* précharge une liste d'identifiants ou de préfixes (« tir-*-nains ») */
function precharge(motifs){
 const go=()=>{if(!manif)return;const ids=Object.keys(manif.sons);
  for(const m of motifs){const re=new RegExp('^'+m.replace(/[.+?^${}()|[\]\\]/g,'\\$&').replace(/\*/g,'.*')+'$');for(const id of ids)if(re.test(id))charger(id)}};
 if(etat=='pret')go();else if(etat=='charge'){const t=setInterval(()=>{if(etat!='charge'){clearInterval(t);go()}},200)}}

function variante(id){const l=tampons[id];if(l.length==1)return l[0];
 let i;do i=Math.floor(Math.random()*l.length);while(i===derniereVariante[id]);derniereVariante[id]=i;return l[i]}

function lire(buf,canal,vol,boucle){
 const s=AC.createBufferSource(),g=AC.createGain();s.buffer=buf;s.loop=!!boucle;
 s.playbackRate.value=boucle?1:.96+Math.random()*.08;   // légère variation de hauteur contre la répétition
 g.gain.value=vol;s.connect(g);g.connect(bus[canal]);s.start();return {s,g}}

/* joue un bruitage ; rend true s'il a été joué (ou volontairement filtré), false si la page doit utiliser la synthèse */
function joue(id,o){
 if(!AC||!manif||!manif.sons[id])return false;
 if(!tampons[id]){charger(id);return false}
 const now=performance.now();o=o||{};
 if(now-(dernier[id]||0)<(o.ecart||ECART_MIN))return true;dernier[id]=now;
 voies=voies.filter(v=>v.fin>now);
 if(voies.length>=MAX_VOIES){const p=o.prio||1,faible=voies.reduce((a,v)=>v.prio<a.prio?v:a,voies[0]);
  if(faible.prio>p)return true;try{faible.s.stop()}catch(e){}voies.splice(voies.indexOf(faible),1)}
 const buf=variante(id),v=lire(buf,'effets',o.vol==null?1:o.vol);v.prio=o.prio||1;v.fin=now+buf.duration*1000;voies.push(v);return true}

/* répliques : une seule voix à la fois, avec un délai propre à chaque contexte */
const delaiVoix={};
function voix(faction,ctx,ecart){
 const id='voix-'+faction+'-'+ctx;if(!AC||!manif||!manif.sons[id])return false;
 if(!tampons[id]){charger(id);return false}
 const now=performance.now();if(now-(delaiVoix[ctx]||0)<(ecart||0))return true;
 if(voixEnCours&&voixEnCours.fin>now){if(ctx!='sel'&&ctx!='agace')return true;try{voixEnCours.s.stop()}catch(e){}}
 delaiVoix[ctx]=now;const buf=variante(id),v=lire(buf,'voix',1);v.fin=now+buf.duration*1000;voixEnCours=v;return true}

/* ambiances en boucle, en fondu */
const amb={};
function ambiance(id,vol){
 if(!AC||!manif)return;const a=amb[id];
 if(vol<=0){if(a){a.g.gain.setTargetAtTime(0,AC.currentTime,.6);const s=a.s;setTimeout(()=>{try{s.stop()}catch(e){}},3000);delete amb[id]}return}
 if(a){a.g.gain.setTargetAtTime(vol,AC.currentTime,.6);return}
 charger(id).then(l=>{if(!l||amb[id])return;const v=lire(l[0],'ambiance',0,true);v.g.gain.setTargetAtTime(vol,AC.currentTime,1.2);amb[id]=v})}

function volume(canal,v){VOL[canal]=v;if(bus[canal])bus[canal].gain.value=v}

window.SON={actif:ACTIF,init,joue,voix,ambiance,precharge,volume,charger,
 etat:()=>({etat,ids:manif?Object.keys(manif.sons).length:0,charges:Object.keys(tampons).length,voies:voies.length})};
})();
