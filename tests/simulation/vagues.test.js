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
test('Monstres verrouillés avant leur heure (« locked »), disponibles ensuite',()=>{
 for(let k=0;k<17;k++){const at=S.CR[k].at||0;if(!at)continue;const G=partie(S);G.B[0].gold=1e6;
  G.time=at-.1;assert.equal(G.action(0,{type:'send',k}),'locked',S.CR[k].n);G.time=at;assert.equal(G.action(0,{type:'send',k}),'',S.CR[k].n)}
});
test('Le Petit limon ne peut pas être envoyé (« bad »)',()=>{const G=partie(S);G.B[0].gold=1e6;assert.equal(G.action(0,{type:'send',k:S.KID}),'bad')});

test('IA : chaque IA agit pour la première fois à 1 s + 0,2 s × son numéro de terrain, avec jusqu\'à 3 actions',()=>{const G=partie(S,{ia:[0,1,1,1]});
 avancer(G,1.15);assert.equal(G.B[1].t.length,0);avancer(G,.1);assert.equal(G.B[1].t.length,3,'IA 1 à 1,2 s : jusqu\'à 3 actions, donc 3 tours');assert.equal(G.B[2].t.length,0);avancer(G,.2);assert.equal(G.B[2].t.length,3,'IA 2 à 1,4 s');
});
test('IA : sa première tour est un Archer au centre de la rangée 8',()=>{const G=partie(S,{ia:[0,1,1,1],factions:[0,1,2,3]});avancer(G,2);
 for(const b of G.B.slice(1)){const t=b.t[0];assert.deepEqual([t.x,t.y,t.k],[6,8,b.classId*10])}
});
test('IA : aucune attaque pendant les 25 premières secondes',()=>{const G=partie(S,{ia:[0,1,1,1],difficulte:2});
 avancer(G,24.9);assert.equal(G.B[0].q.length+G.B[0].cr.length,0);
});
test('IA : elle finit par attaquer et par améliorer ses tours',()=>{const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e6;
 let recu=0;for(let i=0;i<4800&&!G.over;i++){G.step(.05);recu+=G.B[0].q.length}
 assert.ok(recu>0,'le joueur a reçu des monstres');assert.ok(G.B.slice(1).some(b=>b.t.some(t=>t.lv>1)),'au moins une tour améliorée');
});
