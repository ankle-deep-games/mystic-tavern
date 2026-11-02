import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Client, type Room } from "@colyseus/sdk";
import {
  INTRO_LINES,
  ROLE_ORDER,
  ROLES,
  type AbilityDefinition,
  type ClientCommand,
  type GameState,
  type PlayerState,
  type RoleId
} from "@adg/game-core";

const TOKEN_KEY = "adg-reconnection-token";
const endpoint = import.meta.env.VITE_SERVER_URL
  ?? (window.location.port === "5173" ? "http://localhost:2567" : window.location.origin);

export function App() {
  const roomRef = useRef<Room | null>(null);
  const [game, setGame] = useState<GameState | null>(null);
  const [status, setStatus] = useState<"connecting" | "connected" | "disconnected">("disconnected");
  const [error, setError] = useState("");

  const attachRoom = useCallback((room: Room) => {
    roomRef.current = room;
    localStorage.setItem(TOKEN_KEY, room.reconnectionToken);
    setStatus("connected");
    room.onMessage("game-state", (next: GameState) => setGame(structuredClone(next)));
    room.onMessage("game-error", (payload: { message: string }) => {
      setError(payload.message);
      window.setTimeout(() => setError(""), 4200);
    });
    room.onDrop(() => setStatus("connecting"));
    room.onReconnect(() => {
      setStatus("connected");
      room.send("request-state");
    });
    room.onLeave(() => {
      setStatus("disconnected");
      setGame(null);
      roomRef.current = null;
    });
    room.send("request-state");
  }, []);

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return;
    let cancelled = false;
    setStatus("connecting");
    new Client(endpoint).reconnect(token).then((room) => {
      if (!cancelled) attachRoom(room);
    }).catch(() => {
      localStorage.removeItem(TOKEN_KEY);
      if (!cancelled) setStatus("disconnected");
    });
    return () => { cancelled = true; };
  }, [attachRoom]);

  async function connect(mode: "create" | "join", name: string, roomCode?: string) {
    setError("");
    setStatus("connecting");
    try {
      const client = new Client(endpoint);
      const room = mode === "create"
        ? await client.create("party", { name })
        : await client.joinById(roomCode!.trim(), { name });
      attachRoom(room);
    } catch (connectionError) {
      setStatus("disconnected");
      setError(connectionError instanceof Error ? connectionError.message : "Could not reach that party.");
    }
  }

  function send(command: ClientCommand) {
    roomRef.current?.send("command", command);
  }

  function leave() {
    localStorage.removeItem(TOKEN_KEY);
    roomRef.current?.leave();
    setGame(null);
    setStatus("disconnected");
  }

  const selfId = roomRef.current?.sessionId ?? "";

  return (
    <main className="app-shell">
      <Header game={game} status={status} onLeave={leave} />
      {error && <div className="toast" role="alert">{error}</div>}
      {!game ? (
        <Landing onConnect={connect} connecting={status === "connecting"} />
      ) : game.phase === "lobby" ? (
        <Lobby game={game} selfId={selfId} send={send} />
      ) : game.phase === "intro" ? (
        <Story game={game} selfId={selfId} send={send} />
      ) : game.phase === "party-choice" || game.phase === "choice-result" ? (
        <PartyChoice game={game} selfId={selfId} send={send} />
      ) : game.phase === "tutorial-battle" || game.phase === "final-battle" ? (
        <Battle game={game} selfId={selfId} send={send} />
      ) : (
        <Ending game={game} selfId={selfId} send={send} />
      )}
    </main>
  );
}

function Header({ game, status, onLeave }: { game: GameState | null; status: string; onLeave: () => void }) {
  return (
    <header className="topbar">
      <div className="brand-lockup">
        <img src="/assets/logo.png" alt="" />
        <div><span>Ankle Deep Games</span><strong>MYSTIC TAVERN</strong></div>
      </div>
      {game && (
        <div className="room-meta">
          <span className={`connection-dot ${status}`} />
          <span>Party code <button className="code" onClick={() => navigator.clipboard.writeText(game.roomId)}>{game.roomId}</button></span>
          <button className="text-button" onClick={onLeave}>Leave</button>
        </div>
      )}
    </header>
  );
}

