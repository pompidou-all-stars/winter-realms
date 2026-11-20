/* Winter Realms — simulation partagée (navigateur + serveur). Aucun accès au DOM ni au son ici. */
const C=13,R=17,SP=[6,0],EX=[6,16],DIRS=[[1,0],[-1,0],[0,1],[0,-1]],INF=1e9,OUT='#2b1d12';
const BASE_TW=[
 {n:'Archer',c:20,r:2.8,d:8,cd:.5,ps:10,col:'#6aa84f',s:'arrow'},
 {n:'Canon',c:50,r:2.5,d:20,cd:1.2,ps:6.5,sp:1.1,gr:1,col:'#b0703a',s:'canon',tag:'sol'},
 {n:'Givre',c:40,r:2.5,d:2,cd:.9,ps:8,sl:1.5,fsp:1.2,mag:1,col:'#3d85c6',s:'frost',tag:'magie · zone'},
 {n:'Mage',c:90,r:3.2,d:55,cd:1.4,ps:7.5,mg:1,mag:1,col:'#8e44ad',s:'mage',tag:'magie · détecte'},
 {n:'Garde',c:30,r:1.5,d:20,cd:.55,me:1,gr:1,col:'#c0392b',s:'slash',tag:'sol'},
 {n:'Flammes',c:70,r:2,d:3,cd:.12,fl:1,col:'#e67e22',s:'flame'}];
/* ralentissements selon le niveau de la tour (2.18), du niveau 1 au niveau 5. p : part de vitesse retirée, d : durée (s), r : rayon de la zone du Givre (cases).
   Deux familles : le froid (Givre, Totem des pluies glacées) et les racines ; elles s'additionnent, mais la vitesse ne descend jamais sous SF_MIN (règle d'or n°1, 2.39). */
const GIVRE_BONUS=.1,SF_MIN=.3;
const GIVRE_LV={p:[.2,.275,.35,.425,.5],d:[1.5,1.8,2.1,2.4,2.7],r:[1.2,1.4,1.6,1.8,2]},RACINES_LV={p:[.1,.15,.2,.25,.3],d:[.72,.85,1,1.15,1.3]};
/* ---------- 2.39 : races asymétriques ----------
   Chaque race a sa mécanique propre, ses états et ses combos, et 10 tours qui couvrent une grille de rôles commune (ROLES_J).
   L'emplacement j fixe le RÔLE (utilisé par l'IA et par la fiche), pas l'archétype : skin ne sert qu'au dessin 2D et au repli 3D.
   Règles d'équilibrage centrales (voir CLAUDE.md §5 et tests/simulation/races.test.js) :
   - REGLES.radar : profil de chaque race sur 6 axes, somme RADAR_SOMME, chaque axe entre RADAR_MIN et RADAR_MAX, au moins un axe ≤ 4, au plus deux ≥ 7 ;
   - couverture obligatoire : tour sol et air ≤ 25 or (j0), anti-aérien dédié (j4), détection ≤ 120 or (j5), 2 sources non magiques, une réponse aux blindés ;
   - plafonds : amplification cumulée AMP_MAX, vitesse ≥ SF_MIN, poison ≤ DOSE_MAX doses, immobilisations à rendement décroissant (IM_IMMU) et moitié pour les boss ;
   - une seule tour ultime (j9) par terrain.
   Champs des tours (en plus de ceux de BASE_TW) : air / sol (multiplicateur de dégâts contre les volants / au sol), ao (air seulement), rmin (portée minimale),
   cl (nombre de cibles au corps à corps), ch (rebonds d'éclair), ln (tir en ligne qui traverse), bm / bmx (rayon qui monte en puissance), pu (impulsion : 0 = tout ce qui est à portée, n = n cibles),
   no (ne tire pas), det (détecte les invisibles), u (ultime), eco (or toutes les 10 s par niveau), prime (prime en plus à sa portée), au (aura sur les tours voisines),
   effets à l'impact : im (immobilise, s), ab (abat un volant, s), mk (Marqué, s), ma (Maudit, s), tw (Trempé), hx (Maléfice, s), pz / pv (doses de poison / dégâts par dose et par s),
   sg (saignement : part des PV max par s), br (Brisé, points), bu (Brûlant, dégâts par s), pe (Pestiféré, dégâts par s), ex (exécution sous ce seuil de PV), pierce (part d'armure ignorée),
   combos : jug (Jugement sur un Marqué), chu (Chute sur un Abattu), bre (Brèche sur un Brisé au maximum), fus (Fusion sur un Brûlant), cond (Conduction sur un Trempé), flo (Floraison), xim (bonus sur un immobilisé), spe (bonus contre les spéciaux et boss). */
const AMP_MAX=.6,DOSE_MAX=10,IM_IMMU=1.5,COH=.04,FUREUR=.03,FUREUR_MAX=10,CROIT=.01,CROIT_MAX=.25,AMES_MAX=30,BRISE=.15,BRISE_MAX=5,FORGE=.85;
const ROLES_J=[{name:'Base',tag:'sol et air'},{name:'Proximité',tag:'corps à corps'},{name:'Contrôle',tag:'contrôle'},{name:'Zone',tag:'zone'},{name:'Anti-aérien',tag:'anti-aérien'},
 {name:'Détection',tag:'détecte'},{name:'Signature',tag:'signature'},{name:'Soutien',tag:'soutien'},{name:'Anti-boss',tag:'anti-boss'},{name:'Ultime',tag:'ultime'}];
const REGLES={RADAR_SOMME:30,RADAR_MIN:3,RADAR_MAX:8,axes:['Mono-cible','Zone','Anti-aérien','Anti-blindé et boss','Contrôle','Économie et montée en puissance'],court:['Mono-cible','Zone','Anti-air','Anti-blindé','Contrôle','Économie']};
const RACES=[
 {name:'Royaume d’Aubeval',court:'Aubeval',icon:'👑',color:'#d8b45c',dark:'#59451f',ex:'Alliance',
  desc:'Ordre, foi et ingénierie de siège : la race la plus polyvalente, la seule à avoir une économie.',
  histoire:'Les chevaliers d’Aubeval tiennent les cols du Sud depuis mille hivers. Leurs murs se serrent en formation, leurs chapelles marquent l’ennemi du sceau du Jugement, et leurs marchands financent la guerre.',
  meca:{n:'Cohésion',txt:'Chaque tour d’Aubeval voisine donne +4 % de dégâts (jusqu’à +16 %). Les murs serrés du labyrinthe deviennent plus forts.'},
  etats:['Marqué : +15 % de dégâts subis ; l’Inquisiteur et le Rayon de l’Aube font détoner le sceau','Abattu : un volant tombe au sol 2 s, les tours « sol » peuvent le frapper'],
  forces:'polyvalence, économie, anti-boss',faible:'zone moyenne, peu de contrôle',radar:[6,4,6,7,3,4],up:{0:8},
  combos:[{n:'Jugement',a:[5,8],txt:'La Chapelle du guet marque un monstre ; l’Inquisiteur (ou le Rayon de l’Aube) fait détoner le sceau : +60 % sur ce coup.'},
   {n:'Chute',a:[2,3],txt:'Le Lance-filets abat un volant ; le Trébuchet l’écrase au sol : dégâts ×1,5.'},
   {n:'Formation',a:[7,0],txt:'Autour de l’Étendard royal, chaque voisin compte double pour la Cohésion : jusqu’à +32 % de dégâts.'}],
  tours:[
   {n:'Tour d’arbalétriers',skin:0,c:20,r:2.9,d:8,cd:.5,txt:'Carreaux réguliers, au sol et dans les airs. La base, solide et bon marché.'},
   {n:'Poste de hallebardiers',skin:4,me:1,gr:1,c:30,r:1.5,d:16,cd:.6,cl:2,txt:'Corps à corps : chaque balayage frappe 2 monstres à la fois.'},
   {n:'Lance-filets',skin:2,c:45,r:2.6,d:3,cd:2.2,ps:9,im:.8,ab:2,txt:'Lance un filet : le monstre est immobilisé 0,8 s. Un volant est abattu au sol pendant 2 s.'},
   {n:'Trébuchet',skin:1,gr:1,c:65,r:3.6,rmin:1.5,d:34,cd:2.4,ps:5,sp:1.3,chu:1.5,txt:'Très longue portée et grosse explosion, au sol. Ne tire pas à moins de 1,5 case.'},
   {n:'Baliste céleste',skin:0,c:60,r:3.3,d:22,cd:1.3,ln:1,air:2,sol:.5,txt:'Carreau qui traverse tout sur sa ligne. Dégâts ×2 contre les volants, ×0,5 au sol.'},
   {n:'Chapelle du guet',skin:3,mag:1,det:1,c:80,r:3,d:14,cd:1,mk:3,txt:'Révèle les invisibles et pose le sceau du Jugement (Marqué : +15 % de dégâts subis pendant 3 s).'},
   {n:'Comptoir marchand',skin:4,no:1,c:100,r:2.5,eco:5,prime:.2,txt:'Ne tire pas. +5 or toutes les 10 s par niveau, et +20 % de prime sur les monstres tués à sa portée.'},
   {n:'Étendard royal',skin:4,no:1,c:90,r:1.5,au:{cad:.15,coh:2},txt:'Ne tire pas. Tours voisines : +15 % de cadence, et la Cohésion compte double autour de lui.'},
   {n:'Inquisiteur',skin:3,c:140,r:3,d:48,cd:1.3,pierce:1,spe:2,jug:1.6,txt:'Ignore l’armure. Dégâts ×2 contre les monstres spéciaux et les boss. Fait détoner le sceau des Marqués.'},
   {n:'Rayon de l’Aube',skin:3,u:1,mag:1,c:260,r:3.4,d:14,cd:.25,bm:.25,bmx:4,jug:1.6,txt:'Ultime, une seule par terrain. Rayon continu : +25 % à chaque tir sur la même cible, jusqu’à ×4.'}]},
 {name:'Clans de l’Orage Blanc',court:'Orage Blanc',icon:'⚡',color:'#78a94b',dark:'#294322',ex:'Horde',
  desc:'Chamanes des steppes gelées : totems, tambours, foudre en chaîne et rage.',
  histoire:'Quand l’orage blanc gronde sur la toundra, les clans dressent leurs totems. Leurs chamanes appellent la foudre, leurs tambours réveillent la rage, et chaque ennemi abattu nourrit la Fureur du clan.',
  meca:{n:'Fureur',txt:'Chaque monstre tué par une tour lui donne 1 charge de Fureur (+3 % de cadence, jusqu’à 10). Une charge se perd toutes les 2 s sans victoire. À 10 charges : Rage, +30 % de dégâts pendant 3 s.'},
  etats:['Trempé : −20 % de vitesse ; les éclairs rebondissent deux fois plus','Maléfice : le monstre devient un crapaud 1,5 s (armure 0, vitesse ×0,6), jamais sur un boss','Saignement : perd 1,5 % de ses PV max par seconde'],
  forces:'zone en chaîne, foules, anti-aérien',faible:'monstres isolés et blindés, boss',radar:[3,8,6,3,5,5],up:{0:6,1:8},
  combos:[{n:'Conduction',a:[2,6],txt:'Le Totem des pluies glacées trempe les monstres ; l’éclair du Totem de foudre rebondit deux fois plus sur un Trempé.'},
   {n:'Rage du clan',a:[7,1],txt:'Les Grands tambours doublent la Fureur gagnée : la Hutte du berserker atteint vite 10 charges et entre en Rage.'},
   {n:'Crapaud saignant',a:[5,8],txt:'Le Maléfice retire l’armure ; le Totem de sang fait saigner le crapaud sans rien perdre.'}],
  tours:[
   {n:'Lanceurs de haches',skin:0,c:20,r:2.6,d:8.5,cd:.5,txt:'Haches lancées au sol et dans les airs. Gagne vite de la Fureur.'},
   {n:'Hutte du berserker',skin:4,me:1,gr:1,c:30,r:1.5,d:19,cd:.55,fu2:1,txt:'Corps à corps. Sa Fureur monte deux fois plus vite.'},
   {n:'Totem des pluies glacées',skin:2,mag:1,c:40,r:2.5,d:2,cd:1,ps:8,sl:1.5,fsp:1.2,tw:1,txt:'Pluie glacée en zone : ralentit et trempe les monstres (les éclairs rebondissent deux fois plus).'},
   {n:'Catapulte à rochers',skin:1,gr:1,c:55,r:2.7,d:21,cd:1.3,ps:6.5,sp:1.1,im:.3,txt:'Rocher en zone, au sol, qui étourdit 0,3 s.'},
   {n:'Aire des aigles-tempête',skin:0,c:60,r:3,d:16,cd:.8,ch:2,air:2,sol:.6,txt:'L’aigle plonge et son éclair rebondit sur 2 autres cibles. Dégâts ×2 contre les volants.'},
   {n:'Hutte du chaman des esprits',skin:3,mag:1,det:1,c:85,r:3.1,d:26,cd:1.4,hx:1.5,txt:'Révèle les invisibles. Maléfice : change le monstre en crapaud 1,5 s (armure 0, vitesse ×0,6).'},
   {n:'Totem de foudre',skin:3,mag:1,c:75,r:2.8,d:18,cd:1.1,ch:3,cond:2,txt:'Chaîne d’éclairs : 3 rebonds, −25 % par rebond. Deux fois plus de rebonds sur un Trempé.'},
   {n:'Grands tambours de guerre',skin:4,no:1,c:90,r:1.5,au:{cad:.2,fu:2},txt:'Ne tire pas. Tours voisines : +20 % de cadence et Fureur gagnée doublée.'},
   {n:'Totem de sang',skin:3,c:120,r:2.6,d:6,cd:1,sg:.015,txt:'Saignement : la cible perd 1,5 % de ses PV max par seconde pendant 3 s. L’arme des clans contre les géants.'},
   {n:'Cœur de l’Orage',skin:3,u:1,mag:1,c:280,r:4,d:90,cd:4,pu:6,fuG:1,txt:'Ultime, une seule par terrain. Toutes les 4 s, 6 éclairs tombent à sa portée ; chaque victime donne +1 Fureur à toutes tes tours.'}]},
 {name:'Elfes de Lunebois',court:'Lunebois',icon:'🌿',color:'#69bd83',dark:'#214b38',ex:'Sylvestres',
  desc:'La forêt vivante, le venin et la patience : poison, racines et tours qui grandissent.',
  histoire:'Sous la lune d’hiver, les forêts de Lunebois ne dorment jamais. Leurs archers trempent leurs flèches dans le venin, leurs gardiens enracinent l’ennemi, et leurs arbres grandissent à chaque saison de guerre.',
  meca:{n:'Croissance',txt:'Chaque tour gagne +1 % de dégâts et de portée toutes les 10 s sur place, jusqu’à +25 %. La vendre lui fait perdre ce bonus.'},
  etats:['Empoisonné : jusqu’à 10 doses, chacune inflige des dégâts par seconde qui ignorent l’armure','Enraciné : le monstre ne bouge plus (moitié moins longtemps pour un boss)'],
  forces:'blindés, contrôle, contagion',faible:'démarrage lent, monstres rapides',radar:[4,5,5,6,7,3],up:{0:8,3:6},
  combos:[{n:'Floraison',a:[0,6],txt:'Les flèches et la Fleur de venin empilent le poison ; le Cercle de Floraison fait éclore toutes les doses d’un coup.'},
   {n:'Terreau',a:[2,3],txt:'Sur un monstre enraciné par le Gardien, le poison de la Fleur de venin agit deux fois plus vite.'},
   {n:'Spores',a:[3,0],txt:'Un monstre qui meurt avec 5 doses ou plus éclate en spores et empoisonne ses voisins.'}],
  tours:[
   {n:'Archers sylvains',skin:0,c:20,r:2.8,d:5.4,cd:.5,pz:1,pv:.3,txt:'Flèches au sol et dans les airs ; chacune ajoute 1 dose de poison.'},
   {n:'Haie de ronces',skin:4,gr:1,c:25,r:1.3,d:4.5,cd:.5,pu:0,pz:1,pv:.3,txt:'Épines : blesse et empoisonne tout ce qui passe à côté, au sol.'},
   {n:'Gardien enracineur',skin:2,gr:1,c:45,r:2.2,d:5.4,cd:4,pu:0,im:1,txt:'Toutes les 4 s, des racines immobilisent 1 s tous les monstres au sol à sa portée.'},
   {n:'Fleur de venin',skin:1,c:55,r:2.4,d:4,cd:1,ps:6.5,sp:1.3,pz:2,pv:.5,txt:'Nuage de venin en zone, au sol et dans les airs : 2 doses de poison.'},
   {n:'Nid des chouettes des neiges',skin:0,c:55,r:3.1,d:10.8,cd:.7,air:2,sol:.5,pz:1,pv:.4,txt:'Les chouettes chassent les volants (dégâts ×2) et les empoisonnent.'},
   {n:'Puits de lune',skin:3,mag:1,det:1,c:80,r:3.2,d:19.8,cd:1.3,au:{cg:2},txt:'Révèle les invisibles. Les tours voisines grandissent deux fois plus vite.'},
   {n:'Cercle de Floraison',skin:3,mag:1,c:90,r:2.8,d:9,cd:1.6,flo:1.3,txt:'Fait éclore le poison : toutes les doses de la cible explosent d’un coup.'},
   {n:'Bosquet ancien',skin:4,no:1,c:85,r:1.5,au:{rg:.12,dose:1},txt:'Ne tire pas. Tours voisines : +12 % de portée et +1 dose de poison par coup.'},
   {n:'Tireur des cimes',skin:0,c:130,r:4.4,d:54,cd:1.8,vise:'pv',xim:1.5,txt:'Très longue portée, vise le monstre le plus résistant. Dégâts ×1,5 sur un enraciné.'},
   {n:'Arbre-Mère',skin:2,u:1,gr:1,c:250,r:3.6,d:36,cd:10,pu:0,im:1.5,cgG:3,txt:'Ultime, une seule par terrain. Toutes les 10 s, enracine tout à sa portée ; toutes tes tours grandissent trois fois plus vite.'}]},
 {name:'Nains de Hautroc',court:'Hautroc',icon:'⚒️',color:'#c58b55',dark:'#56351f',ex:'Nains',
  desc:'Forge, runes et artillerie lourde : la race de l’armure brisée et de la chauffe.',
  histoire:'Dans les halls de Hautroc, les forges ne s’éteignent jamais. Les nains chauffent leurs canons au rouge, gravent des runes qui fendent les armures et posent des mines sous la neige.',
  meca:{n:'Forge et Chauffe',txt:'Améliorations 15 % moins chères et plus rapides ; étourdissements subis deux fois plus courts. Les tours à tir continu chauffent (+50 % de dégâts au maximum) mais s’arrêtent 2 s en surchauffe, sauf à côté d’une Enclume runique.'},
  etats:['Brisé : −12 % d’armure par point, jusqu’à 5 points','Brûlant : dégâts par seconde'],
  forces:'blindés, boss, artillerie au sol',faible:'volants hors de la tour dédiée, aucun ralentissement',radar:[6,6,4,8,3,3],up:{1:6,3:8},
  combos:[{n:'Brèche',a:[2,3],txt:'La Baliste perce-plaque brise l’armure ; à 5 points, le Mortier runique (et Grondeterre) font +40 %.'},
   {n:'Fusion',a:[6,1],txt:'Un monstre Brûlant frappé par le Marteau-pilon perd 2 points d’armure de plus.'},
   {n:'Forge froide',a:[7,0],txt:'À côté de l’Enclume runique, l’Arbalète à répétition et la Gueule de forge ne surchauffent plus.'}],
  tours:[
   {n:'Arbalète à répétition',skin:0,c:20,r:2.7,d:5.6,cd:.3,ht:.04,txt:'Tir très rapide au sol et dans les airs, qui monte en Chauffe.'},
   {n:'Marteau-pilon',skin:4,gr:1,c:35,r:1.4,d:25,cd:.9,pu:0,im:.2,fus:2,txt:'Onde de choc autour de lui, au sol, qui sonne les monstres 0,2 s.'},
   {n:'Baliste perce-plaque',skin:0,c:45,r:2.9,d:17.5,cd:.8,br:1,txt:'Brise l’armure : −12 % par coup, jusqu’à 5 points.'},
   {n:'Mortier runique',skin:1,gr:1,c:60,r:3.4,d:32.5,cd:1.6,ps:6,sp:1.2,bre:1.4,txt:'Obus runique en zone, longue portée, au sol.'},
   {n:'Canon antiaérien à éclats',skin:1,ao:1,c:60,r:3.2,d:23.8,cd:.6,ps:9,sp:.9,txt:'Ne vise que les volants : éclats qui explosent en l’air.'},
   {n:'Phare runique',skin:3,det:1,c:75,r:3.6,d:15,cd:1,rvb:1,txt:'Rayon runique. Révèle les invisibles et brise d’un point l’armure de tout ce qui passe dans sa lumière.'},
   {n:'Gueule de forge',skin:5,fl:1,c:70,r:2,d:4,cd:.12,bu:4,ht:.02,txt:'Souffle de flammes en cône qui rend les monstres Brûlants, et monte en Chauffe.'},
   {n:'Enclume runique',skin:4,no:1,c:90,r:1.5,au:{dm:.15,nf:1},txt:'Ne tire pas. Tours voisines : +15 % de dégâts, et elles ne surchauffent plus.'},
   {n:'Champ de mines',skin:1,gr:1,c:110,r:2.2,d:68.8,cd:2.5,mn:4,txt:'Pose jusqu’à 4 mines runiques sur le chemin à sa portée ; elles explosent au passage.'},
   {n:'Grondeterre',skin:1,u:1,gr:1,c:280,r:5,d:275,cd:6,ln:1,pierce:1,bre:1.4,txt:'Ultime, une seule par terrain. Canon de siège : toutes les 6 s, un tir en ligne qui traverse tout et ignore l’armure.'}]},
 {name:'Cour des Ossements',court:'Ossements',icon:'☠️',color:'#a879c9',dark:'#39204d',ex:'Légion des ombres',
  desc:'Nécromancie, âmes, peste et malédictions : la race de l’invocation et du nombre.',
  histoire:'Sous les glaciers dorment les morts de mille batailles. La Cour des Ossements récolte les âmes des vaincus, maudit les vivants, répand la peste et relève les morts pour qu’ils combattent encore.',
  meca:{n:'Âmes',txt:'Chaque monstre qui meurt près de tes tours donne 1 âme (2 s’il était Maudit), jusqu’à 30. Le Nécromancien et le Colosse d’os les dépensent ; le Puits des âmes les convertit.'},
  etats:['Maudit : +20 % de dégâts subis','Pestiféré : dégâts par seconde ; à sa mort, la peste saute sur ses voisins'],
  forces:'foules, amplification, blocage',faible:'boss isolé, démarrage lent',radar:[3,6,4,4,6,7],up:{0:8,1:6},
  combos:[{n:'Récolte',a:[2,0],txt:'Un monstre Maudit par l’Obélisque qui meurt donne 2 âmes au lieu d’une.'},
   {n:'Épidémie',a:[3,2],txt:'La peste de l’Autel fait deux fois plus de dégâts sur un monstre Maudit.'},
   {n:'Armée des morts',a:[6,3],txt:'Avec un Autel de peste, les morts relevés par le Nécromancien répandent la peste en frappant.'}],
  tours:[
   {n:'Tour des archers squelettes',skin:0,c:20,r:2.8,d:7.8,cd:.5,txt:'Flèches d’os au sol et dans les airs.'},
   {n:'Ossuaire',skin:4,me:1,gr:1,c:35,r:1.8,d:8,cd:3,im:1.5,os:1,txt:'Des squelettes sortent de la neige et retiennent un monstre 1,5 s.'},
   {n:'Obélisque de malédiction',skin:2,mag:1,c:40,r:2.6,d:3,cd:.9,ps:8,sp:1,ma:3,txt:'Malédiction en zone : Maudit, +20 % de dégâts subis pendant 3 s.'},
   {n:'Autel de peste',skin:1,c:55,r:2.4,d:4,cd:1.2,ps:6.5,sp:1.3,pe:5,txt:'Nuage de peste en zone : dégâts dans la durée, qui sautent sur les voisins à la mort.'},
   {n:'Perchoir des gargouilles',skin:0,c:60,r:3,d:18,cd:.7,air:2,sol:.6,txt:'Les gargouilles harcèlent les volants : dégâts ×2 contre eux.'},
   {n:'Œil du Voile',skin:3,mag:1,det:1,c:85,r:3.2,d:24,cd:1.3,ma:3,txt:'Révèle les invisibles et maudit sa cible.'},
   {n:'Nécromancien',skin:3,mag:1,c:95,r:2.8,d:10,cd:1.2,rz:{d:12,t:6},txt:'Dépense 1 âme pour relever un monstre tué à sa portée : le mort remonte le chemin et frappe.'},
   {n:'Puits des âmes',skin:4,no:1,c:80,r:1.5,au:{am:1},txt:'Ne tire pas. Tours voisines : +2 % de cadence par tranche de 5 âmes. Âmes au maximum : 5 âmes deviennent de l’or.'},
   {n:'Faucheuse',skin:3,c:130,r:2.6,d:50,cd:1.4,ex:.12,txt:'Exécute les monstres sous 12 % de PV. Contre un boss : +50 % de dégâts sous 25 %.'},
   {n:'Colosse d’os',skin:4,u:1,no:1,c:260,r:3,cd:45,col:{am:15,d:60,t:12},txt:'Ultime, un seul par terrain. Dépense 15 âmes : un colosse d’os remonte le chemin et écrase tout autour de lui.'}]}];
