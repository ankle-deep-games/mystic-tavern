# Ankle Deep Games: Mystic Tavern

A bare-bones, start-to-finish proof of concept for a simultaneous four-player cooperative browser RPG.

This is the tracer-bullet successor to the original Django prototype. It keeps the character art, tone, party roles, branching decisions, HP/MP combat, and cooperative structure while replacing page requests and two-second polling with one authoritative realtime game room.

## The ten-minute vertical slice

1. One player creates a party and shares the room code.
2. Four players join as guests from separate browsers or devices.
3. Each player claims one unique role: Paladin, Black Mage, White Mage, or Archer.
4. The party follows a short shared introduction in Lantern Alley.
5. Everyone chooses and locks a combat action simultaneously.
6. The server resolves the round by character speed, then executes enemy attacks.
7. After defeating the two alley thugs, everyone votes to rest or rotate the watch.
8. The winning choice changes both recovery and the composition of the final encounter.
9. The party fights the Arachnid Sovereign.
10. The run ends with a shared victory or defeat summary and can be reset by the party leader.

There are deliberately no accounts, game browser, inventory, equipment progression, campaign save, content management system, matchmaking queue, microservices, or database.

## Architecture

```text
React browser client                 Node.js server
┌────────────────────┐              ┌───────────────────────────┐
│ Existing game art  │              │ Colyseus party room       │
│ Lobby and story UI │  WebSocket   │ - exactly four seats      │
│ Action selection   │◄────────────►│ - validates every command │
│ State rendering    │              │ - owns all game state     │
└────────────────────┘              │ - performs random rolls   │
                                    │ - resolves combat rounds  │
                                    └─────────────┬─────────────┘
                                                  │
                                    ┌─────────────▼─────────────┐
                                    │ Pure TypeScript game core │
                                    │ Content, rules, tests      │
                                    └───────────────────────────┘
```

The client never sends damage values, state patches, phase transitions, or random results. It sends commands such as `choose-character`, `cast-vote`, and `combat-action`. The server validates the command, changes its private game state, and broadcasts a fresh snapshot to the party.

Each party is one in-memory Colyseus room. Temporary disconnects receive a thirty-second reconnection window. Matches intentionally do not survive a server restart; persistence is a follow-up decision, not tracer-bullet infrastructure.

## Project layout

```text
apps/
  web/                 React 19, Vite, responsive game UI, retained artwork
  server/              Node.js, Colyseus, WebSocket room, command validation
packages/
  game-core/           Framework-free game state, rules, content, unit tests
e2e/                   Four independent browser contexts completing one run
```

## Run locally

Requirements:

- Node.js 24 or newer
- pnpm 10.12.1 (Corepack can provide it)

```bash
corepack enable
pnpm install
pnpm dev
```

Open `http://127.0.0.1:5173`. Create a party in one browser, then use three private windows or other browsers to join with the displayed code.

The Vite client runs on port `5173` during development. The Colyseus HTTP and WebSocket server runs on port `2567`.

## Verification

```bash
pnpm typecheck
pnpm test
pnpm build
pnpm exec playwright install chromium
pnpm test:e2e
```

The end-to-end test creates four isolated browser contexts, joins all four players to the same room, assigns every role, advances shared dialogue, completes both battles, resolves the cooperative vote, and asserts the victory summary.

## Production container

The production server serves both the compiled React files and Colyseus from one process and one port:

```bash
docker build -t ankle-deep-games .
docker run --rm -p 2567:2567 ankle-deep-games
```

Then open `http://localhost:2567`.

Any production host must support long-lived WebSocket connections. Because active matches are in memory, run one server instance for this proof of concept. Horizontal scaling and durable match snapshots should be designed together if the game grows beyond the prototype.

## Game rules

- A room contains at most four players and cannot start until all four unique roles are ready.
- Every living player locks one action per round.
- A twenty-second deadline assigns a safe basic attack to players who have not acted, including disconnected players.
- Player actions resolve from highest speed to lowest speed, followed by living enemies.
- The Paladin can guard, the Black Mage can spend MP for burst damage, the White Mage can heal any living ally, and the Archer can damage the whole enemy line.
- `All rest` fully restores the party but gives the Sovereign time to gather a minion.
- `Rotate the watch` restores less health and mana but removes the minion from the final encounter.
- A tied vote follows the party leader's selection.

## What happened to Django?

The Django implementation was intentionally removed from the active feature branch instead of being incrementally converted. Its request handlers, templates, polling loops, database models, seed script, and deployment notes remain available in Git history on `main` before this rewrite.

An additional preservation branch, `archive/django-prototype-as-found-2024`, captures the two uncommitted lines that were present in the working tree when the rewrite began. The ignored local `db.sqlite3` was left untouched and was not committed because it contains local account and session data. All artwork used by this vertical slice was copied into `apps/web/public/assets` before the legacy tree was removed.

## Deliberate next decisions

Do not add these automatically. Validate the game first.

- Whether simultaneous planning is actually more fun than individual speed turns
- Whether the party vote should show selections before everyone locks
- Whether reconnecting players need durable sessions across server restarts
- Whether the battle presentation needs Phaser/PixiJS or should remain DOM-based
- Whether story content should move from TypeScript into Ink
- Whether accounts, matchmaking, progression, and saved campaigns are worth the operational cost
