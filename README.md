# Winter Realms — Tower Wars

## 🗺️ Feuille de route — idées d'améliorations

Une idée ? **[➕ Proposer une idée](https://github.com/pompidou-all-stars/winter-realms/issues/new?template=idee.yml)** (formulaire GitHub, marche aussi sur téléphone), ou ajoute une ligne ici dans une PR. Toutes les idées : [onglet Issues, étiquette « idée »](https://github.com/pompidou-all-stars/winter-realms/issues?q=label%3Aid%C3%A9e).

Statuts : 💡 idée · 🧭 à préciser · 🛠️ en cours · ✅ fait

| Statut | Domaine | Idée |
|---|---|---|
| ✅ | 🐞 Correctif | **Défilement des cartes sur PC** : on ne peut plus faire défiler la barre des tours et des monstres à la souris. *Fait en 2.32 : molette et glisser à la souris.* |
| ✅ | 🐞 Correctif | **Affichage mobile encombré** : trop de fenêtres et de panneaux par-dessus le terrain, on ne voit plus où l'on construit, notamment avec le message « Touchez deux fois pour construire ». *Fait en 2.32 : plus de bulle au milieu du terrain, fiche réduite pendant l'aperçu ; en 2.35 : détails de la fiche sur une ligne, et la vue glisse pour que la tour choisie ne soit jamais cachée par la fiche.* |
| ✅ | 🤖 IA | **Labyrinthes** : construction plus efficace et plus variée. **Chaque tour doit pouvoir tirer** : ne pas laisser de tours à des endroits où les monstres ne passent jamais (hors de portée du chemin). |
| ✅ | 🤖 IA | **Répartition des tours** : meilleur choix des types et des emplacements (Givre, Mages, anti-aérien…). |
| ✅ | 🤖 IA | **Stratégie par phase** : début, milieu et fin de partie (économie, défense, attaque). |
| ✅ | 🤖 IA | **Monstres envoyés** : composition des vagues mieux adaptée aux faiblesses des adversaires. |
| 💡 | ⚖️ Difficulté | **Avantages supplémentaires pour l'IA** si elle reste trop faible (or, revenu, vies, construction plus rapide…). |
| ✅ | 🏰 Tours | **Améliorer en lot** : un moyen d'améliorer plusieurs tours d'un coup. *Fait en 2.32 : toucher deux fois une tour choisit jusqu'à 10 tours du même type et du même niveau, montrées en icônes ; un bouton les améliore toutes ; si l'or manque, les icônes de celles qui ne seront pas améliorées rétrécissent. En 2.37 : panneau « Mes tours » (cocher des types, niveau visé de 2 à 5) et file d'attente qui améliore niveau par niveau dès que l'or le permet, consultable et annulable.* |
| 💡 | 🏰 Tours | **Diversification des tours** : nouveaux effets et rôles, tours plus distinctes d'une faction à l'autre. |
| ✅ | 👹 Monstres | **Volants plus compacts** : réduire la taille des unités volantes pour qu'elles prennent moins de place (deux fois moins). *Fait en 2.35 : ×0,5 en 3D (×0,65 en 2.32).* |
| 💡 | 🧭 Gameplay | **Point de relais** : pouvoir poser un point de passage autour duquel les monstres tournent. |
| ✅ | 🛡️ Factions | **Nouvelles races** jouables, avec leurs tours, leur bonus et leur style. |
| ✅ | 🔧 Outillage | **Accélérer les tests** : la simulation (`node tests/tout.js`) prend plusieurs minutes ; la rendre plus rapide pour tester plus souvent. *Fait en 2.35 : tests et parties entre IA en parallèle ; simulation 24 s → 8 s, 15 parties 1 min 54 → 29 s (sur 22 cœurs).* |
| ✅ | 🎯 Quêtes | **Quêtes bonus** : une récompense pour le premier qui réussit (ex. : « le plus long labyrinthe au tour X gagne N or »). Quêtes tirées au hasard à chaque partie ; l'IA doit savoir les jouer. *Fait en 2.38 : 10 quêtes au titre décalé (« Qui a la plus grosse ? », « Clicker fou », « Picsou »…), une toutes les 3 à 4 min, annoncées par une bannière, suivies dans une pastille, gagnant annoncé ; les IA les jouent.* |
| 🧭 | ✨ Palier 3 | **Pouvoirs magiques payants** : renforcements sur son propre terrain, ou malédictions à lancer sur le terrain d'un adversaire. |
| 💡 | 🧊 Modèles 3D | **Refactorisation des modèles 3D**. |
| 💡 | 🧭 Interface | **Menu de navigation** : lancement d'une partie sur plusieurs écrans successifs. |
| ✅ | 🛡️ Factions | **Gameplay unique par race** : chaque race se joue différemment. |
| 💡 | 🌍 Langues | **Version anglaise** (localisation). |
| 💡 | 📊 Analytique | **Analytique** : mesurer comment le jeu est utilisé. |
| 💡 | 🌐 Site web | **Site web propre** autour du jeu, optimisé pour les moteurs de recherche (SEO) et les moteurs d'IA (GEO). |
| 💡 | 🎓 Tutoriel | **Tutoriel au lancement** du jeu. |
| 💡 | 🔑 Compte | **Connexion** avec Google, ou création d'un compte. |
| 💡 | 🛒 Boutique | **Boutique** (store). |
| 💡 | 📣 Promotion | **Campagnes de promotion** : visuels de campagne, agent pour Reddit et jeuxvideo.com. |
| 💡 | 💳 Paiement | **Système de paiement**. |
| 💡 | 💰 Monétisation | **Monétisation**, une fois les idées précédentes en place. |

A browser tower-wars game: the game itself is `index.html` (interface, drawing, sounds) plus `sim.js` (the simulation, also used by the multiplayer server). No build step, no dependencies.

## Play

Online: **https://pompidou-all-stars.github.io/winter-realms/** (updated automatically on every push to `main`).

Locally: serve the folder with any static web server (for example `npx http-server`) and open http://localhost:8080. Opening `index.html` directly from disk does not always load `sim.js`.

## Contributing

The project is hosted by the [pompidou-all-stars](https://github.com/pompidou-all-stars) organization. Get a copy with:

```bash
git clone https://github.com/pompidou-all-stars/winter-realms.git
```

1. Never commit to `main`. Create a branch from an up-to-date `main` (`git checkout main && git pull && git checkout -b <type>/<topic>`).
2. Make your changes, run the tests (`node tests/tout.js`), then commit and `git push` your branch.
3. Open a pull request. GitHub runs the simulation tests automatically (check "Tests de simulation"). Merge only once it is green and the change is validated.

Game rules, balance tables and project conventions are documented (in French) in [CLAUDE.md](CLAUDE.md). Every change must update CLAUDE.md and the changelog below.

## Tests

Only Node.js 22 is required; browser tests also use Playwright/Chromium when available (skipped otherwise).

```bash
node tests/tout.js
```

- `node tests/tout.js --simulation`: simulation tests only (what GitHub runs on every pull request), about 10 s. Test files run in parallel; `--un-par-un` runs them one after the other.
- `node tests/bilan.js`: the three reports (technical, gameplay, visual) in `rapports/bilan.html`, including a before/after visual comparison with `main`.
- `node tests/captures.js`: phone screenshots (portrait and landscape) in `captures/actuel/`.

Details (in French): CLAUDE.md, sections 12 and 13.

## Play together

On the site, enter a nickname, click **Créer un salon** and share the link (or the 4-letter code). Friends click the link (or type the code and **Rejoindre**), pick a faction, and the room leader clicks **Lancer la partie**. Empty seats are played by AIs.

The multiplayer server runs on Cloudflare Workers (free plan), in [`server/`](server/). It is **redeployed automatically** by a GitHub Action whenever a change to `sim.js` or `server/` is merged into `main` (see CLAUDE.md, section 9 bis). Manual fallback: `cd server` then `npx wrangler deploy`.

## Changelog

### 2.42 — factions et tirs lisibles — 2026-11-21
- Humains, Robots, Créatures, Herbe and Magique are selectable at launch, with 10 towers each and the asymmetric mechanics of 2.40.
- Robot and creature silhouettes appear in game and in tower cards. Projectile trails point back to the shooter in 2D and 3D and shorten in dense fights.
- Base damage is 9 for Chasseur épineux and 5.1 for Drone sentinelle. Damage over time accounts for partial ticks. The bone colossus now summons when 15 souls are available. The multiplayer server sends projectile origins.

### 2.41 — bestiaire épique — 2026-11-21
- New epic bestiary: the 72 monsters are renamed in place (same costs, HP, speeds and abilities; only display sizes change): goblins, rat-men, orcs, ogres, mounted saurians, Ruin warriors, Abyssal Oculus, Brain-eater, Abyssal Elder, Lord of Embers…
- All 78 monster models are rebuilt with the new creature kit: shared skeletons (biped, quadruped, flyer), a detailed sculpt baked into a painted texture and a normal map, walk or fly, hit and death animations. In game, a hit monster flinches; a killed monster falls, stays on the ground, then sinks. 6 models are ready for upcoming abilities (summoning, resurrection). After reviewing the boards, 14 tier 2 and 3 monsters were retouched (carved rock for the golem and titan, wyrm, reaper, spectre, mana eater, Lord of Embers, Abyssal Elder, mammoth tower, behemoth, Ruin champion, chimera, giant, doom wheel). Total 3D budget raised to 20 MB (78 monsters loaded by tier).
- `sim.js` changed (names, model keys and sizes only; the server redeploys automatically).
- Tooling: monster generation is much faster (bat 595 s → 7 s, orc 36 s → 11 s; same models). The GitHub "Assets 3D" check, stopped at 30 min, fits in its time limit again (10 min for all 131 assets locally).

### 2.40 — races asymétriques — 2026-11-20
- The 5 factions become 5 asymmetric races with 10 different towers each, their own mechanic, status effects and combos: Royaume d'Aubeval (cohesion, judgement seal, nets that ground flyers, trading post), Clans de l'Orage Blanc (fury and rage, chain lightning, soaked and conduction, hex, bleeding), Elfes de Lunebois (stacking poison and bloom, roots, growth, spores), Nains de Hautroc (forge, heat and overheat, armour break, mines), Cour des Ossements (souls, raised dead, plague and epidemic, curses, reaper).
- 10 roles per race (base, close range, control, area, dedicated anti-air, detection, signature, support, anti-boss, ultimate — one ultimate per field).
- Central balancing rules (effective power, 30-point radar profile, mandatory coverage, caps) checked by a new test file, and a race bench (`tests/outils/banc-races.js`): every race scores between 1.29 and 1.67 points per game (1.5 = even).
- Home screen: race choice and a race sheet (description, towers, combos). In game: richer tower sheet, status pips on monsters, combo texts, souls counter, lightning, mines and raised dead in 2D and 3D. New 3D models for all 50 towers in a darker, “grimdark” art direction: soldiers, creatures, siege engines and totems sculpted with the organic-monster process (painted texture and baked relief), not all towers are towers. Tower budget raised to 9,000 triangles and 300 KB (approved by the designer).
- `sim.js` and `server/` changed (the server redeploys automatically).

### 2.39 — style peint — 2026-11-20
- Common painted style for every 3D model (towers, monsters, portal, castle): toon shading in 4 steps, a cold rim light on the edges and a thin dark outline of constant on-screen width, so silhouettes stand out from the snow on a phone. Applied when models load: no model regenerated. Add `?style=0` to the address to get the previous look. Costs about 1.7× more draw calls (to check on a low-end phone). Rendering only: `sim.js` unchanged.

### 2.38 — quêtes bonus — 2026-11-19
- Bonus quests: short challenges drawn at random during the game (first at 1:30, then one every 3 to 4 min), with funny titles. Races (the first to reach the goal wins): "Clicker fou" (place 10 more towers; never drawn when someone has no room left), "Le facteur sonne toujours 4 fois" (be the first to get 4 of your own monsters through to an opponent; every monster now remembers who sent it), "Gonflette" (upgrade a tower to a level above the best current one), "Frozen" (own N frost towers, N above the current best), "Le gros cadeau" (send a boss). Snapshots (best score when time runs out): "Qui a la plus grosse ?" (longest maze), "Picsou" (most gold in the bank), "Pigeons voyageurs" (most gold sent as flyers), "Bling-bling" (most expensive tower), "Mamie Gâteau" (lowest income: a catch-up gift). No race can already be won when it starts. Reward: gold, 8 × the average income (at least 100), shared on a tie.
- Banner when a quest starts (title, rule, reward), a tracking pill under the top bar (time left, your score and rank, green when you lead; tap it for the rule), and a banner announcing the winner. "Quêtes" column in the end-of-game table.
- AI: each AI decides whether it plays a quest (50 % in Normal, 75 % in Hard, 100 % in Brutal) and adapts: builds cheap towers, saves its gold, sends small waves early, upgrades its best tower, builds frost towers or sends a boss.
- `sim.js` and `server/` changed (the server redeploys automatically; the snapshot carries the current quest).

### 2.37 — file d'améliorations — 2026-11-19
- "Mes tours" panel: a button under the top bar lists all your towers by type (count per level). Tick types, pick a target level (2 to 5) and add them to an upgrade queue: each tower goes up one level at a time, lowest level first, as soon as gold allows; when gold runs short the queue spends what it can and the rest waits for income. The queue shows each order (progress bar, gold left) and can be cancelled order by order or entirely; queued towers get a gold chevron on the map. Interface only: `sim.js` unchanged.

### 2.36 — cristal hivernal renforcé — 2026-11-19
- The reinforced frost tower (slot 8: Cristal hivernal and its equivalents in every faction) cost more than the basic frost tower but did exactly the same thing. It now deals more damage (modifier ×0.9 → ×1.5, Cristal hivernal 2 → 3.4) and slows 10 points more at every level (−30 % to −60 % instead of −20 % to −50 %). It still does not stack with the basic frost tower: the strongest slow wins. `sim.js` changed (server redeployed automatically).
- Tooling: the maze-generation timing test now runs on its own, after the other tests (`labyrinthe-duree`). Since the parallel tests of 2.35 it shared the CPU with the AI games and failed at random on GitHub. Same thresholds. No game change.
- Tooling fix: the browser test of the rotation arrows failed every time. The swipe used by the test before it sent all its touch events at the same instant, so Chromium saw a very fast fling and, as on a real touch screen, swallowed the next tap (used to stop the fling): the arrow got pointerdown and pointerup but no click. The test swipe (`glisser` in `tests/outils/navigateur.js`) now lasts 0.3 s and holds still 0.2 s before lifting the finger. The test was not disabled. No game change.

### 2.35 — terrain dégagé — 2026-11-19
- Flying monsters are half the size of the other monsters in 3D (×0.5 instead of ×0.65), so they hide less of the field. No rule change.
- Less cluttered mobile display: the details line of the info panel fits on one line (tap it to unfold), and in 3D, when the chosen tower (or batch, or build preview) is hidden by the info panel or the top bar, the view glides just enough to show it above the panel. Interface only.
- Tooling: faster tests. `node tests/tout.js` runs the test files in parallel (one process per file, one per CPU core minus one; `--un-par-un` for the old behaviour) and the AI games run at the same time in worker threads, with identical results. On 22 cores: simulation 24 s → 8 s (13 s pinned to 4 cores, like GitHub), `--complet` 1 min 54 → 29 s. No game change.

### 2.34 — consigne de construction — 2026-11-19
- The "Touche encore la case pour construire" hint now sits between the two rotation arrows and appears only once per game (first build preview); the info card no longer repeats it afterwards. Interface only: `sim.js` unchanged.

### 2.33 — ia plus stratège — 2026-11-19
- AI builds more towers and upgrades less while its maze is unfinished (random upgrades from 12 towers at 25 %, 50 % from 28, instead of 10 towers at 35 %, 60 % from 24). Arena: +0.18 and +0.27 on two seed sets, neutral in long games. Other tweaks tried and dropped (earlier tiers and bosses, sending thresholds, a 20,000-gold wave cap, defence share, estimate caution, more upgrades).
- AI performance: the defence estimate follows the path cell by cell and caches what each tower sees. The AI costs 0.02–0.04 ms per game step on average (0.01–0.03 on `main`); its slowest call drops from 7–10 ms to 3–5 ms (2–3 ms on `main`).
- AI tower types chosen against the threat it receives: the AI remembers the monsters sent to it and, on the ordinary slots of its maze, builds the type that deals the most damage per gold against them (armour, flying, anti-magic, area, path in range): fewer archers and more guards, cannons and mages against bosses and armoured monsters. Arena: +0.52 points per seat (28 wins out of 42).
- Tooling: `--vies` option for the AI arena (long games that reach the end game). Two end-game ideas were tried with it and dropped because they made the AI weaker: rebuilding a level-5 tower as a stronger type, and capping the defence savings. No game change.
- AI waves aimed at what each opponent cannot absorb: for every monster family the AI estimates how many would get through each opponent's towers (damage while crossing, with armour, flying, anti-magic, invisibility and slows) and sends the family that costs them the most lives, with some randomness (more in Normal than in Brutal); otherwise ground monsters for income. Bosses and armoured monsters, very hard to absorb, come much more often. **The AI becomes much more dangerous: difficulty to be checked by playing.**
- AI end game: once its maze is complete and every tower is at level 5, the AI moves its defence savings (which could no longer be spent) into attacks. Arena: +0.76 points per seat against the previous step (35 wins out of 42).
- AI mazes where every tower shoots: the AI now builds its maze in an order that keeps each new tower next to the current monster path ("exposure": path cells seen by each tower), instead of only maximising the path length. Around 15–25 towers, towers far from the path drop from 3–4 to 1–2 on average, and each tower sees 10–50 % more path. In the AI arena it beats the previous AI by +0.64 points per seat (29 wins out of 42 games). `sim.js` changed (automatic server redeploy).
- Tooling: AI arena (`node tests/outils/arene-ia.js`): the current AI plays against the AI of another version (`origin/main` by default) in the same game engine, seats and factions swapped, on all CPU cores; reports points, wins and the gap with its standard error. Not part of the GitHub checks. No game change.

### 2.32 — correctifs de la feuille de route — 2026-11-19
- Mouse scrolling of the tower and monster card bar on PC: the wheel scrolls it horizontally and it can be dragged; the scroll position is kept when a card is chosen.
- Less clutter on mobile: the "Touchez encore la case" bubble in the middle of the board is gone; while previewing a build, the info card shrinks and shows the instruction instead.
- Flying monsters are drawn smaller in 3D (×0.65).
- Batch upgrade: tapping a tower twice selects up to 10 towers of the same type and level (gold frames on the board, a row of icons in the card); one button upgrades them all; when gold is short, the icons of the towers that won't be upgraded shrink.
- Roadmap updated (these four items are done). Interface only: `sim.js` unchanged (no server redeploy).

### 2.31 — équilibrage des tours — 2026-11-19
- Roadmap: the designer's ideas added to the roadmap table (3D model refactoring, multi-screen launch menu, unique gameplay per race, English version, analytics, website with SEO and GEO, launch tutorial, Google login or account, store, promotion campaigns, payment, then monetization). No game change.
- Roadmap: five new ideas (AI mazes where every tower can shoot, cluttered mobile display, batch upgrades, more compact flying units, waypoint for monsters). No game change.
- Tooling: the tower test bench now runs on all CPU cores with identical results (a comparison with `main` takes about 3 min instead of 20–25). It stays out of the GitHub checks.
- Frost towers deal 2 base damage instead of 4 (half as strong); their slow is unchanged, since it is what makes them strong.
- Mages deal 55 base damage instead of 45 (+22 %): they were the weakest value tower. Archers (8) and cannons (20) keep their damage. Flame towers still hit everything in their cone (a 4 then 8 target cap was tried, but since monsters spread out in 2.25 it barely mattered). `sim.js` changed (automatic server redeploy).
- Tooling: tower test bench (`node tests/outils/banc-tours.js`) measuring each tower's damage per gold invested, levels 1 to 5, against 7 typical waves, with before/after comparison. No gameplay change.

### 2.30 — départ façon course — 2026-11-19
- Starting gold is doubled: 200 instead of 100 for every board.
- The first 30 seconds are a "Build!" phase: nobody (human or AI) can send monsters; the monster tabs are disabled and a countdown runs in the top bar.
- Racing-style start: an animated "Construis !" banner with a logo and a big 30-second timer, a 3-2-1 countdown, then an animated "Envoie et résiste !" banner with its own logo.
- `sim.js` is modified (automatic server redeploy).
- Reproducible snowflakes: in 3D, each falling snowflake's position is now computed from the time instead of moving a little at each drawn frame. Same motion on screen, but two captures at the same instant are identical: the visual comparison witness drops from 0.1% to 0.00%, so the 3D comparison is reliable again. Only `rendu3d.js` changes.

### 2.29 — bibliothèque elevenlabs — 2026-11-19
- The whole sound library is remade with ElevenLabs (paid plan, commercial use): 371 files. Realistic, medieval, never shrill tower shots; monster deaths and growls while walking; a war horn when sending a wave, different for ground, flying, special and boss monsters; new interface sounds and ambiences.
- 100 sarcastic dark-fantasy voice lines, with new contexts: placing a tower, maximum level and wave cleared. New voices made for the Horde (deeper, more bestial) and the Dwarves.
- `sim.js` is unchanged (no server redeploy).
- Tooling: lighter 3D tests. When a test fast-forwards the game in 3D, the view is now redrawn 4 times per second of game time instead of 60 (the game itself still advances frame by frame). The software-rendered test browser used to crash around 30 s of play since the 2.26 landscape, although the game runs fine on phones. 3D run in about 1 min instead of 5, 3D screenshots in 1.5 min instead of 10. New `WR_GPU=1` option to run the 3D tests on the machine's real graphics card (about 20 s). No game change.
- Tooling: tests in 3D. The automated mobile walkthrough now runs in the real game (3D view): the former 2D and 3D walkthroughs are merged (26 checks), plus a test that the 2D fallback still works when 3D cannot load. Screenshots and the visual report are taken in 3D. Fixed along the way: the « before » version was extracted without three.js, models or sounds; three.js drew from the same seeded random numbers as the simulation, so the game differed between runs; the clock alignment was sometimes skipped in 3D. Known limit: falling snowflakes leave about 0.1% of changed pixels between two identical captures. No game change.

### 2.28 — mini-cartes d'hiver — 2026-11-19
- The opponents panel (« Adversaires ») gets winter mini-maps: snow and grid like the 3D view, the monsters' path as a navy dotted line, the portal and a small castle with the player's flag. Towers are small tiles in the colour of their role (green archer, red guard, blue frost, copper cannon, orange flames, purple mage), so you can read an opponent's defence at a glance; monsters are outlined (red on the ground, white in the air). Slightly bigger mini-maps with a silver frame; lives with a heart and income with the gold coin.
- Interface only (`sim.js` untouched, no server redeploy).

### 2.27 — sons dark fantasy — 2026-11-18
- Darker, more warlike sound effects: monster death cries and boss arrivals move from cartoon to dark fantasy; tower shots, explosions and sabotage are punchier. 45 prompts rewritten, 124 files regenerated locally. Voices, music and interface sounds are unchanged.

### 2.26 — terrain immersif — 2026-11-18
- More immersive 3D terrain: a less distorted camera (34° field of view instead of 48°), 20% closer, and you can no longer pan far away from the board. The board is now part of a continuous winter landscape, told apart only by its grid: relief around it (the board itself stays flat), patches of grass and melted snow, snow grain, a forest of tall snowy pines, rocks, a gradient sky, distant mountains and haze.
- 3D renderer only: `sim.js` is unchanged (no server redeploy).

### 2.25 — 2026-11-18
- Organisation: **roadmap** at the top of this README (improvement ideas with a status) and an “Idée d'amélioration” issue form to propose new ones. No need to run the simulation tests when a change cannot affect gameplay (docs, project rules). No game change.
- Ground monsters now move diagonally and at any angle: they take the shortest straight-line route (e.g. corner to corner along the diagonal) instead of only horizontal and vertical steps, without cutting through tower corners. They keep a small clearance from towers.
- Monsters no longer pile up: nearby monsters push each other sideways only, never slowing anyone down, so they spread out without creating traffic jams.
- The AI plans its mazes with the same rules (8 directions, no corner cutting), so its walls are judged by the path monsters really take; diagonal walls (towers touching by a corner) now count.
- The dotted path shows this new route, in 2D and 3D. A tower can no longer be placed right next to a ground monster; a tower placed in front of one makes it change its route.
- `sim.js` changed (automatic server redeploy).
- Organisation: every version now gets a very short title (2 to 4 words, e.g. “exploration fin de partie” for 2.23), reused in the commit, the PR, the CLAUDE.md log and this changelog. No game change.

### 2.24 — 2026-11-18
- On a computer, **Shift + click** on a tile builds the selected tower in a single click (no preview step). The tower stays selected, so you can chain builds. Touch screens keep the two-tap build.
- Interface only (`sim.js` untouched, no server redeploy).

### 2.23 — 2026-11-18
- End of game (solo): a window shows Victory/Defeat with stats for the 4 players (rank, towers, maze length, waves sent, monsters killed, final income), an income curve over the game and a personal summary.
- “Regarder la carte” lets you walk around the frozen mazes (drag, rotate, switch board, tap a tower to see it); “Quitter” goes back to the replay screen. Tap a player in the table to look at their maze.
- `sim.js`: stat counters per board (`Board.st`), no effect on gameplay (server redeploys automatically).

### 2.22 — 2026-11-18
- The 3D view is now the only view offered: the "Jouer en vue 2D (classique)" link is gone from the home screen. The 2D renderer stays as a fallback when WebGL is missing and for the tests (`?rendu=2d` still works).
- Interface only (`sim.js` untouched, no server redeploy).

### 2.21 — 2026-11-18
- The monster tier row now sits above the tabs, so the tabs and cards stay in place when switching between towers and monsters. Interface only: `sim.js` is unchanged.

### 2.20 — 2026-11-18
- Frost towers and Sylvan roots now scale with the tower level. Frost: −20 % speed at level 1 up to −50 % at level 5 (was −50 % to −70 %), lasting 1.5 s to 2.7 s, with a blast radius growing from 1.2 to 2 tiles. Roots: −10 % at level 1 up to −30 % at level 5, lasting 0.72 s to 1.3 s.
- Cold and roots now add up (frost −50 % + roots −30 % = −80 %); two effects of the same kind do not stack (the strongest and longest wins).
- The tower card shows the slow, duration and zone, and what the next level brings. `sim.js` changed (automatic server redeploy).

### 2.19 — 2026-11-18
- Clearer icons: tower role and target badges are now round, ringed in the role colour (the gold square that dulled the colours is gone); the wing glyph was redrawn as a real feathered wing.
- Monster tabs show icons instead of words: paw (ground), wing (flying), star (special).
- Monster cards show again the income gained per send, in a green “+N” badge. Interface only: `sim.js` is unchanged.

### 2.18 — 2026-11-18
- Frost skin on the tactical-view interface: the 2.12 frosted textures and silver scrollwork frames are back, laid out like a strategy-game console (a frosted resource bar across the top, a frosted console at the bottom, both edged with a silver frieze set with ice gems). Square framed cards (silver, gold when selected, red for monsters) with the price in a medallion; framed tabs, info card, opponents panel and menu; round metal buttons ringed with gold.
- Interface only: `sim.js` is unchanged (no server redeploy).

### 2.17 — 2026-11-18
- Sound library: about 230 MP3 files generated locally for free (Stable Audio Open for sound effects, Chatterbox for voices, both usable commercially): tower shots per faction, construction, deaths of all 72 monsters, boss arrivals, interface, winter and battle ambiences, and 55 comic voice lines (11 per faction) in the designer's recorded voices.
- New `audio.js` engine (preloading, variants, priorities, one voice at a time); the synthesized sounds remain as a fallback, and `?son=synth` brings them back.
- Generation scripts in `art/sons/`, quality check `art/outils/controle-sons.js`, listening page `ecoute-sons.html`. `sim.js` is unchanged (no server redeploy).

### 2.16 — 2026-11-17
- Background music: three themes composed by the designer with Suno (`assets/musique/`). A random one starts at launch, then they play one after another in a loop for the whole game. A « Musique » toggle in the menu turns it off without muting the sound effects.
- Interface only: `sim.js` is unchanged (no server redeploy).

### 2.15 — 2026-11-17
- New "tactical view" interface, from the mockup approved by the designer: the board fills the screen, with the top bar and the bottom dock floating over it. In 3D, a perspective camera at a fixed height: drag a finger to move the map (like a maps app, with momentum), two arrows rotate the view by 45°. No more pinch zoom or "Vue d'ensemble".
- Portrait only: a phone held in landscape shows "Tourne ton téléphone".
- Top bar: menu (sound, vibrations, gestures reminder, quit), gold, income with a 10-second ring, lives, clock, fullscreen. "Adversaires" button opens the four board thumbnails; you can send monsters while watching an opponent's board.
- One info card, shown only when something is selected (tower to build, placed tower with Upgrade and Sell, monster). Cards show only the icon and price. Building: pick a card, then tap a square twice. Sending: the first tap selects the monster, each following tap sends a group (no auto-repeat, on purpose), with a bounce, a vibration and a ×2, ×3 counter.
- Interface only: `sim.js` is unchanged (no server redeploy).

### 2.14 — 2026-11-15
- Balance: every monster cost is a multiple of 10, and ground-monster income is rounded down onto the curve 10 gold → +1, 100 → +11, 1000 → +120, so no cheap monster pays better than the curve. The Snow rat now costs 20 gold for +2 (was 15 for +2). Tier-1 ground monsters now go from 10 to 120 gold in steps of 10.

### 2.13 — 2026-11-15
- Monster tiers: 3 tiers of 24 monsters (12 ground, 3 flying, 8 magic, 1 boss), 72 monsters instead of 17. Tier 1 is open from the start; tier 2 costs 300 gold and tier 3 costs 1,500 gold. Time unlocks are gone.
- New "accelerated" ability (speeds up the longer it lives); three splitting monsters; one boss per tier.
- The AI opens tiers and sends the strongest monster it can afford in each family.
- Send tab: tier badges to pick or open a tier. `sim.js` and `server/` changed (automatic server redeploy).

### 2.12 (assets) — 2026-11-15
- 3D assets: monster models for the upcoming tier system (3 tiers × 24 monsters, list in `art/monstres/PALIERS.md`). Not used by the game yet. No game change.
### 2.12 — 2026-11-15
- Bigger board: in 3D the camera tilt adapts to the screen shape; in landscape, three columns (top bar and info on the left, board in the middle, tabs and buttons on the right). The "Vue d'ensemble" button now sits on the board.
- "Elven frost" look inspired by strategy-game command bars: ornate screen frame with elven scrolls and frost, frosted night-glass panels with silver frames, framed cards with price medallions (all SVG and CSS).
- In 3D, tower and monster icons are renders of their 3D models.
- Interface only: `sim.js` untouched, no server redeploy.

### 2.11 — 2026-11-14
- Tooling: the AI maze "chunked generation" test no longer fails at random on GitHub (it now checks the number of chunks, with wider time margins). No game change.
- New video-game look for the interface (winter heroic fantasy): redesigned start menu (winter night, mountains, falling snow, emblem, golden title, short description and illustrated rules, faction crests, raised difficulty buttons); in game, night-blue panels with gold trim, raised buttons, framed cards, golden board frame.
- More room for the board: the button to view other players' boards is back in the top bar; the top bar, tabs and info panel are more compact, with the same information.
- Interface only: `sim.js` untouched, no server redeploy.

### 2.9 (rollback) — 2026-11-14
- Back to version 2.9 at the designer's request: version 2.10 (five new faction identities) is reverted and paused. Its work stays in the history (tag `v2.10`).

### 2.9 — 2026-11-14
- Stronger "Winter Realms" theme in the 3D view: snowy board (snow checkerboard lightly tinted by the faction, frosted rock edges), winter scenery (snowy pines, snow-capped rocks, snowdrifts, ice crystals), falling snowflakes and cold winter lighting. The path and range rings turn night blue to stay readable on snow.
- Snow on every tower, the spawn portal and the castle: snow caps on battlements, bases and platforms, snowy roof tops while the faction colours stay visible below. All 3D assets were regenerated.
- The 2D view is unchanged. Game rules unchanged (`sim.js` untouched, no server redeploy).
- Tooling fix: Blender's Python module used in the cloud and on GitHub cannot apply meshopt compression, so cloud-generated models were 2–3× too heavy and wrongly failed the "Assets 3D" check. `art/outils/generer.py` now compresses them with gltf-transform when Blender did not.

### 2.8 — 2026-11-14
- The 3D view is now the default: the normal game address opens it. The classic 2D view stays available with `?rendu=2d`, or the "Jouer en vue 2D (classique)" link on the home screen.
- Game rules unchanged (`sim.js` untouched, no server redeploy).

### 2.7 — 2026-11-14
- Playable 3D view (prototype): add `?rendu=3d` to the address, or tap "Essayer la vue 3D (prototype)" on the home screen. Diorama board, animated towers and monsters, scaffolding while towers are built, projectiles and effects, same controls as 2D (two-tap building with a ghost tower, two-finger zoom and pan, tower panel).
- 3D models for the whole game, one Blender script per asset in `art/`: all 50 towers (5 factions × 10, heroic-fantasy cartoon style, one look per faction), 17 animated monsters (sizes follow their in-game size), spawn portal and castle. `generer.py` now also exports pivots and animations and compresses with meshopt.
- three.js r170 is vendored in `vendor/three/` (MIT), loaded through an import map only in 3D mode; no build step. Model viewer page: `apercu-3d.html`.
- The 2D view stays the default and is unchanged. Game rules unchanged (`sim.js` untouched, no server redeploy).

### 2.6 — 2026-11-14
- AI mazes pay off earlier: each candidate maze is graded on its path length after 15, 25, 40 and 60 towers, not only when finished. With 40 towers, the median path goes from 57 to 66 cells.
- Useless walls (not touching the path and not making it longer) are removed from AI plans, so the gold goes to towers that matter.

### 2.5.1 — 2026-11-14
- Fixes multiplayer: after 2–3 minutes (as soon as a ground monster reached your board), tapping the board crashed the page, the board froze and towers could no longer be built. Monsters received from the server now carry an approximate target cell. Client-only fix (no server redeploy).

### 2.5 — 2026-11-14
- Smarter AI mazes: at the start of each game, every AI draws its own target maze (serpentines, vertical combs or organic labyrinths, refined by a local search), so each AI board looks different and the monster path grows with almost every tower (about 100 cells when complete, against 16 for a straight line).
- The AI builds its maze in an order that keeps the path long at every stage, starting near the centre to hit both the straight path and the flyers early on.
- Frost towers are spread evenly along the maze. Mages are placed to detect Spectres along the whole path, only once an opponent can afford to send them. Anti-air towers sit on the flyers' line, more of them when flyers arrive.
- Fixes a bug where the AI stopped building after about 36 towers.
- Tooling: faster tests. By default only one AI-vs-AI game per difficulty (the 15 full games run with `node tests/tout.js --complet`); the GitHub check drops from 9 min to about 1.5 min.
- Tooling: no more frozen engine copies or recorded reference games (the frozen 2.4 engine is removed too). Tests check that the game works, and the gameplay report compares directly with `main`.

### 2.4 — 2026-11-14
- Towers now take time to build: 1 second per 50 gold spent, between 0.5 and 8 seconds (on Normal, an Archer takes 0.5 s, a Mage 1.7 s, an Archmage 2.6 s). Upgrades work the same way, based on the upgrade price.
- Difficulty slows human builders: ×1 on Normal, ×1.25 on Difficile, ×1.5 on Brutal. AIs always build at ×1.
- While building or upgrading, a tower does not shoot, does not reveal Spectres and cannot be upgraded again. It still blocks the path and can be sold (70 %).
- A building tower is drawn faded, with scaffolding, a hammer and a gold progress bar. The info panel shows the build time and the countdown.

### Tooling — 2026-11-14 (3D assets)
- Groundwork for 3D: one Blender Python script per asset in `art/`, generated identically on a PC (Blender 5.3) or in the cloud (`bpy==5.3.0`) by `art/outils/generer.py`; GLB files and a manifest in `assets/3d/`; size/triangle budgets; a consistency test on every pull request and an "Assets 3D" GitHub Action that regenerates everything and attaches preview images. See `art/LISEZMOI.md` (French).
- `.gitattributes` enforces LF line endings (needed on Windows) and marks 3D/image files as binary.
- No game change.

### 2.3 — 2026-11-14
- Bigger board on phones: the four player thumbnails leave the top bar and open in a floating panel over the board, from a map icon in the top-left corner. Tap a thumbnail to watch that board; tap the banner to come back.
- Your lives now show in the top bar (❤).
- Tower cards get role badges in bevelled gold frames (arrow, sword, snowflake, bomb, flame, star), a target badge (ground only / ground and air) and a magic marker, all drawn in code. Card text now reads "⚔ 15 dégâts/s" and "◎ portée 3,1".
- Long-press a tower card (or hover with the mouse) to preview its info panel without selecting it.
- Interface only (`sim.js` untouched, no server redeploy).

### 2.2 — 2026-11-14
- Building a tower now takes two taps: the first tap shows a preview (ghost tower, range, price), the second tap on the same tile builds it. Invalid tiles are reported on the first tap. Dragging a finger no longer builds towers.
- Game rules unchanged (`sim.js` untouched).

### 2.1 — 2026-11-14
- Clearer interface: an info panel describes the selected tower in plain French (damage per second, range, ground/air targets, effects, faction bonus, next-level gain); tower cards show damage/s, range and anti-air; prices turn red when gold is short; locked monsters show when they unlock.
- Two-finger pinch zoom (1× to 3×) and pan on the board, mouse-wheel zoom, "Vue d'ensemble" reset button. Touch placement now happens on release so a two-finger gesture never builds a tower.
- Landscape layout fixed on phones (the top of the screen and the bottom of the board were cut off).
- Game rules unchanged (`sim.js` untouched, no server redeploy).

### Tooling — 2026-11-14
- The multiplayer server now redeploys automatically (GitHub Action) when `sim.js` or `server/` changes on `main`. No game changes.
- Automated tests in `tests/`: game mechanics, 15 seeded AI-vs-AI games replayed exactly against a frozen copy of the 1.7 engine, mobile browser journey (portrait and landscape).
- Phone screenshots, before/after visual comparison, three separate reports (technical, gameplay, visual), simulation tests on every pull request (GitHub Actions).
- No change to `sim.js` or `index.html`: the game is unchanged.
- Fix: the server deploy Action now uses Node 22 (Wrangler 4 refuses Node 20), so the automatic deploy no longer fails.
- Versioning: every merge into `main` is tagged automatically (`vX.Y.Z`, or `vX.Y.Z.N` when the game version does not change) with a GitHub Release; past versions 1.4 to 2.0.1 are tagged too. Any version can be restored (CLAUDE.md §14).

### Workflow — 2026-11-14
- New branch rule (see CLAUDE.md): no direct commits to `main`. One branch per change (`<type>/<topic>`), then a pull request that the author merges after a quick test (no review required). No game changes.

### 2.0.1 — 2026-11-14
- Online play is restricted to France (the server checks the player's country). Players elsewhere get a clear message; solo play still works everywhere.

### 2.0 — 2026-11-14
- Online multiplayer: 2–4 players in a room (AIs fill free seats), invite link or code, room leader picks AI difficulty, spectators, reconnection.
- Game server on Cloudflare Workers + Durable Objects (free plan).

### 1.7 — 2026-11-14
- Technical: the game simulation moved to `sim.js` (shared with the upcoming multiplayer server). Solo play is unchanged.

### 1.6.1 — 2026-11-14
- Fix Sylvestres roots: all their towers now slow enemies to ×0.82 speed for 0.72 s (Frost towers keep their stronger slow). The strongest active slow wins.
- Fixes ground monsters freezing and flying monsters getting stuck forever (unkillable) when hit by Sylvestres melee or flame towers.

### 1.6 — 2026-11-14
- Visual only: each board is now a diorama (thick base, raised tiles) with a per-faction biome palette.
- Deterministic scenery (rocks, grass, crystals), no flickering; shadows under the spawn portal and the castle.
- Reworded welcome text. No rule or balance changes.

### 1.4 — 2026-11-14
- Initial import of the project: 5 factions × 10 towers, 17 monsters, 3 AI opponents, 3 difficulty levels.
