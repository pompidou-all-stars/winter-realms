# Winter Realms — Tower Wars (Édition 2.40)

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
5. **Les tests doivent passer** (`node tests/tout.js`) avant chaque commit, et chaque évolution est présentée avec ses **trois bilans** (technique, gameplay, visuel). Voir §12. **Exception** : si le bilan gameplay ne peut pas changer (documentation, règles du projet, formulaires GitHub… : ni `sim.js` ni `index.html` modifiés), pas besoin de lancer la simulation ; la vérification GitHub de la PR suffit.
6. **Chaque version a un titre très court** qui résume ce qu'elle fait, en **2 à 4 mots**, en minuscules, sans verbe ni ponctuation. Exemples : 2.23 « exploration fin de partie », 2.24 « Maj + clic », 2.20 « givre selon le niveau ». Ce titre est repris tel quel :
   - dans le commit et la PR : `Version X.Y : <titre>` ;
   - au début de la ligne du **Journal des modifications** : `**<titre>** : …` ;
   - dans le titre de la section du `README.md` : `### X.Y — <titre> — <date>`.

7. **Feuille de route** (en tête du `README.md`) : si l'évolution réalise ou commence une idée de la feuille de route, mettre à jour son statut (🛠️ en cours, ✅ fait). Les nouvelles idées arrivent par le formulaire « Idée d'amélioration » (`.github/ISSUE_TEMPLATE/idee.yml`, étiquette `idée`) ou par une ligne ajoutée au tableau.

Claude : quand tu modifies le jeu, applique cette règle sans qu'on te le demande.

## ⚠️ Règle de commits réguliers (obligatoire)

On commite **souvent, par petites étapes**, pour que tout le monde suive l'avancement :

1. **Un commit par amélioration** (une nouvelle tour, un monstre, une retouche d'équilibrage, un correctif, une évolution visuelle…). On ne mélange pas plusieurs sujets dans un même commit.
2. Chaque commit contient **à la fois** le changement dans `index.html` **et** la mise à jour de `CLAUDE.md`.
3. **Nouvelle version reçue** (fichier HTML partagé par un membre du groupe) : créer une branche, y copier le fichier dans `index.html`, lire le diff (`git diff`), mettre à jour `CLAUDE.md`, puis faire un commit nommé `Version X.Y : <titre>` (titre court de la version, voir la règle de maintenance n°6).
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
  - **Toutes les actions du joueur passent par `doAction()`**, qui appelle `Game.action()`. Cette fonction renvoie `''` si l'action réussit, sinon un code d'erreur : `poor`, `blocked`, `unique` (deuxième tour ultime, depuis la 2.40), `locked`, `max`, `busy` (tour en chantier, depuis la 2.4), `early` (envoi pendant la phase « Construis », depuis la 2.30), `over` ou `bad`.
- **Autour du jeu** (ces dossiers ne sont pas chargés par la page) :
  - `server/` : le serveur multijoueur (Cloudflare Workers), qui importe `sim.js` tel quel (voir §9 bis) ;
  - `tests/` : les tests automatiques, les captures et les bilans (voir §12) ;
  - `art/` : les **recettes des modèles 3D** (un script Blender par asset) et l'outil de génération ; `assets/3d/` : les fichiers 3D produits (GLB) et leur manifeste (voir §15 et `art/LISEZMOI.md`) ;
  - `.github/` : la vérification automatique des Pull Requests (`tests.yml`), le déploiement automatique du serveur (`deploy-server.yml`, voir §9 bis), l'étiquetage automatique des versions (`versions.yml` et `versionner.sh`, voir §14), la régénération des assets 3D (`assets-3d.yml`, voir §15) et le modèle de description de PR.
- **Pour jouer en local**, il faut un petit serveur web : `npx http-server` à la racine, puis ouvrir http://localhost:8080. Un `file://` ne charge pas toujours `sim.js`, surtout dans les aperçus intégrés. **Pour tester**, voir §12 : `node tests/tout.js`.
- **Seule ressource externe** : la police Google Fonts *Fredoka*. three.js est **copié dans le dépôt** (`vendor/three/`, r170, licence MIT) et n'est chargé qu'en mode 3D.
- **Rendu 3D (depuis la 2.7, par défaut depuis la 2.8)** : l'adresse normale du jeu ouvre la 3D (module `rendu3d.js`, three.js, modèles de `assets/3d/`). Le rendu 2D en Canvas reste disponible avec `?rendu=2d` dans l'adresse, sans lien sur l'accueil depuis la 2.22 : il sert de **secours** (WebGL absent ou 3D qui ne se charge pas). Depuis la 2.29, les tests, les captures et le bilan visuel se font en 3D, comme le jeu ; un test vérifie que le secours 2D reste jouable. Si WebGL manque, le jeu revient en 2D avec un message. Voir §15.2.
- **Rendu** : Canvas 2D. Tous les visuels (tours, monstres, effets) sont **dessinés en code**, sans images. La netteté s'adapte à l'écran (`devicePixelRatio`, plafonné à 3).
- **Vue du terrain** (depuis la 2.1 ; refaite en 2.15) : le canevas `#main` couvre tout l'écran, et le bandeau et le dock flottent par-dessus (`bandes()` donne les hauteurs qu'ils couvrent). En 3D, la caméra tactique de `rendu3d.js` fait le passage écran ↔ case (`projeter`, `sol`, voir §15.2). En 2D, le plateau entier est dessiné par `dessinerVue()` entre le bandeau et le dock, avec un décalage (`VUE.ox`, `VUE.oy`), sans zoom. `caseVersEcran(x, y)` donne la position d'une case à l'écran et `caseSous` la case sous un point (elles servent aussi aux tests).
- **Sons** (depuis la 2.17 ; générés avec ElevenLabs depuis la 2.29) : **bibliothèque sonore en fichiers MP3** (`assets/audio/`, moteur `audio.js`, §16) : tirs des tours par faction, construction, cris et morts des monstres, cors d'envoi, interface, ambiances et **répliques vocales des 5 factions**, générés par le script versionné `art/outils/generer-sons.js` à partir de `assets/audio/catalogue.json`. Les sons synthétisés avec Web Audio (oscillateurs et bruit) restent le **secours** quand un fichier manque. **Musique de fond** (2.16) : trois fichiers MP3 dans `assets/musique/` (§9, objet `MUSIQUE`).
- **Pas de sauvegarde** : aucun `localStorage`. Chaque partie repart de zéro.
- **Style de code** : JavaScript compact, presque minifié (noms courts, une logique par ligne). Les **tables de données sont en tête de `sim.js`** et c'est là qu'on règle l'équilibrage :
  | Constante | Rôle |
  |---|---|
  | `C`, `R`, `SP`, `EX` | Taille de la grille, case d'apparition, case de sortie |
  | `BASE_TW` | Les 6 archétypes de dessin (2D et repli 3D) |
  | `RACES` (alias `FACTIONS`) | Les 5 races (depuis la 2.40) : nom, icône, couleurs, histoire, mécanique, états, forces et faiblesses, profil `radar`, combos, version renforcée pour l'IA (`up`) et **les 10 tours écrites une par une** (§5) |
  | `ROLES_J`, `REGLES` | Les 10 rôles des emplacements (§4.2) ; règles d'équilibrage (radar, §5.3) |
  | `AMP_MAX`, `SF_MIN`, `DOSE_MAX`, `IM_IMMU`, `BRISE`, `COH`, `FUREUR`, `CROIT`, `AMES_MAX`, `FORGE` | Plafonds et mécaniques des races (§5) |
  | `TW` | Les 50 tours, construites à partir de `RACES` (`estimer` ajoute `ed`, `dot`, `zf`) |
  | `CR` | Les monstres |
  | `DIFF` | Les niveaux de difficulté |
  | `HPK`, `GRACE`, `GROUP`, `AURA_R` | Constantes de gameplay |
  | `PAL_C`, `ACC`, `ACC_MAX` | Prix des paliers de monstres et vitesse des monstres accélérés (§6, depuis la 2.13) |
  | `BUILD_OR`, `BUILD_MIN`, `BUILD_MAX`, `BUILD_DIFF` | Temps de construction : 1 s par `BUILD_OR` pièces d'or, borné, multiplié selon la difficulté pour les humains (§4.4) |
  | `QUETES`, `QU_T0`, `QU_PAUSE`, `QU_JOUE`, `QU_PLACE` | Quêtes bonus : les 10 quêtes, moment de la première, pause entre deux, part des IA qui les jouent, place minimale pour « Clicker fou » (§2, depuis la 2.38) |
- **Sections de `sim.js`** : tables de données → simulation (`class Board`) → IA (`aiDefend`, `aiAttack`, `aiAct`) → partie (`class Game`).
- **Sections du script de `index.html`** : sons → dessin → interface (dont le multijoueur, objet `NET`) → sons et événements → boucle principale (`loop`).
- **Langue** : toute l'interface est en **français**.
- **Mobile d'abord** : commandes tactiles, zones sûres (`safe-area-inset`), plein écran. **Portrait seulement depuis la 2.15** : un téléphone en paysage affiche « Tourne ton téléphone » ; sur ordinateur, le jeu tient dans une colonne au format portrait (§9).

---

## 2. Déroulement d'une partie

1. **Écran d'accueil** : on choisit une **race** (5 au choix, §5), on peut lire sa **fiche** (Description, Tours, Combos), puis une **difficulté** (Normal, Difficile ou Brutal). Le Royaume d'Aubeval est présélectionné.
2. **Les 4 terrains** : celui du joueur (« Toi ») et ceux de IA 1 (rouge), IA 2 (bleu) et IA 3 (violet). Les IA jouent automatiquement les factions suivantes dans la liste : `(faction du joueur + 1, + 2, + 3) % 5`.
3. **Victoire** : toutes les IA sont éliminées. **Défaite** : le joueur est éliminé. Une fenêtre de fin donne alors les statistiques et propose de regarder la carte ou de quitter (§9, depuis la 2.23).
4. Un joueur est **éliminé** quand ses vies tombent à 0. Son terrain est alors vidé et grisé, et il ne reçoit plus de vagues.
5. **Départ façon jeu de course** (depuis la 2.30) : les **30 premières secondes** (`GRACE`, `sim.js`) sont la phase « Construis » : **personne, humain ou IA, ne peut envoyer de monstres** (`Game.send` refuse, `Game.action` renvoie `early`). On ne fait que construire. Voir §9 pour les annonces et le chrono.

### Ressources de départ (pour chaque terrain)
| Ressource | Valeur |
|---|---|
| Or | 200 (doublé depuis la 2.30 ; avant : 100) |
| Revenu | +10 toutes les 10 s |
| Vies | 40 |

### Économie
- **Revenu** : versé toutes les **10 secondes**. Une barre dorée sous le HUD montre le temps restant.
- **Envoyer un monstre** fait **augmenter définitivement le revenu** (voir la colonne « +revenu » plus bas). C'est le cœur de la stratégie : attaquer, c'est aussi investir.
- **Prime par monstre tué** : `max(1, arrondi(coût / 10))` en or, gagnée par le terrain sur lequel le monstre meurt.
- **Revente d'une tour** : 70 % de l'or investi (achat et améliorations), arrondi à l'inférieur.

