/* Winter Realms — simulation partagée (navigateur + serveur). Aucun accès au DOM ni au son ici. */
const C=13,R=17,SP=[6,0],EX=[6,16],DIRS=[[1,0],[-1,0],[0,1],[0,-1]],INF=1e9,OUT='#2b1d12';
const BASE_TW=[
 {n:'Archer',c:20,r:2.8,d:8,cd:.5,ps:10,col:'#6aa84f',s:'arrow'},
 {n:'Canon',c:50,r:2.5,d:20,cd:1.2,ps:6.5,sp:1.1,gr:1,col:'#b0703a',s:'canon',tag:'sol'},
 {n:'Givre',c:40,r:2.5,d:4,cd:.9,ps:8,sl:1.5,fsp:1.2,mag:1,col:'#3d85c6',s:'frost',tag:'magie · zone'},
 {n:'Mage',c:90,r:3.2,d:45,cd:1.4,ps:7.5,mg:1,mag:1,col:'#8e44ad',s:'mage',tag:'magie · détecte'},
 {n:'Garde',c:30,r:1.5,d:20,cd:.55,me:1,gr:1,col:'#c0392b',s:'slash',tag:'sol'},
 {n:'Flammes',c:70,r:2,d:3,cd:.12,fl:1,col:'#e67e22',s:'flame'}];
