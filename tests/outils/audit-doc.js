/* Compare les tableaux chiffrés de CLAUDE.md (§4.1, §5.1, §6.2, §7) aux valeurs réelles du code.
   Ne corrige rien : liste seulement les écarts, pour décision par le concepteur.
   Usage : node tests/outils/audit-doc.js */
'use strict';
const fs=require('fs'),path=require('path');
const {charger,RACINE}=require('./moteur');

const num=s=>+String(s).replace(/\*/g,'').replace(',','.').replace(/[^\d.\-]/g,'');
const mmss=t=>Math.floor(t/60)+':'+String(t%60).padStart(2,'0');
const cellules=l=>l.split('|').slice(1,-1).map(s=>s.trim());

function auditer(S=charger('actuel')){
 const doc=fs.readFileSync(path.join(RACINE,'CLAUDE.md'),'utf8').split('\n'),ecarts=[],verifie={tours:0,monstres:0,archetypes:0,difficultes:0};
 const ecart=(ou,quoi,docv,codev)=>ecarts.push({ou,quoi,doc:docv,code:codev});
 const proche=(a,b,eps)=>Math.abs(a-b)<=eps;
 let section='',faction=-1;
 for(const l of doc){
  if(l.startsWith('#'))section=l;
  const mf=l.match(/^#### (.+)$/);if(mf)faction=S.FACTIONS.findIndex(F=>F.name==mf[1].trim());
  if(!l.startsWith('|')||/^\|[-| ]+\|$/.test(l))continue;const c=cellules(l);
  /* §5.1 : # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée */
  if(section.startsWith('#### ')&&faction>=0&&/^\d$/.test(c[0])){const k=faction*10+ +c[0],T=S.TW[k],ou=`§5.1 ${S.FACTIONS[faction].name}, ${c[1]}`;verifie.tours++;
   if(c[1].replace('’',"'")!==T.n.replace('’',"'"))ecart(ou,'nom',c[1],T.n);
   if(num(c[3])!==T.c)ecart(ou,'coût',c[3],T.c);
   if(!proche(num(c[4]),T.d,.051))ecart(ou,'dégâts',c[4],T.d);
   if(!proche(num(c[5]),T.cd,.0006))ecart(ou,'recharge',c[5],T.cd);
   if(num(c[6])!==Math.round(T.d/T.cd))ecart(ou,'DPS',c[6],Math.round(T.d/T.cd));
   if(!proche(num(c[7]),T.r,.006))ecart(ou,'portée',c[7],T.r)}
  /* §6.2 : Monstre | Catégorie | Coût | +revenu | PV de base | Vitesse | Disponible à | Capacité */
  if(section.startsWith('### 6.2')&&c[0]!=='Monstre'){const k=S.CR.findIndex(T=>T.n.replace('’',"'")==c[0].replace('’',"'"));const ou=`§6.2 ${c[0]}`;
   if(k<0){ecart(ou,'monstre','présent dans la doc','absent du code');continue}const T=S.CR[k];verifie.monstres++;
   if(num(c[2])!==T.c)ecart(ou,'coût',c[2],T.c);if(num(c[3])!==T.i)ecart(ou,'+revenu',c[3],T.i);
   if(num(c[4])!==T.hp)ecart(ou,'PV de base',c[4],T.hp);if(num(c[5])!==T.s)ecart(ou,'vitesse',c[5],T.s);
   if(c[6]!==mmss(T.at||0))ecart(ou,'disponible à',c[6],mmss(T.at||0))}
  /* §4.1 : Archétype | Coût | Portée | Dégâts | Recharge | … */
  if(section.startsWith('### 4.1')&&c[0]!=='Archétype'){const B=S.BASE_TW.find(b=>b.n==c[0]);if(!B)continue;const ou=`§4.1 ${c[0]}`;verifie.archetypes++;
   if(num(c[1])!==B.c)ecart(ou,'coût',c[1],B.c);if(num(c[2])!==B.r)ecart(ou,'portée',c[2],B.r);if(num(c[3])!==B.d)ecart(ou,'dégâts',c[3],B.d);if(num(c[4])!==B.cd)ecart(ou,'recharge',c[4],B.cd)}
  /* §7 : Niveau | Revenu des IA | Or de départ */
  if(section.startsWith('## 7.')&&c[0]!=='Niveau'){const D=S.DIFF.find(d=>d.n==c[0]);if(!D)continue;const ou=`§7 ${c[0]}`;verifie.difficultes++;
   if(num(c[1])!==D.b)ecart(ou,'revenu des IA',c[1],D.b);if(num(c[2])!==D.g)ecart(ou,'or de départ en plus',c[2],D.g)}
 }
 return {ecarts,verifie};
}
module.exports={auditer};
if(require.main===module){const r=auditer();
 console.log(`Vérifié : ${r.verifie.tours} tours, ${r.verifie.monstres} monstres, ${r.verifie.archetypes} archétypes, ${r.verifie.difficultes} difficultés.`);
 if(!r.ecarts.length)console.log('✅ Aucun écart entre CLAUDE.md et le code.');
 for(const e of r.ecarts)console.log(`⚠️ ${e.ou} — ${e.quoi} : doc « ${e.doc} », code « ${e.code} »`);}