const FACTIONS=RACES;
for(const F of RACES)F.towers=F.tours.map(o=>o.n);
/* ancienne table (avant 2.39), gardée pour compatibilité : l'emplacement j donnait l'archétype */
const ARCH=[0,4,2,1,5,3,0,4,2,3],ROLE=ROLES_J;
/* estimation des dégâts par seconde (niveau 1, une cible, poison compris) et facteur de zone, pour l'IA et la fiche */
function estimer(T){const tir=T.no?0:T.d/T.cd,dot=T.dot=(T.pz?Math.min(DOSE_MAX,T.pz/T.cd*4)*T.pv:0)+(T.bu||0)+(T.pe?T.pe*.6:0);
 T.zf=T.sp?2.5:T.fl?3:T.ch?1+T.ch*.6:T.ln?2:T.pu===0?3:T.pu?Math.min(3,T.pu*.5):T.cl?T.cl:1;T.ed=tir+dot;return T}
const TW=RACES.flatMap((F,fi)=>F.tours.map((o,j)=>{const B=BASE_TW[o.skin];
 const T={...B,sp:0,sl:0,fsp:0,me:0,fl:0,gr:0,mag:0,mg:0,...o,ps:o.ps||B.ps||9,s:o.s||B.s,col:F.color,faction:fi,j,role:ROLES_J[j].name,tag:ROLES_J[j].tag,
  air:o.air||1,sol:o.sol||1,mg:o.det?1:0,ctl:j==2?1:0,cd:o.cd||1,d:o.d||0};
 if(T.fsp)T.sl=GIVRE_LV.d[0];if(T.no){T.d=0;if(!o.cd)T.cd=1}
 return estimer(T)}));
const ORDER=Array.from({length:10},(_,i)=>i);
/* cat : n = sol, f = volant, s = spécial (magique ou boss), x = né d'une division (jamais envoyé). Revenu des monstres au sol sur une courbe croissante (10 → 1, 100 → 11, 1000 → 120).
   t : palier (2.13). Le palier 1 est ouvert dès le début ; les paliers 2 et 3 s'achètent (PAL_C). Chaque palier : 12 monstres au sol, 3 volants, 8 magiques, 1 boss.
   Capacités : aura (hâte), inv (invisible), split (se divise en « kid »), acc (accéléré), mi (anti-magie), heal (soin), arm (armure), stun (étourdit), hero (boss). */
