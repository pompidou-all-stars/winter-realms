// Optimise les GLB bruts exportés par Blender (art/_brut/) vers assets/3d/ avec glTF-Transform :
// compression meshopt, sommets soudés, animations rééchantillonnées, données inutiles retirées.
// Les pivots nommés (Tourelle, Tete, Bras…) sont conservés : pas d'aplatissement de la scène.
// Usage : node art/optimiser.mjs   (glTF-Transform 4.2.1 : npx le télécharge si besoin)
import { readdirSync, mkdirSync, statSync, rmSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..');
const BRUT = join(RACINE, 'art', '_brut'), SORTIE = join(RACINE, 'assets', '3d');
const OUTIL = process.env.GLTF_TRANSFORM || null; // chemin d'un gltf-transform déjà installé (facultatif)

const fichiers = [];
(function lister(d) { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? lister(p) : f.endsWith('.glb') && fichiers.push(p) } })(BRUT);
const options = ['--compress', 'meshopt', '--flatten', 'false', '--join', 'false', '--instance', 'false', '--palette', 'false',
  '--simplify', 'false', '--texture-compress', 'false', '--weld', 'true', '--resample', 'true', '--prune', 'true'];
let total = 0;
for (const f of fichiers) {
  const rel = relative(BRUT, f), out = join(SORTIE, rel);
  mkdirSync(dirname(out), { recursive: true });
  const args = ['optimize', f, out, ...options];
  if (OUTIL) execFileSync(OUTIL, args, { stdio: 'ignore', shell: process.platform == 'win32' });
  else execFileSync('npx', ['--yes', '@gltf-transform/cli@4.2.1', ...args], { stdio: 'ignore', shell: process.platform == 'win32' });
  const t = statSync(out).size; total += t;
  console.log(`${rel.padEnd(32)} ${(statSync(f).size / 1024).toFixed(0).padStart(5)} Ko → ${(t / 1024).toFixed(1).padStart(6)} Ko`);
}
console.log(`\n${fichiers.length} modèles, ${(total / 1024 / 1024).toFixed(2)} Mo au total`);
