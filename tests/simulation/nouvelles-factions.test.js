/* Regression: five playable factions and reliable selection wiring. */
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {charger}=require('../outils/moteur');
const S=charger('actuel');
test('Five new factions, ten distinct towers each',()=>{
 assert.deepEqual(Array.from(S.FACTIONS, f=>f.name),['Humains','Robots','Créatures','Nature','Magiques']);
 assert.equal(S.TW.length,50);
 assert.equal(new Set(S.TW.map(t=>t.n)).size,50);
 for(let f=0;f<5;f++){
  assert.equal(S.FACTIONS[f].towers.length,10);
  for(let j=0;j<10;j++){
   const t=S.TW[f*10+j];
   assert.equal(t.faction,f);assert.equal(t.n,S.FACTIONS[f].towers[j]);
   for(const key of ['c','d','r','cd'])assert.ok(Number.isFinite(t[key])&&t[key]>0,t.n+': '+key);
  }
 }
});
test('Faction buttons are present and use exactly one delegated click handler',()=>{
 const html=fs.readFileSync(path.join(__dirname,'../../index.html'),'utf8');
 for(let f=0;f<5;f++){
  assert.match(html,new RegExp('data-faction="'+f+'"'));
  assert.ok(html.includes('<strong>'+S.FACTIONS[f].name+'</strong>'));
 }
 assert.ok(html.includes("factionBox.addEventListener('click'"));
 assert.ok(!html.includes('onclick="window.chooseFaction('),'no duplicate inline handlers');
 assert.ok(html.includes('chosenClass=i;'));
 assert.ok(html.includes('soloSeats(chosenClass)'));
});
test('Factions retain their balanced roles',()=>{
 assert.equal(S.FACTION_BALANCE[0].airBonus,1.18);
 assert.equal(S.FACTION_BALANCE[1].execute,1.30);
 assert.equal(S.FACTION_BALANCE[2].root,1);
 assert.equal(S.FACTION_BALANCE[3].pierce,.55);
 assert.equal(S.FACTION_BALANCE[4].mark,1.14);
});