const CR=[
 /* ---- palier 1 ---- */
 {n:'Sapeur gobelin',cat:'n',t:1,c:10,hp:12,s:1.6,z:.75,g:'gob',col:'#8fce5a'},
 {n:'Rat des neiges',cat:'n',t:1,c:20,hp:20,s:2.2,z:.7,g:'rat',col:'#d9dfe4'},
 {n:'Warg',cat:'n',t:1,c:30,hp:33,s:2.4,z:.78,g:'wolf',col:'#9aa3ad'},
 {n:'Kobold',cat:'n',t:1,c:40,hp:48,s:1.6,z:.78,g:'kobold',col:'#d9733a'},
 {n:'Squelette du givre',cat:'n',t:1,c:50,hp:60,s:1.5,z:.85,g:'skel',col:'#e6e2d2'},
 {n:'Sanglier de guerre',cat:'n',t:1,c:60,hp:69,s:2,z:.9,g:'boar',col:'#7a4a2e'},
 {n:'Gnoll',cat:'n',t:1,c:70,hp:87,s:1.6,z:.9,g:'gnoll',col:'#c9a25a'},
 {n:'Brute orc',cat:'n',t:1,c:80,hp:101,s:1.4,z:.95,g:'orc',col:'#5f9c45'},
 {n:'Maraudeur',cat:'n',t:1,c:90,hp:114,s:1.5,z:.9,g:'raider',col:'#4f5a3a'},
 {n:'Myconide',cat:'n',t:1,c:100,hp:135,s:1.1,z:.95,g:'myco',col:'#c8322a'},
 {n:'Yéti',cat:'n',t:1,c:110,hp:149,s:1.3,z:1.15,g:'yeti',col:'#e2eaf0'},
 {n:'Troll des glaces',cat:'n',t:1,c:120,hp:160,s:1.5,z:1.1,g:'troll',col:'#57aeb0'},
 {n:'Chauve-souris',cat:'f',t:1,c:30,hp:16,s:2,z:.75,g:'bat',fly:1,col:'#7d5ba6'},
 {n:'Guêpe des glaces',cat:'f',t:1,c:50,hp:26,s:2.3,z:.7,g:'wasp',fly:1,col:'#f5c534'},
 {n:'Harpie',cat:'f',t:1,c:90,hp:55,s:1.9,z:.85,g:'harpy',fly:1,col:'#9aa4b8'},
 {n:'Chaman de guerre',cat:'s',t:1,c:80,hp:70,s:1.5,z:.85,g:'chaman',aura:1,col:'#e8b23a',tag:'hâte'},
 {n:'Spectre',cat:'s',t:1,c:150,hp:90,s:1.5,z:.9,g:'spectre',inv:1,col:'#d7defa',tag:'invisible'},
 {n:'Gelée mutante',cat:'s',t:1,c:140,hp:90,s:1.3,z:.95,g:'slime',split:'Petit limon',col:'#b5e04a',tag:'se divise'},
 {n:'Lutin des glaces',cat:'s',t:1,c:110,hp:70,s:1.5,z:.7,g:'imp',acc:1,col:'#6fc6e8',tag:'accéléré'},
 {n:'Briseur de runes',cat:'s',t:1,c:170,hp:120,s:1.4,z:1,g:'breaker',mi:1,col:'#b9c0c9',tag:'anti-magie'},
 {n:'Prêtresse',cat:'s',t:1,c:100,hp:80,s:1.4,z:.85,g:'healer',heal:1,col:'#6fcf97',tag:'soin'},
 {n:'Tortue',cat:'s',t:1,c:160,hp:140,s:1.1,z:1,g:'turtle',arm:5,col:'#8a6a3a',tag:'blindée'},
 {n:'Saboteur gobelin',cat:'s',t:1,c:190,hp:110,s:1.5,z:.85,g:'sapper',stun:1,col:'#8fce5a',tag:'étourdit'},
 {n:'Roi gobelin',cat:'s',t:1,c:450,hp:900,s:1,z:1.2,g:'gobking',arm:2,stun:1,hero:1,col:'#e0b44e',tag:'BOSS · étourdit'},
 /* ---- palier 2 ---- */
 {n:'Homme-lézard',cat:'n',t:2,c:150,hp:200,s:1.6,z:1.05,g:'lizard',col:'#4f9a5a'},
 {n:'Chevalier noir',cat:'n',t:2,c:180,hp:250,s:1.2,z:1.1,g:'knight',col:'#3a3d48'},
 {n:'Gargouille',cat:'n',t:2,c:210,hp:285,s:1.3,z:1.1,g:'gargoyle',col:'#8a8f99'},
 {n:'Loup-garou',cat:'n',t:2,c:240,hp:310,s:1.9,z:1.15,g:'werewolf',col:'#6f6458'},
 {n:'Ours de guerre',cat:'n',t:2,c:270,hp:370,s:1.5,z:1.15,g:'bear',col:'#6a4630'},
 {n:'Golem runique',cat:'n',t:2,c:300,hp:420,s:1,z:1.2,g:'golem',col:'#9a9ca6'},
 {n:'Ogre',cat:'n',t:2,c:330,hp:460,s:1.1,z:1.2,g:'ogre',col:'#c2a86a'},
 {n:'Minotaure',cat:'n',t:2,c:370,hp:500,s:1.4,z:1.2,g:'minotaur',col:'#7a4a2e'},
 {n:'Automate blindé',cat:'n',t:2,c:410,hp:580,s:1,z:1.2,g:'automaton',col:'#b07a3a'},
 {n:'Wendigo',cat:'n',t:2,c:450,hp:610,s:1.6,z:1.25,g:'wendigo',col:'#3a3330'},
 {n:'Rhinocéros de guerre',cat:'n',t:2,c:500,hp:720,s:1.5,z:1.3,g:'rhino',col:'#8a8f99'},
 {n:'Mammouth de guerre',cat:'n',t:2,c:600,hp:900,s:.9,z:1.45,g:'mammoth',col:'#6e4a30'},
 {n:'Griffon corrompu',cat:'f',t:2,c:150,hp:95,s:1.9,z:1,g:'griffon',fly:1,col:'#d9a441'},
 {n:'Vouivre',cat:'f',t:2,c:260,hp:180,s:1.8,z:1.15,g:'wyvern',fly:1,col:'#3fa060'},
 {n:'Manticore',cat:'f',t:2,c:380,hp:290,s:1.6,z:1.2,g:'manticore',fly:1,col:'#c8743a'},
 {n:'Tambour de guerre',cat:'s',t:2,c:300,hp:300,s:1.4,z:1.05,g:'drummer',aura:1,col:'#4f9a3a',tag:'hâte'},
 {n:'Assassin des ombres',cat:'s',t:2,c:380,hp:300,s:1.6,z:1,g:'assassin',inv:1,col:'#4a2a6a',tag:'invisible'},
 {n:'Golem de boue',cat:'s',t:2,c:400,hp:320,s:1.2,z:1.15,g:'mudgolem',split:'Petite boue',col:'#6b4a2a',tag:'se divise'},
 {n:'Centaure messager',cat:'s',t:2,c:340,hp:260,s:1.6,z:1.15,g:'centaur',acc:1,col:'#3a6ab0',tag:'accéléré'},
 {n:'Inquisiteur',cat:'s',t:2,c:450,hp:380,s:1.3,z:1.1,g:'inquisitor',mi:1,col:'#d9dce2',tag:'anti-magie'},
 {n:'Druidesse',cat:'s',t:2,c:330,hp:280,s:1.4,z:1.05,g:'druid',heal:1,col:'#4a7a3a',tag:'soin'},
 {n:'Scarabée cuirassé',cat:'s',t:2,c:430,hp:380,s:1.2,z:.95,g:'beetle',arm:12,col:'#2f8a7a',tag:'blindé'},
 {n:'Ingénieur nain renégat',cat:'s',t:2,c:480,hp:360,s:1.4,z:1,g:'engineer',stun:1,col:'#c8562a',tag:'étourdit'},
 {n:'Cyclope des cendres',cat:'s',t:2,c:1400,hp:2800,s:1,z:1.5,g:'cyc',arm:6,stun:1,hero:1,col:'#dba878',tag:'BOSS · étourdit'},
 /* ---- palier 3 ---- */
 {n:'Roi-liche',cat:'n',t:3,c:900,hp:1200,s:1.2,z:1.3,g:'lich',col:'#4a3470'},
 {n:'Seigneur de guerre orc',cat:'n',t:3,c:1000,hp:1350,s:1.3,z:1.35,g:'warlord',col:'#3a2c2c'},
 {n:'Élémentaire de feu',cat:'n',t:3,c:1100,hp:1400,s:1.5,z:1.4,g:'fireel',col:'#ff7a1a'},
 {n:'Démon des abysses',cat:'n',t:3,c:1250,hp:1700,s:1.4,z:1.5,g:'demon',col:'#a82a2a'},
 {n:'Golem de lave',cat:'n',t:3,c:1400,hp:2000,s:.9,z:1.5,g:'lavagolem',col:'#3a3330'},
 {n:'Ver des neiges',cat:'n',t:3,c:1550,hp:2100,s:1.2,z:1.5,g:'wyrm',col:'#eef2f5'},
 {n:'Chimère',cat:'n',t:3,c:1700,hp:2250,s:1.5,z:1.5,g:'chimera',col:'#d9a441'},
 {n:'Géant du givre',cat:'n',t:3,c:1900,hp:2700,s:1,z:1.6,g:'giant',col:'#8fb3d4'},
 {n:'Sylvain corrompu',cat:'n',t:3,c:2100,hp:3000,s:.9,z:1.6,g:'treant',col:'#5a4030'},
 {n:'Mastodonte de fer',cat:'n',t:3,c:2400,hp:3500,s:.8,z:1.6,g:'juggernaut',col:'#6c717b'},
 {n:'Béhémoth',cat:'n',t:3,c:2700,hp:3900,s:1.1,z:1.7,g:'behemoth',col:'#4a3a5a'},
 {n:'Colosse de pierre',cat:'n',t:3,c:3000,hp:4500,s:.85,z:1.75,g:'colossus',col:'#c9b48a'},
 {n:'Dragon ancien',cat:'f',t:3,c:900,hp:800,s:1.3,z:1.3,g:'dragon',fly:1,col:'#d6453d'},
 {n:'Phénix de givre',cat:'f',t:3,c:1200,hp:1000,s:1.6,z:1.3,g:'phoenix',fly:1,col:'#9fdcff'},
 {n:'Oiseau-roc',cat:'f',t:3,c:1600,hp:1400,s:1.4,z:1.45,g:'roc',fly:1,col:'#7a5634'},
 {n:'Héraut de guerre',cat:'s',t:3,c:1100,hp:1100,s:1.3,z:1.3,g:'herald',aura:1,col:'#e0b44e',tag:'hâte'},
 {n:'Faucheuse',cat:'s',t:3,c:1300,hp:1050,s:1.5,z:1.3,g:'reaper',inv:1,col:'#24252d',tag:'invisible'},
 {n:'Hydre',cat:'s',t:3,c:1400,hp:1100,s:1.1,z:1.45,g:'hydra',split:'Tête d’hydre',col:'#2f7a6a',tag:'se divise'},
 {n:'Destrier de cauchemar',cat:'s',t:3,c:1200,hp:950,s:1.6,z:1.3,g:'nightmare',acc:1,col:'#a04aff',tag:'accéléré'},
 {n:'Dévoreur de mana',cat:'s',t:3,c:1500,hp:1300,s:1.2,z:1.35,g:'manaeater',mi:1,col:'#5a2a7a',tag:'anti-magie'},
 {n:'Grande prêtresse de sang',cat:'s',t:3,c:1250,hp:1000,s:1.3,z:1.25,g:'bloodpriest',heal:1,col:'#8a2232',tag:'soin'},
 {n:'Tortue-dragon',cat:'s',t:3,c:1600,hp:1400,s:1,z:1.45,g:'dragonturtle',arm:25,col:'#8a3a2a',tag:'blindée'},
 {n:'Golem du tonnerre',cat:'s',t:3,c:1700,hp:1400,s:1.1,z:1.45,g:'thunder',stun:1,col:'#3a4a6a',tag:'étourdit'},
 {n:"Azh’Khar, seigneur des lames",cat:'s',t:3,c:3500,hp:7000,s:1.02,z:1.35,g:'hero',arm:15,stun:1,hero:1,col:'#a77cff',tag:'BOSS · étourdit'},
 /* ---- nés d'une division (cat x, jamais envoyés) ---- */
 {n:'Petit limon',cat:'x',t:1,c:20,hp:35,s:1.6,z:.6,g:'slime',col:'#b5e04a'},
 {n:'Petite boue',cat:'x',t:2,c:60,hp:110,s:1.4,z:.8,g:'mudgolem',col:'#6b4a2a'},
 {n:'Tête d’hydre',cat:'x',t:3,c:200,hp:380,s:1.3,z:.95,g:'hydra',col:'#2f7a6a'}];
/* 2.14 : tous les coûts sont des dizaines, et le revenu des monstres au sol est arrondi à l'inférieur : il ne dépasse jamais la courbe
   (10 or → 1, 100 → 11, 1000 → 120), donc aucun monstre bon marché ne rapporte proportionnellement plus qu'un plus cher (fin de la faille du Rat : 15 or pour +2). */
const revenu=T=>T.cat=='n'?Math.floor(T.c/10*(1+.1*Math.log10(T.c/10))+1e-9):Math.round(T.c*.065);
for(const T of CR){T.i=revenu(T);if(T.split)T.kid=CR.findIndex(U=>U.n==T.split)}
/* paliers (2.13) : prix d'ouverture des paliers 1, 2 et 3 ; accéléré : vitesse × (1 + ACC × secondes de vie), au plus × ACC_MAX */
const PAL_C=[0,300,1500],ACC=.1,ACC_MAX=2;
const byCat=c=>CR.map((T,k)=>k).filter(k=>CR[k].cat==c).sort((a,b)=>CR[a].c-CR[b].c),NORM=byCat('n'),FLY=byCat('f'),idx=f=>CR.findIndex(T=>T[f]),
 /* listes par capacité (tous paliers, par prix croissant) pour l'IA ; AURA, SPEC… restent le monstre du palier 1 */
 byF=f=>CR.map((T,k)=>k).filter(k=>CR[k][f]&&!CR[k].hero&&CR[k].cat!='x').sort((a,b)=>CR[a].c-CR[b].c),
 AURAS=byF('aura'),SPECS=byF('inv'),HEALS=byF('heal'),SPLITS=byF('split'),ACCS=byF('acc'),ARMS=byF('arm'),MIS=byF('mi'),STUNS=byF('stun'),BOSS=CR.map((T,k)=>k).filter(k=>CR[k].hero),
 AURA=idx('aura'),SPEC=idx('inv'),HEAL=idx('heal'),SPLIT=idx('split'),TURT=idx('arm'),BRK=idx('mi'),SAP=idx('stun'),KID=CR.findIndex(T=>T.cat=='x'),AURA_R=1.7;
const DIFF=[{n:'Normal',b:1,g:0},{n:'Difficile',b:1.25,g:30},{n:'Brutal',b:1.5,g:60}];
/* 2.30 : GRACE = phase « Construis » du début de partie : personne (humain ou IA) ne peut envoyer de monstres pendant ces 30 s */
const HPK=.55,GRACE=30,GROUP=4,
/* temps de construction : 1 s pour BUILD_OR pièces d'or dépensées (achat ou amélioration), entre BUILD_MIN et BUILD_MAX secondes,
   multiplié pour les humains par BUILD_DIFF selon la difficulté (les IA gardent ×1, comme pour le revenu) */
 BUILD_OR=50,BUILD_MIN=.5,BUILD_MAX=8,BUILD_DIFF=[1,1.25,1.5],buildT=(c,m=1)=>Math.min(BUILD_MAX,Math.max(BUILD_MIN,c/BUILD_OR))*m,flyH=k=>CR[k].fly?CR[k].z*.35:0;
/* vitesse d'un monstre ralenti : le froid et les racines s'additionnent */
const ralentir=c=>{c.sl=Math.max(c.gt||0,c.rt||0,c.im||0,c.hx||0);c.sf=c.im>0?0:Math.max(SF_MIN,1-(c.gt>0?c.gp:0)-(c.rt>0?c.rp:0))*(c.hx>0?.6:1)};
/* 2.39 : un volant abattu (filet) compte comme au sol ; cible(T, c) : la tour T peut-elle toucher le monstre c (sol, air, anti-magie) */
const vole=c=>CR[c.k].fly&&!(c.ab>0),cible=(T,c)=>!(T.gr&&vole(c))&&!(T.ao&&!CR[c.k].fly)&&!(T.mag&&CR[c.k].mi);
/* durées des états des races (décomptées à chaque pas) ; etats(c) : les états d'un monstre en bits, pour l'affichage et l'instantané du serveur */
const ETATS_T=['mk','ma','im','imI','hx','hxI','ab','tw','pt','sgT','bsT','bu','pe','cx'],
 etats=c=>(c.sl>0?1:0)|(c.h?2:0)|(c.hl?4:0)|(c.hid?8:0)|(c.pz>0?16:0)|(c.mk>0?32:0)|(c.ma>0?64:0)|(c.im>0?128:0)|(c.tw>0?256:0)|(c.bs>0?512:0)|(c.bu>0?1024:0)|(c.pe>0?2048:0)|(c.hx>0?4096:0)|(c.ab>0?8192:0)|(c.sgT>0?16384:0),
 SERVITEUR={n:'Mort relevé',d:0},SERVITEUR_PESTE={n:'Mort relevé',d:0,pe:4};
/* 2.39 : xd, xr = bonus de la tour (Cohésion, auras, Croissance, Chauffe, Rage) ; les Nains (Forge) paient leurs améliorations FORGE × le prix */
const dmg=t=>TW[t.k].d*2**(t.lv-1)*(t.xd||1),rng=t=>TW[t.k].r*(1+.05*(t.lv-1))*(t.xr||1),upCost=t=>Math.round(TW[t.k].c*1.5*2**(t.lv-1)*(TW[t.k].faction==3?FORGE:1)/5)*5,topY=t=>.28+.045*(t.lv-1);
/* 2.38 : quêtes bonus. Une à la fois, tirées au hasard sans remise : la première à QU_T0 s, puis la suivante QU_PAUSE à QU_PAUSE + 60 s après la fin de la précédente.
   f = 'course' : le premier qui atteint la cible gagne (au plus dur s, sinon personne) ; f = 'photo' : au bout de dur s, le meilleur score gagne (sens -1 : le plus petit).
   sc(b) : score du terrain b ; sans abs, il se compte depuis le début de la quête (écart avec le score de départ) ; cible(G) : cible d'une course, calculée au lancement
   pour que personne ne l'ait déjà atteinte ; ok(G) : la quête peut-elle être tirée maintenant ; u : unité affichée. Récompense : quOr (or, selon le revenu moyen).
   Chaque IA décide au lancement si elle joue la quête (QU_JOUE selon la difficulté) ; les quêtes « naturelles » n'ont pas besoin d'elle. */
const QU_T0=90,QU_PAUSE=180,QU_JOUE=[.5,.75,1],QU_PLACE=20,
 quVivants=G=>G.B.filter(b=>!b.dead),
 quOr=G=>{const a=quVivants(G);return Math.max(100,Math.round(8*a.reduce((s,b)=>s+b.inc,0)/Math.max(1,a.length)/10)*10)},
 givres=b=>b.t.filter(t=>TW[t.k].ctl).length,
 /* 2.39 : or versé en plus du revenu par les tours d'économie (Comptoir marchand d'Aubeval), toutes les 10 s */
 eco=b=>b.t.reduce((s,t)=>s+(TW[t.k].eco&&!(t.b>0)?TW[t.k].eco*t.lv:0),0),
 lvMax=b=>b.t.reduce((m,t)=>Math.max(m,t.lv),0),
 ciblesGonflette=G=>Math.max(3,1+Math.max(0,...quVivants(G).map(lvMax)));
/* cases où une tour peut encore être posée sans fermer le chemin (au plus n : on s'arrête dès qu'on en a trouvé assez) */
function posables(b,n){const w=new Uint8Array(C*R);for(let y=0;y<R;y++)for(let x=0;x<C;x++)w[y*C+x]=b.g[y][x];let k=0;
 for(let i=0;i<C*R&&k<n;i++){if(w[i]||i==SP[1]*C+SP[0]||i==EX[1]*C+EX[0])continue;w[i]=1;if(plen(w)>=0)k++;w[i]=0}return k}
const QUETES=[
 {id:'grosse',titre:'Qui a la plus grosse ?',txt:'Le plus long labyrinthe dans 75 s',f:'photo',dur:75,abs:1,u:' cases',sc:b=>Math.round(b.d[SP[1]][SP[0]])},
 {id:'clicker',titre:'Clicker fou',txt:'Le premier qui pose {N} tours',f:'course',dur:90,u:' tours',sc:b=>b.st.pose,cible:()=>10,
  /* pas en fin de partie : chacun doit encore avoir de la place pour construire */
  ok:G=>quVivants(G).every(b=>posables(b,QU_PLACE)>=QU_PLACE)},
 {id:'picsou',titre:'Picsou',txt:'Le plus d’or en banque dans 60 s',f:'photo',dur:60,abs:1,u:' or',sc:b=>Math.floor(b.gold)},
 {id:'facteur',titre:'Le facteur sonne toujours 4 fois',txt:'Le premier qui fait passer {N} de ses monstres chez un adversaire',f:'course',dur:120,u:' passés',sc:b=>b.st.passe,cible:()=>4},
 {id:'gonflette',titre:'Gonflette',txt:'Le premier qui monte une tour au niveau {N}',f:'course',dur:120,abs:1,u:'',pre:'niveau ',
  sc:b=>b.t.reduce((m,t)=>t.b>0?m:Math.max(m,t.lv),0),cible:ciblesGonflette,ok:G=>ciblesGonflette(G)<=5},
 {id:'frozen',titre:'Frozen',txt:'Le premier qui a {N} tours de contrôle',f:'course',dur:120,abs:1,u:' contrôle',sc:givres,
  cible:G=>Math.max(0,...quVivants(G).map(givres))+(G.time<300?2:G.time<600?3:4)},
 {id:'cadeau',titre:'Le gros cadeau',txt:'Le premier qui envoie un boss',f:'course',dur:150,u:' boss',sc:b=>b.st.boss,cible:()=>1,ok:G=>G.time>=180},
 {id:'pigeons',titre:'Pigeons voyageurs',txt:'Le plus d’or envoyé en volants dans 60 s',f:'photo',dur:60,u:' or',sc:b=>b.st.vol},
 {id:'bling',titre:'Bling-bling',txt:'La tour la plus chère dans 60 s',f:'photo',dur:60,abs:1,u:' or',sc:b=>b.t.reduce((m,t)=>Math.max(m,t.inv),0)},
 {id:'mamie',titre:'Mamie Gâteau',txt:'Le plus petit revenu dans 60 s touche le gâteau',f:'photo',dur:60,abs:1,sens:-1,u:'',pre:'+',sc:b=>b.inc}];

