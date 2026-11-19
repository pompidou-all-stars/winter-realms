/* Winter Realms — serveur multijoueur (Cloudflare Worker + Durable Objects, plan gratuit).
   Le Worker redirige chaque salon vers son Durable Object « GameRoom ».
   Le GameRoom gère le salon (sièges, factions, chef), puis fait tourner la partie avec sim.js
   (la même simulation que le solo) et envoie un instantané à tous les joueurs 10 fois par seconde. */
import sim from '../../sim.js';
const {Game,FACTIONS,DIFF}=sim;

/* pages autorisées à se connecter (null = fichier ouvert en local) */
const ORIGINS=['https://pompidou-all-stars.github.io','http://localhost:8000','http://localhost:8080','http://127.0.0.1:8080','null'];
const SEAT_COL=['#f2c14e','#e4572e','#4aa3df','#b06ad0'];
const STEP_MS=50,SNAP_EVERY=2,BACK_TO_LOBBY_MS=8000;

export default {
 async fetch(req,env){
  const url=new URL(req.url),o=req.headers.get('Origin');
  const cors=o&&ORIGINS.includes(o)?{'Access-Control-Allow-Origin':o}:{};
  /* accès réservé à certains pays (ALLOWED_COUNTRIES dans wrangler.toml, vide = tout le monde) */
  const allowed=String(env.ALLOWED_COUNTRIES||'').split(',').map(s=>s.trim()).filter(Boolean),country=req.cf&&req.cf.country;
  if(allowed.length&&!allowed.includes(country))return new Response('Le jeu en ligne est réservé à : '+allowed.join(', '),{status:403,headers:cors});
  if(url.pathname==='/'||url.pathname==='/check')return new Response('Winter Realms : serveur OK',{headers:cors});
  const m=url.pathname.match(/^\/room\/([A-Z0-9]{4})$/);
  if(!m)return new Response('Introuvable',{status:404});
  if(req.headers.get('Upgrade')!=='websocket')return new Response('WebSocket attendu',{status:426});
  if(o&&!ORIGINS.includes(o))return new Response('Origine refusée',{status:403});
  return env.ROOMS.get(env.ROOMS.idFromName(m[1])).fetch(req);
 }
};

const r2=v=>Math.round(v*100)/100;
const clean=(s,n)=>String(s||'').replace(/[\u0000-\u001f<>]/g,'').trim().slice(0,n);

export class GameRoom{
 constructor(ctx){this.ctx=ctx;
  this.clients=new Set();           // {ws, token, name, seat}
  this.seats=[null,null,null,null]; // {token, name, f} pour chaque humain assis
  this.leader=null;                 // jeton du chef de salon
  this.lv=0;this.game=null;this.timer=null;this.last=0;this.n=0;this.back=null}

 async fetch(req){
  const [client,ws]=Object.values(new WebSocketPair());ws.accept();
  const cl={ws,token:null,name:'',seat:-1};this.clients.add(cl);
  ws.addEventListener('message',e=>{let m;try{m=JSON.parse(e.data)}catch(_){return}try{this.onMsg(cl,m)}catch(err){console.log('msg',err)}});
  const bye=()=>{if(this.clients.delete(cl))this.onLeave(cl)};
  ws.addEventListener('close',bye);ws.addEventListener('error',bye);
  return new Response(null,{status:101,webSocket:client});
 }

 put(cl,m){try{cl.ws.send(JSON.stringify(m))}catch(_){}}
 all(m){const s=JSON.stringify(m);for(const cl of this.clients)try{cl.ws.send(s)}catch(_){}}
 online(token){for(const cl of this.clients)if(cl.token===token)return true;return false}

 lobby(){const seats=this.seats.map(s=>s?{name:s.name,f:s.f,online:this.online(s.token)}:null);
  for(const cl of this.clients)this.put(cl,{t:'lobby',seats,lv:this.lv,you:cl.seat,leader:cl.token===this.leader,playing:!!this.game})}

