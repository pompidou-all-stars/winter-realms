/* Construction : pose, refus, chemin, revente, améliorations — tel que le moteur actuel le fait. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,apparaitre,avancerTerrain,pret}=require('../outils/moteur');
const S=charger('actuel');
const nouveau=()=>{const G=partie(S);return {G,b:G.B[0]}};
const chemin=b=>b.d[S.SP[1]][S.SP[0]];

test('Poser une tour débite son coût et occupe la case',()=>{const {G,b}=nouveau();
 assert.equal(G.action(0,{type:'place',x:3,y:5,k:0}),'');
 assert.equal(b.gold,100-S.TW[0].c);assert.equal(b.g[5][3],1);
 assert.equal(b.t.length,1);assert.deepEqual([b.t[0].lv,b.t[0].inv],[1,S.TW[0].c]);
});
test('Refus sur la case d\'apparition, la sortie ou une case occupée (code « blocked »), sans débit',()=>{const {G,b}=nouveau();
 assert.equal(G.action(0,{type:'place',x:6,y:0,k:0}),'blocked');
 assert.equal(G.action(0,{type:'place',x:6,y:16,k:0}),'blocked');
 G.action(0,{type:'place',x:2,y:2,k:0});const or=b.gold;
 assert.equal(G.action(0,{type:'place',x:2,y:2,k:0}),'blocked');assert.equal(b.gold,or);
});
test('Refus hors du terrain (code « blocked »)',()=>{const {G}=nouveau();
 assert.equal(G.action(0,{type:'place',x:-1,y:3,k:0}),'blocked');assert.equal(G.action(0,{type:'place',x:13,y:3,k:0}),'blocked');
});
test('Refus quand l\'or manque (code « poor »)',()=>{const {G,b}=nouveau();
 assert.equal(G.action(0,{type:'place',x:3,y:3,k:9}),'poor');assert.equal(b.gold,100);assert.equal(b.t.length,0);
});
test('Refus d\'une tour d\'une autre faction (code « blocked » si l\'or suffit)',()=>{const {G,b}=nouveau();
 assert.equal(G.action(0,{type:'place',x:3,y:3,k:10}),'blocked');assert.equal(b.t.length,0);
});
test('Refus d\'une tour qui couperait complètement le chemin',()=>{const {G,b}=nouveau();b.gold=1e6;
 for(let x=0;x<12;x++)assert.equal(G.action(0,{type:'place',x,y:5,k:0}),'',`case (${x},5)`);
 const or=b.gold;assert.equal(G.action(0,{type:'place',x:12,y:5,k:0}),'blocked');assert.equal(b.gold,or);assert.equal(b.g[5][12],0);
});
test('Le plus court chemin est recalculé après une pose et après une vente',()=>{const {G,b}=nouveau();
 assert.equal(chemin(b),16);G.action(0,{type:'place',x:6,y:8,k:0});assert.equal(chemin(b),18);
 G.action(0,{type:'sell',x:6,y:8});assert.equal(chemin(b),16);
});
test('Refus sur la case vers laquelle se dirige un monstre au sol',()=>{const {G,b}=nouveau();
 const c=apparaitre(S,b,0);avancerTerrain(b,.3);assert.deepEqual([c.tx,c.ty],[6,1]);
 assert.equal(G.action(0,{type:'place',x:6,y:1,k:0}),'blocked');
});
test('Refus d\'une tour qui couperait le passage d\'un monstre déjà en route (même si l\'apparition reste reliée)',()=>{const {G,b}=nouveau();
 const c=apparaitre(S,b,0);Object.assign(c,{x:0,y:10,tx:0,ty:10});
 assert.equal(G.action(0,{type:'place',x:0,y:9,k:0}),'');assert.equal(G.action(0,{type:'place',x:1,y:10,k:0}),'');
 assert.equal(G.action(0,{type:'place',x:0,y:11,k:0}),'blocked');assert.equal(b.g[11][0],0);
 b.cr=[];assert.equal(G.action(0,{type:'place',x:0,y:11,k:0}),'','sans le monstre, la même pose est acceptée');
});
test('Revente : 70 % de l\'or investi, arrondi à l\'inférieur, et la case est libérée',()=>{const {G,b}=nouveau();
 G.action(0,{type:'place',x:3,y:3,k:0});const avant=b.gold;assert.equal(G.action(0,{type:'sell',x:3,y:3}),'');
 assert.equal(b.gold,avant+Math.floor(S.TW[0].c*.7));assert.equal(b.g[3][3],0);assert.equal(b.t.length,0);
});
test('Améliorations : coût = arrondi(coût × 1,5 × 2^(niveau−1) / 5) × 5, investissement cumulé, revente à 70 %',()=>{const {G,b}=nouveau();b.gold=1e6;
 G.action(0,{type:'place',x:3,y:3,k:0});const t=b.t[0],c0=S.TW[0].c;let inv=c0;
 for(let lv=1;lv<5;lv++){const cout=Math.round(c0*1.5*2**(lv-1)/5)*5,or=b.gold;pret(b);assert.equal(G.action(0,{type:'upgrade',x:3,y:3}),'');
  assert.equal(or-b.gold,cout,`passage au niveau ${lv+1}`);inv+=cout;assert.equal(t.lv,lv+1);assert.equal(t.inv,inv)}
 pret(b);assert.equal(G.action(0,{type:'upgrade',x:3,y:3}),'max');
 const or=b.gold;G.action(0,{type:'sell',x:3,y:3});assert.equal(b.gold-or,Math.floor(inv*.7));
});
test('Amélioration refusée quand l\'or manque (« poor »), action sur une case vide (« bad »)',()=>{const {G,b}=nouveau();
 G.action(0,{type:'place',x:3,y:3,k:0});pret(b);b.gold=0;assert.equal(G.action(0,{type:'upgrade',x:3,y:3}),'poor');
 assert.equal(G.action(0,{type:'upgrade',x:4,y:4}),'bad');assert.equal(G.action(0,{type:'sell',x:4,y:4}),'bad');
 assert.equal(G.action(0,{type:'danse'}),'bad');assert.equal(G.action(0,{type:'place',x:1,y:1,k:99}),'bad');
});
test('Dégâts doublés et portée +5 % à chaque niveau',()=>{
 for(const k of [0,15,33,49])for(let lv=1;lv<=5;lv++){assert.equal(S.dmg({k,lv}),S.TW[k].d*2**(lv-1));assert.equal(S.rng({k,lv}),S.TW[k].r*(1+.05*(lv-1)))}
});
test('Une IA ou un terrain inexistant ne peut pas recevoir d\'action (« over »)',()=>{
 const G=partie(S,{ia:[0,1,1,1]});assert.equal(G.action(1,{type:'place',x:3,y:3,k:10}),'over');assert.equal(G.action(7,{type:'place'}),'over');
});