const FACTIONS=[
 {name:'Alliance',icon:'🛡️',color:'#d8b45c',dark:'#59451f',desc:'Portée supérieure et maîtrise des airs ; dégâts directs légèrement plus modestes.', towers:['Tour des archers','Bastion du chevalier','Obélisque de givre','Bombarde royale','Brasier du griffon','Sanctuaire solaire','Tour des sentinelles','Garde du lion','Cristal hivernal','Arcaniste royal']},
 {name:'Horde',icon:'🪓',color:'#78a94b',dark:'#294322',desc:'Assauts agressifs et exécution des ennemis affaiblis ; portée plus courte.', towers:['Tour des chasseurs','Totem du berserker','Totem de glace','Canon des clans','Fourneau de guerre','Chaman des flammes','Tour des éclaireurs','Garde-lame','Totem des esprits','Grand sorcier orc']},
 {name:'Sylvestres',icon:'🌿',color:'#69bd83',dark:'#214b38',desc:'Racines qui ralentissent et contrôlent les vagues ; dégâts bruts plus faibles.', towers:['Arbre sentinelle','Gardien des racines','Pierre de rosée','Fleur explosive','Cœur ardent','Cercle druidique','Nid des faucons','Dryade protectrice','Cristal lunaire','Ancien arcanique']},
 {name:'Nains',icon:'⚒️',color:'#c58b55',dark:'#56351f',desc:'Artillerie perforante contre les blindés ; cadence plus lente et tours coûteuses.', towers:['Tourelle de guet','Automate garde','Cryo-forge','Mortier runique','Forge incandescente','Canon arcanique','Baliste naine','Sentinelle d’acier','Générateur runique','Maître ingénieur']},
 {name:'Légion des ombres',icon:'☠️',color:'#a879c9',dark:'#39204d',desc:'Marque les cibles pour amplifier les frappes suivantes ; profil polyvalent sans extrême.', towers:['Tour des damnés','Chevalier funeste','Obélisque maudit','Mortier infernal','Puits de lave','Nexus du néant','Œil démoniaque','Gardien spectral','Cristal corrupteur','Archimage noir']}
];
const ARCH=[0,4,2,1,5,3,0,4,2,3];
/* Coefficients volontairement proches en rendement global : chaque avantage a une vraie contrepartie. */
const FACTION_BALANCE=[
 {cost:1.04,dmg:.97,range:1.10,cd:1.03,airBonus:1.18,tag:'anti-aérien'},
 {cost:1.02,dmg:.96,range:.93,cd:1.04,execute:1.30,tag:'frénésie'},
 {cost:1.00,dmg:.96,range:1.00,cd:1.02,root:.72,rootFactor:.82,tag:'racines'},
 {cost:1.07,dmg:1.08,range:1.02,cd:1.08,pierce:.55,tag:'perforant'},
 {cost:1.01,dmg:1.01,range:.99,cd:1.01,mark:1.14,tag:'malédiction'}
];
const ROLE=[
 {name:'Tir rapide',tag:'cadence'}, {name:'Garde rapprochée',tag:'corps-à-corps'},
 {name:'Contrôle',tag:'ralentit'}, {name:'Artillerie',tag:'zone'},
 {name:'Dégâts continus',tag:'zone courte'}, {name:'Arcanes',tag:'détection'},
 {name:'Tireur d’élite',tag:'longue portée'}, {name:'Champion',tag:'frappe lourde'},
 {name:'Entrave',tag:'contrôle renforcé'}, {name:'Archimage',tag:'dégâts élevés'}
];
const TW=FACTIONS.flatMap((F,fi)=>F.towers.map((name,j)=>{
 const base=BASE_TW[ARCH[j]],scale=[1,1.08,.96,1.12,1.18,.92,1.22,1.30,1.16,1.38][j],bal=FACTION_BALANCE[fi];
 const late=j>=6,role=ROLE[j];
 return {...base,n:name,c:Math.max(10,Math.round(base.c*scale*bal.cost/5)*5),
  d:+(base.d*scale*bal.dmg*(late&&j==6?.88:late&&j==7?1.08:late&&j==8?.9:late&&j==9?1.08:1)).toFixed(1),
  cd:+(base.cd*bal.cd*(late&&j==6?.86:late&&j==7?1.12:1)).toFixed(3),
  r:+(base.r*bal.range*(late&&j==6?1.12:late&&j==9?1.08:1)).toFixed(2),
  sl:Math.max(base.sl||0,bal.root||0),sf:bal.rootFactor||base.sf||.5,
  airBonus:bal.airBonus||0,execute:bal.execute||0,pierce:bal.pierce||0,mark:bal.mark||0,
  col:F.color,skin:ARCH[j],faction:fi,role:role.name,tag:bal.tag+' · '+role.tag};
}));
const ORDER=Array.from({length:10},(_,i)=>i);
/* cat : n = sol, f = volant, s = spécial. Revenu des monstres au sol sur une courbe croissante (10 → 1, 100 → 11, 1000 → 120). */
const CR=[
 {n:'Sapeur gobelin',cat:'n',c:10,hp:12,s:1.6,z:.75,g:'gob',col:'#8fce5a'},
 {n:'Warg',cat:'n',c:20,hp:22,s:2.4,z:.78,g:'wolf',col:'#9aa3ad'},
 {n:'Brute orc',cat:'n',c:65,hp:82,s:1.4,z:.95,g:'orc',col:'#5f9c45'},
 {n:'Troll des glaces',cat:'n',c:120,hp:160,s:1.5,z:1.1,g:'troll',col:'#57aeb0'},
 {n:'Golem runique',cat:'n',c:300,hp:420,s:1,z:1.2,g:'golem',col:'#9a9ca6'},
 {n:'Cyclope des cendres',cat:'n',c:1000,hp:1500,s:1.1,z:1.5,g:'cyc',col:'#dba878'},
 {n:'Chauve-souris',cat:'f',c:30,hp:16,s:2,z:.75,g:'bat',fly:1,col:'#7d5ba6'},
 {n:'Griffon corrompu',cat:'f',c:150,hp:95,s:1.9,z:1,g:'griffon',fly:1,col:'#d9a441'},
 {n:'Dragon ancien',cat:'f',c:450,hp:400,s:1.3,z:1.3,g:'dragon',fly:1,col:'#d6453d'},
 {n:'Chaman de guerre',cat:'s',c:80,hp:70,s:1.5,z:.85,g:'chaman',aura:1,col:'#e8b23a',tag:'hâte'},
 {n:'Prêtresse',cat:'s',c:100,hp:80,s:1.4,z:.85,g:'healer',heal:1,col:'#6fcf97',tag:'soin'},
 {n:'Gelée mutante',cat:'s',c:140,hp:90,s:1.3,z:.95,g:'slime',split:1,col:'#b5e04a',tag:'se divise'},
 {n:'Tortue',cat:'s',c:180,hp:150,s:1.1,z:1,g:'turtle',arm:5,at:90,col:'#8a6a3a',tag:'blindée'},
 {n:'Briseur de runes',cat:'s',c:200,hp:130,s:1.4,z:1,g:'breaker',mi:1,at:120,col:'#b9c0c9',tag:'anti-magie'},
 {n:'Spectre',cat:'s',c:200,hp:110,s:1.5,z:.9,g:'spectre',inv:1,at:180,col:'#d7defa',tag:'invisible'},
 {n:'Saboteur gobelin',cat:'s',c:260,hp:120,s:1.5,z:.85,g:'sapper',stun:1,at:240,col:'#8fce5a',tag:'étourdit'},
 {n:"Azh’Khar, seigneur des lames",cat:'s',c:900,hp:1900,s:1.02,z:1.35,g:'hero',arm:4,stun:1,at:360,hero:1,col:'#a77cff',tag:'HÉROS · étourdit · boss'},
 {n:'Petit limon',cat:'x',c:20,hp:35,s:1.6,z:.6,g:'slime',col:'#b5e04a'}];
