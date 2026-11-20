/* Combats : ciblage, restrictions sol/air/magie, armure, bonus de faction, capacités des monstres, primes. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre,avancerTerrain,pret}=require('../outils/moteur');
const S=charger('actuel');
const proche=(a,b,msg,eps=1e-9)=>assert.ok(Math.abs(a-b)<=eps,`${msg||''} attendu ${b}, obtenu ${a}`);
const terrain=(f=0)=>{const b=partie(S,{factions:[f,(f+1)%5,(f+2)%5,(f+3)%5]}).B[0];b.gold=1e6;return b};
const perte=(b,c,d,k,lv)=>{const hp=c.hp;b.hit(c,d,S.TW[k],lv);return hp-c.hp};
const fort=c=>{c.hp=c.max=1e6;return c};
const TROLL=S.CR.findIndex(T=>T.n=='Troll des glaces');

test('Une tour Archer tue un Sapeur gobelin et gagne la prime de 1 or',()=>{const b=terrain();b.place(5,4,0);const or=b.gold;
 apparaitre(S,b,0);avancerTerrain(b,6);assert.equal(b.cr.length,0);assert.equal(b.lives,40);assert.equal(b.gold,or+1);
});
test('Prime = max(1, arrondi(coût / 10)), versée au terrain où le monstre meurt',()=>{const b=terrain();
 for(const k of [0,1,3,5,8,16]){const c=apparaitre(S,b,k),or=b.gold;c.hp=0;b.update(0);assert.equal(b.gold-or,Math.max(1,Math.round(S.CR[k].c/10)),S.CR[k].n);b.cr=[]}
});
test('Ciblage : la tour vise le monstre visible le plus proche de la sortie',()=>{const b=terrain();b.place(5,4,0);pret(b);
 const a=fort(apparaitre(S,b,0)),c=fort(apparaitre(S,b,0));Object.assign(a,{x:6,y:3,tx:6,ty:3});Object.assign(c,{x:6,y:5,tx:6,ty:5});
 b.update(.01);assert.equal(b.pr.length,1);assert.equal(b.pr[0].tg,c);
});
test('Canon et Garde ne touchent pas les volants',()=>{for(const k of [1,3]){const b=terrain();b.place(5,5,k);b.place(7,8,k);
 const c=fort(apparaitre(S,b,S.FLY[0]));const pv=c.hp;let tirs=0;for(let i=0;i<120;i++){b.update(.05);tirs+=b.pr.length}
 assert.equal(c.hp,pv,S.TW[k].n);assert.equal(tirs,0,S.TW[k].n)}
});
test('Archer et Flammes touchent les volants',()=>{for(const k of [0,4]){const b=terrain();b.place(5,4,k);
 const c=fort(apparaitre(S,b,S.FLY[0]));avancerTerrain(b,3);assert.ok(c.hp<c.max,S.TW[k].n)}
});
test('Anti-magie : les tours magiques n\'ont aucun effet sur le Briseur de runes, et ne le ciblent pas',()=>{const b=terrain();
 const c=apparaitre(S,b,S.BRK);for(const k of S.TW.map((T,k)=>k).filter(k=>S.TW[k].mag))assert.equal(perte(b,c,50,k,1),0,S.TW[k].n);assert.equal(c.sl,0);
 assert.ok(perte(b,c,1,0)>0,'un Archer le touche');
 const b2=terrain();b2.place(5,2,5);pret(b2);fort(apparaitre(S,b2,S.BRK));b2.update(.01);assert.equal(b2.pr.length,0);
});
test('Armure : retire un montant fixe par coup mais garde au moins 20 % des dégâts',()=>{const b=terrain(1);const c=fort(apparaitre(S,b,S.TURT));
 assert.equal(c.arm,5);proche(perte(b,c,10,10),5,'10 dégâts − 5');proche(perte(b,c,3,10),.6,'3 dégâts → plancher de 20 %');
});
test('Armure : elle grandit avec le temps comme les PV (× 1 + temps/200)',()=>{const b=terrain();const c=apparaitre(S,b,S.TURT,1.5);assert.equal(c.arm,7.5)});
/* 2.40 : les anciens bonus de faction (perforant, anti-aérien, frénésie, malédiction) sont remplacés par les mécaniques des races : voir races.test.js */
test('Trébuchet (zone au sol) : 60 % des dégâts autour, dans son rayon, sol uniquement',()=>{const b=terrain();
 const a=fort(apparaitre(S,b,0)),v=fort(apparaitre(S,b,0)),loin=fort(apparaitre(S,b,0)),vol=fort(apparaitre(S,b,S.FLY[0]));
 for(const [c,x,y] of [[a,6,5],[v,6.5,5.5],[loin,6,7],[vol,6.3,5.2]])Object.assign(c,{x,y,tx:6,ty:5});
 const hp=[a,v,loin,vol].map(c=>c.hp);b.impact({k:3,tg:a,d:10,tx:a.x+.5,ty:a.y+.5,lv:1});
 proche(hp[0]-a.hp,10,'cible');proche(hp[1]-v.hp,6,'voisin');assert.equal(loin.hp,hp[2],'trop loin');assert.equal(vol.hp,hp[3],'volant épargné');
});
test('Spectre : invisible sauf à portée d\'une tour Mage ; un Spectre caché n\'est ni ciblé ni touché par les explosions',()=>{const b=terrain();
 b.place(5,2,0);pret(b);const s=fort(apparaitre(S,b,S.SPEC));b.update(.01);assert.equal(s.hid,true);assert.equal(b.pr.length,0);
 const a=fort(apparaitre(S,b,0));Object.assign(a,{x:s.x,y:s.y});const pv=s.hp;b.impact({k:3,tg:a,d:10,tx:s.x+.5,ty:s.y+.5,lv:1});assert.equal(s.hp,pv);
 const b2=terrain();b2.place(5,2,5);pret(b2);const s2=fort(apparaitre(S,b2,S.SPEC));b2.update(.01);assert.equal(s2.hid,false);assert.equal(b2.pr.length,1);
});
test('Saboteur : 2 s après son apparition, étourdit 2 s la tour la plus proche (rayon 2,3)',()=>{const b=terrain();b.place(5,3,1);b.place(9,9,0);
 const s=fort(apparaitre(S,b,S.SAP));avancerTerrain(b,1.9);assert.ok(!(b.t[0].stun>0));
 avancerTerrain(b,.15);assert.ok(b.t[0].stun>1.8,'la tour proche est étourdie');assert.ok(!(b.t[1].stun>0),'la tour lointaine ne l\'est pas');
 const cd=b.t[0].cd;b.update(.5);assert.equal(b.t[0].cd,cd,'une tour étourdie ne recharge pas');
});
test('Gelée mutante : se divise en 2 Petits limons à sa mort',()=>{const b=terrain();const c=apparaitre(S,b,S.SPLIT,2);c.hp=0;b.update(0);
 assert.equal(b.cr.length,2);for(const k of b.cr){assert.equal(k.k,S.KID);proche(k.hp,S.CR[S.KID].hp*(c.max/S.CR[S.SPLIT].hp),'PV du limon')}
});
test('Prêtresse : soigne de 5 % des PV max par seconde les alliés proches, pas elle-même',()=>{const b=terrain();
 const p=apparaitre(S,b,S.HEAL),g=fort(apparaitre(S,b,TROLL));g.hp=g.max/2;p.hp=p.max/2;b.update(.1);
 proche(g.hp,g.max/2+g.max*.05*.1,'allié soigné',1e-6);assert.equal(p.hp,p.max/2,'la prêtresse seule n\'est pas soignée');
});
test('Garde : frappe directe au corps à corps, sans projectile',()=>{const b=terrain();b.place(5,1,1);pret(b);const c=fort(apparaitre(S,b,TROLL));
 avancerTerrain(b,.7);assert.ok(c.hp<c.max);assert.equal(b.pr.length,0);
});