/* ---------- simulation ---------- */
/* grille de voisinage (2.5.2, performances) : chaque élément d'une liste est rangé dans sa case, pour ne tester que les voisins d'un point
   au lieu de toute la liste. near() rend les indices dans l'ordre de la liste : les résultats sont identiques à un parcours complet. */
const gcl=(v,m)=>Math.min(m-1,Math.max(0,v|0));
class Grid{constructor(){this.b=Array.from({length:C*R},()=>[]);this.u=[];this.o=[]}
 fill(l){for(const i of this.u)this.b[i].length=0;this.u.length=0;for(let n=0;n<l.length;n++){const i=gcl(l[n].y,R)*C+gcl(l[n].x,C);if(!this.b[i].length)this.u.push(i);this.b[i].push(n)}return this}
 /* éléments dont la case touche le carré de demi-côté r autour de (x, y), dans l'ordre de la liste */
 near(x,y,r){const o=this.o,x0=gcl(Math.floor(x-r),C),x1=gcl(Math.floor(x+r),C),y0=gcl(Math.floor(y-r),R),y1=gcl(Math.floor(y+r),R);o.length=0;
  for(let b=y0;b<=y1;b++)for(let a=x0;a<=x1;a++){const L=this.b[b*C+a];for(let k=0;k<L.length;k++)o.push(L[k])}if(o.length>1)o.sort((p,q)=>p-q);return o}}
const GRID_MIN=12;
/* ---------- chemin au sol en diagonale (depuis la 2.25) ----------
   Distances à la sortie sur 8 directions (diagonale = √2), sans couper le coin d'une tour : une diagonale exige que les deux cases voisines soient libres.
   Le monstre suit ensuite cette chaîne de cases en ligne droite, aussi loin qu'il voit (vue) : il peut donc prendre n'importe quel angle. */
const DIR8=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]],S2=Math.SQRT2,MR=.3,VUE_MAX=16,ESP=.75,ESP_V=1.5;
const cel=(v,n)=>Math.max(0,Math.min(n-1,Math.floor(v+.5)));
/* pas possible de (x, y) dans la direction (dx, dy) */
function libre8(g,x,y,dx,dy){const a=x+dx,b=y+dy;return a>=0&&b>=0&&a<C&&b<R&&!g[b][a]&&(!(dx&&dy)||(!g[y][a]&&!g[b][x]))}
/* case suivante vers la sortie depuis (x, y), ou null */
function pas8(b,x,y){const d0=b.d[y][x];if(!(d0>0&&d0<INF))return null;let best=null,bv=d0+1e-6;
 for(const[dx,dy]of DIR8){if(!libre8(b.g,x,y,dx,dy)||b.d[y+dy][x+dx]>=d0)continue;const v=b.d[y+dy][x+dx]+(dx&&dy?S2:1);if(v<bv){bv=v;best=[x+dx,y+dy]}}return best}
/* suite de cases de (x, y) jusqu'à la sortie (au plus n pas) */
function chaine(b,x,y,n){const out=[[x,y]];for(let p;n-->0&&(p=pas8(b,x,y));){x=p[0];y=p[1];out.push(p)}return out}
/* le segment (x0, y0) → (x1, y1) reste-t-il à MR case des tours et dans le terrain ? (positions en cases, centre de case = entier) */
function vue(g,x0,y0,x1,y1){const e=.5+MR-1e-6,dx=x1-x0,dy=y1-y0,
  a0=Math.max(0,Math.floor(Math.min(x0,x1)-e)),a1=Math.min(C-1,Math.ceil(Math.max(x0,x1)+e)),b0=Math.max(0,Math.floor(Math.min(y0,y1)-e)),b1=Math.min(R-1,Math.ceil(Math.max(y0,y1)+e));
 /* chaque tour, agrandie de MR, est un carré : le segment le traverse-t-il ? (méthode des intervalles) */
 const coupe=(p,d,lo,hi,t)=>{if(Math.abs(d)<1e-12)return p>lo&&p<hi?t:null;let u=(lo-p)/d,v=(hi-p)/d;if(u>v)[u,v]=[v,u];return [Math.max(t[0],u),Math.min(t[1],v)]};
 for(let b=b0;b<=b1;b++)for(let a=a0;a<=a1;a++){if(!g[b][a])continue;let t=coupe(x0,dx,a-e,a+e,[0,1]);if(t)t=coupe(y0,dy,b-e,b+e,t);if(t&&t[0]<t[1])return false}return true}
/* chemin affiché : un monstre fantôme part de l'apparition avec les mêmes règles (cible revue tous les 0,4 case) ; on garde ses points de virage.
   Mis en cache tant que les distances b.d ne changent pas. */
function chemin(b){if(b._chD===b.d)return b._ch;const c={x:SP[0],y:SP[1],tx:SP[0],ty:SP[1]},out=[[SP[0],SP[1]]];
 for(let n=0;n<3000;n++){const dd=Math.hypot(c.tx-c.x,c.ty-c.y),ox=c.tx,oy=c.ty;
  if(dd<1e-4){if(ox==EX[0]&&oy==EX[1])break;b.viser(c);if(c.tx==ox&&c.ty==oy)break}else b.viser(c,1);
  if((c.tx!=ox||c.ty!=oy)&&n)out.push([c.x,c.y]);const d2=Math.hypot(c.tx-c.x,c.ty-c.y),m=Math.min(.4,d2);if(d2>0){c.x+=(c.tx-c.x)/d2*m;c.y+=(c.ty-c.y)/d2*m}}
 out.push([c.x,c.y]);b._chD=b.d;return b._ch=out}
