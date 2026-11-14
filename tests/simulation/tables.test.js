/* Tables d'équilibrage : les tours calculées respectent les formules écrites dans le code (vérification indépendante),
   et les tables ont la forme attendue. Les chiffres eux-mêmes peuvent changer librement (équilibrage). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger}=require('../outils/moteur');
const S=charger('actuel');

test('Les tables ont la forme attendue : 6 archétypes, 5 factions de 10 tours, 50 tours, 3 difficultés',()=>{
 assert.equal(S.BASE_TW.length,6);assert.equal(S.FACTIONS.length,5);for(const F of S.FACTIONS)assert.equal(F.towers.length,10);
 assert.equal(S.FACTION_BALANCE.length,5);assert.equal(S.ARCH.length,10);assert.equal(S.ROLE.length,10);assert.equal(S.TW.length,50);assert.equal(S.DIFF.length,3);
});
test('Chaque tour et chaque monstre a des statistiques valides (nombres positifs)',()=>{
 for(const T of S.TW)for(const f of ['c','d','r','cd'])assert.ok(Number.isFinite(T[f])&&T[f]>0,`${T.n} : ${f}`);
 for(const T of S.CR)for(const f of ['c','hp','s'])assert.ok(Number.isFinite(T[f])&&T[f]>0,`${T.n} : ${f}`);
});

/* Vérification indépendante : on recalcule chaque tour à partir des tables de base, avec les formules du code. */
test('Chaque tour est bien calculée à partir des tables de base (formules recalculées indépendamment)',()=>{
 const PUISSANCE=[1,1.08,.96,1.12,1.18,.92,1.22,1.30,1.16,1.38];
 const RETOUCHE={6:{d:.88,cd:.86,r:1.12},7:{d:1.08,cd:1.12},8:{d:.9},9:{d:1.08,r:1.08}};
 for(let f=0;f<5;f++)for(let j=0;j<10;j++){const T=S.TW[f*10+j],B=S.BASE_TW[S.ARCH[j]],F=S.FACTION_BALANCE[f],x=RETOUCHE[j]||{};
  const nom=`${T.n} (faction ${f}, emplacement ${j})`;
  assert.equal(T.c,Math.max(10,Math.round(B.c*PUISSANCE[j]*F.cost/5)*5),nom+' : coût');
  assert.equal(T.d,+(B.d*PUISSANCE[j]*F.dmg*(x.d||1)).toFixed(1),nom+' : dégâts');
  assert.equal(T.cd,+(B.cd*F.cd*(x.cd||1)).toFixed(3),nom+' : recharge');
  assert.equal(T.r,+(B.r*F.range*(x.r||1)).toFixed(2),nom+' : portée');
  assert.equal(T.skin,S.ARCH[j]);assert.equal(T.faction,f);assert.equal(T.n,S.FACTIONS[f].towers[j])}
});

test('Revenu gagné par envoi : formule du code (sol : courbe log ; autres : 6,5 % du coût)',()=>{
 for(const T of S.CR){const attendu=T.cat=='n'?Math.round(T.c/10*(1+.1*Math.log10(T.c/10))):Math.round(T.c*.065);assert.equal(T.i,attendu,T.n)}
});
