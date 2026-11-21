/* Silhouettes des 50 unités, dans l'ordre des emplacements de sim.js.
   Les pièces sont partagées par le rendu du plateau, le fantôme et les cartes. */
const SILHOUETTES = (() => {
  const boisClair='#c09662', or='#f6ca62', bleu='#315aa2', acier='#a9c6df', cuir='#66402b', peau='#e9b68e',
    brun='#744634', vert='#549748', feuille='#9cde62', cyan='#85ebfb', glace='#a3d7ff',
    violet='#8155c1', rose='#eca5ff', os='#f4e1bb', noir='#352a46', feu='#ff7a38';
  const formes = [];
  let pieces;
  const volume = (type, col, x,y,z, a,b,c) => pieces.push({type,col,x,y,z,a,b,c});
  const boule = (...p) => volume('boule',...p);
  const bloc = (...p) => volume('bloc',...p);
  const cristal = (...p) => volume('cristal',...p);
  const trait = (col, a,b, largeur=.065) => pieces.push({type:'trait',col,a,b,largeur});
  const arc = (x=.24,y=.69,z=.30,col=or) => {
    const bas=[x,y-.33,z-.04], haut=[x,y+.33,z-.04], milieu=[x,y,z+.13];
    trait(col,bas,[x,y-.19,z+.08]);trait(col,[x,y-.19,z+.08],milieu);
    trait(col,milieu,[x,y+.19,z+.08]);trait(col,[x,y+.19,z+.08],haut);
    const main=[x-.12,y,z-.22];
    trait(os,bas,main,.025);trait(os,main,haut,.025);
    trait(os,main,[x,y,z+.23],.028);
    cristal(acier,x,y,z+.25,.07,.05,.11);
  };
  const humain = (tissu, casque, spectre=false) => {
    const pied=spectre?.20:.06;
    for (const x of [-.10,.10]) {
      trait(noir,[x,.43,0],[x*1.25,pied,0],.11);
      if(!spectre)bloc(cuir,x*1.25,.085,.045,.13,.14,.22);
    }
    boule(tissu,0,.55,0,.35,.37,.26);
    bloc(or,0,.44,.11,.28,.065,.06);
    boule(spectre?glace:peau,0,.83,.04,.23,.26,.22);
    boule(casque,0,.94,0,.29,.23,.26);
    trait(tissu,[.14,.69,0],[.24,.69,.32],.115);
    trait(tissu,[-.14,.69,0],[-.16,.64,.18],.115);
  };
  const baton = (col=or,tete=cyan) => {
    trait(col,[-.24,.15,.11],[-.24,1.07,.16],.065);
    cristal(tete,-.24,1.09,.16,.23,.26,.22);
  };
  const lame = (col=acier,x=.25) => {
    trait(or,[x,.53,.22],[x,.73,.26],.08);
    trait(or,[x-.11,.68,.26],[x+.11,.68,.26]);
    cristal(col,x,.91,.27,.13,.47,.06);
  };
  const canon = (col=acier,diam=.17,y=.46) => {
    trait(col,[0,y-.09,-.18],[0,y+.11,.43],diam);
    boule(noir,0,y+.10,.423,diam*.63,diam*.68,.065);
  };
  const chassis = (col=acier) => {
    for(const x of [-.24,.24])bloc(noir,x,.13,0,.16,.23,.60);
    bloc(col,0,.29,0,.49,.24,.49);
  };
  const drone = (col=acier,lumiere=cyan) => {
    boule(col,0,.70,0,.36,.22,.43);
    trait(col,[-.34,.72,0],[.34,.72,0],.08);
    for(const x of [-.34,.34]) {
      boule(noir,x,.71,0,.24,.09,.27);
      boule(lumiere,x,.68,0,.14,.08,.16);
    }
    boule(lumiere,0,.70,.20,.14,.10,.08);
  };
  const fauve = (col, taille=1, y=.39) => {
    boule(col,0,y,-.06,.54*taille,.39,.53);
    boule(col,0,y+.16,.24,.35*taille,.33,.34);
    for(const x of [-.18,.18]) for(const z of [-.21,.15])
      trait(col,[x*taille,y,z],[x*1.24*taille,.07,z+.08],.12);
    for(const x of [-.08,.08])boule(or,x,y+.20,.39,.065,.057,.06);
  };
  const ailes = (col,y=.75) => {
    for(const q of [-1,1]) {
      trait(col,[0,y,0],[q*.38,y+.16,-.05],.16);
      trait(col,[q*.36,y+.16,-.05],[q*.46,y+.05,-.35],.10);
      cristal(col,q*.30,y+.07,-.19,.37,.11,.39);
    }
  };
  const rapace = col => {
    ailes(col,.77);
    boule(col,0,.76,0,.25,.27,.48);
    boule(os,0,.89,.17,.24,.23,.25);
    cristal(or,0,.83,.31,.13,.14,.21);
  };
  const arbre = (tronc=brun,canopée=vert,h=1) => {
    trait(tronc,[0,.06,0],[0,h*.89,0],.20);
    for(const q of [-1,1]) {
      trait(tronc,[0,.19,0],[q*.29,.06,.17],.10);
      trait(tronc,[0,h*.55,0],[q*.30,h*.79,.05],.12);
      boule(canopée,q*.28,h*.84,.05,.36,.30,.40);
    }
    boule(canopée,0,h,0,.45,.36,.42);
  };
  const orbe = (col,y=.78,anneaux=2) => {
    boule(col,0,y,0,.41,.41,.41);
    for(let j=0;j<anneaux;j++){
      const h=y-.22+j*.43;
      for(let i=0;i<6;i++){
        const pt=n=>[Math.cos(n*Math.PI/3)*.34,h,Math.sin(n*Math.PI/3)*.34];
        trait(os,pt(i),pt(i+1),.036);
      }
    }
  };
  const ajouter = dessin => {pieces=[];dessin();formes.push(pieces)};

  // Humains : personnages, armes de siège et bâtiments de soutien.
  ajouter(()=>{humain(bleu,or);arc();trait(cuir,[-.18,.41,-.18],[.03,.97,-.18],.12)});
  ajouter(()=>{humain(acier,bleu);lame();bloc(bleu,-.24,.57,.23,.29,.40,.10);bloc(or,-.24,.57,.29,.08,.23,.025)});
  ajouter(()=>{chassis(cuir);trait(boisClair,[0,.32,0],[0,.78,.27],.10);for(const x of [-.27,0,.27])trait(os,[x,.44,.29],[x,.87,.29],.034);for(const y of [.46,.65,.84])trait(os,[-.28,y,.29],[.28,y,.29],.034)});
  ajouter(()=>{chassis(or);canon(noir,.32,.52);for(const x of [-.29,.29])boule(cuir,x,.19,0,.13,.36,.36)});
  ajouter(()=>{chassis(cuir);trait(or,[0,.46,-.31],[0,.59,.42],.10);for(const q of [-1,1])trait(boisClair,[0,.55,.23],[q*.37,.63,-.12],.12);trait(os,[-.37,.63,-.12],[.37,.63,-.12],.028)});
  ajouter(()=>{humain(os,or);baton(or,or);boule(or,0,1.14,-.10,.33,.33,.055)});
  ajouter(()=>{bloc(cuir,0,.27,0,.62,.43,.49);bloc(bleu,0,.64,0,.71,.13,.59);for(const x of [-.27,.27])trait(cuir,[x,.25,.18],[x,.63,.18]);boule(or,.16,.38,.29,.19,.13,.15)});
  ajouter(()=>{humain(bleu,acier);trait(cuir,[.25,.07,.13],[.25,1.19,.13],.065);bloc(or,.08,1.04,.13,.34,.30,.045);bloc(bleu,.08,1.04,.16,.12,.21,.03)});
  ajouter(()=>{humain(noir,or);lame(or);cristal(feu,-.21,.64,.23,.20,.27,.16)});
  ajouter(()=>{chassis(or);for(const q of [-1,1])trait(or,[q*.25,.24,0],[q*.34,1.05,0],.14);orbe('#fff2ad',.78,1)});

  // Créatures : ailes, griffes, gueules et carapaces.
  ajouter(()=>{fauve('#ad6451');for(const x of [-.22,0,.22])cristal(or,x,.69,-.18,.09,.41,.14)});
  ajouter(()=>{fauve(violet);for(const q of [-1,1])for(const x of [-.07,.07])trait(os,[q*.29+x,.26,.23],[q*.33+x,.19,.43],.055)});
  ajouter(()=>{fauve('#5786ad',.94);for(const q of [-1,1])cristal(glace,q*.24,.75,.19,.15,.32,.14);boule(cyan,0,.51,.43,.22,.13,.10)});
  ajouter(()=>{fauve('#916c52',1.2,.31);boule(noir,0,.43,.43,.29,.20,.15);cristal(acier,0,.47,.51,.20,.19,.18)});
  ajouter(()=>rapace('#8c6054'));
  ajouter(()=>{fauve(violet,.85,.48);for(const q of [-1,1])trait(or,[q*.1,.73,.18],[q*.29,1,.11],.10);boule(rose,0,.78,.38,.14,.12,.06)});
  ajouter(()=>{fauve('#377aa4',.66,.25);trait('#377aa4',[0,.25,-.14],[.29,.45,-.41],.12);for(const z of [-.30,-.14,.02])cristal(cyan,0,.51,z,.13,.31,.15)});
  ajouter(()=>{fauve('#895b4c',1.28,.48);for(const q of [-1,1])trait(os,[q*.15,.49,.28],[q*.34,.73,.48],.10);bloc(cuir,0,.73,-.12,.55,.14,.37)});
  ajouter(()=>{humain(noir,glace,true);ailes('#58375d',.60);for(const q of [-1,1])cristal(os,q*.045,.77,.15,.045,.16,.06)});
  ajouter(()=>{fauve('#8c3e48',1.13,.43);ailes('#b45860',.79);trait('#8c3e48',[0,.4,-.3],[.26,.59,-.48],.13);for(const q of [-1,1])cristal(or,q*.13,.90,.21,.12,.34,.13)});

  // Herbe : pousses vivantes, tireurs végétaux et racines.
  ajouter(()=>{arbre(brun,vert,.94);arc(.29,.64,.31,feuille)});
  ajouter(()=>{for(const x of [-.31,-.1,.1,.31]){boule(vert,x,.25,0,.23,.37,.39);cristal(feuille,x,.53,.19,.10,.32,.12);trait(brun,[x-.13,.14,-.26],[x+.13,.32,.26],.08)}});
  ajouter(()=>{arbre(brun,'#749843',.77);for(const q of [-1,1])trait(brun,[0,.3,0],[q*.43,.06,-.21],.13);boule(or,0,.54,.13,.16,.09,.08)});
  ajouter(()=>{trait(vert,[0,.05,0],[0,.69,0],.13);for(let i=0;i<5;i++){const a=i*2*Math.PI/5;boule('#b05da4',Math.cos(a)*.26,.74,Math.sin(a)*.26,.30,.19,.30)}boule(feuille,0,.78,0,.30,.25,.31)});
  ajouter(()=>rapace('#5b9551'));
  ajouter(()=>{humain(vert,feuille);baton(brun,feuille);for(const q of [-1,1])cristal(vert,q*.18,.73,-.08,.18,.23,.18)});
  ajouter(()=>{for(let i=0;i<6;i++){const a=i*Math.PI/3;const x=Math.cos(a)*.31,z=Math.sin(a)*.31;trait(vert,[x,.03,z],[x,.31,z],.07);boule('#edacd2',x,.34,z,.20,.16,.20)}cristal(feuille,0,.50,0,.29,.36,.28)});
  ajouter(()=>{arbre(brun,'#4b8554',1.04);bloc(brun,-.31,.58,.23,.33,.49,.16);trait(feuille,[-.31,.37,.33],[-.31,.79,.33],.09)});
  ajouter(()=>{humain('#54754b',vert);arc(.27,.71,.32,'#c98850');cristal(feuille,-.03,1.09,-.04,.14,.31,.12)});
  ajouter(()=>{arbre('#5d4330',vert,1.09);for(const q of [-1,1]){trait(brun,[q*.1,.26,0],[q*.43,.09,-.37],.16);boule(feuille,q*.33,.78,.23,.32,.26,.30)}cristal(or,0,.58,.15,.20,.31,.10)});

  // Robots : drones, engins et automates.
  ajouter(()=>{drone();canon(bleu,.12,.65)});
  ajouter(()=>{humain(bleu,acier);for(const x of [-.28,.28])bloc(acier,x,.55,.23,.26,.27,.24);bloc(cyan,0,.84,.15,.20,.075,.04)});
  ajouter(()=>{chassis(bleu);trait(acier,[0,.39,-.1],[0,.55,.25],.22);cristal(cyan,0,.59,.41,.25,.23,.43)});
  ajouter(()=>{chassis(acier);canon(bleu,.28,.47);bloc(cyan,0,.49,-.25,.27,.18,.15)});
  ajouter(()=>{drone(bleu,or);for(const x of [-.22,.22])trait(acier,[x,.66,.02],[x,.86,.37],.14)});
  ajouter(()=>{chassis(noir);orbe(cyan,.71,1);for(const q of [-1,1])trait(bleu,[q*.22,.33,0],[q*.31,.92,0],.10)});
  ajouter(()=>{chassis(bleu);for(const x of [-.19,.19]){boule(feu,x,.59,-.12,.24,.48,.25);trait(acier,[x,.39,-.08],[x,.48,.39],.17)}});
  ajouter(()=>{orbe(rose,.82,2);bloc(bleu,0,.13,0,.57,.19,.57);cristal(cyan,0,.39,0,.19,.25,.20)});
  ajouter(()=>{chassis(bleu);trait(acier,[.18,.32,-.11],[.29,.72,.13],.13);trait(acier,[.29,.72,.13],[.29,.47,.36],.10);for(const x of [-.17,.05,.27])boule(or,x,.38,.31,.17,.13,.17)});
  ajouter(()=>{humain(bleu,acier);for(const q of [-1,1]){bloc(acier,q*.24,.76,0,.28,.43,.27);trait(noir,[q*.24,.74,0],[q*.24,.93,.34],.17)}cristal(cyan,0,.58,.15,.23,.30,.18)});

  // Magique : mages, esprits, reliques et ossements.
  ajouter(()=>{humain(violet,noir);baton(cuir,rose);bloc(rose,0,.61,.15,.19,.065,.025)});
  ajouter(()=>{humain(noir,violet,true);lame(cyan);cristal(violet,0,.23,0,.40,.40,.30)});
  ajouter(()=>{bloc(noir,0,.13,0,.43,.20,.42);cristal(violet,0,.65,0,.48,.91,.26);for(const x of [-.17,.17])trait(rose,[0,.42,.13],[x,.64,.13],.045)});
  ajouter(()=>orbe('#9bca54',.67,1));
  ajouter(()=>{bloc(noir,0,.14,0,.49,.24,.45);trait(noir,[0,.24,0],[0,.68,0],.22);ailes(violet,.77);boule(acier,0,.85,.10,.25,.28,.27)});
  ajouter(()=>{orbe(violet,.75,1);boule(os,0,.77,.18,.38,.26,.12);boule(noir,0,.77,.245,.15,.22,.055);boule(cyan,.015,.79,.274,.065,.08,.025)});
  ajouter(()=>{humain(noir,violet);baton(noir,cyan);for(const x of [-.29,.29])cristal(rose,x,.42,0,.17,.28,.19)});
  ajouter(()=>{humain('#4895a4',glace,true);bloc(glace,-.26,.58,.22,.34,.42,.09);cristal(cyan,-.26,.60,.28,.23,.29,.06)});
  ajouter(()=>{humain(noir,noir,true);trait(cuir,[.28,.17,.22],[.22,1.21,.22],.065);trait(os,[.22,1.21,.22],[-.13,1.14,.22],.085);trait(os,[-.13,1.14,.22],[-.29,.99,.22],.06)});
  ajouter(()=>{humain(os,acier);for(const q of [-1,1]){bloc(os,q*.25,.78,0,.30,.36,.28);trait(os,[q*.27,.76,.04],[q*.37,.34,.20],.16)}for(const y of [.49,.57,.65])bloc(noir,0,y,.14,.24,.04,.055)});

  return formes;
})();
