import { expect, test, type Browser, type Page } from "@playwright/test";

async function newTraveler(browser: Browser, name: string) {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto("/");
  await page.getByLabel("Traveler name").fill(name);
  return { context, page };
}

async function lockRound(page: Page, abilityName: RegExp) {
  const ability = page.getByRole("button", { name: abilityName });
  if (!await ability.isVisible().catch(() => false) || !await ability.isEnabled()) return;
  await ability.click();
  await page.getByRole("button", { name: /Lock action|Change locked action/ }).click();
}

async function finishBattle(pages: Page[], abilities: RegExp[], nextHeading: RegExp) {
  for (let round = 0; round < 10; round += 1) {
    if (await pages[0]!.getByRole("heading", { name: nextHeading }).isVisible().catch(() => false)) return;
    await Promise.all(pages.map((page, index) => lockRound(page, abilities[index]!)));
    await Promise.race([
      pages[0]!.getByRole("heading", { name: nextHeading }).waitFor({ state: "visible" }),
      pages[0]!.getByRole("heading", { name: /Round \d+/ }).waitFor({ state: "visible" })
    ]).catch(() => undefined);
    await pages[0]!.waitForTimeout(200);
  }
  await expect(pages[0]!.getByRole("heading", { name: nextHeading })).toBeVisible();
}

test("four players complete the shared tracer-bullet adventure", async ({ browser }) => {
  const travelers = await Promise.all([
    newTraveler(browser, "Jordan"),
    newTraveler(browser, "David"),
    newTraveler(browser, "Mara"),
    newTraveler(browser, "Theo")
  ]);
  const pages = travelers.map(({ page }) => page);

  await pages[0]!.getByRole("button", { name: "Create a party" }).click();
  const roomCode = (await pages[0]!.locator(".code").textContent())!.trim();
  expect(roomCode).not.toBe("");

  for (const page of pages.slice(1)) {
    await page.getByLabel("Party code").fill(roomCode);
    await page.getByRole("button", { name: "Join", exact: true }).click();
  }

  const roles = [/Paladin/, /Black Mage/, /White Mage/, /Archer/];
  for (let index = 0; index < pages.length; index += 1) {
    await pages[index]!.getByRole("button", { name: roles[index]! }).click();
    await pages[index]!.getByRole("button", { name: "Ready up" }).click();
  }

  await pages[0]!.getByRole("button", { name: "Begin the adventure" }).click();
  for (let line = 0; line < 3; line += 1) await pages[0]!.getByRole("button", { name: "Continue" }).click();
  await pages[0]!.getByRole("button", { name: "Stand together" }).click();

  const abilities = [/Radiant Strike/, /Arcane Bolt/, /Light Burst/, /Quick Shot/];
  await finishBattle(pages, abilities, /How will you meet the night/);

  for (const page of pages) await page.getByRole("button", { name: /Rotate the watch/ }).click();
  await expect(pages[0]!.getByRole("heading", { name: "The watch rotates." })).toBeVisible();
  await pages[0]!.getByRole("button", { name: "Face the Sovereign" }).click();

  await finishBattle(pages, abilities, /Dawn reaches the alley/);
  await expect(pages[0]!.getByText("Sovereign defeated", { exact: true })).toBeVisible();

  await Promise.all(travelers.map(({ context }) => context.close()));
});
