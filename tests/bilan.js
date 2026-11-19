/* Les trois bilans d'une évolution : 🔧 technique, 🎮 gameplay, 🎨 visuel.
   Usage : node tests/bilan.js [version-avant] [--sans-visuel] [--complet]     (version-avant par défaut : origin/main ; --complet : 15 parties entre IA au lieu de 3)
   Produit rapports/bilan.html (lisible sur téléphone) et affiche un résumé.
   Règle : une réussite technique ne valide JAMAIS le gameplay ni le rendu. Ces deux bilans comparent à « version-avant »
   et disent seulement « identique » ou « changé : à examiner », la validation revient au concepteur. */
'use strict';
const fs=require('fs'),path=require('path'),{spawnSync,execFileSync}=require('child_process');
const {charger,RACINE}=require('./outils/moteur');
const {SCENARIOS,jouerEnParallele}=require('./outils/parties');
const {auditer}=require('./outils/audit-doc');
const N=require('./outils/navigateur');

const args=process.argv.slice(2),avant=args.find(a=>!a.startsWith('--'))||'origin/main',sansVisuel=args.includes('--sans-visuel');
const DOSSIER=path.join(RACINE,'rapports');fs.rmSync(DOSSIER,{recursive:true,force:true});fs.mkdirSync(DOSSIER,{recursive:true});
const FICHIERS_TECHNIQUES=['parcours.test.js','assets3d.test.js'];
const FACTIONS=['Alliance','Horde','Sylvestres','Nains','Légion'],NIVEAUX=['Normal','Difficile','Brutal'];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const git=(...a)=>{try{return execFileSync('git',a,{cwd:RACINE,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim()}catch(e){return null}};

async function main(){
 const debut=Date.now();console.log(`Bilan en cours (référence visuelle : ${avant})…\n`);
 /* ---------- exécution des tests ---------- */
 const fRes=path.join(DOSSIER,'resultats.json'),fParties=path.join(DOSSIER,'parties.jsonl');
 const run=spawnSync(process.execPath,[path.join(__dirname,'tout.js'),...(N.disponible()?[]:['--simulation']),...(args.includes('--complet')?['--complet']:[])],{cwd:RACINE,encoding:'utf8',env:{...process.env,WR_RESULTATS:fRes,WR_PARTIES:fParties}});
 fs.writeFileSync(path.join(DOSSIER,'tests.log'),(run.stdout||'')+(run.stderr||''));
 const res=fs.existsSync(fRes)?JSON.parse(fs.readFileSync(fRes,'utf8')):[];
 const tech=res.filter(r=>FICHIERS_TECHNIQUES.includes(r.fichier)),jeu=res.filter(r=>!FICHIERS_TECHNIQUES.includes(r.fichier));
 const compte=l=>({ok:l.filter(r=>r.etat=='ok').length,ko:l.filter(r=>r.etat=='echec'),ign:l.filter(r=>r.etat=='ignore')});

 /* ---------- 🔧 technique ---------- */
 const T=compte(tech),J=compte(jeu);
 const modifies=[...new Set([...(git('diff','--name-only',avant)||'').split('\n'),...(git('ls-files','--others','--exclude-standard')||'').split('\n')].filter(Boolean))].sort();
 const sensibles=modifies.filter(f=>f=='sim.js'||f=='index.html'||f.startsWith('server/'));
 const techOK=run.status!==null&&res.length>0&&T.ko.length==0;
 const technique={verdict:techOK?'ok':'ko',
  resume:techOK?`${T.ok} vérifications techniques réussies${T.ign.length?`, ${T.ign.length} ignorée(s)`:''}`:`${T.ko.length} vérification(s) technique(s) en échec`,
  details:[`Tests lancés : ${res.length} (${T.ok+J.ok} réussis, ${T.ko.length+J.ko.length} échoués, ${T.ign.length+J.ign.length} ignorés), en ${Math.round((Date.now()-debut)/1000)} s.`,
   N.disponible()?'Parcours mobile automatisé (Chromium, portrait et paysage) : '+(tech.some(r=>r.fichier=='parcours.test.js'&&r.etat=='echec')?'❌ en échec':'✅ réussi')+'. Ce test ne garantit pas la compatibilité avec tous les téléphones.':'⏸ Parcours mobile non vérifié : Playwright absent sur cette machine.',
   `Fichiers modifiés par rapport à ${avant} : ${modifies.length?modifies.join(', '):'aucun'}.`,
   sensibles.length?`⚠️ Fichiers du jeu touchés : ${sensibles.join(', ')}.`:'Aucun fichier du jeu touché (sim.js, index.html, server/).',
   'Vérification automatique GitHub (« Tests de simulation ») : à lire sur la Pull Request.'],
  echecs:T.ko};

 /* ---------- 🎮 gameplay : comparaison avec le sim.js de « avant » (par défaut origin/main) ---------- */
 const S=charger('actuel'),codeApres=fs.readFileSync(path.join(RACINE,'sim.js'),'utf8'),codeAvant=git('show',avant+':sim.js'),memeMoteur=codeAvant===codeApres;
 const SA=codeAvant?charger({code:codeAvant}):null;
 const clone=o=>JSON.parse(JSON.stringify(o)),diffs=[];
 const cmp=(nom,a,b)=>{for(const k of new Set([...Object.keys(a),...Object.keys(b)]))if(JSON.stringify(a[k])!==JSON.stringify(b[k]))diffs.push({nom,champ:k,avant:b[k],apres:a[k]})};
 if(SA){S.TW.forEach((t,k)=>{const r=SA.TW[k];if(!r){diffs.push({nom:t.n,champ:'(nouvelle tour)',avant:'—',apres:'ajoutée'});return}cmp(t.n,clone(t),clone(r))});
  S.CR.forEach((t,k)=>{const r=SA.CR[k];if(!r){diffs.push({nom:t.n,champ:'(nouveau monstre)',avant:'—',apres:'ajouté'});return}cmp(t.n,clone(t),clone(r))});
  cmp('Constantes',clone({C:S.C,R:S.R,SP:S.SP,EX:S.EX}),clone({C:SA.C,R:SA.R,SP:SA.SP,EX:SA.EX}));cmp('Difficultés',clone(S.DIFF),clone(SA.DIFF))}
 const parties=fs.existsSync(fParties)?fs.readFileSync(fParties,'utf8').trim().split('\n').filter(Boolean).map(l=>JSON.parse(l)):[];
 /* mêmes parties (mêmes graines) jouées avec le moteur d'avant ; inutile si sim.js n'a pas changé */
 /* 2.35 : jouées en parallèle, une par cœur */
 const PREF=!codeAvant?[]:memeMoteur?parties:await Promise.all(jouerEnParallele({code:codeAvant},SCENARIOS.filter(sc=>parties.some(p=>p.graine==sc.graine)).map(sc=>({sc}))));
 const audit=auditer(S);
 const jeuIdentique=J.ko.length==0&&memeMoteur;
 const gameplay={verdict:jeuIdentique?'identique':'change',
  resume:jeuIdentique?`Identique à ${avant} : sim.js n'a pas changé`:J.ko.length?`${J.ko.length} mécanique(s) en échec : à examiner`:`Moteur modifié par rapport à ${avant} : à examiner et à valider par vous`,
  details:[`Moteur de jeu (sim.js) : ${!codeAvant?`introuvable dans ${avant}`:memeMoteur?`identique à ${avant}`:`modifié par rapport à ${avant}`}.`,
   `Mécaniques vérifiées (construction, déplacements, combats, économie, vagues, fin de partie, IA, labyrinthe, tables) : ${J.ok} conformes, ${J.ko.length} en échec.`,
   `Statistiques des tours et monstres : ${diffs.length?diffs.length+' valeur(s) changée(s)':'aucune valeur changée'} par rapport à ${avant}.`,
   `Parties entre IA : ${parties.length} jouées, ${parties.filter(p=>{const r=PREF.find(x=>x.graine==p.graine);return r&&r.final==p.final}).length} identiques à celles de ${avant}.`,
   `Documentation (CLAUDE.md) comparée au code : ${audit.verifie.tours} tours, ${audit.verifie.monstres} monstres, ${audit.verifie.archetypes} archétypes, ${audit.verifie.difficultes} difficultés — ${audit.ecarts.length?audit.ecarts.length+' écart(s), non corrigé(s)':'aucun écart'}.`],
  echecs:J.ko,diffs,parties,PREF,audit};

 /* ---------- 🎨 visuel ---------- */
 let visuel={verdict:'non',resume:'Non vérifié',details:[],ecrans:[]};
 if(sansVisuel)visuel.details.push('Comparaison visuelle non demandée (--sans-visuel).');
 else if(!N.disponible())visuel.details.push('Playwright absent sur cette machine : comparaison visuelle impossible.');
 else{const {comparer}=require('./comparer-visuel');const r=await comparer(avant);
  const changes=r.ecrans.filter(e=>!e.identique);
  visuel={verdict:!r.fiable?'non':changes.length?'change':'identique',
   resume:!r.fiable?'Comparaison non fiable sur cette machine':changes.length?`${changes.length} écran(s) différent(s) : à examiner et à valider par vous`:`Identique à ${avant} sur les ${r.ecrans.length} écrans comparés`,
   details:[`Avant : ${avant}. Après : fichiers actuels. Même machine, même navigateur, même séance, graine 12345, horloge figée.`,
    `Police : ${r.police=='reelle'?'Fredoka chargée des deux côtés':'police de remplacement des deux côtés'}. Témoin (même version capturée deux fois) : ${r.temoin!==undefined?r.temoin.toFixed(2)+' %':'non mesuré'}.`,
    'Seule la partie visible de chaque écran est comparée (ce qui est sous la ligne de flottaison n\'est pas vu).',...r.remarques],ecrans:r.ecrans};
 }
 const html=await page({technique,gameplay,visuel,avant});
 fs.writeFileSync(path.join(DOSSIER,'bilan.html'),html);
 /* ---------- résumé ---------- */
 const icone={ok:'✅',ko:'❌',identique:'✅',change:'⚠️',non:'⏸'};
 console.log(`🔧 Technique : ${icone[technique.verdict]} ${technique.resume}`);for(const e of technique.echecs)console.log(`   ❌ ${e.nom} → ${e.message}`);
 console.log(`🎮 Gameplay  : ${icone[gameplay.verdict]} ${gameplay.resume}`);for(const e of gameplay.echecs)console.log(`   ⚠️ ${e.nom} → ${e.message}`);
 for(const e of audit.ecarts)console.log(`   📄 Écart doc/code : ${e.ou} — ${e.quoi} : doc « ${e.doc} », code « ${e.code} »`);
 console.log(`🎨 Visuel    : ${icone[visuel.verdict]} ${visuel.resume}`);for(const e of visuel.ecrans.filter(e=>!e.identique))console.log(`   ⚠️ ${e.titre} (${e.format}) : ${e.pc==null?'?':e.pc.toFixed(2)} %`);
 console.log(`\nRapport complet : rapports/bilan.html`);
 process.exit(technique.verdict=='ok'?0:1);
}

/* image réduite en JPEG (le rapport reste léger pour un téléphone) */
async function vignettes(fichiers){if(!fichiers.length||!N.disponible())return {};const nav=await N.lancer(),p=await nav.newPage(),out={};
 for(const f of fichiers){const src='data:image/png;base64,'+fs.readFileSync(f).toString('base64');
  out[f]=await p.evaluate(async src=>{const i=new Image();await new Promise(ok=>{i.onload=ok;i.src=src});const k=Math.min(1,1400/i.width),c=document.createElement('canvas');c.width=i.width*k;c.height=i.height*k;c.getContext('2d').drawImage(i,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.82)},src)}
 await nav.close();return out}

async function page({technique,gameplay,visuel,avant}){
 const v=visuel.ecrans,imgs=await vignettes(v.map(e=>e.image||e.apres).filter(Boolean));
 const boite=(titre,b,cls)=>`<section class="${cls}"><h2>${titre}</h2><p class="verdict">${esc(b.resume)}</p><ul>${b.details.map(d=>`<li>${esc(d)}</li>`).join('')}</ul>`;
 const coul={ok:'ok',ko:'ko',identique:'ok',change:'warn',non:'na'};
 let h=`<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bilan Winter Realms</title><style>
:root{--bg:#f6f4ee;--fg:#1d1d1b;--card:#fff;--ok:#1f7a3f;--warn:#a35c00;--ko:#b3261e;--na:#5f6368;--line:#ddd8cc}
@media(prefers-color-scheme:dark){:root{--bg:#141614;--fg:#ecebe6;--card:#1f221f;--ok:#5cc884;--warn:#f0a94b;--ko:#ff8a80;--na:#a0a4a8;--line:#333}}
body{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,sans-serif;margin:0;padding:16px;max-width:900px;margin:auto}
h1{font-size:22px;margin:4px 0 2px}.sous{color:var(--na);margin:0 0 14px;font-size:14px}
section{background:var(--card);border-radius:12px;padding:12px 14px;margin:12px 0;border-left:6px solid var(--na)}
section.ok{border-color:var(--ok)}section.warn{border-color:var(--warn)}section.ko{border-color:var(--ko)}
h2{font-size:18px;margin:0 0 4px}.verdict{font-weight:700;margin:0 0 6px}.ok .verdict{color:var(--ok)}.warn .verdict{color:var(--warn)}.ko .verdict{color:var(--ko)}
ul{padding-left:20px;margin:6px 0}li{margin:3px 0}table{border-collapse:collapse;width:100%;font-size:13px;margin:8px 0;display:block;overflow-x:auto}
td,th{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;white-space:nowrap}img{width:100%;border-radius:8px;margin:6px 0 14px}
.note{font-size:13px;color:var(--na)}h3{font-size:15px;margin:12px 0 4px}</style></head><body>
<h1>Bilan de l'évolution</h1><p class="sous">Généré le ${new Date().toLocaleString('fr-FR',{timeZone:'Europe/Paris'})} · branche ${esc(git('rev-parse','--abbrev-ref','HEAD')||'?')} · comparée à ${esc(avant)}</p>
<p class="note">Trois bilans séparés. Un bilan technique réussi ne valide ni le gameplay ni le rendu : ces deux-là indiquent seulement « identique » ou « changé », et c'est vous qui validez.</p>`;
 h+=boite('🔧 Technique — tests et erreurs',technique,coul[technique.verdict]);
 if(technique.echecs.length)h+=`<h3>Échecs</h3><ul>${technique.echecs.map(e=>`<li>${esc(e.nom)} → ${esc(e.message)}</li>`).join('')}</ul>`;h+='</section>';
 h+=boite('🎮 Gameplay — mécaniques, statistiques, équilibrage',gameplay,coul[gameplay.verdict]);
 if(gameplay.echecs.length)h+=`<h3>Mécaniques en échec</h3><ul>${gameplay.echecs.map(e=>`<li>${esc(e.nom)} → ${esc(e.message)}</li>`).join('')}</ul>`;
 if(gameplay.diffs.length)h+=`<h3>Valeurs changées</h3><table><tr><th>Élément</th><th>Valeur</th><th>Avant</th><th>Maintenant</th></tr>${gameplay.diffs.map(d=>`<tr><td>${esc(d.nom)}</td><td>${esc(d.champ)}</td><td>${esc(JSON.stringify(d.avant))}</td><td>${esc(JSON.stringify(d.apres))}</td></tr>`).join('')}</table>`;
 if(gameplay.parties.length){const m=l=>l.reduce((s,p)=>s+p.duree,0)/l.length/60;
  h+=`<h3>Parties entre IA (le siège « joueur » est joué par l'IA)</h3><p class="note">Durée moyenne : ${m(gameplay.parties).toFixed(1)} min (avant : ${gameplay.PREF.length?m(gameplay.PREF).toFixed(1):'?'} min). « Joueur éliminé » = la partie s'arrête quand le siège joueur tombe, comme en solo.</p><table><tr><th>Faction joueur</th><th>Difficulté</th><th>Durée</th><th>Issue</th><th>Revenus finaux</th><th>Avant</th></tr>`;
  for(const p of gameplay.parties){const r=gameplay.PREF.find(x=>x.graine==p.graine)||{};h+=`<tr><td>${FACTIONS[p.faction]}</td><td>${NIVEAUX[p.difficulte]}</td><td>${(p.duree/60).toFixed(1)} min</td><td>${p.gagnant==0?'Joueur gagne':'Joueur éliminé'}</td><td>${p.revenus.join(' / ')}</td><td>${r.final==p.final?'= identique':r.duree?'≠ '+(r.duree/60).toFixed(1)+' min, '+(r.gagnant==0?'joueur gagne':'joueur éliminé'):'—'}</td></tr>`}h+='</table>'}
 h+=`<h3>Écarts entre CLAUDE.md et le code</h3>${gameplay.audit.ecarts.length?`<table><tr><th>Où</th><th>Quoi</th><th>Doc</th><th>Code</th></tr>${gameplay.audit.ecarts.map(e=>`<tr><td>${esc(e.ou)}</td><td>${esc(e.quoi)}</td><td>${esc(e.doc)}</td><td>${esc(e.code)}</td></tr>`).join('')}</table><p class="note">Signalés seulement, jamais corrigés automatiquement.</p>`:'<p>Aucun écart sur les tableaux chiffrés.</p>'}</section>`;
 h+=boite('🎨 Visuel — captures et comparaison',visuel,coul[visuel.verdict]);
 for(const e of v){const src=imgs[e.image||e.apres];h+=`<h3>${e.identique?'✅':'⚠️'} ${esc(e.titre)} — ${e.format} — ${e.pc==null?'pas d\'image avant':e.pc.toFixed(2)+' % de pixels changés'}</h3>${src?`<img alt="${esc(e.titre)}" src="${src}">`:''}`}
 return h+'</section></body></html>';
}
main().catch(e=>{console.error('Le bilan n\'a pas pu être produit : '+e.message);process.exit(1)});