function Landing({ onConnect, connecting }: { onConnect: (mode: "create" | "join", name: string, code?: string) => void; connecting: boolean }) {
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [joinError, setJoinError] = useState("");

  function handleJoin() {
    if (!name.trim()) {
      setJoinError("Please enter your traveler name.");
      return;
    }

    if (!code.trim()) {
      setJoinError("Please enter a party code.");
      return;
    }

    setJoinError("");
    onConnect("join", name.trim(), code.trim());
  }

  return (
    <section className="landing panel">
      <div className="landing-copy">
        <p className="eyebrow">A four-player cooperative RPG</p>
        <h1>One night.<br />Four strangers.<br /><em>No polling.</em></h1>
        <p>Choose a hero, decide together, and lock in each combat round at the same time. One party code gets everyone into the same living game.</p>
        <div className="feature-row"><span>4 players</span><span>10 minutes</span><span>1 shared fate</span></div>
      </div>
      <div className="join-card">
        <label htmlFor="traveler-name">Traveler name</label>
        <input id="traveler-name" autoFocus maxLength={18} value={name} onChange={(event) => setName(event.target.value)} placeholder="Dobby" />
        <button className="primary" disabled={connecting || !name.trim()} onClick={() => onConnect("create", name)}>
          {connecting ? "Opening the door…" : "Create a party"}
        </button>
        <div className="divider"><span>or join friends</span></div>
        <label htmlFor="party-code">Party code</label>
        <div className="join-row">
          <input
            id="party-code"
            value={code}
            maxLength={4}
            autoComplete="off"
            placeholder="ABCD"
            onChange={(event) =>
              setCode(event.target.value.toUpperCase().replace(/[^A-Z0-9]/g, ""))
            }
          />
          <button disabled={connecting} onClick={handleJoin}>Join</button>
        </div>
        {joinError && (
          <p className="join-error" role="alert">
            {joinError}
          </p>
        )}
      </div>
    </section>
  );
}

function Lobby({ game, selfId, send }: GameScreenProps) {
  const self = game.players[selfId];
  const players = Object.values(game.players);
  const isHost = game.hostId === selfId;
  const available = (roleId: RoleId) => !players.some((player) => player.id !== selfId && player.roleId === roleId);
  const canStart = players.length === 4 && players.every((player) => player.roleId && player.ready);
  return (
    <section className="game-page">
      <div className="section-heading">
        <div><p className="eyebrow">Party assembly</p><h1>Choose who answers the crystal.</h1></div>
        <span className="seat-count">{players.length} / 4 seats</span>
      </div>
      <div className="role-grid">
        {ROLE_ORDER.map((roleId) => {
          const role = ROLES[roleId];
          const selected = self?.roleId === roleId;
          const claimedBy = players.find((player) => player.id !== selfId && player.roleId === roleId);
          return (
            <button key={roleId} className={`role-card ${selected ? "selected" : ""}`} disabled={!available(roleId) || self?.ready} onClick={() => send({ type: "choose-character", roleId, portrait: self?.portrait ?? "female" })}>
              <img src={portraitPath(roleId, self?.portrait ?? "female")} alt={`${role.name} character`} />
              <div><span className="role-name">{role.name}</span><p>{role.tagline}</p><small>{role.maxHp} HP · {role.maxMp} MP · {role.speed} SPD</small></div>
              {claimedBy && <span className="claimed">Claimed by {claimedBy.name}</span>}
            </button>
          );
        })}
      </div>
      <div className="lobby-footer panel">
        <div className="party-seats">
          {[0, 1, 2, 3].map((index) => <Seat key={index} player={players[index]} hostId={game.hostId} />)}
        </div>
        <div className="ready-controls">
          {self?.roleId && (
            <div className="portrait-toggle" aria-label="Portrait selection">
              {(["female", "male"] as const).map((portrait) => (
                <button key={portrait} className={self.portrait === portrait ? "active" : ""} disabled={self.ready} onClick={() => send({ type: "choose-character", roleId: self.roleId!, portrait })}>{portrait === "female" ? "Portrait A" : "Portrait B"}</button>
              ))}
            </div>
          )}
          <button className="primary" disabled={!self?.roleId} onClick={() => send({ type: "set-ready", ready: !self?.ready })}>{self?.ready ? "Not ready" : "Ready up"}</button>
          {isHost && <button className="gold" disabled={!canStart} onClick={() => send({ type: "start-game" })}>{canStart ? "Begin the adventure" : "Waiting for four ready heroes"}</button>}
          {!isHost && <span className="hint">The party leader will begin when everyone is ready.</span>}
        </div>
      </div>
    </section>
  );
}

