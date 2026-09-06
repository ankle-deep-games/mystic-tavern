import { describe, expect, it } from "vitest";
import {
  addPlayer,
  advanceStory,
  canStart,
  castVote,
  chooseCharacter,
  continueAfterChoice,
  createGame,
  INTRO_LINES,
  ROLES,
  resolveRound,
  setReady,
  startGame,
  submitAction
} from "../src/index.js";

function readyParty() {
  const state = createGame("ROOM123");
  const roles = ["paladin", "black-mage", "white-mage", "archer"] as const;
  roles.forEach((role, index) => {
    const id = `p${index + 1}`;
    addPlayer(state, id, `Player ${index + 1}`);
    chooseCharacter(state, id, role, index % 2 ? "male" : "female");
    setReady(state, id, true);
  });
  return state;
}

function lockBasicActions(state: ReturnType<typeof readyParty>) {
  const enemyId = state.battle!.enemies.find((enemy) => enemy.hp > 0)!.id;
  submitAction(state, "p1", { abilityId: "paladin-strike", targetId: enemyId });
  submitAction(state, "p2", { abilityId: "arcane-bolt", targetId: enemyId });
  submitAction(state, "p3", { abilityId: "light-burst", targetId: enemyId });
  return submitAction(state, "p4", { abilityId: "quick-shot", targetId: enemyId });
}

describe("tracer-bullet game", () => {
  it("requires exactly four unique ready characters", () => {
    const state = readyParty();
    expect(canStart(state)).toBe(true);
    expect(() => chooseCharacter(state, "p2", "paladin", "male")).toThrow(/already claimed/);
  });

  it("runs from lobby through choice and final victory", () => {
    const state = readyParty();
    startGame(state, "p1");
    for (let index = 0; index < INTRO_LINES.length; index += 1) advanceStory(state, "p1", 1_000);
    expect(state.phase).toBe("tutorial-battle");

    while (state.phase === "tutorial-battle") {
      expect(lockBasicActions(state)).toBe(true);
      resolveRound(state, () => 0.99, 2_000);
    }
    expect(state.phase).toBe("party-choice");

    castVote(state, "p1", "rotate-watch");
    castVote(state, "p2", "rotate-watch");
    castVote(state, "p3", "all-rest");
    expect(castVote(state, "p4", "all-rest")).toBe(true);
    expect(state.resolvedChoice).toBe("rotate-watch");

    continueAfterChoice(state, "p1", 3_000);
    expect(state.battle?.enemies).toHaveLength(1);
    while (state.phase === "final-battle") {
      expect(lockBasicActions(state)).toBe(true);
      resolveRound(state, () => 0.99, 4_000);
    }
    expect(state.phase).toBe("ending");
    expect(state.victory).toBe(true);
  });

  it("makes the full-rest vote restore the party and add the ambush minion", () => {
    const state = readyParty();
    state.phase = "party-choice";
    for (const player of Object.values(state.players)) {
      player.hp = 1;
      player.mp = 0;
    }

    for (const id of Object.keys(state.players)) castVote(state, id, "all-rest");
    expect(state.resolvedChoice).toBe("all-rest");
    for (const player of Object.values(state.players)) {
      const role = ROLES[player.roleId!];
      expect(player.hp).toBe(role.maxHp);
      expect(player.mp).toBe(role.maxMp);
    }

    continueAfterChoice(state, "p1", 3_000);
    expect(state.battle?.enemies.map((enemy) => enemy.kind)).toEqual([
      "arachnid-sovereign",
      "arachnid-minion"
    ]);
  });
});