 onMsg(cl,m){
  if(m.t==='hello'){
   cl.token=clean(m.token,40);cl.name=clean(m.name,16)||'Joueur';if(!cl.token){cl.ws.close();return}
   for(const o of this.clients)if(o!==cl&&o.token===cl.token){o.token=null;try{o.ws.close()}catch(_){}} // même joueur, nouvel onglet
   let i=this.seats.findIndex(s=>s&&s.token===cl.token);
   if(i<0&&!this.game){i=this.seats.findIndex(s=>!s);if(i>=0){const used=this.seats.filter(Boolean).map(s=>s.f);const f=[0,1,2,3,4].find(x=>!used.includes(x));this.seats[i]={token:cl.token,name:cl.name,f:f??0}}}
   cl.seat=i;if(i>=0)this.seats[i].name=cl.name;
   if(!this.leader||!this.online(this.leader))this.leader=cl.token;
   this.lobby();
   if(this.game){this.put(cl,this.startMsg(cl));this.put(cl,this.snap(true))}
   return}
  if(!cl.token)return;
  const lead=cl.token===this.leader;
  if(m.t==='faction'&&!this.game&&cl.seat>=0){const f=m.f|0;if(f>=0&&f<FACTIONS.length){this.seats[cl.seat].f=f;this.lobby()}return}
  if(m.t==='diff'&&lead&&!this.game){const lv=m.lv|0;if(lv>=0&&lv<DIFF.length){this.lv=lv;this.lobby()}return}
  if(m.t==='start'&&lead&&!this.game){this.start();return}
  if(m.t==='act'&&this.game&&cl.seat>=0){const err=this.game.action(cl.seat,m.a);this.put(cl,{t:'res',err,a:m.a,q:m.q?1:0});return}
 }

 onLeave(cl){
  if(!this.game&&cl.seat>=0&&this.seats[cl.seat]&&this.seats[cl.seat].token===cl.token&&!this.online(cl.token))this.seats[cl.seat]=null;
  if(cl.token===this.leader&&!this.online(this.leader)){const o=[...this.clients].find(c=>c.token);this.leader=o?o.token:null}
  if(!this.clients.size){this.stop();this.seats=[null,null,null,null];this.leader=null;return}
  this.lobby()}

 /* IA sur les sièges vides : de préférence les factions que personne n'a prises */
 start(){const humans=this.seats.filter(Boolean);if(!humans.length)return;
  const free=[0,1,2,3,4].filter(f=>!humans.some(s=>s.f===f));let k=0;
  this.gseats=this.seats.map((s,i)=>s?{name:s.name,col:SEAT_COL[i],ai:0,classId:s.f}:{name:'IA '+(i+1),col:SEAT_COL[i],ai:1,classId:free.length?free[k++%free.length]:(i%5)});
  this.game=new Game(this.gseats,this.lv);this.n=0;this.last=Date.now();
  for(const cl of this.clients)this.put(cl,this.startMsg(cl));
  this.timer=setInterval(()=>this.step(),STEP_MS)}
 startMsg(cl){return {t:'start',seats:this.gseats,lv:this.lv,you:cl.seat}}
 stop(){if(this.timer)clearInterval(this.timer);this.timer=null;if(this.back)clearTimeout(this.back);this.back=null;this.game=null}

 step(){const g=this.game;if(!g)return;const now=Date.now();let dt=Math.min(.25,(now-this.last)/1000);this.last=now;
  while(dt>0&&!g.over){const s=Math.min(.05,dt);g.step(s);dt-=s}
  this.n++;
  if(g.over||this.n%SNAP_EVERY===0||g.log.length)this.all(this.snap(false));
  if(g.over){clearInterval(this.timer);this.timer=null;
   this.back=setTimeout(()=>{this.back=null;this.game=null;for(let i=0;i<4;i++)if(this.seats[i]&&!this.online(this.seats[i].token))this.seats[i]=null;this.lobby()},BACK_TO_LOBBY_MS)}}

 /* instantané : tout ce qu'il faut pour dessiner les 4 terrains (positions arrondies au centième) */
 snap(full){const g=this.game;
  /* 2.38 : quête bonus en cours (scores en direct) ; son début et sa fin passent par log */
  const q=g.qu;
  return {t:'snap',time:r2(g.time),tick:r2(g.tick),qu:q?{id:q.id,t0:r2(q.t0),fin:r2(q.fin),or:q.or,cible:q.cible,sc:q.sc}:null,log:full?[]:g.log.splice(0),B:g.B.map(b=>({gold:Math.floor(b.gold),inc:b.inc,lives:b.lives,dead:b.dead,tier:b.tier,
   t:b.t.map(t=>[t.x,t.y,t.k,t.lv,t.inv,r2(t.a),t.sw>0?1:0,t.stun>0?1:0,t.b>0?r2(t.b):0,t.b>0?r2(t.bt):0]),
   c:b.cr.map(c=>[c.id,c.k,r2(c.x),r2(c.y),r2(Math.max(0,c.hp/c.max)),(c.sl>0?1:0)|(c.h?2:0)|(c.hl?4:0)|(c.hid?8:0),c.f,r2(c.ph),r2(c.ox),r2(c.oy)]),
   p:b.pr.map(p=>[p.id,p.k,r2(p.x),r2(p.y),r2(p.tx),r2(p.ty),r2(p.tot),r2(p.a)]),
   fx:full?[]:b.fx.filter(f=>!f.s).map(f=>{f.s=1;const o={};for(const k in f)if(k!=='s')o[k]=typeof f[k]=='number'?r2(f[k]):f[k];return o}),
   ev:full?[]:b.ev.splice(0)}))}}
}
