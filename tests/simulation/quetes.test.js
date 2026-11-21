/* Quêtes bonus (2.38) : tirage, annonces dans le journal, courses et photos, récompense, quêtes impossibles au départ, IA qui les joue. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {charger,partie,avancer}=require('../outils/moteur');
const S=charger('actuel');
const IDS=S.QUETES.map(Q=>Q.id);
/* lance la quête id tout de suite (les autres sont marquées comme déjà tirées) */
function lancer(G,id,t=200){G.time=Math.max(G.time,t);G.qu=null;G.quN=0;G.quF=IDS.filter(x=>x!=id);G.quete();assert.equal(G.qu&&G.qu.id,id,'quête '+id+' lancée');return G.qu}
const fins=G=>G.log.filter(l=>l.type=='quete'&&l.ph=='fin').map(l=>({...l,g:[...l.g]}));
const cases=b=>{const l=[];for(let y=1;y<S.R-1;y++)for(let x=0;x<S.C;x++)if(x!=6)l.push([x,y]);return l};

test('Table : 10 quêtes aux identifiants uniques, chacune avec un titre, une règle, une forme et une mesure',()=>{
 assert.equal(S.QUETES.length,10);assert.equal(new Set(IDS).size,10);
 for(const Q of S.QUETES){assert.ok(Q.titre&&Q.txt,Q.id);assert.ok(['course','photo'].includes(Q.f),Q.id);assert.equal(typeof Q.sc,'function');assert.ok(Q.dur>=60&&Q.dur<=150,Q.id);
  if(Q.f=='course')assert.equal(typeof Q.cible,'function',Q.id)}
});
test('La première quête commence à 1:30 et s’annonce dans le journal ; la suivante 3 à 4 min après la fin',()=>{
 const G=partie(S);avancer(G,89);assert.equal(G.qu,null);assert.ok(!G.log.some(l=>l.type=='quete'));
 avancer(G,1.1);assert.ok(G.qu);const d=G.log.find(l=>l.type=='quete');assert.equal(d.ph,'debut');assert.equal(d.id,G.qu.id);assert.ok(d.or>=100);
 G.time=G.qu.fin+.01;G.quete();assert.equal(G.qu,null);assert.equal(fins(G).length,1);assert.ok(G.quN>=G.time+S.QU_PAUSE&&G.quN<=G.time+S.QU_PAUSE+60);
});
test('Tirage sans remise : les 10 quêtes passent avant qu’une revienne',()=>{
 const G=partie(S);G.time=300;const vu=[];
 for(let n=0;n<10;n++){G.quN=0;G.quete();assert.ok(G.qu);vu.push(G.qu.id);G.time=G.qu.fin+.01;G.quete();G.time+=1}
 assert.equal(new Set(vu).size,10,vu.join(','));
});
test('Récompense : au moins 100 or, puis 8 × le revenu moyen des joueurs en jeu (arrondi à la dizaine)',()=>{
 const G=partie(S);assert.equal(S.quOr(G),100);G.B.forEach((b,i)=>b.inc=100*(i+1));assert.equal(S.quOr(G),2000);G.B[3].dead=1;assert.equal(S.quOr(G),1600);
});
test('Clicker fou : le premier qui pose 10 tours de plus gagne l’or, la quête s’arrête aussitôt',()=>{
 const G=partie(S),b=G.B[0];b.gold=1e6;for(const[x,y]of cases(b).slice(0,3))b.place(x,y,0);
 const q=lancer(G,'clicker');assert.equal(q.cible,10);const or=q.or;let n=0;
 for(const[x,y]of cases(b).slice(3)){if(n>=10)break;if(b.place(x,y,0))n++;G.quete();if(n<10)assert.ok(G.qu,'pas encore gagné après '+n)}
 assert.equal(G.qu,null);const f=fins(G)[0];assert.deepEqual(f.g,[0]);assert.equal(f.or,or);assert.equal(b.st.qu,1);assert.equal(b.st.quOr,or);
});
test('Clicker fou : jamais tiré si un joueur n’a plus la place de construire (fin de partie)',()=>{
 const G=partie(S),Q=S.QUETES.find(Q=>Q.id=='clicker');assert.ok(Q.ok(G));
 const b=G.B[2];for(let y=0;y<S.R;y++)for(let x=0;x<S.C;x++)b.g[y][x]=x==6?0:1;assert.ok(S.posables(b,20)<20);assert.ok(!Q.ok(G));
 G.time=300;G.quN=0;G.quF=IDS.filter(x=>x!='clicker');G.quete();assert.notEqual(G.qu&&G.qu.id,'clicker');
});
test('Le facteur : chaque monstre retient son envoyeur ; le premier qui en fait passer 4 chez ses adversaires gagne',()=>{
 const G=partie(S);G.time=200;const q=lancer(G,'facteur');assert.equal(q.cible,4);G.B[0].gold=1e4;
 assert.equal(G.action(0,{type:'send',k:1}),'');assert.ok(G.B[1].q.every(s=>s.o==0));
 avancer(G,25);const f=fins(G)[0];assert.ok(f,'quête finie');assert.deepEqual(f.g,[0]);assert.ok(G.B[0].st.passe>=4);assert.equal(G.B[1].st.passe,0);
});
test('Gonflette : la cible dépasse la meilleure tour du moment (au moins niveau 3) ; impossible si une tour est déjà au niveau 5',()=>{
 const G=partie(S),b=G.B[1];b.gold=1e6;assert.ok(b.place(0,5,b.classId*10));const t=b.t[0];t.lv=3;
 const q=lancer(G,'gonflette');assert.equal(q.cible,4);assert.equal(G.qu.sc[1],0,'tour en chantier : pas comptée');
 t.b=0;G.quete();assert.ok(G.qu,'niveau 3 ne suffit pas');t.lv=4;G.quete();assert.deepEqual(fins(G)[0].g,[1]);
 t.lv=5;assert.ok(!S.QUETES.find(Q=>Q.id=='gonflette').ok(G));
});
test('Frozen : la cible dépasse celui qui a le plus de Givre, d’autant plus que la partie avance',()=>{
 const G=partie(S),b=G.B[2];b.gold=1e6;let n=0;for(const[x,y]of cases(b)){if(n>=3)break;if(b.place(x,y,b.classId*10+2))n++}
 assert.equal(lancer(G,'frozen',200).cible,5);const G2=partie(S);assert.equal(lancer(G2,'frozen',700).cible,4);
});
test('Picsou (photo) : au bout du chrono, le plus riche gagne ; une égalité partage l’or',()=>{
 let G=partie(S);let q=lancer(G,'picsou');G.B.forEach((b,i)=>b.gold=[50,300,120,10][i]);G.time=q.fin-1;G.quete();assert.ok(G.qu);
 G.time=q.fin;G.quete();assert.deepEqual(fins(G)[0].g,[1]);
 G=partie(S);q=lancer(G,'picsou');G.B.forEach((b,i)=>b.gold=[300,300,120,10][i]);G.time=q.fin;G.quete();const f=fins(G)[0];assert.deepEqual(f.g,[0,1]);assert.equal(f.or,Math.round(q.or/2));
});
test('Pigeons voyageurs : si personne n’envoie de volants, personne ne gagne',()=>{
 const G=partie(S);const q=lancer(G,'pigeons');G.time=q.fin;G.quete();const f=fins(G)[0];assert.deepEqual(f.g,[]);assert.equal(f.or,0);
});
test('Mamie Gâteau : le plus petit revenu gagne ; un joueur éliminé ne compte pas',()=>{
 const G=partie(S);const q=lancer(G,'mamie');G.B.forEach((b,i)=>b.inc=[40,15,30,5][i]);G.B[3].dead=1;G.time=q.fin;G.quete();assert.deepEqual(fins(G)[0].g,[1]);
});
test('Course non gagnée : elle s’arrête au bout de sa durée, sans gagnant',()=>{
 const G=partie(S);const q=lancer(G,'cadeau');G.time=q.fin;G.quete();assert.equal(G.qu,null);assert.deepEqual(fins(G)[0].g,[]);
});
/* une IA en milieu de partie (1:40), sans monstre sur son terrain, qui joue la quête id */
function iaEnQuete(id){const G=partie(S,{ia:[0,1,1,1]});G.B[0].lives=1e6;avancer(G,100);const A=G.B[1];A.cr=[];A.q=[];A.hurt=0;A.pen=0;A.gold=2000;A.dp=1000;A.ap=1000;A.lastG=A.gold;
 const q=lancer(G,id,id=='cadeau'?200:G.time);q.joue=[false,true,false,false];assert.equal(S.quJ(A),id);return A}
