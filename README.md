# Winter Realms — Tower Wars

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

- `node tests/tout.js --simulation`: simulation tests only (what GitHub runs on every pull request).
- `node tests/bilan.js`: the three reports (technical, gameplay, visual) in `rapports/bilan.html`, including a before/after visual comparison with `main`.
- `node tests/captures.js`: phone screenshots (portrait and landscape) in `captures/actuel/`.

Details (in French): CLAUDE.md, sections 12 and 13.

## Play together

On the site, enter a nickname, click **Créer un salon** and share the link (or the 4-letter code). Friends click the link (or type the code and **Rejoindre**), pick a faction, and the room leader clicks **Lancer la partie**. Empty seats are played by AIs.

The multiplayer server runs on Cloudflare Workers (free plan), in [`server/`](server/). It is **redeployed automatically** by a GitHub Action whenever a change to `sim.js` or `server/` is merged into `main` (see CLAUDE.md, section 9 bis). Manual fallback: `cd server` then `npx wrangler deploy`.

## Changelog

### 2.26 — équilibrage des tours — 2026-11-18
- Frost towers deal 2 base damage instead of 4 (half as strong); their slow is unchanged, since it is what makes them strong.
- Archers deal 6 base damage instead of 8 (−25 %): cheap to upgrade, they had become the best value tower everywhere; their price is unchanged so mazes stay cheap. Mages deal 55 instead of 45 (+22 %): they were the weakest value tower.
- Tooling: tower test bench (`node tests/outils/banc-tours.js`) measuring each tower's damage per gold invested, levels 1 to 5, against 7 typical waves, with before/after comparison. No gameplay change.
- Area towers rebalanced, measured with the tower test bench. Flame towers now hit at most 8 monsters per burst (those closest to the exit) instead of everything in their cone: against a crowd of 40 monsters, a level-5 flame tower was worth about 5 times a normal tower per gold. Cannons deal 12 base damage instead of 20 (−40 %): their blast still hits everything around (that is the point of the tower), but their overall value is back in line with the other towers. `sim.js` changed (automatic server redeploy).

### 2.25 — 2026-11-18
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
