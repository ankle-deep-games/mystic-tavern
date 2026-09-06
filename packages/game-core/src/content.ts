import type { RoleDefinition, RoleId } from "./types.js";

export const INTRO_LINES = [
  {
    speaker: "Narrator",
    text: "Rain needles the stones of Lantern Alley as four strangers follow the same impossible glow."
  },
  {
    speaker: "Old Man",
    text: "You carry the crystal marks. Good. I was beginning to think the dark had swallowed every hero left."
  },
  {
    speaker: "Drunk Man",
    text: "Heroes? In our alley? Hand over the shiny rocks and nobody has to lose any teeth."
  },
  {
    speaker: "Narrator",
    text: "The strangers exchange one look. Whatever comes next, they face it as a party."
  }
] as const;

export const ROLES: Record<RoleId, RoleDefinition> = {
  paladin: {
    id: "paladin",
    name: "Paladin",
    tagline: "Protect the party and punish the wicked.",
    maxHp: 92,
    maxMp: 18,
    speed: 7,
    abilities: [
      { id: "paladin-strike", name: "Radiant Strike", description: "Reliable damage to one enemy.", target: "enemy", min: 16, max: 22, mpCost: 0 },
      { id: "paladin-guard", name: "Stand Fast", description: "Guard yourself and halve incoming damage.", target: "self", min: 0, max: 0, mpCost: 2, guard: true }
    ]
  },
  "black-mage": {
    id: "black-mage",
    name: "Black Mage",
    tagline: "Spend mana for explosive single-target damage.",
    maxHp: 58,
    maxMp: 32,
    speed: 9,
    abilities: [
      { id: "arcane-bolt", name: "Arcane Bolt", description: "A quick, mana-free spell.", target: "enemy", min: 13, max: 18, mpCost: 0 },
      { id: "cinder-lance", name: "Cinder Lance", description: "Heavy damage to one enemy.", target: "enemy", min: 23, max: 30, mpCost: 7 }
    ]
  },
  "white-mage": {
    id: "white-mage",
    name: "White Mage",
    tagline: "Keep allies standing without becoming helpless.",
    maxHp: 66,
    maxMp: 36,
    speed: 8,
    abilities: [
      { id: "light-burst", name: "Light Burst", description: "Holy damage to one enemy.", target: "enemy", min: 11, max: 16, mpCost: 0 },
      { id: "mend", name: "Mend", description: "Restore health to one party member.", target: "ally", min: 20, max: 27, mpCost: 6, heal: true }
    ]
  },
  archer: {
    id: "archer",
    name: "Archer",
    tagline: "Act first and pressure the entire enemy line.",
    maxHp: 72,
    maxMp: 24,
    speed: 13,
    abilities: [
      { id: "quick-shot", name: "Quick Shot", description: "Fast damage to one enemy.", target: "enemy", min: 15, max: 20, mpCost: 0 },
      { id: "volley", name: "Volley", description: "Damage every living enemy.", target: "all-enemies", min: 10, max: 14, mpCost: 5 }
    ]
  }
};

export const ROLE_ORDER = Object.keys(ROLES) as RoleId[];

export function findAbility(roleId: RoleId, abilityId: string) {
  return ROLES[roleId].abilities.find((ability) => ability.id === abilityId);
}
