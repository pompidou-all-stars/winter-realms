#!/usr/bin/env node
/* Reconstruit assets/audio/manifeste.json à partir des fichiers présents dans assets/audio/.
   Un fichier <dossier>/<id>-<n>.mp3 devient une variante du son <id>. Usage : node art/outils/manifeste-audio.js */
'use strict';
const fs=require('fs'),path=require('path');
const RAC=path.join(__dirname,'..','..','assets','audio');
const sons={};let octets=0,nb=0;
(function parcourir(dos){for(const f of fs.readdirSync(dos).sort()){const p=path.join(dos,f);
 if(fs.statSync(p).isDirectory()){parcourir(p);continue}
 const m=/^(.+)-(\d+)\.mp3$/.exec(f);if(!m)continue;
 (sons[m[1]]=sons[m[1]]||[]).push(path.relative(RAC,p).split(path.sep).join('/'));octets+=fs.statSync(p).size;nb++}})(RAC);
const tri={};for(const k of Object.keys(sons).sort())tri[k]=sons[k];
fs.writeFileSync(path.join(RAC,'manifeste.json'),JSON.stringify({_lisezmoi:'Généré par art/outils/manifeste-audio.js : ne pas éditer à la main.',fichiers:nb,octets,sons:tri},null,1)+'\n');
console.log(nb+' fichiers, '+Object.keys(tri).length+' sons, '+(octets/1048576).toFixed(2)+' Mo');