for(const T of CR)T.i=T.cat=='n'?Math.round(T.c/10*(1+.1*Math.log10(T.c/10))):Math.round(T.c*.065);
const byCat=c=>CR.map((T,k)=>k).filter(k=>CR[k].cat==c).sort((a,b)=>CR[a].c-CR[b].c),NORM=byCat('n'),FLY=byCat('f'),idx=f=>CR.findIndex(T=>T[f]),AURA=idx('aura'),SPEC=idx('inv'),HEAL=idx('heal'),SPLIT=idx('split'),TURT=idx('arm'),BRK=idx('mi'),SAP=idx('stun'),KID=CR.findIndex(T=>T.cat=='x'),AURA_R=1.7;
const DIFF=[{n:'Normal',b:1,g:0},{n:'Difficile',b:1.25,g:30},{n:'Brutal',b:1.5,g:60}];
const HPK=.55,GRACE=25,GROUP=4,
/* temps de construction : 1 s pour BUILD_OR pièces d'or dépensées (achat ou amélioration), entre BUILD_MIN et BUILD_MAX secondes */
 BUILD_OR=30,BUILD_MIN=1,BUILD_MAX=12,buildT=c=>Math.min(BUILD_MAX,Math.max(BUILD_MIN,c/BUILD_OR)),flyH=k=>CR[k].fly?CR[k].z*.35:0;
const dmg=t=>TW[t.k].d*2**(t.lv-1),rng=t=>TW[t.k].r*(1+.05*(t.lv-1)),upCost=t=>Math.round(TW[t.k].c*1.5*2**(t.lv-1)/5)*5,topY=t=>.28+.045*(t.lv-1);

