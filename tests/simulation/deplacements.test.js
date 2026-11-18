/* Déplacements : chemin au sol, vol en ligne droite, sortie, ralentissements, hâte. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre,avancerTerrain,pret}=require('../outils/moteur');
const S=charger('actuel');
const proche=(a,b,msg,eps=1e-9)=>assert.ok(Math.abs(a-b)<=eps,`${msg||''} attendu ${b}, obtenu ${a}`);
const terrain=(factions=[0,1,2,3])=>partie(S,{factions}).B[0];

test('Un Sapeur gobelin (vitesse 1,6) parcourt les 16 cases en 10 s et retire 1 vie à la sortie',()=>{const b=terrain();apparaitre(S,b,0);
 avancerTerrain(b,9.9);assert.equal(b.lives,40);assert.equal(b.cr.length,1);
 avancerTerrain(b,.3);assert.equal(b.lives,39);assert.equal(b.cr.length,0);assert.ok(b.ev.includes('!leak'));
});
test('Un volant va en ligne droite vers la sortie (Chauve-souris, vitesse 2 : 8 s) et ignore les tours',()=>{const b=terrain();b.gold=1e6;
 for(const y of [3,5,7,9])b.place(6,y,0);
 const c=apparaitre(S,b,S.FLY[0]);c.hp=c.max=1e9;for(let i=0;i<150;i++){b.update(.05);if(b.cr.length)assert.equal(c.x,6)}
 assert.equal(b.lives,40);avancerTerrain(b,.6);assert.equal(b.lives,39);
});
test('Un monstre au sol contourne les tours, sans jamais entrer sur une case occupée',()=>{const b=terrain();b.gold=1e6;
 for(let x=0;x<12;x++)b.place(x,4,0);for(let x=1;x<13;x++)b.place(x,9,0);
 const c=apparaitre(S,b,0);c.hp=c.max=1e9;let t=0;
 while(b.cr.length&&t<60){b.update(.05);t+=.05;assert.equal(b.g[c.ty][c.tx],0,`case (${c.tx},${c.ty}) occupée`);assert.equal(b.g[Math.round(c.y)][Math.round(c.x)],0,`monstre sur une tour en (${c.x},${c.y})`)}
 assert.equal(b.lives,39);assert.ok(t>10,'le détour doit prendre plus de 10 s');
});
test('Diagonale : sur un terrain ouvert, un monstre parti du coin haut gauche file en ligne droite vers la sortie',()=>{const b=terrain();
 const c=apparaitre(S,b,0);c.hp=c.max=1e9;Object.assign(c,{x:0,y:0,tx:0,ty:0});
 for(let i=0;i<40;i++){b.update(.05);proche(c.x/6,c.y/16,'sur la droite (0,0) → (6,16)',.03)}
});
test('Diagonale : le monstre coupe le virage en biais au lieu de longer les murs à angle droit',()=>{const b=terrain();b.gold=1e6;
 for(let x=1;x<13;x++)b.place(x,3,0);const c=apparaitre(S,b,0);c.hp=c.max=1e9;let t=0,obl=0;
 while(b.cr.length&&t<30){const x=c.x,y=c.y;b.update(.05);t+=.05;if(Math.abs(c.x-x)>1e-6&&Math.abs(c.y-y)>1e-6)obl++}
 assert.equal(b.lives,39);assert.ok(obl>100,`déplacement en biais la plupart du temps (${obl} pas)`);
 /* en 4 directions : 6 + 16 = 22 cases, soit 13,75 s à 1,6 case/s ; en ligne droite : environ 6,3 + 1,7 + 13,4 ≈ 21,4 cases */
 assert.ok(t<13.6,`trajet en ${t.toFixed(2)} s`);
});
test('Vitesse ralentie : déplacement = vitesse × facteur × temps',()=>{const b=terrain();const c=apparaitre(S,b,0);
 c.sl=10;c.sf=.5;b.update(.5);proche(c.y,1.6*.5*.5,'position');
});
test('Givre : ralentit à ×0,5 au niveau 1 et ×0,3 au niveau 5, pendant 1,5 s',()=>{const b=terrain();const c=apparaitre(S,b,3),T=S.TW[2];
 b.hit(c,0,T,.5-.05*0);assert.equal(c.sf,.5);assert.equal(c.sl,1.5);
 const c2=apparaitre(S,b,3);b.hit(c2,0,T,.5-.05*4);assert.equal(c2.sf,.5-.05*4);
});
test('Givre : le facteur de ralentissement vient du niveau de la tour qui tire',()=>{const G=partie(S),b=G.B[0];b.gold=1e6;
 b.place(5,3,2);const t=b.t[0];pret(b);for(let i=0;i<4;i++){b.upgrade(t);pret(b)}const c=apparaitre(S,b,3);c.hp=c.max=1e9;
 avancerTerrain(b,3);assert.ok(c.sl>0);assert.equal(c.sf,.5-.05*4);
});
test('Racines sylvestres : toutes leurs tours ralentissent à ×0,82 pendant 0,72 s',()=>{const b=terrain([2,0,1,3]);
 for(const k of [20,21,23,24,25,26,27,29]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[k],.5);assert.equal(c.sf,.82,S.TW[k].n);assert.equal(c.sl,.72,S.TW[k].n)}
});
test('Racines : le ralentissement le plus fort reste appliqué, la durée la plus longue est retenue',()=>{const b=terrain([2,0,1,3]);const c=apparaitre(S,b,3);
 b.hit(c,0,S.TW[22],.5);assert.deepEqual([c.sf,c.sl],[.5,1.5]);
 b.hit(c,0,S.TW[20],.5);assert.deepEqual([c.sf,c.sl],[.5,1.5],'les racines n\'écrasent pas le Givre');
 c.sl=0;b.hit(c,0,S.TW[20],.5);assert.deepEqual([c.sf,c.sl],[.82,.72],'ralentissement expiré : les racines s\'appliquent');
});
test('Les autres factions ne ralentissent qu\'avec le Givre',()=>{const b=terrain();
 for(const f of [0,1,3,4])for(const j of [0,1,3,4,5,6,7,9]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[f*10+j],.5);assert.equal(c.sl,0,S.TW[f*10+j].n)}
});
test('Garde et Flammes sylvestres : le monstre continue d\'avancer normalement (pas de vitesse invalide)',()=>{const b=terrain([2,0,1,3]);
 for(const k of [21,24]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[k]);const y=c.y;b.update(.5);assert.ok(Number.isFinite(c.y)&&c.y>y,S.TW[k].n)}
});
test('Hâte du Chaman : les alliés proches vont 1,4 fois plus vite, pas le Chaman lui-même',()=>{const b=terrain();
 const ch=apparaitre(S,b,S.AURA),g=apparaitre(S,b,0);b.update(.1);
 assert.equal(g.h,true);assert.equal(ch.h,false);proche(g.y,1.6*1.4*.1,'gobelin accéléré');proche(ch.y,CRs(S.AURA)*.1,'chaman non accéléré');
});
function CRs(k){return S.CR[k].s}
