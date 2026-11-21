/* Races asymétriques (2.40) : règles d'équilibrage centrales (CLAUDE.md §5.3), mécaniques propres, états et combos.
   Toute nouvelle race (ou retouche) doit passer ces règles ; le banc des races (tests/outils/banc-races.js) vérifie l'équilibre en partie. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre,avancerTerrain,pret}=require('../outils/moteur');
const S=charger('actuel');
const proche=(a,b,msg,eps=1e-6)=>assert.ok(Math.abs(a-b)<=eps,`${msg||''} attendu ${b}, obtenu ${a}`);
const terrain=f=>{const b=partie(S,{factions:[f,(f+1)%5,(f+2)%5,(f+3)%5]}).B[0];b.gold=1e6;return b};
const fort=c=>{c.hp=c.max=1e6;return c};
const TW=(f,j)=>S.TW[f*10+j],K=(f,j)=>f*10+j;

/* ---------- règles centrales ---------- */
test('Règle 1 — profil en radar : 6 axes, somme 30, chaque axe entre 3 et 8, au moins une faiblesse (≤ 4), au plus deux spécialités (≥ 7)',()=>{
 const R=S.REGLES;assert.equal(R.axes.length,6);
 for(const F of S.RACES){const v=F.radar;assert.equal(v.length,6,F.name);assert.equal(v.reduce((a,b)=>a+b,0),R.RADAR_SOMME,F.name+' : somme');
  assert.ok(v.every(n=>n>=R.RADAR_MIN&&n<=R.RADAR_MAX),F.name+' : bornes');assert.ok(v.some(n=>n<=4),F.name+' : faiblesse');assert.ok(v.filter(n=>n>=7).length<=2,F.name+' : spécialités')}
});
test('Règle 2 — couverture : tour de base sol et air ≤ 25 or, anti-aérien dédié, détection ≤ 120 or, 2 sources non magiques, une réponse aux blindés, une seule ultime',()=>{
 for(let f=0;f<5;f++){const F=S.RACES[f],L=Array.from({length:10},(_,j)=>TW(f,j));
  assert.ok(L[0].c<=25&&!L[0].gr&&!L[0].ao&&!L[0].no,F.name+' : base sol et air');
  assert.ok(L[4].air>=2||L[4].ao,F.name+' : anti-aérien dédié');
  assert.ok(L[5].det&&L[5].c<=120,F.name+' : détection');
  assert.ok(L.filter(T=>!T.mag&&!T.no).length>=2,F.name+' : sources non magiques');
  assert.ok(L.some(T=>T.pierce||T.br||T.pz||T.sg||T.ex||T.hx||T.spe||T.pe),F.name+' : réponse aux blindés');
  assert.ok(L[9].u&&L.filter(T=>T.u).length==1,F.name+' : une ultime, en emplacement 9');
  assert.ok(F.combos.length>=2&&F.combos.every(c=>c.a.length==2&&c.a[0]!=c.a[1]),F.name+' : combos à deux tours différentes');
  assert.ok(F.meca&&F.meca.n&&F.etats.length>=1&&F.histoire&&F.forces&&F.faible,F.name+' : fiche complète')}
});
test('Règle 3 — pas de domination : aucune tour n’est meilleure qu’une autre de sa race en prix, dégâts estimés, portée et cibles à la fois',()=>{
 for(let f=0;f<5;f++)for(let a=0;a<10;a++)for(let b=0;b<10;b++){if(a==b)continue;const A=TW(f,a),B=TW(f,b);
  const domine=A.c<=B.c&&A.ed*A.zf>B.ed*B.zf&&A.r>=B.r&&(!A.gr||B.gr)&&(!A.ao||B.ao)&&!A.mag&&!B.det&&!B.au&&!B.eco&&!B.u&&!B.no&&
   !(B.im||B.ab||B.hx||B.mk||B.ma||B.br||B.tw||B.sg||B.flo||B.rz||B.mn||B.fsp||B.jug||B.ex||B.spe||B.pierce||B.ch||B.ln||B.bm||B.pu!==undefined);
  assert.ok(!domine,`${A.n} domine ${B.n}`)}
});
test('Règle 4 — plafonds : amplification ≤ +60 %, poison ≤ 10 doses',()=>{const b=terrain(4);const c=fort(apparaitre(S,b,0));
 c.mk=5;c.ma=5;const hp=c.hp;b.hit(c,10,{n:'essai'},1);proche(hp-c.hp,10*1.35,'Marqué + Maudit = +35 %');assert.ok(S.AMP_MAX==.6);
 const P=TW(2,0);for(let i=0;i<30;i++)b.hit(c,0,P,1);assert.equal(c.pz,S.DOSE_MAX);
});
test('Une seule tour ultime par terrain (code « unique »)',()=>{const G=partie(S),b=G.B[0];b.gold=1e6;
 assert.equal(G.action(0,{type:'place',x:3,y:3,k:K(0,9)}),'');assert.equal(G.action(0,{type:'place',x:9,y:3,k:K(0,9)}),'unique');
});