/* ---------- simulation ---------- */
class Board{
 constructor(i,name,col,ai,classId=0){this.i=i;this.name=name;this.col=col;this.ai=ai;this.classId=classId;this.dead=0;this.aiT=1+i*.2;this.ev=[];this.G=null;
  this.g=Array.from({length:R},()=>Array(C).fill(0));this.t=[];this.cr=[];this.pr=[];this.fx=[];this.q=[];this.gold=100;this.inc=10;this.lives=40;this.hurt=0;this.pen=0;this.dp=60;this.ap=40;this.lastG=100;this.d=this.dist()}
 dist(){const d=Array.from({length:R},()=>Array(C).fill(INF)),q=[[EX[0],EX[1]]];d[EX[1]][EX[0]]=0;
  for(let i=0;i<q.length;i++){const[x,y]=q[i];for(const[dx,dy]of DIRS){const a=x+dx,b=y+dy;if(a<0||b<0||a>=C||b>=R||this.g[b][a]||d[b][a]<INF)continue;d[b][a]=d[y][x]+1;q.push([a,b])}}return d}
 place(x,y,k){const T=TW[k];
  if(Math.floor(k/10)!==this.classId)return false;
  if(x<0||y<0||x>=C||y>=R||this.gold<T.c||this.g[y][x]||(x==SP[0]&&y==SP[1])||(x==EX[0]&&y==EX[1]))return false;
  if(this.cr.some(c=>!CR[c.k].fly&&((Math.abs(c.x-x)<.9&&Math.abs(c.y-y)<.9)||(c.tx==x&&c.ty==y))))return false;
  this.g[y][x]=1;const nd=this.dist();
  if(nd[SP[1]][SP[0]]>=INF||this.cr.some(c=>!CR[c.k].fly&&nd[c.ty][c.tx]>=INF)){this.g[y][x]=0;return false}
  this.d=nd;this.gold-=T.c;const bt=buildT(T.c);this.t.push({x,y,k,cd:0,a:.7,lv:1,inv:T.c,sw:0,b:bt,bt});
  this.fx.push({type:'range',x:x+.5,y:y+.5,r:T.r,t:.6,d:.6,col:T.col});this.ev.push('build');return true}
 sell(x,y){const i=this.t.findIndex(t=>t.x==x&&t.y==y);if(i<0)return false;const b=Math.floor(this.t[i].inv*.7);this.gold+=b;this.t.splice(i,1);this.g[y][x]=0;this.d=this.dist();
  this.fx.push({type:'text',x:x+.5,y:y+.4,txt:'+'+b,col:'#ffd95e',t:.7,d:.7});this.ev.push('sell');return true}
 upgrade(t){const c=upCost(t);if(t.lv>=5||t.b>0||this.gold<c)return false;this.gold-=c;t.inv+=c;t.lv++;t.b=t.bt=buildT(c);
  this.fx.push({type:'text',x:t.x+.5,y:t.y,txt:'Niveau '+t.lv,col:'#ffd95e',t:.9,d:.9},{type:'range',x:t.x+.5,y:t.y+.5,r:rng(t),t:.6,d:.6,col:TW[t.k].col});this.ev.push('up');return true}
 send(k,m){for(let i=0;i<GROUP;i++)this.q.push({k,m,t:i*.38+Math.random()*.25})}
 /* dégâts : l'anti-magie ignore Mage et Givre, la carapace retire un montant fixe à chaque coup */
 hit(c,d,T,sf){
  if(T.mag&&CR[c.k].mi)return;
  if(T.airBonus&&CR[c.k].fly)d*=T.airBonus;
  if(T.execute&&c.hp/c.max<.35)d*=T.execute;
  if(T.mark){if((c.mark||0)>0)d*=T.mark;c.mark=1.35}
  if(c.arm){const armor=c.arm*(1-(T.pierce||0));d=Math.max(d*.2,d-armor)}
  c.hp-=d;
  /* ralentissement : le Givre garde son facteur selon le niveau ; les racines sylvestres (autres tours) appliquent T.sf (.82). Un ralentissement plus faible n'écrase jamais un plus fort en cours. */
  if(T.sl){const f=T.fsp?(sf||.5):T.sf;c.sf=c.sl>0?Math.min(c.sf||1,f):f;c.sl=Math.max(c.sl||0,T.sl)}
 }
 impact(p){const T=TW[p.k],tg=p.tg,rad=T.sp||T.fsp;
  if(!tg.dead&&!tg.leak)this.hit(tg,p.d,T,p.sf);
  if(rad){for(const c of this.cr){if(c===tg||c.hid||(T.gr&&CR[c.k].fly)||Math.hypot(c.x+.5-p.tx,c.y+.5-flyH(c.k)-p.ty)>=rad)continue;this.hit(c,p.d*.6,T,p.sf)}
   this.fx.push({type:'boom',x:p.tx,y:p.ty,r:rad,t:.3,d:.3,col:T.sl?'#8fdcff':'#ffb347'});if(T.sp)this.ev.push('boom')}
  else this.fx.push({type:'ring',x:p.tx,y:p.ty,r:T.skin==3?.45:.26,t:.2,d:.2,col:T.skin==0?'#ffffff':'#e39bff'})}
 update(dt){
  this.hurt=Math.max(0,this.hurt-dt);
  for(const s of this.q){s.t-=dt;if(s.t<=0){const hp=CR[s.k].hp*s.m*HPK;this.cr.push({id:++UID,k:s.k,x:SP[0],y:SP[1],tx:SP[0],ty:SP[1],hp,max:hp,sl:0,sf:.5,f:1,ph:Math.random()*6,ox:(Math.random()-.5)*.3,oy:(Math.random()-.5)*.22,arm:(CR[s.k].arm||0)*s.m,cs:2})}}
  this.q=this.q.filter(s=>s.t>0);
  const au=this.cr.filter(c=>CR[c.k].aura),mg=this.t.filter(t=>TW[t.k].mg&&!(t.b>0)),hl=this.cr.filter(c=>CR[c.k].heal);
  for(const c of this.cr){const T=CR[c.k];c.sl=Math.max(0,c.sl-dt);c.mark=Math.max(0,(c.mark||0)-dt);c.h=!T.aura&&au.some(a=>Math.hypot(a.x-c.x,a.y-c.y)<AURA_R);
   c.hid=T.inv&&!mg.some(m=>Math.hypot(c.x-m.x,c.y-m.y)<=rng(m));
   c.hl=c.hp<c.max&&hl.some(a=>a!==c&&Math.hypot(a.x-c.x,a.y-c.y)<AURA_R);if(c.hl)c.hp=Math.min(c.max,c.hp+c.max*.05*dt);
   if(T.stun){c.cs-=dt;if(c.cs<=0){let bt=null,bd=2.3;for(const t of this.t){const d=Math.hypot(t.x-c.x,t.y-c.y);if(d<bd&&!(t.stun>0)&&!(t.b>0)){bd=d;bt=t}}
    if(bt){bt.stun=2;c.cs=3.5;this.fx.push({type:'zap',x:c.x+.5,y:c.y+.3,x2:bt.x+.5,y2:bt.y+.5-topY(bt),t:.3,d:.3});this.ev.push('zap')}else c.cs=.3}}
   let sp=T.s*(c.sl>0?c.sf:1)*(c.h?1.4:1)*dt;
   if(T.fly){const dx=EX[0]-c.x,dy=EX[1]-c.y,dd=Math.hypot(dx,dy);if(dd<=sp)c.leak=1;else{c.x+=dx/dd*sp;c.y+=dy/dd*sp}continue}
   while(sp>0){const dx=c.tx-c.x,dy=c.ty-c.y,dd=Math.hypot(dx,dy);
    if(dd<1e-4){if(c.tx==EX[0]&&c.ty==EX[1]){c.leak=1;break}
     let best=null,bd=this.d[c.ty][c.tx];
     for(const[ox,oy]of DIRS){const a=c.tx+ox,b=c.ty+oy;if(a<0||b<0||a>=C||b>=R||this.g[b][a])continue;if(this.d[b][a]<bd){bd=this.d[b][a];best=[a,b]}}
     if(!best)break;if(best[0]!=c.tx)c.f=best[0]>c.tx?1:-1;c.tx=best[0];c.ty=best[1];continue}
    const m=Math.min(sp,dd);c.x+=dx/dd*m;c.y+=dy/dd*m;sp-=m}}
  this.pen*=Math.pow(.955,dt);const tot=this.d[SP[1]][SP[0]]||1;
  for(const c of this.cr){const pr=CR[c.k].fly?1-Math.hypot(EX[0]-c.x,EX[1]-c.y)/12:1-(this.d[c.ty][c.tx]+Math.hypot(c.tx-c.x,c.ty-c.y))/tot;if(pr>this.pen)this.pen=pr}
  for(const t of this.t){if(t.b>0){t.b-=dt;if(t.b<=0){t.b=0;t.cd=0;this.fx.push({type:'range',x:t.x+.5,y:t.y+.5,r:rng(t),t:.6,d:.6,col:TW[t.k].col})}continue}
   if(t.stun>0){t.stun-=dt;continue}t.cd-=dt;if(t.sw>0)t.sw-=dt;if(t.cd>0)continue;const T=TW[t.k],r=rng(t),dm=dmg(t);let tg=null,bd=INF;
   for(const c of this.cr){const F=CR[c.k].fly;if(c.hid||(T.gr&&F)||(T.mag&&CR[c.k].mi))continue;if(Math.hypot(c.x-t.x,c.y-t.y)>r)continue;
    const rem=F?Math.hypot(EX[0]-c.x,EX[1]-c.y):this.d[c.ty][c.tx]+Math.hypot(c.tx-c.x,c.ty-c.y);if(rem<bd){bd=rem;tg=c}}
   if(!tg)continue;t.cd=T.cd;t.a=Math.atan2(tg.y-t.y,tg.x-t.x);
   if(T.me){this.hit(tg,dm,T);t.sw=.2;this.fx.push({type:'slash',x:tg.x+.5,y:tg.y+.5,a:t.a,t:.18,d:.18})}
   else if(T.fl){for(const c of this.cr){if(c.hid)continue;const dx=c.x-t.x,dy=c.y-t.y,dd=Math.hypot(dx,dy);if(dd>r)continue;const da=Math.atan2(dy,dx)-t.a;if(dd<.6||Math.abs(Math.atan2(Math.sin(da),Math.cos(da)))<.5)this.hit(c,dm,T)}
    const h=topY(t);for(let i=0;i<2;i++){const a=t.a+(Math.random()-.5)*.5,v=r/.35*(.75+Math.random()*.35);this.fx.push({type:'flame',x:t.x+.5,y:t.y+.5-h,vx:Math.cos(a)*v,vy:Math.sin(a)*v+h/.35,t:.35,d:.35})}}
   else this.pr.push({id:++UID,x:t.x+.5,y:t.y+.5-topY(t),tg,k:t.k,d:dm,sf:.5-.05*(t.lv-1),tx:tg.x+.5,ty:tg.y+.5,tot:Math.hypot(tg.x-t.x,tg.y-t.y)||.1,a:t.a});
   this.ev.push(T.s)}
  for(const p of this.pr){const T=TW[p.k];if(!p.tg.dead&&!p.tg.leak){p.tx=p.tg.x+.5;p.ty=p.tg.y+.5-flyH(p.tg.k)}
   const dx=p.tx-p.x,dy=p.ty-p.y,dd=Math.hypot(dx,dy),m=T.ps*dt;
   if(dd<=m){p.hit=1;this.impact(p)}else{p.x+=dx/dd*m;p.y+=dy/dd*m;p.a=Math.atan2(dy,dx)}}
  this.pr=this.pr.filter(p=>!p.hit);
  const kids=[];
  for(const c of this.cr){
   if(c.leak){this.lives--;this.hurt=6;this.fx.push({type:'text',x:EX[0]+.5,y:EX[1]+.2,txt:'-1 vie',col:'#ff7b6e',t:.9,d:.9});this.ev.push('!leak')}
   else if(c.hp<=0){c.dead=1;const b=Math.max(1,Math.round(CR[c.k].c/10)),fy=flyH(c.k);this.gold+=b;
    this.fx.push({type:'puff',x:c.x+.5,y:c.y+.5-fy,col:CR[c.k].col,t:.35,d:.35},{type:'text',x:c.x+.5,y:c.y+.2-fy,txt:'+'+b,col:'#ffd95e',t:.7,d:.7});this.ev.push('die');
    if(CR[c.k].split){const m=c.max/CR[c.k].hp;for(let i=0;i<2;i++)kids.push({id:++UID,k:KID,x:c.x,y:c.y,tx:c.tx,ty:c.ty,hp:CR[KID].hp*m,max:CR[KID].hp*m,sl:0,sf:.5,f:c.f,ph:Math.random()*6,ox:(i-.5)*.3,oy:(Math.random()-.5)*.2,arm:0,cs:9})}}}
  this.cr=this.cr.filter(c=>!c.dead&&!c.leak).concat(kids);
  for(const f of this.fx){f.t-=dt;if(f.vx!==undefined){f.x+=f.vx*dt;f.y+=f.vy*dt}}this.fx=this.fx.filter(f=>f.t>0)}
}

