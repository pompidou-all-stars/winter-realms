/* Vagues : groupes de 4, destinataires, renforcement avec le temps, déblocages, comportement de l'IA. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
const S=charger('actuel');

test('Un envoi fait apparaître un groupe de 4 chez chaque adversaire encore en jeu, et rien chez soi',()=>{const G=partie(S);
 G.action(0,{type:'send',k:0});assert.equal(G.B[0].q.length,0);
 for(const b of G.B.slice(1)){assert.equal(b.q.length,4);for(const s of b.q){assert.equal(s.k,0);assert.equal(s.m,1);assert.ok(s.t>=0&&s.t<=.38*3+.25)}}
});
test('Les 4 monstres apparaissent en moins de 1,4 s, à la case de départ',()=>{const G=partie(S);assert.equal(G.action(0,{type:'send',k:1}),'');
 avancer(G,1.4);for(const b of G.B.slice(1)){assert.equal(b.q.length,0);assert.equal(b.cr.length,4)}
});
test('Un terrain éliminé ne reçoit plus de vagues',()=>{const G=partie(S);G.B[2].dead=1;G.action(0,{type:'send',k:0});
 assert.equal(G.B[2].q.length,0);assert.equal(G.B[1].q.length,4);
});
test('Les monstres se renforcent avec le temps : PV = PV de base × (1 + temps/200) × 0,55',()=>{
 for(const t of [0,100,600]){const G=partie(S);G.time=t;G.B[0].gold=1e6;G.action(0,{type:'send',k:3});avancer(G,1.5);
  const m=1+t/200;for(const c of G.B[1].cr){assert.equal(c.max,S.CR[3].hp*m*.55);assert.equal(c.hp,c.max)}}
});
test('Paliers (2.13) : 3 paliers de 24 monstres (12 au sol, 3 volants, 8 magiques, 1 boss)',()=>{
 const CAP=['aura','inv','split','acc','mi','heal','arm','stun'];
 for(const t of [1,2,3]){const L=S.CR.filter(T=>T.t==t&&T.cat!='x');assert.equal(L.length,24,'palier '+t);
  assert.equal(L.filter(T=>T.cat=='n').length,12);assert.equal(L.filter(T=>T.cat=='f').length,3);assert.equal(L.filter(T=>T.hero).length,1);
  const mag=L.filter(T=>T.cat=='s'&&!T.hero);assert.equal(mag.length,8);for(const f of CAP)assert.equal(mag.filter(T=>T[f]).length,1,'palier '+t+' : '+f)}
});
test('Paliers (2.13) : un monstre d’un palier fermé est refusé (« locked ») ; ouvrir un palier coûte PAL_C et débloque ses monstres',()=>{
 const G=partie(S),b=G.B[0];b.gold=1e6;const k2=S.CR.findIndex(T=>T.t==2&&T.cat=='n'),k3=S.CR.findIndex(T=>T.t==3&&T.cat=='n');
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
test('IA : aucune attaque pendant les 25 premières secondes',()=>{const G=partie(S,{ia:[0,1,1,1],difficulte:2});
 avancer(G,24.9);assert.equal(G.B[0].q.length+G.B[0].cr.length,0);
});
test('IA : elle finit par attaquer et par améliorer ses tours',()=>{const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e6;
 let recu=0;for(let i=0;i<4800&&!G.over;i++){G.step(.05);recu+=G.B[0].q.length}
 assert.ok(recu>0,'le joueur a reçu des monstres');assert.ok(G.B.slice(1).some(b=>b.t.some(t=>t.lv>1)),'au moins une tour améliorée');
});
