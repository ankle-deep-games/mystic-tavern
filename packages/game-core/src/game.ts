import { findAbility, INTRO_LINES, ROLE_ORDER, ROLES } from "./content.js";
import type {
  BattleId,
  ChoiceId,
  CombatAction,
  EnemyState,
  GameState,
  PlayerState,
  PortraitId,
  RoleId
} from "./types.js";

export const ROUND_SECONDS = 20;

export class GameRuleError extends Error {}

export function createGame(roomId: string): GameState {
  return {
    roomId,
    phase: "lobby",
    hostId: null,
    players: {},
    introIndex: 0,
    votes: {},
    resolvedChoice: null,
    battle: null,
    events: [],
    eventSequence: 0,
    victory: null
  };
}

export function addPlayer(state: GameState, id: string, name: string): void {
  if (state.phase !== "lobby") throw new GameRuleError("This adventure has already begun.");
  if (Object.keys(state.players).length >= 4) throw new GameRuleError("This party is already full.");
  const safeName = name.trim().slice(0, 18) || `Traveler ${Object.keys(state.players).length + 1}`;
  state.players[id] = {
    id,
    name: safeName,
    roleId: null,
    portrait: "female",
    ready: false,
    connected: true,
    hp: 0,
    mp: 0,
    guarding: false,
    action: null
  };
  state.hostId ??= id;
  event(state, "system", `${safeName} joined the party.`);
}

export function removePlayer(state: GameState, id: string): void {
  const player = state.players[id];
  if (!player) return;
  if (state.phase === "lobby") {
    delete state.players[id];
    if (state.hostId === id) state.hostId = Object.keys(state.players)[0] ?? null;
    event(state, "system", `${player.name} left the party.`);
  } else {
    player.connected = false;
    event(state, "system", `${player.name} lost their connection. They will defend until they return.`);
  }
}

export function setConnected(state: GameState, id: string, connected: boolean): void {
  const player = requirePlayer(state, id);
  player.connected = connected;
  if (connected) event(state, "system", `${player.name} rejoined the party.`);
}

export function chooseCharacter(state: GameState, id: string, roleId: RoleId, portrait: PortraitId): void {
  requirePhase(state, "lobby");
  const player = requirePlayer(state, id);
  const roleTaken = Object.values(state.players).some((candidate) => candidate.id !== id && candidate.roleId === roleId);
  if (roleTaken) throw new GameRuleError(`${ROLES[roleId].name} is already claimed.`);
  player.roleId = roleId;
  player.portrait = portrait;
  player.ready = false;
  event(state, "system", `${player.name} chose ${ROLES[roleId].name}.`);
}

export function setReady(state: GameState, id: string, ready: boolean): void {
  requirePhase(state, "lobby");
  const player = requirePlayer(state, id);
  if (!player.roleId) throw new GameRuleError("Choose a character first.");
  player.ready = ready;
}

export function canStart(state: GameState): boolean {
  const players = Object.values(state.players);
  return players.length === 4 && players.every((player) => player.roleId && player.ready);
}

export function startGame(state: GameState, id: string): void {
  requirePhase(state, "lobby");
  if (state.hostId !== id) throw new GameRuleError("Only the party leader can begin.");
  if (!canStart(state)) throw new GameRuleError("Four characters must be chosen and ready.");
  for (const player of Object.values(state.players)) {
    const role = ROLES[player.roleId!];
    player.hp = role.maxHp;
    player.mp = role.maxMp;
  }
  state.phase = "intro";
  state.events = [];
  event(state, "story", INTRO_LINES[0].text);
}

export function advanceStory(state: GameState, id: string, now = Date.now()): void {
  requirePhase(state, "intro");
  if (state.hostId !== id) throw new GameRuleError("The party leader advances shared dialogue.");
  state.introIndex += 1;
  if (state.introIndex >= INTRO_LINES.length) {
    beginBattle(state, "alley-brawl", now);
    return;
  }
  event(state, "story", INTRO_LINES[state.introIndex]!.text);
}

export function castVote(state: GameState, id: string, choiceId: ChoiceId): boolean {
  requirePhase(state, "party-choice");
  requirePlayer(state, id);
  state.votes[id] = choiceId;
  const livingVoters = Object.values(state.players).filter((player) => player.hp > 0);
  if (!livingVoters.every((player) => state.votes[player.id])) return false;

  const counts: Record<ChoiceId, number> = { "all-rest": 0, "rotate-watch": 0 };
  for (const vote of Object.values(state.votes)) counts[vote] += 1;
  const hostVote = state.hostId ? state.votes[state.hostId] : undefined;
  state.resolvedChoice = counts["all-rest"] === counts["rotate-watch"]
    ? hostVote ?? "rotate-watch"
    : counts["all-rest"] > counts["rotate-watch"] ? "all-rest" : "rotate-watch";

  const rest = state.resolvedChoice === "all-rest";
  for (const player of Object.values(state.players)) {
    if (!player.roleId || player.hp <= 0) continue;
    const role = ROLES[player.roleId];
    const ratio = rest ? 1 : 0.45;
    player.hp = Math.min(role.maxHp, player.hp + Math.round(role.maxHp * ratio));
    player.mp = Math.min(role.maxMp, player.mp + Math.round(role.maxMp * ratio));
  }
  state.phase = "choice-result";
  event(state, "story", rest
    ? "The party sleeps deeply and wakes restored—too late to prevent the brood from gathering."
    : "Taking turns on watch costs some rest, but the sentry spots the brood before it can mass.");
  return true;
}

