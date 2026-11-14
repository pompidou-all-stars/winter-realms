/* Tables d'équilibrage : le moteur actuel a exactement les mêmes chiffres que la référence 2.4,
   et les tours calculées respectent les formules écrites dans le code (vérification indépendante). */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {charger,RACINE}=require('../outils/moteur');
const S=charger('actuel');
const REF=JSON.parse(fs.readFileSync(path.join(RACINE,'tests','references','statistiques-v2.4.json'),'utf8'));
const clone=o=>JSON.parse(JSON.stringify(o));

test('Constantes du terrain et du jeu identiques à la référence',()=>{
 assert.deepEqual(clone({C:S.C,R:S.R,SP:S.SP,EX:S.EX,HPK:S.HPK,GRACE:S.GRACE,GROUP:S.GROUP,AURA_R:S.AURA_R}),REF.constantes);
});
test('Les 6 archétypes de tours (BASE_TW) sont identiques à la référence',()=>assert.deepEqual(clone(S.BASE_TW),REF.BASE_TW));
test('Les coefficients de faction (FACTION_BALANCE) sont identiques à la référence',()=>assert.deepEqual(clone(S.FACTION_BALANCE),REF.FACTION_BALANCE));
test('Les emplacements (ARCH) et les rôles (ROLE) sont identiques à la référence',()=>{assert.deepEqual(clone(S.ARCH),REF.ARCH);assert.deepEqual(clone(S.ROLE),REF.ROLE)});
test('Les niveaux de difficulté (DIFF) sont identiques à la référence',()=>assert.deepEqual(clone(S.DIFF),REF.DIFF));

test('Les 50 tours ont les mêmes statistiques que la référence, à chaque niveau',()=>{
 assert.equal(S.TW.length,50);
 for(const r of REF.tours){const T=S.TW[r.k];const {k,niveaux,...fiche}=r;
  assert.deepEqual(clone(T),fiche,`Tour n°${k} (${r.n}) différente de la référence`);
  for(const n of niveaux){assert.equal(S.dmg({k,lv:n.lv}),n.degats,`${r.n} : dégâts au niveau ${n.lv}`);assert.equal(S.rng({k,lv:n.lv}),n.portee,`${r.n} : portée au niveau ${n.lv}`);
   if(n.lv<5)assert.equal(S.upCost({k,lv:n.lv}),n.coutPourPasserAuSuivant,`${r.n} : coût d'amélioration au niveau ${n.lv}`)}}
});

test('Les 18 monstres (dont le Petit limon) ont les mêmes statistiques que la référence',()=>{
 assert.equal(S.CR.length,18);
 for(const r of REF.monstres){const {k,...fiche}=r;assert.deepEqual(clone(S.CR[k]),fiche,`Monstre n°${k} (${r.n}) différent de la référence`)}
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
