/* Économie : valeurs de départ, revenu toutes les 10 s, revenu gagné par envoi, bonus de difficulté des IA. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
const S=charger('actuel');

test('Départ : 100 or, +10 de revenu, 40 vies pour chaque terrain humain',()=>{const G=partie(S);
 for(const b of G.B)assert.deepEqual([b.gold,b.inc,b.lives,b.dead],[100,10,40,0]);
});
test('Difficulté : or de départ des IA +0 / +30 / +60, le joueur humain garde 100',()=>{
 [0,30,60].forEach((bonus,lv)=>{const G=partie(S,{ia:[0,1,1,1],difficulte:lv});assert.equal(G.B[0].gold,100);for(const b of G.B.slice(1))assert.equal(b.gold,100+bonus)});
});
test('Difficulté : revenu effectif des IA ×1 / ×1,25 / ×1,5 (arrondi), humain toujours ×1',()=>{
 [1,1.25,1.5].forEach((m,lv)=>{const G=partie(S,{ia:[0,1,1,1],difficulte:lv});for(const inc of [10,13,37]){G.B[1].inc=inc;G.B[0].inc=inc;assert.equal(G.eff(G.B[1]),Math.round(inc*m));assert.equal(G.eff(G.B[0]),inc)}});
});
test('Le revenu tombe toutes les 10 secondes',()=>{const G=partie(S);
 avancer(G,9.9);assert.equal(G.B[0].gold,100);avancer(G,.2);assert.equal(G.B[0].gold,110);assert.ok(G.log.some(l=>l.type=='income'));
 avancer(G,9.7);assert.equal(G.B[0].gold,110,'pas encore le 2e revenu à 19,8 s');avancer(G,.4);assert.equal(G.B[0].gold,120,'2e revenu à 20 s');
});
test('Le revenu versé aux IA tient compte de la difficulté',()=>{const G=partie(S,{ia:[0,1,1,1],difficulte:2});
 for(const b of G.B)b.aiT=1e9; // on empêche les IA de dépenser pour mesurer le versement seul
 const avant=G.B[1].gold;avancer(G,10.1);assert.equal(G.B[1].gold-avant,15);
});
test('Envoyer un monstre coûte son prix et augmente définitivement le revenu',()=>{
 for(let k=0;k<17;k++){const G=partie(S),b=G.B[0];G.time=1e4;b.gold=1e6;const inc=b.inc;
  assert.equal(G.action(0,{type:'send',k}),'',S.CR[k].n);assert.equal(b.gold,1e6-S.CR[k].c);assert.equal(b.inc,inc+S.CR[k].i,S.CR[k].n)}
});
test('Envoi refusé quand l\'or manque (« poor »), sans effet sur le revenu',()=>{const G=partie(S),b=G.B[0];
 assert.equal(G.action(0,{type:'send',k:S.CR.findIndex(T=>T.n=='Troll des glaces')}),'poor');assert.deepEqual([b.gold,b.inc],[100,10]);
});
