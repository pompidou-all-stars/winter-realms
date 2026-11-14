# Moteur figé — version 1.7

Ce dossier contient une **copie exacte et immuable** du moteur de jeu (`sim.js`) tel qu'il était dans la version 1.7.

| Information | Valeur |
|---|---|
| Commit d'origine | `c868ff9fcd9562c724c40d20c5e5753220459d6f` (« Version 1.7 : la simulation passe dans sim.js ») |
| Extraction | `git show c868ff9:sim.js > tests/moteurs/v1.7/sim.js` |
| Empreinte SHA-256 | `e0cd2f786b5a3aa616d7446a787436b77d1e30b1bd930e7849a1f1a2a0615f6f` |
| Taille | 20 892 octets |

Le `sim.js` des versions 2.0 et 2.0.1 est **identique octet pour octet** à celui-ci : le multijoueur n'a modifié que `index.html` et ajouté `server/`.

## Règles

- **Ne jamais modifier ce fichier.** Le test `tests/simulation/integrite.test.js` recalcule son empreinte à chaque lancement et échoue à la moindre différence.
- Toutes les références de `tests/references/*-v1.7.json` ont été produites à partir de ce moteur, jamais à partir de `main`.
- Quand une future version modifiera le gameplay, on ajoutera un nouveau dossier (`tests/moteurs/v2.1/`…) **sans supprimer celui-ci**.