test('IA : une IA qui joue Picsou ne dépense rien tant qu’elle n’est pas en danger',()=>{
 const A=iaEnQuete('picsou'),t=A.t.map(t=>t.k+':'+t.lv).join();for(let i=0;i<5;i++)S.aiAct(A);assert.equal(A.gold,2000);assert.equal(A.t.map(t=>t.k+':'+t.lv).join(),t);
});
test('IA : Clicker fou, elle pose des Archers sans rien améliorer ; Frozen, du Givre ; Gonflette, elle monte sa tour la plus haute',()=>{
 let A=iaEnQuete('clicker'),n=A.t.length,lv=A.t.reduce((s,t)=>s+t.lv,0);for(let i=0;i<3;i++)S.aiDefend(A);
 assert.ok(A.t.length>n,'tours posées');assert.equal(A.t.reduce((s,t)=>s+t.lv,0)-lv,A.t.length-n,'aucune amélioration');assert.ok(A.t.slice(n).every(t=>t.k==A.classId*10),'des Archers');
 A=iaEnQuete('frozen');n=A.t.length;for(let i=0;i<6;i++)S.aiDefend(A);assert.ok(A.t.length>n);assert.ok(A.t.slice(n).every(t=>S.TW[t.k].ctl),'des tours de contrôle');
 A=iaEnQuete('gonflette');const haut=A.t.slice().sort((a,b)=>b.lv-a.lv||b.inv-a.inv)[0];for(const t of A.t)t.b=0;const l0=haut.lv;S.aiDefend(A);assert.equal(haut.lv,l0+1);
});
test('IA : Le gros cadeau, elle envoie un boss dès qu’elle peut le payer',()=>{
 const A=iaEnQuete('cadeau');A.gold=500;A.ap=0;assert.ok(S.aiAttack(A));assert.equal(A.st.boss,1);
});
test('Partie entre IA : les quêtes se suivent, chacune finit, et les IA en remportent',()=>{
 const S2=charger('actuel',{graine:7}),G=partie(S2,{ia:[0,1,1,1],difficulte:2});G.B[0].lives=1e6;
 const L=[];for(let n=0;n<10*60/.05&&!G.over;n++){G.step(.05);for(const l of G.log.splice(0))if(l.type=='quete')L.push(l)}
 const d=L.filter(l=>l.ph=='debut'),f=L.filter(l=>l.ph=='fin');assert.ok(d.length>=3,d.length+' quêtes');assert.ok(f.length>=d.length-1);
 for(let i=0;i<f.length;i++)assert.equal(f[i].id,d[i].id);
 assert.ok(f.some(l=>l.g.some(i=>i>0)),'une IA gagne au moins une quête');
});