/* ---------- IA ---------- */
const PLAN=[];for(const y of[8,6,10,4,12,2,14])for(const x of((y/2)%2?[6,5,7,4,8,3,9,2,10,1,11,0,12]:[6,7,5,8,4,9,3,10,2,11,1,12,0]))PLAN.push([x,y]);
const invest=b=>b.t.reduce((s,t)=>s+t.inv,0),airInv=b=>b.t.reduce((s,t)=>s+(!TW[t.k].gr&&Math.abs(t.x-6)<=2?t.inv:0),0),mages=b=>b.t.filter(t=>TW[t.k].mg).length;
function pathCells(b){const out=[];let x=SP[0],y=SP[1];out.push([x,y]);for(let n=0;n<200&&b.d[y][x]>0&&b.d[y][x]<INF;n++){for(const[dx,dy]of DIRS){const a=x+dx,c=y+dy;if(a>=0&&c>=0&&a<C&&c<R&&b.d[c][a]==b.d[y][x]-1){x=a;y=c;break}}out.push([x,y])}return out}
/* Chaque pièce gagnée est répartie entre deux bourses, défense et attaque, selon la pression subie (pen = jusqu'où les monstres avancent chez elle). */
function aiDefend(A){const time=A.G.time,bud=Math.min(A.dp,A.gold),g0=A.gold,free=PLAN.filter(([x,y])=>!A.g[y][x]),ups=A.t.filter(t=>t.lv<5&&!(t.b>0)&&bud>=upCost(t)),n=A.t.length,cnt=k=>A.t.filter(t=>t.k==k).length;let ok=false;
 if(time>140&&mages(A)<Math.min(5,2+Math.floor(time/300))){const c=A.t.filter(t=>!TW[t.k].mg&&!(t.b>0)&&t.lv<=2&&Math.abs(t.x-6)<=3&&bud>=90-Math.floor(t.inv*.7));
  if(c.length){const t=c[Math.floor(Math.random()*c.length)];const mc=TW[A.classId*10+5].c-Math.floor(t.inv*.7);if(A.gold<mc)return false;A.gold-=mc;t.k=A.classId*10+5;t.lv=1;t.inv=TW[t.k].c;t.b=t.bt=buildT(t.inv);A.dp-=g0-A.gold;return true}}
 /* amélioration : la tour qui couvre le plus de chemin (et de couloir aérien) pour son prix */
 if(ups.length&&(!free.length||(n>=10&&Math.random()<(n>=24?.6:.35)))){const path=pathCells(A),val=t=>{const T=TW[t.k],r=rng(t);let c=0;for(const[x,y]of path)if(Math.hypot(x-t.x,y-t.y)<=r)c++;if(!T.gr)for(let y=0;y<R;y++)if(Math.hypot(6-t.x,y-t.y)<=r)c+=.6;
   return c*T.d/T.cd*(T.sp?2.5:T.fl?3:T.fsp?1.6:T.mg?1.4:1)/T.c};
  ups.sort((a,b)=>val(b)-val(a));ok=A.upgrade(ups[Math.random()<.75?0:Math.floor(Math.random()*ups.length)])}
 else{let tries=0;for(const[x,y]of free){const g=bud,ctr=Math.abs(x-6)<=1;
  const base=A.classId*10,k=n<3?(ctr?base:base+1):ctr?(g>=40&&cnt(base+2)<1+n/9?base+2:g>=70&&cnt(base+4)<n/7?base+4:g>=90&&cnt(base+5)<1+n/10?base+5:base):(g>=50&&cnt(base+3)<n/6?base+3:g>=30&&Math.random()<.7?base+1:base);
  if(TW[k].c<=bud&&A.place(x,y,k)){ok=true;break}if(++tries>=3)break}}
 A.dp-=g0-A.gold;return ok}