### Quêtes bonus (depuis la 2.38)
Des défis courts au titre volontairement décalé, choix du concepteur : **drôles** et sources de fun. Familles retenues : construction, attaque, économie (pas de quête de défense).
- **Rythme** : une quête à la fois. La première commence à **1:30** (`QU_T0`), la suivante **3 à 4 min** après la fin de la précédente (`QU_PAUSE` + 0 à 60 s, au hasard). Tirage au hasard **sans remise** : les 10 quêtes passent avant qu'une revienne. Il faut au moins 2 joueurs en jeu.
- **Deux formes** : **course** (le premier qui atteint la cible gagne, la quête s'arrête aussitôt ; sinon, personne au bout de sa durée) et **photo** (au bout du chrono, le meilleur score gagne).
- **Aucune course n'est déjà gagnée au lancement** : elle se compte depuis son début (Clicker fou, Facteur, Gros cadeau) ou vise au-dessus du meilleur du moment (Gonflette, Frozen).
- **Récompense** : de l'or, `max(100, 8 × revenu moyen des joueurs en jeu)` arrondi à la dizaine (`quOr`), donc environ 1 min 20 de revenu ; annoncée au lancement. Une égalité partage l'or ; un score nul ne gagne pas une photo (sauf Mamie Gâteau).

| Quête | Forme | Durée | Règle |
|---|---|---|---|
| Qui a la plus grosse ? | photo | 75 s | le plus long labyrinthe (chemin du portail au château) |
| Clicker fou | course | 90 s | le premier qui pose **10 tours** de plus. **Pas tirée en fin de partie** : chaque joueur en jeu doit avoir encore au moins 20 cases où une tour est posable sans fermer le chemin (`posables`, `QU_PLACE`) |
| Picsou | photo | 60 s | le plus d'or en banque |
| Le facteur sonne toujours 4 fois | course | 120 s | le premier qui fait passer **4 de ses monstres** chez ses adversaires (tous confondus). Chaque monstre retient son envoyeur (`c.o`, donné par `Board.send(k, m, o)` ; les petits d'une division en héritent) ; à sa sortie, `st.passe` de l'envoyeur augmente |
| Gonflette | course | 120 s | le premier qui monte une tour (chantier fini) au niveau N = 1 de plus que la meilleure tour du moment, au moins 3 ; pas tirée si N dépasserait 5 |
| Frozen | course | 120 s | le premier qui a N tours de **contrôle** (emplacement 2 de sa race, `ctl`, depuis la 2.40 ; avant : le Givre), N = le plus grand nombre de tours de contrôle d'un joueur au lancement + 2 (avant 5 min), + 3 (avant 10 min), + 4 ensuite |
| Le gros cadeau | course | 150 s | le premier qui envoie un boss (à partir de 3:00) |
| Pigeons voyageurs | photo | 60 s | le plus d'or envoyé en volants |
| Bling-bling | photo | 60 s | la tour la plus chère (or investi) |
| Mamie Gâteau | photo | 60 s | le **plus petit** revenu gagne : un coup de pouce au joueur en retard |

- Journal de partie : `{type:'quete', ph:'debut', id, or, cible, fin}` puis `{type:'quete', ph:'fin', id, g:[gagnants], or}` (or par gagnant). Statistiques `Board.st` : `passe`, `boss`, `vol`, `qu` (quêtes gagnées), `quOr`.

---

## 3. Le terrain

- Grille de **13 × 17 cases**. Les monstres apparaissent en **(6, 0)**, en haut au centre, et visent la sortie (un château) en **(6, 16)**, en bas au centre.
- **Monstres au sol** (déplacement en diagonale depuis la 2.25) : ils suivent le **plus court chemin** vers la sortie, **en ligne droite et à n'importe quel angle** (du coin haut gauche au coin bas droit, ils suivent la diagonale).
  - **Distances** (`Board.dist`, recalculées à chaque pose ou vente) : Dijkstra sur **8 directions**, diagonale de longueur √2, **sans couper le coin d'une tour** (une diagonale exige que les deux cases voisines soient libres).
  - **Cible** (`Board.viser`) : le monstre regarde la suite de cases vers la sortie (`chaine`, 16 cases au plus, `VUE_MAX`) et vise **la plus lointaine qu'il peut rejoindre en ligne droite** en restant à **0,3 case** des tours (`MR`, test exact segment-carré `vue`). Il revoit sa cible en l'atteignant, **toutes les 0,25 s** (pour couper au plus court après un virage) et après chaque pose ou vente (`revoir`).
  - **Espacement** (`Board.ecarter`) : deux monstres à moins de **0,75 case** (`ESP` ; au sol entre eux, volants entre eux) se poussent **sur le côté seulement**, perpendiculairement à leur marche, au plus **1,5 case/s** (`ESP_V`). Personne n'est freiné ni repoussé en arrière, donc **aucun bouchon possible** : le temps de trajet ne change pas. Un monstre qui en suit un autre dans la même file part d'un côté choisi selon son numéro. Au sol, le pas de côté est refusé s'il approcherait une tour à moins de `MR`. Dans un couloir d'une case, ils restent donc presque en file.
  - Le chemin actuel est affiché en pointillés animés : `chemin(b)` fait parcourir le terrain à un monstre fantôme avec les mêmes règles et garde ses points de virage (en cache tant que `b.d` ne change pas).
  - L'IA planifie ses labyrinthes avec les mêmes règles (8 directions, sans couper les coins, §8).
- **Monstres volants** : ils vont **en ligne droite** vers la sortie et ignorent les tours posées sur leur trajet.
- **On ne peut pas poser une tour** :
  - sur la case d'apparition ou de sortie ;
  - si elle **bloquerait complètement** le chemin, ou couperait le passage d'un monstre déjà en route ;
  - à moins de 0,9 case d'un monstre au sol (sur chaque axe), ou si la case d'un monstre au sol ne mènerait plus à la sortie (`genant`, partagé avec le contrôle de la page). Depuis la 2.25, on peut poser devant un monstre : il change alors de cible.
- Chaque monstre qui atteint la sortie retire **1 vie**.

---

## 4. Les tours

### 4.1 Les 6 archétypes (`BASE_TW`)
| Archétype | Coût | Portée | Dégâts | Recharge | Particularités |
|---|---|---|---|---|---|
| Archer | 20 | 2,8 | 8 | 0,5 s | Tir simple, touche le sol et les airs |
| Canon | 50 | 2,5 | 20 | 1,2 s | Explosion de rayon 1,1 (60 % des dégâts autour, sans limite de cibles), **sol uniquement** |
| Givre | 40 | 2,5 | 2 | 0,9 s | Explosion de rayon 1,2 à 2 selon le niveau, **ralentit** (voir plus bas), **magique**. Dégâts 4 → 2 en 2.31 |
| Mage | 90 | 3,2 | 55 | 1,4 s | **Magique**, **détecte les invisibles** dans sa portée. Dégâts 45 → 55 en 2.31 |
| Garde | 30 | 1,5 | 20 | 0,55 s | Corps à corps (frappe directe), **sol uniquement** |
| Flammes | 70 | 2,0 | 3 | 0,12 s | Cône d'environ ±29°, plus tout ce qui est à moins de 0,6 case ; touche les airs |

- **Depuis la 2.40, ces archétypes ne servent plus qu'au dessin** (2D et repli 3D, champ `skin`) : les 50 tours sont définies une par une dans `RACES` (§5). Seul le froid garde la table `GIVRE_LV`.
- Les tours **magiques** (`mag`) **n'ont aucun effet sur le Briseur de runes** ; chaque race en a au moins 2 qui ne le sont pas.
- **Ciblage** : chaque tour vise, dans sa portée, le monstre visible **le plus proche de la sortie** (le Tireur des cimes vise le plus résistant, `vise:'pv'`). `cible(T, c)` dit si une tour peut toucher un monstre (sol, air, air seulement `ao`, anti-magie) ; un volant **abattu** (filet) compte comme au sol (`vole`).
- **Froid** (table `GIVRE_LV`, Totem des pluies glacées de l'Orage Blanc) : la force, la durée et la zone dépendent du **niveau de la tour** qui frappe.
  | Niveau | 1 | 2 | 3 | 4 | 5 |
  |---|---|---|---|---|---|
  | Vitesse retirée | 20 % | 27,5 % | 35 % | 42,5 % | 50 % |
  | Durée | 1,5 s | 1,8 s | 2,1 s | 2,4 s | 2,7 s |
  | Rayon de l'explosion | 1,2 | 1,4 | 1,6 | 1,8 | 2 |
  - Deux familles de ralentissement restent dans le moteur (froid `gp`/`gt`, racines `rp`/`rt`, table `RACINES_LV`, plus utilisée par une tour depuis la 2.40) : elles s'additionnent, mais **la vitesse ne descend jamais sous ×0,3** (`SF_MIN`, règle d'or n°1). Dans une même famille, pas de cumul : l'effet le plus fort et la durée la plus longue l'emportent.
  - **Immobilisation** (`im` : filets, racines, chocs, squelettes) : vitesse 0 pendant la durée (+10 % par niveau), **moitié pour un boss**, puis le monstre est **immunisé** 1,5 fois cette durée (`IM_IMMU`, rendement décroissant).
  - **Maléfice** (`hx`) : vitesse ×0,6 et armure 0 pendant 1,5 s, jamais sur un boss, puis immunité.

### 4.2 Les 10 rôles (`ROLES_J`, depuis la 2.40)
Chaque race a 10 tours **différentes** ; l'emplacement `j` fixe le **rôle** (la grille de couverture commune), pas l'archétype. L'IA s'appuie sur ces rôles (§8).

| j | Rôle | Palier | Ce que la race doit y mettre |
|---|---|---|---|
| 0 | Base | I (≤ 25 or) | tour bon marché qui touche **le sol et les airs** |
| 1 | Proximité | I | corps à corps ou impulsion autour d'elle, au sol |
| 2 | Contrôle | I | effet sur le chemin (filet, froid, racines, armure brisée, malédiction) ; compte pour la quête « Frozen » (`ctl`) |
| 3 | Zone | II | dégâts de zone |
| 4 | Anti-aérien | II | **dédié aux volants** (dégâts ×2 en l'air ou air seulement) |
| 5 | Détection | II-III (≤ 120 or) | **révèle les invisibles** (`det`) |
| 6 | Signature | III | la tour qui incarne la race (économie, chaîne d'éclairs, Floraison, Chauffe, morts relevés) |
| 7 | Soutien | III | aura sur les 8 cases voisines (`au` : cadence, dégâts, portée, doses, Fureur, Croissance, âmes), ne tire pas |
| 8 | Anti-boss | III | contre les blindés et les boss |
| 9 | Ultime | IV | **une seule par terrain** (`u`, code d'erreur `unique`) |

### 4.3 Améliorations
- **5 niveaux** au maximum. Les points jaunes au pied de la tour indiquent son niveau.
- Coût pour passer au niveau suivant : `arrondi(coût × 1,5 × 2^(niveau−1) / 5) × 5`.
- **Les dégâts doublent à chaque niveau** (`dégâts × 2^(niveau−1)`).
- La portée augmente de **5 % par niveau**.
- **Forge** (Nains de Hautroc, depuis la 2.40) : améliorations **15 % moins chères**, donc aussi plus courtes (`FORGE`).
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

## 5. Les races (depuis la 2.40)

Depuis la 2.40, les 5 factions sont devenues des **races asymétriques** (table `RACES` de `sim.js`, alias `FACTIONS`) : chacune a sa **mécanique propre**, ses **états**, ses **combos** et **10 tours toutes différentes**. Les anciens coefficients (`FACTION_BALANCE`) et le calcul automatique des tours ont disparu : chaque tour est écrite à la main dans `RACES[f].tours`, puis complétée par `estimer` (dégâts par seconde estimés `ed`, part dans la durée `dot`, facteur de zone `zf`).
Les noms ne reprennent aucun univers existant (l'Alliance et la Horde étaient trop proches d'un jeu connu). **10 races sont prévues à terme** (idées : Géants du givre, Gobelins ferrailleurs, Fées des aurores, Draconides, Ordre céleste) : chacune suivra les règles du §5.3.

Chaque race garde son style visuel de terrain (socle, couleur du sol, palette). **Modèles 3D** : en attendant leur refonte (§15.1), chaque tour utilise le modèle de son emplacement dans l'ancienne faction (`tours/<faction>-<j>`).

### 5.1 Mécaniques communes
- **États** (champs des monstres, décomptés à chaque pas ; `etats(c)` les donne en bits pour l'affichage et le serveur) : Marqué `mk`, Maudit `ma`, immobilisé `im`, Maléfice `hx`, Abattu `ab`, Trempé `tw`, poison `pz` (doses) / `pd` / `pt`, saignement `sg`, Brisé `bs`, Brûlant `bu`, Pestiféré `pe`.
- **Dégâts dans la durée** (poison, saignement, brûlure, peste) : ils **ignorent l'armure**. Poison : jusqu'à **10 doses** (`DOSE_MAX`), chacune fait `pv × (1 + niveau − 1)` dégâts par seconde, rafraîchies 4 s ; deux fois plus vite sur un monstre immobilisé (Terreau).
- **Amplification** : Marqué +15 %, Maudit +20 %, cumul plafonné à **+60 %** (`AMP_MAX`).
- **Armure brisée** : −15 % d'armure par point (`BRISE`), jusqu'à 5 points.
- **Auras** : une tour de soutien agit sur les **8 cases voisines** ; ses bonus montent de 20 % par niveau. Les bonus des tours (`xd` dégâts, `xr` portée, `xc` cadence) sont recalculés tous les 0,25 s (`Board.bonus`).
- **Combos** : un texte flottant nommé (« JUGEMENT ! », « FLORAISON ! »…), au plus un par demi-seconde et par monstre, et le même combo au plus toutes les 0,4 s sur un terrain.
- **Economie** : le Comptoir marchand verse son or avec le revenu (`eco(b)`), sans augmenter le revenu affiché.

### 5.2 Les 5 races
Recharge en secondes, portée en cases. DPS = dégâts ÷ recharge du tir direct, sans poison, zone, chaîne ni bonus (les tours qui ne tirent pas valent 0).

#### Royaume d’Aubeval
👑 *Ordre, foi et ingénierie de siège : la race la plus polyvalente, la seule à avoir une économie.* (ex-Alliance)

- **Mécanique propre — Cohésion** : Chaque tour d’Aubeval voisine donne +4 % de dégâts (jusqu’à +16 %). Les murs serrés du labyrinthe deviennent plus forts.
- **États** : Marqué : +15 % de dégâts subis ; l’Inquisiteur et le Rayon de l’Aube font détoner le sceau ; Abattu : un volant tombe au sol 2 s, les tours « sol » peuvent le frapper.
- **Forces** : polyvalence, économie, anti-boss. **Faiblesses** : zone moyenne, peu de contrôle.
- **Profil** (Mono-cible, Zone, Anti-air, Anti-blindé, Contrôle, Économie) : 6 / 4 / 6 / 7 / 3 / 4.
- **Combos** :
  - **Jugement** (Chapelle du guet + Inquisiteur) : La Chapelle du guet marque un monstre ; l’Inquisiteur (ou le Rayon de l’Aube) fait détoner le sceau : +60 % sur ce coup.
  - **Chute** (Lance-filets + Trébuchet) : Le Lance-filets abat un volant ; le Trébuchet l’écrase au sol : dégâts ×1,5.
  - **Formation** (Étendard royal + Tour d’arbalétriers) : Autour de l’Étendard royal, chaque voisin compte double pour la Cohésion : jusqu’à +32 % de dégâts.
- **IA, version renforcée** (`up`) : Tour d’arbalétriers → Inquisiteur.

| # | Tour | Rôle | Coût | Dégâts | Recharge | DPS | Portée | Effet |
|---|---|---|---|---|---|---|---|---|
| 0 | Tour d’arbalétriers | Base | 20 | 8 | 0,5 | 16 | 2,9 | Carreaux réguliers, au sol et dans les airs. La base, solide et bon marché. |
| 1 | Poste de hallebardiers | Proximité | 30 | 16 | 0,6 | 27 | 1,5 | Corps à corps : chaque balayage frappe 2 monstres à la fois. |
| 2 | Lance-filets | Contrôle | 45 | 3 | 2,2 | 1 | 2,6 | Lance un filet : le monstre est immobilisé 0,8 s. Un volant est abattu au sol pendant 2 s. |
| 3 | Trébuchet | Zone | 65 | 34 | 2,4 | 14 | 3,6 | Très longue portée et grosse explosion, au sol. Ne tire pas à moins de 1,5 case. |
| 4 | Baliste céleste | Anti-aérien | 60 | 22 | 1,3 | 17 | 3,3 | Carreau qui traverse tout sur sa ligne. Dégâts ×2 contre les volants, ×0,5 au sol. |
| 5 | Chapelle du guet | Détection | 80 | 14 | 1 | 14 | 3 | Révèle les invisibles et pose le sceau du Jugement (Marqué : +15 % de dégâts subis pendant 3 s). |
| 6 | Comptoir marchand | Signature | 100 | 0 | 1 | 0 | 2,5 | Ne tire pas. +5 or toutes les 10 s par niveau, et +20 % de prime sur les monstres tués à sa portée. |
| 7 | Étendard royal | Soutien | 90 | 0 | 1 | 0 | 1,5 | Ne tire pas. Tours voisines : +15 % de cadence, et la Cohésion compte double autour de lui. |
| 8 | Inquisiteur | Anti-boss | 140 | 48 | 1,3 | 37 | 3 | Ignore l’armure. Dégâts ×2 contre les monstres spéciaux et les boss. Fait détoner le sceau des Marqués. |
| 9 | Rayon de l’Aube | Ultime | 260 | 14 | 0,25 | 56 | 3,4 | Ultime, une seule par terrain. Rayon continu : +25 % à chaque tir sur la même cible, jusqu’à ×4. |

#### Clans de l’Orage Blanc
⚡ *Chamanes des steppes gelées : totems, tambours, foudre en chaîne et rage.* (ex-Horde)

- **Mécanique propre — Fureur** : Chaque monstre tué par une tour lui donne 1 charge de Fureur (+3 % de cadence, jusqu’à 10). Une charge se perd toutes les 2 s sans victoire. À 10 charges : Rage, +30 % de dégâts pendant 3 s.
- **États** : Trempé : −20 % de vitesse ; les éclairs rebondissent deux fois plus ; Maléfice : le monstre devient un crapaud 1,5 s (armure 0, vitesse ×0,6), jamais sur un boss ; Saignement : perd 1,5 % de ses PV max par seconde.
- **Forces** : zone en chaîne, foules, anti-aérien. **Faiblesses** : monstres isolés et blindés, boss.
- **Profil** (Mono-cible, Zone, Anti-air, Anti-blindé, Contrôle, Économie) : 3 / 8 / 6 / 3 / 5 / 5.
- **Combos** :
  - **Conduction** (Totem des pluies glacées + Totem de foudre) : Le Totem des pluies glacées trempe les monstres ; l’éclair du Totem de foudre rebondit deux fois plus sur un Trempé.
  - **Rage du clan** (Grands tambours de guerre + Hutte du berserker) : Les Grands tambours doublent la Fureur gagnée : la Hutte du berserker atteint vite 10 charges et entre en Rage.
  - **Crapaud saignant** (Hutte du chaman des esprits + Totem de sang) : Le Maléfice retire l’armure ; le Totem de sang fait saigner le crapaud sans rien perdre.
- **IA, version renforcée** (`up`) : Lanceurs de haches → Totem de foudre, Hutte du berserker → Totem de sang.

| # | Tour | Rôle | Coût | Dégâts | Recharge | DPS | Portée | Effet |
|---|---|---|---|---|---|---|---|---|
| 0 | Lanceurs de haches | Base | 20 | 8,5 | 0,5 | 17 | 2,6 | Haches lancées au sol et dans les airs. Gagne vite de la Fureur. |
| 1 | Hutte du berserker | Proximité | 30 | 19 | 0,55 | 35 | 1,5 | Corps à corps. Sa Fureur monte deux fois plus vite. |
| 2 | Totem des pluies glacées | Contrôle | 40 | 2 | 1 | 2 | 2,5 | Pluie glacée en zone : ralentit et trempe les monstres (les éclairs rebondissent deux fois plus). |
| 3 | Catapulte à rochers | Zone | 55 | 21 | 1,3 | 16 | 2,7 | Rocher en zone, au sol, qui étourdit 0,3 s. |
| 4 | Aire des aigles-tempête | Anti-aérien | 60 | 16 | 0,8 | 20 | 3 | L’aigle plonge et son éclair rebondit sur 2 autres cibles. Dégâts ×2 contre les volants. |
| 5 | Hutte du chaman des esprits | Détection | 85 | 26 | 1,4 | 19 | 3,1 | Révèle les invisibles. Maléfice : change le monstre en crapaud 1,5 s (armure 0, vitesse ×0,6). |
| 6 | Totem de foudre | Signature | 75 | 18 | 1,1 | 16 | 2,8 | Chaîne d’éclairs : 3 rebonds, −25 % par rebond. Deux fois plus de rebonds sur un Trempé. |
| 7 | Grands tambours de guerre | Soutien | 90 | 0 | 1 | 0 | 1,5 | Ne tire pas. Tours voisines : +20 % de cadence et Fureur gagnée doublée. |
| 8 | Totem de sang | Anti-boss | 120 | 6 | 1 | 6 | 2,6 | Saignement : la cible perd 1,5 % de ses PV max par seconde pendant 3 s. L’arme des clans contre les géants. |
| 9 | Cœur de l’Orage | Ultime | 280 | 90 | 4 | 23 | 4 | Ultime, une seule par terrain. Toutes les 4 s, 6 éclairs tombent à sa portée ; chaque victime donne +1 Fureur à toutes tes tours. |

#### Elfes de Lunebois
🌿 *La forêt vivante, le venin et la patience : poison, racines et tours qui grandissent.* (ex-Sylvestres)

- **Mécanique propre — Croissance** : Chaque tour gagne +1 % de dégâts et de portée toutes les 10 s sur place, jusqu’à +25 %. La vendre lui fait perdre ce bonus.
- **États** : Empoisonné : jusqu’à 10 doses, chacune inflige des dégâts par seconde qui ignorent l’armure ; Enraciné : le monstre ne bouge plus (moitié moins longtemps pour un boss).
- **Forces** : blindés, contrôle, contagion. **Faiblesses** : démarrage lent, monstres rapides.
- **Profil** (Mono-cible, Zone, Anti-air, Anti-blindé, Contrôle, Économie) : 4 / 5 / 5 / 6 / 7 / 3.
- **Combos** :
  - **Floraison** (Archers sylvains + Cercle de Floraison) : Les flèches et la Fleur de venin empilent le poison ; le Cercle de Floraison fait éclore toutes les doses d’un coup.
  - **Terreau** (Gardien enracineur + Fleur de venin) : Sur un monstre enraciné par le Gardien, le poison de la Fleur de venin agit deux fois plus vite.
  - **Spores** (Fleur de venin + Archers sylvains) : Un monstre qui meurt avec 5 doses ou plus éclate en spores et empoisonne ses voisins.
- **IA, version renforcée** (`up`) : Archers sylvains → Tireur des cimes, Fleur de venin → Cercle de Floraison.

| # | Tour | Rôle | Coût | Dégâts | Recharge | DPS | Portée | Effet |
|---|---|---|---|---|---|---|---|---|
| 0 | Archers sylvains | Base | 20 | 5,4 | 0,5 | 11 | 2,8 | Flèches au sol et dans les airs ; chacune ajoute 1 dose de poison. |
| 1 | Haie de ronces | Proximité | 25 | 4,5 | 0,5 | 9 | 1,3 | Épines : blesse et empoisonne tout ce qui passe à côté, au sol. |
| 2 | Gardien enracineur | Contrôle | 45 | 5,4 | 4 | 1 | 2,2 | Toutes les 4 s, des racines immobilisent 1 s tous les monstres au sol à sa portée. |
| 3 | Fleur de venin | Zone | 55 | 4 | 1 | 4 | 2,4 | Nuage de venin en zone, au sol et dans les airs : 2 doses de poison. |
| 4 | Nid des chouettes des neiges | Anti-aérien | 55 | 10,8 | 0,7 | 15 | 3,1 | Les chouettes chassent les volants (dégâts ×2) et les empoisonnent. |
| 5 | Puits de lune | Détection | 80 | 19,8 | 1,3 | 15 | 3,2 | Révèle les invisibles. Les tours voisines grandissent deux fois plus vite. |
| 6 | Cercle de Floraison | Signature | 90 | 9 | 1,6 | 6 | 2,8 | Fait éclore le poison : toutes les doses de la cible explosent d’un coup. |
| 7 | Bosquet ancien | Soutien | 85 | 0 | 1 | 0 | 1,5 | Ne tire pas. Tours voisines : +12 % de portée et +1 dose de poison par coup. |
| 8 | Tireur des cimes | Anti-boss | 130 | 54 | 1,8 | 30 | 4,4 | Très longue portée, vise le monstre le plus résistant. Dégâts ×1,5 sur un enraciné. |
| 9 | Arbre-Mère | Ultime | 250 | 36 | 10 | 4 | 3,6 | Ultime, une seule par terrain. Toutes les 10 s, enracine tout à sa portée ; toutes tes tours grandissent trois fois plus vite. |

#### Nains de Hautroc
⚒️ *Forge, runes et artillerie lourde : la race de l’armure brisée et de la chauffe.* (ex-Nains)

- **Mécanique propre — Forge et Chauffe** : Améliorations 15 % moins chères et plus rapides ; étourdissements subis deux fois plus courts. Les tours à tir continu chauffent (+50 % de dégâts au maximum) mais s’arrêtent 2 s en surchauffe, sauf à côté d’une Enclume runique.
- **États** : Brisé : −12 % d’armure par point, jusqu’à 5 points ; Brûlant : dégâts par seconde.
- **Forces** : blindés, boss, artillerie au sol. **Faiblesses** : volants hors de la tour dédiée, aucun ralentissement.
- **Profil** (Mono-cible, Zone, Anti-air, Anti-blindé, Contrôle, Économie) : 6 / 6 / 4 / 8 / 3 / 3.
- **Combos** :
  - **Brèche** (Baliste perce-plaque + Mortier runique) : La Baliste perce-plaque brise l’armure ; à 5 points, le Mortier runique (et Grondeterre) font +40 %.
  - **Fusion** (Gueule de forge + Marteau-pilon) : Un monstre Brûlant frappé par le Marteau-pilon perd 2 points d’armure de plus.
  - **Forge froide** (Enclume runique + Arbalète à répétition) : À côté de l’Enclume runique, l’Arbalète à répétition et la Gueule de forge ne surchauffent plus.
- **IA, version renforcée** (`up`) : Marteau-pilon → Gueule de forge, Mortier runique → Champ de mines.

| # | Tour | Rôle | Coût | Dégâts | Recharge | DPS | Portée | Effet |
|---|---|---|---|---|---|---|---|---|
| 0 | Arbalète à répétition | Base | 20 | 5,6 | 0,3 | 19 | 2,7 | Tir très rapide au sol et dans les airs, qui monte en Chauffe. |
| 1 | Marteau-pilon | Proximité | 35 | 25 | 0,9 | 28 | 1,4 | Onde de choc autour de lui, au sol, qui sonne les monstres 0,2 s. |
| 2 | Baliste perce-plaque | Contrôle | 45 | 17,5 | 0,8 | 22 | 2,9 | Brise l’armure : −12 % par coup, jusqu’à 5 points. |
| 3 | Mortier runique | Zone | 60 | 32,5 | 1,6 | 20 | 3,4 | Obus runique en zone, longue portée, au sol. |
| 4 | Canon antiaérien à éclats | Anti-aérien | 60 | 23,8 | 0,6 | 40 | 3,2 | Ne vise que les volants : éclats qui explosent en l’air. |
| 5 | Phare runique | Détection | 75 | 15 | 1 | 15 | 3,6 | Rayon runique. Révèle les invisibles et brise d’un point l’armure de tout ce qui passe dans sa lumière. |
| 6 | Gueule de forge | Signature | 70 | 4 | 0,12 | 33 | 2 | Souffle de flammes en cône qui rend les monstres Brûlants, et monte en Chauffe. |
| 7 | Enclume runique | Soutien | 90 | 0 | 1 | 0 | 1,5 | Ne tire pas. Tours voisines : +15 % de dégâts, et elles ne surchauffent plus. |
| 8 | Champ de mines | Anti-boss | 110 | 68,8 | 2,5 | 28 | 2,2 | Pose jusqu’à 4 mines runiques sur le chemin à sa portée ; elles explosent au passage. |
| 9 | Grondeterre | Ultime | 280 | 275 | 6 | 46 | 5 | Ultime, une seule par terrain. Canon de siège : toutes les 6 s, un tir en ligne qui traverse tout et ignore l’armure. |

#### Cour des Ossements
☠️ *Nécromancie, âmes, peste et malédictions : la race de l’invocation et du nombre.* (ex-Légion des ombres)

- **Mécanique propre — Âmes** : Chaque monstre qui meurt près de tes tours donne 1 âme (2 s’il était Maudit), jusqu’à 30. Le Nécromancien et le Colosse d’os les dépensent ; le Puits des âmes les convertit.
- **États** : Maudit : +20 % de dégâts subis ; Pestiféré : dégâts par seconde ; à sa mort, la peste saute sur ses voisins.
- **Forces** : foules, amplification, blocage. **Faiblesses** : boss isolé, démarrage lent.
- **Profil** (Mono-cible, Zone, Anti-air, Anti-blindé, Contrôle, Économie) : 3 / 6 / 4 / 4 / 6 / 7.
- **Combos** :
  - **Récolte** (Obélisque de malédiction + Tour des archers squelettes) : Un monstre Maudit par l’Obélisque qui meurt donne 2 âmes au lieu d’une.
  - **Épidémie** (Autel de peste + Obélisque de malédiction) : La peste de l’Autel fait deux fois plus de dégâts sur un monstre Maudit.
  - **Armée des morts** (Nécromancien + Autel de peste) : Avec un Autel de peste, les morts relevés par le Nécromancien répandent la peste en frappant.
- **IA, version renforcée** (`up`) : Tour des archers squelettes → Faucheuse, Ossuaire → Nécromancien.

| # | Tour | Rôle | Coût | Dégâts | Recharge | DPS | Portée | Effet |
|---|---|---|---|---|---|---|---|---|
| 0 | Tour des archers squelettes | Base | 20 | 7,8 | 0,5 | 16 | 2,8 | Flèches d’os au sol et dans les airs. |
| 1 | Ossuaire | Proximité | 35 | 8 | 3 | 3 | 1,8 | Des squelettes sortent de la neige et retiennent un monstre 1,5 s. |
| 2 | Obélisque de malédiction | Contrôle | 40 | 3 | 0,9 | 3 | 2,6 | Malédiction en zone : Maudit, +20 % de dégâts subis pendant 3 s. |
| 3 | Autel de peste | Zone | 55 | 4 | 1,2 | 3 | 2,4 | Nuage de peste en zone : dégâts dans la durée, qui sautent sur les voisins à la mort. |
| 4 | Perchoir des gargouilles | Anti-aérien | 60 | 18 | 0,7 | 26 | 3 | Les gargouilles harcèlent les volants : dégâts ×2 contre eux. |
| 5 | Œil du Voile | Détection | 85 | 24 | 1,3 | 18 | 3,2 | Révèle les invisibles et maudit sa cible. |
| 6 | Nécromancien | Signature | 95 | 10 | 1,2 | 8 | 2,8 | Dépense 1 âme pour relever un monstre tué à sa portée : le mort remonte le chemin et frappe. |
| 7 | Puits des âmes | Soutien | 80 | 0 | 1 | 0 | 1,5 | Ne tire pas. Tours voisines : +2 % de cadence par tranche de 5 âmes. Âmes au maximum : 5 âmes deviennent de l’or. |
| 8 | Faucheuse | Anti-boss | 130 | 50 | 1,4 | 36 | 2,6 | Exécute les monstres sous 12 % de PV. Contre un boss : +50 % de dégâts sous 25 %. |
| 9 | Colosse d’os | Ultime | 260 | 0 | 45 | 0 | 3 | Ultime, un seul par terrain. Dépense 15 âmes : un colosse d’os remonte le chemin et écrase tout autour de lui. |


### 5.3 Règles d'équilibrage (centrales, obligatoires pour toute race nouvelle ou modifiée)
Le DPS ne suffit pas : le poison agit dans la durée, le gel profite à toutes les autres tours. Chaque tour est donc évaluée en **Puissance effective** (PE, en « DPS équivalent ») :

`PE = dégâts directs utiles + zone + dégâts dans la durée + contrôle + amplification + aura + invocation + économie`

1. **Dégâts directs utiles** = DPS × couverture (cases de chemin à portée sur le labyrinthe de référence) × (1 − dégâts perdus sur des monstres déjà morts).
2. **Zone** : × nombre moyen de cibles touchées (groupes de 4) ; chaîne : `1 + Σ 0,75^k` rebonds.
3. **Dans la durée** : dégâts totaux × chance que la cible vive assez longtemps.
4. **Contrôle** : temps d'exposition gagné × DPS allié de référence. Ralentissement : `durée × part retirée` ; immobilisation : la durée.
5. **Amplification** : `bonus × temps actif × DPS allié`. **Aura** : `bonus × DPS des tours couvertes` (3 voisines de référence).
6. **Économie** : une tour qui rapporte de l'or doit mettre **au moins 120 s** à se rembourser.
7. **Efficacité** `PE ÷ prix` : dans une bande de ±10 % autour de la référence (Archer : 20 or, 16 DPS, portée 2,8), +6 % par palier (case et chantier économisés).

**Règles vérifiées par `tests/simulation/races.test.js`** :
- **Radar** (`radar`, axes `REGLES.axes`) : 6 axes notés de 1 à 10, **somme 30**, chaque axe entre **3 et 8**, au moins une faiblesse (≤ 4), au plus deux spécialités (≥ 7).
- **Couverture** : tour de base sol et air ≤ 25 or (j0), anti-aérien dédié (j4), détection ≤ 120 or (j5), au moins 2 sources non magiques, une réponse aux blindés, une seule ultime (j9), au moins 2 combos à deux tours différentes, fiche complète (histoire, mécanique, états, forces, faiblesses).
- **Pas de domination** : aucune tour n'est meilleure qu'une autre de sa race en prix, dégâts estimés, portée et cibles à la fois (sauf si l'autre a un effet).
- **Plafonds** : amplification +60 %, vitesse ≥ ×0,3, 10 doses, immobilisations à rendement décroissant, moitié pour les boss, pas d'exécution ni de Maléfice sur un boss.
- **Une seule ultime** par terrain.

**Équilibre en partie** : `node tests/outils/banc-races.js [--parties N]` fait jouer les 5 races l'une contre l'autre par l'IA (4 races par partie, places tournantes). **Critère : chaque race entre 1,2 et 1,8 point par partie** (1,5 = équilibre). Réglages essayés sans toucher à `sim.js` : `WR_MODIF="<code>"` (par exemple `WR_MODIF="S.TW[20].pv=.3"`). Mesure de la 2.40 (6 graines, 30 parties) : Aubeval 1,46, Orage Blanc 1,67, Lunebois 1,29, Hautroc 1,58, Ossements 1,50. Premiers essais : le poison dominait (Lunebois 2,9 points, 14 victoires sur 16), Hautroc s'effondrait (0,2 point : l'IA posait son anti-aérien « air seulement » face à des vagues au sol). Corrigé : poison qui progresse en `1 + niveau` au lieu de `2^niveau` et dégâts de Lunebois ×0,9 ; Hautroc ×1,25 en dégâts ; l'IA attend des volants pour poser l'anti-aérien.

---

## 6. Les monstres (`CR`)

### 6.1 Envoi
- Un envoi coûte le prix du monstre et fait apparaître un **groupe de 4** (`GROUP`) chez **chaque adversaire encore en jeu**, espacés d'environ 0,4 s.
- **Les monstres se renforcent avec le temps** : `PV = PV_base × (1 + temps/200) × 0,55` (`HPK`). L'armure suit le même multiplicateur `(1 + temps/200)`. À 10 minutes, les monstres ont donc 4 fois plus de PV.
- **Revenu gagné par envoi** :
  - monstres au sol : `arrondi à l'inférieur(coût/10 × (1 + 0,1 × log10(coût/10)))`, une courbe croissante qui passe par **10 or → +1, 100 → +11, 1000 → +120**. Depuis la 2.14, l'arrondi se fait à l'inférieur : aucun monstre ne rapporte plus que la courbe, donc un monstre bon marché n'est jamais proportionnellement plus rentable qu'un plus cher ;
  - **tous les coûts sont des dizaines** (depuis la 2.14) ;
  - autres monstres : `arrondi(coût × 0,065)`.
- **Paliers** (depuis la 2.13, à la place des déblocages par le temps) : les monstres sont rangés en **3 paliers de 24** (12 au sol, 3 volants, 8 magiques, 1 boss). Le palier 1 est ouvert dès le début ; chaque joueur ouvre ensuite le palier 2 pour **300 or** puis le palier 3 pour **1 500 or** (`PAL_C`, action `tier`), une fois pour toute la partie. Un monstre d'un palier fermé est refusé (`locked`). Les 8 capacités magiques de chaque palier : hâte, invisible, se divise, accéléré, anti-magie, soin, armure, étourdissement. Les monstres au sol restent les plus rentables pour le revenu (courbe ci-dessus, contre 6,5 % du coût pour les autres).

### 6.2 Liste
Vitesse en cases par seconde. Dans chaque palier, les monstres sont rangés par catégorie puis par coût.

| Monstre | Catégorie | Coût | +revenu | PV de base | Vitesse | Palier | Capacité |
|---|---|---|---|---|---|---|---|
| Sapeur gobelin | Sol | 10 | +1 | 12 | 1,6 | 1 | — |
| Rat des neiges | Sol | 20 | +2 | 20 | 2,2 | 1 | — |
| Warg | Sol | 30 | +3 | 33 | 2,4 | 1 | — |
| Kobold | Sol | 40 | +4 | 48 | 1,6 | 1 | — |
| Squelette du givre | Sol | 50 | +5 | 60 | 1,5 | 1 | — |
| Sanglier de guerre | Sol | 60 | +6 | 69 | 2 | 1 | — |
| Gnoll | Sol | 70 | +7 | 87 | 1,6 | 1 | — |
| Brute orc | Sol | 80 | +8 | 101 | 1,4 | 1 | — |
| Maraudeur | Sol | 90 | +9 | 114 | 1,5 | 1 | — |
| Myconide | Sol | 100 | +11 | 135 | 1,1 | 1 | — |
| Yéti | Sol | 110 | +12 | 149 | 1,3 | 1 | — |
| Troll des glaces | Sol | 120 | +13 | 160 | 1,5 | 1 | — |
| Chauve-souris | Volant | 30 | +2 | 16 | 2 | 1 | Vol |
| Guêpe des glaces | Volant | 50 | +3 | 26 | 2,3 | 1 | Vol |
| Harpie | Volant | 90 | +6 | 55 | 1,9 | 1 | Vol |
| Chaman de guerre | Magique | 80 | +5 | 70 | 1,5 | 1 | **Hâte** : les alliés à moins de 1,7 case vont 1,4 fois plus vite |
| Prêtresse | Magique | 100 | +7 | 80 | 1,4 | 1 | **Soin** : les alliés à moins de 1,7 case regagnent 5 % de leurs PV max par seconde |
| Lutin des glaces | Magique | 110 | +7 | 70 | 1,5 | 1 | **Accéléré** : vitesse × (1 + 0,1 × secondes de vie), au plus × 2 |
| Gelée mutante | Magique | 140 | +9 | 90 | 1,3 | 1 | **Se divise** en 2 Petit limon à sa mort |
| Spectre | Magique | 150 | +10 | 90 | 1,5 | 1 | **Invisible** sauf à portée d'une tour Mage |
| Tortue | Magique | 160 | +10 | 140 | 1,1 | 1 | **Blindé** : armure 5 |
| Briseur de runes | Magique | 170 | +11 | 120 | 1,4 | 1 | **Anti-magie** : insensible au Givre et au Mage |
| Saboteur gobelin | Magique | 190 | +12 | 110 | 1,5 | 1 | **Étourdit** la tour la plus proche |
| Roi gobelin | Boss | 450 | +29 | 900 | 1 | 1 | **Boss** : armure 2 et étourdissement |
| Homme-lézard | Sol | 150 | +16 | 200 | 1,6 | 2 | — |
| Chevalier noir | Sol | 180 | +20 | 250 | 1,2 | 2 | — |
| Gargouille | Sol | 210 | +23 | 285 | 1,3 | 2 | — |
| Loup-garou | Sol | 240 | +27 | 310 | 1,9 | 2 | — |
| Ours de guerre | Sol | 270 | +30 | 370 | 1,5 | 2 | — |
| Golem runique | Sol | 300 | +34 | 420 | 1 | 2 | — |
| Ogre | Sol | 330 | +38 | 460 | 1,1 | 2 | — |
| Minotaure | Sol | 370 | +42 | 500 | 1,4 | 2 | — |
| Automate blindé | Sol | 410 | +47 | 580 | 1 | 2 | — |
| Wendigo | Sol | 450 | +52 | 610 | 1,6 | 2 | — |
| Rhinocéros de guerre | Sol | 500 | +58 | 720 | 1,5 | 2 | — |
| Mammouth de guerre | Sol | 600 | +70 | 900 | 0,9 | 2 | — |
| Griffon corrompu | Volant | 150 | +10 | 95 | 1,9 | 2 | Vol |
| Vouivre | Volant | 260 | +17 | 180 | 1,8 | 2 | Vol |
| Manticore | Volant | 380 | +25 | 290 | 1,6 | 2 | Vol |
| Tambour de guerre | Magique | 300 | +20 | 300 | 1,4 | 2 | **Hâte** : les alliés à moins de 1,7 case vont 1,4 fois plus vite |
| Druidesse | Magique | 330 | +21 | 280 | 1,4 | 2 | **Soin** : les alliés à moins de 1,7 case regagnent 5 % de leurs PV max par seconde |
| Centaure messager | Magique | 340 | +22 | 260 | 1,6 | 2 | **Accéléré** : vitesse × (1 + 0,1 × secondes de vie), au plus × 2 |
| Assassin des ombres | Magique | 380 | +25 | 300 | 1,6 | 2 | **Invisible** sauf à portée d'une tour Mage |
| Golem de boue | Magique | 400 | +26 | 320 | 1,2 | 2 | **Se divise** en 2 Petite boue à sa mort |
| Scarabée cuirassé | Magique | 430 | +28 | 380 | 1,2 | 2 | **Blindé** : armure 12 |
| Inquisiteur | Magique | 450 | +29 | 380 | 1,3 | 2 | **Anti-magie** : insensible au Givre et au Mage |
| Ingénieur nain renégat | Magique | 480 | +31 | 360 | 1,4 | 2 | **Étourdit** la tour la plus proche |
| Cyclope des cendres | Boss | 1400 | +91 | 2800 | 1 | 2 | **Boss** : armure 6 et étourdissement |
| Roi-liche | Sol | 900 | +107 | 1200 | 1,2 | 3 | — |
| Seigneur de guerre orc | Sol | 1000 | +120 | 1350 | 1,3 | 3 | — |
| Élémentaire de feu | Sol | 1100 | +132 | 1400 | 1,5 | 3 | — |
| Démon des abysses | Sol | 1250 | +151 | 1700 | 1,4 | 3 | — |
| Golem de lave | Sol | 1400 | +170 | 2000 | 0,9 | 3 | — |
| Ver des neiges | Sol | 1550 | +188 | 2100 | 1,2 | 3 | — |
| Chimère | Sol | 1700 | +207 | 2250 | 1,5 | 3 | — |
| Géant du givre | Sol | 1900 | +233 | 2700 | 1 | 3 | — |
| Sylvain corrompu | Sol | 2100 | +258 | 3000 | 0,9 | 3 | — |
| Mastodonte de fer | Sol | 2400 | +297 | 3500 | 0,8 | 3 | — |
| Béhémoth | Sol | 2700 | +335 | 3900 | 1,1 | 3 | — |
| Colosse de pierre | Sol | 3000 | +374 | 4500 | 0,85 | 3 | — |
| Dragon ancien | Volant | 900 | +59 | 800 | 1,3 | 3 | Vol |
| Phénix de givre | Volant | 1200 | +78 | 1000 | 1,6 | 3 | Vol |
| Oiseau-roc | Volant | 1600 | +104 | 1400 | 1,4 | 3 | Vol |
| Héraut de guerre | Magique | 1100 | +72 | 1100 | 1,3 | 3 | **Hâte** : les alliés à moins de 1,7 case vont 1,4 fois plus vite |
| Destrier de cauchemar | Magique | 1200 | +78 | 950 | 1,6 | 3 | **Accéléré** : vitesse × (1 + 0,1 × secondes de vie), au plus × 2 |
| Grande prêtresse de sang | Magique | 1250 | +81 | 1000 | 1,3 | 3 | **Soin** : les alliés à moins de 1,7 case regagnent 5 % de leurs PV max par seconde |
| Faucheuse | Magique | 1300 | +85 | 1050 | 1,5 | 3 | **Invisible** sauf à portée d'une tour Mage |
| Hydre | Magique | 1400 | +91 | 1100 | 1,1 | 3 | **Se divise** en 2 Tête d’hydre à sa mort |
| Dévoreur de mana | Magique | 1500 | +98 | 1300 | 1,2 | 3 | **Anti-magie** : insensible au Givre et au Mage |
| Tortue-dragon | Magique | 1600 | +104 | 1400 | 1 | 3 | **Blindé** : armure 25 |
| Golem du tonnerre | Magique | 1700 | +111 | 1400 | 1,1 | 3 | **Étourdit** la tour la plus proche |
| Azh'Khar, seigneur des lames | Boss | 3500 | +228 | 7000 | 1,02 | 3 | **Boss** : armure 15 et étourdissement |
| Petit limon | Né d'une division | 20 | +1 | 35 | 1,6 | 1 | — |
| Petite boue | Né d'une division | 60 | +4 | 110 | 1,4 | 2 | — |
| Tête d'hydre | Né d'une division | 200 | +13 | 380 | 1,3 | 3 | — |

Les « nés d'une division » ne s'envoient pas : ils apparaissent par 2 à la mort de leur parent, avec ses PV multipliés de la même façon.

### 6.3 Détails des capacités
- **Armure** : chaque coup perd un montant fixe de dégâts (`armure × multiplicateur de temps`), mais garde toujours au moins **20 %** des dégâts. Les Nains réduisent cette armure de 55 %.
- **Étourdissement** : toutes les **3,5 s** (premier essai 2 s après l'apparition), le monstre étourdit pendant **2 s** la tour la plus proche dans un rayon de **2,3 cases**. Une tour déjà étourdie ne peut pas être ciblée.
- **Invisibilité** : un Spectre caché ne peut être ni ciblé, ni touché par les explosions ou les flammes.
- **Accéléré** (depuis la 2.13) : la vitesse est multipliée par `1 + 0,1 × secondes de vie` (`ACC`), au plus × 2 (`ACC_MAX`), avant les ralentissements et la hâte.
- **Se divise** : à sa mort, le monstre laisse 2 petits (`kid`) : Gelée → Petit limon, Golem de boue → Petite boue, Hydre → Tête d'hydre.
- **Boss** (un par palier) : armure et étourdissement, avec un halo violet en 2D.
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
- **Fin de partie** (depuis la 2.33) : quand sa défense est au maximum (plan entièrement construit, toutes les tours au niveau 5 : `A.plein`, calculé par `aiDefend`), toute sa réserve de défense passe à l'attaque, à chaque tour d'action. Avant, la part de défense (15 % à 80 % des gains, plus encore sous pression) dormait sans pouvoir servir.

**Labyrinthe** (depuis la 2.5) : chaque IA reçoit un **plan cible** (`A.mz`) au début de la partie.
- **Génération** (`mzStep`) : 4 candidats. Chacun part d'une forme tirée au hasard (serpentin horizontal à couloirs de 1 ou 2, serpentin vertical, semis aléatoire), puis il est affiné par une recherche locale avec recuit léger : on ajoute ou retire une case ou un petit segment (dans l'une des 8 directions : depuis la 2.25, deux tours qui se touchent par un coin font mur). Score = longueur du chemin − 0,3 × nombre de tours.
  - **Longueur du chemin** (`plen`, depuis la 2.25) : mêmes règles que les monstres, 8 directions sans couper le coin d'un mur, coûts entiers 5 (droit) et 7 (diagonale, ≈ 5 × √2), calculée par files circulaires (algorithme de Dial) ; `mzPath` en donne les cases.
  - Itérations par candidat : 2 000 / 2 500 / 3 200 selon la difficulté.
  - **Murs inutiles retirés** (depuis la 2.6) : une tour qui ne touche pas le chemin (les 8 cases autour) et dont le retrait ne le raccourcit pas est enlevée du plan. Il ne reste loin du chemin que les tours nécessaires à sa longueur.
  - **Note de milieu de partie** (depuis la 2.6 ; selon l'exposition depuis la 2.33) : chaque candidat est noté sur l'**exposition par tour** (voir « Ordre de construction ») après 15, 25, 40 et 60 tours de son ordre de construction, et une fois complet (`MZ_AT`). De la 2.6 à la 2.31, la note était la longueur moyenne du chemin à ces étapes ; avant la 2.6, seule comptait la longueur finale, ce qui favorisait les serpentins classiques, très longs une fois finis mais courts tant qu'un mur n'est pas fermé. `M.pre` garde la longueur du chemin à ces étapes.
  - Le plan retenu est tiré parmi les 3 meilleures notes en Normal (50/30/20 %), parmi les 2 meilleures en Difficile (60/40 %), et c'est la meilleure en Brutal.
  - Mesuré en 8 directions sur 30 graines (2.25) : un plan complet fait en moyenne 84 cases de chemin en Normal et 95 en Brutal, contre 16 en ligne droite ; avec 40 tours, 57 cases en Normal (au moins 42) et 61 en Brutal (au moins 52). Les plans d'avant la 2.25, conçus en 4 directions, faisaient 56 et 59 cases à 40 tours une fois mesurés de la même façon.
- **Hasard propre** : la graine est tirée une fois de `Math.random`, ce qui rend la génération indépendante du découpage dans le temps.
- **Découpage** : la génération avance de 600 essais par pas de jeu (≈ 2 à 5 ms) ; elle dure environ 60 à 75 ms au total (deux fois plus qu'avant la 2.25, à cause des 8 directions ; inchangé en 2.32, car un essai de l'ordre de construction compte désormais double). Elle est terminée avant la première action, ou bien elle est finie d'un coup à la première action. Un calcul de `plen` sur grille plate prend environ 2,5 à 3,5 µs (1,1 à 1,7 µs en 4 directions avant la 2.25).
- **Ordre de construction** (selon l'exposition depuis la 2.33) : l'**exposition** d'un labyrinthe (`expo`) est la somme, sur toutes ses tours, du nombre de cases du chemin à moins de 2,5 cases de la tour (`MZ_RE`, à peu près la portée d'un Archer) : c'est le temps que les monstres passent à portée des tours. Une tour loin du chemin ne compte pas ; un chemin plus long compte pour chaque tour qui le borde. À partir du plan complet, on retire une à une la tour dont le retrait fait perdre le moins d'exposition (parmi 24 tirées au hasard, à égalité celle hors du couloir aérien), et on construit dans l'ordre inverse : à chaque étape, les tours posées voient le chemin du moment. **Mesuré sur 16 graines** : vers 15 à 25 tours, il restait 3 à 4 tours sur 15 à 25 loin du chemin (aucune case à 2,5 cases), il en reste 1 à 2 ; chaque tour voit 10 à 50 % de cases de chemin en plus ; en échange, le chemin est un peu plus court à 40 tours (49 cases en Normal au lieu de 53). Une variante qui repoussait d'office à la fin toute tour loin du chemin a été essayée et écartée : elle gagnait 0,19 point dans l'arène, contre 0,64 pour celle-ci. Avant la 2.33, on retirait la tour qui raccourcissait le moins le chemin : le chemin s'allongeait presque à chaque tour, mais vers 3 min de jeu jusqu'à un tiers des tours de l'IA bouchaient un raccourci loin du chemin, sans jamais tirer.
- **Rôles des cases** (`mzRoles`) :
  - **Givre** : 2 à 6 emplacements (`L/15`), répartis à intervalles réguliers le long du chemin final. Ils sont construits en Givre seulement tant que leur nombre reste sous `1 + 15 % des tours` ; sinon un Archer est posé, puis transformé plus tard.
  - **Mage** : jusqu'à 6 emplacements choisis pour que leur détection couvre tout le chemin. Ce sont des Archers tant qu'il n'y a pas de **menace de Spectres** : temps ≥ 2:30 et un adversaire avec un revenu ≥ 35, ou un Spectre déjà reçu (`specSeen`). Dès la menace, ils sont transformés en Mages (prix réel du Mage de la faction).
  - **Couloir aérien** (|x − 6| ≤ 2) : Archer, ou Flammes au centre s'il y a beaucoup de chemin autour. Jamais de Canon ni de Garde.
  - **Ailleurs** : Canon dans les virages, Garde entre deux couloirs, Archer sinon, avec un peu de hasard.
  - Si plus de 35 % des PV reçus volent (`flyIn/hpIn`), les Canons et Gardes prévus près du centre deviennent des Archers, et les améliorations favorisent le couloir aérien.
  - Depuis la 2.40, l'emplacement j du plan désigne un **rôle** (§4.2) : 0 base, 1 proximité, 2 contrôle (ex-Givre), 3 zone (ex-Canon), 4 anti-aérien (ex-Flammes, au centre du couloir aérien ; **posé seulement quand 15 % ou plus des PV reçus volent**, sinon une tour de base), 5 détection (ex-Mage).
  - **Version renforcée** propre à chaque race (`RACES[f].up`, par exemple Tour d'arbalétriers → Inquisiteur) : une fois sur deux à partir de 8 tours, si l'or le permet.
  - **Soutien et ultime** (depuis la 2.40, `transformer`) : à partir de 14 tours, environ une tour sur 12 devient une tour de soutien (emplacement 7), sur la tour de base, de proximité ou de zone qui a le plus de voisines ; après 7:00, une tour de ce type devient l'**ultime** (emplacement 9), celle qui voit le plus de chemin. L'IA ne pose pas le Comptoir marchand.
  - L'estimation des défenses (`contreMenace`, `encaisse`) compte à part les dégâts dans la durée, qui ignorent l'armure (`W.dot`), et le facteur de zone de chaque tour (`W.zf`).
  - **Type choisi selon la menace reçue** (depuis la 2.33, `observer`, `contreMenace`, `choixType`) : l'IA retient les PV de chaque monstre reçu (`A.menace`, un compteur par monstre de `CR`, oublié peu à peu : ×0,997 à chaque action, environ 2 min de demi-vie). Sur un emplacement ordinaire (Archer, Garde, Canon ou Flammes du plan ; pas le Givre ni les Mages de détection), dès que la menace dépasse 200 PV, elle pose le type qui fait le plus de dégâts par or contre cette menace sur cette case : dégâts d'un coup moins l'armure (au moins 20 %, perforation des Nains comprise), bonus anti-aérien, rien contre les volants pour une tour au sol seulement ni contre l'anti-magie pour une tour magique, × cibles touchées (`ZONE`), × longueur du chemin actuel (ou du couloir des volants) à portée, ÷ recharge ÷ prix. Le type prévu par le plan garde un avantage de 15 % ; dans le couloir aérien, seulement Archer ou Flammes ; le Mage s'ajoute aux choix à partir de 8 tours, tant que les tours magiques restent sous 40 % (`MAG_MAX`). Face aux boss et aux blindés, les Archers (8 dégâts par coup) laissent place aux Gardes, aux Canons ou aux Mages. **Arène** : +0,52 point par siège (± 0,14) avec 40 vies, +0,14 (± 0,14) avec 400 vies. Essayé et écarté : choisir aussi les **améliorations** selon la menace (aucun gain seul, et moins bien avec le choix du type : +0,29).

**Quêtes bonus** (depuis la 2.38, `quJ`) : au lancement d'une quête, chaque IA décide si elle la joue (`QU_JOUE` : 50 % en Normal, 75 % en Difficile, 100 % en Brutal). Si oui :
- **Clicker fou** : elle construit des Archers (les moins chers) sur les cases de son plan, sans rien améliorer, avec tout son or ;
- **Frozen** : elle construit sa tour de contrôle (emplacement 2) sur les cases de son plan ; plan fini, elle transforme ses tours de niveau 1 ou 2 (pas ses détecteurs) en tours de contrôle ;
- **Gonflette** / **Bling-bling** : elle améliore sa tour la plus haute (la plus chère) et garde son or pour elle tant qu'elle ne prend pas de coups ;
- **Picsou** : elle ne dépense rien tant qu'elle n'est pas en danger (vie perdue récemment ou monstres à plus de 65 % du chemin) ;
- **Facteur** et **Pigeons voyageurs** : elle envoie dès 60 or de réserve d'attaque au lieu d'attendre une grosse vague (Pigeons : des volants) ;
- **Le gros cadeau** : elle envoie un boss dès que tout son or le paie, et garde son or d'attaque pour lui ;
- Qui a la plus grosse ? et Mamie Gâteau : rien de spécial (son labyrinthe est déjà long ; on ne cherche pas à perdre du revenu).
L'or dépensé en plus de sa réserve de défense est repris sur sa réserve d'attaque (`aiDefend` enveloppe `aiDefendre`).

**Défense** (`aiDefend`), jusqu'à 3 actions par tour :
- d'abord, une **transformation** si besoin (détection ou contrôle sur sa case, puis soutien et ultime depuis la 2.40, seulement pour une tour de niveau 1 ou 2 qui n'est pas en chantier ; la tour transformée repart en chantier) ;
- sinon, elle **améliore** la tour la plus rentable (celle qui couvre le plus de chemin et de couloir aérien par pièce d'or, jamais une tour en chantier), dès que le plan est terminé, ou par hasard à partir de 12 tours (25 %, puis 50 % à partir de 28 tours ; depuis la 2.33, avant : 10 tours, 35 %, puis 60 % à partir de 24 tours) ;
- sinon, elle **construit** la prochaine case du plan. Si un monstre l'occupe, elle essaie les 3 suivantes, mais ne saute jamais une case faute d'or. L'IA ne pose jamais de tour hors de son plan, ce qui corrige le blocage d'avant la 2.5 (l'IA cessait de construire vers 36 tours).

**Attaque** (`aiAttack`) :
- rien pendant les **30 premières secondes** (`GRACE`, phase « Construis » du §2 ; 25 s avant la 2.30) ;
- elle accumule de l'or jusqu'à `min(6000, max(60, revenu × 3))`, puis envoie une grosse vague ;
- **composition selon ce que chaque adversaire peut encaisser** (depuis la 2.33) :
  - `encaisse(b, k, m)` estime les PV qu'une foule du monstre `k` perd en traversant le terrain `b` : pour chaque tour active, dégâts d'un coup contre ce monstre (niveau, armure moins la perforation des Nains, bonus anti-aérien, Malédiction, Frénésie), divisés par la recharge, × nombre de cibles touchées (`ZONE` : Canon ×2,5, Givre ×2, Flammes ×3), × temps passé à portée (longueur du chemin réel à portée, ou du couloir des volants, divisée par la vitesse, + 1 s). Les tours au sol seulement ignorent les volants, Mage et Givre ignorent l'anti-magie, un invisible n'est touché que sur la part du chemin vue par un Mage, le Givre ralentit (−30 % sur la part du chemin qu'il couvre). Le profil de chaque terrain (chemin échantillonné toutes les 0,5 case de case en case, `trajet`, et tours, `profil`) reste en cache tant que ses tours et son chemin ne changent pas ; les points vus par chaque tour restent gardés sur la tour, si bien qu'une amélioration ne refait que le calcul de cette tour ;
  - c'est une estimation prudente : vérifiée en envoyant de vraies foules, les monstres commencent à passer vers 1 à 2 fois l'estimation, d'où le coefficient `ENC` = 1,5 ;
  - pour chaque famille (sol, volants, invisibles, blindés, anti-magie, se divise, accélérés, étourdissants, et le boss une fois l'heure venue), elle prend le monstre le plus cher qu'elle peut payer parmi ses paliers ouverts et calcule combien de monstres passeraient chez chaque adversaire si toute sa réserve y allait (au plus les vies qui lui restent, +3 si l'adversaire serait éliminé). Elle envoie la famille qui fait perdre le plus de vies, avec du hasard (`VAGUE_HZ` : chaque note est multipliée au hasard entre 0,6 et 1,4 en Normal, 0,75 et 1,25 en Difficile, 0,9 et 1,1 en Brutal) ;
  - si aucune famille ne passe, la vague sert l'**économie** : les meilleurs monstres au sol (le plus fort revenu par or) ;
  - quand le monstre choisi devient trop cher pour ce qui reste, le reste part en monstres au sol ; 12 envois au plus à chaque fois ;
  - mesuré (exemples à 5 et à 12 min de jeu) : les **boss** et les **blindés** sont de loin les plus difficiles à encaisser (4 Cyclopes passent dès 5 min), puis les volants ; les monstres au sol sont les plus faciles. Avant la 2.33, l'IA tirait ses familles au hasard avec des poids fixes (sol ×5, volants ×4 si un adversaire avait peu de défense aérienne, invisibles ×4 si l'un d'eux n'avait pas de Mage…) et n'envoyait le boss qu'avec 28 % de chances ;
- **paliers** (2.13) : elle ouvre le palier 2 à partir de 2:30 et le palier 3 à partir de 7:00, dès que sa réserve d'attaque vaut 1,5 fois le prix ;
- elle ajoute le soigneur et le monstre de hâte les plus forts possibles (60 % de chances chacun) si sa réserve dépasse 500 et 4 fois leur prix, sauf pour une vague de volants ;
- le boss (le plus fort de ses paliers) entre dans les familles possibles après **4:00** pour celui du palier 1, **7:00** pour les autres.

---

## 9. Interface et commandes

- **Disposition « vue tactique »** (depuis la 2.15, d'après la maquette validée par le concepteur) : le terrain occupe **tout l'écran** ; le bandeau (en haut) et le dock (en bas : fiche, onglets, paliers, cartes) **flottent par-dessus**, sur un dégradé de nuit. Style : pastilles et panneaux en verre de nuit à liseré d'or, or pour les tours, rouge pour les monstres.
- **Habillage « givre »** (depuis la 2.18, retour des textures gelées et des cadres à volutes de la 2.12, disposés comme la console d'un jeu de stratégie, dans un style propre au jeu) : tout en SVG et CSS (`--orne-argent`, `--orne-or`, `--orne-rouge`, `--givre`, `--frise`) :
  - **barre de ressources** (`#hud`) : bande de verre de nuit givré sur toute la largeur, bordée dessous d'une **frise d'argent à gemmes de glace** ; ressources serties comme des pierres de lune, boutons ronds en métal bleuté cerclés d'or (menu, plein écran, flèches de rotation) ;
  - **console du bas** (`#console` : onglets, paliers, cartes) : dalle de verre givré bordée dessus de la même frise ; la fiche flotte au-dessus, dans un cadre d'argent à volutes (rouge pour un monstre) ;
  - **cartes** : emplacements carrés sertis d'argent (or quand la carte est choisie, rouge pour les monstres), icône sur fond de glace, **prix dans un médaillon** posé sur le bas du cadre ; onglets en relief (or pour Tours, rouge pour l'onglet de monstres ouvert) ;
  - bouton Adversaires, panneau des vignettes et menu : verre givré et cadre d'argent ; léger voile de froid sur les bords du terrain.
- **Portrait seulement** (depuis la 2.15) : un téléphone tenu en paysage affiche « Tourne ton téléphone : Winter Realms se joue en portrait » (`#tourner`, écran tactile de moins de 540 px de haut). Sur ordinateur ou tablette en paysage, le jeu tient dans une colonne au format portrait, centrée.
- **Bandeau du haut** (2.15 ; barre givrée depuis la 2.18) : bouton **menu** (☰), or, revenu avec un **anneau** qui se remplit pendant les 10 s avant le versement, **vies du joueur** (♥), horloge, bouton **plein écran**. Le plein écran verrouille l'écran en portrait quand le téléphone le permet.
- **Départ façon jeu de course** (depuis la 2.30, `departTick()`, `annonce()`), piloté par le temps de jeu (solo ou instantanés du serveur), sans bloquer les gestes (`pointer-events:none`) :
  - au lancement, bannière animée **« Construis ! »** (≈ 3 s) : bande inclinée à liseré d'or, **logo** (médaillon doré, tour de glace et marteau, rayons qui tournent), titre doré qui traverse l'écran avec un reflet, et le **chrono « 30 » en gros**, qui s'envole ensuite vers le bandeau ;
  - pendant la phase, le **chrono du bandeau** (`#prep`, marteau doré) remplace l'horloge et décompte de 0:30 à 0:01 (rouge et pulsant sous 5 s) ; les **onglets de monstres** (Sol, Volants, Spéciaux) sont **désactivés** (grisés, cadenas, non cliquables) ;
  - **3, 2, 1** en très gros au centre, avec un bip à chaque chiffre ;
  - à 0:30, bannière **« Envoie et résiste ! »** (≈ 2,7 s) : flash, bande à liseré rouge, **logo** (deux épées croisées derrière un écu rouge), titre rouge ; les onglets de monstres se déverrouillent en clignotant. L'horloge normale revient.
  - sons synthétisés : `cor` (Construis), `bip` (3-2-1), `go` (Envoie et résiste). Logos en SVG dans le code. Avec « réduire les animations », les annonces s'affichent sans mouvement.
- **Menu** (2.15, `#menu`) : Reprendre, Musique (activée/coupée, depuis la 2.16), Son (activé/coupé, les bruitages seulement), Vibrations (activées/coupées), Rappel des gestes, Quitter la partie (deux touchers : « Confirmer : quitter la partie »). En solo, quitter ramène à l'accueil ; en ligne, quitte le salon.
- **Musique de fond** (depuis la 2.16, objet `MUSIQUE`) : trois thèmes composés par le concepteur avec **Suno** (`assets/musique/winter-realm.mp3`, `winter-realm-1.mp3`, `winter-realm-2.mp3`, environ 8 Mo chacun, lus en continu pendant le téléchargement). Le premier thème est **tiré au hasard** au lancement, puis ils s'**enchaînent les uns après les autres, en boucle**, de l'accueil jusqu'à la fin de la partie. La musique démarre au premier toucher sur la page (les navigateurs bloquent le son avant) ; elle passe par Web Audio (volume 0,4, réglable aussi sur iPhone) ; elle se met en pause quand la page est cachée. Le menu la coupe sans toucher aux bruitages. Un fichier illisible est sauté.
- **Adversaires** (panneau flottant depuis la 2.3 ; bouton « Adversaires » sous le bandeau, à droite, depuis la 2.15, avec un point de la couleur de chaque adversaire) : le bouton (`#cartesBtn`) ouvre un panneau posé **par-dessus le terrain** (`#chips`), avec les 4 vignettes : mini-carte, vies et revenu (bonus de difficulté compris) de chaque terrain. En 3D, la vignette du terrain regardé montre en or la partie visible.
  - **Mini-cartes d'hiver** (depuis la 2.28, `drawMini`, 6 px par case, `MINI`) : neige et grille comme la 3D, chemin des monstres en pointillés bleu nuit, portail violet, petit château au drapeau du joueur ; chaque tour est une petite pièce biseautée à la **couleur de son rôle** (celle des pastilles `BADGE` : vert Archer, rouge Garde, bleu Givre, cuivre Canon, orange Flammes, violet Mage), avec un point d'or à partir du niveau 2 et en transparence pendant le chantier ; monstres cerclés de nuit, rouges au sol, blancs en vol. Vignette sertie d'argent ; vies avec un cœur et revenu avec la pièce d'or du bandeau. Terrain éliminé : neige grise.
  - **Toucher une vignette** affiche le terrain correspondant et referme le panneau ; le bouton prend alors la couleur et le nom de ce joueur. On ne peut pas y construire (« lecture seule »), mais **on peut envoyer des monstres depuis là** et les regarder arriver.
  - Toucher le terrain pendant que le panneau est ouvert le referme **sans poser de tour**.
  - La bannière au-dessus du dock (« Terrain de … · ↩ revenir au tien ») se touche pour revenir à son propre terrain.
- **Icônes issues des modèles 3D** (depuis la 2.12, en vue 3D) : les cartes de tours et de monstres et la fiche montrent un rendu de trois quarts du modèle 3D (`vignette()` de `rendu3d.js`, petit moteur de rendu à part, fond transparent, images mises en cache) ; les pastilles de rôle et de cibles restent par-dessus. En vue 2D, ou si un modèle manque, les icônes dessinées en 2D restent.
- **Écran d'accueil** (depuis la 2.11) : nuit d'hiver avec montagnes enneigées (SVG) et neige qui tombe (`#ovSnow`, dessinée par la boucle du jeu, positions calculées sans hasard), emblème (écu au flocon, épées croisées), titre doré « Winter Realms », sous-titre « Tower Wars », courte description, trois règles illustrées (Bâtis, Envoie, Résiste, masquées en fin de partie), factions en cartes avec blason en forme d'écu, titre « Lance la bataille » et trois boutons de difficulté avec leur effet (Normal : IA à revenu égal ; Difficile : +25 % ; Brutal : +50 %). Sur téléphone en portrait, les factions passent sur deux colonnes pour que les boutons de difficulté restent visibles sans faire défiler.
- **Choix de la race et fiche de race** (depuis la 2.40) : les 5 boutons de race sont générés depuis `RACES` (blason, nom, description, mécanique propre en étiquette). Sous la grille, le bouton **« 📜 Fiche de la race : … »** (`#ficheRaceBtn`) ouvre la fiche (`#raceFiche`, `ouvrirFicheRace`) :
  - en-tête : blason, nom, description, flèches ‹ › pour passer d'une race à l'autre ;
  - **1. Description** : histoire, mécanique propre, états infligés, forces et faiblesses, **profil en radar** (6 axes, `radarSVG`) ;
  - **2. Les tours** : les 10 tours avec leur icône (rendu du modèle 3D en vue 3D), leur rôle, prix, dégâts par seconde, portée, cibles et effet en clair ;
  - **3. Les combos** : « icône + icône » des deux tours, nom du combo et explication simple ;
  - boutons **Retour** et **Choisir cette race**.
- **Onglets** (2.15 ; icônes depuis la 2.19) : « 🏰 Tours », puis trois onglets d'envoi en **icônes dessinées en code** (`glyphe()`) : **patte** (monstres au sol), **aile** (volants), **étoile** (spéciaux) ; leur nom reste dans `aria-label` et `title`. Les cartes trop chères sont grisées, et leur prix passe en rouge quand l'or manque.
- **Cartes** (2.15) : **l'icône et le prix seulement** (le nom est dans l'étiquette `aria-label`, le reste dans la fiche) ; depuis la 2.19, les cartes de monstres affichent en plus le **gain de revenu** de l'envoi dans une pastille verte « +N » en haut à droite ; la barre en montre 5 à 6 de front et défile. La carte choisie est sertie d'or ; une carte de monstre choisie affiche « ENVOYER ». **Paliers** (depuis la 2.13 ; sur une ligne **au-dessus des onglets** depuis la 2.21, pour que les onglets et les cartes restent à la même place quand on passe des tours aux monstres) : « Palier 1 », « Palier 2 · 300 or », « Palier 3 · 🔒 » ; un palier ouvert se touche pour afficher ses monstres, le palier suivant affiche son prix (un toucher l'achète), le dernier reste « 🔒 » tant que le précédent est fermé. Seuls les monstres du palier affiché sont proposés. Les nouveaux monstres sans dessin 2D dédié sont dessinés en silhouette simple à leur couleur (`dessinMonstre`) ; en 3D, ils ont leur modèle.
- **Une seule fiche, seulement quand on choisit** (2.1, refaite en 2.15) : au-dessus des onglets, elle décrit l'élément choisi et rien d'autre ; **sans choix, elle disparaît**. Le × la referme et annule le choix.
  - **tour à construire** : nom, type, rôle, ⚔ dégâts par seconde, ◎ portée en cases, cibles (« sol et air » ou « sol uniquement »), prix, temps de construction, effets (explosion de zone, ralentissement, souffle en cône, corps à corps, révèle les Spectres, magique), bonus de faction chiffré (calculé à partir de `FACTION_BALANCE`), et le geste suivant : « Touche deux fois une case du terrain pour construire ». **Pendant l'aperçu d'une construction** (depuis la 2.32), la fiche se réduit (classe `compacte` : sans la ligne de détails ni consigne). Depuis la 2.34, la consigne « Touche deux fois une case… » de la fiche n'apparaît plus après le premier aperçu de la partie ;
  - **tour posée** : les mêmes informations au niveau actuel, le gain du niveau suivant, et les boutons **Améliorer · prix** et **Vendre · +or** ; s'il existe d'autres tours pareilles, la ligne « Touche encore la tour : améliorer les N pareilles d'un coup » (2.32) ;
  - **lot de tours** (2.32, voir « Améliorer en lot ») ;
  - **monstre** : catégorie, capacité, palier, PV actuels (ils montent avec le temps), vitesse, revenu gagné, prix, et « Chaque toucher sur la carte envoie 4 × … à chaque adversaire ».
  - **Fiche moins haute** (depuis la 2.35) : la ligne de détails (temps de construction, niveau suivant, effets, bonus de faction) tient sur **une seule ligne**, coupée par « … » ; la toucher la déplie ou la replie (`detailsOuverts`, gardé d'une fiche à l'autre).
  - **Depuis la 2.40**, la fiche d'une tour donne son rôle (et « ultime »), « air uniquement » pour un anti-aérien dédié, « — » en dégâts pour une tour qui ne tire pas, l'effet en clair (`T.txt`), l'**état de la tour posée** (Cohésion, Fureur et Rage, Chauffe et surchauffe, Croissance), les **combos** où elle entre (« Combo Jugement avec Inquisiteur ») et la mécanique de la race.
- **États des monstres** (depuis la 2.40, `pastillesEtat`) : au-dessus de chaque monstre (sous la barre de vie en 3D), une pastille par état, cerclée de sa couleur : poison (vert, nombre de doses), Marqué (or, « ! »), Maudit (violet), immobilisé (brun), Trempé (bleu), Brisé (orange, nombre de points), Brûlant, Pestiféré, Maléfice, Abattu, saignement.
- **Combos** (2.40) : texte flottant nommé, plus gros que les gains d'or (« CONDUCTION ! », « FLORAISON ! », « RAGE ! »…). Éclairs colorés (chaînes, frappes du ciel du Cœur de l'Orage), traits droits (Baliste céleste, Grondeterre, Rayon de l'Aube), mines runiques et morts relevés (squelettes, Colosse d'os ; en 3D, modèles du Squelette du givre et du Colosse de pierre) sont dessinés en 2D et en 3D.
- **Âmes** (2.40) : pour la Cour des Ossements, une pastille ✦ dans le bandeau (`#ames`) compte les âmes récoltées (0 à 30).
- **Tour choisie toujours visible** (depuis la 2.35, en 3D, `garderVisible`) : quand on choisit une tour posée (ou un lot, ou l'aperçu d'une construction) et que sa case se trouve sous la fiche ou contre le bandeau, la vue **glisse en douceur** juste assez pour la montrer au-dessus de la fiche (à 28 px ; au-dessus de la consigne `#aideBat` de la 2.34 quand elle est affichée), hors des flèches de rotation (`amener` de `rendu3d.js`). Avant, la fiche d'une tour posée près du bas de l'écran recouvrait la tour elle-même. Rien ne bouge si la case est déjà visible ; glisser le doigt arrête le mouvement.
- **Pastilles de rôle** (depuis la 2.3) : sur l'icône de chaque carte de tour (56 × 46 px, fonction `towerIcon`) et dans la fiche, des pastilles **rondes, cerclées de la couleur du rôle** (depuis la 2.19 ; avant, carrées à cadre doré, ce qui diluait la couleur) (glyphes dessinés en code, fonctions `drawBadge` et `drawTowerBadges`, table `BADGE`) :
  - **en haut à droite, le rôle** (archétype `T.s`) : flèche (Archer), épée (Garde), flocon (Givre), bombe (Canon), flamme (Flammes), étoile (Mage) ;
  - **en bas à gauche, les cibles** : montagne = sol uniquement (`T.gr`), aile déployée (redessinée en 2.19) = sol et air ;
  - **petite étoile violette** à côté : tour magique (`T.mag`), sans effet sur le Briseur de runes.
- **Construire une tour** (deux touchers depuis la 2.2 ; choix préalable depuis la 2.15). Le concepteur a choisi de garder **deux touchers sur la case** plutôt qu'un bouton « Construire » dans la fiche (2.15) :
  - **choisir la tour** en touchant sa carte (rien n'est construit) ; sans tour choisie, toucher une case affiche « Choisis d'abord une tour en bas de l'écran » ;
  - **1er toucher** sur une case libre : **aperçu** (tour fantôme, cercle de portée, case surlignée en or) et, **au premier aperçu de la partie seulement** (depuis la 2.34, `#aideBat`), la consigne « Touche encore la case pour construire » **calée entre les deux flèches de rotation** ; elle disparaît à la pose ou à l'annulation et ne revient plus de la partie (avant la 2.32, une bulle au milieu du terrain à chaque aperçu ; en 2.32, la consigne dans la fiche). Rien n'est construit ni payé ;
  - **2e toucher sur la même case** : construction. Il n'y a pas de délai imposé entre les deux touchers ;
  - toucher une **autre case** déplace l'aperçu ; choisir une autre tour dans la barre change la tour de l'aperçu ; changer d'onglet ou de terrain l'annule ;
  - une case **impossible** (or insuffisant, chemin bloqué, case occupée) est signalée **dès le 1er toucher**, sans aperçu. Le contrôle (`peutConstruire`) reprend celui de `Board.place` sans rien modifier ;
  - un toucher compte au relâcher, s'il n'a pas glissé (doigt ou souris) : un glissement ne construit jamais rien ;
  - **Maj + clic** (depuis la 2.24, souris seulement) : construit **en un seul clic**, sans aperçu, si la case est possible (sinon, le même refus qu'au 1er toucher). La tour reste choisie, ce qui permet d'enchaîner les poses. Avec une souris (`pointer:fine`), la fiche le rappelle : « … (Maj + clic : en un seul clic) ». Sur écran tactile, rien ne change.
- **Envoyer des monstres** (2.15) : le **1er toucher** sur une carte de monstre la choisit (fiche, « ENVOYER ») sans rien envoyer ; **chaque toucher suivant** envoie un groupe. **Pas d'envoi automatique en rafale, c'est voulu** (choix du concepteur) : marteler la carte fait partie du plaisir. Chaque envoi répond par un rebond de la carte, une petite vibration et un compteur « ×2, ×3… » dans le message quand on enchaîne le même monstre (moins de 1,5 s entre deux envois).
- **Se déplacer et pivoter** (2.15, vue 3D) : **glisser le doigt** (ou la souris, bouton appuyé) déplace la carte **comme une appli de cartes** : le sol reste sous le doigt, donc glisser vers la droite montre ce qui est à gauche ; lâchée vite, la carte continue un peu sur sa lancée (élan gardé : choix du concepteur, 2.15). Deux **flèches** rondes, en bas à gauche et à droite au-dessus du dock, font **pivoter la vue d'un huitième de tour (45°)**, en douceur, autour du point regardé. Plus de pincement, de molette ni de bouton « Vue d'ensemble » : la vue tactique a une hauteur fixe (§15.2). En 2D, le plateau entier tient à l'écran, sans déplacement ni rotation (les flèches sont cachées).
- **Toucher une tour** : ouvre sa fiche (voir plus haut), avec les boutons Améliorer et Vendre, et le × pour la fermer.
- **Améliorer en lot** (depuis la 2.32, `ouvrirLot`, `ficheLot`, `LOT_MAX`) : **toucher deux fois une tour** (ou double-cliquer) choisit **toutes les tours du même type et du même niveau**, jusqu'à **10** (les plus proches d'abord), hors tours en chantier et tours au niveau 5.
  - Sur le terrain, chaque tour du lot a un cadre doré qui pulse ; dans la fiche, « N × nom · niveau n → n+1 », le prix unitaire et le total, puis **une rangée d'icônes, une par tour**.
  - Le bouton **« Améliorer les N · prix »** les améliore toutes d'un coup (une action `upgrade` par tour, donc rien ne change côté `sim.js` ni serveur). « Annuler », le ×, ou toucher à nouveau la tour reviennent à la fiche d'une seule tour.
  - **Si l'or ne suffit pas pour toutes**, les icônes des tours qui ne seront pas améliorées **rétrécissent** (et pâlissent), et le bouton devient « Améliorer k / N · prix » ; les plus proches de la tour touchée passent en premier. La fiche suit l'or en direct.
- **Panneau « Mes tours » et file d'améliorations** (depuis la 2.37, `parc`, `FILE`, `fileTick`) : pour améliorer beaucoup de tours d'un coup, surtout en fin de partie.
  - Le bouton **« Mes tours »** (sous le bandeau, à gauche, en miroir du bouton Adversaires) ouvre un panneau par-dessus le terrain : **une ligne par type de tour** posé (icône, nom, nombre, répartition par niveau, « max » pour le niveau 5). Toucher une ligne la **coche** ; « Toutes » / « Aucune » cochent tout. Les tours cochées sont encadrées d'or sur le terrain.
  - **« Amener au niveau » 2, 3, 4 ou 5**, puis **« Ajouter à la file »**. Le résumé donne le nombre de tours, d'améliorations et le prix total, et combien l'or actuel en paie tout de suite. Les tours déjà au niveau visé ou plus sont ignorées.
  - **File d'attente** : chaque tour monte **niveau par niveau** (une tour au niveau 1 visée au 4 fait 2, puis 3, puis 4), **la moins avancée d'abord** (à égalité, l'ordre le plus ancien), dès que l'or suffit et que son chantier est fini. La file s'arrête à la première amélioration qu'elle ne peut pas payer : **faute d'or, elle dépense ce qu'elle peut et le reste attend les revenus suivants**. Un ordre terminé disparaît (« File : … au niveau N ✓ »).
  - Dans le même panneau, chaque ordre montre ses tours, une jauge (améliorations faites sur le total) et l'or qui reste à payer ; **×** annule l'ordre, **« Tout annuler »** vide la file. Les travaux déjà payés continuent.
  - Sur le terrain, un **chevron doré** marque chaque tour qui attend dans la file ; sa fiche dit « ⏫ Dans la file : vers le niveau N ». Le bouton affiche le nombre d'améliorations restantes (« ⏫ N »).
  - Une tour vendue sort de la file. La file est vidée à chaque nouvelle partie et ne joue plus en fin de partie. Toucher le terrain referme le panneau sans rien construire ; il se ferme aussi quand on ouvre les Adversaires ou le menu.
  - Tout se passe dans la page (`index.html`) : une action `upgrade` par niveau, donc rien ne change côté `sim.js` ni serveur. En ligne, une amélioration au plus toutes les 0,35 s (l'or vient des instantanés), sans message d'erreur.
- **Barre des cartes à la souris** (2.32) : sur PC, la **molette** fait défiler horizontalement la barre des tours et des monstres, et on peut la faire **glisser** bouton appuyé (un glissement ne choisit pas de carte). La position de défilement est gardée quand la barre est redessinée (choix d'une carte). Au doigt, rien ne change.
- **Astuce** au lancement d'une partie (9 s, ou jusqu'au premier geste) : en 3D, « Glisse le doigt pour déplacer la carte ; les flèches la font pivoter. Choisis une tour en bas, puis touche deux fois une case. »
- **Vue 3D** (par défaut depuis la 2.8 ; seule vue proposée au joueur depuis la 2.22) : l'accueil n'a plus de lien vers la 2D, qui reste accessible avec `?rendu=2d` (secours et tests). En 3D, il faut toucher le **pied** d'une tour (sa case au sol) pour l'ouvrir.
- **Fin de partie** (depuis la 2.23, en solo ; en ligne, rien ne change : écran de fin puis retour au salon) : une fenêtre (`#fin`) affiche **Victoire !** ou **Défaite**, la durée et la difficulté, puis :
  - un **tableau des 4 joueurs**, classés (gagnant, terrains encore debout par vies, puis éliminés du dernier au premier) : tours en place, longueur du **chemin** (cases du labyrinthe, de l'apparition à la sortie), **vagues** envoyées (groupes de 4), monstres **tués** sur son terrain, **revenu** final ;
  - une **courbe du revenu** de chaque joueur, un point par versement (toutes les 10 s) ;
  - un résumé pour le joueur : tours posées, or dans ses tours, or envoyé en monstres, vies perdues, tour la plus chère ;
  - **Regarder la carte** : la partie reste figée et on se balade sur les labyrinthes (glisser, flèches de rotation, bouton Adversaires pour changer de terrain). Toucher une tour, sur n'importe quel terrain, ouvre sa fiche sans boutons (or investi). Les terrains éliminés gardent leurs tours, avec une simple étiquette « Éliminé ». La console du bas laisse place au bouton « 🏁 Partie terminée · stats et quitter », qui rouvre la fenêtre ;
  - toucher une ligne du tableau ouvre le terrain de ce joueur ;
  - **Quitter** : écran de fin habituel (Rejouer en Normal, Difficile ou Brutal).
  - Les chiffres viennent de `Board.st` (`sim.js`) : `pose` (tours posées), `env` et `envOr` (envois), `tue` (monstres tués), `rev` (revenu à chaque versement), `mort` (temps de l'élimination, −1 sinon). Ils n'influencent pas le jeu et ne sont pas transmis par le serveur.
- **Quêtes bonus** (depuis la 2.38, `annonceQuete`, `queteTick`, `queteLog`) :
  - au lancement, bannière **« Quête bonus ! »** dans le style des annonces de départ (bande à liseré bleu glacier, logo **trophée**), avec le titre, la règle et la récompense (« +N or ») ; son `cor` ;
  - pendant la quête, une **pastille** (`#quete`) sous le bandeau, centrée sous les boutons « Mes tours » et « Adversaires » : trophée, titre, temps restant, **ton score et ton rang** (« Toi : 38 cases · 2e ») ; cadre vert quand tu mènes, chrono rouge dans les 10 dernières secondes ; la toucher rappelle la règle ;
  - à la fin, bannière **« Fin de la quête »** : « Bravo, c'est toi ! » (son `win`, vibration), sinon le nom du gagnant (ou « X et Y se partagent… ») et l'or gagné, ou « Raté ! » si personne ne gagne ; « +N or » s'affiche aussi au-dessus du château du gagnant ;
  - la fenêtre de fin de partie a une colonne **Quêtes** (quêtes gagnées) et le résumé du joueur donne ses quêtes et leur or.
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
- La page (`NET` dans `index.html`) envoie des actions (`{t:'act', a:{type, x, y, k}}`) et dessine les instantanés avec les fonctions de dessin existantes. Elle lisse les positions des monstres et des projectiles entre deux instantanés, et recalcule le chemin (`Board.dist`) à partir de la grille des tours. L'instantané ne transmet pas la case visée par un monstre (`tx`, `ty`) : la page prend la case la plus proche de sa position (depuis la 2.5.1), ce qui suffit au contrôle de pose `peutConstruire` (le serveur valide de toute façon chaque pose).
- Messages du client : `hello`, `faction`, `diff`, `start`, `act`. Messages du serveur : `lobby`, `start`, `snap`, `res`.
- Dans l'instantané, chaque tour est un tableau `[x, y, k, lv, inv, a, sw, stun, b, bt]` ; `b` et `bt` (temps de chantier restant et total, depuis la 2.4) valent 0 hors chantier.
- Depuis la 2.40, le 6ᵉ champ d'un monstre porte **tous ses états en bits** (`etats(c)` : ralenti 1, hâté 2, soigné 4, caché 8, poison 16, Marqué 32, Maudit 64, immobile 128, Trempé 256, Brisé 512, Brûlant 1024, Pestiféré 2048, Maléfice 4096, Abattu 8192, saignement 16384), et chaque terrain transmet ses **âmes** (`am`), ses **morts relevés** (`al : [x, y, gros, sens]`) et ses **mines** (`mi : [x, y]`).
- Depuis la 2.38, l'instantané transmet aussi la quête bonus en cours, `qu: {id, t0, fin, or, cible, sc}` (scores en direct, `null` pour un terrain éliminé) ou `null` ; son début et sa fin passent par `log`.
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
2. **Tout est produit par du code** : les **sons** sont des fichiers **générés par un script versionné** (`art/outils/generer-sons.js`, §16), à partir des consignes de `assets/audio/catalogue.json`, avec **ElevenLabs** sur une offre payante (2.29 : usage commercial autorisé, et conservé après la fin de l'abonnement pour ce qui a été généré pendant) ; les sons synthétisés restent le secours. Seule exception, voulue par le concepteur (2.16) : la **musique de fond**, trois thèmes MP3 qu'il a composés avec Suno (`assets/musique/`). Le rendu 2D est dessiné en code (Canvas 2D). Les **modèles 3D** (depuis la préparation de la 3D) sont des fichiers GLB **générés par des scripts Blender versionnés** dans `art/` (§15), jamais retouchés à la main ; **aucun asset externe sans licence CC0**.
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
| `node tests/tout.js` | Tout : simulation (mécaniques et **une partie entre IA par difficulté**) et parcours mobile dans un navigateur. Depuis la 2.35, les fichiers de test tournent **en parallèle** (voir §12.2) : la durée est celle du parcours navigateur | ≈ 2 min |
| `node tests/tout.js --simulation` | Simulation seule. C'est ce que GitHub lance à chaque Pull Request. (`--rapide` en est un synonyme.) | ≈ 10 s (8 s sur 22 cœurs, 13 s sur 4 ; 24 s et plus avant la 2.35) |
| `node tests/tout.js --complet` | Ajoute les **15 parties entre IA complètes** (5 factions × 3 difficultés), jouées en parallèle. À lancer à la main après un changement d'équilibrage ou d'IA ; jamais lancé par GitHub. | ≈ 30 s en simulation seule (sur 22 cœurs) |
| `node tests/tout.js --un-par-un` | Un fichier de test après l'autre, comme avant la 2.35 (les parties entre IA restent en parallèle). Utile si un test semble dépendre de la charge de la machine | ≈ 20 s en simulation seule |
| `node tests/bilan.js [version] [--complet]` | Les **trois bilans** dans `rapports/bilan.html`, avec la comparaison visuelle par rapport à `version` (par défaut `origin/main`). `--complet` : 15 parties au lieu de 3. | ≈ 4 min |
| `node tests/captures.js` | 6 captures du vrai jeu, en 3D (5 écrans en portrait, et l'accueil en paysage), dans `captures/actuel/` | ≈ 1 min 30 (WebGL logiciel) |
| `node tests/captures.js --2d` | Les mêmes captures avec la 2D de secours, dans `captures/2d/` | ≈ 1 min |
| `node tests/comparer-visuel.js [version]` | Avant/après visuel seul, en 3D, dans `captures/comparaison/` | ≈ 5 min (WebGL logiciel) |
| `node tests/outils/audit-doc.js` | Compare les tableaux chiffrés de ce document au code et liste les écarts, sans rien corriger | 1 s |
| `node tests/outils/banc-tours.js [--avant <réf git>] [--niveaux 1,5] [--coeurs N]` | **Banc d'essai des tours** (§12.2), à lancer à la main pour l'équilibrage (ni dans `tout.js` ni sur GitHub) : rendement de chaque tour (dégâts pour 100 or investis), du niveau 1 au niveau 5, dans 7 vagues types ; avec `--avant`, comparaison avant → après ; `--niveaux 1,5` pour un essai rapide. Réparti sur tous les cœurs du processeur. Détail dans `rapports/banc-tours.md` | ≈ 1 min 30, ≈ 3 min avec `--avant` (sur 22 cœurs) |
| `node tests/outils/banc-races.js [--parties N] [--coeurs N]` | **Banc des races** (2.40, §5.3) : les 5 races s'affrontent, jouées par l'IA ; points par partie de chaque race (critère 1,2 à 1,8). `WR_MODIF="<code>"` essaie un réglage sans toucher à `sim.js`. À la main, ni dans `tout.js` ni sur GitHub | ≈ 1 min 30 (4 graines) |
| `node tests/outils/arene-ia.js [--avant <réf git>] [--parties N] [--difficulte 0-2] [--coeurs N] [--vies V] [--moteur <sim.js>]` | **Arène des IA** (§12.2, depuis la 2.33), à lancer à la main après un changement d'IA (ni dans `tout.js` ni sur GitHub) : l'IA actuelle affronte celle d'une autre version (par défaut `origin/main`) sur N graines × 2 parties, et donne les points, les victoires et l'écart avec son erreur type. Réparti sur tous les cœurs | ≈ 4 min pour 21 graines (42 parties, sur 22 cœurs) |
| `python art/outils/generer.py [asset…] [--verifier] [--apercus dossier]` | Génère (ou vérifie) les fichiers 3D à partir des scripts de `art/` ; demande Blender 5.3 (`pip install bpy==5.3.0`) et, dans le cloud, Node.js pour la compression de secours | quelques s par asset |

Seul **Node.js** (version 22) est nécessaire. Les tests navigateur utilisent en plus **Playwright** et Chromium, présents dans l'environnement de Claude mais **pas ajoutés au projet**. Sans eux, ces tests sont ignorés avec un message clair.

### 12.2 Ce que contient `tests/`
- **Tests en parallèle** (depuis la 2.35) : `tout.js` lance chaque fichier de test dans son propre processus, autant à la fois que de cœurs du processeur moins un (`--test-concurrency`), les plus longs d'abord (parcours navigateur, parties entre IA, labyrinthe). Les tests d'un même fichier restent l'un après l'autre. Chaque fichier charge son propre moteur avec sa graine : les résultats ne changent pas. **Mesures de temps réel lancées seules** (depuis la 2.36, liste `SEULS` de `tout.js`) : le test de durée de la génération du labyrinthe (moins de 10 ms par tranche, moins de 150 ms au total) est dans son propre fichier, `labyrinthe-duree`, lancé **après** les autres et seul. En parallèle des parties entre IA, sur les 4 cœurs de GitHub, il mesurait 160 à 190 ms et échouait au hasard.
- `simulation/` : les tests du moteur (`sim.js`). Ils vérifient que le jeu fonctionne (mécaniques, formules, parties qui se terminent). **Il n'y a pas de moteur figé ni de parties enregistrées** (supprimés en 2.5) : un changement d'équilibrage ou d'IA ne fait échouer que les tests qui décrivent précisément la mécanique modifiée, et on met ces tests à jour dans le même commit.
  - `tables` : forme des tables (5 races de 10 tours, chaque tour fidèle à sa définition dans `RACES`, 50 tours, 75 monstres…), statistiques valides, et chaque tour recalculée à partir des formules. Les chiffres eux-mêmes peuvent changer librement.
  - `races` (2.40) : règles d'équilibrage centrales (radar, couverture, pas de domination, plafonds, une seule ultime) et mécaniques des 5 races (Cohésion, Comptoir, Jugement, filet, chaîne d'éclairs et Conduction, Fureur et Rage, Maléfice, poison et Floraison, Croissance, Forge, Brèche, Chauffe, mines, âmes et morts relevés, peste et Épidémie, Faucheuse), états en bits, et une partie de 12 min où chaque race construit et améliore.
  - `construction`, `chantier` (temps de construction, depuis la 2.4), `deplacements`, `combats`, `economie`, `vagues` (avec l'IA), `fin-de-partie` : les mécaniques. Les tests qui ont besoin d'une tour active appellent `pret(b)`, qui fait avancer le terrain jusqu'à la fin des chantiers.
  - `parties-ia` : **une partie complète par difficulté** (Alliance en Normal, Horde en Difficile, Sylvestres en Brutal ; les 15 avec `--complet`) qui doit se terminer en moins de 30 min de jeu, sans valeur invalide, avec des tours construites et des attaques ; plus les 2 premières minutes d'une partie rejouées deux fois avec la même graine, qui doivent être identiques. **Depuis la 2.35, toutes ces parties sont jouées en même temps** (`jouerEnParallele` de `tests/outils/parties.js` : une partie par fil `worker_threads`, au plus une par cœur moins un), avec exactement les mêmes résultats qu'une à une (vérifié sur les empreintes finales) ; le bilan gameplay rejoue de la même façon les parties avec le moteur d'avant.
  - `quetes` (2.38) : table des 10 quêtes, première à 1:30 et pause de 3 à 4 min, tirage sans remise, récompense, chaque course et photo (gagnant, égalité partagée, personne), Clicker fou retiré quand la place manque, envoyeur des monstres pour le Facteur, cibles de Gonflette et Frozen au-dessus du meilleur, comportement des IA qui jouent la quête, et une partie entre IA de 10 min où les quêtes se suivent.
  - `labyrinthe`, `labyrinthe-partie` (2.35 : le test « en partie », le plus long, est dans son propre fichier pour tourner en parallèle des autres) et `labyrinthe-duree` (2.36 : la mesure de durée, lancée seule).
- `simulation/modeles-3d.test.js` (2.7) : un modèle 3D pour chaque tour (`tours/<faction>-<j>`) et chaque clé de monstre (`monstres/<g>`), portail et château présents, monstres animés (`marche` ou `vol`), pièce `Tourelle` sur les tours qui visent, compression meshopt.
- Variable `WR_CANAL` : utiliser un navigateur déjà installé à la place du Chromium de Playwright (par exemple `WR_CANAL=msedge` sur Windows). `NODE_PATH` peut pointer vers un Playwright installé hors du dépôt. Edge demande l'icône d'onglet `/favicon.ico`, que le jeu n'a pas : depuis la 2.35, cette erreur 404 est ignorée par le test « aucune erreur JavaScript ».
- **Glissements de test** (`glisser` de `tests/outils/navigateur.js`, depuis la 2.36) : les événements tactiles sont horodatés (0,3 s de geste, puis 0,2 s immobile avant de lever le doigt). Sans cela, Chromium y voit un lancer (« fling ») et avale le toucher suivant, comme un vrai écran tactile qui arrête un défilement.
- Variable `WR_GPU=1` : les tests 3D utilisent la **vraie carte graphique** de la machine au lieu de SwiftShader : plus rapide (parcours 3D en environ 20 s au lieu d'1 min) et plus proche d'un téléphone. Seulement sur un PC qui a une carte graphique (GitHub et le cloud n'en ont pas) ; les captures avant/après restent comparables tant qu'elles sont prises dans la même séance.
- `navigateur/parcours.test.js` (refait en 2.15 ; **en 3D depuis la 2.29**, il réunit l'ancien parcours 2D et l'ancien `parcours-3d.test.js`) : le **parcours automatisé** d'un joueur dans le vrai jeu (vue 3D), dans Chromium au format téléphone, en portrait (390 × 844) : accueil sans lien vers la 2D, chargement de WebGL et des modèles, caméra tactique en perspective, faction, difficulté, disposition (terrain plein écran, bandeau, dock, flèches de rotation, plateau dessiné), pas de construction sans tour choisie, choix d'une carte et fiche, construction en deux touchers (tour fantôme et portée, confirmation, déplacement de l'aperçu) et refus, fiche d'une tour posée en touchant son pied (Améliorer, Vendre, ×), envoi (1er toucher : choix, toucher suivant : envoi, compteur ×2) et monstres en 3D chez l'adversaire, paliers, adversaires (lecture seule, bannière), revenu, glisser le doigt pour déplacer la carte sans construire, rotation d'un huitième de tour dans les deux sens, pose exacte dans une vue pivotée, panneau « Mes tours » et file d'améliorations (2.37), quêtes bonus (2.38 : bannière, pastille, gagnant, or versé), menu (son, musique, gestes, quitter en deux touchers), musique (un des 3 thèmes dès le premier toucher, puis enchaînement en boucle), aucune erreur JavaScript ; en paysage (844 × 390), le message « Tourne ton téléphone » ; **secours 2D** : si la 3D ne se charge pas (`rendu3d.js` rendu introuvable), le jeu le dit, passe en 2D et on peut y construire ; `?rendu=2d` force la 2D. WebGL y tourne en **rendu logiciel SwiftShader** (`lancer({webgl:true})`), sans carte graphique. **Avance rapide allégée** (`avancer`, 2.29) : la partie avance image par image, mais la vue 3D n'est redessinée que 4 fois par seconde de jeu, puis à l'instant exact ; sinon le navigateur de test plantait (« Target crashed ») vers 30 s de jeu depuis le paysage de la 2.26, alors que le jeu tourne normalement sur téléphone. **Un plantage du navigateur de test seul n'est pas un bug du jeu** : le reproduire avec `WR_GPU=1` ou sur un téléphone avant de conclure. Durée : environ 2 min (35 s avec `WR_GPU=1`). **Ce n'est pas une garantie de compatibilité avec tous les téléphones** : Safari sur iPhone, les anciens Android et les vrais écrans tactiles ne sont pas testés.
- `outils/` : chargement du moteur dans un environnement isolé, hasard à graine, serveur web local, pilotage du navigateur, affichage en français, audit de la documentation.
- `outils/banc-tours.js` (2.20) : **banc d'essai des tours**, pour l'équilibrage. Une tour seule dans un labyrinthe en serpentin (deux emplacements : dans un mur et dans un virage en épingle), montée du niveau 1 au niveau 5, voit passer 7 vagues types de la 8e minute : groupe de 4 Ogres, Ogre seul, 12 Ogres, 4 Vouivres (volants), 4 Scarabées (blindés), 4 Inquisiteurs (anti-magie) et une **foule** de 40 Ogres d'un coup (comme une vague d'IA). Les monstres sont rendus quasi immortels pour mesurer tous les dégâts infligés. Indice 100 = médiane des 50 tours au niveau 1 dans le même scénario. Limites : le ralentissement du Givre n'aide aucune autre tour, et la Frénésie de la Horde ne se déclenche pas. **En parallèle** (depuis la 2.31) : les mesures sont réparties sur les cœurs du processeur (`worker_threads`, un cœur de moins que la machine, option `--coeurs`), les plus longues (la foule) en premier ; chaque mesure repart de sa propre graine et remet à zéro le compteur des monstres (`regrainer`, ajouté à `tests/outils/moteur.js`), donc le résultat est **identique** sur 1 cœur ou sur 20 (vérifié). Avec les monstres qui s'écartent (2.25), une comparaison `--avant` prenait 20 à 25 min sur un cœur.
- `outils/arene-ia.js` (2.33) : **arène des IA**, pour mesurer un changement d'IA. Le moteur de jeu est celui de la version actuelle ; la section « IA » du `sim.js` d'une autre version (entre « ---------- IA ---------- » et « ---------- partie ---------- ») est chargée à côté, dans sa propre portée, et chaque terrain est joué par l'une ou l'autre IA (l'IA d'avant doit rester compatible avec le moteur actuel). 4 terrains, 2 par IA en sièges alternés, puis la même partie (même graine, mêmes factions) sièges échangés : chaque IA joue chaque faction à chaque place. Les 4 sièges sont « humains » pour le moteur (ni bonus de difficulté, ni fin de partie à l'élimination des humains) mais joués par une IA ; la difficulté ne règle que la génération du labyrinthe. Classement par moment d'élimination (au bout de 30 min, par les vies), 3, 2, 1, 0 points du 1er au 4e : 1,50 en moyenne si les deux IA se valent. Contrôle : la même IA des deux côtés donne exactement 1,50 / 1,50. `--vies V` donne V vies à chaque terrain (40 par défaut) : avec 400 vies, les parties durent jusqu'à la fin de partie (toutes les tours au niveau 5), qui sinon n'arrive presque jamais entre IA depuis la 2.33 (les vagues font perdre beaucoup de vies vers 5 à 8 min). `--moteur` compare un autre `sim.js` (une variante en essai) à la place de la version actuelle.

### 12.3 Reproductibilité sans toucher au jeu
Les tests chargent `sim.js` dans un environnement isolé et y remplacent `Math.random` par un **hasard à graine** (`tests/outils/hasard.js`). Une même graine donne donc toujours la même partie. **Tous les tests utilisent une graine fixe** (1 par défaut, une graine par partie entre IA) : un test ne dépend jamais du vrai hasard, donc il réussit ou échoue toujours de la même façon. Dans le navigateur, le même hasard est injecté avant le chargement de la page, et l'horloge est figée. **Deux suites séparées** (depuis la 2.29) : une pour la simulation (appels venant de `sim.js`), une pour tout le reste (interface, sons, three.js). En 3D, three.js tire un nombre à chaque objet créé et les modèles se chargent en temps réel : avec une suite commune, la partie changeait d'un lancement à l'autre (autres vagues des IA, autre or). **Le jeu publié n'est pas modifié.**

### 12.4 Règles
1. Quand une évolution **change volontairement une mécanique**, on met à jour les tests qui la décrivent dans le même commit. Le bilan gameplay (avant → après, par rapport à `main`) montre ce qui a changé.
2. Un désaccord entre le code et ce document est **signalé, pas corrigé d'office** : le concepteur décide.
3. Ne jamais désactiver ou ignorer un test pour obtenir un résultat vert.
4. **Pas de simulation quand le gameplay ne peut pas changer** : pour une évolution qui ne touche ni `sim.js` ni `index.html` (documentation, règles, outillage GitHub), le bilan gameplay est « identique à `main` » sans lancer `node tests/tout.js` ; la vérification « Tests de simulation » de la PR suffit.

### 12.5 Les trois bilans
Chaque évolution est présentée avec trois bilans **séparés** (`node tests/bilan.js`) :
| Bilan | Contenu | Verdicts |
|---|---|---|
| 🔧 **Technique** | Les tests s'exécutent, le parcours mobile fonctionne, aucune erreur JavaScript. Liste des fichiers modifiés. | ✅ réussi / ❌ en échec |
| 🎮 **Gameplay** | Mécaniques vérifiées, statistiques changées et parties entre IA (3, ou 15 avec `--complet`), comparées au `sim.js` de `main` (avant → après), écarts entre la documentation et le code | ✅ identique à `main` / ⚠️ changé : **à valider par le concepteur** |
| 🎨 **Visuel** | Captures (portrait, et l'accueil en paysage), avant \| après \| différences, pourcentage de pixels changés | ✅ identique / ⚠️ changé : **à valider par le concepteur** / ⏸ non vérifiable |

**Une réussite technique ne vaut jamais validation du gameplay ni du rendu.** Le gameplay et le visuel ne sont « validés » que par le concepteur.

### 12.6 Conditions de la comparaison visuelle (contre les fausses différences)
- **Vue 3D** (depuis la 2.29) : les captures montrent le vrai jeu ; la 2D seulement si la version d'avant n'a pas de 3D (avant la 2.7). L'« avant » est extrait de git **en entier** (jeu, three.js, modèles, sons, images ; sans `art/`, `tests/`, `server/`) : avant la 2.29, seuls `index.html` et `sim.js` l'étaient, et la version d'avant tournait sans 3D ni sons (erreurs 404 et fausses différences).
- **Flocons en 3D** (depuis la 2.30) : la position de chaque flocon qui tombe ne dépend que du temps (`fairePleuvoir(temps)` dans `rendu3d.js`). Avant, ils avançaient un peu à chaque image dessinée : deux captures de la même version différaient d'environ 0,1 % (points isolés), au-dessus du seuil du témoin, et la comparaison 3D était signalée « non fiable ». Témoin depuis : 0,00 %. Face à une version d'avant ce correctif, seuls les flocons diffèrent (environ 0,1 %, points isolés).
- **Même machine, même navigateur, même séance** : l'« avant » (extrait de git) et l'« après » sont capturés l'un après l'autre par le même Chromium. On ne compare **jamais** des images faites sur deux machines différentes, ni des images enregistrées dans le dépôt.
- **Même scénario** : graine 12345, Alliance, Normal, 4 tours posées en (5,6), (7,6), (5,10) et (7,10), capture à 35 s de jeu, puis fiche de la tour (5,6), puis panneau des adversaires (avant la 2.15 : zoom à deux doigts). Depuis la 2.15, une carte de tour est touchée avant de construire, et en paysage seul l'accueil est capturé.
- **Horloge figée** : le temps du navigateur est en pause et n'avance que sur commande. Sans cela, les animations (pointillés du chemin, barre de revenu) diffèrent d'une capture à l'autre. Au chargement, l'horloge est en plus **alignée sur exactement 2 000 ms** : l'horloge simulée de Playwright démarre avec un décalage variable selon les passages, ce qui suffisait à décaler les animations. Avant la 2.29, l'alignement visait 200 ms ; en 3D, le chargement est plus long et l'horloge avait parfois déjà dépassé ce point (jusqu'à 986 ms) : l'alignement était sauté et toute la partie décalée.
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
- **Budgets** (`art/budgets.json`) : tour ≤ 9 000 triangles et 300 Ko (depuis la 2.40, validé par le concepteur), monstre ≤ 3 000 triangles et 150 Ko, décor ≤ 6 000 triangles et 300 Ko, total ≤ 16 Mo (8 Mo avant la 2.40).
- **Contrôles** : `tests/simulation/assets3d.test.js` (chaque PR, sans Blender : manifeste complet, aucun fichier en retard sur son script, GLB valides, budgets) ; action GitHub **« Assets 3D »** (`.github/workflows/assets-3d.yml`, PR qui touchent `art/` ou `assets/3d/`) : régénère tout avec Blender 5.3, vérifie et joint les images d'aperçu.
- **Qui fait quoi** : la conception d'un nouveau modèle ou d'un nouveau style se fait de préférence sur le PC du concepteur (Blender + MCP, en direct ou via Remote Control) ; les retouches mineures peuvent être faites par n'importe quel contributeur ou une session cloud, en modifiant le script puis en régénérant.
- **Repli obligatoire** : le jeu doit fonctionner même si un modèle manque (un contributeur peut ajouter un monstre avant son modèle 3D).
- **Fins de ligne** : `.gitattributes` impose LF dans le dépôt (les empreintes vérifiées par les tests en dépendent) et traite les fichiers 3D et images comme binaires. Les fichiers `.blend` ne sont pas versionnés.

### 15.1 Modèles du jeu : style et pièces communes (depuis la 2.7)
- **Style validé par le concepteur** : heroic fantasy flamboyante, cartoon mais fin (proportions trapues, épaulières, détails sculptés, liserés dorés), couleurs vives, **dégradé peint** sur chaque modèle (sombre en bas, clair en haut, léger grain), dans l'esprit d'un jeu de stratégie fantasy classique mais avec des modèles originaux.
- **Tours des races (depuis la 2.40, direction « grimdark »)** : à la demande du concepteur (« plus Warhammer, moins Clash Royale »), les 50 tours sont refaites race par race, et **une tour n'est pas forcément une tour** : soldats, créatures, machines, totems, arbres. Proportions réalistes, pierre et fer ternis, palette désaturée, lueurs rares, neige sur les détails.
  - **Un module par race** dans `art/communs/` : `aubeval_hd.py` (calcaire, ardoise, bleu royal et or terni : arbalétriers, hallebardier, lance-filets, trébuchet, baliste, chapelle, comptoir, étendard, inquisiteur, Rayon de l'Aube), `orage_hd.py` (rondins, peaux, os, pierres levées, foudre bleu pâle : lanceur de haches orc, berserker, totems, catapulte, aigle-tempête, chaman, tambours, Cœur de l'Orage), `lunebois_hd.py` (écorce noire, mousse, pins, argent lunaire, venin : archers elfes, ronces, gardien sylvestre, fleur de venin, chouette des neiges, puits de lune, Arbre-Mère), `hautroc_hd.py` (granit, fer riveté, cuivre, runes de forge : arbalétrier nain, marteau-pilon, mortier, canon antiaérien, phare, gueule de forge, forgeron, mines, Grondeterre), `ossements_hd.py` (mausolée, os, fer rouillé : squelettes, chevalier mort, obélisque, encensoir de peste, gargouille, œil, nécromancien, puits des âmes, faucheuse, colosse). Chaque `art/tours/<faction>-<j>.py` appelle `tour(j)` de son module.
  - **Créatures au procédé des monstres organiques** (`communs/organique.py`, repris de la branche du bestiaire) adapté aux tours dans `communs/tours_hd.py` : union de volumes fondue d'un seul tenant (remaillage en voxels), **sculpture détaillée cuite en texture peinte et en carte de relief** (matériau « Peau », textures en WebP) sur un modèle léger, sans squelette d'animation (les tours ne s'animent que par pivots). Construction rapide en numpy (≈ 10 s par créature au lieu de plus de 15 min). Accessoires (armes, casques) et architecture gardent la peinture par sommets (« Peint ») avec l'**occlusion ambiante cuite dans les sommets** (`occlusion_sommets`, `peindre_architecture`).
  - `communs/peuples_hd.py` : corps humain paramétrable (gabarits **humain, orc, elfe, nain**), poses (arbalète, arme d'hast, bras levés, lancer, arc), rapaces (aigle, chouette).
  - Neige : un pivot `SansNeige` protège l'eau, les braises et les intérieurs (`neige.py`). `export_jeu.cuire` laisse intacts les matériaux « Peau » et « Peint ».
- **Ancien système de tours** (2.7 à 2.39, plus utilisé par le jeu) : `communs/tours_communes.py` déclinait les **6 archétypes** selon le `STYLE` de la faction.
- **Monstres** : `art/monstres/<g>.py` (17 scripts, un par clé `CR[…].g` ; le Petit limon utilise le modèle `slime`, réduit par le jeu). Tailles dans `communs/echelles.py` : `hauteur = 0,40 × z^1,8` (z de `CR`) : Sapeur gobelin 0,24 case, Brute orc 0,36, Troll 0,47, Golem 0,55, Cyclope 0,83 ; les tours font 1,1 à 1,4 case.
- **Monstres des paliers (préparés pour la PR B, pas encore dans `sim.js`)** : 3 paliers de **24 monstres** chacun (12 au sol, 3 volants, 8 magiques : aura de vitesse, invisible, se divise, accéléré, anti-magie, soin, armure, étourdissement ; 1 boss), soit 72 monstres. La liste, les clés `CR[…].g` proposées et les tailles `z` sont dans **`art/monstres/PALIERS.md`**. Les nouveaux modèles ne sont pas utilisés par le jeu tant que `CR` ne les déclare pas ; leur `z` est écrit dans leur script (à reporter dans `CR` et `echelles.py` avec la PR B). Noms, clés et tailles : **propositions à valider** par le concepteur.
- **Décor** : `art/decor/portail.py` et `art/decor/chateau.py` (drapeau recoloré par le jeu à la couleur du joueur).
- **Pièces communes** (`art/communs/`) : `outils.py` (formes, matériaux, peinture des sommets, budget de facettes), `factions.py` (palettes et socles des 5 factions), `personnages.py` (personnage caricatural paramétrable et armes), `betes.py` (quadrupèdes, volants, gelées), `animations.py` (animations par pièces, sans squelette : `marche`, `trot`, `saut`, `flotte`, `vol`), `echelles.py`, `neige.py` (neige sur les modèles, 2.9), `tours_communes.py`, `decor.py`, `export_jeu.py`, `rendu.py` (rendus de validation).
- **Export pour le jeu** (`communs/export_jeu.py`, appelé à la fin de chaque `construire`) : la couleur de chaque pièce est **cuite dans ses sommets** et un matériau unique `Peint` la lit (les pièces lumineuses gardent un matériau `Lueur_<couleur>`) ; les pièces qui bougent ensemble sont **fusionnées** (une dizaine de pièces par modèle au lieu d'une centaine, pour le téléphone). `generer.py` exporte aussi les **pivots** (objets vides) et les **animations** (pistes NLA), et compresse en **meshopt**. **Compression de secours** (depuis la 2.9) : le module `bpy` du cloud et de GitHub n'a pas la bibliothèque meshopt de Blender (export sans compression, sans message) ; `generer.py` compresse alors lui-même avec **gltf-transform** (`npx @gltf-transform/cli@4.2.1 meshopt`, licence MIT, demande Node.js), qui garde les pièces nommées et les animations et ajoute une quantification lue nativement par three.js. Sur le PC, Blender compresse lui-même et rien ne change.
- **Pièces nommées** utilisées par le jeu : `Tourelle` (pivote vers la cible), `Cristal`, `Eclats`, `Flamme`, `Anneaux`, `Orbe`, `AnneauFlottant`, portail `Anneau1..3` (animées en code), `Drapeau` (couleur du joueur) ; animations glTF `marche` (au sol) et `vol` (volants).
- **Concevoir dans Blender ouvert (MCP)** : `exec(open(r'<dépôt>\art\outils\atelier.py', encoding='utf-8').read())` recharge les pièces communes ; `atelier_asset('tours/alliance-0')` construit un asset dans la scène ; `art/outils/planches.py` fait les planches de validation (une par faction, trois pour les monstres).

- **Neige sur les modèles** (thème « Winter Realms », depuis la 2.9) : `communs/neige.py`, `enneiger(racine)`, appelé à la fin de chaque tour (`tour()`), du portail et du château. Une couche blanc bleuté (`#eef4fb`) recouvre les faces tournées vers le ciel : les surfaces planes (créneaux, socles, plates-formes, chapiteaux) presque entièrement, les **pentes** (toits, dômes) seulement sur leur partie haute (55 % depuis le sommet), pour que l'avant-toit garde la couleur de la faction. Pas de neige sur les personnages, les pièces animées ni les pièces lumineuses. Le nombre de triangles ajoutés est plafonné pour rester sous le budget (2 990 pour une tour) : les plus grandes faces passent en premier. Les monstres n'ont pas de neige.

### 15.2 Rendu 3D dans le jeu (`rendu3d.js`, depuis la 2.7)
- **Activation** : **par défaut depuis la 2.8** (adresse sans paramètre). `?rendu=2d` dans l'adresse garde la 2D (depuis la 2.22, l'accueil n'a plus de lien vers elle). Depuis la 2.29, les tests (parcours, captures, bilan visuel) se font en 3D, et un test vérifie le secours 2D. Si WebGL ou le module manquent, le jeu revient en 2D avec un message.
- **Chargement** : `index.html` déclare un *importmap* (`three` → `vendor/three/three.module.min.js`, `three/addons/` → `vendor/three/addons/`) et importe `rendu3d.js` à la demande (`charger3D`). Pas d'étape de build. Les modèles des factions en jeu et tous les monstres sont préchargés ; les autres au besoin.
- **Repli** : si un modèle manque (fichier absent ou illisible), le jeu affiche une forme simple à la couleur de la tour ou du monstre (règle de §15).
- **Caméra (2.7 à 2.14)** : orthographique, inclinée à **42°** par défaut ; depuis la 2.12, l'inclinaison s'adapte au format de la zone de jeu (`inclinerSelonFormat`, entre 34° et 66° ; la marge `TOPM` au-dessus du plateau suit, `1,6 × cos E`) pour que le plateau la remplisse : plus redressée en portrait, plus rasante en paysage (`incliner()` du module, `KY` relu à chaque `fit`). Une case (x, y) est en (x, 0, y) dans le monde ; à l'écran, `sx = ox + x·s` et `sy = oy + (y·KY − h·KH)·s`, avec `KY = sin 42°`, `KH = cos 42°`. C'est la formule de la 2D avec un tassement vertical `R3D.KY` : `fit`, `borner`, `zoomer`, `caseVersEcran`, `caseSous` (case sous le doigt), le pincement et le cadre de la vignette l'utilisent. En 2D, `KY = 1` et `TOPM = 0`, donc rien ne change. `TOPM` = 1,2 case libre au-dessus du plateau pour les tours hautes.
- **Caméra « vue tactique » (depuis la 2.15)** : **perspective** (champ vertical `FOV` 34°, 48° avant la 2.26), à hauteur fixe, inclinée à **44°** (`ELEV`, 40° avant la 2.26), qui regarde un point du sol (`V.fx`, `V.fz`) ; à la largeur de ce point, on voit **8,4 cases** (`COLONNES`, 10,5 avant la 2.26 : 20 % plus près depuis), et ce point est au centre de la zone libre entre le bandeau et le dock (`cadre({w, h, haut, bas})`, décalage de la vue par `setViewOffset`). Elle remplace la caméra orthographique : plus de pincement, de molette, de zoom ni d'inclinaison selon le format. Fonctions du module : `projeter(x, y, z)` (monde → pixels), `echelle(x, z)` (pixels par case à cet endroit), `sol(px, py)` (pixels → point du sol, par un rayon), `glisser` (le point du sol sous le doigt reste sous le doigt), `lancer` (élan au lâcher, amorti), `pivoter(±1)` (un huitième de tour, animé), `viser`, `amener(x, z, px, py)` (2.35 : la vue glisse en douceur pour que le point du sol arrive au pixel donné ; annulé par `glisser`, `lancer` ou `viser`), `empreinte` (partie visible, pour la vignette). Le point regardé reste à au moins `MARGE` cases (environ 3) des bords du terrain (2.26) : on ne voit jamais plus d'une case et demie de paysage sur le côté. La brume suit la distance de la caméra. Autour du plateau, un champ de neige se fond dans la brume bleu nuit (`scene.fog`).
- **Commandes** : identiques à la 2D pour construire (choix de la carte, puis deux touchers), car le canevas 2D `#main` reste par-dessus le canevas WebGL `#main3d` et reçoit les gestes ; en plus, glisser le doigt déplace la carte et les flèches la font pivoter (§9). Il faut toucher le **pied** d'une tour (sa case au sol) pour l'ouvrir.
- **Ce qui est dessiné en 3D** : paysage d'hiver continu avec la grille du terrain de jeu (depuis la 2.26, voir « Paysage »), petit décor déterministe sur le terrain, portail (anneaux qui tournent), château (drapeau à la couleur du joueur), chemin en pointillés animés, tours (la `Tourelle` vise la cible, le garde frappe, cristaux, flammes, anneaux et orbes animés, taille et points d'or selon le niveau, étoiles quand elle est étourdie, **échafaudage** et tour qui monte pendant le chantier), monstres (animation de marche ou de vol, vitesse selon le monstre et le ralentissement, orientation selon le déplacement, halo au sol ralenti/hâté/soigné, cercles d'aura du Chaman et de la Prêtresse, Spectre translucide quand il est caché), projectiles (flèche, boulet en cloche, éclat de givre, orbe arcanique), effets (explosion, impact, portée, fumée, flammes, coup d'épée, éclair, case refusée), tour fantôme et cercle de portée de l'aperçu.
- **Surcouche 2D** (sur `#main`) : barres de vie, barre de progression des chantiers, textes flottants (or, « −1 vie », niveau), terrain éliminé ; en perspective, leur taille suit `echelle`.
- **Volants plus compacts** (depuis la 2.32) : les volants sont dessinés à **×0,5** de cette taille (`ECH_VOLANTS`, fonction `echMonstre` ; ×0,65 en 2.32 et 2.33, deux fois moins grands depuis la 2.35), leurs ailes déployées cachaient le terrain ; leur barre de vie suit. Le rendu 2D de secours et les vignettes ne changent pas.
- **Monstres agrandis ×1,4 en jeu** (`ECH_MONSTRES`) pour rester lisibles sur téléphone ; les rapports de taille de `echelles.py` sont gardés.
- **Paysage** (depuis la 2.26, `construirePaysage`, construit une seule fois) : plus de plateau-diorama posé dans le vide ; le terrain de jeu fait partie d'un grand **paysage d'hiver continu** (100 × 100 cases), et **seule sa grille** (lignes bleu nuit, bord un peu plus marqué) montre où l'on joue. Le sol est **plat sur le terrain de jeu** (aucun effet sur le jeu) et prend **du relief tout autour** (collines de plus en plus hautes en s'éloignant, `hauteur`). Ses couleurs sont peintes dans une image de 1024 × 1024 (`texturePaysage`, environ 11 pixels par case) : neige, neige grise, **plaques d'herbe** aux bords déchirés (avec des touffes d'herbe sèche), terre, **flaques de neige fondue** gris bleu (plus petites et plus pâles sur le terrain de jeu) ; un **grain de neige en relief** (`bumpMap`) couvre tout. Autour : **forêt de grands sapins enneigés** par bosquets (petits près du bord pour ne jamais cacher le jeu, jusqu'à environ 3 cases de haut au loin), rochers enneigés, **ciel en dégradé** (nuit en haut, bleu gris à l'horizon), **chaîne de montagnes** lointaine et brume. Tout est calculé à partir des coordonnées (bruit déterministe) : même paysage à chaque partie. Le soleil est plus haut, pour que l'ombre des sapins ne couvre pas le terrain. Les petits sapins posés sur le terrain sont 1,6 fois plus grands.
- **Thème hiver** (depuis la 2.9) : le plateau est **enneigé** (damier blanc bleuté `NEIGE`, à peine teinté par la couleur de la faction `TEINTE`, bord en roche givrée `BIOME`), avec un décor d'hiver toujours placé au même endroit (rochers coiffés de neige, petits sapins enneigés, congères, cristaux de glace aux couleurs de la faction) et **des flocons qui tombent** (260 points, un seul dessin ; depuis la 2.30, la position de chaque flocon ne dépend que du temps, `fairePleuvoir(temps)`, et plus de l'enchaînement des images). Le chemin, le cercle de portée et l'anneau de construction passent en bleu nuit pour rester lisibles sur la neige. Fond bleu nuit.
- **Lumières** : ciel froid et sol bleuté, soleil pâle avec ombres douces (carte 2048), contre-jour bleuté (depuis la 2.9 ; avant : lumière chaude). Netteté plafonnée à ×2.
- **Style peint commun** (depuis la 2.39, `styliser()` de `rendu3d.js`) : au chargement, chaque modèle (tours, monstres, portail, château) passe en **ombres en paliers** (matériau « toon », 4 paliers `PALIERS`), reçoit un **liseré de lumière froide** sur les bords (rim light, `RIM`) et un **contour sombre** d'épaisseur constante à l'écran (coque inversée, 1,15 pixel CSS, `LARGEUR`), pour que la silhouette se détache de la neige sur téléphone. Les pièces lumineuses (« Lueur… ») gardent leur matériau ; les contours sont masqués sur la tour fantôme et les monstres invisibles ; les icônes des boutons (`vignette`) ont aussi le style. Coût : environ 1,7 fois plus d'appels de dessin (455 au lieu de 264 dans la scène de test). `?style=0` dans l'adresse revient au rendu d'avant (comparaison, téléphone trop lent).
- Le multijoueur fonctionne aussi en 3D : le module lit les terrains reconstruits à partir des instantanés, comme `draw()`.
- **Page d'aperçu** : `apercu-3d.html` montre chaque modèle du manifeste (tours, monstres, décor) en rotation avec son animation, son nombre de triangles et sa taille ; `?modele=nains-9` ouvre directement un modèle.

---

## 16. Bibliothèque sonore (depuis la 2.17, ElevenLabs depuis la 2.29)

- **Fichiers** : `assets/audio/<dossier>/<id>-<n>.mp3` (44,1 kHz, 128 kbit/s) : `tours/` (tirs `tir-<archétype>-<faction>`), `construction/` (`chantier-`, `fini-`, `up-` par faction), `monstres/` (`mort-<famille>`, `cri-<famille>`, `arrivee-<boss>`), `interface/` (dont les cors d'envoi `send-sol`, `send-volant`, `send-special`, `send-boss`), `ambiances/` (boucles `amb-hiver`, `amb-bataille`), `voix/<faction>/` (`voix-<faction>-<contexte>`). `assets/audio/manifeste.json` liste les variantes (`node art/outils/manifeste-audio.js`). 2.29 : 371 fichiers, 122 sons, 9,9 Mo.
- **Consignes** (`assets/audio/catalogue.json`) : pour chaque bruitage la description en anglais (`p`, courte et concrète, sans mots « cinématiques », comme le demande le guide d'ElevenLabs), la durée, le nombre de variantes et la boucle ; pour chaque faction sa voix ElevenLabs (`voix` : identifiant et ton entre crochets) et ses répliques par contexte (`repliques`).
- **Direction validée par le concepteur (2.29)** :
  - **tours** : réalistes et médiévales, en fond sonore, graves ou médiums, jamais stridentes ; 3 à 4 variantes par tir, dans l'univers de chaque faction (brief de départ : Alliance métal et arbalètes, Horde bois, os et armes lourdes, Sylvestres arcs légers et nature, Nains forge et mécanismes, Légion magie noire et murmures) ;
  - **monstres** : morts et **cris pendant la marche** (grognements courts pour les humanoïdes, bruits d'animaux réalistes sinon), 10 familles ;
  - **envoi d'une vague** : **cor de guerre** (appel au combat, deux longs appels), différent selon la catégorie envoyée (sol, volants, spéciaux, boss) ; jamais un klaxon ;
  - **répliques** : **dark fantasy mais sarcastiques**, courtes, accrocheuses et mémorables, avec 2 ou 3 variantes par contexte ; 7 contextes : `sel` (toucher une tour), `agace` (4ᵉ toucher rapproché), `construit` (pose d'une tour : toujours le thème « du travail, encore du travail », mais jamais cette phrase mot pour mot), `ameliore` (niveaux 2 à 4), `max` (niveau 5), `vague` (vague éliminée), `impossible` ;
  - **voix** (modèle `eleven_v3`) : Alliance, Sylvestres et Légion gardent les voix de la bibliothèque ElevenLabs de la première production ; **Horde** et **Nains** ont des **voix créées pour le compte** (outil de création de voix, choisies à l'écoute par le concepteur), car une voix de la bibliothèque partagée peut être retirée par son auteur (c'est arrivé à la voix de nain en 2.29). Horde : très grave, gutturale, bestiale.
- **Génération** : `node art/outils/generer-sons.js [--motif X] [--max N] [--reserve R] [--sans-voix]`, avec la clé API du concepteur dans `ELEVENLABS_API_KEY` (accès Text to Speech, Sound Effects, Voices et User en lecture). Seuls les fichiers manquants sont produits, un à la fois (la réplique n° i d'un contexte va toujours dans le fichier `-i`) ; chaque fichier passe le contrôle qualité, un fichier refusé (presque muet, saturé…) est refait 2 fois au plus puis le son est sauté. En cas d'erreur de l'API : 3 essais au plus, et 3 sons de suite en échec arrêtent tout. `--reserve` arrête la génération sous un nombre de crédits restants (2.29 : plafond de 70 000 crédits voulu par le concepteur ; la bibliothèque complète en a coûté environ 14 000). Pour refaire un son ou une réplique : supprimer son fichier, puis relancer.
- **Droits** : offre payante ElevenLabs (Creator en 2.29) : usage commercial autorisé ; ce qui est généré pendant l'abonnement reste utilisable commercialement après sa fin, sans mention obligatoire. Les modèles en « bêta » ne sont pas couverts : `eleven_text_to_sound_v2` et `eleven_v3` ne le sont pas.
- **Contrôle qualité** : `node art/outils/controle-sons.js [motif]` (Playwright) mesure durée, crête, niveau moyen, silences et saturation ; `ecoute-sons.html` permet d'écouter chaque variante. **La validation se fait à l'oreille par le concepteur**, par petits lots : les mesures ne jugent pas le timbre.
- **Moteur** (`audio.js`, objet `SON`) : indépendant de `sim.js`. Préchargement de la faction du joueur et des sons communs, variantes tirées sans répéter la précédente, légère variation de hauteur, 10 sons au plus en même temps avec priorités, une seule voix à la fois, ambiances en fondu, silences du début et de la fin coupés au chargement, crête ramenée à -3 dB avec un gain plafonné à **×2** (2.29 ; ×8 avant, ce qui faisait remonter le souffle). Si un fichier manque, `sfx()` joue le son synthétisé d'origine. `?son=synth` revient aux seuls sons synthétisés.
- **Raccordement** (`index.html`, sans changer `sim.js`) : les événements `board.ev` donnent les tirs, constructions, améliorations, ventes, explosions, étourdissements, vies perdues et vagues ; la faction du terrain choisit la variante. L'envoi joue le cor de la catégorie du monstre (`CAT_SON`, `sonEnvoi`). Une **couche d'observation** (`ecouterSons`) donne ce que `sim.js` ne note pas : cri de mort selon la famille (couleur du nuage `puff`, table `FAM_SON` des 72 clés de monstres), **cri d'un monstre visible du terrain regardé toutes les 3,5 à 8 s**, arrivée d'un boss (`BOSS_SON`), fin d'un chantier du joueur (`t.b` qui passe à 0), **nouvelle tour** (réplique `construit`), **niveau qui monte** (`ameliore` ou `max`), **vague éliminée** (le terrain du joueur a reçu au moins 4 monstres et n'en a plus : réplique `vague`).
- **Historique** : 2.17 à 2.27, bibliothèque générée en local (Stable Audio Open et Chatterbox, scripts `art/sons/`, gardés pour mémoire) ; le concepteur l'a jugée trop pauvre (tirs « pistolet de 1993 », fanfares de vieille console, voix trop proches de la sienne) et l'a remplacée en 2.29.

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
| 2026-11-14 | 2.5 | Outillage : **tests plus courts**. Par défaut, une seule partie entre IA par difficulté au lieu de 15, et la vérification de reproductibilité ne rejoue que 2 minutes. Les 15 parties restent disponibles avec `--complet` (tests et bilan). La vérification GitHub passe de 9 min à environ 1 min 30 (délai maximal ramené à 10 min). **Aucun changement de jeu.** |
| 2026-11-14 | 2.5.1 | **Correctif multijoueur** : après 2 ou 3 minutes, dès qu'un monstre au sol arrivait sur le terrain du joueur, `peutConstruire` lisait la case visée `tx`/`ty`, absente des instantanés du serveur. L'erreur arrêtait la boucle de dessin : terrain figé et grisé, plus aucune tour posable. La page donne maintenant à chaque monstre reçu la case la plus proche de sa position. `index.html` seul (pas de redéploiement du serveur). |
| 2026-11-14 | 2.6 | **IA : labyrinthes efficaces dès le milieu de partie**. Les candidats sont notés sur la longueur du chemin après 15, 25, 40 et 60 tours (et une fois complets), plus seulement à la fin. Les murs qui ne touchent pas le chemin et ne l'allongent pas sont retirés du plan. Avec 40 tours, le chemin passe d'une médiane de 57 à 66 cases (minimum 40 → 56) ; plans de 57 à 74 tours au lieu de 66 à 89. Génération ≈ 25 à 40 ms (≤ 3 ms par pas). `sim.js` modifié (redéploiement du serveur). Deux tests ajoutés à `labyrinthe`. |
| 2026-11-14 | 2.7 | **Rendu 3D jouable (prototype)** avec `?rendu=3d` ou le lien de l'accueil (§15.2) : `rendu3d.js` et three.js r170 copié dans `vendor/three/` (importmap, sans build), caméra orthographique inclinée à 42°, plateau-diorama, tours et monstres animés, chantiers, projectiles et effets, chemin, construction en deux touchers avec tour fantôme, zoom et déplacement à deux doigts, panneau de tour. **Modèles 3D de tout le jeu** (§15.1) : 50 tours (5 factions × 10, style heroic fantasy cartoon validé par le concepteur), 17 monstres animés et le portail et le château, un script par asset dans `art/` selon `art/LISEZMOI.md` ; pièces communes dans `art/communs/` ; `generer.py` exporte maintenant aussi les pivots et les animations, et compresse en meshopt. Page `apercu-3d.html`. La 2D reste le rendu par défaut et est inchangée. Tests : `modeles-3d`, parcours mobile en 3D (WebGL logiciel), captures `--3d`, `WR_CANAL`. **Règles du jeu inchangées** (`sim.js` non modifié, pas de redéploiement du serveur). |
| 2026-11-14 | 2.8 | **La 3D devient le rendu par défaut** : l'adresse normale du jeu ouvre la vue 3D ; `?rendu=2d` (ou le lien « Jouer en vue 2D (classique) » de l'accueil) garde la 2D, qui reste inchangée. Tests 2D et captures ouverts avec `?rendu=2d` ; nouveau test de l'adresse par défaut. **Règles du jeu inchangées** (`sim.js` non modifié). |
| 2026-11-14 | 2.9 | **Thème hiver plus présent** (§15.1, §15.2), en 3D : plateau enneigé (damier de neige teinté par la faction, roche givrée), décor d'hiver (sapins enneigés, rochers coiffés de neige, congères, cristaux de glace), flocons qui tombent, lumière d'hiver froide ; chemin et portée en bleu nuit. **Neige sur les tours**, le portail et le château (`art/communs/neige.py`) : calottes de neige sur les créneaux, socles et plates-formes, haut des toits et des dômes enneigé, couleurs de faction gardées. Les 70 assets ont été régénérés. La 2D est inchangée. **Règles du jeu inchangées** (`sim.js` non modifié). |
| 2026-11-14 | 2.9 | Correctif outillage : **compression des modèles dans le cloud**. Le Blender du cloud et de GitHub (`bpy`) exportait sans compression meshopt, sans le signaler : l'action « Assets 3D » mesurait des fichiers 2 à 3 fois trop lourds et refusait à tort trois tours du thème hiver, et une régénération en ligne aurait produit des fichiers refusés par `modeles-3d`. `generer.py` compresse désormais avec gltf-transform quand Blender ne l'a pas fait. Rendu identique vérifié en 3D. **Aucun changement de jeu.** |
| 2026-11-14 | 2.9 | **Retour à la version 2.9** à la demande du concepteur : la 2.10 (cinq nouvelles identités de factions, PR 22, reprise de la PR 19) est annulée et **mise en pause**. Les factions redeviennent Alliance, Horde, Sylvestres, Nains et Légion des ombres. Le travail de la 2.10 reste dans l'historique (commit `ef01c65`, étiquette `v2.10`) et pourra être repris après décision du concepteur. `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-14 | 2.11 | **Nouvelle direction artistique de l'interface, façon jeu vidéo** (heroic fantasy hivernale) : écran d'accueil refait (nuit d'hiver, montagnes, neige qui tombe, emblème, titre doré, description et règles illustrées, factions à blason, boutons de difficulté en relief avec leur effet) ; en jeu, panneaux bleu nuit à liseré d'or, boutons en relief, cartes serties, cadre doré du terrain. **Gain de place** : le bouton des terrains des autres joueurs revient dans le bandeau du haut (le coin du terrain est libéré), bandeau, onglets et fiche plus compacts, mêmes informations. Interface uniquement : `sim.js` non modifié (pas de redéploiement du serveur). |
| 2026-11-14 | 2.11 | Outillage : le test « génération découpée » de l'IA (`labyrinthe`) échouait souvent sur GitHub (tranche de 7 ms pour une limite de 6 ms) selon la charge des machines. Il vérifie désormais avec certitude que la génération se fait en au moins 3 tranches, et ne garde la durée que comme garde-fou : meilleure de 3 mesures, moins de 10 ms par tranche et 100 ms au total (avant : 6 et 60 ms). **Aucun changement de jeu.** |
| 2026-11-15 | 2.12 | **Interface : terrain plus grand et habillage « givre elfique »**. Le terrain occupe toute la place : en 3D, l'inclinaison de la caméra s'adapte au format de l'écran (34° à 66°) ; en paysage, trois colonnes (bandeau et fiche à gauche, terrain au centre, onglets et boutons à droite). Bouton « Vue d'ensemble » posé sur le plateau. Habillage inspiré des barres de commande des jeux de stratégie : cadre d'écran à volutes elfiques et voile de givre, panneaux en verre de nuit à texture de givre et cadres argentés, cartes serties avec prix en médaillon (tout en SVG et CSS). En 3D, les icônes des tours et des monstres sont des rendus des modèles 3D. Interface uniquement : `sim.js` non modifié (pas de redéploiement du serveur). Test de mise en page paysage adapté. |
| 2026-11-15 | 2.12 | Assets 3D : **modèles des monstres des paliers** (PR B : 3 paliers × 24 monstres, liste dans `art/monstres/PALIERS.md`), un script par modèle dans `art/monstres/` (§15.1). Ils ne sont pas encore utilisés par le jeu. **Aucun changement de jeu** (`sim.js` et `index.html` inchangés). |
| 2026-11-15 | 2.13 | **Paliers de monstres** (§6) : 3 paliers de 24 monstres (12 au sol, 3 volants, 8 magiques : hâte, invisible, se divise, accéléré, anti-magie, soin, armure, étourdissement ; 1 boss), soit 72 monstres au lieu de 17, avec les modèles 3D de la PR 26. Palier 1 ouvert dès le début, palier 2 à 300 or, palier 3 à 1 500 or (`PAL_C`, action `tier`) ; les déblocages par le temps disparaissent. Nouvelle capacité **accéléré** ; trois monstres qui se divisent (Petit limon, Petite boue, Tête d'hydre) ; un boss par palier (Roi gobelin, Cyclope, Azh'Khar). L'IA ouvre les paliers (2:30 et 7:00 au plus tôt) et envoie le plus fort monstre de chaque famille parmi ses paliers ouverts. Interface : écussons de palier dans l'onglet Envoyer, silhouette 2D de secours. **`sim.js` et `server/` modifiés** (redéploiement automatique du serveur ; l'instantané transmet le palier). Tests : `vagues` (paliers, accéléré), `combats` et `economie` adaptés, parcours mobile (palier 2). Chiffres d'équilibrage proposés, **à valider par le concepteur**. |
| 2026-11-15 | 2.14 | **Coûts en dizaines et revenus sur la courbe** (§2, §6) : le Rat des neiges coûtait 15 or pour +2 de revenu (13 %, mieux que tous les autres monstres) ; il coûte maintenant 20 or pour +2. Les monstres au sol du palier 1 passent sur une échelle de 10 en 10 (10 à 120 or), PV ajustés au même rapport. Le revenu des monstres au sol est arrondi à l'inférieur sur la courbe 10 → 1, 100 → 11, 1000 → 120 : aucun monstre ne la dépasse. Volants et spéciaux : coûts déjà en dizaines, revenu inchangé (6,5 % du coût). `sim.js` modifié (redéploiement automatique du serveur). Test `tables` : coûts en dizaines et revenus sous la courbe. Chiffres **à valider par le concepteur**. |
| 2026-11-17 | 2.15 | **Interface « vue tactique »** (§9, §15.2), d'après la maquette validée par le concepteur : le terrain occupe tout l'écran, le bandeau et le dock flottent par-dessus. En 3D, **caméra en perspective à hauteur fixe** (40°, 10,5 cases de large) : **glisser le doigt déplace la carte** comme une appli de cartes (avec élan), **deux flèches la font pivoter d'un huitième de tour** ; plus de pincement, de molette ni de « Vue d'ensemble » ; champ de neige et brume autour du plateau. **Portrait seulement** (« Tourne ton téléphone » en paysage). Bandeau : **menu** (son, vibrations, rappel des gestes, quitter), or, revenu avec anneau des 10 s, vies, horloge, **plein écran** (verrouillé en portrait si possible). Bouton **Adversaires** (vignettes ; on peut envoyer depuis le terrain d'un adversaire). **Une seule fiche, seulement quand on choisit** (tour, tour posée avec Améliorer et Vendre, monstre). **Cartes réduites à l'icône et au prix** ; paliers sur une ligne. Construire : choisir une carte, puis deux touchers. Envoyer : 1er toucher = choix, chaque toucher suivant = un groupe (**pas d'envoi en rafale, voulu**), avec rebond, vibration et compteur ×2, ×3. En 2D, plateau entier sans zoom. Retrait de l'aperçu par appui long et des ornements « givre elfique ». Interface uniquement : `sim.js` non modifié (pas de redéploiement du serveur). Tests navigateur refaits (portrait seulement, 2D et 3D), captures adaptées. |
| 2026-11-17 | 2.16 | **Musique de fond** (§9) : trois thèmes composés par le concepteur avec Suno (`assets/musique/`, MP3). Le premier est tiré au hasard au lancement, puis ils s'enchaînent en boucle, en arrière-plan, pendant toute la partie. Bouton « Musique » dans le menu (indépendant du son des bruitages). Règle de conception n°2 adaptée : les bruitages restent synthétisés, la musique est la seule exception. `.gitattributes` : fichiers audio en binaire. Interface uniquement : `sim.js` non modifié. Test du parcours mobile complété (musique). |
| 2026-11-18 | 2.17 | **Bibliothèque sonore** (§16) : environ 230 fichiers MP3 générés en local et gratuitement (Stable Audio Open pour les bruitages, Chatterbox pour les voix, licences compatibles avec un usage commercial) : tirs des 6 archétypes pour chaque faction, construction, fin de chantier et amélioration par faction, cris de mort des 72 monstres (10 familles), arrivées de boss, interface, ambiances d'hiver et de bataille, et **55 répliques vocales** caricaturales (11 par faction) dites avec les voix enregistrées par le concepteur. Moteur `audio.js` (préchargement, variantes, priorités, une voix à la fois, sons synthétisés en secours, `?son=synth`). Scripts de génération `art/sons/`, contrôle qualité `art/outils/controle-sons.js` et page `ecoute-sons.html`. Règle de conception n°2 adaptée. `sim.js` non modifié (pas de redéploiement du serveur). |
| 2026-11-18 | 2.18 | **Habillage « givre » sur l'interface vue tactique** (§9) : retour des textures gelées et des cadres à volutes de la 2.12, disposés comme la console d'un jeu de stratégie (style propre au jeu) : barre de ressources givrée sur toute la largeur et console du bas givrée, bordées d'une frise d'argent à gemmes de glace ; cartes carrées serties (argent, or si choisie, rouge pour les monstres) avec prix en médaillon ; onglets, fiche, bouton Adversaires, vignettes et menu dans des cadres d'argent ; boutons ronds en métal cerclés d'or ; voile de froid sur les bords du terrain. Onglets, paliers et cartes regroupés dans `#console`. Interface uniquement : `sim.js` non modifié. |
| 2026-11-18 | 2.19 | **Icônes plus lisibles** (§9) : pastilles de rôle et de cibles des tours rondes et cerclées de la couleur du rôle (le carré doré, qui diluait la couleur, est retiré) ; aile redessinée en vraie aile à plumes. Onglets d'envoi en icônes : patte (sol), aile (volants), étoile (spéciaux). Le **gain de revenu** revient sur les cartes de monstres (pastille verte « +N »). Interface uniquement : `sim.js` non modifié. |
| 2026-11-18 | 2.20 | **Givre et racines selon le niveau** (§4.1, §5) : le Givre ralentit de −20 % (niveau 1) à −50 % (niveau 5) au lieu de −50 % à −70 %, pendant 1,5 s à 2,7 s, avec une explosion de rayon 1,2 à 2 cases ; les racines sylvestres de −10 % pendant 0,72 s à −30 % pendant 1,3 s (avant : −18 % à tous les niveaux). **Le froid et les racines s'additionnent** (jusqu'à −80 %) ; deux effets de la même famille ne se cumulent pas. Tables `GIVRE_LV` et `RACINES_LV`. Fiche : ralentissement, durée et zone au niveau actuel et au suivant. `sim.js` modifié (redéploiement automatique du serveur). Tests `deplacements` et `combats` adaptés. Valeurs demandées par le concepteur ; durées et rayons **à valider**. |
| 2026-11-18 | 2.21 | **Paliers au-dessus des onglets** (§9) : la ligne des paliers passe au-dessus des onglets ; les onglets et les cartes ne bougent plus quand on passe des tours aux monstres. Interface uniquement : `sim.js` non modifié. |
| 2026-11-18 | 2.22 | **La 3D devient la seule vue proposée** (§1, §9, §15.2) : le lien « Jouer en vue 2D (classique) » de l'accueil est retiré. Le rendu 2D reste dans le code comme **secours** quand WebGL manque et pour les **tests** (`?rendu=2d` fonctionne toujours). Test `parcours-3d` adapté (plus de lien sur l'accueil). Interface uniquement : `sim.js` non modifié. |
| 2026-11-18 | 2.23 | **Fin de partie : statistiques et exploration des labyrinthes** (§9) : en solo, une fenêtre donne Victoire ou Défaite, un tableau des 4 joueurs (classement, tours, longueur du chemin, vagues envoyées, monstres tués, revenu), la courbe du revenu et un résumé du joueur ; « Regarder la carte » fige la partie et permet de se balader sur les 4 labyrinthes (toucher une tour ouvre sa fiche), « Quitter » ramène à l'écran de fin. Compteurs `Board.st` dans `sim.js`, sans effet sur le jeu (redéploiement automatique du serveur). Test `fin-de-partie` complété. |
| 2026-11-18 | 2.24 | **Maj + clic pour construire en un clic** (§9), sur ordinateur : la tour choisie est posée directement, sans l'aperçu du 1er toucher ; elle reste choisie pour enchaîner. Le toucher en deux temps reste la règle sur écran tactile. Interface uniquement : `sim.js` non modifié. |
| 2026-11-18 | 2.25 | **Monstres au sol en diagonale** (§3) : distances sur 8 directions (diagonale √2, sans couper le coin d'une tour), puis déplacement en ligne droite vers la case la plus lointaine visible du chemin, à 0,3 case des tours, cible revue toutes les 0,25 s : les monstres prennent le chemin le plus court à n'importe quel angle (du coin haut gauche au coin bas droit, la diagonale). Chemin en pointillés (2D et 3D) tracé avec les mêmes règles (`chemin`). Pose refusée à moins de 0,9 case d'un monstre au sol (plus de case « visée » protégée) ; une pose devant un monstre lui fait changer de cible. L'IA garde ses labyrinthes calculés en 4 directions. **`sim.js` modifié** (redéploiement automatique du serveur). Tests `construction` et `deplacements` adaptés, deux tests de diagonale ajoutés. La colonne « Chemin » des statistiques de fin de partie (2.23) donne la longueur réelle de ce chemin, arrondie à la case. |
| 2026-11-18 | 2.25 | **Monstres espacés** (§3, `Board.ecarter`) : les monstres proches (moins de 0,75 case) se poussent sur le côté seulement, au plus 1,5 case/s, sans jamais être freinés : ils ne se superposent plus (chevauchements de 3 % à 0 % des paires dans un essai à 40 monstres) et le temps de trajet est inchangé, donc pas de bouchon. Les volants s'écartent aussi entre eux. `sim.js` modifié (redéploiement automatique du serveur). Deux tests ajoutés à `deplacements`. |
| 2026-11-18 | 2.25 | **IA adaptée aux déplacements en diagonale** (§8) : la longueur du chemin de ses plans (`plen`, `mzPath`) suit les règles des monstres (8 directions sans couper les coins, coûts 5 et 7, algorithme de Dial) et la recherche locale peut ajouter des segments en diagonale. Mesuré sur 30 graines avec le vrai chemin : à 40 tours, 56,1 → 57,0 cases en Normal et 59,0 → 61,1 en Brutal ; plan complet 89 → 95 cases en Brutal. Génération ≈ 60 à 75 ms (au lieu de 30 à 40), par tranches de 5 ms au plus ; garde-fou du test `labyrinthe` porté de 100 à 150 ms au total (10 ms par tranche inchangé). `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-18 | 2.25 | Organisation : **titre court pour chaque version** (règle de maintenance n°6) : 2 à 4 mots qui résument la version (par exemple « exploration fin de partie » pour la 2.23), repris dans le commit, la PR, le journal et le `README.md`. **Aucun changement de jeu.** |
| 2026-11-18 | 2.25 | **feuille de route** : tableau des idées d'améliorations en tête du `README.md` (IA, difficulté, tours, factions, quêtes bonus, pouvoirs du palier 3, correctif du défilement sur PC, accélération des tests), avec un statut par idée, et formulaire GitHub « Idée d'amélioration » (`.github/ISSUE_TEMPLATE/idee.yml`) pour en proposer. Règle de maintenance n°7. Pas de simulation à lancer quand le gameplay ne peut pas changer (règle n°5, §12.4). **Aucun changement de jeu.** |
| 2026-11-18 | 2.26 | **Terrain immersif** (§15.2) : caméra moins déformée (champ de 34° au lieu de 48°, inclinée à 44°) et **20 % plus près** (8,4 cases de large au lieu de 10,5) ; on ne peut plus s'éloigner du terrain (point regardé à au moins environ 3 cases des bords). Plus de plateau-diorama : le terrain fait partie d'un **paysage d'hiver continu** que seule sa grille distingue, avec du **relief autour** (le terrain de jeu reste plat), des **plaques d'herbe** et des **flaques de neige fondue**, un **grain de neige en relief**, une **forêt de grands sapins**, des rochers, un **ciel en dégradé**, des **montagnes** au loin et de la brume ; petits sapins du terrain plus grands ; soleil plus haut. Le paysage est construit une seule fois (plus rapide quand on regarde un adversaire). `rendu3d.js` seulement : `sim.js` non modifié. |
| 2026-11-18 | 2.27 | **sons dark fantasy** : bruitages plus sombres et plus guerriers (§16), à la demande du concepteur : les sons des monstres (cris de mort des 10 familles, arrivées de boss) passent du cartoon à la **dark fantasy** (râles, rugissements, chutes lourdes), et les tirs des tours (flèches, lames, givre, canons, magie, flammes), l'explosion et le sabotage deviennent plus **percutants**. 45 consignes réécrites dans `catalogue.json` et 124 fichiers régénérés en local ; nouveau champ `neg` (mots à éviter par son). Voix, musique, interface et construction inchangées. `sim.js` non modifié. |
| 2026-11-19 | 2.28 | **mini-cartes d'hiver** (§9) : les vignettes du panneau Adversaires reprennent la direction artistique d'hiver (neige, grille, chemin en pointillés bleu nuit, portail, petit château au drapeau du joueur) ; tours en petites pièces à la couleur de leur rôle (on voit d'un coup d'œil la défense d'un adversaire : anti-aérien, Givre, Mages…), monstres cerclés (rouges au sol, blancs en vol) ; vignettes un peu plus grandes (6 px par case au lieu de 4), serties d'argent ; vies avec un cœur, revenu avec la pièce d'or ; cadre de la partie visible en or. Interface uniquement : `sim.js` non modifié. |
| 2026-11-19 | 2.29 | **bibliothèque elevenlabs** : toute la bibliothèque sonore (§16) refaite avec ElevenLabs (offre Creator, usage commercial) à la place des modèles locaux, jugés trop pauvres : 371 fichiers, environ 14 000 crédits. Tirs des tours réalistes et médiévaux, jamais stridents (3 à 4 variantes) ; morts et **cris des monstres pendant la marche** ; **cor de guerre** à l'envoi, différent pour le sol, les volants, les spéciaux et les boss ; interface et ambiances refaites. **100 répliques** dark fantasy sarcastiques, avec 3 nouveaux contextes : pose d'une tour (« du travail… »), **niveau maximum** et **vague éliminée** ; nouvelles voix créées pour la Horde (plus grave et bestiale) et les Nains. Moteur : gain au chargement plafonné à ×2. Script `generer-sons.js` : 3 essais au plus, arrêt après 3 échecs de suite. `sim.js` non modifié. |
| 2026-11-19 | 2.29 | Outillage : **tests 3D allégés** (§12.2) : en 3D, l'avance rapide des tests (`avancer`) ne redessine plus la vue que 4 fois par seconde de jeu (la partie, elle, avance toujours image par image). Le navigateur de test plantait vers 30 s de jeu depuis le paysage de la 2.26, alors que le jeu tourne normalement sur téléphone. Parcours 3D en 1 min au lieu de 5, captures 3D en 1 min 30 au lieu de 10 ; nouvelle variable `WR_GPU=1` pour tester la 3D avec la vraie carte graphique (environ 20 s). **Aucun changement de jeu.** |
| 2026-11-19 | 2.29 | Outillage : **tests en 3D** (§12) : le parcours automatisé se fait dans le vrai jeu, en 3D. Il réunit l'ancien parcours 2D (interface : menu, paliers, revenu, vente, adversaires…) et l'ancien `parcours-3d.test.js` (supprimé) : 26 vérifications. Un test vérifie le **secours 2D** (3D introuvable : message, passage en 2D, construction possible). Captures et bilan visuel en 3D (`captures.js --2d` pour la 2D). Corrigés en chemin : la version d'avant était extraite sans three.js, modèles ni sons ; three.js puisait dans le même hasard à graine que la simulation (partie différente d'un lancement à l'autre) ; l'alignement de l'horloge était parfois sauté en 3D. Limite : les flocons qui tombent laissent environ 0,1 % de différence entre deux captures identiques (seuil du témoin : 0,05 %). **Aucun changement de jeu.** |
| 2026-11-19 | 2.30 | **départ façon course** (§2, §8, §9) : l'**or de départ est doublé** (200 au lieu de 100 pour chaque terrain ; réserves internes de l'IA doublées aussi). Les **30 premières secondes** sont la phase « Construis » : **aucun envoi de monstres** pour personne (`GRACE` passe de 25 à 30 s et bloque aussi les humains, code d'erreur `early`). Bannière animée « Construis ! » avec logo et chrono « 30 » en gros, chrono de la phase dans le bandeau, onglets de monstres désactivés, 3-2-1, puis bannière « Envoie et résiste ! » avec logo ; sons synthétisés `cor`, `bip`, `go`. **`sim.js` modifié** (redéploiement automatique du serveur). Tests adaptés (or de départ, envois après 30 s) ; nouveaux tests de la phase « Construis » (simulation et parcours mobile). |
| 2026-11-19 | 2.30 | **Flocons reproductibles** (§12.6, §15.2) : en 3D, la position de chaque flocon qui tombe est calculée à partir du temps (`fairePleuvoir(temps)`), et plus en avançant un peu à chaque image. Même mouvement à l'écran. Deux captures au même instant sont désormais identiques : le témoin de la comparaison visuelle 3D passe de 0,1 % à **0,00 %** et la comparaison redevient fiable. `rendu3d.js` seul (`sim.js` et `index.html` non modifiés). |
| 2026-11-18 | 2.31 | **équilibrage des tours** : outillage, **banc d'essai des tours** (`tests/outils/banc-tours.js`, §12) : rendement par or investi de chaque tour et de chaque niveau dans 7 vagues types, avec comparaison avant → après. Premier constat : face à une foule (vague d'IA), une Flammes niveau 5 inflige 187 % des PV de 40 Ogres de la 8e minute, contre 19 % pour un Mage niveau 5 au même prix. **Aucun changement de jeu.** |
| 2026-11-18 | 2.31 | **équilibrage des tours** : Mage (§4.1, §5.1), mesuré avec le banc d'essai : le **Mage** passe de **45 à 55** dégâts de base (+22 %), car il était la tour la moins rentable (indice global 107 au niveau 5, contre 114 à 212 pour les autres). `sim.js` modifié (redéploiement automatique du serveur). Chiffres **à valider par le concepteur**. |
| 2026-11-18 | 2.31 | **équilibrage des tours** : Givre deux fois moins puissant (§4.1, §5.1), à la demande du concepteur : ses dégâts de base passent de **4 à 2** ; son ralentissement (§4.1, `GIVRE_LV`) ne change pas, car c'est lui qui fait la force de la tour. Indice du banc d'essai : 83 → 43 au niveau 1, 137 → 68 au niveau 5 (le banc ne compte pas l'aide du ralentissement aux autres tours). `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-19 | 2.31 | **équilibrage des tours** : outillage, **banc d'essai en parallèle** (§12) : les mesures sont réparties sur tous les cœurs du processeur, avec des résultats identiques à un calcul sur un seul cœur ; une comparaison avec `main` passe d'environ 20 à 25 min à environ 3 min (essai : 16 s au lieu de 126 s). Options `--coeurs` et `--niveaux`. Le banc reste hors de `tout.js` et de la vérification GitHub. **Aucun changement de jeu.** |
| 2026-11-19 | 2.31 | **équilibrage des tours** : l'**Archer** et le **Canon** gardent leurs dégâts d'origine (**8** et **20**), à la demande du concepteur, après des essais à 6 et à 12 au cours de cette version. Seuls le Mage (45 → 55) et le Givre (4 → 2) changent par rapport à la 2.30. `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-19 | 2.31 | **équilibrage des tours** : la **Flammes** garde son cône **sans limite de cibles**, à la demande du concepteur. Une limite à 4 puis à 8 monstres par jet avait été essayée au cours de cette version. Mais depuis la 2.25, les monstres s'écartent les uns des autres, donc une foule tient moins dans le cône : contre une foule de 40 monstres, l'indice du banc d'essai (niveau 5) est passé de 459 avant la 2.25 à 181 sur la 2.30, et la limite à 8 ne le ramenait qu'à 153. **Aucun changement de la Flammes par rapport à la 2.30.** |
| 2026-11-19 | 2.31 | **feuille de route** : idées ajoutées au `README.md` : labyrinthes de l'IA où **chaque tour peut tirer** (pas de tour là où les monstres ne passent jamais), affichage mobile encombré (notamment le message « Touchez deux fois pour construire »), amélioration de plusieurs tours en lot, volants plus compacts, point de relais autour duquel les monstres tournent. **Aucun changement de jeu.** |
| 2026-11-19 | 2.31 | **feuille de route** : idées du concepteur ajoutées au tableau du `README.md`, dans l'ordre prévu : refactorisation des modèles 3D, menu de navigation (lancement d'une partie sur plusieurs écrans), gameplay unique par race (les nouvelles races y étaient déjà), version anglaise, analytique, site web propre (SEO et GEO), tutoriel au lancement, connexion Google ou compte, boutique, campagnes de promotion (visuels, agent Reddit et jeuxvideo.com), paiement, puis monétisation. **Aucun changement de jeu.** |
| 2026-11-19 | 2.32 | **Correctifs et améliorations de la feuille de route** (§9, §15.2) : **barre des cartes à la souris** (molette et glisser, position gardée) ; **affichage mobile désencombré** : plus de bulle « Touchez encore la case » au milieu du terrain, la fiche se réduit pendant l'aperçu et porte la consigne ; **volants plus compacts** (×0,65 en 3D) ; **amélioration en lot** : toucher deux fois une tour choisit jusqu'à 10 tours du même type et du même niveau, rangée d'icônes (celles qu'on ne peut pas payer rétrécissent), un bouton les améliore toutes. Interface seulement : `sim.js` non modifié (pas de redéploiement du serveur). Tests du parcours mobile : aperçu sans bulle, lot, molette. |
| 2026-11-19 | 2.33 | **ia plus stratège** : outillage, **arène des IA** (`tests/outils/arene-ia.js`, §12) : l'IA actuelle affronte celle de `main` dans le même moteur, sièges et factions échangés, sur tous les cœurs du processeur ; points, victoires et écart avec son erreur type. Contrôle : la même IA des deux côtés donne une égalité parfaite. Premier constat : la Horde est la faction la plus faible entre IA (0,88 point de moyenne, contre 1,24 à 1,82). **Aucun changement de jeu.** |
| 2026-11-19 | 2.33 | **ia plus stratège** : **labyrinthes où chaque tour tire** (§8) : l'ordre de construction et la note des plans de l'IA suivent l'**exposition** (cases du chemin vues par chaque tour) au lieu de la seule longueur du chemin. Vers 15 à 25 tours, les tours loin du chemin passent de 3 à 4 à 1 à 2 en moyenne, et chaque tour voit 10 à 50 % de chemin en plus ; chemin un peu plus court à 40 tours (49 cases au lieu de 53 en Normal). **Arène** contre l'IA de `main` (42 parties) : +0,64 point par siège (± 0,19), 29 victoires sur 42. `sim.js` modifié (redéploiement automatique du serveur). Test `labyrinthe` adapté (exposition à 15, 25 et 40 tours au lieu d'un chemin de 50 cases à 40 tours). |
| 2026-11-19 | 2.33 | **ia plus stratège** : **fin de partie** (§8) : quand le plan de l'IA est entièrement construit et toutes ses tours au niveau 5, sa réserve de défense, qui ne pouvait plus servir, passe à l'attaque. **Arène** contre l'étape précédente (42 parties) : +0,76 point par siège (± 0,12), 35 victoires sur 42. `sim.js` modifié (redéploiement automatique du serveur). Nouveau test dans `vagues`. |
| 2026-11-19 | 2.33 | **ia plus stratège** : **vagues selon ce que chaque adversaire peut encaisser** (§8) : l'IA estime, pour chaque famille de monstres, combien passeraient chez chaque adversaire (`encaisse` : dégâts de ses tours contre ce monstre pendant la traversée, avec armure, vol, anti-magie, invisibilité et ralentissement), et envoie celle qui fait perdre le plus de vies, avec du hasard (plus en Normal qu'en Brutal) ; sinon, des monstres au sol pour l'économie. Les boss et les blindés, très difficiles à encaisser, sortent bien plus souvent. **Arène** contre l'étape précédente (42 parties) : +1,33 point par siège (± 0,11), 42 victoires sur 42, parties bien plus courtes. **L'IA devient beaucoup plus dangereuse : difficulté à valider par le concepteur en jouant.** `sim.js` modifié (redéploiement automatique du serveur). Deux tests ajoutés à `vagues`. |
| 2026-11-19 | 2.33 | **ia plus stratège** : outillage, option `--vies` de l'**arène des IA** (§12), pour des parties longues qui atteignent la fin de partie. Deux idées de fin de partie y ont été essayées et **écartées**, car elles affaiblissaient l'IA : remplacer une tour niveau 5 par une plus forte sur sa case (−0,52 point par siège, la tour manque pendant sa reconstruction) et plafonner la réserve de défense à ce qui reste à dépenser (−0,17). **Aucun changement de jeu.** |
| 2026-11-19 | 2.33 | **ia plus stratège** : **type des tours selon la menace reçue** (§8) : l'IA retient les monstres qu'elle reçoit (oubliés peu à peu) et, sur les emplacements ordinaires de son plan, pose le type qui fait le plus de dégâts par or contre eux (armure, vol, anti-magie, zone, chemin à portée) : contre les boss et les blindés, moins d'Archers, plus de Gardes, de Canons et de Mages. Givre et Mages de détection inchangés. **Arène** contre l'étape précédente : +0,52 point par siège (± 0,14), 28 victoires sur 42 ; +0,14 (± 0,14) en parties longues (400 vies). `sim.js` modifié (redéploiement automatique du serveur). Test ajouté à `labyrinthe`. |
| 2026-11-19 | 2.33 | **ia plus stratège** : **performances de l'IA** : l'estimation des défenses adverses suit le chemin de case en case (`chaine`) au lieu du tracé exact (`chemin`, environ 4 % plus court), et garde sur chaque tour les points du chemin qu'elle voit. Mesuré sur 5 parties de 10 min (3 IA, pas de 0,05 s) : l'IA coûte en moyenne 0,02 à 0,04 ms par pas (0,01 à 0,03 sur `main`) ; son pire appel passe de 7 à 10 ms à 3 à 5 ms (2 à 3 ms sur `main`). Mêmes décisions. `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-19 | 2.33 | **ia plus stratège** : **plus de tours, moins d'améliorations en milieu de partie** (§8) : tant que son plan n'est pas fini, l'IA améliore par hasard à partir de 12 tours (25 %, puis 50 % à partir de 28 tours) au lieu de 10 tours (35 %, puis 60 % à partir de 24). **Arène** contre l'étape précédente (60 parties par série) : +0,18 (± 0,11) et +0,27 (± 0,13) sur deux séries de graines, −0,05 (± 0,09) en parties longues. Réglages essayés et écartés : paliers et boss plus tôt (aucun effet), seuil d'envoi à 2 ou 5 revenus (aucun effet net), plafond des vagues à 20 000 or (gagnant en parties courtes, −0,52 en parties longues), plus ou moins de part de défense, coefficient `ENC` à 1,2 ou 2, plus d'améliorations (−0,22). `sim.js` modifié (redéploiement automatique du serveur). |
| 2026-11-19 | 2.34 | **Consigne de construction allégée** (§9) : « Touche encore la case pour construire » s'affiche **entre les deux flèches de rotation**, **une seule fois par partie** (premier aperçu), et la fiche ne répète plus la consigne ensuite. Interface seulement : `sim.js` non modifié. Test du parcours mobile adapté. |
| 2026-11-19 | 2.36 | **cristal hivernal renforcé** : le **Givre renforcé** (emplacement 8 : Cristal hivernal, Totem des esprits, Cristal lunaire, Générateur runique, Cristal corrupteur) coûtait plus cher que le Givre de base mais faisait exactement la même chose. Dégâts : retouche ×0,9 → **×1,5** (Cristal hivernal 2 → 3,4) ; ralentissement : **+10 points** à chaque niveau (`GIVRE_BONUS` : −30 % à −60 % au lieu de −20 % à −50 %). Toujours **pas de cumul avec le Givre** (même famille, le plus fort l'emporte). Fiche à jour. `sim.js` modifié (redéploiement automatique du serveur). Deux tests ajoutés à `deplacements`, `tables` adapté. Chiffres **à valider par le concepteur**. |
| 2026-11-19 | 2.36 | **cristal hivernal renforcé** : outillage, le test de durée de la génération du labyrinthe passe dans son propre fichier (`labyrinthe-duree`), que `tout.js` lance **seul, après les autres** (liste `SEULS`) : depuis les tests en parallèle de la 2.35, il partageait le processeur avec les parties entre IA et échouait au hasard sur GitHub (160 à 190 ms pour 150). Seuils inchangés. **Aucun changement de jeu.** |
| 2026-11-19 | 2.36 | **cristal hivernal renforcé** : correctif outillage, le test navigateur « Les flèches font pivoter la vue… » échouait à chaque fois (la vue ne pivotait pas). Cause : le glissement du test précédent (`glisser` de `tests/outils/navigateur.js`) envoyait tous ses événements tactiles au même instant ; Chromium y voyait un lancer très rapide (« fling ») et, comme sur un vrai écran tactile, avalait le toucher suivant, qui sert à arrêter ce défilement : la flèche recevait pointerdown et pointerup, mais pas de click. Le glissement de test dure désormais 0,3 s (événements horodatés) et le doigt reste immobile 0,2 s avant d'être levé. Test non désactivé, parcours à 30 sur 30. **Aucun changement de jeu.** |
| 2026-11-19 | 2.35 | **terrain dégagé** : **volants deux fois moins grands** (§15.2) : en 3D, les monstres volants passent de ×0,65 à **×0,5** de la taille des autres monstres (`ECH_VOLANTS`), pour moins cacher le terrain. Le rendu 2D de secours et les vignettes ne changent pas. `rendu3d.js` seul : `sim.js` non modifié (pas de redéploiement du serveur). |
| 2026-11-19 | 2.35 | **terrain dégagé** : **affichage mobile désencombré** (§9, §15.2), suite de la 2.32 : la **ligne de détails de la fiche tient sur une ligne** (coupée par « … », un toucher la déplie) ; en 3D, quand on choisit une tour posée, un lot ou l'aperçu d'une construction dont la case est cachée par la fiche ou le bandeau, **la vue glisse en douceur pour la montrer au-dessus de la fiche** (`garderVisible`, `amener`). Avant, la fiche d'une tour posée près du bas de l'écran recouvrait la tour. Interface seulement : `sim.js` non modifié (pas de redéploiement du serveur). |
| 2026-11-19 | 2.35 | **terrain dégagé** : outillage, **tests plus rapides** (§12) : `tout.js` lance les fichiers de test en parallèle (autant que de cœurs moins un, les plus longs d'abord ; `--un-par-un` pour l'ancien fonctionnement), les parties entre IA sont jouées en même temps (`jouerEnParallele`, `worker_threads`, mêmes résultats vérifiés sur les empreintes), et le test « en partie » du labyrinthe a son propre fichier (`labyrinthe-partie`). Mesuré sur 22 cœurs : simulation **24 s → 8 s** (13 s bridé à 4 cœurs, comme sur GitHub), `--complet` **1 min 54 → 29 s**, tout avec le parcours navigateur ≈ 2 min (le parcours 3D en est l'essentiel). Le bilan gameplay rejoue aussi en parallèle les parties du moteur d'avant. Le test « aucune erreur JavaScript » ignore l'icône d'onglet absente que demande Edge (`WR_CANAL=msedge`). **Aucun changement de jeu.** |
| 2026-11-19 | 2.37 | **file d'améliorations** : **panneau « Mes tours »** (§9) : un bouton sous le bandeau ouvre la liste de ses tours par type (nombre par niveau) ; on coche des types, on choisit le niveau visé (2 à 5) et on les ajoute à une **file d'attente** : chaque tour monte niveau par niveau, la moins avancée d'abord, dès que l'or le permet ; faute d'or, la file dépense ce qu'elle peut et le reste attend les revenus. La file se consulte (jauge, or restant) et s'annule ordre par ordre ou en entier ; chevron doré sur les tours en attente. Interface seulement : `sim.js` non modifié (pas de redéploiement du serveur). Nouveau test dans le parcours mobile. |
| 2026-11-19 | 2.38 | **quêtes bonus** : **10 quêtes bonus** au titre décalé (§2), une à la fois, la première à 1:30 puis toutes les 3 à 4 min, tirées sans remise : courses (« Clicker fou » : 10 tours de plus, jamais en fin de partie ; « Le facteur sonne toujours 4 fois » : faire passer 4 de ses monstres, chaque monstre retenant son envoyeur ; « Gonflette » ; « Frozen » ; « Le gros cadeau ») et photos (« Qui a la plus grosse ? » : plus long labyrinthe ; « Picsou » ; « Pigeons voyageurs » ; « Bling-bling » ; « Mamie Gâteau » : le plus petit revenu). Aucune course n'est gagnée d'avance. Récompense : 8 × le revenu moyen (au moins 100 or), partagée en cas d'égalité. Bannière au début et à la fin, pastille de suivi (score, rang, chrono), colonne Quêtes en fin de partie. Les IA jouent les quêtes (50 / 75 / 100 % selon la difficulté) en adaptant constructions, améliorations, économies et envois (§8). **`sim.js` et `server/` modifiés** (redéploiement automatique du serveur ; l'instantané transmet la quête). Nouveau fichier de tests `quetes`, test ajouté au parcours mobile. Choix des quêtes, récompense et rythme validés par le concepteur ; équilibrage **à valider en jouant**. |
| 2026-11-20 | 2.39 | **Style peint commun en 3D** (§15.2) : ombres en paliers, liseré de lumière froide et contour sombre sur toutes les tours, tous les monstres, le portail et le château, ajoutés au chargement des modèles (`rendu3d.js`, aucun modèle régénéré). Les silhouettes se détachent mieux de la neige sur téléphone. `?style=0` garde l'ancien rendu. Coût : ≈ 1,7 fois plus d'appels de dessin, **à vérifier sur un téléphone modeste**. Visuel uniquement : `sim.js` non modifié (pas de redéploiement du serveur). |
| 2026-11-20 | 2.40 | **Races asymétriques** (§4.2, §5) : les 5 factions deviennent 5 races aux tours toutes différentes, chacune avec sa mécanique, ses états et ses combos : **Royaume d'Aubeval** (ex-Alliance : Cohésion, Marqué et Jugement, filets qui abattent les volants, Comptoir marchand), **Clans de l'Orage Blanc** (ex-Horde : Fureur et Rage, chaînes d'éclairs, Trempé et Conduction, Maléfice, saignement), **Elfes de Lunebois** (ex-Sylvestres : poison et Floraison, racines, Croissance, Spores), **Nains de Hautroc** (Forge, Chauffe, armure brisée et Brèche, mines), **Cour des Ossements** (ex-Légion des ombres : âmes, morts relevés, peste et Épidémie, malédictions, Faucheuse). Grille de 10 rôles (dont un anti-aérien dédié, une détection, un soutien et **une ultime par terrain**, code `unique`). **Règles d'équilibrage centrales** (§5.3 : puissance effective, radar à 30 points, couverture obligatoire, plafonds) vérifiées par le nouveau fichier de tests `races`, et **banc des races** (`tests/outils/banc-races.js`) : chaque race entre 1,29 et 1,67 point par partie (1,5 = équilibre). L'IA joue les 5 races (rôles, version renforcée `up`, soutien et ultime, anti-aérien seulement face aux volants, dégâts dans la durée comptés à part). Quête « Frozen » : tours de contrôle au lieu du Givre. Accueil : choix de la race et **fiche de race** (Description, Tours, Combos). En jeu : fiche de tour enrichie, pastilles d'états sur les monstres, textes de combo, âmes dans le bandeau, éclairs, mines et morts relevés en 2D et en 3D. **Modèles 3D des 50 tours refaits** en direction « grimdark » (§15.1 : soldats, créatures, machines et totems sculptés, texture peinte et relief cuits ; budget des tours relevé à 9 000 triangles et 300 Ko, validé par le concepteur). Retouches : arcs et arbalètes épaissis et éclaircis pour rester lisibles, lance-filets (filet déplié sur un râtelier, tromblon à plombs) et champ de mines (poste de sapeurs, chèvre de levage, mines runiques à pointes) refaits. **`sim.js` et `server/` modifiés** (redéploiement automatique du serveur ; l'instantané transmet les états, les âmes, les morts relevés et les mines). Tests adaptés (`tables`, `combats`, `deplacements`, `chantier`, `labyrinthe`, `quetes`, parcours). Chiffres **à valider par le concepteur en jouant**. |