export function continueAfterChoice(state: GameState, id: string, now = Date.now()): void {
  requirePhase(state, "choice-result");
  if (state.hostId !== id) throw new GameRuleError("The party leader advances the adventure.");
  beginBattle(state, "arachnid-lair", now);
}

export function submitAction(state: GameState, id: string, action: CombatAction): boolean {
  requireBattlePhase(state);
  const player = requirePlayer(state, id);
  if (player.hp <= 0) throw new GameRuleError("A fallen character cannot act.");
  if (!player.roleId) throw new GameRuleError("Character role is missing.");
  const ability = findAbility(player.roleId, action.abilityId);
  if (!ability) throw new GameRuleError("That ability does not belong to this character.");
  if (player.mp < ability.mpCost) throw new GameRuleError("Not enough MP.");
  validateTarget(state, id, action, ability.target);
  player.action = action;
  return livingPlayers(state).every((candidate) => candidate.action !== null);
}

export function fillMissingActions(state: GameState): void {
  if (!state.battle) return;
  const firstEnemy = state.battle.enemies.find((enemy) => enemy.hp > 0);
  for (const player of livingPlayers(state)) {
    if (player.action || !player.roleId || !firstEnemy) continue;
    const basic = ROLES[player.roleId].abilities.find((ability) => ability.target === "enemy" && ability.mpCost === 0)!;
    player.action = { abilityId: basic.id, targetId: firstEnemy.id };
  }
}

export function resolveRound(state: GameState, random: () => number = Math.random, now = Date.now()): void {
  requireBattlePhase(state);
  if (!state.battle) return;
  fillMissingActions(state);
  const orderedPlayers = livingPlayers(state).sort((a, b) => ROLES[b.roleId!].speed - ROLES[a.roleId!].speed);
  for (const player of Object.values(state.players)) player.guarding = false;

  for (const player of orderedPlayers) {
    if (player.hp <= 0 || !player.roleId || !player.action) continue;
    const ability = findAbility(player.roleId, player.action.abilityId)!;
    player.mp -= ability.mpCost;
    if (ability.guard) {
      player.guarding = true;
      event(state, "action", `${player.name} stands fast and braces for impact.`);
    } else if (ability.heal) {
      const target = state.players[player.action.targetId ?? player.id];
      if (target && target.hp > 0 && target.roleId) {
        const amount = roll(ability.min, ability.max, random);
        const before = target.hp;
        target.hp = Math.min(ROLES[target.roleId].maxHp, target.hp + amount);
        event(state, "heal", `${player.name} uses ${ability.name}; ${target.name} recovers ${target.hp - before} HP.`);
      }
    } else {
      const targets = ability.target === "all-enemies"
        ? state.battle.enemies.filter((enemy) => enemy.hp > 0)
        : state.battle.enemies.filter((enemy) => enemy.id === player.action?.targetId && enemy.hp > 0);
      for (const target of targets) {
        const amount = roll(ability.min, ability.max, random);
        target.hp = Math.max(0, target.hp - amount);
        event(state, "damage", `${player.name} uses ${ability.name} on ${target.name} for ${amount} damage.`);
      }
    }
  }

  if (state.battle.enemies.every((enemy) => enemy.hp <= 0)) {
    finishBattle(state);
    return;
  }

  const enemies = state.battle.enemies.filter((enemy) => enemy.hp > 0).sort((a, b) => b.speed - a.speed);
  for (const enemy of enemies) {
    const targets = livingPlayers(state);
    if (targets.length === 0) break;
    const target = targets[Math.floor(random() * targets.length)] ?? targets[0]!;
    let amount = roll(enemy.minDamage, enemy.maxDamage, random);
    if (target.guarding) amount = Math.ceil(amount / 2);
    target.hp = Math.max(0, target.hp - amount);
    event(state, "damage", `${enemy.name} strikes ${target.name} for ${amount} damage.`);
  }

  if (livingPlayers(state).length === 0) {
    state.phase = "ending";
    state.victory = false;
    state.battle = null;
    event(state, "story", "The crystal light gutters out. The brood claims Lantern Alley—for now.");
    return;
  }

  state.battle.round += 1;
  state.battle.deadline = now + ROUND_SECONDS * 1000;
  for (const player of Object.values(state.players)) player.action = null;
}