/* attaque : elle empile plusieurs revenus puis lâche une grosse vague, composée selon les faiblesses des adversaires */
function aiAttack(A){const time=A.G.time;let bud=Math.min(A.ap,A.gold),sent=false;if(time<GRACE||bud<Math.min(6000,Math.max(60,A.inc*3)))return false;
 const fo=A.G.foes(A),share=ks=>{let a=0,b=0;for(const o of fo)for(const t of o.t){b+=t.inv;if(ks.includes(t.k))a+=t.inv}return b?a/b:0};
 const weakAir=fo.some(b=>airInv(b)<50+time*1.5),noMage=fo.some(b=>!mages(b)),phys=share(fo.flatMap(b=>[b.classId*10,b.classId*10+4])),magic=share(fo.flatMap(b=>[b.classId*10+2,b.classId*10+5]));
 const ok=k=>bud>=CR[k].c&&time>=(CR[k].at||0),top=l=>l.filter(ok).pop(),go=k=>{const g=A.gold;if(!A.G.send(A,k))return false;sent=true;bud-=g-A.gold;A.ap-=g-A.gold;return true};
 if(bud>=500)for(const k of[HEAL,AURA])if(ok(k)&&Math.random()<.6)go(k);
 for(let n=0;n<12;n++){const opts=[[top(NORM),5],[top(FLY),weakAir?4:1],[SPEC,noMage?4:.8],[TURT,phys>.45?2.5:.7],[BRK,magic>.3?2.5:.6],[SPLIT,.7],[SAP,1]].filter(o=>o[0]!==undefined&&ok(o[0]));
  if(!opts.length)break;let r=Math.random()*opts.reduce((s,o)=>s+o[1],0),k=opts[0][0];for(const o of opts){r-=o[1];if(r<=0){k=o[0];break}}
  if(!go(k))break}
 const hero=CR.findIndex(T=>T.hero);if(hero>=0&&ok(hero)&&time>420&&Math.random()<.28)go(hero);
 return sent}
