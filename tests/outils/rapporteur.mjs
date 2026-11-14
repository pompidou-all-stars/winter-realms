/* Affichage des résultats de tests en français, lisible sans connaissance technique.
   Si la variable WR_RESULTATS contient un chemin, les résultats y sont aussi écrits en JSON (utilisé par le bilan). */
import fs from 'node:fs';
import path from 'node:path';
export default async function*(source){
 const res=[];
 for await(const ev of source){
  if(ev.type!=='test:pass'&&ev.type!=='test:fail')continue;const d=ev.data,det=d.details||{};
  const fichier=d.file?path.basename(d.file):'';
  if(det.type==='suite'){if(ev.type==='test:fail'&&det.error&&det.error.failureType!=='subtestsFailed'){res.push({fichier,nom:d.name,etat:'echec',message:String(det.error.cause?.message||det.error.message).split('\n')[0]});yield `❌ ${d.name}\n   → ${res.at(-1).message}\n`}continue}
  if(d.skip){res.push({fichier,nom:d.name,etat:'ignore',message:String(d.skip)});yield `⏭️  ${d.name} — ${d.skip}\n`;continue}
  if(ev.type==='test:pass'){res.push({fichier,nom:d.name,etat:'ok'});yield `✅ ${d.name}\n`}
  else{const e=det.error||{},c=e.cause||e;let m=String(c.message||e.message||'échec').split('\n')[0];
   if(/^Expected values|^The expression evaluated|^Values identical/.test(m))m='valeurs différentes de ce qui est attendu';
   if(c.expected!==undefined&&typeof c.expected!=='object'&&typeof c.expected!=='boolean'&&!/attendu/.test(m))m+=` (attendu : ${c.expected}, obtenu : ${c.actual})`;
   res.push({fichier,nom:d.name,etat:'echec',message:m});yield `❌ ${d.name}\n   → ${m}\n`}
 }
 const n=e=>res.filter(r=>r.etat===e).length;
 yield `\n${n('echec')?'❌':'✅'} Bilan : ${n('ok')} réussi(s), ${n('echec')} échoué(s), ${n('ignore')} ignoré(s)\n`;
 if(process.env.WR_RESULTATS)fs.writeFileSync(process.env.WR_RESULTATS,JSON.stringify(res,null,1));
}
