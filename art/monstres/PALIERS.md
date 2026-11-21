# Monstres des paliers (préparation de la PR B)

> **2.40 : bestiaire épique.** Les noms et les modèles ci-dessous sont ceux d'avant la 2.40. Les monstres ont été renommés à la même place (mêmes prix et capacités) : la liste à jour est dans CLAUDE.md §6.2, les scripts dans ce dossier (kit `communs/creatures.py`, CLAUDE.md §15.1).

Décision du concepteur (2026-11-15) : **3 paliers**, et dans chaque palier **24 monstres** :
12 au sol (les plus rentables pour le revenu), 3 volants, 8 magiques et 1 boss. Soit 72 monstres.

Capacités magiques (une par monstre magique, dans chaque palier) : **aura de vitesse**, **invisible**,
**se divise**, **accéléré**, **anti-magie** (insensible au Givre et au Mage), **soin**, **armure (blindé)**,
**étourdissement**.

La colonne « clé » est la clé `CR[…].g` à utiliser dans `sim.js` : le modèle est `assets/3d/monstres/<clé>.glb`.
Les noms, les clés et les tailles (`z`) sont des propositions ; seule la composition (12 / 3 / 8 / 1 par palier)
est une décision du concepteur. ✅ = modèle prêt.

## Palier 1 (gratuit)

| Rôle | Monstre | Clé | z |
|---|---|---|---|
| Sol | Sapeur gobelin ✅ | `gob` | 0,75 |
| Sol | Rat des neiges ✅ | `rat` | 0,7 |
| Sol | Kobold ✅ | `kobold` | 0,78 |
| Sol | Warg ✅ | `wolf` | 0,78 |
| Sol | Squelette du givre ✅ | `skel` | 0,85 |
| Sol | Sanglier de guerre ✅ | `boar` | 0,9 |
| Sol | Gnoll ✅ | `gnoll` | 0,9 |
| Sol | Maraudeur ✅ | `raider` | 0,9 |
| Sol | Myconide ✅ | `myco` | 0,95 |
| Sol | Brute orc ✅ | `orc` | 0,95 |
| Sol | Troll des glaces ✅ | `troll` | 1,1 |
| Sol | Yéti ✅ | `yeti` | 1,15 |
| Volant | Chauve-souris ✅ | `bat` | 0,75 |
| Volant | Guêpe des glaces ✅ | `wasp` | 0,7 |
| Volant | Harpie ✅ | `harpy` | 0,85 |
| Aura de vitesse | Chaman de guerre ✅ | `chaman` | 0,85 |
| Invisible | Spectre ✅ | `spectre` | 0,9 |
| Se divise | Gelée mutante ✅ | `slime` | 0,95 |
| Accéléré | Lutin des glaces ✅ | `imp` | 0,7 |
| Anti-magie | Briseur de runes ✅ | `breaker` | 1,0 |
| Soin | Prêtresse ✅ | `healer` | 0,85 |
| Armure | Tortue ✅ | `turtle` | 1,0 |
| Étourdissement | Saboteur gobelin ✅ | `sapper` | 0,85 |
| Boss | Roi gobelin ✅ | `gobking` | 1,2 |

## Palier 2

| Rôle | Monstre | Clé | z |
|---|---|---|---|
| Sol | Homme-lézard ✅ | `lizard` | 1,05 |
| Sol | Chevalier noir ✅ | `knight` | 1,1 |
| Sol | Gargouille ✅ | `gargoyle` | 1,1 |
| Sol | Loup-garou ✅ | `werewolf` | 1,15 |
| Sol | Ours de guerre ✅ | `bear` | 1,15 |
| Sol | Ogre ✅ | `ogre` | 1,2 |
| Sol | Minotaure ✅ | `minotaur` | 1,2 |
| Sol | Golem runique ✅ | `golem` | 1,2 |
| Sol | Automate blindé ✅ | `automaton` | 1,2 |
| Sol | Wendigo ✅ | `wendigo` | 1,25 |
| Sol | Rhinocéros de guerre ✅ | `rhino` | 1,3 |
| Sol | Mammouth de guerre ✅ | `mammoth` | 1,45 |
| Volant | Griffon corrompu ✅ | `griffon` | 1,0 |
| Volant | Vouivre ✅ | `wyvern` | 1,15 |
| Volant | Manticore ✅ | `manticore` | 1,2 |
| Aura de vitesse | Tambour de guerre ✅ | `drummer` | 1,05 |
| Invisible | Assassin des ombres ✅ | `assassin` | 1,0 |
| Se divise | Golem de boue ✅ | `mudgolem` | 1,15 |
| Accéléré | Centaure messager ✅ | `centaur` | 1,15 |
| Anti-magie | Inquisiteur ✅ | `inquisitor` | 1,1 |
| Soin | Druidesse ✅ | `druid` | 1,05 |
| Armure | Scarabée cuirassé ✅ | `beetle` | 0,95 |
| Étourdissement | Ingénieur nain renégat ✅ | `engineer` | 1,0 |
| Boss | Cyclope des cendres ✅ | `cyc` | 1,5 |

## Palier 3

| Rôle | Monstre | Clé | z |
|---|---|---|---|
| Sol | Roi-liche ✅ | `lich` | 1,3 |
| Sol | Seigneur de guerre orc ✅ | `warlord` | 1,35 |
| Sol | Élémentaire de feu ✅ | `fireel` | 1,4 |
| Sol | Démon des abysses ✅ | `demon` | 1,5 |
| Sol | Golem de lave ✅ | `lavagolem` | 1,5 |
| Sol | Ver des neiges ✅ | `wyrm` | 1,5 |
| Sol | Chimère ✅ | `chimera` | 1,5 |
| Sol | Géant du givre ✅ | `giant` | 1,6 |
| Sol | Sylvain corrompu ✅ | `treant` | 1,6 |
| Sol | Mastodonte de fer ✅ | `juggernaut` | 1,6 |
| Sol | Béhémoth ✅ | `behemoth` | 1,7 |
| Sol | Colosse de pierre ✅ | `colossus` | 1,75 |
| Volant | Dragon ancien ✅ | `dragon` | 1,3 |
| Volant | Phénix de givre ✅ | `phoenix` | 1,3 |
| Volant | Oiseau-roc ✅ | `roc` | 1,45 |
| Aura de vitesse | Héraut de guerre ✅ | `herald` | 1,3 |
| Invisible | Faucheuse ✅ | `reaper` | 1,3 |
| Se divise | Hydre ✅ | `hydra` | 1,45 |
| Accéléré | Destrier de cauchemar ✅ | `nightmare` | 1,3 |
| Anti-magie | Dévoreur de mana ✅ | `manaeater` | 1,35 |
| Soin | Grande prêtresse de sang ✅ | `bloodpriest` | 1,25 |
| Armure | Tortue-dragon ✅ | `dragonturtle` | 1,45 |
| Étourdissement | Golem du tonnerre ✅ | `thunder` | 1,45 |
| Boss | Azh'Khar, seigneur des lames ✅ | `hero` | 1,35 |