/* une tour en (x, y) gênerait-elle un monstre au sol ? (trop près de lui, ou sa case ne mène plus à la sortie avec les distances nd) */
function genant(b,x,y,nd){return b.cr.some(c=>!CR[c.k].fly&&((Math.abs(c.x-x)<.9&&Math.abs(c.y-y)<.9)||nd[cel(c.y,R)][cel(c.x,C)]>=INF))}
class Board{
 constructor(i,name,col,ai,classId=0){this.i=i;this.name=name;this.col=col;this.ai=ai;this.classId=classId;this.dead=0;this.aiT=1+i*.2;this.ev=[];this.G=null;
  this.g=Array.from({length:R},()=>Array(C).fill(0));this.t=[];this.cr=[];this.pr=[];this.fx=[];this.q=[];this.gold=200;this.inc=10;this.lives=40;this.hurt=0;this.pen=0;this.dp=120;this.ap=80;this.lastG=200;this.flyIn=0;this.hpIn=0;this.specSeen=0;this.tier=1;this.mz=null;this.d=this.dist();
  /* 2.23 : statistiques de fin de partie (sans effet sur le jeu) : tours posées, envois (groupes et or), monstres tués, revenu à chaque versement, moment de l'élimination ;
     2.38 (quêtes) : monstres de ce joueur passés chez un adversaire, boss envoyés, or envoyé en volants, quêtes gagnées et leur or */
  this.st={pose:0,env:0,envOr:0,tue:0,rev:[],mort:-1,passe:0,boss:0,vol:0,qu:0,quOr:0}}
 /* distances à la sortie (Dijkstra sur 8 directions, diagonale √2, sans couper les coins) */
 dist(){const d=Array.from({length:R},()=>Array(C).fill(INF)),g=this.g,f=new Uint8Array(C*R);d[EX[1]][EX[0]]=0;
  for(;;){let x=-1,y=0,v=INF;for(let j=0;j<R;j++)for(let i=0;i<C;i++)if(!f[j*C+i]&&d[j][i]<v){v=d[j][i];x=i;y=j}if(x<0)break;f[y*C+x]=1;
   for(const[dx,dy]of DIR8){if(!libre8(g,x,y,dx,dy))continue;const w=v+(dx&&dy?S2:1);if(w<d[y+dy][x+dx])d[y+dy][x+dx]=w}}return d}
 /* nouvelle cible d'un monstre au sol : la case la plus lointaine de sa chaîne qu'il peut rejoindre en ligne droite */
 viser(c,garder){const x=cel(c.x,C),y=cel(c.y,R),ch=chaine(this,x,y,VUE_MAX);let j=0;
  for(let k=1;k<ch.length&&vue(this.g,c.x,c.y,ch[k][0],ch[k][1]);k++)j=k;
  if(garder&&!j)return;const[a,b]=ch[j];if(Math.abs(a-c.x)>1e-3)c.f=a>c.x?1:-1;c.tx=a;c.ty=b}
 /* après une pose ou une vente, chaque monstre au sol recalcule sa cible */
 revoir(){for(const c of this.cr)if(!CR[c.k].fly)this.viser(c)}
 place(x,y,k){const T=TW[k];
  if(Math.floor(k/10)!==this.classId)return false;
  /* 2.39 : une seule tour ultime par terrain */
  if(T.u&&this.t.some(t=>TW[t.k].u))return false;
  if(x<0||y<0||x>=C||y>=R||this.gold<T.c||this.g[y][x]||(x==SP[0]&&y==SP[1])||(x==EX[0]&&y==EX[1]))return false;
  this.g[y][x]=1;const nd=this.dist();
  if(nd[SP[1]][SP[0]]>=INF||genant(this,x,y,nd)){this.g[y][x]=0;return false}
  this.d=nd;this.revoir();this.gold-=T.c;this.st.pose++;const bt=buildT(T.c,this.bm());this.t.push({x,y,k,cd:0,a:.7,lv:1,inv:T.c,sw:0,b:bt,bt});
  this.fx.push({type:'range',x:x+.5,y:y+.5,r:T.r,t:.6,d:.6,col:T.col});this.ev.push('build');return true}
 /* multiplicateur de temps de construction : selon la difficulté pour un humain, ×1 pour une IA */
 bm(){return this.G&&!this.ai?BUILD_DIFF[this.G.LV]||1:1}
 sell(x,y){const i=this.t.findIndex(t=>t.x==x&&t.y==y);if(i<0)return false;const b=Math.floor(this.t[i].inv*.7);this.gold+=b;this.t.splice(i,1);this.g[y][x]=0;this.d=this.dist();this.revoir();
  this.fx.push({type:'text',x:x+.5,y:y+.4,txt:'+'+b,col:'#ffd95e',t:.7,d:.7});this.ev.push('sell');return true}
 upgrade(t){const c=upCost(t);if(t.lv>=5||t.b>0||this.gold<c)return false;this.gold-=c;t.inv+=c;t.lv++;t.b=t.bt=buildT(c,this.bm());
  this.fx.push({type:'text',x:t.x+.5,y:t.y,txt:'Niveau '+t.lv,col:'#ffd95e',t:.9,d:.9},{type:'range',x:t.x+.5,y:t.y+.5,r:rng(t),t:.6,d:.6,col:TW[t.k].col});this.ev.push('up');return true}
 /* o : terrain qui envoie (2.38 : chaque monstre retient son envoyeur, pour la quête du facteur) */
 send(k,m,o=-1){for(let i=0;i<GROUP;i++)this.q.push({k,m,o,t:i*.38+Math.random()*.25})}
 /* dégâts d'un coup (2.39 : états et combos des races). L'anti-magie ignore les tours magiques ; l'armure retire un montant fixe (moins si Brisé, rien si Maléfice),
    mais chaque coup garde au moins 20 %. t : tour qui frappe (Fureur, Âmes). Renvoie les dégâts infligés. */
 hit(c,d,T,lv,t){
  if(T.mag&&CR[c.k].mi)return 0;
  const F=vole(c),i=Math.min(4,Math.max(0,(lv||1)-1)),du=1+.1*i,hero=CR[c.k].hero;
  d*=F?(T.air||1):(T.sol||1);
  if(T.spe&&CR[c.k].cat=='s')d*=T.spe;
  if(T.ex&&hero&&c.hp<c.max*.25)d*=1.5;
  if(T.xim&&c.im>0)d*=T.xim;
  if(T.chu&&c.ab>0){d*=T.chu;this.combo(c,'CHUTE !','#ffd95e')}
  if(T.bre&&(c.bs||0)>=BRISE_MAX){d*=T.bre;this.combo(c,'BRÈCHE !','#ff9a3d')}
  if(T.jug&&c.mk>0){d*=T.jug;c.mk=0;this.combo(c,'JUGEMENT !','#ffe9a0')}
  d*=1+Math.min(AMP_MAX,(c.mk>0?.15:0)+(c.ma>0?.2:0));
  if(c.arm&&!(T.pierce>=1)){const armor=(c.hx>0?0:c.arm)*(1-(T.pierce||0))*(1-BRISE*(c.bs||0));d=Math.max(d*.2,d-armor)}
  c.hp-=d;if(t)c.lt=t;
  if(T.ex&&!hero&&c.hp>0&&c.hp<c.max*T.ex){c.hp=0;this.combo(c,'FAUCHÉ !','#d9c2ff')}
  /* ralentissement selon le niveau de la tour : froid (GIVRE_LV) ou racines (RACINES_LV) ; dans une même famille, le plus fort et le plus long l'emportent */
  if(T.sl){if(T.fsp){const gp=GIVRE_LV.p[i]+(T.gb||0);c.gp=c.gt>0?Math.max(c.gp,gp):gp;c.gt=Math.max(c.gt||0,GIVRE_LV.d[i]);if(T.tw)c.tw=Math.max(c.tw||0,GIVRE_LV.d[i]+.5)}
   else{c.rp=c.rt>0?Math.max(c.rp,RACINES_LV.p[i]):RACINES_LV.p[i];c.rt=Math.max(c.rt||0,RACINES_LV.d[i])}}
  /* immobilisation (filets, racines, chocs, squelettes) : rendement décroissant (immunité IM_IMMU × la durée), moitié pour un boss, deux fois plus courte… jamais */
  if(T.im&&!(c.imI>0)){const D=T.im*du*(hero?.5:1);c.im=Math.max(c.im||0,D);c.imI=D*(1+IM_IMMU)}
  if(T.ab&&CR[c.k].fly)c.ab=Math.max(c.ab||0,T.ab*du);
  if(T.mk)c.mk=Math.max(c.mk||0,T.mk*du);
  if(T.ma)c.ma=Math.max(c.ma||0,T.ma*du);
  if(T.hx&&!hero&&!(c.hxI>0)){c.hx=T.hx*du;c.hxI=c.hx*(1+IM_IMMU)+1}
  if(T.pz){c.pz=Math.min(DOSE_MAX,(c.pz||0)+T.pz+(t&&t.bz||0));c.pd=Math.max(c.pt>0?c.pd||0:0,T.pv*(1+i));c.pt=4}
  if(T.sg){c.sg=Math.max(c.sgT>0?c.sg:0,T.sg*(1+.25*i));c.sgT=3}
  if(T.fus&&c.bu>0&&(c.bs||0)<BRISE_MAX){c.bs=Math.min(BRISE_MAX,(c.bs||0)+T.fus);c.bsT=4;this.combo(c,'FUSION !','#ff7a3d')}
  if(T.br){c.bs=Math.min(BRISE_MAX,(c.bs||0)+T.br);c.bsT=4}
  if(T.bu){c.bu=2;c.bud=Math.max(c.bud||0,T.bu*2**i)}
  if(T.pe){c.pe=3;c.ped=Math.max(c.ped||0,T.pe*2**i)}
  if(T.flo&&c.pz>0&&c.pt>0){const v=c.pz*c.pd*c.pt*T.flo;c.hp-=v;c.pz=0;this.combo(c,'FLORAISON !','#b6f27a')}
  ralentir(c);return d}
 /* texte d'un combo au-dessus du monstre (au plus un par demi-seconde et par monstre, et un même combo au plus toutes les 0,4 s sur le terrain) */
 combo(c,txt,col){const tm=this.G?this.G.time:0,cn=this.cxN||(this.cxN={});if((c.cx||0)>0||(cn[txt]||0)>tm)return;c.cx=.5;cn[txt]=tm+.4;this.fx.push({type:'text',x:c.x+.5,y:c.y-.1-flyH(c.k),txt,col,t:.9,d:.9,combo:1});this.ev.push('combo')}
 impact(p){const T=TW[p.k],tg=p.tg,rad=T.fsp?GIVRE_LV.r[Math.min(4,Math.max(0,(p.lv||1)-1))]:T.sp;
  if(!tg.dead&&!tg.leak)this.hit(tg,p.d,T,p.lv,p.t);
  if(rad){const cg=this.cgOk&&this.cr.length>GRID_MIN?this.cg.near(p.tx-.5,p.ty-.5,rad+.5).map(n=>this.cr[n]):this.cr;for(const c of cg){if(c===tg||c.hid||!cible(T,c)||Math.hypot(c.x+.5-p.tx,c.y+.5-flyH(c.k)-p.ty)>=rad)continue;this.hit(c,p.d*.6,T,p.lv,p.t)}
   this.fx.push({type:'boom',x:p.tx,y:p.ty,r:rad,t:.3,d:.3,col:T.fsp?'#8fdcff':T.pz?'#9be36a':T.pe?'#a5c45a':T.ma?'#b98cff':T.ao?'#ffd27a':'#ffb347'});if(T.sp)this.ev.push('boom')}
  else this.fx.push({type:'ring',x:p.tx,y:p.ty,r:T.skin==3?.45:.26,t:.2,d:.2,col:T.pz?'#9be36a':T.im?'#e8e2c8':T.skin==0?'#ffffff':'#e39bff'})}
 /* espacement (depuis la 2.25) : deux monstres à moins de ESP case (au sol entre eux, volants entre eux) se poussent SUR LE CÔTÉ seulement,
    perpendiculairement à leur marche, au plus ESP_V case/s. Personne n'est freiné ni repoussé en arrière : ils s'étalent sans jamais faire bouchon.
    Un monstre qui en suit un autre dans la même file part d'un côté choisi selon son numéro. Au sol, le pas de côté garde MR case des tours. */
 ecarter(dt){const L=this.cr,n=L.length;if(n<2||!(dt>0))return;const G=n>GRID_MIN&&(this.sg||(this.sg=new Grid())).fill(L),mv=[];
  for(let i=0;i<n;i++){const c=L[i],F=!!CR[c.k].fly,hx=(F?EX[0]:c.tx)-c.x,hy=(F?EX[1]:c.ty)-c.y,h=Math.hypot(hx,hy);if(h<.05)continue;
   const px=-hy/h,py=hx/h;let s=0;
   for(const j of G?G.near(c.x,c.y,ESP):L.keys()){const o=L[j];if(o===c||!!CR[o.k].fly!==F)continue;const dx=c.x-o.x,dy=c.y-o.y,d=Math.hypot(dx,dy);if(d>=ESP)continue;
    const w=(ESP-d)/ESP,lat=d>1e-3?(dx*px+dy*py)/d:0;s+=(lat+(Math.abs(lat)<.5?(c.id>o.id?.5:-.5):0))*w}
   if(Math.abs(s)>1e-3)mv.push([c,F,px,py,Math.max(-1,Math.min(1,s))*ESP_V*dt])}
  for(const[c,F,px,py,m]of mv){const nx=Math.max(0,Math.min(C-1,c.x+px*m)),ny=Math.max(0,Math.min(R-1,c.y+py*m));
   if(F||(vue(this.g,c.x,c.y,nx,ny)&&vue(this.g,nx,ny,c.tx,c.ty))){c.x=nx;c.y=ny}}}
 /* 2.39 : bonus des tours (Cohésion, auras, Croissance, Fureur, Chauffe), recalculés tous les 0,25 s. Voisine = une des 8 cases autour. */
 bonus(){const L=this.t,act=L.filter(t=>!(t.b>0)),cg=this.t.some(t=>!(t.b>0)&&TW[t.k].cgG)?3:1,am=this.am||0;
  for(const t of L){const T=TW[t.k];let coh=0,cad=0,dm=0,rg=0,dose=0,nf=0,crg=1,fu=1,cw=1;
   for(const o of act){if(o===t||Math.abs(o.x-t.x)>1||Math.abs(o.y-t.y)>1)continue;const O=TW[o.k],a=O.au;
    if(O.faction==0&&T.faction==0)coh++;if(!a)continue;const lv=1+.2*(o.lv-1);
    if(a.cad)cad+=a.cad*lv;if(a.dm)dm+=a.dm*lv;if(a.rg)rg+=a.rg*lv;if(a.dose)dose+=a.dose;if(a.nf)nf=1;if(a.cg)crg=Math.max(crg,a.cg);if(a.fu)fu=Math.max(fu,a.fu);if(a.coh)cw=Math.max(cw,a.coh);
    if(a.am)cad+=Math.min(.12,.02*Math.floor(am/5))*lv}
   const cr=T.faction==2?Math.min(CROIT_MAX,CROIT*Math.floor((t.age||0)/10)):0;
   t.co=T.faction==0?Math.min(4*cw,coh*cw)*COH:0;t.bz=dose;t.nf=nf;t.fm=fu;t.cgr=crg*cg;
   t.xc=(1+cad)*(1+FUREUR*(t.fu||0));t.xd=(1+t.co)*(1+dm)*(1+cr)*(1+.5*Math.min(1,t.ht||0))*(t.rg>0?1.3:1);t.xr=(1+rg)*(1+cr)}}
 update(dt){
  this.hurt=Math.max(0,this.hurt-dt);
  for(const s of this.q){s.t-=dt;if(s.t<=0){const hp=CR[s.k].hp*s.m*HPK;this.hpIn+=hp;if(CR[s.k].fly)this.flyIn+=hp;if(CR[s.k].inv)this.specSeen=1;this.cr.push({id:++UID,k:s.k,o:s.o,x:SP[0],y:SP[1],tx:SP[0],ty:SP[1],hp,max:hp,sl:0,sf:1,gp:0,gt:0,rp:0,rt:0,f:1,ph:Math.random()*6,ox:(Math.random()-.5)*.3,oy:(Math.random()-.5)*.22,arm:(CR[s.k].arm||0)*s.m,cs:2})}}
  this.q=this.q.filter(s=>s.t>0);
  this.bfT=(this.bfT||0)-dt;if(this.bfT<=0){this.bfT=.25;this.bonus()}
  const au=this.cr.filter(c=>CR[c.k].aura),mg=this.t.filter(t=>TW[t.k].mg&&!(t.b>0)),hl=this.cr.filter(c=>CR[c.k].heal),ph=mg.filter(t=>TW[t.k].rvb);
  /* hâte et soin : avec beaucoup de Chamans ou de Prêtresses, on ne regarde que ceux des cases voisines. Ils bougent pendant la boucle (au plus 3,4 cases/s × dt),
     d'où la marge ajoutée au rayon ; la distance exacte est ensuite vérifiée comme avant. */
  const ar=AURA_R+3.4*dt+.01,auG=au.length>GRID_MIN&&(this.ag||(this.ag=new Grid())).fill(au),hlG=hl.length>GRID_MIN&&(this.hg||(this.hg=new Grid())).fill(hl);
  for(const c of this.cr){const T=CR[c.k];c.gt=Math.max(0,(c.gt||0)-dt);c.rt=Math.max(0,(c.rt||0)-dt);
   /* 2.39 : états des races (durées) et dégâts dans la durée, qui ignorent l'armure (poison deux fois plus rapide sur un immobilisé : Terreau ; peste deux fois plus forte sur un Maudit : Épidémie) */
   for(const e of ETATS_T)if(c[e]>0)c[e]=Math.max(0,c[e]-dt);
   let dot=0;if(c.pz>0){if(c.pt>0)dot+=c.pz*c.pd*(c.im>0?2:1);else c.pz=0}if(c.sgT>0)dot+=c.sg*c.max;if(c.bu>0)dot+=c.bud;else c.bud=0;if(c.pe>0)dot+=c.ped*(c.ma>0?2:1);else c.ped=0;
   if(!(c.bsT>0))c.bs=0;if(dot)c.hp-=dot*dt;
   for(const t of ph)if(Math.hypot(c.x-t.x,c.y-t.y)<=rng(t)){c.bs=Math.max(c.bs||0,1);c.bsT=Math.max(c.bsT||0,.3)}
   ralentir(c);if(T.acc)c.age=(c.age||0)+dt;c.mark=Math.max(0,(c.mark||0)-dt);c.h=!T.aura&&(auG?auG.near(c.x,c.y,ar).some(n=>Math.hypot(au[n].x-c.x,au[n].y-c.y)<AURA_R):au.some(a=>Math.hypot(a.x-c.x,a.y-c.y)<AURA_R));
   c.hid=T.inv&&!mg.some(m=>Math.hypot(c.x-m.x,c.y-m.y)<=rng(m));
   c.hl=c.hp<c.max&&(hlG?hlG.near(c.x,c.y,ar).some(n=>hl[n]!==c&&Math.hypot(hl[n].x-c.x,hl[n].y-c.y)<AURA_R):hl.some(a=>a!==c&&Math.hypot(a.x-c.x,a.y-c.y)<AURA_R));if(c.hl)c.hp=Math.min(c.max,c.hp+c.max*.05*dt);
   if(T.stun){c.cs-=dt;if(c.cs<=0){let bt=null,bd=2.3;for(const t of this.t){const d=Math.hypot(t.x-c.x,t.y-c.y);if(d<bd&&!(t.stun>0)&&!(t.b>0)){bd=d;bt=t}}
    /* 2.39 : les tours naines (Forge) ne restent étourdies que moitié moins longtemps */
    if(bt){bt.stun=TW[bt.k].faction==3?1:2;c.cs=3.5;this.fx.push({type:'zap',x:c.x+.5,y:c.y+.3,x2:bt.x+.5,y2:bt.y+.5-topY(bt),t:.3,d:.3});this.ev.push('zap')}else c.cs=.3}}
   let sp=T.s*(c.sl>0?c.sf:1)*(c.h?1.4:1)*(T.acc?Math.min(ACC_MAX,1+ACC*c.age):1)*dt;
   if(T.fly){const dx=EX[0]-c.x,dy=EX[1]-c.y,dd=Math.hypot(dx,dy);if(dd<=sp)c.leak=1;else{c.x+=dx/dd*sp;c.y+=dy/dd*sp}continue}
   /* toutes les 0,25 s, le monstre regarde s'il voit plus loin sur son chemin (il coupe ainsi au plus court après un virage) */
   c.rv=(c.rv||0)-dt;if(c.rv<=0){c.rv=.25;this.viser(c,1)}
   while(sp>0){const dx=c.tx-c.x,dy=c.ty-c.y,dd=Math.hypot(dx,dy);
    if(dd<1e-4){if(c.tx==EX[0]&&c.ty==EX[1]){c.leak=1;break}
     const ox=c.tx,oy=c.ty;this.viser(c);if(c.tx==ox&&c.ty==oy)break;continue}
    const m=Math.min(sp,dd);c.x+=dx/dd*m;c.y+=dy/dd*m;sp-=m}}
  this.ecarter(dt);
  this.pen*=Math.pow(.955,dt);const tot=this.d[SP[1]][SP[0]]||1;
  for(const c of this.cr){const pr=CR[c.k].fly?1-Math.hypot(EX[0]-c.x,EX[1]-c.y)/12:1-(this.d[c.ty][c.tx]+Math.hypot(c.tx-c.x,c.ty-c.y))/tot;if(pr>this.pen)this.pen=pr}
  /* tours et explosions : seuls les monstres des cases à portée sont examinés (grille remplie une fois par pas, les monstres ne bougent plus ensuite) */
  const cr=this.cr,useG=cr.length>GRID_MIN;if(useG)(this.cg||(this.cg=new Grid())).fill(cr);this.cgOk=useG;const voisins=(x,y,r)=>useG?this.cg.near(x,y,r).map(n=>cr[n]):cr;
  const ok=(T,c,t,r)=>!c.hid&&cible(T,c)&&Math.hypot(c.x-t.x,c.y-t.y)<=r&&!(T.rmin&&Math.hypot(c.x-t.x,c.y-t.y)<T.rmin);
  for(const t of this.t){if(t.b>0){t.b-=dt;if(t.b<=0){t.b=0;t.cd=0;this.fx.push({type:'range',x:t.x+.5,y:t.y+.5,r:rng(t),t:.6,d:.6,col:TW[t.k].col})}continue}
   const T=TW[t.k];
   /* 2.39 : Croissance (Lunebois), Fureur qui retombe, Rage, Chauffe qui refroidit, surchauffe */
   if(T.faction==2)t.age=(t.age||0)+dt*(t.cgr||1);
   if(t.fu>0){t.fuT=(t.fuT||0)-dt;if(t.fuT<=0){t.fu--;t.fuT=2}}if(t.rg>0)t.rg-=dt;t.lf=(t.lf||0)+dt;if(t.ht>0&&t.lf>1)t.ht=Math.max(0,t.ht-.5*dt);if(t.oh>0){t.oh-=dt;continue}
   if(t.stun>0){t.stun-=dt;continue}t.cd-=dt;if(t.sw>0)t.sw-=dt;if(t.cd>0)continue;const r=rng(t),dm=dmg(t),cdx=T.cd/(t.xc||1);
   if(T.no){if(T.col){if((this.am||0)>=T.col.am&&this.cr.some(c=>!CR[c.k].fly)){this.am-=T.col.am;this.invoquer(t.x,t.y,T.col.d*2**(t.lv-1),T.col.t,1);t.cd=T.cd;this.combo({x:t.x,y:t.y,k:0},'COLOSSE D’OS !','#e8e2c8')}else t.cd=1}else t.cd=1;continue}
   /* mines : une nouvelle mine sur une case du chemin à portée (au plus T.mn par tour) */
   if(T.mn){const mi=this.mi||(this.mi=[]);if(mi.filter(m=>m.t===t).length<T.mn){const P=trajet(this).filter(([a,b])=>Math.hypot(a-t.x,b-t.y)<=r&&!mi.some(m=>Math.hypot(m.x-a,m.y-b)<.8));
     if(P.length){const[a,b]=P[Math.floor(Math.random()*P.length)];mi.push({id:++UID,x:a,y:b,t,d:dm,lv:t.lv});t.cd=cdx}else t.cd=.5}else t.cd=.5;continue}
   /* impulsion : tout ce qui est à portée (pu = 0) ou pu cibles tirées au hasard */
   if(T.pu!==undefined){const L=voisins(t.x,t.y,r).filter(c=>ok(T,c,t,r));if(!L.length){t.cd=.2;continue}t.cd=cdx;
    const cib=T.pu?L.sort(()=>Math.random()-.5).slice(0,T.pu):L;for(const c of cib){this.hit(c,dm,T,t.lv,t);if(T.pu)this.fx.push({type:'zap',x:c.x+.5,y:c.y-1.9,x2:c.x+.5,y2:c.y+.5-flyH(c.k),t:.3,d:.3,col:'#bfe6ff',ciel:1})}
    if(!T.pu)this.fx.push({type:'boom',x:t.x+.5,y:t.y+.5,r,t:.4,d:.4,col:T.im&&T.faction==2?'#7ac46a':T.im?'#ffe2a8':'#9be36a'});this.ev.push(T.pu?'zap':T.s);continue}
   let tg=null,bd=INF;
   for(const c of voisins(t.x,t.y,r)){if(!ok(T,c,t,r))continue;const F=CR[c.k].fly;
    const rem=T.vise=='pv'?-c.hp:F?Math.hypot(EX[0]-c.x,EX[1]-c.y):this.d[c.ty][c.tx]+Math.hypot(c.tx-c.x,c.ty-c.y);if(rem<bd){bd=rem;tg=c}}
   if(!tg)continue;t.cd=cdx;t.a=Math.atan2(tg.y-t.y,tg.x-t.x);
   t.lf=0;if(T.ht){t.ht=(t.ht||0)+T.ht;if(t.ht>=1){if(t.nf)t.ht=.99;else{t.ht=0;t.oh=2;this.fx.push({type:'text',x:t.x+.5,y:t.y-.2,txt:'Surchauffe',col:'#ff8a5a',t:.8,d:.8})}}}
   if(T.me){const L=T.cl?voisins(t.x,t.y,r).filter(c=>ok(T,c,t,r)).sort((a,b)=>Math.hypot(a.x-t.x,a.y-t.y)-Math.hypot(b.x-t.x,b.y-t.y)).slice(0,T.cl):[tg];
    for(const c of L){this.hit(c,dm,T,t.lv,t);this.fx.push({type:'slash',x:c.x+.5,y:c.y+.5,a:t.a,t:.18,d:.18,col:T.os?'#e8e2c8':undefined})}t.sw=.2}
   else if(T.fl){for(const c of voisins(t.x,t.y,r)){if(c.hid||!cible(T,c))continue;const dx=c.x-t.x,dy=c.y-t.y,dd=Math.hypot(dx,dy);if(dd>r)continue;const da=Math.atan2(dy,dx)-t.a;if(dd<.6||Math.abs(Math.atan2(Math.sin(da),Math.cos(da)))<.5)this.hit(c,dm,T,t.lv,t)}
    const h=topY(t);for(let i=0;i<2;i++){const a=t.a+(Math.random()-.5)*.5,v=r/.35*(.75+Math.random()*.35);this.fx.push({type:'flame',x:t.x+.5,y:t.y+.5-h,vx:Math.cos(a)*v,vy:Math.sin(a)*v+h/.35,t:.35,d:.35})}}
   /* éclair en chaîne : chaque rebond perd 25 % ; deux fois plus de rebonds si la première cible est Trempée (Conduction) */
   else if(T.ch){let n=T.ch,cur=tg,d=dm;const vus=new Set([tg]);if(T.cond&&tg.tw>0){n*=T.cond;this.combo(tg,'CONDUCTION !','#9fe0ff')}
    this.fx.push({type:'zap',x:t.x+.5,y:t.y+.5-topY(t),x2:tg.x+.5,y2:tg.y+.5-flyH(tg.k),t:.25,d:.25,col:'#bfe6ff'});this.hit(tg,d,T,t.lv,t);
    for(let k=0;k<n;k++){let nx=null,nd=2.2;for(const c of voisins(cur.x,cur.y,2.2)){if(vus.has(c)||c.hid||!cible(T,c)||c.dead)continue;const q=Math.hypot(c.x-cur.x,c.y-cur.y);if(q<nd){nd=q;nx=c}}
     if(!nx)break;vus.add(nx);d*=.75;this.fx.push({type:'zap',x:cur.x+.5,y:cur.y+.5-flyH(cur.k),x2:nx.x+.5,y2:nx.y+.5-flyH(nx.k),t:.25,d:.25,col:'#bfe6ff'});this.hit(nx,d,T,t.lv,t);cur=nx}}
   /* tir en ligne : tout ce qui est à moins de 0,45 case du trait, jusqu'au bout de la portée */
   else if(T.ln){const ux=Math.cos(t.a),uy=Math.sin(t.a);for(const c of voisins(t.x,t.y,r)){if(c.hid||!cible(T,c))continue;const vx=c.x-t.x,vy=c.y-t.y,s=vx*ux+vy*uy;if(s<0||s>r)continue;if(Math.abs(vx*uy-vy*ux)<=.45)this.hit(c,dm,T,t.lv,t)}
    this.fx.push({type:'zap',x:t.x+.5,y:t.y+.5-topY(t),x2:t.x+.5+ux*r,y2:t.y+.5+uy*r,t:.3,d:.3,col:T.u?'#ffb36b':'#f4f0d0',ln:1})}
   /* rayon : +bm à chaque tir sur la même cible, jusqu'à ×bmx */
   else if(T.bm){t.rm=t.bt0===tg?Math.min(T.bmx,(t.rm||1)+T.bm):1;t.bt0=tg;this.hit(tg,dm*t.rm,T,t.lv,t);this.fx.push({type:'zap',x:t.x+.5,y:t.y+.5-topY(t),x2:tg.x+.5,y2:tg.y+.5-flyH(tg.k),t:.2,d:.2,col:'#ffe9a0',ln:1})}
   else this.pr.push({id:++UID,x:t.x+.5,y:t.y+.5-topY(t),tg,k:t.k,d:dm,lv:t.lv,t,tx:tg.x+.5,ty:tg.y+.5,tot:Math.hypot(tg.x-t.x,tg.y-t.y)||.1,a:t.a});
   this.ev.push(T.s)}
  for(const p of this.pr){const T=TW[p.k];if(!p.tg.dead&&!p.tg.leak){p.tx=p.tg.x+.5;p.ty=p.tg.y+.5-flyH(p.tg.k)}
   const dx=p.tx-p.x,dy=p.ty-p.y,dd=Math.hypot(dx,dy),m=T.ps*dt;
   if(dd<=m){p.hit=1;this.impact(p)}else{p.x+=dx/dd*m;p.y+=dy/dd*m;p.a=Math.atan2(dy,dx)}}
  this.pr=this.pr.filter(p=>!p.hit);
  /* 2.39 : mines (Hautroc) et morts relevés (Ossements) */
  if(this.mi&&this.mi.length){this.mi=this.mi.filter(m=>this.t.includes(m.t));for(const m of this.mi){const T=TW[m.t.k];if(!voisins(m.x,m.y,.6).some(c=>!c.hid&&!vole(c)&&Math.hypot(c.x-m.x,c.y-m.y)<.5))continue;
    m.go=1;for(const c of voisins(m.x,m.y,1.1))if(!c.hid&&!vole(c)&&Math.hypot(c.x-m.x,c.y-m.y)<1.1)this.hit(c,m.d,T,m.lv,m.t);this.fx.push({type:'boom',x:m.x+.5,y:m.y+.5,r:1.1,t:.35,d:.35,col:'#ffb347'});this.ev.push('boom')}
   this.mi=this.mi.filter(m=>!m.go)}
  if(this.al&&this.al.length)this.allies(dt,voisins);
  this.cgOk=false;
  const kids=[],me=this.classId;
  for(const c of this.cr){
   if(!c.leak&&c.hp<=0&&c.pe>0&&!c.dead){/* la peste saute sur les 2 voisins les plus proches */
    for(const o of this.cr.filter(o=>o!==c&&o.hp>0&&Math.hypot(o.x-c.x,o.y-c.y)<1.3).slice(0,2)){o.pe=3;o.ped=Math.max(o.ped||0,c.ped);if(o.ma>0)this.combo(o,'ÉPIDÉMIE !','#c9e07a')}}
   if(c.leak){this.lives--;this.hurt=6;const ex=c.o>=0&&this.G&&this.G.B[c.o];if(ex)ex.st.passe++;this.fx.push({type:'text',x:EX[0]+.5,y:EX[1]+.2,txt:'-1 vie',col:'#ff7b6e',t:.9,d:.9});this.ev.push('!leak')}
   else if(c.hp<=0){c.dead=1;this.st.tue++;const fy=flyH(c.k),pr=this.t.some(t=>TW[t.k].prime&&!(t.b>0)&&Math.hypot(t.x-c.x,t.y-c.y)<=rng(t));const b=Math.max(1,Math.round(CR[c.k].c/10*(pr?1.2:1)));this.gold+=b;
    this.fx.push({type:'puff',x:c.x+.5,y:c.y+.5-fy,col:CR[c.k].col,t:.35,d:.35},{type:'text',x:c.x+.5,y:c.y+.2-fy,txt:'+'+b,col:'#ffd95e',t:.7,d:.7});this.ev.push('die');
    this.mourir(c,me);
    if(CR[c.k].split){const m=c.max/CR[c.k].hp,K=CR[c.k].kid;for(let i=0;i<2;i++)kids.push({id:++UID,k:K,o:c.o,x:c.x,y:c.y,tx:c.tx,ty:c.ty,hp:CR[K].hp*m,max:CR[K].hp*m,sl:0,sf:1,gp:0,gt:0,rp:0,rt:0,f:c.f,ph:Math.random()*6,ox:(i-.5)*.3,oy:(Math.random()-.5)*.2,arm:0,cs:9})}}}
  this.cr=this.cr.filter(c=>!c.dead&&!c.leak).concat(kids);
  for(const f of this.fx){f.t-=dt;if(f.vx!==undefined){f.x+=f.vx*dt;f.y+=f.vy*dt}}this.fx=this.fx.filter(f=>f.t>0)}
 /* 2.39 : ce que la mort d'un monstre déclenche selon la race du terrain (Fureur, Spores, Âmes, morts relevés) */
 mourir(c,me){const lt=c.lt&&this.t.includes(c.lt)?c.lt:null,LT=lt&&TW[lt.k];
  if(LT&&LT.faction==1){const g=(LT.fu2?2:1)*(lt.fm||1),av=lt.fu||0;lt.fu=Math.min(FUREUR_MAX,av+g);lt.fuT=2;if(lt.fu>=FUREUR_MAX&&av<FUREUR_MAX&&!(lt.rg>0)){lt.rg=3;this.combo({x:lt.x,y:lt.y,k:0},'RAGE !','#ff6a4a')}
   if(LT.fuG)for(const t of this.t)if(TW[t.k].faction==1&&t!==lt){t.fu=Math.min(FUREUR_MAX,(t.fu||0)+1);t.fuT=2}}
  if(c.pz>=5){let n=0;for(const o of this.cr)if(o!==c&&o.hp>0&&Math.hypot(o.x-c.x,o.y-c.y)<1.3){o.pz=Math.min(DOSE_MAX,(o.pz||0)+3);o.pd=Math.max(o.pd||0,c.pd);o.pt=4;n++}
   if(n){this.fx.push({type:'boom',x:c.x+.5,y:c.y+.5,r:1.3,t:.4,d:.4,col:'#9be36a'});this.combo(c,'SPORES !','#b6f27a')}}
  if(me==4){const pr=this.t.some(t=>!(t.b>0)&&Math.hypot(t.x-c.x,t.y-c.y)<=rng(t)+.5);if(pr){this.am=Math.min(AMES_MAX,(this.am||0)+(c.ma>0?2:1));if(c.ma>0)this.combo(c,'RÉCOLTE !','#9fe8ff')}
   /* Nécromancien : 1 âme pour relever le mort (jamais un volant) */
   if(!CR[c.k].fly&&this.am>=1){const n=this.t.find(t=>TW[t.k].rz&&!(t.b>0)&&Math.hypot(t.x-c.x,t.y-c.y)<=rng(t));if(n){this.am--;const Z=TW[n.k].rz;this.invoquer(c.x,c.y,Z.d*2**(n.lv-1),Z.t,0)}}
   /* Puits des âmes : réserve pleine, 5 âmes deviennent de l'or */
   if(this.am>=AMES_MAX){const p=this.t.find(t=>TW[t.k].au&&TW[t.k].au.am&&!(t.b>0));if(p){this.am-=5;const g=10*p.lv;this.gold+=g;this.fx.push({type:'text',x:p.x+.5,y:p.y,txt:'+'+g+' or',col:'#9fe8ff',t:.9,d:.9})}}}}
 /* un mort relevé (gros = Colosse d'os) part de (x, y) et remonte le chemin vers l'apparition ; il frappe les monstres au sol autour de lui */
 invoquer(x,y,d,t,gros){const P=chemin(this);let bi=0,bd=INF;for(let i=0;i<P.length;i++){const q=Math.hypot(P[i][0]-x,P[i][1]-y);if(q<bd){bd=q;bi=i}}
  (this.al||(this.al=[])).push({id:++UID,x,y,i:bi,d,t,T:t,cd:0,g:gros?1:0,pe:this.t.some(o=>TW[o.k].pe&&!(o.b>0))});this.fx.push({type:'puff',x:x+.5,y:y+.5,col:'#e8e2c8',t:.4,d:.4})}
 allies(dt,voisins){const P=chemin(this);
  for(const a of this.al){a.t-=dt;a.cd-=dt;const v=a.g?.7:1.1;let sp=v*dt;
   while(sp>0&&a.i>=0){const[px,py]=P[a.i],dx=px-a.x,dy=py-a.y,dd=Math.hypot(dx,dy);if(dd<1e-3){a.i--;continue}const m=Math.min(sp,dd);a.x+=dx/dd*m;a.y+=dy/dd*m;sp-=m;a.f=dx>0?1:-1}
   if(a.i<0)a.t=0;
   if(a.cd<=0){const R=a.g?1:.65,L=voisins(a.x,a.y,R).filter(c=>!c.hid&&!vole(c)&&Math.hypot(c.x-a.x,c.y-a.y)<R);if(L.length){a.cd=a.g?.6:.5;
     for(const c of a.g?L:[L[0]]){this.hit(c,a.d,a.pe?SERVITEUR_PESTE:SERVITEUR,1);if(a.g&&!(c.imI>0)){c.im=.3;c.imI=.6}}this.fx.push({type:'slash',x:a.x+.5,y:a.y+.5,a:0,t:.18,d:.18,col:'#e8e2c8'})}}}
  for(const a of this.al)if(a.t<=0)this.fx.push({type:'puff',x:a.x+.5,y:a.y+.5,col:'#d8d2c0',t:.35,d:.35});this.al=this.al.filter(a=>a.t>0)}
}

