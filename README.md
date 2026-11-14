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

### 2.4 — 2026-11-14
- Towers now take time to build: 1 second per 30 gold spent, between 1 and 12 seconds (an Archer takes 1 s, a Mage about 3 s, an Archmage about 4.5 s). Upgrades work the same way, based on the upgrade price.
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