/* ---------- mécaniques propres ---------- */
test('Aubeval — Cohésion : +4 % de dégâts par tour d’Aubeval voisine (jusqu’à +16 %) ; l’Étendard royal la double',()=>{const b=terrain(0);
 b.place(5,5,K(0,0));b.place(6,5,K(0,0));b.place(4,5,K(0,0));pret(b);b.bonus();proche(b.t[0].co,.08,'deux voisines');
 b.place(5,6,K(0,7));pret(b);b.bonus();proche(b.t[0].co,.24,'trois voisines, Étendard : ×2');proche(S.dmg(b.t[0])/TW(0,0).d,(1+.24),'dégâts');
});
test('Aubeval — Comptoir marchand : +5 or toutes les 10 s par niveau, en plus du revenu',()=>{const G=partie(S),b=G.B[0];b.gold=1e6;G.action(0,{type:'place',x:3,y:3,k:K(0,6)});pret(b);
 const or=b.gold;G.time=50;G.tick=.01;G.step(.02);assert.equal(b.gold-or,b.inc+5);
});
test('Aubeval — Jugement : la Chapelle marque (+15 %), l’Inquisiteur fait détoner le sceau (+60 %) et l’efface',()=>{const b=terrain(0);const c=fort(apparaitre(S,b,0));
 b.hit(c,0,TW(0,5),1);assert.ok(c.mk>0);let hp=c.hp;b.hit(c,10,{n:'essai'},1);proche(hp-c.hp,11.5,'Marqué');
 hp=c.hp;b.hit(c,10,TW(0,8),1);proche(hp-c.hp,10*1.6,'Jugement (remplace le bonus du sceau)');assert.equal(c.mk,0);assert.ok(b.fx.some(f=>f.txt=='JUGEMENT !'));
});
test('Aubeval — filet : un volant abattu peut être frappé par une tour « sol uniquement »',()=>{const b=terrain(0);const c=fort(apparaitre(S,b,S.FLY[0]));
 assert.ok(!S.cible(TW(0,3),c));b.hit(c,0,TW(0,2),1);assert.ok(c.ab>0);assert.ok(S.cible(TW(0,3),c));
});
test('Orage Blanc — chaîne d’éclairs : 3 rebonds, deux fois plus sur un Trempé (Conduction)',()=>{const b=terrain(1);b.place(6,6,K(1,6));pret(b);
 const L=[];for(let i=0;i<8;i++){const c=fort(apparaitre(S,b,0));Object.assign(c,{x:6,y:4+i*.5,tx:6,ty:Math.round(4+i*.5)});L.push(c)}
 for(const c of L)c.hp=c.max;b.t[0].cd=0;b.update(.01);assert.equal(L.filter(c=>c.hp<c.max).length,4,'cible + 3 rebonds');
 const b2=terrain(1);b2.place(6,6,K(1,6));pret(b2);const L2=[];for(let i=0;i<8;i++){const c=fort(apparaitre(S,b2,0));Object.assign(c,{x:6,y:4+i*.5,tx:6,ty:Math.round(4+i*.5),tw:5});L2.push(c)}
 for(const c of L2)c.hp=c.max;b2.t[0].cd=0;b2.update(.01);assert.equal(L2.filter(c=>c.hp<c.max).length,7,'Trempé : cible + 6 rebonds');
});
test('Orage Blanc — Fureur : une victime donne une charge (+3 % de cadence) ; à 10 charges, Rage',()=>{const b=terrain(1);b.place(6,3,K(1,0));pret(b);const t=b.t[0];
 for(let i=0;i<10;i++){const c=apparaitre(S,b,0);c.lt=t;c.hp=0;b.update(0)}assert.equal(t.fu,10);assert.ok(t.rg>0,'Rage');b.bonus();proche(t.xc,1.3,'cadence');
});
test('Orage Blanc — Maléfice : armure 0 et vitesse ×0,6 pendant 1,5 s, jamais sur un boss',()=>{const b=terrain(1);const c=fort(apparaitre(S,b,S.TURT));
 b.hit(c,0,TW(1,5),1);assert.ok(c.hx>0);proche(c.sf,.6,'vitesse');const hp=c.hp;b.hit(c,10,{n:'essai'},1);proche(hp-c.hp,10,'armure ignorée');
 const h=fort(apparaitre(S,b,S.BOSS[0]));b.hit(h,0,TW(1,5),1);assert.ok(!(h.hx>0));
});
test('Lunebois — poison : les doses ignorent l’armure ; Floraison les fait éclore d’un coup',()=>{const b=terrain(2);const c=fort(apparaitre(S,b,S.TURT));
 for(let i=0;i<5;i++)b.hit(c,0,TW(2,0),1);assert.equal(c.pz,5);let hp=c.hp;b.update(1);proche(hp-c.hp,5*TW(2,0).pv,'1 s de poison, sans armure',1e-3);
 hp=c.hp;const pz=c.pz,pd=c.pd,pt=c.pt;b.hit(c,0,TW(2,6),1);assert.equal(c.pz,0);assert.ok(hp-c.hp>=pz*pd*pt*TW(2,6).flo-1e-6,'Floraison');
});
test('Lunebois — Croissance : +1 % de dégâts et de portée toutes les 10 s, jusqu’à +25 %',()=>{const b=terrain(2);b.place(6,3,K(2,0));pret(b);const t=b.t[0];
 t.age=50;b.bonus();proche(S.dmg(t)/TW(2,0).d,1.05,'50 s');t.age=1e4;b.bonus();proche(S.rng(t)/TW(2,0).r,1.25,'plafond');
});
test('Hautroc — Forge : améliorations 15 % moins chères ; Brisé retire 15 % d’armure par point (Brèche à 5 points)',()=>{
 assert.equal(S.upCost({k:K(3,0),lv:1}),Math.round(TW(3,0).c*1.5*.85/5)*5);
 const b=terrain(3);const c=fort(apparaitre(S,b,S.TURT));for(let i=0;i<5;i++)b.hit(c,0,TW(3,2),1);assert.equal(c.bs,5);
 const hp=c.hp;b.hit(c,10,TW(3,3),1);proche(hp-c.hp,10*1.4-5*(1-.75),'Brèche, armure brisée');
});
test('Hautroc — Chauffe : une tour à tir continu surchauffe et s’arrête 2 s, sauf à côté d’une Enclume runique',()=>{const b=terrain(3);b.place(6,3,K(3,0));pret(b);const t=b.t[0];
 const c=fort(apparaitre(S,b,0));Object.assign(c,{x:6,y:4,tx:6,ty:4});c.im=99;c.imI=99;for(let i=0;i<200&&!(t.oh>0);i++)b.update(.05);assert.ok(t.oh>0,'surchauffe');
 const b2=terrain(3);b2.place(6,3,K(3,0));b2.place(5,3,K(3,7));pret(b2);const t2=b2.t[0];const c2=fort(apparaitre(S,b2,0));Object.assign(c2,{x:6,y:4,tx:6,ty:4});c2.im=99;c2.imI=99;
 for(let i=0;i<300;i++)b2.update(.05);assert.ok(!(t2.oh>0)&&t2.ht>.9,'pas de surchauffe');
});
test('Hautroc — Champ de mines : pose des mines sur le chemin ; un monstre au sol les fait exploser',()=>{const b=terrain(3);b.place(5,4,K(3,8));pret(b);
 for(let i=0;i<60;i++)b.update(.05);assert.ok(b.mi.length>=2,'mines posées');const m=b.mi[0],c=fort(apparaitre(S,b,0));Object.assign(c,{x:m.x,y:m.y,tx:m.x,ty:m.y});
 const n=b.mi.length;b.update(.01);assert.ok(c.hp<c.max&&b.mi.length<n);
});
test('Ossements — Âmes : un monstre tué près des tours donne 1 âme (2 s’il est Maudit) ; le Nécromancien relève un mort',()=>{const b=terrain(4);b.place(6,3,K(4,0));pret(b);
 let c=apparaitre(S,b,0);Object.assign(c,{x:6,y:4});c.hp=0;b.update(0);assert.equal(b.am,1);c=apparaitre(S,b,0);Object.assign(c,{x:6,y:4,ma:2});c.hp=0;b.update(0);assert.equal(b.am,3,'Récolte');
 b.place(7,3,K(4,6));pret(b);c=apparaitre(S,b,0);Object.assign(c,{x:6,y:4});c.hp=0;b.update(0);assert.equal(b.al.length,1,'mort relevé');assert.equal(b.am,3,'+1 âme, −1 pour le relever');
 const a=b.al[0],m=fort(apparaitre(S,b,3));Object.assign(m,{x:a.x,y:a.y+.2,tx:a.x,ty:a.y+.2});a.cd=0;b.update(.01);assert.ok(m.hp<m.max,'le mort frappe');
});
test('Ossements — peste : à la mort, elle saute sur les voisins (Épidémie : ×2 sur un Maudit)',()=>{const b=terrain(4);const a=apparaitre(S,b,0),v=fort(apparaitre(S,b,0));
 Object.assign(a,{x:6,y:5});Object.assign(v,{x:6,y:5.5,ma:3});b.hit(a,0,TW(4,3),1);a.hp=0;b.update(0);assert.ok(v.pe>0,'contaminé');
 const hp=v.hp;b.update(.5);assert.ok(hp-v.hp>=v.ped*2*.5-1e-6,'×2 sur un Maudit');
});
test('Faucheuse : exécute sous 12 % de PV, jamais un boss',()=>{const b=terrain(4);const c=apparaitre(S,b,3);c.hp=c.max*.11;b.hit(c,1,TW(4,8),1);assert.ok(c.hp<=0);
 const b2=terrain(4),h=apparaitre(S,b2,S.BOSS[0]);h.hp=h.max*.11;b2.hit(h,1,TW(4,8),1);assert.ok(h.hp>0);
});
test('États : etats(c) donne les états en bits pour l’affichage et l’instantané du serveur',()=>{const b=terrain(2);const c=fort(apparaitre(S,b,0));
 b.hit(c,0,TW(2,0),1);b.hit(c,0,TW(4,2),1);const e=S.etats(c);assert.ok(e&16,'poison');assert.ok(e&64,'Maudit');
});
/* les 4 terrains sont « humains » pour le moteur mais joués par l'IA, comme dans le banc des races */
test('IA : chaque race construit, améliore, et pose au moins une tour de soutien ou une ultime en 12 minutes',()=>{
 const G=partie(S,{factions:[0,1,2,3]}),G2=partie(S,{factions:[4,0,1,2]});
 for(const g of [G,G2]){const aiT=g.B.map((b,i)=>.6+i*.2);while(g.time<720&&!g.over){for(const b of g.B)if(!b.dead){aiT[b.i]-=.05;if(aiT[b.i]<=0){aiT[b.i]=.6;b.ai=1;S.aiAct(b);b.ai=0}}g.step(.05)}}
 for(const b of [...G.B,G2.B[0]]){const F=S.RACES[b.classId].name;if(b.dead&&b.st.mort<300)continue;
  assert.ok(b.t.length>=15,F+' : '+b.t.length+' tours');assert.ok(b.t.some(t=>t.lv>1),F+' : améliorations')}
 assert.ok([...G.B,...G2.B].some(b=>b.t.some(t=>S.TW[t.k].j==7||S.TW[t.k].u)),'soutien ou ultime posé');
});

