# Winter Realms — Tower Wars (Édition 2.0)

Jeu de type « tower wars » dans le navigateur : chaque joueur défend son propre terrain avec des tours et envoie des vagues de monstres chez ses adversaires. Le joueur affronte 3 IA, sur 4 terrains en parallèle.

Ce document a été **reconstitué à partir du code** (`index.html`). Il décrit les règles, les valeurs chiffrées et les choix de conception en vigueur.

---

## ⚠️ Règle de maintenance (obligatoire)

**À chaque ajout ou modification du jeu (nouvelle tour, nouveau monstre, changement d'équilibrage, de règle, d'interface, d'IA…), ce fichier `CLAUDE.md` DOIT être mis à jour dans le même commit.**

Concrètement :
1. Mettre à jour la ou les sections concernées (tableaux, règles, constantes).
2. Ajouter une ligne dans le **Journal des modifications** en bas du fichier **et** dans la section **Changelog** du `README.md`.
3. Si la version change, mettre à jour le numéro dans le `<title>` de `index.html` **et** dans le titre de ce fichier.
4. Un changement qui contredit ce document sans le mettre à jour est considéré comme incomplet.

Claude : quand tu modifies le jeu, applique cette règle sans qu'on te le demande.

## ⚠️ Règle de commits réguliers (obligatoire)

On commite **souvent, par petites étapes**, pour que tout le monde suive l'avancement :

1. **Un commit par amélioration** (une nouvelle tour, un monstre, une retouche d'équilibrage, un correctif, une évolution visuelle…). On ne mélange pas plusieurs sujets dans un même commit.
2. Chaque commit contient **à la fois** le changement dans `index.html` **et** la mise à jour de `CLAUDE.md`.
3. **Nouvelle version reçue** (fichier HTML partagé par un membre du groupe) : la copier dans `index.html`, lire le diff (`git diff`), mettre à jour `CLAUDE.md`, puis faire un commit nommé `Version X.Y : <résumé>`.
4. **Messages de commit** en français, au présent, courts et précis : `Ajoute la tour …`, `Corrige …`, `Rééquilibre …`, `Version 1.6 : plateau diorama`.
5. Faire `git pull` avant de commencer et `git push` juste après chaque commit, pour que les autres récupèrent les changements.
6. Ne jamais laisser une modification qui marche sans la commiter à la fin d'une séance de travail.

Claude : après chaque amélioration terminée, propose (ou fais, si on te l'a demandé) le commit et le push correspondants.

---

## 1. Structure technique

- **Deux fichiers, sans build ni dépendances** :
  - `sim.js` contient **toute la simulation** : tables de données, `class Board`, IA, et `class Game`, qui fait tourner une partie de 4 terrains. Il ne touche ni au DOM ni au son, ce qui permet au serveur multijoueur de le réutiliser tel quel. Les sons y sont seulement notés dans `board.ev` (un `!` devant signifie « toujours audible pour le propriétaire du terrain »). Les événements de partie (revenu, élimination, fin) vont dans `game.log`.
  - `index.html` contient l'interface, le dessin et les sons. Il charge `sim.js` avec `<script src="sim.js">`.
  - **Toutes les actions du joueur passent par `doAction()`**, qui appelle `Game.action()`. Cette fonction renvoie `''` si l'action réussit, sinon un code d'erreur : `poor`, `blocked`, `locked`, `max`, `over` ou `bad`.
- **Pour tester en local**, il faut un petit serveur web : `npx http-server` à la racine, puis ouvrir http://localhost:8080. Un `file://` ne charge pas toujours `sim.js`, surtout dans les aperçus intégrés. Ouvert normalement dans un navigateur, le fichier fonctionne aussi.
- **Seule ressource externe** : la police Google Fonts *Fredoka*.
- **Rendu** : Canvas 2D. Tous les visuels (tours, monstres, effets) sont **dessinés en code**, sans images. La netteté s'adapte à l'écran (`devicePixelRatio`, plafonné à 3).
- **Sons** : synthétisés avec Web Audio (oscillateurs et bruit), **aucun fichier audio**.
- **Pas de sauvegarde** : aucun `localStorage`. Chaque partie repart de zéro.
- **Style de code** : JavaScript compact, presque minifié (noms courts, une logique par ligne). Les **tables de données sont en tête du script** et c'est là qu'on règle l'équilibrage :
  | Constante | Rôle |
  |---|---|
  | `C`, `R`, `SP`, `EX` | Taille de la grille, case d'apparition, case de sortie |
  | `BASE_TW` | Les 6 archétypes de tours |
  | `FACTIONS` | Nom, icône, couleurs et noms des 10 tours de chaque faction |
  | `ARCH` | Archétype utilisé par chacun des 10 emplacements de tour |
  | `FACTION_BALANCE` | Modificateurs de coût, dégâts, portée et cadence, plus le bonus propre à chaque faction |
  | `ROLE` | Libellé de rôle de chaque emplacement |
  | `TW` | Les 50 tours, **calculées** à partir des tables précédentes (à ne pas éditer à la main) |
  | `CR` | Les monstres |
  | `DIFF` | Les niveaux de difficulté |
  | `HPK`, `GRACE`, `GROUP`, `AURA_R` | Constantes de gameplay |
- **Sections du script** : sons → simulation (`class Board`) → dessin → interface → IA → boucle principale (`loop`).
- **Langue** : toute l'interface est en **français**.
- **Mobile d'abord** : commandes tactiles, zones sûres (`safe-area-inset`), plein écran, mise en page portrait. En paysage (largeur ≥ 560 px), le HUD passe sur le côté.

---

## 2. Déroulement d'une partie

1. **Écran d'accueil** : on choisit une **faction** (5 au choix), puis une **difficulté** (Normal, Difficile ou Brutal). Les boutons de difficulté restent grisés tant qu'aucune faction n'est choisie (en pratique, l'Alliance est présélectionnée).
2. **Les 4 terrains** : celui du joueur (« Toi ») et ceux de IA 1 (rouge), IA 2 (bleu) et IA 3 (violet). Les IA jouent automatiquement les factions suivantes dans la liste : `(faction du joueur + 1, + 2, + 3) % 5`.
3. **Victoire** : toutes les IA sont éliminées. **Défaite** : le joueur est éliminé.
4. Un joueur est **éliminé** quand ses vies tombent à 0. Son terrain est alors vidé et grisé, et il ne reçoit plus de vagues.

### Ressources de départ (pour chaque terrain)
| Ressource | Valeur |
|---|---|
| Or | 100 |
| Revenu | +10 toutes les 10 s |
| Vies | 40 |

### Économie
- **Revenu** : versé toutes les **10 secondes**. Une barre dorée sous le HUD montre le temps restant.
- **Envoyer un monstre** fait **augmenter définitivement le revenu** (voir la colonne « +revenu » plus bas). C'est le cœur de la stratégie : attaquer, c'est aussi investir.
- **Prime par monstre tué** : `max(1, arrondi(coût / 10))` en or, gagnée par le terrain sur lequel le monstre meurt.
- **Revente d'une tour** : 70 % de l'or investi (achat et améliorations), arrondi à l'inférieur.

---

## 3. Le terrain

- Grille de **13 × 17 cases**. Les monstres apparaissent en **(6, 0)**, en haut au centre, et visent la sortie (un château) en **(6, 16)**, en bas au centre.
- **Monstres au sol** : ils suivent le **plus court chemin** vers la sortie (calcul en largeur sur 4 directions), recalculé à chaque pose ou vente de tour. Le chemin actuel est affiché en pointillés animés.
- **Monstres volants** : ils vont **en ligne droite** vers la sortie et ignorent les tours posées sur leur trajet.
- **On ne peut pas poser une tour** :
  - sur la case d'apparition ou de sortie ;
  - si elle **bloquerait complètement** le chemin, ou couperait le passage d'un monstre déjà en route ;
  - sur une case occupée par un monstre au sol, ou sur la case vers laquelle il se dirige.
- Chaque monstre qui atteint la sortie retire **1 vie**.

---

## 4. Les tours

### 4.1 Les 6 archétypes (`BASE_TW`)
| Archétype | Coût | Portée | Dégâts | Recharge | Particularités |
|---|---|---|---|---|---|
| Archer | 20 | 2,8 | 8 | 0,5 s | Tir simple, touche le sol et les airs |
| Canon | 50 | 2,5 | 20 | 1,2 s | Explosion de rayon 1,1 (60 % des dégâts autour), **sol uniquement** |
| Givre | 40 | 2,5 | 4 | 0,9 s | Explosion de rayon 1,2, **ralentit** pendant 1,5 s, **magique** |
| Mage | 90 | 3,2 | 45 | 1,4 s | **Magique**, **détecte les invisibles** dans sa portée |
| Garde | 30 | 1,5 | 20 | 0,55 s | Corps à corps (frappe directe), **sol uniquement** |
| Flammes | 70 | 2,0 | 3 | 0,12 s | Cône d'environ ±29°, plus tout ce qui est à moins de 0,6 case ; touche les airs |

- Les tours « magiques » (Givre, Mage) **n'ont aucun effet sur le Briseur de runes**.
- **Ciblage** : chaque tour vise, dans sa portée, le monstre visible **le plus proche de la sortie**.
- **Ralentissement** : le Givre multiplie la vitesse par `0,5 − 0,05 × (niveau − 1)`, soit ×0,5 au niveau 1 et ×0,3 au niveau 5, pendant 1,5 s. Les racines des Sylvestres multiplient la vitesse par ×0,82 (`T.sf`). Si un monstre est déjà ralenti, c'est le ralentissement **le plus fort** qui reste appliqué, et la durée retenue est la plus longue.

### 4.2 Les 10 emplacements par faction (`ARCH`, `ROLE`)
Chaque faction a 10 tours. L'emplacement `j` détermine l'archétype, un multiplicateur de puissance (qui s'applique au coût et aux dégâts) et quelques retouches :

| j | Archétype | Rôle | Puissance | Retouches |
|---|---|---|---|---|
| 0 | Archer | Tir rapide | ×1,00 | — |
| 1 | Garde | Garde rapprochée | ×1,08 | — |
| 2 | Givre | Contrôle | ×0,96 | — |
| 3 | Canon | Artillerie | ×1,12 | — |
| 4 | Flammes | Dégâts continus | ×1,18 | — |
| 5 | Mage | Arcanes | ×0,92 | — |
| 6 | Archer | Tireur d'élite | ×1,22 | dégâts ×0,88, recharge ×0,86, portée ×1,12 |
| 7 | Garde | Champion | ×1,30 | dégâts ×1,08, recharge ×1,12 |
| 8 | Givre | Entrave | ×1,16 | dégâts ×0,9 |
| 9 | Mage | Archimage | ×1,38 | dégâts ×1,08, portée ×1,08 |

Formules : `coût = max(10, arrondi(coût_base × puissance × coût_faction / 5) × 5)`, `dégâts = dégâts_base × puissance × dégâts_faction × retouche`. La portée et la recharge dépendent de la faction et des retouches, **pas** de la puissance.

### 4.3 Améliorations
- **5 niveaux** au maximum. Les points jaunes au pied de la tour indiquent son niveau.
- Coût pour passer au niveau suivant : `arrondi(coût × 1,5 × 2^(niveau−1) / 5) × 5`.
- **Les dégâts doublent à chaque niveau** (`dégâts × 2^(niveau−1)`).
- La portée augmente de **5 % par niveau**.
- La tour grandit visuellement à chaque niveau.

---

## 5. Les factions

Principe d'équilibrage (commentaire dans le code) : *des coefficients volontairement proches en rendement global ; chaque avantage a une vraie contrepartie.*

| Faction | Icône | Coût | Dégâts | Portée | Recharge | Bonus propre |
|---|---|---|---|---|---|---|
| Alliance | 🛡️ | ×1,04 | ×0,97 | **×1,10** | ×1,03 | **Anti-aérien** : +18 % de dégâts contre les volants |
| Horde | 🪓 | ×1,02 | ×0,96 | ×0,93 | ×1,04 | **Frénésie** : +30 % de dégâts sur les cibles à moins de 35 % de PV |
| Sylvestres | 🌿 | ×1,00 | ×0,96 | ×1,00 | ×1,02 | **Racines** : *toutes* leurs tours ralentissent les monstres (vitesse ×0,82 pendant 0,72 s). Leurs tours Givre gardent le ralentissement normal du Givre |
| Nains | ⚒️ | ×1,07 | **×1,08** | ×1,02 | ×1,08 | **Perforant** : ignorent 55 % de l'armure |
| Légion des ombres | ☠️ | ×1,01 | ×1,01 | ×0,99 | ×1,01 | **Malédiction** : une cible touchée est marquée 1,35 s, et chaque coup suivant sur elle fait +14 % |

Chaque faction a aussi un style visuel qui lui est propre : socle (pierre et créneaux, rondins, racines, hexagone riveté, anneaux flottants), couleur du sol de son terrain et palette.

### 5.1 Statistiques au niveau 1 (calculées)
Recharge en secondes, portée en cases. DPS = dégâts ÷ recharge, sans compter les bonus de faction ni les explosions.

#### Alliance
| # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée |
|---|---|---|---|---|---|---|---|
| 0 | Tour des archers | Archer | 20 | 7,8 | 0,515 | 15 | 3,08 |
| 1 | Bastion du chevalier | Garde | 35 | 21 | 0,567 | 37 | 1,65 |
| 2 | Obélisque de givre | Givre | 40 | 3,7 | 0,927 | 4 | 2,75 |
| 3 | Bombarde royale | Canon | 60 | 21,7 | 1,236 | 18 | 2,75 |
| 4 | Brasier du griffon | Flammes | 85 | 3,4 | 0,124 | 27 | 2,2 |
| 5 | Sanctuaire solaire | Mage | 85 | 40,2 | 1,442 | 28 | 3,52 |
| 6 | Tour des sentinelles | Archer | 25 | 8,3 | 0,443 | 19 | 3,45 |
| 7 | Garde du lion | Garde | 40 | 27,2 | 0,634 | 43 | 1,65 |
| 8 | Cristal hivernal | Givre | 50 | 4,1 | 0,927 | 4 | 2,75 |
| 9 | Arcaniste royal | Mage | 130 | 65,1 | 1,442 | 45 | 3,8 |

#### Horde
| # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée |
|---|---|---|---|---|---|---|---|
| 0 | Tour des chasseurs | Archer | 20 | 7,7 | 0,52 | 15 | 2,6 |
| 1 | Totem du berserker | Garde | 35 | 20,7 | 0,572 | 36 | 1,4 |
| 2 | Totem de glace | Givre | 40 | 3,7 | 0,936 | 4 | 2,33 |
| 3 | Canon des clans | Canon | 55 | 21,5 | 1,248 | 17 | 2,33 |
| 4 | Fourneau de guerre | Flammes | 85 | 3,4 | 0,125 | 27 | 1,86 |
| 5 | Chaman des flammes | Mage | 85 | 39,7 | 1,456 | 27 | 2,98 |
| 6 | Tour des éclaireurs | Archer | 25 | 8,2 | 0,447 | 18 | 2,92 |
| 7 | Garde-lame | Garde | 40 | 27 | 0,641 | 42 | 1,4 |
| 8 | Totem des esprits | Givre | 45 | 4 | 0,936 | 4 | 2,33 |
| 9 | Grand sorcier orc | Mage | 125 | 64,4 | 1,456 | 44 | 3,21 |

#### Sylvestres
| # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée |
|---|---|---|---|---|---|---|---|
| 0 | Arbre sentinelle | Archer | 20 | 7,7 | 0,51 | 15 | 2,8 |
| 1 | Gardien des racines | Garde | 30 | 20,7 | 0,561 | 37 | 1,5 |
| 2 | Pierre de rosée | Givre | 40 | 3,7 | 0,918 | 4 | 2,5 |
| 3 | Fleur explosive | Canon | 55 | 21,5 | 1,224 | 18 | 2,5 |
| 4 | Cœur ardent | Flammes | 85 | 3,4 | 0,122 | 28 | 2 |
| 5 | Cercle druidique | Mage | 85 | 39,7 | 1,428 | 28 | 3,2 |
| 6 | Nid des faucons | Archer | 25 | 8,2 | 0,439 | 19 | 3,14 |
| 7 | Dryade protectrice | Garde | 40 | 27 | 0,628 | 43 | 1,5 |
| 8 | Cristal lunaire | Givre | 45 | 4 | 0,918 | 4 | 2,5 |
| 9 | Ancien arcanique | Mage | 125 | 64,4 | 1,428 | 45 | 3,46 |

#### Nains
| # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée |
|---|---|---|---|---|---|---|---|
| 0 | Tourelle de guet | Archer | 20 | 8,6 | 0,54 | 16 | 2,86 |
| 1 | Automate garde | Garde | 35 | 23,3 | 0,594 | 39 | 1,53 |
| 2 | Cryo-forge | Givre | 40 | 4,1 | 0,972 | 4 | 2,55 |
| 3 | Mortier runique | Canon | 60 | 24,2 | 1,296 | 19 | 2,55 |
| 4 | Forge incandescente | Flammes | 90 | 3,8 | 0,13 | 29 | 2,04 |
| 5 | Canon arcanique | Mage | 90 | 44,7 | 1,512 | 30 | 3,26 |
| 6 | Baliste naine | Archer | 25 | 9,3 | 0,464 | 20 | 3,2 |
| 7 | Sentinelle d'acier | Garde | 40 | 30,3 | 0,665 | 46 | 1,53 |
| 8 | Générateur runique | Givre | 50 | 4,5 | 0,972 | 5 | 2,55 |
| 9 | Maître ingénieur | Mage | 135 | 72,4 | 1,512 | 48 | 3,53 |

#### Légion des ombres
| # | Tour | Type | Coût | Dégâts | Recharge | DPS | Portée |
|---|---|---|---|---|---|---|---|
| 0 | Tour des damnés | Archer | 20 | 8,1 | 0,505 | 16 | 2,77 |
| 1 | Chevalier funeste | Garde | 35 | 21,8 | 0,556 | 39 | 1,48 |
| 2 | Obélisque maudit | Givre | 40 | 3,9 | 0,909 | 4 | 2,48 |
| 3 | Mortier infernal | Canon | 55 | 22,6 | 1,212 | 19 | 2,48 |
| 4 | Puits de lave | Flammes | 85 | 3,6 | 0,121 | 30 | 1,98 |
| 5 | Nexus du néant | Mage | 85 | 41,8 | 1,414 | 30 | 3,17 |
| 6 | Œil démoniaque | Archer | 25 | 8,7 | 0,434 | 20 | 3,1 |
| 7 | Gardien spectral | Garde | 40 | 28,4 | 0,622 | 46 | 1,48 |
| 8 | Cristal corrupteur | Givre | 45 | 4,2 | 0,909 | 5 | 2,48 |
| 9 | Archimage noir | Mage | 125 | 67,7 | 1,414 | 48 | 3,42 |

---

## 6. Les monstres (`CR`)

### 6.1 Envoi
- Un envoi coûte le prix du monstre et fait apparaître un **groupe de 4** (`GROUP`) chez **chaque adversaire encore en jeu**, espacés d'environ 0,4 s.
- **Les monstres se renforcent avec le temps** : `PV = PV_base × (1 + temps/200) × 0,55` (`HPK`). L'armure suit le même multiplicateur `(1 + temps/200)`. À 10 minutes, les monstres ont donc 4 fois plus de PV.
- **Revenu gagné par envoi** :
  - monstres au sol : `arrondi(coût/10 × (1 + 0,1 × log10(coût/10)))`, une courbe croissante ;
  - autres monstres : `arrondi(coût × 0,065)`.
- Certains monstres ne peuvent être envoyés qu'après un **temps de jeu minimum**.

### 6.2 Liste
Vitesse en cases par seconde.

| Monstre | Catégorie | Coût | +revenu | PV de base | Vitesse | Disponible à | Capacité |
|---|---|---|---|---|---|---|---|
| Sapeur gobelin | Sol | 10 | +1 | 12 | 1,6 | 0:00 | — |
| Warg | Sol | 20 | +2 | 22 | 2,4 | 0:00 | Rapide |
| Brute orc | Sol | 65 | +7 | 82 | 1,4 | 0:00 | — |
| Troll des glaces | Sol | 120 | +13 | 160 | 1,5 | 0:00 | — |
| Golem runique | Sol | 300 | +34 | 420 | 1,0 | 0:00 | — |
| Cyclope des cendres | Sol | 1000 | +120 | 1500 | 1,1 | 0:00 | — |
| Chauve-souris | Volant | 30 | +2 | 16 | 2,0 | 0:00 | Vol |
| Griffon corrompu | Volant | 150 | +10 | 95 | 1,9 | 0:00 | Vol |
| Dragon ancien | Volant | 450 | +29 | 400 | 1,3 | 0:00 | Vol |
| Chaman de guerre | Spécial | 80 | +5 | 70 | 1,5 | 0:00 | **Hâte** : les alliés à moins de 1,7 case vont 1,4 fois plus vite |
| Prêtresse | Spécial | 100 | +7 | 80 | 1,4 | 0:00 | **Soin** : les alliés à moins de 1,7 case regagnent 5 % de leurs PV max par seconde |
| Gelée mutante | Spécial | 140 | +9 | 90 | 1,3 | 0:00 | **Se divise** en 2 Petits limons (35 PV de base, vitesse 1,6) à sa mort |
| Tortue | Spécial | 180 | +12 | 150 | 1,1 | 1:30 | **Blindée** : armure 5 |
| Briseur de runes | Spécial | 200 | +13 | 130 | 1,4 | 2:00 | **Anti-magie** : insensible au Givre et au Mage |
| Spectre | Spécial | 200 | +13 | 110 | 1,5 | 3:00 | **Invisible** sauf à portée d'une tour Mage |
| Saboteur gobelin | Spécial | 260 | +17 | 120 | 1,5 | 4:00 | **Étourdit** la tour la plus proche |
| Azh'Khar, seigneur des lames | Spécial (héros) | 900 | +59 | 1900 | 1,02 | 6:00 | **Boss** : armure 4 et étourdissement |

### 6.3 Détails des capacités
- **Armure** : chaque coup perd un montant fixe de dégâts (`armure × multiplicateur de temps`), mais garde toujours au moins **20 %** des dégâts. Les Nains réduisent cette armure de 55 %.
- **Étourdissement** : toutes les **3,5 s** (premier essai 2 s après l'apparition), le monstre étourdit pendant **2 s** la tour la plus proche dans un rayon de **2,3 cases**. Une tour déjà étourdie ne peut pas être ciblée.
- **Invisibilité** : un Spectre caché ne peut être ni ciblé, ni touché par les explosions ou les flammes.
- **Hâte et soin** : un monstre n'en profite pas pour lui-même. Les zones d'effet sont affichées en cercles colorés (jaune pour la hâte, vert pour le soin).

---

## 7. Difficulté (`DIFF`)
| Niveau | Revenu des IA | Or de départ en plus pour les IA |
|---|---|---|
| Normal | ×1,00 | +0 |
| Difficile | ×1,25 | +30 |
| Brutal | ×1,50 | +60 |

Le joueur, lui, garde toujours un revenu ×1.

---

## 8. Intelligence artificielle

Chaque IA agit toutes les **0,6 s**. Elle range chaque pièce d'or gagnée dans l'une de deux réserves :
- **défense**, qui reçoit 15 % à 80 % des gains selon la **pression** subie (`pen` : jusqu'où les monstres avancent sur son terrain), si elle a perdu une vie récemment, ou si sa défense est trop faible par rapport au revenu de ses adversaires ;
- **attaque** pour le reste. Si elle est en danger avec moins de 12 vies, la moitié de sa réserve d'attaque passe en défense.

**Défense** (`aiDefend`), jusqu'à 3 actions par tour :
- elle place ses tours selon un plan fixe (`PLAN`), dans l'ordre des rangées 8, 6, 10, 4, 12, 2, 14, en partant du centre ;
- elle choisit la tour selon ce qu'elle a déjà : Archer ou Garde au début, puis Givre, Flammes et Mage au centre, Canon ailleurs ;
- à partir de 10 tours, ou quand il n'y a plus de place, elle **améliore** la tour la plus rentable, celle qui couvre le plus de chemin et de couloir aérien par pièce d'or ;
- après **2:20**, elle **transforme** des tours faibles du centre en Mages, jusqu'à `min(5, 2 + minutes/5)` Mages.

**Attaque** (`aiAttack`) :
- rien pendant les **25 premières secondes** (`GRACE`) ;
- elle accumule de l'or jusqu'à `min(6000, max(60, revenu × 3))`, puis envoie une grosse vague ;
- elle compose cette vague selon les **faiblesses de ses adversaires** : des volants s'ils ont peu de défense aérienne, des Spectres s'ils n'ont pas de Mage, des Tortues s'ils ont beaucoup de tours « physiques », des Briseurs s'ils ont beaucoup de tours magiques ;
- elle ajoute Prêtresse et Chaman si sa réserve dépasse 500 ;
- elle envoie le héros après **7:00**, avec 28 % de chances à chaque vague.

---

## 9. Interface et commandes

- **HUD** : or, revenu toutes les 10 s, horloge, faction, bouton son, bouton plein écran. On y trouve aussi 4 vignettes avec une mini-carte, les vies et le revenu (bonus de difficulté compris) de chaque terrain. **Toucher une vignette** affiche le terrain correspondant (en lecture seule).
- **Onglets** : « Construire » ou « Envoyer » (Sol, Volants, Spéciaux). Les boutons trop chers ou pas encore débloqués sont grisés.
- **Poser une tour** : toucher une case. **Glisser** le doigt permet d'en poser plusieurs d'affilée.
- **Toucher une tour** : affiche ses DPS, sa portée, son rôle et ses bonus, avec les boutons Améliorer, Vendre et Fermer.
- **Retours visuels** : case rouge si la pose est refusée, textes flottants (+or, −1 vie, niveau), et un message en bas de l'écran (« Pas assez d'or », « le chemin serait bloqué », etc.).

---

## 9 bis. Multijoueur en ligne (depuis la v2.0)

### Règles
- **2 à 4 humains** sur les 4 terrains habituels. Les sièges libres sont joués par des **IA**, qui prennent de préférence les factions qu'aucun humain n'a choisies. La difficulté (Normal, Difficile, Brutal) **ne s'applique qu'aux IA**.
- **Salon** : on le crée depuis l'accueil (« Créer un salon »), ce qui génère un code de 4 caractères. On le rejoint avec ce code ou avec le lien `…/?salon=CODE`.
  - Le premier arrivé est le **chef du salon** : il choisit la difficulté des IA et lance la partie.
  - Chaque joueur choisit sa faction et un pseudo (16 caractères au plus).
  - Deux humains peuvent prendre la même faction.
- **Fin de partie** : il ne reste qu'un terrain, ou plus aucun humain en vie. Un humain éliminé reste spectateur jusqu'à la fin. Le salon revient automatiquement au lobby **8 s** après la fin de la partie.
- **Déconnexion** : le terrain du joueur reste en jeu, sans être repris par une IA. En revenant avec le même navigateur, il retrouve son siège (son jeton `wr-token` est gardé dans `localStorage`).
- Un joueur qui arrive pendant une partie, ou dans un salon complet, la regarde en **spectateur**.
- Couleurs des sièges : or, rouge, bleu, violet.

### Architecture
- `server/src/worker.js` : le **Worker** Cloudflare reçoit `GET /room/:CODE` en WebSocket et le redirige vers le **Durable Object `GameRoom`** de ce salon (`idFromName(CODE)`).
- `GameRoom` fait tourner `Game` (de `sim.js`, importé tel quel) **toutes les 50 ms** et envoie un **instantané toutes les 100 ms** : or, revenu, vies, tours, monstres, projectiles, nouveaux effets et sons. Le serveur fait autorité : les actions des joueurs sont validées par `Game.action()`.
- La page (`NET` dans `index.html`) envoie des actions (`{t:'act', a:{type, x, y, k}}`) et dessine les instantanés avec les fonctions de dessin existantes. Elle lisse les positions des monstres et des projectiles entre deux instantanés, et recalcule le chemin (`Board.dist`) à partir de la grille des tours.
- Messages du client : `hello`, `faction`, `diff`, `start`, `act`. Messages du serveur : `lobby`, `start`, `snap`, `res`.
- Origines autorisées : la constante `ORIGINS` dans `worker.js` (GitHub Pages, localhost, fichiers locaux).
- Adresse du serveur : la constante `SERVER` dans `index.html`, à `wss://winter-realms.winter-realms-server.workers.dev` en production et `ws://localhost:8787` en local. On peut forcer une autre adresse avec `?serveur=wss://…`.

### Coût : 0 €
Tout tient dans le plan gratuit Cloudflare Workers, sans carte bancaire :
- 100 000 requêtes par jour (chaque message reçu d'un joueur compte pour 1/20 de requête) ;
- 13 000 Go·s de Durable Objects par jour, soit environ 28 h de salon actif par jour ;
- les messages envoyés par le serveur ne sont pas comptés.

Le Durable Object est déclaré en **SQLite** (`new_sqlite_classes`), le seul type autorisé sur le plan gratuit. Le salon reste en mémoire tant qu'un joueur est connecté. Quand tout le monde part, il se vide.

### ⚠️ Déployer
- **Le site** (`index.html`, `sim.js`) est mis à jour **automatiquement** par GitHub Pages à chaque push sur `main`.
- **Le serveur, lui, ne se met pas à jour tout seul.** Après **toute modification de `sim.js`** (règles, équilibrage, IA) ou de `server/`, il faut le redéployer :
  ```bash
  cd server
  npx wrangler deploy
  ```
  Sinon, les parties en ligne tournent avec les anciennes règles.
- La première fois sur une machine : installer Node.js LTS, lancer `npm install` dans `server/`, puis `npx wrangler login`. Le compte Cloudflare utilisé est celui d'Emilien. Pour déployer, un autre membre doit être invité sur ce compte Cloudflare.
- **Tester en local** :
  - `npx wrangler dev` dans `server/` (port 8787) ;
  - en parallèle, un serveur web à la racine (`npx http-server -p 8080`), puis ouvrir http://localhost:8080 ;
  - pour jouer à deux sur la même machine, utiliser deux navigateurs différents : deux onglets du même navigateur partagent le même jeton joueur.

## 10. Choix de conception à respecter

1. **Pas d'étape de build** : `index.html` + `sim.js`, jouable hors ligne en solo (sauf la police). **La simulation reste dans `sim.js`, sans DOM ni son**, pour être partagée avec le serveur multijoueur.
2. **Tout est dessiné en code** (Canvas 2D) et **tous les sons sont synthétisés** : pas d'images ni de fichiers audio.
3. **Univers fantasy original** : noms, personnages et visuels propres au jeu. On ne copie pas les personnages, les visuels ou les noms d'un jeu existant.
4. **Style « maquette 2.5D » en relief** : ombres portées, dalles biseautées, éclairage doux, personnages caricaturaux (grosse tête, gros nez).
   - Depuis la v1.6, chaque terrain est un **plateau-diorama** : un socle épais aux bords arrondis et des dalles surélevées avec une tranche visible. Une **palette de biome** propre à chaque faction (bord, reflets, ombres, détails) colore le terrain.
   - Le **décor est placé de façon déterministe**, calculé à partir des coordonnées de la case et de la faction, sans hasard à chaque image, donc **sans scintillement**. On y trouve des motifs minéraux, des touffes d'herbe et des reflets sur les dalles, plus 22 petits éléments sur les marges (rochers, végétation).
   - Le portail d'apparition et le château de sortie ont une ombre portée.
   - Ces décors sont **purement visuels** : ils ne bloquent ni la pose de tours ni les déplacements.
5. **Équilibrage par coefficients** : on règle les tables (`BASE_TW`, `FACTION_BALANCE`, `CR`…) plutôt que les tours une par une. Chaque bonus de faction doit avoir une contrepartie.
6. **Attaquer = investir** : chaque envoi augmente définitivement le revenu. C'est le moteur de la partie.
7. **Montée en puissance avec le temps** : les PV des monstres augmentent avec le temps de jeu, et les monstres spéciaux se débloquent progressivement.
8. **Interface en français, pensée pour le mobile**, utilisable au doigt comme à la souris.

---

## 11. Points connus à vérifier

- ~~Racines des Sylvestres~~ : **corrigé en v1.6.1**. Avant, `hit()` lisait `T.rootFactor`, qui n'existait pas sur les tours. Les tours Garde et Flammes sylvestres donnaient alors une vitesse `NaN` : les monstres au sol étaient figés, et les volants restaient bloqués pour toujours sans pouvoir être tués.
- Le texte d'accueil annonce « +25 % / +50 % de revenu » pour les IA : c'est cohérent avec `DIFF`.

---

## Journal des modifications

| Date | Version | Modification |
|---|---|---|
| 2026-11-14 | 1.4 | Import initial du projet et création de ce document par rétro-ingénierie du code. |
| 2026-11-14 | 1.6 | Visuel uniquement : plateau-diorama avec socle et dalles surélevées, palette de biome par faction, décor déterministe (rochers, herbes, cristaux), ombres sous le portail et le château. Texte d'accueil retouché. **Aucun changement de règles ni d'équilibrage.** Le bug des racines sylvestres (§11) est toujours présent. |
| 2026-11-14 | 1.6.1 | Correction des racines sylvestres : ralentissement ×0,82 pendant 0,72 s sur toutes leurs tours (le Givre garde son propre ralentissement). Le ralentissement le plus fort l'emporte. Fin des monstres figés et des volants bloqués pour toujours. |
| 2026-11-14 | 1.7 | Technique : la simulation passe dans `sim.js` (classe `Game`, sons notés sous forme d'événements, actions via `Game.action`), en préparation du multijoueur. La fin de partie survient quand il ne reste qu'un terrain, ou plus aucun humain. **Aucun changement de règles en solo.** |
| 2026-11-14 | 2.0 | **Multijoueur en ligne** : salons de 2 à 4 humains (IA sur les places libres), code ou lien d'invitation, chef de salon, spectateurs, reconnexion. Serveur Cloudflare Workers et Durable Objects (`server/`, plan gratuit). Site publié sur GitHub Pages. |