/* ---------- IA ---------- */
const invest=b=>b.t.reduce((s,t)=>s+t.inv,0),airInv=b=>b.t.reduce((s,t)=>s+(!TW[t.k].gr&&Math.abs(t.x-6)<=2?t.inv:0),0),mages=b=>b.t.filter(t=>TW[t.k].mg).length;
function pathCells(b){return chaine(b,SP[0],SP[1],200)}

/* --- labyrinthe de l'IA (2.5, affiné en 2.6) : chaque terrain IA reçoit un plan cible au début de la partie ---
   grille plate (case i = y*C+x, 1 = mur), parcours en largeur rapide, hasard propre (graine tirée une fois) pour que le découpage dans le temps ne change rien. */
/* depuis la 2.25, mêmes règles que les monstres : 8 directions, sans couper le coin d'un mur. Coûts entiers : 5 en ligne droite, 7 en diagonale (≈ 5 × √2),
   d'où un parcours par files de priorité circulaires (8 files, Dial) presque aussi rapide que le parcours en largeur d'avant. NB : par case, nombre de voisins puis (voisin, coût, coin 1, coin 2). */
const N=C*R,SPI=SP[1]*C+SP[0],EXI=EX[1]*C+EX[0],NB=new Int16Array(N*33),DB=new Int16Array(N),BH=new Int16Array(8),EN=new Int16Array(N*8+8),ENX=new Int16Array(N*8+8);
for(let i=0;i<N;i++){const x=i%C,y=i/C|0;let k=0;for(const[dx,dy]of DIR8){const a=x+dx,b=y+dy;if(a<0||b<0||a>=C||b>=R)continue;const o=i*33+1+k++*4;
 NB[o]=b*C+a;NB[o+1]=dx&&dy?7:5;NB[o+2]=dx&&dy?y*C+a:-1;NB[o+3]=dx&&dy?b*C+x:-1}NB[i*33]=k}
/* longueur (en cases) du plus court chemin apparition → sortie, -1 si bloqué (DB garde les distances à la sortie, ×5) */
function plen(w){DB.fill(32767);BH.fill(-1);DB[EXI]=0;let ne=1,live=1;EN[0]=EXI;ENX[0]=-1;BH[0]=0;
 for(let d=0;live>0;d++){let e=BH[d&7];BH[d&7]=-1;
  while(e>=0){const i=EN[e];e=ENX[e];live--;if(DB[i]!=d)continue;if(i==SPI)return d/5;const o=i*33,q=o+1+NB[o]*4;
   for(let p=o+1;p<q;p+=4){const j=NB[p];if(w[j])continue;const nd=d+NB[p+1];if(nd>=DB[j])continue;const c1=NB[p+2];if(c1>=0&&(w[c1]||w[NB[p+3]]))continue;
    DB[j]=nd;const b=nd&7;EN[ne]=j;ENX[ne]=BH[b];BH[b]=ne++;live++}}}return -1}
function mzPath(w){if(plen(w)<0)return[];const out=[SPI];let i=SPI;
 while(DB[i]>0){const o=i*33;let nx=-1;for(let k=0;k<NB[o];k++){const p=o+1+k*4,j=NB[p];if(!w[j]&&DB[j]+NB[p+1]==DB[i]&&(NB[p+2]<0||(!w[NB[p+2]]&&!w[NB[p+3]]))){nx=j;break}}if(nx<0)break;i=nx;out.push(i)}return out}
const rnd32=a=>()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const MZ_LAM=.3,MZ_NC=4,MZ_K=[2000,2500,3200],MZ_PICK=[[.5,.3,.2],[.6,.4],[1]];
/* forme de départ tirée au hasard : serpentin horizontal (couloirs de 1 ou 2), serpentin vertical, ou semis aléatoire */
function mzTemplate(r){const w=new Uint8Array(N),f=r()<.35?0:r()<.25?1:2;
 if(f==0){const p=r()<.7?2:3;let side=r()<.5;for(let y=2+(r()*2|0);y<R-1;y+=p){const gw=1+(p==3&&r()<.5);for(let x=0;x<C;x++)if(side?x<C-gw:x>=gw)w[y*C+x]=1;side=!side}}
 else if(f==1){let top=r()<.5;for(let x=r()<.5?1:0;x<C;x+=2){for(let y=1;y<R-1;y++)if(top?y>1:y<R-2)w[y*C+x]=1;top=!top}}
 else for(let i=0;i<N;i++)w[i]=r()<.35?1:0;
 w[SPI]=w[EXI]=0;while(plen(w)<0)w[r()*N|0]=0;
 let n=0;for(let i=0;i<N;i++)n+=w[i];const L=plen(w);return {w,f,n,L,s:L-MZ_LAM*n,best:w.slice(),bs:L-MZ_LAM*n,it:0}}
/* recherche locale (recuit léger) : on ajoute ou retire une case ou un petit segment, on garde si le chemin s'allonge sans trop de tours */
function mzClimb(c,r,K,steps){for(let e=0;e<steps&&c.it<K;e++,c.it++){const w=c.w,T=2*(1-c.it/K)+.05,i=r()*N|0;if(i==SPI||i==EXI)continue;
 const seg=[i];if(r()<.3){const[dx,dy]=DIR8[r()*8|0];let x=i%C,y=i/C|0;for(let k=1+(r()*3|0);k>0;k--){x+=dx;y+=dy;if(x<0||y<0||x>=C||y>=R)break;const j=y*C+x;if(j!=SPI&&j!=EXI)seg.push(j)}}
 const v=w[i]?0:1,ch=seg.filter(j=>w[j]!=v);for(const j of ch)w[j]=v;const L=plen(w),n=c.n+(v?ch.length:-ch.length),s=L-MZ_LAM*n;
 if(L>=0&&(s>=c.s||r()<Math.exp((s-c.s)/T))){c.L=L;c.n=n;c.s=s;if(s>c.bs){c.bs=s;c.best=w.slice()}}else for(const j of ch)w[j]=1-v}}
