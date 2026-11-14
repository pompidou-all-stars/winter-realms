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

### 2.11 — 2026-11-14
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