function Seat({ player, hostId }: { player: PlayerState | undefined; hostId: string | null }) {
  if (!player) return <div className="seat empty"><span>Open seat</span></div>;
  return <div className={`seat ${player.ready ? "ready" : ""}`}><span>{player.name}{player.id === hostId ? " ★" : ""}</span><small>{player.roleId ? ROLES[player.roleId].name : "Choosing…"} · {player.ready ? "Ready" : "Not ready"}</small></div>;
}

function Story({ game, selfId, send }: GameScreenProps) {
  const line = INTRO_LINES[Math.min(game.introIndex, INTRO_LINES.length - 1)]!;
  const isHost = game.hostId === selfId;
  return (
    <section className="story-stage">
      <img className="scene-background" src="/assets/setting-alley.png" alt="A rain-darkened fantasy alley" />
      <div className="story-party">{Object.values(game.players).map((player) => <MiniPortrait key={player.id} player={player} />)}</div>
      <div className="dialogue-box">
        <img src={line.speaker === "Old Man" ? "/assets/old-man.png" : line.speaker === "Drunk Man" ? "/assets/drunk-man-1.png" : "/assets/logo.png"} alt="" />
        <div><p className="eyebrow">{line.speaker}</p><p className="dialogue-line">{line.text}</p></div>
        {isHost ? <button className="gold" onClick={() => send({ type: "advance-story" })}>{game.introIndex === INTRO_LINES.length - 1 ? "Stand together" : "Continue"}</button> : <span className="hint">Following the party leader…</span>}
      </div>
    </section>
  );
}

function PartyChoice({ game, selfId, send }: GameScreenProps) {
  const resolved = game.phase === "choice-result";
  const voteCount = Object.keys(game.votes).length;
  const selfVote = game.votes[selfId];
  return (
    <section className="choice-page panel">
      <div className="choice-copy">
        <p className="eyebrow">The party decides</p>
        <h1>{resolved ? (game.resolvedChoice === "all-rest" ? "The party sleeps." : "The watch rotates.") : "How will you meet the night?"}</h1>
        <p>{resolved
          ? game.events.at(-1)?.message
          : "Every living hero votes. A tie follows the party leader; the consequence belongs to everyone."}</p>
      </div>
      {!resolved ? (
        <div className="choice-grid">
          <button className={selfVote === "all-rest" ? "selected" : ""} onClick={() => send({ type: "cast-vote", choiceId: "all-rest" })}><strong>All rest</strong><span>Fully restore HP and MP—but risk letting the brood gather.</span></button>
          <button className={selfVote === "rotate-watch" ? "selected" : ""} onClick={() => send({ type: "cast-vote", choiceId: "rotate-watch" })}><strong>Rotate the watch</strong><span>Recover less, but intercept the Sovereign before its minion arrives.</span></button>
          <p className="vote-status">{voteCount} / {Object.values(game.players).filter((player) => player.hp > 0).length} votes locked</p>
        </div>
      ) : game.hostId === selfId ? (
        <button className="gold final-continue" onClick={() => send({ type: "continue-after-choice" })}>Face the Sovereign</button>
      ) : <span className="hint">The party leader is advancing the story…</span>}
    </section>
  );
}

