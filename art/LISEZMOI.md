# Assets 3D de Winter Realms

Ce dossier contient les **recettes** des modèles 3D du jeu : un script Python Blender par asset.
Les fichiers 3D livrés au jeu (`assets/3d/*.glb`) sont **toujours produits à partir de ces scripts**, jamais retouchés à la main.
Avantages : tout est reproductible, modifiable par une simple instruction (« tour plus massive »), versionné, et chacun peut contribuer en parallèle.

## Où se passe quoi

| Besoin | Où | Comment |
|---|---|---|
| Créer un nouveau modèle ou changer de style, en voyant le résultat en direct | PC du concepteur (Blender + MCP), ou à distance via Remote Control | Claude travaille dans la scène Blender ouverte, puis écrit/met à jour le script de l'asset |
| Retouche mineure (couleur, proportion, détail) | N'importe où : session cloud, PC, autre contributeur | Modifier le script, puis lancer la génération (ci-dessous) |
| Vérifier une PR | GitHub, automatiquement | Action « Assets 3D » : régénère tout, contrôle budgets et manifeste, joint les aperçus |

Blender tourne sans écran ni carte graphique : **une session cloud peut régénérer les assets** (`pip install bpy==5.3.0`), même PC éteint.

## Organisation et noms

| Chemin du script | Fichier produit | Correspond dans le jeu à |
|---|---|---|
| `art/tours/<faction>-<j>.py` | `assets/3d/tours/<faction>-<j>.glb` | la tour `TW[faction × 10 + j]` (`j` = emplacement 0 à 9, §4.2 de CLAUDE.md) |
| `art/monstres/<g>.py` | `assets/3d/monstres/<g>.glb` | le monstre dont `CR[…].g` vaut `<g>` (`gob`, `wolf`, `orc`, `troll`, `golem`, `cyc`, `bat`, `griffon`, `dragon`, `chaman`, `healer`, `slime`, `turtle`, `breaker`, `spectre`, `sapper`, `hero`) |
| `art/decor/<nom>.py` | `assets/3d/decor/<nom>.glb` | terrain, portail, château, décor |
| `art/exemples/<nom>.py` | `assets/3d/exemples/<nom>.glb` | non utilisé par le jeu (démonstration) |
| `art/communs/*.py` | — | pièces et réglages partagés (socles de faction, matériaux…), importables : `from communs import socles` |

