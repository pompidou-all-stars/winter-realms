/* Parties complètes entre IA, rejouables à l'identique grâce à une graine.
   Le siège 0 est un siège « humain » (sinon la partie s'arrête aussitôt : plus aucun humain),
   mais il est joué par la même logique que les IA, sans bonus de difficulté. */
'use strict';
const crypto=require('crypto');
const {charger}=require('./moteur');

/* les 15 parties entre IA : 5 factions × 3 difficultés, une graine fixe chacune */
const SCENARIOS=[];for(let d=0;d<3;d++)for(let f=0;f<5;f++)SCENARIOS.push({nom:`faction ${f}, difficulté ${d}`,faction:f,difficulte:d,graine:1000+d*10+f});
const DT=.05,DUREE_MAX=1800,POINTS_CONTROLE=30;

/* « photo » complète de l'état de la partie : sert à vérifier que deux parties sont identiques */
function etat(G){return JSON.stringify({t:G.time,tick:G.tick,over:G.over,w:G.winner,B:G.B.map(b=>({or:b.gold,inc:b.inc,v:b.lives,m:b.dead,dp:b.dp,ap:b.ap,pen:b.pen,
 t:b.t.map(t=>[t.x,t.y,t.k,t.lv,t.inv,t.cd,t.stun||0]),c:b.cr.map(c=>[c.k,c.x,c.y,c.hp,c.max,c.sl,c.sf,c.tx,c.ty,c.mark||0,c.arm]),p:b.pr.map(p=>[p.k,p.x,p.y,p.d]),q:b.q.map(s=>[s.k,s.m,s.t])}))})}
const empreinte=s=>crypto.createHash('sha256').update(s).digest('hex').slice(0,16);

function jouer(source,sc,{surEtape}={}){
 const S=charger(source,{graine:sc.graine});
 const seats=[0,1,2,3].map(i=>({name:i?'IA '+i:'Joueur',col:'#fff',ai:i?1:0,classId:(sc.faction+i)%5}));
 const G=new S.Game(seats,sc.difficulte),h=G.B[0];
 let aiT=1,envois=[0,0,0,0];const origSend=G.send.bind(G);G.send=(from,k)=>{const ok=origSend(from,k);if(ok)envois[from.i]++;return ok};
 const controles=[];let prochain=POINTS_CONTROLE,n=0;
 while(!G.over&&G.time<DUREE_MAX){
  if(!h.dead){aiT-=DT;if(aiT<=0){aiT=.6;h.ai=1;S.aiAct(h);h.ai=0}}
  G.step(DT);n++;if(surEtape)surEtape(G,n);
  if(G.time>=prochain){controles.push(empreinte(etat(G)));prochain+=POINTS_CONTROLE}}
 return {graine:sc.graine,faction:sc.faction,difficulte:sc.difficulte,duree:+G.time.toFixed(2),terminee:G.over,gagnant:G.winner,
  vies:G.B.map(b=>b.lives),revenus:G.B.map(b=>b.inc),tours:G.B.map(b=>b.t.length),envois,
  invalide:G.B.some(b=>b.cr.some(c=>!isFinite(c.x)||!isFinite(c.y)||!isFinite(c.hp))||!isFinite(b.gold)),
  controles,final:empreinte(etat(G))};
}
module.exports={SCENARIOS,jouer,etat,empreinte,DT};
