/* Temps de construction (depuis la 2.4) : durée selon l'or dépensé et la difficulté, tour inactive pendant le chantier. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre,avancerTerrain,pret}=require('../outils/moteur');
const S=charger('actuel');
const proche=(a,b,msg)=>assert.ok(Math.abs(a-b)<1e-9,`${msg||''} attendu ${b}, obtenu ${a}`);
const nouveau=(difficulte=0,ia=[0,0,0,0])=>{const G=partie(S,{difficulte,ia});for(const b of G.B)b.gold=1e6;return {G,b:G.B[0]}};

test('Durée = min(8, max(0,5, prix / 50)) secondes, à la pose (Normal)',()=>{const {G,b}=nouveau();
 for(const [x,k] of [[1,0],[3,5],[5,9]]){const attendu=Math.min(8,Math.max(.5,S.TW[k].c/50));G.action(0,{type:'place',x,y:3,k});const t=b.t.at(-1);proche(t.bt,attendu,S.TW[k].n);proche(t.b,attendu)}
});
test('Une amélioration prend le temps de son prix, plafonné à 8 s',()=>{const {G,b}=nouveau();G.action(0,{type:'place',x:3,y:3,k:9});const t=b.t[0];pret(b);
 G.action(0,{type:'upgrade',x:3,y:3});proche(t.bt,Math.min(8,S.upCost({k:9,lv:1})/50));assert.equal(t.lv,2);
});
test('Difficulté : les humains construisent ×1 / ×1,25 / ×1,5, les IA restent à ×1',()=>{
 for(const [lv,m] of [[0,1],[1,1.25],[2,1.5]]){const {b,G}=nouveau(lv,[0,1,1,1]);G.action(0,{type:'place',x:3,y:3,k:9});proche(b.t[0].bt,Math.min(8,Math.max(.5,S.TW[9].c/50))*m,'humain, difficulté '+lv);
  const ia=G.B[1];ia.place(3,3,19);proche(ia.t[0].bt,Math.min(8,Math.max(.5,S.TW[19].c/50)),'IA, difficulté '+lv)}
});
test('Pendant le chantier : pas de tir, amélioration refusée (« busy »), la case bloque déjà le chemin',()=>{const {G,b}=nouveau();
 G.action(0,{type:'place',x:5,y:4,k:0});const t=b.t[0];assert.equal(b.g[4][5],1);
 assert.equal(G.action(0,{type:'upgrade',x:5,y:4}),'busy');assert.equal(t.lv,1);
 const c=apparaitre(S,b,0);c.hp=c.max=1e6;Object.assign(c,{x:6,y:4,tx:6,ty:4});b.update(.01);assert.equal(b.pr.length,0,'aucun projectile pendant le chantier');
 pret(b);Object.assign(c,{x:6,y:4,tx:6,ty:4});b.update(.01);assert.equal(b.pr.length,1,'la tour tire une fois prête');
});
test('Pendant le chantier : une tour Mage ne révèle pas les Spectres, et la tour n\'est pas étourdie',()=>{const {G,b}=nouveau();
 G.action(0,{type:'place',x:5,y:2,k:5});const s=apparaitre(S,b,S.SPEC);s.hp=s.max=1e6;b.update(.01);assert.equal(s.hid,true);
 const sab=apparaitre(S,b,S.SAP);sab.hp=sab.max=1e6;Object.assign(sab,{x:5,y:3,tx:5,ty:3,cs:0});b.update(.01);assert.ok(!(b.t[0].stun>0));
});
test('Une tour en chantier se vend au tarif normal (70 %)',()=>{const {G,b}=nouveau();G.action(0,{type:'place',x:3,y:3,k:9});const or=b.gold;
 assert.equal(G.action(0,{type:'sell',x:3,y:3}),'');assert.equal(b.gold-or,Math.floor(S.TW[9].c*.7));
});
