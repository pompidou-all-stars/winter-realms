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
test('Espacement : 3 envois rapprochés (12 monstres) s\'écartent sur le côté, sans retard ni bouchon',()=>{const b=terrain();
 for(let i=0;i<3;i++)b.send(0,1);const vie=()=>{for(const c of b.cr)c.hp=c.max=1e9};
 for(let i=0;i<40;i++){b.update(.05);vie()}const L=b.cr;let dmin=9;for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++)dmin=Math.min(dmin,Math.hypot(L[i].x-L[j].x,L[i].y-L[j].y));
 assert.equal(L.length,12);assert.ok(dmin>.35,`distance minimale ${dmin.toFixed(2)}`);
 /* le dernier apparaît au plus tard à 1,39 s ; un Sapeur seul met 10 s */
 for(let i=0;i<190;i++){b.update(.05);vie()}assert.equal(b.cr.length,0,'tous sortis à temps');assert.equal(b.lives,28);
});
test('Espacement dans un couloir d\'une case : on ne sort jamais du couloir et personne ne reste coincé',()=>{const b=terrain();b.gold=1e7;
 for(let x=0;x<12;x++)b.place(x,4,0);for(let x=1;x<13;x++)b.place(x,8,0);for(const t of b.t)t.b=0;
 for(let i=0;i<20;i++)b.q.push({k:i%3,m:1,t:i*.1});let t=0;
 while((b.q.length||b.cr.length)&&t<60){b.update(.05);t+=.05;for(const c of b.cr){c.hp=c.max=1e9;assert.equal(b.g[Math.round(c.y)][Math.round(c.x)],0,'monstre sur une tour')}}
 assert.equal(b.lives,20);assert.ok(t<25,`tous sortis en ${t.toFixed(1)} s`);
});
test('Vitesse ralentie : déplacement = vitesse × facteur × temps',()=>{const b=terrain();const c=apparaitre(S,b,0);
 c.gt=10;c.gp=.5;b.update(.5);proche(c.y,1.6*.5*.5,'position');
});
/* 2.39 : le froid vient du Totem des pluies glacées (Clans de l'Orage Blanc, emplacement 2) ; GIVRE_LV règle toujours son effet */
const GV=12,orage=()=>{const b=partie(S,{factions:[1,0,2,3]}).B[0];b.gold=1e6;return b};
test('Froid (Totem des pluies glacées) : de −20 % (niveau 1) à −50 % (niveau 5), pendant 1,5 s à 2,7 s',()=>{const b=terrain(),T=S.TW[GV];
 const att=[[.8,1.5],[.725,1.8],[.65,2.1],[.575,2.4],[.5,2.7]];
 for(let lv=1;lv<=5;lv++){const c=apparaitre(S,b,3);b.hit(c,0,T,lv);proche(c.sf,att[lv-1][0],'vitesse niveau '+lv);proche(c.sl,att[lv-1][1],'durée niveau '+lv)}
});
test('Froid : deux coups ne s’additionnent pas, le plus fort et le plus long l’emportent',()=>{const b=terrain();const c=apparaitre(S,b,3);
 b.hit(c,0,S.TW[GV],5);b.hit(c,0,S.TW[GV],1);proche(c.sf,.5,'deux coups');proche(c.sl,2.7,'durée');
});
test('Froid : la zone d’effet passe de 1,2 case (niveau 1) à 2 cases (niveau 5)',()=>{
 for(const [lv,ralenti] of [[1,false],[5,true]]){const b=terrain();const a=apparaitre(S,b,0),v=apparaitre(S,b,0);a.hp=a.max=v.hp=v.max=1e9;
  Object.assign(a,{x:6,y:5,tx:6,ty:5});Object.assign(v,{x:6,y:6.8,tx:6,ty:7});
  b.impact({k:GV,tg:a,d:1,tx:a.x+.5,ty:a.y+.5,lv});assert.ok(a.sl>0,'cible');assert.equal(v.sl>0,ralenti,'voisin à 1,8 case, niveau '+lv);
  const z=b.fx.find(f=>f.type=='boom');proche(z.r,S.GIVRE_LV.r[lv-1],'rayon affiché')}
});
test('Froid : le ralentissement vient du niveau de la tour qui tire',()=>{const b=orage();
 b.place(5,3,GV);const t=b.t[0];pret(b);for(let i=0;i<4;i++){b.upgrade(t);pret(b)}const c=apparaitre(S,b,3);c.hp=c.max=1e9;
 avancerTerrain(b,3);assert.ok(c.sl>0);proche(c.sf,.5,'niveau 5');
});
test('Plancher (règle d’or n°1) : les ralentissements cumulés ne descendent jamais sous ×0,3',()=>{const b=terrain();const c=apparaitre(S,b,3);
 Object.assign(c,{gp:.5,gt:5,rp:.4,rt:5});b.update(0);proche(c.sf,S.SF_MIN,'froid + racines');assert.equal(S.SF_MIN,.3);
});
test('Immobilisation : le monstre s’arrête, puis il est immunisé un moment (rendement décroissant) ; un boss moitié moins longtemps',()=>{const b=terrain(),T=S.TW[2];
 const c=apparaitre(S,b,3);c.hp=c.max=1e9;b.hit(c,0,T,1);proche(c.im,T.im,'durée');assert.equal(c.sf,0);const y=c.y;b.update(.5);proche(c.y,y,'immobile');
 b.update(.4);assert.equal(c.im,0);b.hit(c,0,T,1);assert.equal(c.im,0,'immunisé juste après');b.update(2);b.hit(c,0,T,1);proche(c.im,T.im,'de nouveau sensible');
 const k=S.BOSS[0],h=apparaitre(S,b,k);h.hp=h.max=1e9;b.hit(h,0,T,1);proche(h.im,T.im/2,'boss : moitié');
});
test('Aucun ralentissement en dehors des tours de froid et d’immobilisation (pas de vitesse invalide)',()=>{const b=terrain();
 for(const T of S.TW){if(T.fsp||T.im||T.hx)continue;const c=apparaitre(S,b,3);c.hp=c.max=1e9;b.hit(c,1,T,1);assert.equal(c.sl,0,T.n);const y=c.y;b.update(.5);assert.ok(Number.isFinite(c.y)&&c.y>y,T.n)}
});
test('Hâte du Chaman : les alliés proches vont 1,4 fois plus vite, pas le Chaman lui-même',()=>{const b=terrain();
 const ch=apparaitre(S,b,S.AURA),g=apparaitre(S,b,0);b.update(.1);
 assert.equal(g.h,true);assert.equal(ch.h,false);proche(g.y,1.6*1.4*.1,'gobelin accéléré');proche(ch.y,CRs(S.AURA)*.1,'chaman non accéléré');
});
function CRs(k){return S.CR[k].s}