/* fait avancer la génération du plan d'au plus « steps » essais (un essai ≈ un parcours en largeur) ; renvoie le plan quand il est prêt.
   Étapes : 1) MZ_NC formes de départ affinées par recherche locale ; 2) pour chacune : murs inutiles retirés, ordre de construction, note de milieu de partie ; 3) choix et rôles. */
function mzStep(A,steps){let M=A.mz;if(M&&M.ok)return M;
 if(!M)M=A.mz={r:rnd32(Math.random()*4294967296>>>0),c:[],ok:0,o:0};const r=M.r,LV=A.G?A.G.LV|0:0,K=MZ_K[LV];
 while(steps>0){let c=M.c[M.c.length-1];if(c&&c.it>=K&&M.c.length>=MZ_NC)break;if(!c||c.it>=K){c=mzTemplate(r);M.c.push(c)}const s=Math.min(steps,K-c.it);mzClimb(c,r,K,s);steps-=s}
 while(steps>0&&M.o<MZ_NC){const c=M.c[M.o];if(!c.left)steps-=mzPrune(c);else if(c.left.length)steps-=mzRemove(c,r);else{steps-=mzEval(c);M.o++}}
 if(M.o<MZ_NC)return null;
 mzChoose(M,LV);mzRoles(A,M);M.ok=1;return M}
const MZX=new Int8Array(N),MZY=new Int8Array(N);for(let i=0;i<N;i++){MZX[i]=i%C;MZY[i]=i/C|0}
const near=(i,j,d)=>{const dx=MZX[i]-MZX[j],dy=MZY[i]-MZY[j];return dx*dx+dy*dy<=d*d};
/* 2.33 : exposition = nombre de cases du chemin que voit chaque tour (rayon MZ_RE, à peu près la portée d'un Archer), additionné sur toutes les tours.
   C'est le temps que les monstres passent à portée des tours : une tour loin du chemin ne compte pas, et un chemin plus long compte pour chaque tour qui le borde.
   VOI : pour chaque case, les cases à moins de MZ_RE (21 au plus), pour un calcul rapide sur la grille. */
const MZ_RE=2.5,VOI=[],VOH=new Uint8Array(N);
for(let i=0;i<N;i++){const l=[];for(let j=0;j<N;j++)if(near(i,j,MZ_RE))l.push(j);VOI.push(Int16Array.from(l))}
function expo(w,P=mzPath(w)){VOH.fill(0);for(const j of P){const l=VOI[j];for(let k=0;k<l.length;k++)VOH[l[k]]++}let e=0;for(let i=0;i<N;i++)if(w[i])e+=VOH[i];return e}
/* murs inutiles : une tour qui ne touche pas le chemin (8 cases autour) et dont le retrait ne le raccourcit pas est retirée du plan ; puis l'ordre de construction est préparé */
function mzPrune(c){const w=c.best.slice(),L=plen(w);let n=1,ch=1;
 while(ch){ch=0;const adj=new Uint8Array(N);for(const j of mzPath(w)){n++;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const x=MZX[j]+dx,y=MZY[j]+dy;if(x>=0&&y>=0&&x<C&&y<R)adj[y*C+x]=1}}
  for(let i=0;i<N;i++)if(w[i]&&!adj[i]){w[i]=0;n++;if(plen(w)==L)ch=1;else w[i]=1}}
 c.w=w;c.cur=w.slice();c.left=[];for(let i=0;i<N;i++)if(w[i])c.left.push(i);c.walls=c.left.slice();c.rev=[];return n}
/* ordre de construction : on retire une à une, depuis le plan complet, la tour dont le retrait fait perdre le moins d'exposition (à égalité, celle hors du couloir aérien) ;
   construire dans l'ordre inverse donne, à chaque étape, des tours qui voient le chemin du moment. 2.33 : avant, seule comptait la longueur du chemin,
   et vers 3 min de jeu jusqu'à un tiers des tours de l'IA étaient loin du chemin (elles bouchaient un raccourci sans jamais tirer). */
const MZ_SMP=24;
function mzRemove(c,r){const cur=c.cur,left=c.left,E0=expo(cur);let bi=0,bk=INF;
 const smp=left.length<=MZ_SMP?left.map((_,k)=>k):Array.from({length:MZ_SMP},()=>r()*left.length|0);
 for(const k of smp){const i=left[k];cur[i]=0;const E=expo(cur);cur[i]=1;
  const key=(E0-E)+(Math.abs(MZX[i]-6)<=2?.3:0)+r()*.2;if(key<bk){bk=key;bi=k}}
 const i=left[bi];left.splice(bi,1);cur[i]=0;c.rev.push(i);return 2*smp.length+2}
/* note d'un candidat : exposition par tour après 15, 25, 40 et 60 tours (l'IA en a rarement plus en milieu de partie) et une fois complet
   (2.33 ; avant : longueur du chemin). pre garde la longueur du chemin à ces étapes. */
const MZ_AT=[15,25,40,60];
function mzEval(c){c.ord=c.rev.reverse();const w=new Uint8Array(N),Ls=[],Es=[];c.ord.forEach((i,n)=>{w[i]=1;if(MZ_AT.includes(n+1)){Ls.push(plen(w));Es.push(expo(w)/(n+1))}});
 c.L=plen(c.w);const Ef=expo(c.w)/c.ord.length;while(Ls.length<MZ_AT.length){Ls.push(c.L);Es.push(Ef)}
 c.pre=Ls;c.note=(Es.reduce((a,b)=>a+b,0)+Ef)/(MZ_AT.length+1);delete c.cur;delete c.rev;delete c.left;return 3*MZ_AT.length+4}
/* choix du plan parmi les candidats, sur la note de milieu de partie (le meilleur en Brutal, un des 2 ou 3 meilleurs sinon) */
function mzChoose(M,LV){const r=M.r;M.c.sort((a,b)=>b.note-a.note);const P=MZ_PICK[LV];let q=r(),ch=0;for(;ch<P.length-1;ch++){q-=P[ch];if(q<=0)break}
 const c=M.c[ch];M.f=c.f;M.w=c.w;M.ord=c.ord;M.walls=c.walls;M.pre=c.pre;M.note=c.note;M.c=null}
/* rôles (emplacement j de la faction) : Givre répartis le long du chemin final, Mages pour que leur détection couvre tout le chemin, air près du couloir des volants */
function mzRoles(A,M){const base=A.classId*10,rg=j=>TW[base+j].r,w=M.w,P=mzPath(w),walls=M.walls,role=new Int8Array(N).fill(-1);
 M.L=P.length-1;delete M.walls;
 const cov=(i,d)=>{let n=0;for(const j of P)if(near(i,j,d))n++;return n},gain=(i,d,cv)=>{let v=0;for(let n=0;n<P.length;n++)if(!cv[n]&&near(i,P[n],d))v++;return v},mark=(i,d,cv)=>{for(let n=0;n<P.length;n++)if(near(i,P[n],d))cv[n]=1};
 const ng=Math.min(6,Math.max(2,Math.round(M.L/15))),cG=new Uint8Array(P.length);
 for(let k=0;k<ng;k++){const tgt=P[Math.floor(P.length*(k+.5)/ng)];let bi=-1,bv=0;for(const i of walls){if(role[i]>=0||!near(i,tgt,rg(2)))continue;const v=gain(i,rg(2),cG);if(v>bv){bv=v;bi=i}}
  if(bi>=0){role[bi]=2;mark(bi,rg(2),cG)}}
 const cM=new Uint8Array(P.length);for(let k=0;k<6;k++){let bi=-1,bv=2;for(const i of walls){if(role[i]>=0)continue;const v=gain(i,rg(5),cM);if(v>bv){bv=v;bi=i}}
  if(bi<0)break;role[bi]=5;mark(bi,rg(5),cM)}
 /* hors couloir aérien : Canon dans les virages (beaucoup de chemin autour), Garde entre deux couloirs, sinon Archer ; un peu de hasard pour varier */
 for(const i of walls)if(role[i]<0){const ax=Math.abs(MZX[i]-6),cc=cov(i,rg(3)),cg=cov(i,Math.max(rg(1),1.45));
  role[i]=ax<=2?(ax<=1&&cov(i,rg(4))>=7?4:0):cc>=12||(cg>=4&&M.r()<.3)?3:cg>=4?1:cc>=8?3:0}
 M.role=role}
/* 2.33 : menace = PV des monstres reçus, monstre par monstre, avec un oubli progressif (×MEN_OUBLI à chaque action, environ 2 min de demi-vie) */
const MEN_OUBLI=.997,MEN_MIN=200,MAG_MAX=.4;
function observer(A){const mn=A.menace||(A.menace=new Float64Array(CR.length));for(let k=0;k<mn.length;k++)mn[k]*=MEN_OUBLI;for(const c of A.cr)if(!c._ia){c._ia=1;mn[c.k]+=c.max}}
/* dégâts par seconde et par or d'une tour k (niveau 1) posée en (x, y), contre la menace reçue : armure, vol, anti-magie, zone, longueur de chemin à portée */
function contreMenace(A,k,x,y){const W=TW[k],mn=A.menace,m=1+A.G.time/200,P=trajet(A),r=W.r;let Lg=0;for(const[a,b]of P)if(Math.hypot(a-x,b-y)<=r)Lg+=PAS_TR;const La=air({x,y},r);let v=0,tot=0;
 for(let q=0;q<mn.length;q++){const w=mn[q];if(!w)continue;tot+=w;const T=CR[q];if((T.fly&&W.gr)||(!T.fly&&W.ao)||(T.mi&&W.mag))continue;const mu=T.fly?W.air:W.sol;let d=(W.no?0:W.d)*mu;const ar=(T.arm||0)*m;if(ar&&!(W.pierce>=1))d=Math.max(d*.2,d-ar*(1-(W.pierce||0)));
  /* 2.39 : le poison, la brûlure et la peste ignorent l'armure */
  v+=w*(d+W.dot*mu*W.cd)*(T.fly?La:Lg)}return tot?v/tot/W.cd*W.zf/W.c:0}
/* emplacements ordinaires (Archer, Garde, Canon, Flammes du plan) : une fois la menace connue, le type qui fait le plus de dégâts par or contre elle sur cette case ;
   le type prévu par le plan garde un petit avantage (×1,15) ; pas de tour au sol seulement dans le couloir des volants, Mages au plus MAG_MAX des tours */
function choixType(A,i,j,n){const mn=A.menace;if(!mn||mn.reduce((a,b)=>a+b,0)<MEN_MIN)return j;const base=A.classId*10,x=i%C,y=i/C|0,ax=Math.abs(x-6);
 const opts=ax<=2?[0,4]:[0,1,3,4];if(n>=8&&A.t.filter(t=>TW[t.k].mag).length<MAG_MAX*n)opts.push(5);let bj=j,bv=-1;
 for(const o of opts){const v=contreMenace(A,base+o,x,y)*(o==j?1.15:1)*(.95+.1*Math.random());if(v>bv){bv=v;bj=o}}return bj}
/* tour à poser sur la case i du plan selon la situation (-1 : attendre d'avoir l'or) */
function mzKind(A,i,n,bud,thr,fs){const M=A.mz,base=A.classId*10,x=i%C,cnt=js=>A.t.filter(t=>js.includes(t.k-base)).length;let j=M.role[i];
 if(j==5&&!thr)j=0;if(j!=2&&j!=5)j=choixType(A,i,j,n);if(j==2&&cnt([2])>=1+n*.15)j=0;if((j==1||j==3)&&fs>.35&&Math.abs(x-6)<=3)j=0;
 /* 2.39 : l’anti-aérien dédié (emplacement 4) attend que des volants arrivent */
 if(j==4&&fs<.15)j=0;
 if(n<5&&TW[base+j].c>bud)j=0;
 /* 2.39 : version renforcée propre à chaque race (RACES[…].up), une fois sur deux à partir de 8 tours */
 const e=RACES[A.classId].up[j];if(e!==undefined&&n>=8&&bud>=TW[base+e].c&&Math.random()<.5)j=e;
 return TW[base+j].c<=bud?base+j:-1}
/* Chaque pièce gagnée est répartie entre deux bourses, défense et attaque, selon la pression subie (pen = jusqu'où les monstres avancent chez elle). */
/* 2.38 : quête en cours que cette IA a choisi de jouer (Game.qu.joue, tiré au lancement selon la difficulté), sinon '' */
const quJ=A=>{const q=A.G&&A.G.qu;return q&&q.joue&&q.joue[A.i]?q.id:''};
/* quêtes de construction : l'IA prend dans tout son or ; ce qu'elle dépense en trop est repris sur sa réserve d'attaque */
/* remplace la tour t par la tour k sur sa case (revente à 70 % déduite), avec un chantier ; false si l'or manque */
function transformer(A,t,k,bud){const mc=TW[k].c-Math.floor(t.inv*.7);if(bud<mc||A.gold<mc)return false;A.gold-=mc;t.k=k;t.lv=1;t.inv=TW[k].c;t.b=t.bt=buildT(t.inv,A.bm());t.fu=t.ht=t.age=0;A.ev.push('build');return true}
function aiDefend(A){const r=aiDefendre(A);if(A.dp<0){A.ap+=A.dp;A.dp=0}return r}
function aiDefendre(A){const M=mzStep(A,INF),time=A.G.time,qj=quJ(A),bud=['clicker','frozen','gonflette','bling'].includes(qj)?A.gold:Math.min(A.dp,A.gold),g0=A.gold,base=A.classId*10,n=A.t.length,ups=A.t.filter(t=>t.lv<5&&!(t.b>0)&&bud>=upCost(t));let ok=false;
 const todo=M.ord.filter(i=>!A.g[i/C|0][i%C]);
 /* 2.38, Gonflette et Bling-bling : monter sa tour la plus haute (ou la plus chère) ; si elle est en chantier ou trop chère, l'IA attend (sauf si elle prend des coups) */
 if(qj=='gonflette'||qj=='bling'){const c=A.t.filter(t=>t.lv<5).sort((a,b)=>qj=='bling'?b.inv-a.inv:b.lv-a.lv||b.inv-a.inv)[0];
  if(c){if(!(c.b>0)&&A.upgrade(c)){A.dp-=g0-A.gold;return true}if(!(A.hurt>0))return false}}
 const fs=(A.flyIn||0)/((A.hpIn||0)+1),thr=A.specSeen||(time>=150&&A.G.foes(A).some(b=>b.inc>=35));
 /* transformations : Mages sur leurs cases quand des Spectres deviennent possibles, Givre sur les siens quand le plafond le permet */
 for(const t of A.t){const i=t.y*C+t.x,j=M.role[i],cur=t.k-base;if(t.lv>2||t.b>0)continue;
  const fz=qj=='frozen'&&!todo.length&&!TW[t.k].mg;
  const want=j==5&&thr&&!TW[t.k].mg?5:(j==2||fz)&&cur!=2&&(fz||A.t.filter(o=>o.k-base==2).length<1+n*.15)?2:-1;if(want<0)continue;
  if(transformer(A,t,base+want,bud)){A.dp-=g0-A.gold;return true}}
 /* 2.39 : soutien (emplacement 7) sur la case qui a le plus de voisines, environ une tour sur 12 ; ultime (emplacement 9) après 7:00, sur la tour qui voit le plus de chemin */
 const libres=A.t.filter(t=>t.lv<=2&&!(t.b>0)&&[0,1,3].includes(t.k-base));
 if(n>=14&&libres.length&&A.t.filter(o=>o.k-base==7).length<Math.floor(n/12)){const vois=t=>A.t.filter(o=>o!==t&&Math.abs(o.x-t.x)<=1&&Math.abs(o.y-t.y)<=1).length;const t=libres.sort((a,b)=>vois(b)-vois(a))[0];if(transformer(A,t,base+7,bud)){A.dp-=g0-A.gold;return true}}
 if(time>420&&libres.length&&!A.t.some(o=>TW[o.k].u)&&bud>=TW[base+9].c*.8){const P=trajet(A),vu=t=>P.filter(([a,b])=>Math.hypot(a-t.x,b-t.y)<=TW[base+9].r).length;const t=libres.sort((a,b)=>vu(b)-vu(a))[0];if(transformer(A,t,base+9,bud)){A.dp-=g0-A.gold;return true}}
 /* 2.33 : défense complète (plan construit, toutes les tours au niveau 5) : l'or de défense ne peut plus servir, aiAct le passe à l'attaque */
 A.plein=!todo.length&&A.t.every(t=>t.lv>=5);
 /* amélioration : la tour qui couvre le plus de chemin (et de couloir aérien, d'autant plus que des volants arrivent) pour son prix */
 if(ups.length&&qj!='clicker'&&qj!='frozen'&&(!todo.length||(n>=12&&Math.random()<(n>=28?.5:.25)))){const path=pathCells(A),aw=.6*(1+2*fs),val=t=>{const T=TW[t.k],r=rng(t);let c=0;for(const[x,y]of path)if(Math.hypot(x-t.x,y-t.y)<=r)c++;if(!T.gr)for(let y=0;y<R;y++)if(Math.hypot(6-t.x,y-t.y)<=r)c+=aw;
   return c*(T.ed||.5)*T.zf*(T.fsp||T.im?1.6:T.mg?1.4:1)/T.c};
  const vs=new Map(ups.map(t=>[t,val(t)]));ups.sort((a,b)=>vs.get(b)-vs.get(a));ok=A.upgrade(ups[Math.random()<.75?0:Math.floor(Math.random()*ups.length)])}
 /* construction : la prochaine case du plan ; si elle est occupée par un monstre, on essaie les suivantes, mais on n'en saute pas une faute d'or */
 /* 2.38 : Clicker fou, des Archers (les moins chers) ; Frozen, du Givre ; les cases du plan restent les mêmes */
 else for(const i of todo.slice(0,4)){const qk=qj=='clicker'?base:qj=='frozen'?base+2:-1,k=qk>=0?(TW[qk].c<=bud?qk:-1):mzKind(A,i,n,bud,thr,fs);if(k<0)break;if(A.place(i%C,i/C|0,k)){ok=true;break}}
 A.dp-=g0-A.gold;return ok}
