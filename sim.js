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
 {name:'Humains',icon:'🏹',color:'#d8b45c',dark:'#59451f',desc:'Archers, chevaliers et mages : longue portée et défense anti-aérienne.',towers:['Archer du rempart','Chevalier du lion','Mage de givre','Bombardier royal','Pyromancien','Prêtre solaire','Rôdeur d'élite','Paladin','Enchanteur du froid','Archimage humain']},
 {name:'Robots',icon:'🤖',color:'#69bde1',dark:'#203e58',desc:'Automates, drones et canons : puissance perforante et armures mécaniques.',towers:['Drone arbalète','Mécha sentinelle','Cryobot','Canon à impulsion','Lance-flammes MK2','Technomancien','Drone sniper','Titan d'acier','Noyau cryogénique','Colosse plasma']},
 {name:'Créatures',icon:'🦎',color:'#b66add',dark:'#44234f',desc:'Bestioles mutantes et prédateurs : frénésie et exécution des ennemis blessés.',towers:['Cracheur d'épines','Griffeur alpha','Gelée glaciale','Bombardier chitineux','Salamandre ardente','Oracle tentaculaire','Rapace venimeux','Brute carapace','Mante de givre','Reine des essaims']},
 {name:'Végétaux',icon:'🌳',color:'#69bd83',dark:'#214b38',desc:'Arbres vivants, fleurs et dryades : racines et ralentissement.',towers:['Arbre archer','Gardien de l'écorce','Fleur de gel','Graine explosive','Ronce brûlante','Druide des mousses','Saule tireur','Ent ancestral','Lotus hivernal','Esprit de la forêt']},
 {name:'Magiques',icon:'🔮',color:'#a879e9',dark:'#39204d',desc:'Spectres, sorciers et cristaux : malédictions qui amplifient les dégâts.',towers:['Spectre archer','Chevalier astral','Cristal de stase','Orbe du chaos','Phénix arcanique','Sorcière des runes','Œil éthéré','Golem spectral','Prisme maudit','Archimage du néant']}
];
const ARCH=[0,4,2,1,5,3,0,4,2,3];
/* Coefficients volontairement proches en rendement global : chaque avantage a une vraie contrepartie. */
const FACTION_BALANCE=[
 {cost:1.04,dmg:.97,range:1.10,cd:1.03,airBonus:1.18,tag:'anti-aérien'},
 {cost:1.07,dmg:1.08,range:1.02,cd:1.08,pierce:.55,tag:'perforant'},
 {cost:1.02,dmg:.96,range:.93,cd:1.04,execute:1.30,tag:'frénésie'},
 {cost:1.00,dmg:.96,range:1.00,cd:1.02,root:.72,rootFactor:.82,tag:'racines'},
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
/* temps de construction : 1 s pour BUILD_OR pièces d'or dépensées (achat ou amélioration), entre BUILD_MIN et BUILD_MAX secondes,
   multiplié pour les humains par BUILD_DIFF selon la difficulté (les IA gardent ×1, comme pour le revenu) */
 BUILD_OR=50,BUILD_MIN=.5,BUILD_MAX=8,BUILD_DIFF=[1,1.25,1.5],buildT=(c,m=1)=>Math.min(BUILD_MAX,Math.max(BUILD_MIN,c/BUILD_OR))*m,flyH=k=>CR[k].fly?CR[k].z*.35:0;
const dmg=t=>TW[t.k].d*2**(t.lv-1),rng=t=>TW[t.k].r*(1+.05*(t.lv-1)),upCost=t=>Math.round(TW[t.k].c*1.5*2**(t.lv-1)/5)*5,topY=t=>.28+.045*(t.lv-1);

/* ---------- simulation ---------- */
/* grille de voisinage (2.5.2, performances) : chaque élément d'une liste est rangé dans sa case, pour ne tester que les voisins d'un point
   au lieu de toute la liste. near() rend les indices dans l'ordre de la liste : les résultats sont identiques à un parcours complet. */
const gcl=(v,m)=>Math.min(m-1,Math.max(0,v|0));
class Grid{constructor(){this.b=Array.from({length:C*R},()=>[]);this.u=[];this.o=[]}
 fill(l){for(const i of this.u)this.b[i].length=0;this.u.length=0;for(let n=0;n<l.length;n++){const i=gcl(l[n].y,R)*C+gcl(l[n].x,C);if(!this.b[i].length)this.u.push(i);this.b[i].push(n)}return this}
 /* éléments dont la case touche le carré de demi-côté r autour de (x, y), dans l'ordre de la liste */
 near(x,y,r){const o=this.o,x0=gcl(Math.floor(x-r),C),x1=gcl(Math.floor(x+r),C),y0=gcl(Math.floor(y-r),R),y1=gcl(Math.floor(y+r),R);o.length=0;
  for(let b=y0;b<=y1;b++)for(let a=x0;a<=x1;a++){const L=this.b[b*C+a];for(let k=0;k<L.length;k++)o.push(L[k])}if(o.length>1)o.sort((p,q)=>p-q);return o}}
const GRID_MIN=12;
class Board{
 constructor(i,name,col,ai,classId=0){this.i=i;this.name=name;this.col=col;this.ai=ai;this.classId=classId;this.dead=0;this.aiT=1+i*.2;this.ev=[];this.G=null;
  this.g=Array.from({length:R},()=>Array(C).fill(0));this.t=[];this.cr=[];this.pr=[];this.fx=[];this.q=[];this.gold=100;this.inc=10;this.lives=40;this.hurt=0;this.pen=0;this.dp=60;this.ap=40;this.lastG=100;this.flyIn=0;this.hpIn=0;this.specSeen=0;this.mz=null;this.d=this.dist()}
 dist(){const d=Array.from({length:R},()=>Array(C).fill(INF)),q=[[EX[0],EX[1]]];d[EX[1]][EX[0]]=0;
  for(let i=0;i<q.length;i++){const[x,y]=q[i];for(const[dx,dy]of DIRS){const a=x+dx,b=y+dy;if(a<0||b<0||a>=C||b>=R||this.g[b][a]||d[b][a]<INF)continue;d[b][a]=d[y][x]+1;q.push([a,b])}}return d}
 place(x,y,k){const T=TW[k];
  if(Math.floor(k/10)!==this.classId)return false;
  if(x<0||y<0||x>=C||y>=R||this.gold<T.c||this.g[y][x]||(x==SP[0]&&y==SP[1])||(x==EX[0]&&y==EX[1]))return false;
  if(this.cr.some(c=>!CR[c.k].fly&&((Math.abs(c.x-x)<.9&&Math.abs(c.y-y)<.9)||(c.tx==x&&c.ty==y))))return false;
  this.g[y][x]=1;const nd=this.dist();
  if(nd[SP[1]][SP[0]]>=INF||this.cr.some(c=>!CR[c.k].fly&&nd[c.ty][c.tx]>=INF)){this.g[y][x]=0;return false}
  this.d=nd;this.gold-=T.c;const bt=buildT(T.c,this.bm());this.t.push({x,y,k,cd:0,a:.7,lv:1,inv:T.c,sw:0,b:bt,bt});
  this.fx.push({type:'range',x:x+.5,y:y+.5,r:T.r,t:.6,d:.6,col:T.col});this.ev.push('build');return true}
 /* multiplicateur de temps de construction : selon la difficulté pour un humain, ×1 pour une IA */
 bm(){return this.G&&!this.ai?BUILD_DIFF[this.G.LV]||1:1}
 sell(x,y){const i=this.t.findIndex(t=>t.x==x&&t.y==y);if(i<0)return false;const b=Math.floor(this.t[i].inv*.7);this.gold+=b;this.t.splice(i,1);this.g[y][x]=0;this.d=this.dist();
  this.fx.push({type:'text',x:x+.5,y:y+.4,txt:'+'+b,col:'#ffd95e',t:.7,d:.7});this.ev.push('sell');return true}
 upgrade(t){const c=upCost(t);if(t.lv>=5||t.b>0||this.gold<c)return false;this.gold-=c;t.inv+=c;t.lv++;t.b=t.bt=buildT(c,this.bm());
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
  if(rad){const cg=this.cgOk&&this.cr.length>GRID_MIN?this.cg.near(p.tx-.5,p.ty-.5,rad+.5).map(n=>this.cr[n]):this.cr;for(const c of cg){if(c===tg||c.hid||(T.gr&&CR[c.k].fly)||Math.hypot(c.x+.5-p.tx,c.y+.5-flyH(c.k)-p.ty)>=rad)continue;this.hit(c,p.d*.6,T,p.sf)}
   this.fx.push({type:'boom',x:p.tx,y:p.ty,r:rad,t:.3,d:.3,col:T.sl?'#8fdcff':'#ffb347'});if(T.sp)this.ev.push('boom')}
  else this.fx.push({type:'ring',x:p.tx,y:p.ty,r:T.skin==3?.45:.26,t:.2,d:.2,col:T.skin==0?'#ffffff':'#e39bff'})}
 update(dt){
  this.hurt=Math.max(0,this.hurt-dt);
  for(const s of this.q){s.t-=dt;if(s.t<=0){const hp=CR[s.k].hp*s.m*HPK;this.hpIn+=hp;if(CR[s.k].fly)this.flyIn+=hp;if(CR[s.k].inv)this.specSeen=1;this.cr.push({id:++UID,k:s.k,x:SP[0],y:SP[1],tx:SP[0],ty:SP[1],hp,max:hp,sl:0,sf:.5,f:1,ph:Math.random()*6,ox:(Math.random()-.5)*.3,oy:(Math.random()-.5)*.22,arm:(CR[s.k].arm||0)*s.m,cs:2})}}
  this.q=this.q.filter(s=>s.t>0);
  const au=this.cr.filter(c=>CR[c.k].aura),mg=this.t.filter(t=>TW[t.k].mg&&!(t.b>0)),hl=this.cr.filter(c=>CR[c.k].heal);
  /* hâte et soin : avec beaucoup de Chamans ou de Prêtresses, on ne regarde que ceux des cases voisines. Ils bougent pendant la boucle (au plus 3,4 cases/s × dt),
     d'où la marge ajoutée au rayon ; la distance exacte est ensuite vérifiée comme avant. */
  const ar=AURA_R+3.4*dt+.01,auG=au.length>GRID_MIN&&(this.ag||(this.ag=new Grid())).fill(au),hlG=hl.length>GRID_MIN&&(this.hg||(this.hg=new Grid())).fill(hl);
  for(const c of this.cr){const T=CR[c.k];c.sl=Math.max(0,c.sl-dt);c.mark=Math.max(0,(c.mark||0)-dt);c.h=!T.aura&&(auG?auG.near(c.x,c.y,ar).some(n=>Math.hypot(au[n].x-c.x,au[n].y-c.y)<AURA_R):au.some(a=>Math.hypot(a.x-c.x,a.y-c.y)<AURA_R));
   c.hid=T.inv&&!mg.some(m=>Math.hypot(c.x-m.x,c.y-m.y)<=rng(m));
   c.hl=c.hp<c.max&&(hlG?hlG.near(c.x,c.y,ar).some(n=>hl[n]!==c&&Math.hypot(hl[n].x-c.x,hl[n].y-c.y)<AURA_R):hl.some(a=>a!==c&&Math.hypot(a.x-c.x,a.y-c.y)<AURA_R));if(c.hl)c.hp=Math.min(c.max,c.hp+c.max*.05*dt);
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
  /* tours et explosions : seuls les monstres des cases à portée sont examinés (grille remplie une fois par pas, les monstres ne bougent plus ensuite) */
  const cr=this.cr,useG=cr.length>GRID_MIN;if(useG)(this.cg||(this.cg=new Grid())).fill(cr);this.cgOk=useG;const voisins=(x,y,r)=>useG?this.cg.near(x,y,r).map(n=>cr[n]):cr;
  for(const t of this.t){if(t.b>0){t.b-=dt;if(t.b<=0){t.b=0;t.cd=0;this.fx.push({type:'range',x:t.x+.5,y:t.y+.5,r:rng(t),t:.6,d:.6,col:TW[t.k].col})}continue}
   if(t.stun>0){t.stun-=dt;continue}t.cd-=dt;if(t.sw>0)t.sw-=dt;if(t.cd>0)continue;const T=TW[t.k],r=rng(t),dm=dmg(t);let tg=null,bd=INF;
   for(const c of voisins(t.x,t.y,r)){const F=CR[c.k].fly;if(c.hid||(T.gr&&F)||(T.mag&&CR[c.k].mi))continue;if(Math.hypot(c.x-t.x,c.y-t.y)>r)continue;
    const rem=F?Math.hypot(EX[0]-c.x,EX[1]-c.y):this.d[c.ty][c.tx]+Math.hypot(c.tx-c.x,c.ty-c.y);if(rem<bd){bd=rem;tg=c}}
   if(!tg)continue;t.cd=T.cd;t.a=Math.atan2(tg.y-t.y,tg.x-t.x);
   if(T.me){this.hit(tg,dm,T);t.sw=.2;this.fx.push({type:'slash',x:tg.x+.5,y:tg.y+.5,a:t.a,t:.18,d:.18})}
   else if(T.fl){for(const c of voisins(t.x,t.y,r)){if(c.hid)continue;const dx=c.x-t.x,dy=c.y-t.y,dd=Math.hypot(dx,dy);if(dd>r)continue;const da=Math.atan2(dy,dx)-t.a;if(dd<.6||Math.abs(Math.atan2(Math.sin(da),Math.cos(da)))<.5)this.hit(c,dm,T)}
    const h=topY(t);for(let i=0;i<2;i++){const a=t.a+(Math.random()-.5)*.5,v=r/.35*(.75+Math.random()*.35);this.fx.push({type:'flame',x:t.x+.5,y:t.y+.5-h,vx:Math.cos(a)*v,vy:Math.sin(a)*v+h/.35,t:.35,d:.35})}}
   else this.pr.push({id:++UID,x:t.x+.5,y:t.y+.5-topY(t),tg,k:t.k,d:dm,sf:.5-.05*(t.lv-1),tx:tg.x+.5,ty:tg.y+.5,tot:Math.hypot(tg.x-t.x,tg.y-t.y)||.1,a:t.a});
   this.ev.push(T.s)}
  for(const p of this.pr){const T=TW[p.k];if(!p.tg.dead&&!p.tg.leak){p.tx=p.tg.x+.5;p.ty=p.tg.y+.5-flyH(p.tg.k)}
   const dx=p.tx-p.x,dy=p.ty-p.y,dd=Math.hypot(dx,dy),m=T.ps*dt;
   if(dd<=m){p.hit=1;this.impact(p)}else{p.x+=dx/dd*m;p.y+=dy/dd*m;p.a=Math.atan2(dy,dx)}}
  this.pr=this.pr.filter(p=>!p.hit);this.cgOk=false;
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
const invest=b=>b.t.reduce((s,t)=>s+t.inv,0),airInv=b=>b.t.reduce((s,t)=>s+(!TW[t.k].gr&&Math.abs(t.x-6)<=2?t.inv:0),0),mages=b=>b.t.filter(t=>TW[t.k].mg).length;
function pathCells(b){const out=[];let x=SP[0],y=SP[1];out.push([x,y]);for(let n=0;n<200&&b.d[y][x]>0&&b.d[y][x]<INF;n++){for(const[dx,dy]of DIRS){const a=x+dx,c=y+dy;if(a>=0&&c>=0&&a<C&&c<R&&b.d[c][a]==b.d[y][x]-1){x=a;y=c;break}}out.push([x,y])}return out}

/* --- labyrinthe de l'IA (2.5, affiné en 2.6) : chaque terrain IA reçoit un plan cible au début de la partie ---
   grille plate (case i = y*C+x, 1 = mur), parcours en largeur rapide, hasard propre (graine tirée une fois) pour que le découpage dans le temps ne change rien. */
const N=C*R,SPI=SP[1]*C+SP[0],EXI=EX[1]*C+EX[0],NB=new Int16Array(N*5),QB=new Int16Array(N),DB=new Int16Array(N);
for(let i=0;i<N;i++){const x=i%C,y=i/C|0;let k=0;for(const[dx,dy]of DIRS){const a=x+dx,b=y+dy;if(a>=0&&b>=0&&a<C&&b<R)NB[i*5+1+k++]=b*C+a}NB[i*5]=k}
/* longueur du plus court chemin apparition → sortie, -1 si bloqué (DB garde les distances à la sortie) */
function plen(w){DB.fill(-1);DB[EXI]=0;QB[0]=EXI;let h=0,t=1;while(h<t){const i=QB[h++],d=DB[i]+1,o=i*5;for(let k=1;k<=NB[o];k++){const j=NB[o+k];if(!w[j]&&DB[j]<0){DB[j]=d;if(j==SPI)return d;QB[t++]=j}}}return -1}
function mzPath(w){if(plen(w)<0)return[];const out=[SPI];let i=SPI;for(let d=DB[SPI];d>0;d--){const o=i*5;for(let k=1;k<=NB[o];k++){const j=NB[o+k];if(!w[j]&&DB[j]==d-1){i=j;break}}out.push(i)}return out}
const rnd32=a=>()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const MZ_LAM=.3,MZ_NC=4,MZ_K=[2000,2500,3200],MZ_PICK=[[.5,.3,.2],[.6,.4],[1]];
/* forme de départ tirée au hasard : serpentin horizontal (couloirs de 1 ou 2), serpentin vertical, ou semis aléatoire */
function mzTemplate(r){const w=new Uint8Array(N),f=r()<.35?0:r()<.25?1:2;
 if(f==0){const p=r()<.7?2:3;let side=r()<.5;for(let y=2+(r()*2|0);y<R-1;y+=p){const gw=1+(p==3&&r()<.5);for(let x=0;x<C;x++)if(side?x<C-gw:x>=gw)w[y*C+x]=1;side=!side}}
 else if(f==1){let top=r()<.5;for(let x=r()<.5?1:0;x<C;x+=2){for(let y=1;y<R-1;y++)if(top?y>1:y<R-2)w[y*C+x]=1;top=!top}}
 else for(let i=0;i<N;i++)w[i]=r()<.35?1:0;
 w[SPI]=w[EXI]=0;while(plen(w)<0)w[r()*N|0]=0;
 let n=0;for(let i=0;i<N;i++)n+=w[i];const L=plen(w);return {w,f,n,L,s:L-MZ_LAM*n,best:w.slice(),bs:L-MZ_LAM*n,it:0}}
/* recherche locale (recuit léger) : on ajoute ou retire une case ou un petit segment, on garde si le chemin s'allonge sans trop de tours */
function mzClimb(c,r,K,steps){for(let e=0;e<steps&&c.it<K;e++,c.it++){const w=c.w,T=2*(1-c.it/K)+.05,i=r()*N|0;if(i==SPI||i==EXI)continue;
 const seg=[i];if(r()<.3){const[dx,dy]=DIRS[r()*4|0];let x=i%C,y=i/C|0;for(let k=1+(r()*3|0);k>0;k--){x+=dx;y+=dy;if(x<0||y<0||x>=C||y>=R)break;const j=y*C+x;if(j!=SPI&&j!=EXI)seg.push(j)}}
 const v=w[i]?0:1,ch=seg.filter(j=>w[j]!=v);for(const j of ch)w[j]=v;const L=plen(w),n=c.n+(v?ch.length:-ch.length),s=L-MZ_LAM*n;
 if(L>=0&&(s>=c.s||r()<Math.exp((s-c.s)/T))){c.L=L;c.n=n;c.s=s;if(s>c.bs){c.bs=s;c.best=w.slice()}}else for(const j of ch)w[j]=1-v}}
/* fait avancer la génération du plan d'au plus « steps » essais (un essai ≈ un parcours en largeur) ; renvoie le plan quand il est prêt.
   Étapes : 1) MZ_NC formes de départ affinées par recherche locale ; 2) pour chacune : murs inutiles retirés, ordre de construction, note de milieu de partie ; 3) choix et rôles. */
function mzStep(A,steps){let M=A.mz;if(M&&M.ok)return M;
 if(!M)M=A.mz={r:rnd32(Math.random()*4294967296>>>0),c:[],ok:0,o:0};const r=M.r,LV=A.G?A.G.LV|0:0,K=MZ_K[LV];
 while(steps>0){let c=M.c[M.c.length-1];if(c&&c.it>=K&&M.c.length>=MZ_NC)break;if(!c||c.it>=K){c=mzTemplate(r);M.c.push(c)}const s=Math.min(steps,K-c.it);mzClimb(c,r,K,s);steps-=s}
 while(steps>0&&M.o<MZ_NC){const c=M.c[M.o];if(!c.left)steps-=mzPrune(c);else if(c.left.length)steps-=mzRemove(c,r);else{steps-=mzEval(c);M.o++}}
 if(M.o<MZ_NC)return null;
 mzChoose(M,LV);mzRoles(A,M);M.ok=1;return M}
const MZX=new Int8Array(N),MZY=new Int8Array(N);for(let i=0;i<N;i++){MZX[i]=i%C;MZY[i]=i/C|0}
const near=(i,j,d)=>{const dx=MZX[i]-MZX[j],dy=MZY[i]-MZY[j];return dx*dx+dy*dy<=d*d};
/* murs inutiles : une tour qui ne touche pas le chemin (8 cases autour) et dont le retrait ne le raccourcit pas est retirée du plan ; puis l'ordre de construction est préparé */
function mzPrune(c){const w=c.best.slice(),L=plen(w);let n=1,ch=1;
 while(ch){ch=0;const adj=new Uint8Array(N);for(const j of mzPath(w)){n++;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const x=MZX[j]+dx,y=MZY[j]+dy;if(x>=0&&y>=0&&x<C&&y<R)adj[y*C+x]=1}}
  for(let i=0;i<N;i++)if(w[i]&&!adj[i]){w[i]=0;n++;if(plen(w)==L)ch=1;else w[i]=1}}
 c.w=w;c.cur=w.slice();c.left=[];for(let i=0;i<N;i++)if(w[i])c.left.push(i);c.walls=c.left.slice();c.rev=[];return n}
/* ordre de construction : on retire une à une, depuis le plan complet, la tour qui raccourcit le moins le chemin (puis la moins utile au chemin actuel et au couloir aérien) ;
   construire dans l'ordre inverse allonge le chemin presque à chaque tour et, au début, place les tours près du chemin droit et des volants */
function mzRemove(c,r){const cur=c.cur,left=c.left,L0=plen(cur),Pc=mzPath(cur);let bi=0,bk=INF;
 const smp=left.length<=24?left.map((_,k)=>k):Array.from({length:24},()=>r()*left.length|0);
 for(const k of smp){const i=left[k];cur[i]=0;const L=plen(cur);cur[i]=1;let cv=0;for(const j of Pc)if(near(i,j,2.5))cv++;
  const key=(L0-L)+.05*cv+(Math.abs(MZX[i]-6)<=2?.3:0)+r()*.2;if(key<bk){bk=key;bi=k}}
 const i=left[bi];left.splice(bi,1);cur[i]=0;c.rev.push(i);return smp.length+2}
/* note d'un candidat : longueur moyenne du chemin après 15, 25, 40 et 60 tours (l'IA en a rarement plus en milieu de partie) et une fois complet */
const MZ_AT=[15,25,40,60];
function mzEval(c){c.ord=c.rev.reverse();const w=new Uint8Array(N),Ls=[];c.ord.forEach((i,n)=>{w[i]=1;if(MZ_AT.includes(n+1))Ls.push(plen(w))});
 c.L=plen(c.w);while(Ls.length<MZ_AT.length)Ls.push(c.L);c.pre=Ls;c.note=(Ls.reduce((a,b)=>a+b,0)+c.L)/(MZ_AT.length+1);delete c.cur;delete c.rev;delete c.left;return MZ_AT.length+2}
/* choix du plan parmi les candidats, sur la note de milieu de partie (le meilleur en Brutal, un des 2 ou 3 meilleurs sinon) */
function mzChoose(M,LV){const r=M.r;M.c.sort((a,b)=>b.note-a.note);const P=MZ_PICK[LV];let q=r(),ch=0;for(;ch<P.length-1;ch++){q-=P[ch];if(q<=0)break}
 const c=M.c[ch];M.f=c.f;M.w=c.w;M.ord=c.ord;M.walls=c.walls;M.pre=c.pre;M.note=c.note;M.c=null}
/* rôles (emplacement j de la faction) : Givre répartis le long du chemin final, Mages pour que leur détection couvre tout le chemin, air près du couloir des volants */
function mzRoles(A,M){const base=A.classId*10,rg=j=>TW[base+j].r,w=M.w,P=mzPath(w),walls=M.walls,role=new Int8Array(N).fill(-1);
 M.L=P.length-1;delete M.walls;
 const cov=(i,d)=>{let n=0;for(const j of P)if(near(i,j,d))n++;return n},gain=(i,d,cv)=>{let v=0;for(let n=0;n<P.length;n++)if(!cv[n]&&near(i,P[n],d))v++;return v},mark=(i,d,cv)=>{for(let n=0;n<P.length;n++)if(near(i,P[n],d))cv[n]=1};
 const ng=Math.min(6,Math.max(2,Math.round(M.L/15))),cG=new Uint8Array(P.length);
 for(let k=0;k<ng;k++){const tgt=P[Math.floor(P.length*(k+.5)/ng)];let bi=-1,bv=0;for(const i of walls){if(role[i]>=0||!near(i,tgt,rg(2)))continue;const v=gain(i,rg(2),cG);if(v>bv){bv=v;bi=i}}
  if(bi>=0){role[bi]=2;mark(bi,rg(2),cG)}}
 const cM=new Uint8Array(P.length);for(let k=0;k<6;k++){let bi=-1,bv=2;for(const i of walls){if(role[i]>=0)continue;const v=gain(i,rg(5),cM);if(v>bv){bv=v;bi=i}}
  if(bi<0)break;role[bi]=5;mark(bi,rg(5),cM)}
 /* hors couloir aérien : Canon dans les virages (beaucoup de chemin autour), Garde entre deux couloirs, sinon Archer ; un peu de hasard pour varier */
 for(const i of walls)if(role[i]<0){const ax=Math.abs(MZX[i]-6),cc=cov(i,rg(3)),cg=cov(i,Math.max(rg(1),1.45));
  role[i]=ax<=2?(ax<=1&&cov(i,rg(4))>=7?4:0):cc>=12||(cg>=4&&M.r()<.3)?3:cg>=4?1:cc>=8?3:0}
 M.role=role}
/* tour à poser sur la case i du plan selon la situation (-1 : attendre d'avoir l'or) */
function mzKind(A,i,n,bud,thr,fs){const M=A.mz,base=A.classId*10,x=i%C,cnt=js=>A.t.filter(t=>js.includes(t.k-base)).length;let j=M.role[i];
 if(j==5&&!thr)j=0;if(j==2&&cnt([2,8])>=1+n*.15)j=0;if((j==1||j==3)&&fs>.35&&Math.abs(x-6)<=3)j=0;
 if(n<5&&TW[base+j].c>bud)j=0;
 const e={0:6,1:7,2:8,5:9}[j];if(e!==undefined&&n>=(j==5?16:j==2?12:8)&&(j!=5||A.G.time>360)&&bud>=TW[base+e].c)j=e;
 return TW[base+j].c<=bud?base+j:-1}
/* Chaque pièce gagnée est répartie entre deux bourses, défense et attaque, selon la pression subie (pen = jusqu'où les monstres avancent chez elle). */
function aiDefend(A){const M=mzStep(A,INF),time=A.G.time,bud=Math.min(A.dp,A.gold),g0=A.gold,base=A.classId*10,n=A.t.length,ups=A.t.filter(t=>t.lv<5&&!(t.b>0)&&bud>=upCost(t));let ok=false;
 const fs=(A.flyIn||0)/((A.hpIn||0)+1),thr=A.specSeen||(time>=150&&A.G.foes(A).some(b=>b.inc>=35));
 /* transformations : Mages sur leurs cases quand des Spectres deviennent possibles, Givre sur les siens quand le plafond le permet */
 for(const t of A.t){const i=t.y*C+t.x,j=M.role[i],cur=t.k-base;if(t.lv>2||t.b>0)continue;
  const want=j==5&&thr&&!TW[t.k].mg?5:j==2&&cur!=2&&cur!=8&&A.t.filter(o=>o.k-base==2||o.k-base==8).length<1+n*.15?2:-1;if(want<0)continue;
  const k=base+want,mc=TW[k].c-Math.floor(t.inv*.7);if(bud<mc)continue;A.gold-=mc;t.k=k;t.lv=1;t.inv=TW[k].c;t.b=t.bt=buildT(t.inv,A.bm());A.ev.push('build');A.dp-=g0-A.gold;return true}
 const todo=M.ord.filter(i=>!A.g[i/C|0][i%C]);
 /* amélioration : la tour qui couvre le plus de chemin (et de couloir aérien, d'autant plus que des volants arrivent) pour son prix */
 if(ups.length&&(!todo.length||(n>=10&&Math.random()<(n>=24?.6:.35)))){const path=pathCells(A),aw=.6*(1+2*fs),val=t=>{const T=TW[t.k],r=rng(t);let c=0;for(const[x,y]of path)if(Math.hypot(x-t.x,y-t.y)<=r)c++;if(!T.gr)for(let y=0;y<R;y++)if(Math.hypot(6-t.x,y-t.y)<=r)c+=aw;
   return c*T.d/T.cd*(T.sp?2.5:T.fl?3:T.fsp?1.6:T.mg?1.4:1)/T.c};
  const vs=new Map(ups.map(t=>[t,val(t)]));ups.sort((a,b)=>vs.get(b)-vs.get(a));ok=A.upgrade(ups[Math.random()<.75?0:Math.floor(Math.random()*ups.length)])}
 /* construction : la prochaine case du plan ; si elle est occupée par un monstre, on essaie les suivantes, mais on n'en saute pas une faute d'or */
 else for(const i of todo.slice(0,4)){const k=mzKind(A,i,n,bud,thr,fs);if(k<0)break;if(A.place(i%C,i/C|0,k)){ok=true;break}}
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
  for(const b of B)if(b.ai&&!b.dead){mzStep(b,600);b.aiT-=dt;if(b.aiT<=0){b.aiT=.6;aiAct(b)}}
  for(const b of B)if(!b.dead)b.update(dt);
  for(const b of B)if(!b.dead&&b.lives<=0){b.dead=1;b.cr=[];b.q=[];b.pr=[];this.log.push({type:'out',i:b.i})}
  /* fin : un seul terrain debout, ou plus aucun humain en jeu */
  const alive=B.filter(b=>!b.dead);
  if(alive.length<=1||!alive.some(b=>!b.ai)){this.over=true;this.winner=alive.length==1?alive[0].i:-1;this.log.push({type:'end',winner:this.winner})}}
}
if(typeof module!='undefined'&&module.exports)module.exports={C,R,SP,EX,INF,TW,CR,DIFF,FACTIONS,Board,Game};