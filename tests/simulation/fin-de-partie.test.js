/* Fin de partie : élimination, victoire, défaite, actions après la fin. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre}=require('../outils/moteur');
const S=charger('actuel');

test('Un terrain à 0 vie est éliminé, vidé, et l\'élimination est annoncée',()=>{const G=partie(S),b=G.B[1];
 apparaitre(S,b,3);G.action(0,{type:'send',k:0});b.lives=0;G.step(.05);
 assert.equal(b.dead,1);assert.deepEqual([b.cr.length,b.q.length,b.pr.length],[0,0,0]);assert.ok(G.log.some(l=>l.type=='out'&&l.i==1));assert.equal(G.over,false);
});
test('Victoire : il ne reste qu\'un terrain debout',()=>{const G=partie(S,{ia:[0,1,1,1]});for(const b of G.B.slice(1))b.lives=0;G.step(.05);
 assert.equal(G.over,true);assert.equal(G.winner,0);assert.ok(G.log.some(l=>l.type=='end'&&l.winner==0));
});
test('Défaite en solo : le joueur humain tombe, la partie s\'arrête sans vainqueur (−1)',()=>{const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=0;G.step(.05);
 assert.equal(G.over,true);assert.equal(G.winner,-1);
});
test('Avec plusieurs humains, la partie continue tant qu\'il en reste un en jeu',()=>{const G=partie(S,{ia:[0,0,1,1]});G.B[0].lives=0;G.step(.05);
 assert.equal(G.over,false);G.B[1].lives=0;G.step(.05);assert.equal(G.over,true);assert.equal(G.winner,-1);
});
test('Après la fin : toute action est refusée (« over ») et le temps ne s\'écoule plus',()=>{const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=0;G.step(.05);
 const t=G.time;G.step(.05);assert.equal(G.time,t);assert.equal(G.action(0,{type:'place',x:1,y:1,k:0}),'over');
});
test('Comportement constaté : plusieurs fuites simultanées font passer les vies sous zéro',()=>{const G=partie(S),b=G.B[0];b.lives=1;
 for(let i=0;i<3;i++){const c=apparaitre(S,b,0);Object.assign(c,{x:6,y:16,tx:6,ty:16})}
 b.update(.05);assert.equal(b.lives,-2);G.step(.05);assert.equal(b.dead,1);
});
test('Statistiques de fin de partie (2.23) : tours posées, envois, monstres tués, revenu à chaque versement, moment de l\'élimination',()=>{const G=partie(S,{ia:[0,1,1,1]}),P=G.B[0];
 assert.equal(G.action(0,{type:'place',x:1,y:1,k:0}),'');assert.equal(G.action(0,{type:'send',k:0}),'');
 assert.equal(P.st.pose,1);assert.equal(P.st.env,1);assert.equal(P.st.envOr,S.CR[0].c);
 const c=apparaitre(S,P,0);c.hp=0;P.update(.05);assert.equal(P.st.tue,1);
 for(let i=0;i<201;i++)G.step(.05);assert.deepEqual([...P.st.rev],[G.eff(P)]);
 G.B[2].lives=0;G.step(.05);assert.ok(Math.abs(G.B[2].st.mort-G.time)<1e-9);assert.equal(G.B[1].st.mort,-1);
});
