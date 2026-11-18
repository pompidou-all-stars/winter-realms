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
 while(b.cr.length&&t<60){b.update(.05);t+=.05;assert.equal(b.g[c.ty][c.tx],0,`case (${c.tx},${c.ty}) occupée`)}
 assert.equal(b.lives,39);assert.ok(t>10,'le détour doit prendre plus de 10 s');
});
test('Vitesse ralentie : déplacement = vitesse × facteur × temps',()=>{const b=terrain();const c=apparaitre(S,b,0);
 c.gt=10;c.gp=.5;b.update(.5);proche(c.y,1.6*.5*.5,'position');
});
test('Givre : de −20 % (niveau 1) à −50 % (niveau 5), pendant 1,5 s à 2,7 s',()=>{const b=terrain(),T=S.TW[2];
 const att=[[.8,1.5],[.725,1.8],[.65,2.1],[.575,2.4],[.5,2.7]];
 for(let lv=1;lv<=5;lv++){const c=apparaitre(S,b,3);b.hit(c,0,T,lv);proche(c.sf,att[lv-1][0],'vitesse niveau '+lv);proche(c.sl,att[lv-1][1],'durée niveau '+lv)}
});
test('Givre : la zone d’effet passe de 1,2 case (niveau 1) à 2 cases (niveau 5)',()=>{
 for(const [lv,ralenti] of [[1,false],[5,true]]){const b=terrain();const a=apparaitre(S,b,0),v=apparaitre(S,b,0);a.hp=a.max=v.hp=v.max=1e9;
  Object.assign(a,{x:6,y:5,tx:6,ty:5});Object.assign(v,{x:6,y:6.8,tx:6,ty:7});
  b.impact({k:2,tg:a,d:1,tx:a.x+.5,ty:a.y+.5,lv});assert.ok(a.sl>0,'cible');assert.equal(v.sl>0,ralenti,'voisin à 1,8 case, niveau '+lv);
  const z=b.fx.find(f=>f.type=='boom');proche(z.r,S.GIVRE_LV.r[lv-1],'rayon affiché')}
});
test('Givre : le ralentissement vient du niveau de la tour qui tire',()=>{const G=partie(S),b=G.B[0];b.gold=1e6;
 b.place(5,3,2);const t=b.t[0];pret(b);for(let i=0;i<4;i++){b.upgrade(t);pret(b)}const c=apparaitre(S,b,3);c.hp=c.max=1e9;
 avancerTerrain(b,3);assert.ok(c.sl>0);proche(c.sf,.5,'niveau 5');
});
test('Racines sylvestres : toutes leurs tours ralentissent, de −10 % pendant 0,72 s (niveau 1) à −30 % pendant 1,3 s (niveau 5)',()=>{const b=terrain([2,0,1,3]);
 for(const k of [20,21,23,24,25,26,27,29]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[k],1);proche(c.sf,.9,S.TW[k].n);proche(c.sl,.72,S.TW[k].n);
  const c5=apparaitre(S,b,3);b.hit(c5,1,S.TW[k],5);proche(c5.sf,.7,S.TW[k].n+' niv. 5');proche(c5.sl,1.3,S.TW[k].n+' niv. 5')}
});
test('Le froid et les racines s’additionnent : Givre niveau 5 + racines niveau 5 = vitesse ×0,2',()=>{const b=terrain([2,0,1,3]);const c=apparaitre(S,b,3);
 b.hit(c,0,S.TW[22],5);b.hit(c,0,S.TW[20],5);proche(c.sf,.2,'cumul');
 b.update(1.4);proche(c.sf,.5,'racines finies, le froid reste');b.update(1.4);assert.equal(c.sl,0);proche(c.sf,1,'plus de ralentissement');
});
test('Deux effets de la même famille ne s’additionnent pas : le plus fort et le plus long l’emportent',()=>{const b=terrain([2,0,1,3]);const c=apparaitre(S,b,3);
 b.hit(c,0,S.TW[22],5);b.hit(c,0,S.TW[22],1);proche(c.sf,.5,'deux Givre');proche(c.sl,2.7,'durée');
 b.hit(c,0,S.TW[20],1);b.hit(c,0,S.TW[20],3);proche(c.sf,.5-.2,'racines niv. 3 l’emportent sur niv. 1');
 b.hit(c,0,S.TW[20],1);proche(c.sf,.3,'des racines plus faibles n’écrasent pas les plus fortes');
});
test('Les autres factions ne ralentissent qu’avec le Givre',()=>{const b=terrain();
 for(const f of [0,1,3,4])for(const j of [0,1,3,4,5,6,7,9]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[f*10+j],1);assert.equal(c.sl,0,S.TW[f*10+j].n)}
});
test('Garde et Flammes sylvestres : le monstre continue d\'avancer normalement (pas de vitesse invalide)',()=>{const b=terrain([2,0,1,3]);
 for(const k of [21,24]){const c=apparaitre(S,b,3);b.hit(c,1,S.TW[k]);const y=c.y;b.update(.5);assert.ok(Number.isFinite(c.y)&&c.y>y,S.TW[k].n)}
});
test('Hâte du Chaman : les alliés proches vont 1,4 fois plus vite, pas le Chaman lui-même',()=>{const b=terrain();
 const ch=apparaitre(S,b,S.AURA),g=apparaitre(S,b,0);b.update(.1);
 assert.equal(g.h,true);assert.equal(ch.h,false);proche(g.y,1.6*1.4*.1,'gobelin accéléré');proche(ch.y,CRs(S.AURA)*.1,'chaman non accéléré');
});
function CRs(k){return S.CR[k].s}