function aiAct(A){const time=A.G.time,gain=A.gold-A.lastG,danger=A.hurt>0,need=(A.G.foes(A).reduce((s,b)=>s+b.inc,0)*4+20)*(1+time/400);
 const f=danger||A.pen>.85?.8:A.pen>.65?.55:invest(A)<need*.35?.5:A.pen>.45?.3:.15;
 A.dp+=gain*f;A.ap+=gain*(1-f);if(danger&&A.lives<12){A.dp+=A.ap*.5;A.ap*=.5}
 for(let i=0;i<3&&aiDefend(A);i++);
 if(aiAttack(A))for(const b of A.G.foes(A))b.ev.push('warn');A.lastG=A.gold}


/* ---------- partie ---------- */
/* Une partie = 4 terrains. Utilisée telle quelle en solo (navigateur) et en ligne (serveur Cloudflare). */
let UID=0;
class Game{
 /* seats : [{name,col,ai,classId}] ; LV : difficulté, ne touche que les IA */
 constructor(seats,LV=0){this.LV=LV;this.time=0;this.tick=10;this.over=false;this.winner=-1;this.log=[];
  this.B=seats.map((s,i)=>{const b=new Board(i,s.name,s.col,s.ai?1:0,s.classId);b.G=this;if(b.ai){b.gold+=DIFF[LV].g;b.dp+=DIFF[LV].g;b.lastG=b.gold}return b})}
 foes(b){return this.B.filter(o=>o!==b&&!o.dead)}
 eff(b){return b.ai?Math.round(b.inc*DIFF[this.LV].b):b.inc}
 /* un envoi part chez tous les adversaires encore en jeu */
 send(from,k){const T=CR[k];if(from.gold<T.c||this.time<(T.at||0))return false;from.gold-=T.c;from.inc+=T.i;for(const b of this.foes(from))b.send(k,1+this.time/200);return true}
 /* action d'un joueur humain : renvoie '' si accepté, sinon un code d'erreur (poor, blocked, locked, max, busy, over, bad) */
 action(i,a){const b=this.B[i];if(!b||b.dead||b.ai||this.over||!a)return 'over';
  const x=a.x|0,y=a.y|0,k=a.k|0;
  if(a.type=='place'){const T=TW[k];if(!T)return 'bad';if(b.place(x,y,k))return '';return b.gold<T.c?'poor':'blocked'}
  if(a.type=='sell')return b.sell(x,y)?'':'bad';
  if(a.type=='upgrade'){const t=b.t.find(t=>t.x==x&&t.y==y);if(!t)return 'bad';return b.upgrade(t)?'':t.lv>=5?'max':t.b>0?'busy':'poor'}
  if(a.type=='send'){const T=CR[k];if(!T||T.cat=='x')return 'bad';if(this.time<(T.at||0))return 'locked';return this.send(b,k)?'':'poor'}
  return 'bad'}
 /* avance la partie de dt secondes (dt ≤ 0,05) ; les événements de partie vont dans this.log */
 step(dt){if(this.over)return;const B=this.B;this.time+=dt;this.tick-=dt;
  if(this.tick<=0){this.tick+=10;for(const b of B)if(!b.dead)b.gold+=this.eff(b);this.log.push({type:'income'})}
  for(const b of B)if(b.ai&&!b.dead){b.aiT-=dt;if(b.aiT<=0){b.aiT=.6;aiAct(b)}}
  for(const b of B)if(!b.dead)b.update(dt);
  for(const b of B)if(!b.dead&&b.lives<=0){b.dead=1;b.cr=[];b.q=[];b.pr=[];this.log.push({type:'out',i:b.i})}
  /* fin : un seul terrain debout, ou plus aucun humain en jeu */
  const alive=B.filter(b=>!b.dead);
  if(alive.length<=1||!alive.some(b=>!b.ai)){this.over=true;this.winner=alive.length==1?alive[0].i:-1;this.log.push({type:'end',winner:this.winner})}}
}
if(typeof module!='undefined'&&module.exports)module.exports={C,R,SP,EX,INF,TW,CR,DIFF,FACTIONS,Board,Game};