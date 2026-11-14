/* Générateur de hasard « à graine » (mulberry32), utilisé UNIQUEMENT par les tests.
   Une même graine donne toujours la même suite de nombres, donc la même partie.
   Le jeu lui-même n'est pas modifié : les tests remplacent Math.random dans un environnement isolé. */
'use strict';
function mulberry32(graine){let a=graine>>>0;return function(){a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}}
/* même code, sous forme de texte, pour l'injecter dans le navigateur */
const SOURCE_NAVIGATEUR=`(function(){var g=window.__GRAINE__>>>0;var a=g;Math.random=function(){a=(a+0x6D2B79F5)>>>0;var t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296}})();`;
module.exports={mulberry32,SOURCE_NAVIGATEUR};