/* --- 2.33 : ce que chaque adversaire peut encaisser ---
   trajet(b) : points tous les PAS_TR case le long du chemin des monstres au sol, de case en case (chaine : pas le tracé exact en ligne droite de chemin(),
   environ 4 % plus long mais bien moins coûteux), en cache tant que le labyrinthe ne change pas.
   encaisse(b, k, m) : PV qu'une foule du monstre k (PV × m) perd en traversant le terrain b : pour chaque tour, dégâts par seconde contre ce monstre
   (armure, vol, anti-magie, invisibilité, bonus de faction), × temps passé à portée, × nombre de cibles touchées (zone). Une estimation, pas une simulation. */
const PAS_TR=.5,ZONE=[1,2.5,2,1,1,3],ENC=1.5,VAGUE_HZ=[.4,.25,.1];
function trajet(b){if(b._trD===b.d)return b._tr;const ch=chaine(b,SP[0],SP[1],C*R),out=[];
 for(let n=1;n<ch.length;n++){const[a,c]=ch[n-1],[d,e]=ch[n],k=Math.max(1,Math.round(Math.hypot(d-a,e-c)/PAS_TR));for(let q=0;q<k;q++)out.push([a+(d-a)*q/k,c+(e-c)*q/k])}
 b._trD=b.d;return b._tr=out}
/* profil de défense d'un terrain (en cache tant que ses tours et son chemin ne changent pas) : pour chaque tour active, dégâts d'un coup et longueur
   de chemin à portée (au sol, Lg ; couloir des volants, La) ; part du chemin à portée d'un Mage (détection) et d'un Givre (ralentissement) */
function profil(b){let h=b.t.length;for(const t of b.t)h=(h*31+t.k*7+t.lv*131+(t.b>0?3:0)+t.x*17+t.y*19)%1e9;if(b._prD===b.d&&b._prH===h)return b._pr;
 const P=trajet(b),act=b.t.filter(t=>!(t.b>0)),tw=[];
 /* points du chemin à portée de chaque tour, gardés sur la tour tant que le chemin, sa position et sa portée ne changent pas (une amélioration ailleurs ne refait pas tout) */
 const vus=t=>{const r=rng(t);if(t._vP===P&&t._vR===r)return t._v;const r2=r*r,v=[];for(let n=0;n<P.length;n++){const dx=P[n][0]-t.x,dy=P[n][1]-t.y;if(dx*dx+dy*dy<=r2)v.push(n)}t._vP=P;t._vR=r;return t._v=v};
 for(const t of act){const r=rng(t);tw.push({W:TW[t.k],d:dmg(t),Lg:vus(t).length*PAS_TR,La:air(t,r)})}
 const part=f=>{const ts=act.filter(t=>f(TW[t.k])),m=new Uint8Array(P.length);let n=0;for(const t of ts)for(const q of vus(t))if(!m[q]){m[q]=1;n++}
  return[P.length?n/P.length:0,Math.min(1,ts.reduce((s,t)=>s+air(t,rng(t)),0)/16)]};
 b._prD=b.d;b._prH=h;return b._pr={tw,mg:part(W=>W.mg),gel:part(W=>W.fsp||W.im)}}
function encaisse(b,k,m){const T=CR[k],p=profil(b),fly=T.fly?1:0,arm=(T.arm||0)*m;
 const vu=T.inv?p.mg[fly]:1,v=T.s*(T.acc?1.6:1)*(1-(T.mi?0:.3*p.gel[fly]));let K=0;
 for(const{W,d:d0,Lg,La}of p.tw){if((fly&&W.gr)||(T.mi&&W.mag))continue;const L=fly?La:Lg;if(!L)continue;
  if(!fly&&W.ao)continue;const mu=(fly?W.air:W.sol)*(W.ma||W.mk?1.07:1)*(W.ex?1.1:1);let d=(W.no?0:d0)*mu;if(arm&&!(W.pierce>=1))d=Math.max(d*.2,d-arm*(1-(W.pierce||0)));
  K+=(d/W.cd+W.dot*mu*(W.d?d0/W.d:1))*W.zf*(L/v+1)}
 return K*vu}
/* longueur du couloir des volants (colonne 6, de la ligne 0 à la ligne 16) à portée r de la tour t */
function air(t,r){const dx=Math.abs(t.x-EX[0]);if(dx>=r)return 0;const h=Math.sqrt(r*r-dx*dx);return Math.max(0,Math.min(EX[1],t.y+h)-Math.max(0,t.y-h))}
/* attaque : elle empile plusieurs revenus puis lâche une grosse vague, composée selon les faiblesses des adversaires */
function aiAttack(A){const time=A.G.time,qj=quJ(A);let bud=Math.min(A.ap,A.gold),sent=false;if(time<GRACE)return false;
 /* 2.38, Le gros cadeau : un boss dès que tout son or le paie (sinon elle garde son or pour lui) */
 if(qj=='cadeau'){const k=BOSS.filter(k=>CR[k].t<=A.tier&&A.gold>=CR[k].c).pop();if(k===undefined)return false;const g=A.gold;if(!A.G.send(A,k))return false;A.ap-=g-A.gold;return true}
 /* 2.38, Facteur et Pigeons : des petites vagues tout de suite, sans attendre la grosse réserve */
 if(bud<(qj=='facteur'||qj=='pigeons'?60:Math.min(6000,Math.max(60,A.inc*3))))return false;
 /* 2.13 : ouvre le palier suivant quand sa réserve d'attaque le permet (palier 2 dès 2:30, palier 3 dès 7:00) */
 const pc=PAL_C[A.tier];if(pc!==undefined&&time>=(A.tier==1?150:420)&&bud>=pc*1.5){const g=A.gold;if(A.G.unlock(A)){bud-=g-A.gold;A.ap-=g-A.gold}}
 const fo=A.G.foes(A),m=1+time/200;
 /* dans chaque famille, le monstre le plus cher que la réserve paie, parmi les paliers ouverts */
 const ok=k=>bud>=CR[k].c&&CR[k].t<=A.tier,top=l=>l.filter(ok).pop(),go=k=>{const g=A.gold;if(!A.G.send(A,k))return false;sent=true;bud-=g-A.gold;A.ap-=g-A.gold;return true};
 /* 2.33 : pour chaque famille, combien de monstres passeraient chez chaque adversaire si toute la réserve y allait (encaisse, ×ENC car l'estimation est prudente) ;
    on retient la famille qui fait perdre le plus de vies (avec du hasard : ±VAGUE_HZ selon la difficulté, plus en Normal), avec un bonus si un adversaire serait éliminé.
    Si aucune ne passe, la vague sert l'économie : monstres au sol, ceux qui rapportent le plus de revenu. */
 const cands=[...new Set([NORM,FLY,SPECS,ARMS,MIS,SPLITS,ACCS,STUNS].map(top).filter(k=>k!==undefined))],boss=top(BOSS);
 if(boss!==undefined&&time>(CR[boss].t==1?240:420))cands.push(boss);
 const vies=k=>{const T=CR[k],hp=T.hp*m*HPK,H=Math.floor(bud/T.c)*GROUP*hp;let s=0;for(const b of fo){const l=Math.max(0,H-ENC*encaisse(b,k,m))/hp;s+=Math.min(l,b.lives)+(l>=b.lives?3:0)}return s};
 const hz=VAGUE_HZ[A.G.LV|0]||VAGUE_HZ[0];let best=top(NORM),bs=0;for(const k of cands){const s=vies(k)*(1-hz+2*hz*Math.random());if(s>bs){bs=s;best=k}}
 if(qj=='pigeons'&&top(FLY)!==undefined)best=top(FLY);
 if(best===undefined)return false;
 /* soigneur et hâte avec une vague au sol assez grosse */
 if(bud>=500&&!CR[best].fly)for(const l of[HEALS,AURAS]){const k=top(l);if(k!==undefined&&bud>=CR[k].c*4&&Math.random()<.6)go(k)}
 for(let n=0;n<12;n++){const k=ok(best)?best:top(NORM);if(k===undefined||!go(k))break}
 return sent}
function aiAct(A){const time=A.G.time,gain=A.gold-A.lastG,danger=A.hurt>0,need=(A.G.foes(A).reduce((s,b)=>s+b.inc,0)*4+20)*(1+time/400);
 const f=danger||A.pen>.85?.8:A.pen>.65?.55:invest(A)<need*.35?.5:A.pen>.45?.3:.15;
 A.dp+=gain*f;A.ap+=gain*(1-f);if(danger&&A.lives<12){A.dp+=A.ap*.5;A.ap*=.5}
 /* fin de partie : défense au maximum, tout part en attaque */
 if(A.plein){A.ap+=A.dp;A.dp=0}
 observer(A);
 /* 2.38, Picsou : elle ne dépense rien tant que la quête dure (sauf si elle prend des coups) */
 if(quJ(A)=='picsou'&&!danger&&A.pen<.65){A.lastG=A.gold;return}
 for(let i=0;i<3&&aiDefend(A);i++);
 if(aiAttack(A))for(const b of A.G.foes(A))b.ev.push('warn');A.lastG=A.gold}


/* ---------- partie ---------- */
/* Une partie = 4 terrains. Utilisée telle quelle en solo (navigateur) et en ligne (serveur Cloudflare). */
let UID=0;
class Game{
 /* seats : [{name,col,ai,classId}] ; LV : difficulté, ne touche que les IA */
 constructor(seats,LV=0){this.LV=LV;this.time=0;this.tick=10;this.over=false;this.winner=-1;this.log=[];this.qu=null;this.quN=QU_T0;this.quF=[];
  this.B=seats.map((s,i)=>{const b=new Board(i,s.name,s.col,s.ai?1:0,s.classId);b.G=this;if(b.ai){b.gold+=DIFF[LV].g;b.dp+=DIFF[LV].g;b.lastG=b.gold}return b})}
 foes(b){return this.B.filter(o=>o!==b&&!o.dead)}
 eff(b){return b.ai?Math.round(b.inc*DIFF[this.LV].b):b.inc}
 /* 2.13 : ouvre le palier de monstres suivant (paliers 2 et 3 payants) */
 unlock(b){const c=PAL_C[b.tier];if(c===undefined||b.gold<c)return false;b.gold-=c;b.tier++;b.ev.push('up');return true}
 /* un envoi part chez tous les adversaires encore en jeu */
 send(from,k){const T=CR[k];if(this.time<GRACE||from.gold<T.c||T.t>from.tier)return false;from.gold-=T.c;from.inc+=T.i;from.st.env++;from.st.envOr+=T.c;if(T.fly)from.st.vol+=T.c;if(T.hero)from.st.boss++;for(const b of this.foes(from))b.send(k,1+this.time/200,from.i);return true}
 /* action d'un joueur humain : renvoie '' si accepté, sinon un code d'erreur (poor, blocked, unique, locked, max, busy, early, over, bad ; unique = deuxième tour ultime, 2.39) ; early = envoi pendant la phase « Construis » (2.30) */
 action(i,a){const b=this.B[i];if(!b||b.dead||b.ai||this.over||!a)return 'over';
  const x=a.x|0,y=a.y|0,k=a.k|0;
  if(a.type=='place'){const T=TW[k];if(!T)return 'bad';if(b.place(x,y,k))return '';return b.gold<T.c?'poor':T.u&&b.t.some(t=>TW[t.k].u)?'unique':'blocked'}
  if(a.type=='sell')return b.sell(x,y)?'':'bad';
  if(a.type=='upgrade'){const t=b.t.find(t=>t.x==x&&t.y==y);if(!t)return 'bad';return b.upgrade(t)?'':t.lv>=5?'max':t.b>0?'busy':'poor'}
  if(a.type=='send'){const T=CR[k];if(!T||T.cat=='x')return 'bad';if(this.time<GRACE)return 'early';if(T.t>b.tier)return 'locked';return this.send(b,k)?'':'poor'}
  if(a.type=='tier'){if(b.tier>=PAL_C.length)return 'max';return this.unlock(b)?'':'poor'}
  return 'bad'}
 /* avance la partie de dt secondes (dt ≤ 0,05) ; les événements de partie vont dans this.log */
 /* 2.38 : quêtes bonus (table QUETES). qu : quête en cours (id, fin, or, cible, scores sc, base, joue : les IA qui la jouent) ; quN : moment de la prochaine ;
    quF : quêtes déjà tirées (tirage sans remise, la liste repart de zéro quand tout est passé). Journal : {type:'quete', ph:'debut'|'fin', …}. */
 quete(){const B=this.B,al=quVivants(this);let q=this.qu;
  if(!q){if(this.time<this.quN||al.length<2)return;
   let L=QUETES.filter(Q=>!this.quF.includes(Q.id)&&(!Q.ok||Q.ok(this)));
   if(!L.length){const der=this.quF[this.quF.length-1];this.quF=[];L=QUETES.filter(Q=>Q.id!=der&&(!Q.ok||Q.ok(this)))}
   if(!L.length){this.quN=this.time+10;return}
   const Q=L[Math.floor(Math.random()*L.length)];this.quF.push(Q.id);
   q=this.qu={id:Q.id,t0:this.time,fin:this.time+Q.dur,or:quOr(this),cible:Q.cible?Q.cible(this):0,base:B.map(b=>Q.abs?0:Q.sc(b)),joue:B.map(b=>b.ai?Math.random()<(QU_JOUE[this.LV]||.5):false),sc:[]};
   this.log.push({type:'quete',ph:'debut',id:q.id,or:q.or,cible:q.cible,fin:q.fin})}
  const Q=QUETES.find(Q=>Q.id==q.id),sens=Q.sens||1;q.sc=B.map((b,i)=>b.dead?null:Q.sc(b)-q.base[i]);
  let g=[];
  if(Q.f=='course')g=al.filter(b=>q.sc[b.i]>=q.cible);
  if(!g.length&&this.time>=q.fin&&Q.f=='photo'){const v=al.map(b=>q.sc[b.i]*sens),m=Math.max(...v);if(sens<0||m>0)g=al.filter(b=>q.sc[b.i]*sens==m)}
  if(!g.length&&this.time<q.fin)return;
  const or=g.length?Math.round(q.or/g.length):0;
  for(const b of g){b.gold+=or;b.st.qu++;b.st.quOr+=or;b.fx.push({type:'text',x:EX[0]+.5,y:EX[1]-.6,txt:'+'+or+' or',col:'#ffd95e',t:1.6,d:1.6})}
  this.log.push({type:'quete',ph:'fin',id:q.id,g:g.map(b=>b.i),or});
  this.qu=null;this.quN=this.time+QU_PAUSE+Math.random()*60}
 step(dt){if(this.over)return;const B=this.B;this.time+=dt;this.tick-=dt;
  if(this.tick<=0){this.tick+=10;for(const b of B)if(!b.dead){const g=this.eff(b)+eco(b);b.gold+=g;b.st.rev.push(g)}this.log.push({type:'income'})}
  for(const b of B)if(b.ai&&!b.dead){mzStep(b,600);b.aiT-=dt;if(b.aiT<=0){b.aiT=.6;aiAct(b)}}
  for(const b of B)if(!b.dead)b.update(dt);
  for(const b of B)if(!b.dead&&b.lives<=0){b.dead=1;b.st.mort=this.time;b.cr=[];b.q=[];b.pr=[];this.log.push({type:'out',i:b.i})}
  this.quete();
  /* fin : un seul terrain debout, ou plus aucun humain en jeu */
  const alive=B.filter(b=>!b.dead);
  if(alive.length<=1||!alive.some(b=>!b.ai)){this.over=true;this.winner=alive.length==1?alive[0].i:-1;this.log.push({type:'end',winner:this.winner})}}
}
if(typeof module!='undefined'&&module.exports)module.exports={C,R,SP,EX,INF,TW,CR,RACES,REGLES,ROLES_J,etats,PAL_C,DIFF,GRACE,FACTIONS,GIVRE_LV,GIVRE_BONUS,RACINES_LV,QUETES,QU_T0,QU_PAUSE,Board,Game};