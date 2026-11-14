/* Intégrité des références : le moteur figé et les fichiers de référence n'ont pas été altérés. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
const {sha256,MOTEURS,RACINE}=require('../outils/moteur');

const EMPREINTE_V17='e0cd2f786b5a3aa616d7446a787436b77d1e30b1bd930e7849a1f1a2a0615f6f'; // git show c868ff9:sim.js | sha256sum

test('Le moteur figé 1.7 est intact (empreinte SHA-256 du commit c868ff9)',()=>{
 assert.equal(sha256(MOTEURS['v1.7']),EMPREINTE_V17,'Le fichier tests/moteurs/v1.7/sim.js a été modifié : il ne doit jamais l\'être.');
});

test('Les références 1.7 ont été produites par ce moteur figé',()=>{
 for(const f of ['statistiques-v1.7.json','parties-v1.7.json']){
  const ref=JSON.parse(fs.readFileSync(path.join(RACINE,'tests','references',f),'utf8'));
  assert.equal(ref.moteur.version,'v1.7');
  assert.equal(ref.moteur.sha256,EMPREINTE_V17,f+' ne provient pas du moteur figé 1.7');
 }
});
