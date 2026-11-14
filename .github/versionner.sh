#!/usr/bin/env bash
# Pose une étiquette de version (tag git + « Release » GitHub) sur le commit courant de main.
# Lancé automatiquement par .github/workflows/versions.yml après chaque fusion dans main.
#   - version du jeu lue dans le <title> d'index.html (« Édition X.Y.Z ») ;
#   - première fois qu'une version apparaît : étiquette vX.Y.Z ;
#   - fusions suivantes sans changement de version (tests, documentation, outillage) : vX.Y.Z.1, vX.Y.Z.2…
#   - crée aussi, une seule fois, les étiquettes des versions historiques (1.4 à 2.0.1).
# Essai local sans rien envoyer : SIMULATION=1 bash .github/versionner.sh
set -euo pipefail

SIMULATION="${SIMULATION:-0}"
DEPOT="${GITHUB_REPOSITORY:-pompidou-all-stars/winter-realms}"

existe() { git rev-parse -q --verify "refs/tags/$1" >/dev/null; }

creer() { # creer <étiquette> <commit> <titre> <notes>
  local tag="$1" commit="$2" titre="$3" notes="$4"
  if [ "$SIMULATION" = "1" ]; then
    echo "[simulation] $tag → $(git rev-parse --short "$commit") : $titre"
    git tag -a "$tag" "$commit" -m "$titre" # étiquette locale seulement, pour la suite du calcul
    return
  fi
  git tag -a "$tag" "$commit" -m "$titre"
  git push origin "refs/tags/$tag"
  gh release create "$tag" --repo "$DEPOT" --verify-tag --title "$titre" --notes "$notes"
  echo "Créé : $tag → $(git rev-parse --short "$commit")"
}

RETOUR="Pour revenir à cette version, demander à Claude : « reviens à la version TAG » (voir CLAUDE.md §14). Le code de cette version est aussi téléchargeable ci-dessous (Source code)."

# 1. versions historiques, créées une seule fois
while read -r tag commit titre; do
  [ -z "$tag" ] && continue
  if ! existe "$tag" && git cat-file -e "${commit}^{commit}" 2>/dev/null; then
    creer "$tag" "$commit" "Winter Realms $titre" "Version historique. ${RETOUR//TAG/$tag}"
  fi
done <<'EOF'
v1.4 bfc655acb6fbdc61dac0452f0e55ba181e09bfc1 1.4 — import initial
v1.6 5dee0621f463e3784294252eb171091ea6e8213b 1.6 — plateau diorama et décor par biome
v1.6.1 313ce1032aee8e3b8267e91d3cfdd4be5466eaac 1.6.1 — correction des racines sylvestres
v1.7 c868ff9fcd9562c724c40d20c5e5753220459d6f 1.7 — la simulation passe dans sim.js
v2.0 e4636a4d5f52e2c7d641725a664591505b903332 2.0 — multijoueur en ligne
v2.0.1 4a1fb640d05e31b467d3ac40281e4611ac91f9e7 2.0.1 — jeu en ligne réservé à la France, règle des branches, déploiement automatique du serveur
EOF

# 2. le commit courant
if [ -n "$(git tag --points-at HEAD)" ]; then
  echo "Ce commit a déjà une étiquette : $(git tag --points-at HEAD | tr '\n' ' ')"; exit 0
fi
version="$(grep -o 'Édition [0-9][0-9.]*[0-9]' index.html | head -1 | sed 's/^Édition //')"
if [ -z "$version" ]; then echo "Version introuvable dans le <title> d'index.html"; exit 1; fi
precedent="$(git describe --tags --abbrev=0 HEAD 2>/dev/null || true)"
tag="v$version"; n=0
while existe "$tag"; do n=$((n+1)); tag="v$version.$n"; done
if [ "$n" = "0" ]; then titre="Winter Realms $version"; else titre="Winter Realms $version — révision $n (jeu inchangé)"; fi
changements="$(git log --no-merges --format='- %s' ${precedent:+$precedent..}HEAD | head -40)"
creer "$tag" HEAD "$titre" "Changements depuis ${precedent:-le début} :
$changements

${RETOUR//TAG/$tag}"
