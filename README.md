# Winter Realms — Tower Wars

A browser tower-defense game in a single HTML file.

## Play

Online: **https://pompidou-all-stars.github.io/winter-realms/** (updated automatically on every push to `main`).

Offline: open `index.html` in a browser.

## Contributing

The project is hosted by the [pompidou-all-stars](https://github.com/pompidou-all-stars) organization. Get a copy with:

```bash
git clone https://github.com/pompidou-all-stars/winter-realms.git
```

1. `git pull` before you start.
2. Make your changes, then `git add -A` and `git commit -m "what you changed"`.
3. `git push`.

Game rules, balance tables and project conventions are documented (in French) in [CLAUDE.md](CLAUDE.md). Every change must update CLAUDE.md and the changelog below.

## Play together

On the site, enter a nickname, click **Créer un salon** and share the link (or the 4-letter code). Friends click the link (or type the code and **Rejoindre**), pick a faction, and the room leader clicks **Lancer la partie**. Empty seats are played by AIs.

The multiplayer server runs on Cloudflare Workers (free plan), in [`server/`](server/). It is **redeployed automatically** by a GitHub Action whenever a change to `sim.js` or `server/` is merged into `main` (see CLAUDE.md, section 9 bis). Manual fallback: `cd server` then `npx wrangler deploy`.

## Changelog

### Tooling — 2026-11-14
- The multiplayer server now redeploys automatically (GitHub Action) when `sim.js` or `server/` changes on `main`. No game changes.

### Workflow — 2026-11-14
- New branch rule (see CLAUDE.md): no direct commits to `main`. One branch per change (`<type>/<topic>`), then a pull request reviewed by another member before merging. No game changes.

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