`<faction>` : `alliance`, `horde`, `sylvestres`, `nains`, `ombres` (dans l'ordre de `FACTIONS`).

## Écrire un asset

```python
INFOS = {'categorie': 'tour', 'titre': 'Tour des archers'}   # catégorie : tour, monstre, decor ou exemple

def construire(ctx):
    bpy = ctx.bpy                       # Blender
    couleur = ctx.jeu['FACTIONS'][0]['color']   # tables du jeu lues dans sim.js (FACTIONS, TW, CR)
    pierre = ctx.materiau('pierre', '#e9e2cf')  # couleur '#rrggbb', rugosite=…, metal=…
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.9, location=(0, 0, 0.45))
    ctx.habiller(ctx.biseau(bpy.context.object, 0.02), pierre)
```

Le script part d'une scène **vide** et crée seulement ses objets : pas de caméra ni de lumière (elles ne sont pas exportées).
Modèle complet : `art/exemples/caisse.py`.

### Conventions de forme
- **1 unité = 1 case** du terrain. L'origine (0, 0, 0) est **au sol, au centre de la case**. Axe Z vers le haut (Blender).
- Une tour tient dans **0,9 × 0,9** au sol et mesure au plus **1,6** de haut ; sa face avant regarde vers **−Y**.
- Les couleurs de faction viennent de `ctx.jeu['FACTIONS'][f]['color']` : un changement de couleur dans le jeu se reporte sur les modèles à la prochaine génération.
- Les **niveaux d'amélioration** (taille, pastilles) sont gérés par le jeu à l'affichage : un seul modèle par tour et par monstre. Depuis la 2.7, les **animations de marche et de vol** des monstres sont dans le fichier (pistes NLA `marche` et `vol`, voir plus bas) ; les autres petits mouvements (rotation des cristaux, flammes, visée) sont faits par le jeu sur des **pivots nommés**.
- **Licences** : aucun modèle ni texture externe sauf licence **CC0** (par exemple Poly Haven), avec la source notée en commentaire dans le script. Pas de génération 3D par IA sans accord du concepteur.

## Générer les fichiers 3D

Depuis la racine du dépôt :

- **Cloud ou Python avec bpy** (`pip install -r art/outils/requirements.txt`, et **Node.js** : ce Blender ne sait pas compresser, `generer.py` compresse alors automatiquement avec gltf-transform) :
  ```bash
  python art/outils/generer.py tours/alliance-0      # un asset
  python art/outils/generer.py                        # tous
  python art/outils/generer.py --apercus apercus      # + une image PNG par asset dans apercus/
  python art/outils/generer.py --verifier             # contrôle sans rien modifier
  ```
- **PC avec Blender installé** (adapter le chemin de Blender) :
  ```bash
  "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --background --python art/outils/generer.py -- tours/alliance-0
  ```
- **Ne pas lancer la génération depuis la scène Blender ouverte** (MCP) : elle vide la scène. Dans Blender ouvert, on conçoit ; l'export définitif passe toujours par la commande.

Puis commiter **le script, le `.glb` et `assets/3d/manifeste.json` ensemble**.

## Contrôles automatiques
- `assets/3d/manifeste.json` note pour chaque asset : son fichier, ses triangles, sa taille et l'**empreinte de son script** (script + `art/communs/`).
- `tests/simulation/assets3d.test.js` (sur chaque PR, sans Blender) : chaque script a son fichier, aucun fichier n'est en retard sur son script, chaque fichier est un GLB valide et respecte son budget.
- Action GitHub « Assets 3D » (sur les PR qui touchent `art/` ou `assets/3d/`) : régénère tout avec Blender 5.3, vérifie, et joint les images d'aperçu (onglet *Actions → Artifacts → apercus-3d*).
- Budgets par fichier dans `art/budgets.json` : tour et monstre ≤ 3 000 triangles et 150 Ko, décor ≤ 6 000 triangles et 300 Ko, total ≤ 20 Mo depuis la 2.40 (monstres ≤ 4 500 triangles et 300 Ko). Le jeu doit rester fluide sur téléphone.
- Modifier un fichier de `art/communs/` change l'empreinte de **tous** les assets : il faut alors tout régénérer (`python art/outils/generer.py`).

## Modèles du jeu (depuis la 2.7)

Les 50 tours, les 17 monstres, le portail et le château sont construits avec les pièces communes de `art/communs/` (un paquet Python : `from communs.tours_communes import tour`) :

| Module | Rôle |
|---|---|
| `outils.py` | formes de base (cylindre, boîte, sphère, cône, tore, prisme), matériaux par couleur, **peinture des sommets** (dégradé sombre en bas, clair en haut, léger grain), `SIMPLE` pour alléger les petits personnages |
| `factions.py` | palettes des 5 factions (reprises de la 2D, avivées) et **socles** |
| `personnages.py` | personnage caricatural paramétrable (nez, oreilles, défenses, casque, capuche, barbe, robe, cape, couronne, plumes, un œil…) et armes |
| `betes.py` | quadrupèdes, volants (ailes membrane ou plumes), gelées |
| `animations.py` | animations par pièces, sans squelette : `marche`, `trot`, `saut`, `flotte`, `vol` |
| `echelles.py` | tailles des monstres : `0,40 × z^1,8` cases (z de `CR`) |
| `tours_communes.py` | les 6 archétypes de tours déclinés par `STYLE` de faction ; `tour(faction, j)` |
| `neige.py` | `enneiger(racine)` (2.9) : neige sur les faces tournées vers le ciel (haut seulement sur les pentes), hors personnages, pièces animées et lumineuses, dans la limite du budget de triangles |
| `decor.py` | portail, château, plateau de référence |
| `export_jeu.py` | `preparer(racine)`, à appeler **à la fin de `construire`** : couleurs cuites dans les sommets (matériau unique `Peint`, `Lueur_…` pour les pièces lumineuses, `Drapeau` gardé), pièces fusionnées sous chaque pivot |
| `rendu.py` | rendus de validation (EEVEE) |

- **Pivots nommés** (objets vides) : `Tourelle` (vise la cible), `Cristal`, `Eclats`, `Flamme`, `Anneaux`, `Orbe`, `AnneauFlottant`, `Anneau1..3` (portail), `Corps`, `Tete`, `BrasG`, `BrasD`, `JambeG`… `generer.py` exporte les maillages **et** les objets vides, les animations **par piste NLA** et compresse en **meshopt** (`EXT_meshopt_compression`, lu par three.js).
- **Monstres** : `monstres/<g>.py` pour chaque clé `g` de `CR`. Plusieurs monstres peuvent partager une clé (le Petit limon utilise `slime`) : le jeu met alors le modèle à l'échelle de leur `z`.
- **Concevoir dans Blender ouvert** (MCP) : `exec(open(r'<dépôt>\art\outils\atelier.py', encoding='utf-8').read())` recharge les pièces communes ; `atelier_asset('tours/horde-3')` construit un asset dans la scène, sans l'exporter ; `art/outils/planches.py` fait les planches de validation. L'export définitif passe toujours par `generer.py`.
- Vérifications propres aux modèles du jeu : `tests/simulation/modeles-3d.test.js` (un modèle par tour et par clé de monstre, animations, `Tourelle`, meshopt, `Drapeau`).

## Travailler à plusieurs
- **Un asset = un fichier** : deux personnes qui travaillent sur deux tours différentes n'ont jamais de conflit.
- `art/communs/` est partagé : prévenir les autres avant d'y toucher, et régénérer tous les assets dans la même PR.
- Si deux branches régénèrent le même asset, garder la version du script retenu et **relancer la génération** plutôt que de fusionner les `.glb` à la main.
- Le jeu doit toujours fonctionner si un modèle manque (affichage de repli) : un contributeur peut ajouter un monstre au jeu avant que son modèle 3D existe.