test('Les cinq factions conservent leurs identifiants et ont 50 noms de tours distincts',()=>{
 assert.deepEqual(Array.from(S.RACES,f=>f.name),['Humains','Créatures','Herbe','Robots','Magique']);
 assert.equal(new Set(Array.from(S.TW,t=>t.n)).size,50);
});

test('Brûlure et poison ignorent l’armure et appliquent leur durée exacte, même entre deux pas',()=>{
 const b=terrain(3),c=fort(apparaitre(S,b,S.TURT));
 b.hit(c,0,TW(3,6),1);b.hit(c,0,TW(3,6),2);b.hit(c,0,TW(3,6),1);
 b.hit(c,0,TW(2,0),1);b.hit(c,0,TW(2,3),2);
 assert.equal(c.pz,3);assert.equal(c.bud,8);
 const hp=c.hp;
 for(let i=0;i<45;i++)b.update(.093);
 proche(hp-c.hp,8*2+3*1*4,'dégâts cumulés');
 assert.equal(c.pz,0);assert.equal(c.bud,0);
});

test('L’ultime Magique invoque un colosse quand les 15 âmes sont disponibles',()=>{
 const b=terrain(4);b.place(5,3,K(4,9));pret(b);fort(apparaitre(S,b,0));
 b.am=14;b.update(.05);assert.equal(b.al?.length||0,0);
 b.am=15;b.t[0].cd=0;b.update(.05);
 assert.equal(b.am,0);assert.equal(b.al.length,1);assert.equal(b.al[0].g,1);
});

