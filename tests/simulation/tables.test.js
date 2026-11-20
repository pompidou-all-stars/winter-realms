/* Tables d'équilibrage : forme des tables et cohérence des 50 tours avec leur définition dans RACES (2.40).
   Les chiffres eux-mêmes peuvent changer librement (équilibrage) ; les règles d'équilibrage sont vérifiées dans races.test.js. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger}=require('../outils/moteur');
const S=charger('actuel');

test('Les tables ont la forme attendue : 6 archétypes de dessin, 5 races de 10 tours, 10 rôles, 50 tours, 3 difficultés',()=>{
 assert.equal(S.BASE_TW.length,6);assert.equal(S.RACES.length,5);assert.equal(S.FACTIONS,S.RACES);for(const F of S.RACES){assert.equal(F.tours.length,10);assert.equal(F.towers.length,10)}
 assert.equal(S.ROLES_J.length,10);assert.equal(S.TW.length,50);assert.equal(S.DIFF.length,3);
});
test('Chaque tour et chaque monstre a des statistiques valides (nombres positifs)',()=>{
 for(const T of S.TW){for(const f of ['c','r','cd'])assert.ok(Number.isFinite(T[f])&&T[f]>0,`${T.n} : ${f}`);
  assert.ok(T.no?T.d===0:Number.isFinite(T.d)&&T.d>0,`${T.n} : dégâts`);assert.ok(Number.isFinite(T.ed)&&T.ed>=0&&Number.isFinite(T.zf)&&T.zf>0,`${T.n} : estimation`);
  assert.equal(T.c%5,0,`${T.n} : prix multiple de 5`);assert.ok(T.txt&&T.txt.length>10,`${T.n} : description`)}
 for(const T of S.CR)for(const f of ['c','hp','s'])assert.ok(Number.isFinite(T[f])&&T[f]>0,`${T.n} : ${f}`);
});
test('Chaque tour reprend sa définition (RACES), sa race, son emplacement et son rôle',()=>{
 for(let f=0;f<5;f++)for(let j=0;j<10;j++){const T=S.TW[f*10+j],o=S.RACES[f].tours[j],nom=`${T.n} (race ${f}, emplacement ${j})`;
  assert.equal(T.n,o.n,nom);assert.equal(T.c,o.c,nom+' : prix');assert.equal(T.r,o.r,nom+' : portée');assert.equal(T.d,o.no?0:o.d,nom+' : dégâts');
  assert.equal(T.faction,f);assert.equal(T.j,j);assert.equal(T.role,S.ROLES_J[j].name);assert.equal(T.skin,o.skin);assert.equal(T.mg,o.det?1:0,nom+' : détection')}
});

test('Revenu gagné par envoi : formule du code (sol : courbe log ; autres : 6,5 % du coût)',()=>{
 for(const T of S.CR){const attendu=T.cat=='n'?Math.floor(T.c/10*(1+.1*Math.log10(T.c/10))+1e-9):Math.round(T.c*.065);assert.equal(T.i,attendu,T.n)}
 /* 2.14 : coûts en dizaines, et aucun monstre au sol ne dépasse la courbe 10 → 1, 100 → 11, 1000 → 120 */
 for(const T of S.CR){assert.equal(T.c%10,0,T.n+' : coût en dizaines');if(T.cat=='n')assert.ok(T.i<=T.c/10*(1+.1*Math.log10(T.c/10))+1e-9,T.n+' : sous la courbe')}
 for(const[c,i]of[[10,1],[100,11],[1000,120]]){const T=S.CR.find(U=>U.cat=='n'&&U.c==c);if(T)assert.equal(T.i,i,T.n)}
});