export function resetGame(state: GameState, id: string): void {
  requirePhase(state, "ending");
  if (state.hostId !== id) throw new GameRuleError("Only the party leader can reset the room.");
  state.phase = "lobby";
  state.introIndex = 0;
  state.votes = {};
  state.resolvedChoice = null;
  state.battle = null;
  state.events = [];
  state.victory = null;
  for (const player of Object.values(state.players)) {
    player.ready = false;
    player.hp = 0;
    player.mp = 0;
    player.guarding = false;
    player.action = null;
  }
  event(state, "system", "The party gathers for another run.");
}

export function roleAvailability(state: GameState): Record<RoleId, boolean> {
  return Object.fromEntries(ROLE_ORDER.map((roleId) => [roleId, !Object.values(state.players).some((player) => player.roleId === roleId)])) as Record<RoleId, boolean>;
}

function beginBattle(state: GameState, battleId: BattleId, now: number): void {
  state.phase = battleId === "alley-brawl" ? "tutorial-battle" : "final-battle";
  state.battle = {
    id: battleId,
    round: 1,
    deadline: now + ROUND_SECONDS * 1000,
    enemies: battleId === "alley-brawl"
      ? [enemy("drunk-1", "drunk-man-1", "Drunk Man One", 66, 6, 8, 13), enemy("drunk-2", "drunk-man-2", "Drunk Man Two", 66, 5, 8, 13)]
      : finalEnemies(state.resolvedChoice === "all-rest")
  };
  for (const player of Object.values(state.players)) player.action = null;
  event(state, "story", battleId === "alley-brawl"
    ? "The two thugs lunge. Choose actions together, then watch the round resolve by speed."
    : "The Arachnid Sovereign descends, blotting out the last clean sliver of moonlight.");
}

function finalEnemies(ambushed: boolean): EnemyState[] {
  const enemies = [enemy("sovereign", "arachnid-sovereign", "Arachnid Sovereign", 190, 10, 13, 18)];
  if (ambushed) enemies.push(enemy("minion", "arachnid-minion", "Brood Minion", 62, 12, 7, 11));
  return enemies;
}

function finishBattle(state: GameState): void {
  const battleId = state.battle?.id;
  state.battle = null;
  for (const player of Object.values(state.players)) player.action = null;
  if (battleId === "alley-brawl") {
    state.phase = "party-choice";
    state.votes = {};
    event(state, "story", "The Old Man leads the party to a ruined watch-house. Rest fully and risk an ambush, or rotate the watch and meet the brood early?");
  } else {
    state.phase = "ending";
    state.victory = true;
    event(state, "story", "The Sovereign collapses. Four crystals answer one another, and dawn finally reaches Lantern Alley.");
  }
}

function enemy(id: string, kind: EnemyState["kind"], name: string, hp: number, speed: number, minDamage: number, maxDamage: number): EnemyState {
  return { id, kind, name, hp, maxHp: hp, speed, minDamage, maxDamage };
}

function validateTarget(state: GameState, id: string, action: CombatAction, target: string): void {
  if (!state.battle) throw new GameRuleError("There is no active battle.");
  if (target === "enemy" && !state.battle.enemies.some((enemy) => enemy.id === action.targetId && enemy.hp > 0)) {
    throw new GameRuleError("Choose a living enemy.");
  }
  if (target === "ally" && !Object.values(state.players).some((player) => player.id === action.targetId && player.hp > 0)) {
    throw new GameRuleError("Choose a living ally.");
  }
  if (target === "self" && action.targetId && action.targetId !== id) throw new GameRuleError("That ability targets its caster.");
}

function requirePlayer(state: GameState, id: string): PlayerState {
  const player = state.players[id];
  if (!player) throw new GameRuleError("Player is not in this room.");
  return player;
}

function requirePhase(state: GameState, phase: GameState["phase"]): void {
  if (state.phase !== phase) throw new GameRuleError(`That action is not available during ${state.phase}.`);
}

function requireBattlePhase(state: GameState): void {
  if (state.phase !== "tutorial-battle" && state.phase !== "final-battle") {
    throw new GameRuleError("There is no active battle.");
  }
}

function livingPlayers(state: GameState): PlayerState[] {
  return Object.values(state.players).filter((player) => player.hp > 0);
}

function roll(min: number, max: number, random: () => number): number {
  return Math.floor(random() * (max - min + 1)) + min;
}

function event(state: GameState, tone: GameState["events"][number]["tone"], message: string): void {
  state.eventSequence += 1;
  state.events.push({ id: state.eventSequence, tone, message });
  state.events = state.events.slice(-12);
}