function Battle({ game, selfId, send }: GameScreenProps) {
  const self = game.players[selfId];
  const role = self?.roleId ? ROLES[self.roleId] : null;
  const [abilityId, setAbilityId] = useState("");
  const [targetId, setTargetId] = useState("");
  const round = game.battle?.round ?? 0;

  useEffect(() => { setAbilityId(""); setTargetId(""); }, [round]);
  const ability = role?.abilities.find((candidate) => candidate.id === abilityId);
  const defaultTarget = ability?.target === "self" ? selfId
    : ability?.target === "ally" ? selfId
    : ability?.target === "enemy" ? game.battle?.enemies.find((enemy) => enemy.hp > 0)?.id ?? ""
    : "";
  const chosenTarget = targetId || defaultTarget;
  const locked = Boolean(self?.action);
  const lockedCount = Object.values(game.players).filter((player) => player.hp > 0 && player.action).length;
  const aliveCount = Object.values(game.players).filter((player) => player.hp > 0).length;

  function lockAction() {
    if (!ability) return;
    send({ type: "combat-action", action: { abilityId: ability.id, ...(chosenTarget ? { targetId: chosenTarget } : {}) } });
  }

  return (
    <section className="battle-page">
      <div className="battle-topline"><div><p className="eyebrow">{game.battle?.id === "alley-brawl" ? "Lantern Alley" : "The ruined watch-house"}</p><h1>Round {round}</h1></div><RoundTimer deadline={game.battle?.deadline ?? Date.now()} /><span className="lock-count">{lockedCount}/{aliveCount} locked</span></div>
      <div className="battlefield panel">
        <div className="unit-line enemies">
          {game.battle?.enemies.map((enemy) => <UnitCard key={enemy.id} name={enemy.name} image={`/assets/${enemy.kind}.png`} hp={enemy.hp} maxHp={enemy.maxHp} defeated={enemy.hp <= 0} />)}
        </div>
        <div className="versus-mark">VS</div>
        <div className="unit-line party">
          {Object.values(game.players).map((player) => <PlayerUnit key={player.id} player={player} active={player.id === selfId} />)}
        </div>
      </div>
      <div className="battle-console">
        <div className="action-picker panel">
          <div className="console-title"><div><p className="eyebrow">Your action</p><h2>{self?.hp ? (locked ? "Action locked" : "Choose together") : "You have fallen"}</h2></div>{locked && <span className="locked-badge">Ready</span>}</div>
          {self && self.hp > 0 && role && (
            <>
              <div className="ability-grid">{role.abilities.map((candidate) => <button key={candidate.id} className={abilityId === candidate.id ? "selected" : ""} disabled={candidate.mpCost > self.mp} onClick={() => { setAbilityId(candidate.id); setTargetId(""); }}><strong>{candidate.name}</strong><span>{candidate.description}</span><small>{candidate.mpCost ? `${candidate.mpCost} MP` : "Free"}</small></button>)}</div>
              {ability && <TargetPicker ability={ability} game={game} selfId={selfId} targetId={chosenTarget} setTargetId={setTargetId} />}
              <button className="gold lock-button" disabled={!ability || (ability.target !== "all-enemies" && !chosenTarget)} onClick={lockAction}>{locked ? "Change locked action" : "Lock action"}</button>
            </>
          )}
        </div>
        <EventLog game={game} />
      </div>
    </section>
  );
}

function TargetPicker({ ability, game, selfId, targetId, setTargetId }: { ability: AbilityDefinition; game: GameState; selfId: string; targetId: string; setTargetId: (id: string) => void }) {
  if (ability.target === "all-enemies") return <p className="target-note">Targets every living enemy.</p>;
  if (ability.target === "self") return <p className="target-note">Targets you.</p>;
  const targets = ability.target === "ally"
    ? Object.values(game.players).filter((player) => player.hp > 0)
    : game.battle!.enemies.filter((enemy) => enemy.hp > 0);
  return <div className="target-row"><span>Target</span>{targets.map((target) => <button key={target.id} className={targetId === target.id ? "selected" : ""} onClick={() => setTargetId(target.id)}>{"roleId" in target ? (target.id === selfId ? "Yourself" : target.name) : target.name}</button>)}</div>;
}

