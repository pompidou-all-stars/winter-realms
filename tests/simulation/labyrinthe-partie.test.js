/* Labyrinthe de l'IA (2.5), en partie : sorti de labyrinthe.test.js en 2.34 pour tourner en parallèle (c'est le plus long, environ 5 s). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
const C=13;

test('En partie, l\'IA construit son plan, continue au-delà de 36 tours et n\'a pas de Mage avant la menace des Spectres',()=>{
 const S=charger('actuel',{graine:5});const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e9;const b=G.B[1];b.lives=1e9;
 avancer(G,140);assert.equal(b.t.filter(t=>S.TW[t.k].mg).length,0,'Mage avant 2:30');
 b.gold+=1e5;b.dp+=1e5;avancer(G,60);
 assert.ok(b.t.length>36,`seulement ${b.t.length} tours`);
 for(const t of b.t)assert.equal(b.mz.w[t.y*C+t.x],1,`tour hors du plan en (${t.x},${t.y})`);
});
