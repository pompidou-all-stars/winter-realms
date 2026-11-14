# three.js r170 (copie figée)

- Source : paquet npm `three@0.170.0` (https://github.com/mrdoob/three.js), licence MIT (fichier `LICENSE`).
- Fichiers copiés tels quels, sans modification :
  - `build/three.module.min.js` → `three.module.min.js`
  - `examples/jsm/loaders/GLTFLoader.js` → `addons/loaders/GLTFLoader.js`
  - `examples/jsm/utils/BufferGeometryUtils.js` → `addons/utils/BufferGeometryUtils.js`
  - `examples/jsm/libs/meshopt_decoder.module.js` → `addons/libs/meshopt_decoder.module.js`
- Chargés par l'importmap d'`index.html` (`three` et `three/addons/`), uniquement en mode `?rendu=3d`.
- Pour changer de version : refaire la copie depuis le paquet npm et mettre à jour ce fichier.
