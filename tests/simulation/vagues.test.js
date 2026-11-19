/* Vagues : groupes de 4, destinataires, renforcement avec le temps, déblocages, comportement de l'IA. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
const S=charger('actuel');

test('Un envoi fait apparaître un groupe de 4 chez chaque adversaire encore en jeu, et rien chez soi',()=>{const G=partie(S);G.time=S.GRACE;
 G.action(0,{type:'send',k:0});assert.equal(G.B[0].q.length,0);
 for(const b of G.B.slice(1)){assert.equal(b.q.length,4);for(const s of b.q){assert.equal(s.k,0);assert.equal(s.m,1+S.GRACE/200);assert.ok(s.t>=0&&s.t<=.38*3+.25)}}
});
test('Les 4 monstres apparaissent en moins de 1,4 s, à la case de départ',()=>{const G=partie(S);G.time=S.GRACE;assert.equal(G.action(0,{type:'send',k:1}),'');
 avancer(G,1.4);for(const b of G.B.slice(1)){assert.equal(b.q.length,0);assert.equal(b.cr.length,4)}
});
test('Un terrain éliminé ne reçoit plus de vagues',()=>{const G=partie(S);G.time=S.GRACE;G.B[2].dead=1;G.action(0,{type:'send',k:0});
 assert.equal(G.B[2].q.length,0);assert.equal(G.B[1].q.length,4);
});
test('Les monstres se renforcent avec le temps : PV = PV de base × (1 + temps/200) × 0,55',()=>{
 for(const t of [S.GRACE,100,600]){const G=partie(S);G.time=t;G.B[0].gold=1e6;G.action(0,{type:'send',k:3});avancer(G,1.5);
  const m=1+t/200;assert.equal(G.B[1].cr.length,4);for(const c of G.B[1].cr){assert.equal(c.max,S.CR[3].hp*m*.55);assert.equal(c.hp,c.max)}}
});
test('Paliers (2.13) : 3 paliers de 24 monstres (12 au sol, 3 volants, 8 magiques, 1 boss)',()=>{
 const CAP=['aura','inv','split','acc','mi','heal','arm','stun'];
 for(const t of [1,2,3]){const L=S.CR.filter(T=>T.t==t&&T.cat!='x');assert.equal(L.length,24,'palier '+t);
  assert.equal(L.filter(T=>T.cat=='n').length,12);assert.equal(L.filter(T=>T.cat=='f').length,3);assert.equal(L.filter(T=>T.hero).length,1);
  const mag=L.filter(T=>T.cat=='s'&&!T.hero);assert.equal(mag.length,8);for(const f of CAP)assert.equal(mag.filter(T=>T[f]).length,1,'palier '+t+' : '+f)}
});
test('Paliers (2.13) : un monstre d’un palier fermé est refusé (« locked ») ; ouvrir un palier coûte PAL_C et débloque ses monstres',()=>{
 const G=partie(S),b=G.B[0];G.time=S.GRACE;b.gold=1e6;const k2=S.CR.findIndex(T=>T.t==2&&T.cat=='n'),k3=S.CR.findIndex(T=>T.t==3&&T.cat=='n');
 assert.equal(b.tier,1);assert.equal(G.action(0,{type:'send',k:k2}),'locked');
 let or=b.gold;assert.equal(G.action(0,{type:'tier'}),'');assert.equal(b.tier,2);assert.equal(b.gold,or-S.PAL_C[1]);
 assert.equal(G.action(0,{type:'send',k:k2}),'');assert.equal(G.action(0,{type:'send',k:k3}),'locked');
 or=b.gold;assert.equal(G.action(0,{type:'tier'}),'');assert.equal(b.gold,or-S.PAL_C[2]);assert.equal(G.action(0,{type:'send',k:k3}),'');
 assert.equal(G.action(0,{type:'tier'}),'max');
 const G2=partie(S);assert.equal(G2.action(0,{type:'tier'}),'poor');assert.equal(G2.B[0].tier,1);
});
test('Accéléré (2.13) : la vitesse grandit avec le temps de vie, jusqu’au plafond',()=>{
 const G=partie(S),b=G.B[0],k=S.CR.findIndex(T=>T.acc);b.q.push({k,m:1,t:0});b.update(0);const c=b.cr[0];c.hp=c.max=1e6;
 const y0=c.y;b.update(.05);const v0=(c.y-y0)/.05;c.age=100;const y1=c.y;b.update(.05);const v1=(c.y-y1)/.05;
 assert.ok(Math.abs(v1/v0-2)<.05,'vitesse ×2 au plafond, obtenu ×'+(v1/v0).toFixed(2));
});
test('Le Petit limon ne peut pas être envoyé (« bad »)',()=>{const G=partie(S);G.B[0].gold=1e6;assert.equal(G.action(0,{type:'send',k:S.KID}),'bad')});

test('IA : chaque IA agit pour la première fois à 1 s + 0,2 s × son numéro de terrain, avec jusqu\'à 3 actions',()=>{const G=partie(S,{ia:[0,1,1,1]});
 avancer(G,1.15);assert.equal(G.B[1].t.length,0);avancer(G,.1);assert.equal(G.B[1].t.length,3,'IA 1 à 1,2 s : jusqu\'à 3 actions, donc 3 tours');assert.equal(G.B[2].t.length,0);avancer(G,.2);assert.equal(G.B[2].t.length,3,'IA 2 à 1,4 s');
});
/* depuis la 2.5 (avant : un Archer au centre de la rangée 8) */
test('IA : sa première tour est une tour de sa faction, posée sur une case de son plan de labyrinthe',()=>{const G=partie(S,{ia:[0,1,1,1],factions:[0,1,2,3]});avancer(G,2);
 for(const b of G.B.slice(1)){const t=b.t[0];assert.ok(t,'aucune tour');assert.equal(Math.floor(t.k/10),b.classId);assert.equal(b.mz.w[t.y*13+t.x],1);assert.equal(t.y*13+t.x,b.mz.ord[0])}
});
test('IA : aucune attaque pendant les 30 premières secondes (phase « Construis »)',()=>{const G=partie(S,{ia:[0,1,1,1],difficulte:2});
 avancer(G,29.9);assert.equal(G.B[0].q.length+G.B[0].cr.length,0);
});
test('IA : elle finit par attaquer et par améliorer ses tours',()=>{const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e6;
 let recu=0;for(let i=0;i<4800&&!G.over;i++){G.step(.05);recu+=G.B[0].q.length}
 assert.ok(recu>0,'le joueur a reçu des monstres');assert.ok(G.B.slice(1).some(b=>b.t.some(t=>t.lv>1)),'au moins une tour améliorée');
});
/* depuis la 2.32 : fin de partie, défense au maximum */
test('IA : quand son plan est construit et toutes ses tours au niveau 5, son or de défense passe à l\'attaque',()=>{const G=partie(S,{ia:[0,1,1,1]});const b=G.B[1],M=S.mzStep(b,Infinity);
 b.gold=1e7;for(const i of M.ord)b.place(i%13,i/13|0,b.classId*10);for(const t of b.t){t.lv=5;t.b=0}
 assert.equal(b.t.length,M.ord.length,'plan complet');b.dp=5000;b.ap=0;b.gold=1000;b.lastG=1000;G.time=60;S.aiAct(b);S.aiAct(b);
 assert.equal(b.dp,0,'réserve de défense vidée');assert.ok(b.ap>0,'réserve d\'attaque remplie');
});
/* depuis la 2.32 : vagues composées selon ce que chaque adversaire peut encaisser */
const murCanons=(b,k)=>{b.gold=1e6;for(let x=0;x<12;x++)b.place(x,8,k);for(let x=1;x<13;x++)b.place(x,4,k);for(const t of b.t)t.b=0};
test('Estimation des défenses : un volant ne craint pas les Canons, un invisible rien sans Mage, un anti-magie rien contre les Mages',()=>{
 const G=partie(S),b=G.B[0],vol=S.FLY[1],sol=S.NORM[5],inv=S.SPEC,mi=S.BRK;murCanons(b,b.classId*10+3);
 assert.ok(S.encaisse(b,sol,1)>0,'les Canons touchent le sol');assert.equal(S.encaisse(b,vol,1),0,'les Canons ne touchent pas les airs');
 assert.equal(S.encaisse(b,inv,1),0,'invisible sans Mage');
 const G2=partie(S),b2=G2.B[0];murCanons(b2,b2.classId*10+5);assert.ok(S.encaisse(b2,inv,1)>0,'les Mages révèlent et frappent');assert.equal(S.encaisse(b2,mi,1),0,'anti-magie contre des Mages');
});
test('IA : contre des adversaires qui n\'ont que des Canons, l\'essentiel de sa vague (en or) est ce qu\'ils ne peuvent pas toucher (volants ou invisibles)',()=>{
 const G=partie(S,{ia:[0,1,0,0]});for(const i of [0,2,3])murCanons(G.B[i],G.B[i].classId*10+3);
 const A=G.B[1];G.time=60;A.gold=A.ap=600;A.inc=10;const env=[];const o=G.send.bind(G);G.send=(f,k)=>{const r=o(f,k);if(r)env.push(k);return r};
 S.aiAttack(A);assert.ok(env.length>0,'aucun envoi');const or=f=>env.filter(f).reduce((a,k)=>a+S.CR[k].c,0);
 assert.ok(or(k=>S.CR[k].fly||S.CR[k].inv)>=or(()=>1)/2,env.map(k=>S.CR[k].n).join(', '));
});
