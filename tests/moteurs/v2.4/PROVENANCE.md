# Moteur figé — version 2.4

Ce dossier contient une **copie exacte et immuable** du moteur de jeu (`sim.js`) de la version 2.4 (temps de construction des tours), figée après la validation du concepteur.

| Information | Valeur |
|---|---|
| Commit d'origine | `b309a257829012b654e4b4c1062d2b6bcbfb6eb0` (« Raccourcit le temps de construction et le lie à la difficulté ») |
| Extraction | `git show b309a25:sim.js > tests/moteurs/v2.4/sim.js` |
| Empreinte SHA-256 | `1d2b8ad6a567bf4478615f7bb7920a38334dd4b8eab76ef7160975aa6398ad36` |
| Taille | 21 726 octets |

## Règles

- **Ne jamais modifier ce fichier.** Le test `tests/simulation/integrite.test.js` recalcule son empreinte à chaque lancement.
- Les références `tests/references/*-v2.4.json` ont été produites à partir de ce moteur (`node tests/outils/creer-references.js v2.4`), jamais à partir de `main`.
- Depuis la 2.4, ce sont **ces références** que les tests comparent au jeu. Le moteur 1.7 et ses références restent dans le dépôt, sans être supprimés.