function UnitCard({ name, image, hp, maxHp, defeated }: { name: string; image: string; hp: number; maxHp: number; defeated?: boolean }) {
  return <div className={`unit-card ${defeated ? "defeated" : ""}`}><img src={image} alt={name} /><strong>{name}</strong><Meter value={hp} max={maxHp} kind="hp" /><small>{hp} / {maxHp} HP</small></div>;
}

function PlayerUnit({ player, active }: { player: PlayerState; active: boolean }) {
  const role = player.roleId ? ROLES[player.roleId] : null;
  return <div className={`unit-card player-unit ${active ? "active" : ""} ${player.hp <= 0 ? "defeated" : ""}`}><img src={player.roleId ? portraitPath(player.roleId, player.portrait) : "/assets/logo.png"} alt="" /><strong>{player.name}</strong><small>{role?.name}</small>{role && <><Meter value={player.hp} max={role.maxHp} kind="hp" /><Meter value={player.mp} max={role.maxMp} kind="mp" /></>}</div>;
}

function Meter({ value, max, kind }: { value: number; max: number; kind: "hp" | "mp" }) {
  const width = Math.max(0, Math.min(100, (value / max) * 100));
  return <span className={`meter ${kind}`} aria-label={`${value} of ${max} ${kind.toUpperCase()}`}><i style={{ width: `${width}%` }} /></span>;
}

function EventLog({ game }: { game: GameState }) {
  return <aside className="event-log panel"><p className="eyebrow">The round unfolds</p><div>{game.events.slice(-7).reverse().map((entry) => <p key={entry.id} className={entry.tone}>{entry.message}</p>)}</div></aside>;
}

function RoundTimer({ deadline }: { deadline: number }) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => { const timer = window.setInterval(() => setNow(Date.now()), 250); return () => window.clearInterval(timer); }, []);
  const remaining = Math.max(0, Math.ceil((deadline - now) / 1000));
  return <span className="round-timer"><b>{remaining}</b> seconds to lock</span>;
}

function Ending({ game, selfId, send }: GameScreenProps) {
  return (
    <section className={`ending panel ${game.victory ? "victory" : "defeat"}`}>
      <p className="eyebrow">The tracer bullet lands</p>
      <h1>{game.victory ? "Dawn reaches the alley." : "The dark wins this run."}</h1>
      <p>{game.events.at(-1)?.message}</p>
      <div className="ending-party">{Object.values(game.players).map((player) => <div key={player.id}><img src={player.roleId ? portraitPath(player.roleId, player.portrait) : "/assets/logo.png"} alt="" /><strong>{player.name}</strong><span>{player.roleId ? ROLES[player.roleId].name : "Traveler"} · {player.hp} HP</span></div>)}</div>
      <div className="run-summary"><span>Party choice <b>{game.resolvedChoice === "all-rest" ? "All rest" : "Rotate watch"}</b></span><span>Outcome <b>{game.victory ? "Sovereign defeated" : "Party defeated"}</b></span></div>
      {game.hostId === selfId ? <button className="gold" onClick={() => send({ type: "play-again" })}>Gather the party again</button> : <span className="hint">Waiting for the party leader…</span>}
    </section>
  );
}

function MiniPortrait({ player }: { player: PlayerState }) {
  return <div><img src={player.roleId ? portraitPath(player.roleId, player.portrait) : "/assets/logo.png"} alt="" /><span>{player.name}</span></div>;
}

function portraitPath(roleId: RoleId, portrait: "male" | "female") {
  return `/assets/${roleId.toUpperCase().replace("-", "")}-${portrait.toUpperCase()}.png`;
}

interface GameScreenProps {
  game: GameState;
  selfId: string;
  send: (command: ClientCommand) => void;
}
