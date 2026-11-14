# Winter Realms — Tower Wars (Édition 2.5)

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
5. **Les tests doivent passer** (`node tests/tout.js`) avant chaque commit, et chaque évolution est présentée avec ses **trois bilans** (technique, gameplay, visuel). Voir §12.

Claude : quand tu modifies le jeu, applique cette règle sans qu'on te le demande.

## ⚠️ Règle de commits réguliers (obligatoire)

On commite **souvent, par petites étapes**, pour que tout le monde suive l'avancement :

1. **Un commit par amélioration** (une nouvelle tour, un monstre, une retouche d'équilibrage, un correctif, une évolution visuelle…). On ne mélange pas plusieurs sujets dans un même commit.
2. Chaque commit contient **à la fois** le changement dans `index.html` **et** la mise à jour de `CLAUDE.md`.
3. **Nouvelle version reçue** (fichier HTML partagé par un membre du groupe) : créer une branche, y copier le fichier dans `index.html`, lire le diff (`git diff`), mettre à jour `CLAUDE.md`, puis faire un commit nommé `Version X.Y : <résumé>`.
4. **Messages de commit** en français, au présent, courts et précis : `Ajoute la tour …`, `Corrige …`, `Rééquilibre …`, `Version 1.6 : plateau diorama`.
5. Faire `git push` juste après chaque commit **sur sa branche**, pour que les autres voient l'avancement.
6. Ne jamais laisser une modification qui marche sans la commiter à la fin d'une séance de travail.

Claude : après chaque amélioration terminée, propose (ou fais, si on te l'a demandé) le commit et le push correspondants, **toujours sur une branche, jamais sur `main`**.

## ⚠️ Règle des branches (obligatoire)

Plusieurs personnes travaillent en même temps, souvent depuis un téléphone, sur deux gros fichiers (`index.html`, `sim.js`). Pour éviter les conflits et les régressions :

1. **Interdit de commiter ou de pousser directement sur `main`.** Toute modification passe par une branche, puis une *pull request* (PR) sur GitHub.
2. **Une branche par sujet**, créée à partir d'un `main` à jour :
   ```bash
   git checkout main
   git pull
   git checkout -b <type>/<sujet-court>
   ```
3. **Nom de branche** : `<type>/<sujet-court>`, en minuscules, avec des tirets et sans accents. Types :
   - `tour/` : nouvelle tour ou modification d'une tour (`tour/baliste-glace`) ;
   - `monstre/` : nouveau monstre ou capacité (`monstre/necromancien`) ;
   - `equilibrage/` : retouche de chiffres (`equilibrage/cout-mage`) ;
   - `correctif/` : correction de bug (`correctif/racines-sylvestres`) ;
   - `visuel/`, `son/`, `ia/`, `interface/`, `serveur/`, `doc/` : selon le sujet.
4. **Petites branches, courte durée** : une branche = une amélioration, fusionnée dans les jours qui suivent. Si `main` a bougé entretemps, y récupérer les changements (`git pull origin main`) et régler les conflits **avant** la fusion.
5. **Pull request** : titre en français au même format que les commits. La description dit ce qui change et comment le tester. Elle signale si `sim.js` ou `server/` est modifié (le serveur devra être redéployé).
6. **Fusion dans `main`** : **pas de relecture obligatoire**. L'auteur fusionne lui-même sa PR après un test rapide du jeu (solo, et multijoueur si `sim.js` ou `server/` a changé). Après la fusion, on supprime la branche.
7. **Après une fusion qui touche `sim.js` ou `server/`** : le serveur se redéploie tout seul. Vérifier dans l'onglet **Actions** que le déploiement a réussi (voir §9 bis, « Déployer »).

Claude : avant de modifier quoi que ce soit, vérifie la branche courante. Si tu es sur `main`, crée d'abord une branche selon ces règles. Ne pousse jamais directement sur `main` : ouvre une PR. Fusionne-la seulement si on te le demande, après avoir testé le jeu.

**Règles supplémentaires pour Claude** :
- Les sessions Claude Code dans le cloud imposent leur propre nom de branche (`claude/…`). Il remplace alors le format `<type>/<sujet>`.
- **Ne jamais fusionner une PR sans l'accord explicite du concepteur**, donné dans la conversation (par exemple « je valide la fusion de la PR 4 »). Avant de fusionner, répéter le numéro et le titre de la PR et attendre un « oui » : les instructions sont souvent dictées à la voix, une erreur de transcription est possible.
- Ne jamais activer de fusion automatique.
- Une PR par évolution importante. Sa description suit le modèle `.github/pull_request_template.md` (trois bilans).

---

## 1. Structure technique

- **Le jeu tient en deux fichiers, sans build ni dépendances** :
  - `sim.js` contient **toute la simulation** : tables de données, `class Board`, IA, et `class Game`, qui fait tourner une partie de 4 terrains. Il ne touche ni au DOM ni au son, ce qui permet au serveur multijoueur de le réutiliser tel quel. Les sons y sont seulement notés dans `board.ev` (un `!` devant signifie « toujours audible pour le propriétaire du terrain »). Les événements de partie (revenu, élimination, fin) vont dans `game.log`.
  - `index.html` contient l'interface, le dessin et les sons. Il charge `sim.js` avec `<script src="sim.js">`.
  - **Toutes les actions du joueur passent par `doAction()`**, qui appelle `Game.action()`. Cette fonction renvoie `''` si l'action réussit, sinon un code d'erreur : `poor`, `blocked`, `locked`, `max`, `busy` (tour en chantier, depuis la 2.4), `over` ou `bad`.
- **Autour du jeu** (ces dossiers ne sont pas chargés par la page) :
  - `server/` : le serveur multijoueur (Cloudflare Workers), qui importe `sim.js` tel quel (voir §9 bis) ;
  - `tests/` : les tests automatiques, les captures et les bilans (voir §12) ;
  - `art/` : les **recettes des modèles 3D** (un script Blender par asset) et l'outil de génération ; `assets/3d/` : les fichiers 3D produits (GLB) et leur manifeste (voir §15 et `art/LISEZMOI.md`) ;
  - `.github/` : la vérification automatique des Pull Requests (`tests.yml`), le déploiement automatique du serveur (`deploy-server.yml`, voir §9 bis), l'étiquetage automatique des versions (`versions.yml` et `versionner.sh`, voir §14), la régénération des assets 3D (`assets-3d.yml`, voir §15) et le modèle de description de PR.
- **Pour jouer en local**, il faut un petit serveur web : `npx http-server` à la racine, puis ouvrir http://localhost:8080. Un `file://` ne charge pas toujours `sim.js`, surtout dans les aperçus intégrés. **Pour tester**, voir §12 : `node tests/tout.js`.
- **Seule ressource externe** : la police Google Fonts *Fredoka*.
- **Rendu** : Canvas 2D. Tous les visuels (tours, monstres, effets) sont **dessinés en code**, sans images. La netteté s'adapte à l'écran (`devicePixelRatio`, plafonné à 3).
- **Vue du terrain** (depuis la 2.1) : le canevas `#main` couvre toute la zone de jeu. Le plateau y est dessiné par `dessinerVue()` avec un zoom et un décalage (`VUE.z`, `VUE.ox`, `VUE.oy`), et son cadre est dessiné dans le canevas. `caseVersEcran(x, y)` donne la position d'une case à l'écran (elle sert aussi aux tests).
- **Sons** : synthétisés avec Web Audio (oscillateurs et bruit), **aucun fichier audio**.
- **Pas de sauvegarde** : aucun `localStorage`. Chaque partie repart de zéro.
- **Style de code** : JavaScript compact, presque minifié (noms courts, une logique par ligne). Les **tables de données sont en tête de `sim.js`** et c'est là qu'on règle l'équilibrage :
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
  | `BUILD_OR`, `BUILD_MIN`, `BUILD_MAX`, `BUILD_DIFF` | Temps de construction : 1 s par `BUILD_OR` pièces d'or, borné, multiplié selon la difficulté pour les humains (§4.4) |
- **Sections de `sim.js`** : tables de données → simulation (`class Board`) → IA (`aiDefend`, `aiAttack`, `aiAct`) → partie (`class Game`).
- **Sections du script de `index.html`** : sons → dessin → interface (dont le multijoueur, objet `NET`) → sons et événements → boucle principale (`loop`).
- **Retouches des emplacements 6 à 9** (§4.2) : elles sont écrites directement dans le calcul de `TW` (`late&&j==6?…`), pas dans une table.
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
- Chaque amélioration prend du temps (voir §4.4).

### 4.4 Temps de construction (depuis la 2.4)
- **Ratio** : **1 seconde pour 50 pièces d'or** dépensées (`BUILD_OR`), au minimum **0,5 s** (`BUILD_MIN`) et au maximum **8 s** (`BUILD_MAX`), puis multiplié selon la difficulté : `temps = min(8, max(0,5, prix / 50)) × multiplicateur`.
- **Multiplicateur de difficulté** (`BUILD_DIFF`, méthode `Board.bm()`) : il ne touche que les **humains**, comme les bonus de difficulté du §7 ne touchent que les IA. Les IA gardent toujours ×1.
  | Difficulté | Humains | IA |
  |---|---|---|
  | Normal | ×1 | ×1 |
  | Difficile | ×1,25 | ×1 |
  | Brutal | ×1,5 | ×1 |
- Il s'applique à la **pose** (prix de la tour) et à **chaque amélioration** (prix de l'amélioration). Exemples en Normal : Archer 20 or → 0,5 s ; Mage 85 or → 1,7 s ; Archimage 130 or → 2,6 s ; Archer du niveau 4 au 5 (240 or) → 4,8 s ; toute amélioration à 400 or ou plus → 8 s. En Brutal, un humain met 1,5 fois plus longtemps (Archimage 3,9 s, au plus 12 s).
- **Pendant le chantier**, la tour (champ `t.b` : secondes restantes, `t.bt` : durée totale) :
  - ne tire pas, et une tour Mage ne révèle pas les Spectres ;
  - ne peut pas être améliorée (code d'erreur `busy`) ;
  - n'est pas visée par l'étourdissement des Saboteurs et du héros ;
  - **bloque déjà le chemin** (la case est occupée dès la pose) ;
  - peut être vendue, au tarif normal de 70 %.
- Pendant une amélioration, le niveau affiché est déjà le nouveau ; la tour ne tire pas jusqu'à la fin des travaux.
- La transformation d'une tour en Mage par l'IA (§8) déclenche aussi un chantier (prix du Mage).
- **Visuel** : tour en transparence, échafaudage en bois, marteau qui frappe et barre de progression dorée sous la case. La fiche affiche « 🔨 Construction : N s » avant la pose, puis le compte à rebours ; le bouton Améliorer indique la durée de l'amélioration.

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

Le joueur, lui, garde toujours un revenu ×1. Depuis la 2.4, la difficulté rallonge aussi le temps de construction des humains : ×1, ×1,25 ou ×1,5 (§4.4).

---

## 8. Intelligence artificielle

Chaque IA agit toutes les **0,6 s**. Elle range chaque pièce d'or gagnée dans l'une de deux réserves :
- **défense**, qui reçoit 15 % à 80 % des gains selon la **pression** subie (`pen` : jusqu'où les monstres avancent sur son terrain), si elle a perdu une vie récemment, ou si sa défense est trop faible par rapport au revenu de ses adversaires ;
- **attaque** pour le reste. Si elle est en danger avec moins de 12 vies, la moitié de sa réserve d'attaque passe en défense.

**Labyrinthe** (depuis la 2.5) : chaque IA reçoit un **plan cible** (`A.mz`) au début de la partie.
- **Génération** (`mzStep`) : 4 candidats. Chacun part d'une forme tirée au hasard (serpentin horizontal à couloirs de 1 ou 2, serpentin vertical, semis aléatoire), puis il est affiné par une recherche locale avec recuit léger : on ajoute ou retire une case ou un petit segment. Score = longueur du chemin − 0,3 × nombre de tours.
  - Itérations par candidat : 2 000 / 2 500 / 3 200 selon la difficulté.
  - Le plan retenu est tiré parmi les 3 meilleurs en Normal (50/30/20 %), parmi les 2 meilleurs en Difficile (60/40 %), et c'est le meilleur en Brutal.
  - Un plan complet fait environ 100 cases de chemin, contre 16 en ligne droite.
- **Hasard propre** : la graine est tirée une fois de `Math.random`, ce qui rend la génération indépendante du découpage dans le temps.
- **Découpage** : la génération avance de 600 essais par pas de jeu (≈ 1 à 2,5 ms) ; elle dure environ 20 ms au total. Elle est terminée avant la première action, ou bien elle est finie d'un coup à la première action. Un parcours en largeur sur grille plate (`plen`) prend environ 1,3 µs.
- **Ordre de construction** : à partir du plan complet, on retire une à une la tour qui raccourcit le moins le chemin (à égalité, la moins utile au chemin actuel et au couloir des volants). On construit dans l'ordre inverse, si bien que le chemin s'allonge presque à chaque tour. En début de partie, les premières tours vont près du chemin droit et du couloir aérien (colonne 6).
- **Rôles des cases** (`mzRoles`) :
  - **Givre** : 2 à 6 emplacements (`L/15`), répartis à intervalles réguliers le long du chemin final. Ils sont construits en Givre seulement tant que leur nombre reste sous `1 + 15 % des tours` ; sinon un Archer est posé, puis transformé plus tard.
  - **Mage** : jusqu'à 6 emplacements choisis pour que leur détection couvre tout le chemin. Ce sont des Archers tant qu'il n'y a pas de **menace de Spectres** : temps ≥ 2:30 et un adversaire avec un revenu ≥ 35, ou un Spectre déjà reçu (`specSeen`). Dès la menace, ils sont transformés en Mages (prix réel du Mage de la faction).
  - **Couloir aérien** (|x − 6| ≤ 2) : Archer, ou Flammes au centre s'il y a beaucoup de chemin autour. Jamais de Canon ni de Garde.
  - **Ailleurs** : Canon dans les virages, Garde entre deux couloirs, Archer sinon, avec un peu de hasard.
  - Si plus de 35 % des PV reçus volent (`flyIn/hpIn`), les Canons et Gardes prévus près du centre deviennent des Archers, et les améliorations favorisent le couloir aérien.
  - Les versions renforcées (emplacements 6 à 9) sont utilisées quand l'IA a assez de tours et d'or.

**Défense** (`aiDefend`), jusqu'à 3 actions par tour :
- d'abord, une **transformation** si besoin (Mage ou Givre sur sa case, seulement pour une tour de niveau 1 ou 2 qui n'est pas en chantier ; la tour transformée repart en chantier) ;
- sinon, elle **améliore** la tour la plus rentable (celle qui couvre le plus de chemin et de couloir aérien par pièce d'or, jamais une tour en chantier), dès que le plan est terminé, ou par hasard à partir de 10 tours (35 %, puis 60 % à partir de 24 tours) ;
- sinon, elle **construit** la prochaine case du plan. Si un monstre l'occupe, elle essaie les 3 suivantes, mais ne saute jamais une case faute d'or. L'IA ne pose jamais de tour hors de son plan, ce qui corrige le blocage d'avant la 2.5 (l'IA cessait de construire vers 36 tours).

**Attaque** (`aiAttack`) :
- rien pendant les **25 premières secondes** (`GRACE`) ;
- elle accumule de l'or jusqu'à `min(6000, max(60, revenu × 3))`, puis envoie une grosse vague ;
- elle compose cette vague selon les **faiblesses de ses adversaires** : des volants s'ils ont peu de défense aérienne, des Spectres s'ils n'ont pas de Mage, des Tortues s'ils ont beaucoup de tours « physiques », des Briseurs s'ils ont beaucoup de tours magiques ;
- elle ajoute Prêtresse et Chaman si sa réserve dépasse 500 ;
- elle envoie le héros après **7:00**, avec 28 % de chances à chaque vague.

---

## 9. Interface et commandes

- **HUD** : or, revenu toutes les 10 s, horloge, **vies du joueur** (❤, depuis la 2.3), faction, bouton son, bouton plein écran.
- **Terrains des joueurs** (flottants depuis la 2.3, pour agrandir la carte sur téléphone) : un **bouton rond avec une icône de carte**, en haut à gauche du terrain (`#cartesBtn`), ouvre un panneau posé **par-dessus le terrain** (`#chips`) avec les 4 vignettes : mini-carte, vies et revenu (bonus de difficulté compris) de chaque terrain.
  - **Toucher une vignette** affiche le terrain correspondant (en lecture seule) et referme le panneau ; le bouton prend alors la couleur et le nom de ce joueur.
  - Toucher le terrain pendant que le panneau est ouvert le referme **sans poser de tour**.
  - La bannière en bas du terrain (« Terrain de … · ↩ revenir au tien ») se touche pour revenir à son propre terrain.
- **Onglets** : « Construire » ou « Envoyer » (Sol, Volants, Spéciaux). Les boutons trop chers ou pas encore débloqués sont grisés, et leur prix passe en rouge quand l'or manque.
- **Fiche d'information** (depuis la 2.1), entre les onglets et les boutons :
  - **Construire** : la tour sélectionnée est décrite en clair : nom, type, rôle, ⚔ dégâts par seconde, ◎ portée en cases, cibles (« sol et air » ou « sol uniquement »), effets (explosion de zone, ralentissement, souffle en cône, corps à corps, révèle les Spectres, magique), bonus de faction chiffré (calculé à partir de `FACTION_BALANCE`) ;
  - **tour posée** : les mêmes informations au niveau actuel, avec le gain du niveau suivant et son prix ;
  - **Envoyer** : rappel de la règle (chaque envoi attaque tous les adversaires et augmente le revenu).
  - En portrait, la fiche a une hauteur fixe pour que le terrain ne change pas de taille.
- **Cartes de tours** : prix, puis deux lignes en clair, « ⚔ N dégâts/s » et « ◎ portée N » (depuis la 2.3 ; avant, `⚔N/s ◎N ✈`). Le `✈` est remplacé par la pastille de cibles. **Cartes de monstres** : prix et revenu gagné ; un monstre verrouillé affiche « 🔒 dès m:ss ».
- **Pastilles de rôle** (depuis la 2.3) : sur l'icône de chaque carte de tour (56 × 46 px, fonction `towerIcon`) et dans la fiche, des pastilles carrées à cadre doré biseauté, dans l'esprit des icônes de commande des jeux de stratégie (glyphes dessinés en code, fonctions `drawBadge` et `drawTowerBadges`, table `BADGE`) :
  - **en haut à droite, le rôle** (archétype `T.s`) : flèche (Archer), épée (Garde), flocon (Givre), bombe (Canon), flamme (Flammes), étoile (Mage) ;
  - **en bas à gauche, les cibles** : montagne = sol uniquement (`T.gr`), aile = sol et air ;
  - **petite étoile violette** à côté : tour magique (`T.mag`), sans effet sur le Briseur de runes.
- **Aperçu sans sélectionner** (depuis la 2.3) : un **appui long** (400 ms) sur une carte de tour affiche sa fiche (liseré doré) sans changer la tour sélectionnée ; en relâchant, la fiche revient à la tour sélectionnée. À la souris, le **survol** fait la même chose. Un simple toucher sélectionne la tour, comme avant.
- **Construire une tour : deux touchers** (depuis la 2.2, pour éviter les constructions par erreur) :
  - **1er toucher** sur une case libre : **aperçu** (tour fantôme, cercle de portée en pointillés, case surlignée en or) et message « Touchez encore la case pour construire (prix) ». Rien n'est construit ni payé ;
  - **2e toucher sur la même case** : construction. Il n'y a pas de délai imposé entre les deux touchers ;
  - toucher une **autre case** déplace l'aperçu ; choisir une autre tour dans la barre change la tour de l'aperçu ; changer d'onglet ou de terrain l'annule ;
  - une case **impossible** (or insuffisant, chemin bloqué, case occupée) est signalée **dès le 1er toucher**, sans aperçu. Le contrôle (`peutConstruire`) reprend celui de `Board.place` sans rien modifier ;
  - au doigt, un toucher compte au relâcher ; un doigt qui **glisse** vers une autre case ne fait rien (la construction « à la volée » en glissant est supprimée) ;
  - à la souris : deux clics sur la même case.
- **Zoom et déplacement** (depuis la 2.1) : **deux doigts** pour zoomer (de 1× à 3×) et pour faire glisser la carte ; **molette** à la souris. Le bouton « Vue d'ensemble » apparaît quand on a zoomé et ramène au zoom normal. Sur la vignette du terrain affiché, un cadre blanc montre la partie visible. Une astuce l'annonce au lancement d'une partie solo.
- **Toucher une tour** : ouvre sa fiche (voir plus haut), avec les boutons Améliorer, Vendre et Fermer.
- **Paysage** (depuis la 2.1) : la colonne de droite défile si elle est trop haute ; avant, le haut de l'écran et le bas du terrain étaient coupés sur téléphone.
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
- **Accès réservé à la France** (depuis la v2.0.1) :
  - le serveur refuse (403) toute connexion dont le pays détecté par Cloudflare (`request.cf.country`) ne figure pas dans `ALLOWED_COUNTRIES` (`server/wrangler.toml`, actuellement `"FR"`) ;
  - la page affiche alors « Jeu en ligne indisponible ici », et le solo reste jouable ;
  - en local, `server/.dev.vars` désactive ce filtre ;
  - pour ajouter un pays, par exemple la Belgique : `ALLOWED_COUNTRIES = "FR,BE"`, puis redéployer.
  - **Limites** : ce filtre ne protège que le serveur multijoueur, pas le site GitHub Pages. Il bloque un ami en voyage à l'étranger, ainsi que les VPN et relais privés (iCloud Private Relay) qui sortent hors de France. À l'inverse, un VPN français permet de le contourner. C'est un frein, pas une vraie sécurité.

### Architecture
- `server/src/worker.js` : le **Worker** Cloudflare reçoit `GET /room/:CODE` en WebSocket et le redirige vers le **Durable Object `GameRoom`** de ce salon (`idFromName(CODE)`).
- `GameRoom` fait tourner `Game` (de `sim.js`, importé tel quel) **toutes les 50 ms** et envoie un **instantané toutes les 100 ms** : or, revenu, vies, tours, monstres, projectiles, nouveaux effets et sons. Le serveur fait autorité : les actions des joueurs sont validées par `Game.action()`.
- La page (`NET` dans `index.html`) envoie des actions (`{t:'act', a:{type, x, y, k}}`) et dessine les instantanés avec les fonctions de dessin existantes. Elle lisse les positions des monstres et des projectiles entre deux instantanés, et recalcule le chemin (`Board.dist`) à partir de la grille des tours.
- Messages du client : `hello`, `faction`, `diff`, `start`, `act`. Messages du serveur : `lobby`, `start`, `snap`, `res`.
- Dans l'instantané, chaque tour est un tableau `[x, y, k, lv, inv, a, sw, stun, b, bt]` ; `b` et `bt` (temps de chantier restant et total, depuis la 2.4) valent 0 hors chantier.
- Origines autorisées : la constante `ORIGINS` dans `worker.js` (GitHub Pages, localhost, fichiers locaux).
- Adresse du serveur : la constante `SERVER` dans `index.html`, à `wss://winter-realms.winter-realms-server.workers.dev` en production et `ws://localhost:8787` en local. On peut forcer une autre adresse avec `?serveur=wss://…`.

### Coût : 0 €
Tout tient dans le plan gratuit Cloudflare Workers, sans carte bancaire :
- 100 000 requêtes par jour (chaque message reçu d'un joueur compte pour 1/20 de requête) ;
- 13 000 Go·s de Durable Objects par jour, soit environ 28 h de salon actif par jour ;
- les messages envoyés par le serveur ne sont pas comptés.

Le Durable Object est déclaré en **SQLite** (`new_sqlite_classes`), le seul type autorisé sur le plan gratuit. Le salon reste en mémoire tant qu'un joueur est connecté. Quand tout le monde part, il se vide.

### ⚠️ Déployer
- **Le site** (`index.html`, `sim.js`) est mis à jour **automatiquement** par GitHub Pages à chaque fusion dans `main`.
- **Le serveur est redéployé automatiquement** par la GitHub Action `.github/workflows/deploy-server.yml` à chaque fusion dans `main` qui touche `sim.js`, `server/` ou ce fichier. On suit le déploiement dans l'onglet **Actions** du dépôt. On peut aussi le relancer à la main : **Actions → Déployer le serveur → Run workflow**.
  - L'action utilise deux secrets du dépôt (**Settings → Secrets and variables → Actions**) : `CLOUDFLARE_API_TOKEN`, un jeton API créé sur le compte Cloudflare d'Emilien avec le modèle « Edit Cloudflare Workers », et `CLOUDFLARE_ACCOUNT_ID`. Sans eux, le déploiement échoue.
  - Si le déploiement échoue (croix rouge dans Actions), les parties en ligne tournent avec les anciennes règles tant qu'il n'est pas réparé.
  - L'action tourne sous **Node 22** : Wrangler 4 exige Node 22.12 ou plus récent et refuse de démarrer sous Node 20.
- **Déploiement manuel** (secours, depuis un ordinateur) :
  ```bash
  cd server
  npx wrangler deploy
  ```
  La première fois sur une machine : installer Node.js LTS, lancer `npm install` dans `server/`, puis `npx wrangler login`. Le compte Cloudflare utilisé est celui d'Emilien. Pour déployer à la main, un autre membre doit être invité sur ce compte Cloudflare.
- **Tester en local** :
  - `npx wrangler dev` dans `server/` (port 8787) ;
  - en parallèle, un serveur web à la racine (`npx http-server -p 8080`), puis ouvrir http://localhost:8080 ;
  - pour jouer à deux sur la même machine, utiliser deux navigateurs différents : deux onglets du même navigateur partagent le même jeton joueur.

## 10. Choix de conception à respecter

1. **Pas d'étape de build** : `index.html` + `sim.js`, jouable hors ligne en solo (sauf la police). **La simulation reste dans `sim.js`, sans DOM ni son**, pour être partagée avec le serveur multijoueur.
2. **Tout est produit par du code** et **tous les sons sont synthétisés** : pas de fichiers audio. Le rendu 2D est dessiné en code (Canvas 2D). Les **modèles 3D** (depuis la préparation de la 3D) sont des fichiers GLB **générés par des scripts Blender versionnés** dans `art/` (§15), jamais retouchés à la main ; **aucun asset externe sans licence CC0**.
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
- **Constaté par les tests** (2.0.1). Ce sont des comportements réels du code, **non corrigés**, qui attendent une décision du concepteur :
  - plusieurs monstres qui sortent au même instant peuvent faire passer les vies **sous zéro** en interne (l'affichage montre 0) ;
  - ~~prix du Mage fixé à 90 pour la transformation~~ : disparu en 2.5 (l'IA utilise le vrai prix de la faction) ;
  - dès sa première action, chaque IA pose **jusqu'à 3 tours** (règle « jusqu'à 3 actions par tour ») ;
  - le §1 dit « aucun `localStorage` », mais depuis la v2.0 la page y garde le pseudo et le jeton multijoueur (§9 bis) ;
  - **2.4, temps de construction** : après validation par le concepteur, le moteur 2.4 a été figé (`tests/moteurs/v2.4/`) et les tests comparent désormais le jeu aux références 2.4. Les tests de mécanique qui supposaient une tour active dès sa pose attendent maintenant la fin du chantier (`pret(b)` dans `tests/outils/moteur.js`) ;
  - les tableaux chiffrés de ce document (§4.1, §5.1, §6.2, §7) correspondent exactement au code (vérifié par `node tests/outils/audit-doc.js`).

---

## 12. Tests et validation

### 12.1 Lancer les tests
| Commande | Ce qu'elle fait | Durée |
|---|---|---|
| `node tests/tout.js` | Tout : simulation (mécaniques et 15 parties entre IA) et parcours mobile dans un navigateur | ≈ 1 min |
| `node tests/tout.js --simulation` | Simulation seule. C'est ce que GitHub lance à chaque Pull Request. | ≈ 35 s |
| `node tests/tout.js --rapide` | Simulation avec 5 parties au lieu de 15, pour les petites retouches | ≈ 20 s |
| `node tests/bilan.js [version]` | Les **trois bilans** dans `rapports/bilan.html`, avec la comparaison visuelle par rapport à `version` (par défaut `origin/main`) | ≈ 3 min |
| `node tests/captures.js` | 10 captures (5 écrans × portrait et paysage) dans `captures/actuel/` | ≈ 1 min |
| `node tests/comparer-visuel.js [version]` | Avant/après visuel seul, dans `captures/comparaison/` | ≈ 2 min 30 |
| `node tests/outils/audit-doc.js` | Compare les tableaux chiffrés de ce document au code et liste les écarts, sans rien corriger | 1 s |
| `python art/outils/generer.py [asset…] [--verifier] [--apercus dossier]` | Génère (ou vérifie) les fichiers 3D à partir des scripts de `art/` ; demande Blender 5.3 (`pip install bpy==5.3.0`) | quelques s par asset |

Seul **Node.js** (version 22) est nécessaire. Les tests navigateur utilisent en plus **Playwright** et Chromium, présents dans l'environnement de Claude mais **pas ajoutés au projet**. Sans eux, ces tests sont ignorés avec un message clair.

### 12.2 Ce que contient `tests/`
- `simulation/` : les tests du moteur (`sim.js`). Ils vérifient que le jeu fonctionne (mécaniques, formules, parties qui se terminent). **Il n'y a pas de moteur figé ni de parties enregistrées** (supprimés en 2.5) : un changement d'équilibrage ou d'IA ne fait échouer que les tests qui décrivent précisément la mécanique modifiée, et on met ces tests à jour dans le même commit.
  - `tables` : forme des tables (50 tours, 18 monstres…), statistiques valides, et chaque tour recalculée à partir des formules. Les chiffres eux-mêmes peuvent changer librement.
  - `construction`, `chantier` (temps de construction, depuis la 2.4), `deplacements`, `combats`, `economie`, `vagues` (avec l'IA), `fin-de-partie` : les mécaniques. Les tests qui ont besoin d'une tour active appellent `pret(b)`, qui fait avancer le terrain jusqu'à la fin des chantiers.
  - `parties-ia` : 15 parties complètes (5 factions × 3 difficultés) qui doivent se terminer en moins de 30 min de jeu, sans valeur invalide, avec des tours construites et des attaques ; plus une partie rejouée deux fois avec la même graine, qui doit être identique.
- `navigateur/parcours.test.js` : le **parcours automatisé** d'un joueur dans Chromium au format téléphone (390 × 844 en portrait, 844 × 390 en paysage) : accueil, faction, difficulté, construction en deux touchers (aperçu, confirmation, déplacement de l'aperçu, glisser sans effet) et refus, panneau de tour, envoi, vignettes, fiche d'information, monstres verrouillés, zoom et déplacement à deux doigts (sans pose accidentelle), pose exacte en mode zoomé, « Vue d'ensemble », revenu, mise en page. **Ce n'est pas une garantie de compatibilité avec tous les téléphones** : Safari sur iPhone, les anciens Android et les vrais écrans tactiles ne sont pas testés.
- `outils/` : chargement du moteur dans un environnement isolé, hasard à graine, serveur web local, pilotage du navigateur, affichage en français, audit de la documentation.

### 12.3 Reproductibilité sans toucher au jeu
Les tests chargent `sim.js` dans un environnement isolé et y remplacent `Math.random` par un **hasard à graine** (`tests/outils/hasard.js`). Une même graine donne donc toujours la même partie. **Tous les tests utilisent une graine fixe** (1 par défaut, une graine par partie entre IA) : un test ne dépend jamais du vrai hasard, donc il réussit ou échoue toujours de la même façon. Dans le navigateur, le même hasard est injecté avant le chargement de la page, et l'horloge est figée. **Le jeu publié n'est pas modifié.**

### 12.4 Règles
1. Quand une évolution **change volontairement une mécanique**, on met à jour les tests qui la décrivent dans le même commit. Le bilan gameplay (avant → après, par rapport à `main`) montre ce qui a changé.
2. Un désaccord entre le code et ce document est **signalé, pas corrigé d'office** : le concepteur décide.
3. Ne jamais désactiver ou ignorer un test pour obtenir un résultat vert.

### 12.5 Les trois bilans
Chaque évolution est présentée avec trois bilans **séparés** (`node tests/bilan.js`) :
| Bilan | Contenu | Verdicts |
|---|---|---|
| 🔧 **Technique** | Les tests s'exécutent, le parcours mobile fonctionne, aucune erreur JavaScript. Liste des fichiers modifiés. | ✅ réussi / ❌ en échec |
| 🎮 **Gameplay** | Mécaniques vérifiées, statistiques changées et 15 parties entre IA, comparées au `sim.js` de `main` (avant → après), écarts entre la documentation et le code | ✅ identique à `main` / ⚠️ changé : **à valider par le concepteur** |
| 🎨 **Visuel** | Captures portrait et paysage, avant \| après \| différences, pourcentage de pixels changés | ✅ identique / ⚠️ changé : **à valider par le concepteur** / ⏸ non vérifiable |

**Une réussite technique ne vaut jamais validation du gameplay ni du rendu.** Le gameplay et le visuel ne sont « validés » que par le concepteur.

### 12.6 Conditions de la comparaison visuelle (contre les fausses différences)
- **Même machine, même navigateur, même séance** : l'« avant » (extrait de git) et l'« après » sont capturés l'un après l'autre par le même Chromium. On ne compare **jamais** des images faites sur deux machines différentes, ni des images enregistrées dans le dépôt.
- **Même scénario** : graine 12345, Alliance, Normal, 4 tours posées en (5,6), (7,6), (5,10) et (7,10), capture à 35 s de jeu, puis panneau de la tour (5,6), puis zoom à deux doigts autour de la case (6,7).
- **Horloge figée** : le temps du navigateur est en pause et n'avance que sur commande. Sans cela, les animations (pointillés du chemin, barre de revenu) diffèrent d'une capture à l'autre. Au chargement, l'horloge est en plus **alignée sur exactement 200 ms** : l'horloge simulée de Playwright démarre avec 1 ou 2 ms de décalage selon les passages, ce qui suffisait à décaler les animations.
- **Écran fixé** : 390 × 844 et 844 × 390, densité ×2, mode mobile tactile, langue `fr-FR`, fuseau `Europe/Paris`.
- **Rendu reproductible** : Chromium est lancé en rendu logiciel (`--disable-gpu`), sans lissage sous-pixel du texte (`--disable-lcd-text`, `--font-render-hinting=none`), avec un profil de couleur fixe (`--force-color-profile=srgb`) et sans optimisations variables. Sans ces options, le texte en gras pouvait être dessiné légèrement différemment d'une capture à l'autre (jusqu'à 0,4 % de faux écarts).
- **Police** : **tous** les fichiers de Fredoka (graisses 500 et 700, tous les jeux de caractères) sont chargés avant la première capture. Si la police manque d'un côté, les deux versions sont recapturées avec la police de remplacement.
- **Réseau** : seule la police est autorisée. Le serveur multijoueur n'est jamais contacté.
- **Tolérance** : un pixel compte comme changé si une couleur varie de plus de 16 sur 255. Ce seuil absorbe les infimes variations de lissage, qu'on observe jusqu'à 1 sur 255. Un écran est « identique » sous 0,05 % de pixels changés.
- **Témoin** : la version actuelle est capturée deux fois. Si le témoin dépasse 0,05 %, la comparaison est déclarée **non fiable** au lieu d'afficher de fausses différences.
- **Limite** : seule la partie visible de l'écran est comparée. Un élément sous la ligne de flottaison (par exemple « Jouer entre amis » en paysage) n'est pas vu.

### 12.7 Procédure de validation (pour le concepteur, sans connaissance technique)
1. **Lire le compte rendu de Claude** : ce qui a changé, puis les trois bilans d'une ligne chacun.
2. **Regarder les images** envoyées : les captures, et pour un changement visuel, l'image « avant | après | différences ». Les zones rouges montrent ce qui a bougé.
3. **Ouvrir la Pull Request** sur GitHub : vérifier la coche verte « Tests de simulation » et la liste des fichiers modifiés.
4. *(Facultatif)* Jouer sur la branche, ou demander d'autres captures à Claude.
5. **Répondre** : « je valide la fusion de la PR N », ou demander des corrections. Claude répète le titre et attend votre « oui » avant de fusionner.

### 12.8 Vérification automatique sur GitHub
`.github/workflows/tests.yml` lance `node tests/tout.js --simulation` à **chaque Pull Request vers `main`**, avec Node 22, sans rien installer d'autre. Le résultat s'affiche dans la PR sous le nom « Tests de simulation ». Les tests navigateur n'y sont pas lancés. La vérification ne publie rien et ne fusionne rien.

---

## 13. Protection de la branche `main` (réglage GitHub)

À faire par un administrateur du dépôt, **dans un navigateur** (l'application mobile GitHub n'a pas ces réglages ; sur téléphone, utiliser le mode « version ordinateur »). Objectif : rendre **impossible** toute modification directe de `main` et imposer le passage par une Pull Request, **sans fusion automatique**.

1. github.com/pompidou-all-stars/winter-realms → **Settings** → **Rules** → **Rulesets** → **New ruleset** → **New branch ruleset**.
2. **Ruleset name** : `Protection de main`. **Enforcement status** : `Active`.
3. **Bypass list** : la laisser **vide** (personne ne contourne la règle, administrateurs compris).
4. **Target branches** → **Add target** → **Include default branch**.
5. Cocher :
   - **Restrict deletions** ;
   - **Require a pull request before merging**, avec **Required approvals : 0** (personne n'est obligé d'approuver, mais tout passe par une PR) ;
   - **Block force pushes**.
6. **Create**.
7. **Plus tard**, une fois que la vérification « Tests de simulation » a tourné au moins une fois sur une PR : modifier la règle, cocher **Require status checks to pass**, puis **Add checks** → `Tests de simulation`. Le nom n'est proposé qu'après un premier passage.
8. **Settings** → **General** → section **Pull Requests** : vérifier que **Allow auto-merge** est **décoché**.

9. *(Facultatif, recommandé)* Protéger aussi les **étiquettes de version** : **New ruleset** → **New tag ruleset**, nom `Protection des versions`, cible `Include by pattern` → `v*`, cocher **Restrict updates** et **Restrict deletions** (ne **pas** cocher « Restrict creations », sinon l'étiquetage automatique du §14 serait bloqué).

Pour vérifier : une tentative de `git push` directe sur `main` doit être refusée par GitHub.

---

## 14. Versions et retour arrière

### 14.1 Chaque fusion dans `main` reçoit une version
L'action GitHub `.github/workflows/versions.yml` (script `.github/versionner.sh`) tourne **après chaque fusion dans `main`** et pose une **étiquette de version** (tag git et « Release » GitHub, visibles dans l'onglet *Releases* du dépôt) :
- la version vient du `<title>` d'`index.html` (« Édition X.Y.Z ») ;
- **nouvelle version du jeu** (le numéro a changé) : étiquette `vX.Y.Z` ;
- **fusion sans changement de version** (tests, documentation, outillage) : `vX.Y.Z.1`, puis `vX.Y.Z.2`… (« révision, jeu inchangé ») ;
- chaque Release liste les changements depuis la version précédente, et permet de télécharger le code de cette version.

Versions historiques étiquetées automatiquement (une seule fois) :

| Étiquette | Commit | Contenu |
|---|---|---|
| `v1.4` | `bfc655a` | Import initial |
| `v1.6` | `5dee062` | Plateau diorama |
| `v1.6.1` | `313ce10` | Correction des racines sylvestres |
| `v1.7` | `c868ff9` | Simulation dans `sim.js` |
| `v2.0` | `e4636a4` | Multijoueur en ligne |
| `v2.0.1` | `4a1fb64` | État de `main` juste avant le socle de tests (France, règle des branches, déploiement auto) |

Claude ne peut pas créer d'étiquette lui-même (l'environnement cloud n'autorise que l'envoi de sa propre branche) : c'est pour cela que GitHub s'en charge. Pré-requis : dans **Settings → Actions → General → Workflow permissions**, l'organisation doit permettre « Read and write permissions » ; sinon l'action échoue et il faut cocher ce réglage.

### 14.2 Revenir à une version (« rollback »)
Le concepteur dit à Claude : « **reviens à la version vX.Y.Z** ». Claude :
1. crée une branche à partir de `main` à jour et y **restaure tous les fichiers** de l'étiquette demandée (`git restore --source vX.Y.Z -- .`, l'historique est conservé, rien n'est effacé) ;
2. présente les trois bilans (comparaison visuelle avec `main`, gameplay comparé à `main`) ;
3. ouvre une PR « Revient à la version vX.Y.Z » et attend l'accord explicite du concepteur avant de fusionner ;
4. à la fusion : le site GitHub Pages revient à cette version, le **serveur est redéployé automatiquement** si `sim.js` ou `server/` changent (§9 bis), et une nouvelle étiquette est posée (un retour arrière est lui-même une version, donc on peut l'annuler de la même façon).

On ne réécrit **jamais** l'historique de `main` (pas de « force push ») : le retour arrière est une nouvelle modification.

Attention : revenir à une version **antérieure à v2.0.1.1** retire aussi les tests (`tests/`) et ces règles ; il vaut mieux alors ne restaurer que les fichiers du jeu (`index.html`, `sim.js`, `server/`) — Claude le proposera.

---

## 15. Assets 3D (préparation)

Le mode d'emploi complet est dans **`art/LISEZMOI.md`**. L'essentiel :
- **Un script Python Blender par asset** dans `art/` : c'est la **source** du modèle. `art/outils/generer.py` l'exécute dans une scène vide, exporte `assets/3d/<asset>.glb` et met à jour `assets/3d/manifeste.json` (taille, triangles, empreinte du script). Le même programme fonctionne sur le PC du concepteur (Blender 5.3) et dans le cloud (module `bpy==5.3.0`, sans écran ni carte graphique).
- **Noms** : `tours/<faction>-<j>` pour `TW[faction × 10 + j]`, `monstres/<g>` pour le monstre de clé `CR[…].g`, `decor/<nom>`, `exemples/<nom>` (non utilisés par le jeu) ; pièces partagées dans `art/communs/`.
- **Conventions** : 1 unité = 1 case, origine au sol au centre de la case, couleurs de faction lues dans `FACTIONS` ; un seul modèle par tour et par monstre (niveaux et petites animations gérés par le jeu).
- **Budgets** (`art/budgets.json`) : tour et monstre ≤ 3 000 triangles et 150 Ko, décor ≤ 6 000 triangles et 300 Ko, total ≤ 8 Mo.
- **Contrôles** : `tests/simulation/assets3d.test.js` (chaque PR, sans Blender : manifeste complet, aucun fichier en retard sur son script, GLB valides, budgets) ; action GitHub **« Assets 3D »** (`.github/workflows/assets-3d.yml`, PR qui touchent `art/` ou `assets/3d/`) : régénère tout avec Blender 5.3, vérifie et joint les images d'aperçu.
- **Qui fait quoi** : la conception d'un nouveau modèle ou d'un nouveau style se fait de préférence sur le PC du concepteur (Blender + MCP, en direct ou via Remote Control) ; les retouches mineures peuvent être faites par n'importe quel contributeur ou une session cloud, en modifiant le script puis en régénérant.
- **Repli obligatoire** : le jeu doit fonctionner même si un modèle manque (un contributeur peut ajouter un monstre avant son modèle 3D).
- **Fins de ligne** : `.gitattributes` impose LF dans le dépôt (les empreintes vérifiées par les tests en dépendent) et traite les fichiers 3D et images comme binaires. Les fichiers `.blend` ne sont pas versionnés.

---

## Journal des modifications

| Date | Version | Modification |
|---|---|---|
| 2026-11-14 | 1.4 | Import initial du projet et création de ce document par rétro-ingénierie du code. |
| 2026-11-14 | 1.6 | Visuel uniquement : plateau-diorama avec socle et dalles surélevées, palette de biome par faction, décor déterministe (rochers, herbes, cristaux), ombres sous le portail et le château. Texte d'accueil retouché. **Aucun changement de règles ni d'équilibrage.** Le bug des racines sylvestres (§11) est toujours présent. |
| 2026-11-14 | 1.6.1 | Correction des racines sylvestres : ralentissement ×0,82 pendant 0,72 s sur toutes leurs tours (le Givre garde son propre ralentissement). Le ralentissement le plus fort l'emporte. Fin des monstres figés et des volants bloqués pour toujours. |
| 2026-11-14 | 1.7 | Technique : la simulation passe dans `sim.js` (classe `Game`, sons notés sous forme d'événements, actions via `Game.action`), en préparation du multijoueur. La fin de partie survient quand il ne reste qu'un terrain, ou plus aucun humain. **Aucun changement de règles en solo.** |
| 2026-11-14 | 2.0 | **Multijoueur en ligne** : salons de 2 à 4 humains (IA sur les places libres), code ou lien d'invitation, chef de salon, spectateurs, reconnexion. Serveur Cloudflare Workers et Durable Objects (`server/`, plan gratuit). Site publié sur GitHub Pages. |
| 2026-11-14 | 2.0.1 | Jeu en ligne **réservé à la France** (`ALLOWED_COUNTRIES`, contrôlé par le serveur), avec un message clair côté page. Le solo reste disponible partout. |
| 2026-11-14 | 2.0.1 | Organisation : nouvelle **règle des branches**. Plus de commit direct sur `main` : une branche par sujet (`<type>/<sujet>`), pull request, puis fusion par l'auteur après un test rapide (pas de relecture obligatoire). **Aucun changement de jeu.** |
| 2026-11-14 | 2.0.1 | Outillage : **déploiement automatique du serveur** par une GitHub Action (`.github/workflows/deploy-server.yml`) à chaque fusion dans `main` qui touche `sim.js` ou `server/`. Secrets `CLOUDFLARE_API_TOKEN` et `CLOUDFLARE_ACCOUNT_ID`. **Aucun changement de jeu.** |
| 2026-11-14 | 2.0.1 | Outillage : tests automatiques (`tests/`, 116 vérifications : mécaniques, 15 parties entre IA rejouées à l'identique, parcours mobile portrait et paysage), moteur 1.7 figé comme référence, captures et comparaison visuelle avant/après, trois bilans (technique, gameplay, visuel), vérification GitHub à chaque PR, procédure de validation et protection de `main` (§12, §13). **Aucune modification de `sim.js` ni d'`index.html`.** |
| 2026-11-14 | 2.0.1 | Outillage : **versions et retour arrière** (§14). Étiquette automatique à chaque fusion dans `main` (`vX.Y.Z`, ou `vX.Y.Z.N` sans changement du jeu), Releases GitHub, versions historiques 1.4 à 2.0.1 étiquetées, procédure « reviens à la version … ». **Aucun changement de jeu.** |
| 2026-11-14 | 2.0.1 | Correctif outillage : le déploiement automatique du serveur passe de Node 20 à **Node 22** (Wrangler 4 refuse Node 20 ; le premier déploiement automatique avait échoué). **Aucun changement de jeu.** |
| 2026-11-14 | 2.1 | **Interface plus claire** : fiche d'information de la tour (dégâts/s, portée, cibles, effets, bonus de faction chiffré, gain du niveau suivant), cartes de tours avec dégâts/s, portée et ✈, prix en rouge si l'or manque, monstres verrouillés avec heure de déblocage. **Zoom (1× à 3×) et déplacement à deux doigts**, molette, bouton « Vue d'ensemble », cadre de la partie visible sur la vignette. Pose au doigt au relâcher. Correction du paysage sur téléphone (haut et bas coupés). Tests navigateur complétés (19 vérifications par orientation), 5ᵉ capture (zoom). **Règles du jeu inchangées** (`sim.js` non modifié, pas de redéploiement du serveur). |
| 2026-11-14 | 2.2 | **Construction en deux touchers** : le 1er toucher montre un aperçu (tour fantôme, portée, prix), le 2e sur la même case construit ; une case impossible est signalée dès le 1er toucher ; glisser le doigt ne construit plus rien. Tests navigateur complétés (22 vérifications par orientation). **Règles du jeu inchangées** (`sim.js` non modifié). |
| 2026-11-14 | 2.3 | **Carte plus grande sur téléphone et pastilles de rôle des tours**. Carte : les 4 vignettes des joueurs quittent le HUD et s'ouvrent dans un panneau flottant par-dessus le terrain, depuis un bouton-icône en haut à gauche. Vies du joueur ajoutées dans le HUD (❤). Bannière « ↩ revenir au tien » cliquable. Mini-cartes un peu plus grandes. Tours : pastilles de rôle (flèche, épée, flocon, bombe, flamme, étoile), de cibles (sol ou sol et air) et de magie dans des cadres dorés biseautés dessinés en code ; texte des cartes « ⚔ N dégâts/s » et « ◎ portée N » ; appui long (ou survol) sur une carte pour voir sa fiche sans la sélectionner. Interface uniquement : `sim.js` inchangé. Test du parcours mobile adapté (ouvrir le panneau avant de toucher une vignette). |
| 2026-11-14 | 2.3 | Outillage : **préparation des assets 3D** (§15, `art/LISEZMOI.md`) : un script Blender par asset dans `art/`, génération identique sur PC et dans le cloud (`art/outils/generer.py`, Blender 5.3), manifeste et budgets, test de cohérence sur chaque PR, action GitHub « Assets 3D » avec aperçus, exemple `exemples/caisse`. Règle de conception n°2 adaptée aux modèles 3D générés par script. `.gitattributes` (fins de ligne LF, fichiers binaires). **Aucun changement de jeu.** |
| 2026-11-14 | 2.4 | **Temps de construction des tours** : 1 s pour 50 or dépensés, entre 0,5 et 8 s, multiplié pour les humains par ×1 / ×1,25 / ×1,5 selon la difficulté (les IA restent à ×1), à la pose comme à chaque amélioration (§4.4). Pendant le chantier, la tour ne tire pas, ne révèle pas les Spectres, ne peut pas être améliorée (`busy`) et n'est pas étourdie ; elle bloque déjà le chemin. L'IA n'améliore pas une tour en chantier. Visuel : tour en transparence, échafaudage, marteau et barre de progression ; durée affichée dans la fiche, le bouton Améliorer et le message de pose. **`sim.js` et `server/` modifiés** (redéploiement automatique du serveur). Tests de mécanique adaptés pour attendre la fin du chantier, nouveau fichier de tests `chantier`. |
| 2026-11-14 | 2.5 | **IA : labyrinthes optimisés et variés**. Plan cible par IA (formes tirées au hasard puis affinées par recherche locale, environ 100 cases de chemin une fois complet), ordre de construction qui allonge le chemin presque à chaque tour, Givre répartis le long du chemin, Mages détecteurs placés seulement quand un adversaire peut envoyer des Spectres, tours anti-aériennes sur le couloir des volants, adaptation aux volants reçus. Corrige le blocage de l'IA vers 36 tours. Génération découpée dans le temps (≈ 20 ms en tout, ≤ 2,5 ms par pas). Les transformations de l'IA respectent le temps de construction. `sim.js` modifié (redéploiement du serveur). Nouveau test `labyrinthe` ; le test « première tour de l'IA » suit désormais son plan. |
| 2026-11-14 | 2.5 | Outillage : **fin du moteur figé** (`tests/moteurs/`, `tests/references/`, `creer-references.js`, test `integrite` supprimés, y compris le moteur 2.4 figé). Les tests vérifient le bon fonctionnement sans comparer à des parties enregistrées ; le bilan gameplay compare directement au `sim.js` de `main` (statistiques et 15 parties). Plus de « gel » à faire après chaque changement de gameplay. |
