import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {
  loadModel, freshState, applyXp, commitCorrect, applyMiss, commitBoss, commitVerseSeen,
  commitGift, commitRestVerse, gemCount, reconcile, regionOpenMap, zoneOpen, chooseZone,
  buildRun, advanceAfterReveal, finishZoneRun, shouldRest, verseForDate, prepareRestore,
  buyItem, equipItem, playClip, bannerKey, levelForXp, xpToReach, showsEnglishAnswer, missOutcome,
  gearBonuses, awardExtras, noteMiss, shopRows, beginKneel, thaiReviewQueue, endingPairs,
  endingDiscrepancy, buildDuelSchedule, speakEnglish, bonusWordsFor, spellStep, countPlates,
  SETTLED_APPROVALS, countPrompt, trophiesByTab, pendingMaxwell, fillBackupCompare, pickNewerState
} from "../js/engine.mjs";

const raw = JSON.parse(fs.readFileSync(new URL("../data/cards.json", import.meta.url), "utf8"));
const daily = JSON.parse(fs.readFileSync(new URL("../data/daily-verses.json", import.meta.url), "utf8"));
const model = loadModel(raw, daily);

function addDays(iso, n) {
  var p = iso.split("-");
  var d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]));
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

test("card file is the 211-card approved set", function () {
  assert.equal(model.cards.length, 211);
  ["ms-04", "ms-05", "ms-06"].forEach(function (id) {
    var card = model.byId[id];
    assert.equal(card.playable, true);
    assert.equal(card.showExample, false);
    assert.equal(card.tag, null);
    assert.ok(card.en);
  });
});

test("reward ledger does not double-commit", function () {
  var first = applyXp(freshState(model), model, 250, "award:once");
  assert.equal(first.duplicate, false);
  assert.equal(first.state.xp, 250);
  assert.equal(first.state.level, 3);
  assert.equal(first.state.goldStars, 0);
  var ids = first.state.rewardQueue.map(function (q) { return q.id; });
  assert.equal(ids.filter(function (id) { return id === "gem-emerald"; }).length, 1);
  assert.equal(ids.filter(function (id) { return id === "cape-purple"; }).length, 1);
  var second = applyXp(first.state, model, 250, "award:once");
  assert.equal(second.duplicate, true);
  assert.equal(second.state.xp, 250);
  assert.equal(second.state.rewardQueue.length, first.state.rewardQueue.length);
});

test("answer commit is once and a miss changes nothing", function () {
  var state = freshState(model);
  var ok = commitCorrect(state, model, { ledgerId: "card:r:0", zone: "phonics", cardId: "ph-03" });
  assert.equal(ok.state.xp, 10);
  assert.equal(ok.state.pips, 1);
  assert.equal(ok.state.goldStars, 1);
  var again = commitCorrect(ok.state, model, { ledgerId: "card:r:0", zone: "phonics", cardId: "ph-03" });
  assert.equal(again.duplicate, true);
  assert.equal(again.state.xp, 10);
  assert.equal(again.state.pips, 1);
  assert.equal(again.state.goldStars, 1);
  var missed = applyMiss(ok.state);
  assert.equal(missed.red, false);
  assert.equal(missed.glow, "moonstone");
  assert.equal(missed.state.xp, ok.state.xp);
  assert.equal(missed.state.pips, ok.state.pips);
  assert.equal(missed.state.goldStars, ok.state.goldStars);
  assert.equal(missOutcome().red, false);
});