test('Un projectile garde les coordonnées de sa tour après son premier déplacement',()=>{
 const b=terrain(0);b.place(5,2,K(0,0));pret(b);fort(apparaitre(S,b,0));
 b.update(.01);
 const p=b.pr[0];assert.ok(p);assert.equal(p.sx,5.5);
 assert.ok(p.sy<2.5);assert.notEqual(p.x,p.sx);
 const source=[p.sx,p.sy];b.update(.01);assert.deepEqual([p.sx,p.sy],source);
});

test('Les 50 tours, construites en jeu, produisent l’action ou le soutien de leur rôle',()=>{
 const attendus=[
  ['projectile','slash','projectile','projectile','zap','projectile','soutien','soutien','projectile','zap'],
  ['projectile','slash','projectile','projectile','zap','projectile','zap','soutien','projectile','zap'],
  ['projectile','boom','boom','projectile','projectile','projectile','projectile','soutien','projectile','boom'],
  ['projectile','boom','projectile','projectile','projectile','projectile','flame','soutien','mine','zap'],
  ['projectile','slash','projectile','projectile','projectile','projectile','projectile','soutien','projectile','invocation']
 ];
 for(let f=0;f<5;f++)for(let j=0;j<10;j++){
  const T=TW(f,j),b=terrain(f);assert.ok(b.place(5,3,K(f,j)),T.n);pret(b);b.am=15;b.t[0].stun=1;
  const c=fort(apparaitre(S,b,T.ao||T.ab?S.FLY[0]:0));c.x=6;c.y=3.25;c.tx=6;c.ty=4;
  if(T.rmin)c.y=4.5;
  b.t[0].stun=0;b.fx=[];b.update(.01);
  const a=attendus[f][j];
  if(a==='projectile')assert.equal(b.pr[0]?.k,K(f,j),T.n);
  else if(a==='mine')assert.ok(b.mi?.length===1||b.fx.some(e=>e.type==='boom'),T.n);
  else if(a==='invocation')assert.equal(b.al?.length,1,T.n);
  else if(a==='soutien')assert.ok(T.au||T.eco,T.n);
  else assert.ok(b.fx.some(e=>e.type===a),T.n+' : '+a);
 }
});

test('L’instantané multijoueur conserve les états et l’origine des tirs',async()=>{
 const {GameRoom}=await import('../../server/src/worker.js');
 const game=partie(S),b=game.B[0],c=fort(apparaitre(S,b,0));
 b.hit(c,0,TW(2,0),1);b.hit(c,0,TW(3,6),1);
 b.pr.push({id:42,k:0,x:5.75,y:2,tx:6.5,ty:4.25,tot:3,a:0,sx:5.5,sy:1.75});
 const snap=GameRoom.prototype.snap.call({game},true);
 assert.equal(snap.B[0].c[0][5]&(16|1024),16|1024);
 assert.deepEqual(Array.from(snap.B[0].p[0]),[42,0,5.75,2,6.5,4.25,3,0,5.5,1.75]);
});
