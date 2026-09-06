import {
  GameRuleError,
  addPlayer,
  advanceStory,
  castVote,
  chooseCharacter,
  continueAfterChoice,
  createGame,
  removePlayer,
  resetGame,
  resolveRound,
  setConnected,
  setReady,
  startGame,
  submitAction,
  type ClientCommand,
  type GameState
} from "@adg/game-core";
import { Client, Room } from "colyseus";
import { z } from "zod";

const roleId = z.enum(["paladin", "black-mage", "white-mage", "archer"]);
const portrait = z.enum(["male", "female"]);
const choiceId = z.enum(["all-rest", "rotate-watch"]);

const commandSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("choose-character"), roleId, portrait }),
  z.object({ type: z.literal("set-ready"), ready: z.boolean() }),
  z.object({ type: z.literal("start-game") }),
  z.object({ type: z.literal("advance-story") }),
  z.object({ type: z.literal("cast-vote"), choiceId }),
  z.object({ type: z.literal("continue-after-choice") }),
  z.object({
    type: z.literal("combat-action"),
    action: z.object({ abilityId: z.string().min(1).max(40), targetId: z.string().min(1).max(80).optional() })
  }),
  z.object({ type: z.literal("play-again") })
]);

const joinOptions = z.object({ name: z.string().trim().min(1).max(18) });

export class GameRoom extends Room {
  maxClients = 4;
  private game!: GameState;
  private roundTimer: ReturnType<typeof setTimeout> | null = null;

  onCreate(): void {
    this.game = createGame(this.roomId);
    this.onMessage("command", (client, payload) => this.handleCommand(client, payload));
    this.onMessage("request-state", (client) => client.send("game-state", this.game));
  }

  onJoin(client: Client, options: unknown): void {
    const parsed = joinOptions.safeParse(options);
    if (!parsed.success) throw new GameRuleError("Enter a traveler name between 1 and 18 characters.");
    addPlayer(this.game, client.sessionId, parsed.data.name);
    this.publish();
  }

  async onDrop(client: Client): Promise<void> {
    if (!this.game.players[client.sessionId]) return;
    setConnected(this.game, client.sessionId, false);
    this.publish();
    try {
      await this.allowReconnection(client, 30);
    } catch {
      removePlayer(this.game, client.sessionId);
      this.publish();
    }
  }

  onReconnect(client: Client): void {
    if (!this.game.players[client.sessionId]) return;
    setConnected(this.game, client.sessionId, true);
    this.publish();
  }

  onLeave(client: Client): void {
    removePlayer(this.game, client.sessionId);
    this.publish();
  }

  onDispose(): void {
    this.clearRoundTimer();
  }

  private handleCommand(client: Client, payload: unknown): void {
    const parsed = commandSchema.safeParse(payload);
    if (!parsed.success) {
      client.send("game-error", { message: "That command was malformed." });
      return;
    }

    try {
      const command = parsed.data as ClientCommand;
      switch (command.type) {
        case "choose-character":
          chooseCharacter(this.game, client.sessionId, command.roleId, command.portrait);
          break;
        case "set-ready":
          setReady(this.game, client.sessionId, command.ready);
          break;
        case "start-game":
          startGame(this.game, client.sessionId);
          break;
        case "advance-story":
          advanceStory(this.game, client.sessionId);
          break;
        case "cast-vote":
          castVote(this.game, client.sessionId, command.choiceId);
          break;
        case "continue-after-choice":
          continueAfterChoice(this.game, client.sessionId);
          break;
        case "combat-action": {
          const everyoneLocked = submitAction(this.game, client.sessionId, command.action);
          if (everyoneLocked) this.resolveNow();
          break;
        }
        case "play-again":
          resetGame(this.game, client.sessionId);
          break;
      }
      this.publish();
      this.scheduleRoundTimer();
    } catch (error) {
      const message = error instanceof GameRuleError ? error.message : "The server could not perform that action.";
      client.send("game-error", { message });
    }
  }

  private resolveNow(): void {
    this.clearRoundTimer();
    resolveRound(this.game);
  }

  private scheduleRoundTimer(): void {
    const battle = this.game.battle;
    if (!battle || this.roundTimer) return;
    const delay = Math.max(0, battle.deadline - Date.now());
    this.roundTimer = setTimeout(() => {
      this.roundTimer = null;
      try {
        resolveRound(this.game);
        this.publish();
        this.scheduleRoundTimer();
      } catch {
        // The phase may have moved on while the timeout was queued.
      }
    }, delay);
  }

  private clearRoundTimer(): void {
    if (!this.roundTimer) return;
    clearTimeout(this.roundTimer);
    this.roundTimer = null;
  }

  private publish(): void {
    this.broadcast("game-state", this.game);
  }
}