test("ten coins become one pip fill and stars stay a separate spend", function () {
  var state = freshState(model);
  for (var i = 0; i < 10; i++) {
    state = commitCorrect(state, model, { ledgerId: "card:r:" + i, zone: "phonics", cardId: "ph-03" }).state;
  }
  assert.equal(state.pips, 0);
  assert.equal(state.pipFills, 1);
  assert.equal(state.goldStars, 10);
  assert.equal(gemCount(state, model), 1);
  assert.equal(state.owned.indexOf("gem-emerald") >= 0, true);
  state.goldStars = 120;
  var bought = buyItem(state, model, "pet-bunny");
  assert.equal(bought.ok, true);
  assert.equal(bought.state.goldStars, 0);
  assert.equal(bought.state.pantryOwned.indexOf("pet-bunny") >= 0, true);
  var twice = buyItem(bought.state, model, "pet-bunny");
  assert.equal(twice.duplicate, true);
  assert.equal(twice.state.goldStars, 0);
  var broke = buyItem(bought.state, model, "pet-kitten");
  assert.equal(broke.error, "stars");
  assert.equal(broke.state.goldStars, 0);
});

test("gem unlocks do not spend stars or follow the daily gift counter", function () {
  var state = freshState(model);
  state.xp = 60;
  state = reconcile(state, model);
  assert.equal(state.goldStars, 0);
  assert.equal(gemCount(state, model), 1);
  assert.equal(state.owned.indexOf("gem-emerald") >= 0, true);
  var again = reconcile(state, model);
  assert.equal(again.owned.filter(function (id) { return id === "gem-emerald"; }).length, 1);
  var gift = commitGift(again, "2026-11-07");
  assert.equal(gift.state.giftGems, 1);
  assert.equal(gemCount(gift.state, model), 1);
  assert.equal(gift.state.goldStars, 0);
  var equipped = equipItem(gift.state, model, "cape-green");
  assert.equal(equipped.ok, true);
  assert.equal(equipped.state.xp, gift.state.xp);
  assert.equal(equipped.state.goldStars, gift.state.goldStars);
  assert.equal(equipped.state.owned.length, gift.state.owned.length);
});

test("region gates follow end guardians and bossless zones end at scene 5", function () {
  var state = freshState(model);
  assert.equal(zoneOpen(state, model, "phonics"), true);
  assert.equal(zoneOpen(state, model, "sight-words"), true);
  assert.equal(zoneOpen(state, model, "maxwell-says"), true);
  assert.equal(zoneOpen(state, model, "kitchen"), true);
  assert.equal(zoneOpen(state, model, "numbers"), false);
  assert.equal(zoneOpen(state, model, "colors-shapes"), false);
  assert.equal(zoneOpen(state, model, "baby-hospital"), false);
  assert.equal(zoneOpen(state, model, "soundDuel"), false);
  state = commitBoss(state, model, "phonics").state;
  assert.equal(regionOpenMap(state).r2, false);
  state = commitBoss(state, model, "sight-words").state;
  assert.equal(zoneOpen(state, model, "numbers"), true);
  assert.equal(zoneOpen(state, model, "colors-shapes"), true);
  assert.equal(zoneOpen(state, model, "baby-hospital"), false);
  state = commitBoss(state, model, "numbers").state;
  assert.equal(zoneOpen(state, model, "baby-hospital"), true);
  assert.equal(zoneOpen(state, model, "soundDuel"), false);
  state = commitBoss(state, model, "baby-hospital").state;
  assert.equal(zoneOpen(state, model, "soundDuel"), true);
  var again = commitBoss(state, model, "sight-words");
  assert.equal(again.duplicate, true);
  assert.equal(again.state.bossesWon.filter(function (z) { return z === "sight-words"; }).length, 1);
  assert.equal(again.state.scrolls.filter(function (s) { return s.id === "scroll:sight-words"; }).length, 1);
  var ms = buildRun(model, freshState(model), "maxwell-says", { rng: function () { return 0.2; } });
  assert.equal(ms.bossIds.length, 0);
  assert.equal(ms.scenes.length, 5);
  ms.scenes.forEach(function (scene) { assert.equal(scene.length, 5); });
  ms.index = ms.steps.length - 1;
  var done = advanceAfterReveal(ms, function () { return 0; });
  assert.equal(done.phase, "done");
  var ph = buildRun(model, freshState(model), "phonics", { rng: function () { return 0.2; } });
  assert.equal(ph.bossIds.length, 10);
  ph.index = ph.steps.length - 1;
  assert.equal(advanceAfterReveal(ph, function () { return 0; }).phase, "boss");
});

