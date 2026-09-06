export type Phase =
  | "lobby"
  | "intro"
  | "tutorial-battle"
  | "party-choice"
  | "choice-result"
  | "final-battle"
  | "ending";

export type RoleId = "paladin" | "black-mage" | "white-mage" | "archer";
export type PortraitId = "male" | "female";
export type BattleId = "alley-brawl" | "arachnid-lair";
export type ChoiceId = "all-rest" | "rotate-watch";
export type TargetKind = "enemy" | "ally" | "self" | "all-enemies";

export interface AbilityDefinition {
  id: string;
  name: string;
  description: string;
  target: TargetKind;
  min: number;
  max: number;
  mpCost: number;
  heal?: boolean;
  guard?: boolean;
}

export interface RoleDefinition {
  id: RoleId;
  name: string;
  tagline: string;
  maxHp: number;
  maxMp: number;
  speed: number;
  abilities: AbilityDefinition[];
}

export interface PlayerState {
  id: string;
  name: string;
  roleId: RoleId | null;
  portrait: PortraitId;
  ready: boolean;
  connected: boolean;
  hp: number;
  mp: number;
  guarding: boolean;
  action: CombatAction | null;
}

export interface EnemyState {
  id: string;
  kind: "drunk-man-1" | "drunk-man-2" | "arachnid-sovereign" | "arachnid-minion";
  name: string;
  hp: number;
  maxHp: number;
  speed: number;
  minDamage: number;
  maxDamage: number;
}

export interface CombatAction {
  abilityId: string;
  targetId?: string;
}

export interface BattleState {
  id: BattleId;
  round: number;
  enemies: EnemyState[];
  deadline: number;
}

export interface GameEvent {
  id: number;
  tone: "story" | "action" | "damage" | "heal" | "system";
  message: string;
}

export interface GameState {
  roomId: string;
  phase: Phase;
  hostId: string | null;
  players: Record<string, PlayerState>;
  introIndex: number;
  votes: Record<string, ChoiceId>;
  resolvedChoice: ChoiceId | null;
  battle: BattleState | null;
  events: GameEvent[];
  eventSequence: number;
  victory: boolean | null;
}

export type ClientCommand =
  | { type: "choose-character"; roleId: RoleId; portrait: PortraitId }
  | { type: "set-ready"; ready: boolean }
  | { type: "start-game" }
  | { type: "advance-story" }
  | { type: "cast-vote"; choiceId: ChoiceId }
  | { type: "continue-after-choice" }
  | { type: "combat-action"; action: CombatAction }
  | { type: "play-again" };

export interface CommandEnvelope {
  command: ClientCommand;
}
