"""Échelle des modèles, en cases (1 case = 1 unité).

Les tours font environ 1,1 case de haut. Les monstres sont nettement plus petits, et leur taille
suit le facteur `z` de la table CR de sim.js (le même que pour le dessin 2D), amplifié pour que
la hiérarchie se lise bien : hauteur = 0,40 × z^1,8.
  z 0,75 (Sapeur gobelin) → 0,24   z 0,95 (Brute orc) → 0,36   z 1,1 (Troll) → 0,47
  z 1,2 (Golem) → 0,55             z 1,5 (Cyclope) → 0,83
Volants : envergure ≈ 1,6 × cette hauteur, et ils volent à 0,45 case au-dessus du sol."""

Z = {'sapeur_gobelin': .75, 'warg': .78, 'brute_orc': .95, 'troll': 1.1, 'golem': 1.2, 'cyclope': 1.5,
     'chauve_souris': .75, 'griffon': 1.0, 'dragon': 1.3, 'chaman': .85, 'pretresse': .85, 'gelee': .95,
     'tortue': 1.0, 'briseur': 1.0, 'spectre': .9, 'saboteur': .85, 'heros': 1.35, 'petit_limon': .6}

def hauteur(nom): return .40 * Z[nom] ** 1.8

HAUT_TOUR = 1.1
VOL = .45