test("personal openers and real inn cards keep their approved order", function () {
  var ms = buildRun(model, freshState(model), "maxwell-says", { newVisit: false, rng: function () { return 0.3; } });
  var asks = ms.steps.filter(function (s) { return s.kind === "ask"; }).map(function (s) { return s.id; });
  assert.deepEqual(asks.slice(0, 3), ["ms-28", "ms-29", "ms-30"]);
  ["ms-04", "ms-05", "ms-06"].forEach(function (id) {
    assert.equal(ms.steps.some(function (s) { return s.id === id; }), true);
    assert.equal(model.byId[id].showExample, false);
  });
  var bh = buildRun(model, freshState(model), "baby-hospital", { newVisit: false, rng: function () { return 0.3; } });
  var bhAsks = bh.steps.filter(function (s) { return s.kind === "ask"; }).map(function (s) { return s.id; });
  assert.equal(bhAsks[0], "bh-30");
  assert.equal(bh.steps[0].id, "bh-30");
  assert.equal(bh.steps.some(function (s) { return model.byId[s.id].easy; }), true);
  assert.equal(showsEnglishAnswer(model.byId["ph-09"], "ask"), false);
});

test("verses stay exact free gifts and rest does not spend stars", function () {
  var state = freshState(model);
  state.goldStars = 7;
  var day = verseForDate(model, "2026-11-02");
  assert.equal(day.en, model.verses.weekly[0].en);
  assert.equal(day.th, model.verses.weekly[0].th);
  var later = verseForDate(model, addDays("2026-11-02", 40));
  assert.equal(later.en, model.verses.weekly[0].en);
  assert.equal(later.th, model.verses.weekly[0].th);
  var seen = commitVerseSeen(state, day, "2026-11-02");
  assert.equal(seen.state.goldStars, 7);
  assert.equal(seen.state.scrolls[0].en, day.en);
  assert.equal(seen.state.scrolls[0].th, day.th);
  assert.equal(seen.state.scrolls[0].cost, undefined);
  assert.equal(bannerKey({ kind: "verse" }), "verseGift");
  assert.notEqual(bannerKey({ kind: "verse" }), "rewardText");
  var rest = commitRestVerse(seen.state, model.verses.rest);
  assert.equal(rest.state.scrolls.some(function (s) { return s.id === "scroll:rest" && s.en === model.verses.rest.en && s.th === model.verses.rest.th; }), true);
  assert.equal(rest.state.goldStars, 7);
  assert.equal(shouldRest(3), true);
  assert.equal(shouldRest(2), false);
});

test("save continuity and corrupt backups", function () {
  var state = freshState(model);
  state = commitCorrect(state, model, { ledgerId: "card:r:1", zone: "phonics", cardId: "ph-01" }).state;
  state.run = { id: "run-phonics-0", phase: "reveal", index: 2, steps: [{ id: "ph-01" }] };
  var saved = JSON.parse(JSON.stringify(state));
  assert.equal(saved.xp, state.xp);
  assert.equal(saved.run.phase, "reveal");
  assert.equal(saved.run.index, 2);
  var resumed = JSON.parse(JSON.stringify(saved));
  assert.equal(resumed.xp, state.xp);
  var bad = prepareRestore(state, "{");
  assert.equal(bad.ok, false);
  assert.equal(bad.state, state);
  var empty = prepareRestore(state, "");
  assert.equal(empty.ok, false);
  assert.equal(empty.state.goldStars, state.goldStars);
  var partial = prepareRestore(state, { schema: 5020, xp: 1 });
  assert.equal(partial.ok, false);
  assert.equal(partial.state.xp, state.xp);
  var copy = JSON.parse(JSON.stringify(state));
  copy.xp = 40;
  copy.goldStars = 3;
  delete copy.giftGems;
  var ok = prepareRestore(state, copy);
  assert.equal(ok.ok, true);
  assert.equal(ok.state.xp, 40);
  assert.equal(ok.bak.xp, state.xp);
  assert.equal(ok.state.giftGems, state.giftGems);
  var finished = finishZoneRun(state, model, { id: "run-1", zone: "maxwell-says", regionId: "r3", steps: [] }, "2026-11-07");
  assert.equal(finished.state.run, null);
  assert.equal(finished.state.zoneRuns["maxwell-says"], 1);
  assert.equal(finished.state.ledger["scenes5:maxwell-says"], 1);
});

