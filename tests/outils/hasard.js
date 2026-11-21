/* Générateur de hasard « à graine » (mulberry32), utilisé UNIQUEMENT par les tests.
   Une même graine donne toujours la même suite de nombres, donc la même partie.
   Le jeu lui-même n'est pas modifié : les tests remplacent Math.random dans un environnement isolé. */
'use strict';
function mulberry32(graine){let a=graine>>>0;return function(){a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
/* même code, sous forme de texte, pour l'injecter dans le navigateur.
   2.29 : deux suites séparées, choisies selon le fichier qui appelle Math.random : une pour la simulation (sim.js), une pour
   tout le reste (interface, sons, three.js). En 3D, three.js tire un nombre à chaque objet créé, et les modèles se chargent en
   temps réel : sur une suite commune, la partie changeait d'un lancement à l'autre (autres vagues des IA, autre or), et les
   captures 3D n'étaient pas comparables. Le jeu n'est pas modifié. */
const SOURCE_NAVIGATEUR=`(function(){function suite(a){return function(){a=(a+0x6D2B79F5)>>>0;var t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
var g=window.__GRAINE__>>>0,jeu=suite(g),reste=suite((g^0x9E3779B9)>>>0),simJs=/\\/sim\\.js[?:]/;
Math.random=function(){var l=Error.stackTraceLimit;Error.stackTraceLimit=2;var s=new Error().stack||'';Error.stackTraceLimit=l;
 return simJs.test(s.split('\\n').slice(2).join(' '))?jeu():reste()}})();`;
module.exports={mulberry32,SOURCE_NAVIGATEUR};