test("missing audio does not throw", async function () {
  var ok = await playClip("audio/maxwell-phonics.m4a", function () { throw new Error("missing"); });
  assert.equal(ok, false);
  var missing = await playClip("audio/nope.m4a", function () { return Promise.resolve({ ok: false }); });
  assert.equal(missing, false);
});

test("gear bonuses, weapon shop, and kneel follow the card file", function () {
  var fresh = freshState(model);
  assert.equal(bonusWordsFor(model, "sword-iron"), "Hint");
  assert.equal(gearBonuses(fresh, model).hint, 1);
  fresh.equipped.offHand = "shield-sunrise";
  var both = gearBonuses(fresh, model);
  assert.equal(both.hint, 1);
  assert.equal(both.retry, 1);
  var sun = freshState(model);
  sun.equipped.weapon = "sword-sunforged";
  var sunBag = gearBonuses(sun, model);
  assert.equal(sunBag.hint, 1);
  assert.equal(sunBag.retry, 1);
  assert.equal(sunBag.star, 1);
  var spoken = commitCorrect(sun, model, { ledgerId: "say:1", zone: "phonics", cardId: "ph-09", spoken: true, starBonus: sunBag.star });
  assert.equal(spoken.state.goldStars, 2);
  var sling = freshState(model);
  sling.equipped.weapon = "sling-shepherd";
  var streak = awardExtras({ rightRow: 2 }, gearBonuses(sling, model), false);
  assert.equal(streak.coinBonus, 1);
  var staff = freshState(model);
  staff.equipped.weapon = "staff-shepherd";
  var staffBag = gearBonuses(staff, model);
  assert.equal(staffBag.slow, true);
  assert.equal(staffBag.respell, true);
  var retryRun = { retriesLeft: 1, wasMiss: false, rightRow: 2 };
  var firstMiss = noteMiss(retryRun);
  assert.equal(firstMiss.retry, true);
  assert.equal(firstMiss.run.wasMiss, false);
  assert.equal(firstMiss.run.retriesLeft, 0);
  var secondMiss = noteMiss(firstMiss.run);
  assert.equal(secondMiss.retry, false);
  assert.equal(secondMiss.run.wasMiss, true);
  var buyer = freshState(model);
  buyer.xp = 910;
  buyer.level = 6;
  buyer.goldStars = 10;
  var poor = buyItem(buyer, model, "sword-crystal");
  assert.equal(poor.error, "stars");
  assert.equal(poor.state.goldStars, 10);
  buyer.goldStars = 45;
  var bought = buyItem(buyer, model, "sword-crystal");
  assert.equal(bought.ok, true);
  assert.equal(bought.state.goldStars, 0);
  assert.equal(bought.state.equipped.weapon, "sword-crystal");
  var again = buyItem(bought.state, model, "sword-crystal");
  assert.equal(again.duplicate, true);
  assert.equal(again.state.goldStars, 0);
  var closed = buyItem(buyer, model, "axe1-t2");
  assert.equal(closed.error, "closed");
  assert.equal(closed.state.goldStars, 45);
  var rows = shopRows(freshState(model), model);
  var sword = rows.filter(function (row) { return row.wt === "sword1"; })[0];
  assert.equal(sword.slots[2].silhouette, true);
  var knelt = beginKneel(freshState(model), model, "phonics");
  assert.equal(knelt.state.bossesWon.indexOf("phonics") >= 0, true);
  assert.equal(knelt.state.scrolls.filter(function (s) { return s.id === "scroll:phonics"; }).length, 1);
  assert.equal(knelt.state.rewardQueue[0].kind, "bossWin");
  assert.equal(knelt.state.rewardQueue[1].kind, "verse");
  var kneltAgain = beginKneel(knelt.state, model, "phonics");
  assert.equal(kneltAgain.duplicate, true);
  assert.equal(kneltAgain.state.scrolls.length, knelt.state.scrolls.length);
});

test("backup review order and sound duel schedule", function () {
  var queue = thaiReviewQueue(model);
  assert.deepEqual(queue.needsMaxwell, ["ms-04", "ms-05", "ms-06", "bh-30", "ms-28", "ms-29", "ms-30"]);
  assert.equal(queue.nurse[0], "bh-01");
  assert.equal(queue.nurse.length, 10);
  assert.equal(queue.thDef.indexOf("bh-01"), -1);
  assert.equal(queue.thDef.indexOf("ph-01") >= 0, true);
  var pairs = model.soundDuel.pairs;
  var endings = endingPairs(pairs);
  var gap = endingDiscrepancy(pairs);
  assert.equal(gap.resolved, true);
  assert.equal(gap.specCount, 6);
  assert.equal(gap.found.length, 8);
  assert.equal(gap.resolution.indexOf("normal pool") >= 0, true);
  assert.equal(endings.some(function (p) { return p.a === "light" && p.b === "right"; }), true);
  assert.equal(spellStep("bed", "", "b").got, "b");
  assert.equal(spellStep("bed", "be", "d").done, true);
  assert.equal(spellStep("bed", "", "x").correct, false);
  assert.equal(countPlates("three").length, 3);
  assert.equal(countPlates("three").indexOf("three") >= 0, true);
  assert.equal(pairs.filter(function (p) { return p.pics; }).length, 6);
  var plan = buildDuelSchedule(pairs);
  assert.equal(plan.rounds.length, 4);
  plan.rounds.forEach(function (round) { assert.equal(round.length, 8); });
  assert.equal(plan.recap.length, 10);
  var pictureIds = ["three/tree", "bath/bat", "mouth/mouse", "ship/sheep", "card/car", "bread/bed"];
  assert.deepEqual(plan.rounds[0].slice(0, 6).map(function (p) { return p.a + "/" + p.b; }), pictureIds);
  assert.equal(plan.rounds[0].filter(function (p) { return p.pics; }).length, 6);
  var seen = {};
  plan.rounds.concat([plan.recap]).forEach(function (round) { round.forEach(function (p) { seen[p.a + "/" + p.b] = 1; }); });
  pictureIds.forEach(function (id) { assert.equal(seen[id], 1); });
  endings.forEach(function (p) { assert.equal(seen[p.a + "/" + p.b], 1); });
  var state = freshState(model);
  state.pips = 4;
  state.goldStars = 3;
  var missed = applyMiss(state);
  assert.equal(missed.red, false);
  assert.equal(missed.state.pips, 4);
  assert.equal(missed.state.goldStars, 3);
  var round = applyXp(state, model, 30, "round:test");
  var round2 = applyXp(round.state, model, 30, "round:test");
  assert.equal(round.state.xp, 30);
  assert.equal(round2.duplicate, true);
  assert.equal(speakEnglish("bed", null), false);
  assert.equal(speakEnglish("bed", { speak: function () { throw new Error("no voice"); } }), false);
});

test("opener order and later runs reach starved cards", function () {
  var fresh = freshState(model);
  var ms = buildRun(model, fresh, "maxwell-says", { rng: function () { return 0.2; } });
  assert.deepEqual(ms.steps.slice(0, 3).map(function (s) { return s.id; }), ["ms-28", "ms-29", "ms-30"]);
  function cover(zone, limit) {
    var state = freshState(model);
    var hit = {};
    var n;
    for (n = 0; n < limit; n++) {
      var run = buildRun(model, state, zone, { rng: function () { return 0.25; } });
      run.steps.forEach(function (step) {
        hit[step.id] = 1;
        if (state.seen.indexOf(step.id) < 0) state.seen.push(step.id);
      });
    }
    return hit;
  }
  assert.equal(cover("maxwell-says", 6)["ms-31"], 1);
  assert.equal(cover("baby-hospital", 6)["bh-11"], 1);
  assert.equal(cover("kitchen", 8)["fd-38"], 1);
  assert.deepEqual(SETTLED_APPROVALS.needsMaxwell, model.raw.needsMaxwell);
  assert.equal(SETTLED_APPROVALS.choices, "t1315u all A");
  assert.equal(SETTLED_APPROVALS.thaiHold, "t1329u waived");
  var prompt = countPrompt(model.byId["nm-10"], model.raw.uiText);
  assert.equal(prompt.n, 3);
  assert.equal(prompt.en.indexOf("{"), -1);
  assert.equal(["cows", "baskets", "hats"].indexOf(prompt.thing) >= 0, true);
  assert.deepEqual(pendingMaxwell(model.raw.needsMaxwell, SETTLED_APPROVALS.needsMaxwell), []);
  var compared = fillBackupCompare(model.raw.uiText.backupCompare.en, 2, 3, 4, 5);
  assert.equal(compared, "Backup: level 2, 3 days · Now: level 4, 5 days");
  assert.equal(compared.indexOf("{"), -1);
  var tabs = trophiesByTab(model);
  var all = tabs.gems.concat(tabs.themes, tabs.titles, tabs.gear);
  assert.equal(all.length, 42);
  assert.equal(tabs.gems.length, 5);
  assert.equal(tabs.themes.length, 14);
  assert.equal(tabs.titles.length, 6);
  assert.equal(tabs.gear.length, 17);
});

test("level curve matches the spec knots", function () {
  assert.equal(xpToReach(2), 60);
  assert.equal(xpToReach(3), 250);
  assert.equal(levelForXp(0), 1);
  assert.equal(levelForXp(59), 1);
  assert.equal(levelForXp(60), 2);
  assert.equal(levelForXp(249), 2);
  assert.equal(levelForXp(250), 3);
  assert.equal(chooseZone(freshState(model), model, "r1"), "phonics");
  var turned = freshState(model);
  turned.lastZone = { r1: "phonics" };
  assert.equal(chooseZone(turned, model, "r1"), "sight-words");
});

test("a newer mirror beats a stale indexed record and does not award twice", function () {
  var stale = freshState(model);
  stale.schema = 5020;
  stale.rev = 1;
  stale.savedAt = 5000;
  stale.xp = 150;
  var fresh = freshState(model);
  fresh.schema = 5020;
  fresh.rev = 2;
  fresh.savedAt = 1000;
  fresh.xp = 180;
  fresh.ledger["round:race:1"] = 1;
  assert.equal(pickNewerState(stale, fresh).xp, 180);
  assert.equal(pickNewerState(fresh, stale).xp, 180);
  var awarded = applyXp(pickNewerState(stale, fresh), model, 30, "round:race:1");
  assert.equal(awarded.state.xp, 180);
  var olderMirror = freshState(model);
  olderMirror.schema = 5020;
  olderMirror.rev = 4;
  olderMirror.xp = 111;
  var newerIndex = freshState(model);
  newerIndex.schema = 5020;
  newerIndex.rev = 5;
  newerIndex.xp = 999;
  newerIndex.ledger["round:race:1"] = 1;
  assert.equal(pickNewerState(newerIndex, olderMirror).xp, 999);
  assert.equal(applyXp(pickNewerState(newerIndex, olderMirror), model, 30, "round:race:1").state.xp, 999);
  var unstamped = freshState(model);
  unstamped.schema = 5020;
  unstamped.xp = 10;
  assert.equal(pickNewerState(unstamped, fresh).xp, 180);
  assert.equal(pickNewerState(null, fresh).xp, 180);
  assert.equal(pickNewerState(stale, null).xp, 150);
});
