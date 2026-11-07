/* Nancy's Adventure English — pure rules. No DOM, no network. */

export var SCHEMA = 5020;
export var PRIORITY_IDS = ["bh-30", "ms-28", "ms-29", "ms-30"];
export var SETTLED_APPROVALS = {
  needsMaxwell: ["ms-04", "ms-05", "ms-06", "bh-30", "ms-28", "ms-29", "ms-30"],
  choices: "t1315u all A",
  thaiHold: "t1329u waived"
};
var DAY_ONE = { "maxwell-says": 1, kitchen: 1 };
var REGION_GATE = { "sight-words": "r2", numbers: "r3", "baby-hospital": "r4" };
var TAP_EXCLUDE = {
  "ph-02": 1, "ph-07": 1, "ph-08": 1, "ph-11": 1, "ph-17": 1, "ph-21": 1, "ph-24": 1,
  "cs-22": 1, "cs-23": 1, "cs-24": 1, "sw-15": 1, "sw-18": 1, "sw-19": 1, "sw-24": 1
};
var NUMBER_N = { two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 };
var REQUIRED_KEYS = ["xp", "level", "pipFills", "goldStars", "pantryOwned", "rightByZone", "bossesWon", "owned", "equipped", "ledger", "rewardQueue", "scrolls", "seen", "run", "pips", "streak", "settings"];

export function clone(v) {
  return JSON.parse(JSON.stringify(v));
}

export function dayDiff(a, b) {
  function p(s) {
    var x = String(s || "").split("-");
    return Date.UTC(+x[0], (+x[1] || 1) - 1, +x[2] || 1);
  }
  return Math.round((p(b) - p(a)) / 86400000);
}

export function mulberry32(seed) {
  var a = seed >>> 0;
  return function () {
    a = (a + 0x6D2B79F5) | 0;
    var t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function shuffle(list, rng) {
  var a = list.slice();
  var rand = rng || Math.random;
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(rand() * (i + 1));
    var tmp = a[i];
    a[i] = a[j];
    a[j] = tmp;
  }
  return a;
}

function wordCount(en) {
  return String(en || "").trim().split(/\s+/).filter(Boolean).length;
}

function hintOf(card) {
  var en = card.en || "";
  var h = card.hint;
  if (Array.isArray(h)) {
    return { letters: h[0] || "", sound: h[1] || "", word: h[2] || en };
  }
  if (typeof h === "string") {
    var letters = "";
    if (en) {
      letters = en.charAt(0);
      for (var i = 1; i < en.length; i++) {
        letters += /[A-Za-z]/.test(en.charAt(i)) ? "_" : en.charAt(i);
      }
    }
    return { letters: letters, sound: h, word: en };
  }
  return { letters: "", sound: "", word: en };
}

function choiceList(raw) {
  if (!raw) return [];
  var out = [];
  for (var i = 0; i < raw.length; i++) {
    var c = raw[i];
    if (typeof c === "string") out.push({ en: c });
    else if (c && typeof c === "object") out.push(c);
  }
  return out;
}

export function loadModel(raw, daily) {
  var zones = raw.zones || [];
  var byPrefix = {};
  zones.forEach(function (z) {
    String(z.prefix || "").split(/\s+/).forEach(function (p) {
      if (p) byPrefix[p] = z.key;
    });
  });
  var meta = raw.meta || {};
  var defaults = meta.cardDefaults || {};
  var typeByZone = meta.typeByZone || {};
  var modeByType = meta.modeByType || {};
  var cards = (raw.cards || []).map(function (rawCard, index) {
    var pre = String(rawCard.id || "").split("-")[0];
    var zone = byPrefix[pre] || "";
    var type = rawCard.type || typeByZone[zone] || defaults.type || "picture";
    var mode = rawCard.mode || modeByType[type] || (type === "picture" ? "picture-recall" : "");
    var fill = rawCard.fill != null ? !!rawCard.fill : !!defaults.fill;
    var card = {
      id: rawCard.id,
      order: index,
      zone: zone,
      type: type,
      mode: mode,
      en: rawCard.en || "",
      th: rawCard.th || "",
      thDef: rawCard.thDef || "",
      respell: rawCard.respell || "",
      pic: rawCard.pic == null ? null : rawCard.pic,
      choices: choiceList(rawCard.choices != null ? rawCard.choices : defaults.choices),
      answer: rawCard.answer != null ? rawCard.answer : (type === "picture" || type === "server-talk" ? rawCard.en : null),
      hint: hintOf(rawCard),
      trap: rawCard.trap != null ? rawCard.trap : (defaults.trap == null ? null : defaults.trap),
      trapNote: rawCard.trapNote || "",
      fill: fill,
      tag: rawCard.tag != null ? rawCard.tag : (defaults.tag == null ? null : defaults.tag),
      easy: rawCard.easy != null ? !!rawCard.easy : !!defaults.easy,
      faith: rawCard.faith != null ? !!rawCard.faith : !!defaults.faith,
      personal: rawCard.personal != null ? !!rawCard.personal : !!defaults.personal,
      prompts: rawCard.prompts || null,
      reply: rawCard.reply || null,
      syl: rawCard.syl || "",
      nursePhrase: rawCard.nursePhrase != null ? !!rawCard.nursePhrase : !!defaults.nursePhrase
    };
    card.showExample = card.tag === "Example";
    card.playable = !(card.fill && !String(card.en || "").trim());
    return card;
  });
  var byId = {};
  cards.forEach(function (c) { byId[c.id] = c; });
  var zoneByKey = {};
  zones.forEach(function (z) { zoneByKey[z.key] = z; });
  var regionOf = {};
  (raw.mapLayout.regions || []).forEach(function (r) {
    (r.zones || []).forEach(function (z) { regionOf[z] = r.id; });
  });
  return {
    raw: raw,
    daily: daily || { verses: [] },
    cards: cards,
    byId: byId,
    zones: zones,
    zoneByKey: zoneByKey,
    regionOf: regionOf,
    regions: raw.mapLayout.regions || [],
    ui: raw.uiText,
    trophies: raw.trophies || [],
    trophyRules: raw.trophyRules || {},
    pantry: raw.pantry || { earn: { rightAnswer: 1, runDone: 5 }, items: [] },
    verses: raw.verses,
    jesusWords: raw.jesusWords || [],
    jesusWordsFallback: raw.jesusWordsFallback || [],
    encouragement: raw.encouragement || [],
    rewardText: raw.rewardText,
    wrongText: raw.wrongText,
    welcomeBack: raw.welcomeBack,
    restScreen: raw.restScreen,
    gotItText: raw.gotItText,
    meta: meta,
    soundDuel: raw.soundDuel || { pairs: [] },
    picPlan: raw.picPlan || {}
  };
}

export function xpToReach(level) {
  if (level <= 1) return 0;
  if (level === 2) return 60;
  if (level === 3) return 250;
  var total = 250;
  for (var k = 4; k <= level; k++) total += 100 + 60 * (k - 3);
  return total;
}

export function levelForXp(xp) {
  var level = 1;
  var n = xp || 0;
  for (var L = 2; L <= 20; L++) {
    if (n >= xpToReach(L)) level = L;
  }
  return level;
}

export function freshState(model) {
  var owned = [];
  var ledger = {};
  (model.trophies || []).forEach(function (t) {
    if (t.unlock && t.unlock.type === "start") {
      owned.push(t.id);
      ledger["unlock:" + t.id] = 1;
    }
  });
  var equipped = {};
  var defs = (model.trophyRules && model.trophyRules.defaults) || {};
  Object.keys(defs).forEach(function (slot) {
    if (defs[slot]) equipped[slot] = defs[slot];
  });
  return {
    schema: SCHEMA,
    xp: 0,
    level: 1,
    pipFills: 0,
    goldStars: 0,
    pantryOwned: [],
    rightByZone: {},
    bossesWon: [],
    owned: owned,
    equipped: equipped,
    ledger: ledger,
    rewardQueue: [],
    scrolls: [],
    seen: [],
    run: null,
    pips: 0,
    streak: { n: 0, last: null },
    giftGems: 0,
    hero: "sam",
    zoneRuns: {},
    settings: { slowMode: false, restWeeks: false },
    spoken: 0,
    regionsDone: [],
    lastZone: {}
  };
}

export function gemCount(state, model) {
  var n = 0;
  (model.trophies || []).forEach(function (t) {
    if (t.cat === "gems" && state.owned.indexOf(t.id) >= 0) n += 1;
  });
  return n;
}

export function missOutcome() {
  return { xp: 0, pips: 0, stars: 0, glow: "moonstone", red: false, text: "wrongText" };
}

export function applyMiss(state) {
  return { state: clone(state), xp: 0, pips: 0, stars: 0, glow: "moonstone", red: false, text: "wrongText" };
}

function goalMet(t, state) {
  var u = t.unlock;
  if (!u || !u.type) return false;
  if (u.type === "start") return true;
  if (u.type === "level") return levelForXp(state.xp) >= u.n;
  if (u.type === "pipFills") return (state.pipFills || 0) >= u.n;
  if (u.type === "bossesWon") return (state.bossesWon || []).length >= u.n;
  if (u.type === "zoneRight") return (state.rightByZone[u.zone] || 0) >= u.n;
  if (u.type === "guardian") return (state.bossesWon || []).indexOf(u.zone) >= 0;
  if (u.type === "secret") {
    return (state.regionsDone || []).length >= (u.regions || 4) && (state.spoken || 0) >= (u.spokenGotIt || 100);
  }
  return false;
}

function tierLevel(model, tier) {
  var table = (model.meta && model.meta.weaponTiers) || { "1": 3, "2": 6, "3": 10 };
  return +table[String(tier)] || 99;
}

function rowOpen(state, wt) {
  if (wt === "sword1" || wt === "sword2") return true;
  if (wt === "axe1") return (state.bossesWon || []).indexOf("sight-words") >= 0;
  if (wt === "mace1") return (state.bossesWon || []).indexOf("numbers") >= 0;
  return false;
}

var FREE_TIER1 = ["sling-shepherd", "shield-sunrise", "axe-oak", "hammer-builder"];

function checkTrophies(state, model) {
  var queued = [];
  (model.trophies || []).forEach(function (t) {
    if (!goalMet(t, state)) return;
    var id = "unlock:" + t.id;
    if (state.ledger[id]) return;
    state.ledger[id] = 1;
    if (state.owned.indexOf(t.id) < 0) state.owned.push(t.id);
    queued.push({ kind: t.wt ? "weaponNew" : "trophy", id: t.id, en: t.en, th: t.th || t.thGloss || "" });
  });
  if (levelForXp(state.xp) >= tierLevel(model, 1)) {
    FREE_TIER1.forEach(function (wid) {
      var t = null;
      (model.trophies || []).some(function (x) { if (x.id === wid) { t = x; return true; } return false; });
      if (!t || !t.wt || !rowOpen(state, t.wt)) return;
      var id = "unlock:" + wid;
      if (state.ledger[id]) return;
      state.ledger[id] = 1;
      if (state.owned.indexOf(wid) < 0) state.owned.push(wid);
      queued.push({ kind: "weaponNew", id: wid, en: t.en, th: t.thGloss || "" });
    });
  }
  return queued;
}

function rememberCard(state, cardId) {
  if (!cardId) return;
  state.seen = (state.seen || []).filter(function (id) { return id !== cardId; });
  state.seen.push(cardId);
}

function addXp(state, model, amount) {
  var before = state.xp || 0;
  var gain = amount > 0 ? amount : 0;
  state.xp = before + gain;
  var startL = levelForXp(before);
  var endL = levelForXp(state.xp);
  if (endL > 20) endL = 20;
  state.level = endL;
  for (var L = startL + 1; L <= endL; L++) {
    var lid = "level:" + L;
    if (!state.ledger[lid]) state.ledger[lid] = 1;
  }
  return checkTrophies(state, model);
}

export function applyXp(state, model, amount, ledgerId) {
  var next = clone(state);
  if (ledgerId) {
    if (next.ledger[ledgerId]) return { state: next, duplicate: true, queued: [] };
    next.ledger[ledgerId] = 1;
  }
  var queued = addXp(next, model, amount);
  queued.forEach(function (q) { next.rewardQueue.push(q); });
  return { state: next, duplicate: false, queued: queued };
}

export function commitCorrect(state, model, opts) {
  opts = opts || {};
  var next = clone(state);
  var ledgerId = opts.ledgerId;
  if (!ledgerId) ledgerId = "card:loose:" + (opts.cardId || "x");
  if (next.ledger[ledgerId]) return { state: next, duplicate: true, pipGlow: false };
  next.ledger[ledgerId] = 1;
  var earn = (model.pantry && model.pantry.earn && model.pantry.earn.rightAnswer) || 1;
  next.goldStars = (next.goldStars || 0) + earn + (opts.starBonus || 0);
  var zone = opts.zone || "";
  if (zone) next.rightByZone[zone] = (next.rightByZone[zone] || 0) + 1;
  var coins = 1 + (opts.coinBonus || 0);
  next.pips = (next.pips || 0) + coins;
  var pipGlow = false;
  while (next.pips >= 10) {
    next.pips -= 10;
    next.pipFills = (next.pipFills || 0) + 1;
    var pid = "pips:" + next.pipFills;
    if (!next.ledger[pid]) next.ledger[pid] = 1;
    pipGlow = true;
  }
  rememberCard(next, opts.cardId);
  if (opts.spoken) next.spoken = (next.spoken || 0) + 1;
  var queued = addXp(next, model, opts.xp == null ? 10 : opts.xp);
  queued.forEach(function (q) { next.rewardQueue.push(q); });
  return { state: next, duplicate: false, pipGlow: pipGlow, queued: queued };
}

export function commitBoss(state, model, zoneKey) {
  var next = clone(state);
  var id = "boss:" + zoneKey;
  if (next.ledger[id]) return { state: next, duplicate: true };
  next.ledger[id] = 1;
  if (next.bossesWon.indexOf(zoneKey) < 0) next.bossesWon.push(zoneKey);
  var zone = model.zoneByKey[zoneKey];
  var scroll = zone && zone.boss && zone.boss.scroll;
  if (scroll) {
    var sid = "scroll:" + zoneKey;
    if (!next.scrolls.some(function (s) { return s.id === sid; })) {
      next.scrolls.push({
        id: sid,
        kind: "boss",
        ref: scroll.ref,
        en: scroll.en,
        th: scroll.th,
        enSource: scroll.enSource,
        thSource: scroll.thSource
      });
    }
    next.rewardQueue.push({ kind: "bossWin", zone: zoneKey });
    next.rewardQueue.push({ kind: "verse", gift: true, scrollId: sid });
  }
  var gate = REGION_GATE[zoneKey];
  if (gate && !next.ledger["region:" + gate]) {
    next.ledger["region:" + gate] = 1;
    next.rewardQueue.push({ kind: "region", regionId: gate });
  }
  checkTrophies(next, model).forEach(function (q) { next.rewardQueue.push(q); });
  return { state: next, duplicate: false };
}

export function commitVerseSeen(state, verse, dateStr) {
  var next = clone(state);
  var id = "verse:" + dateStr;
  if (next.ledger[id]) return { state: next, duplicate: true };
  next.ledger[id] = 1;
  next.scrolls.push({
    id: id,
    kind: "daily",
    ref: verse.ref,
    en: verse.en,
    th: verse.th,
    enSource: verse.enSource || "ESV",
    thSource: verse.thSource || "THSV11"
  });
  return { state: next, duplicate: false };
}

export function commitRestVerse(state, verse) {
  var next = clone(state);
  var id = "scroll:rest";
  if (next.scrolls.some(function (s) { return s.id === id; })) return { state: next, duplicate: true };
  next.scrolls.push({
    id: id,
    kind: "rest",
    ref: verse.ref,
    en: verse.en,
    th: verse.th,
    enSource: verse.enSource,
    thSource: verse.thSource
  });
  next.ledger["verse:rest"] = 1;
  return { state: next, duplicate: false };
}

export function commitGift(state, dateStr) {
  var next = clone(state);
  var id = "gift:" + dateStr;
  if (next.ledger[id]) return { state: next, duplicate: true };
  next.ledger[id] = 1;
  next.giftGems = (next.giftGems || 0) + 1;
  return { state: next, duplicate: false };
}

export function bannerKey(entry) {
  if (!entry) return "rewardText";
  if (entry.kind === "verse" || entry.kind === "daily" || entry.kind === "restVerse") return "verseGift";
  if (entry.kind === "region") return "regionOpen";
  return "rewardText";
}

export function reconcile(state, model) {
  var next = clone(state);
  if (next.schema !== SCHEMA) return freshState(model);
  var seen = {};
  var known = {};
  (model.trophies || []).forEach(function (t) { known[t.id] = 1; });
  ((model.pantry && model.pantry.items) || []).forEach(function (t) { known[t.id] = 1; });
  next.owned = (next.owned || []).filter(function (id) {
    if (seen[id]) return false;
    seen[id] = 1;
    if (known[id]) return true;
    return /-t[123]$/.test(id);
  });
  var defs = (model.trophyRules && model.trophyRules.defaults) || {};
  Object.keys(next.equipped || {}).forEach(function (slot) {
    var id = next.equipped[slot];
    if (!id) return;
    var owned = next.owned.indexOf(id) >= 0 || (next.pantryOwned || []).indexOf(id) >= 0;
    if (!owned && defs[slot] !== id) next.equipped[slot] = defs[slot] || null;
  });
  checkTrophies(next, model).forEach(function (q) { next.rewardQueue.push(q); });
  next.level = levelForXp(next.xp);
  return next;
}

export function regionOpenMap(state) {
  var bosses = state.bossesWon || [];
  return {
    r1: true,
    r2: bosses.indexOf("sight-words") >= 0,
    r3: bosses.indexOf("numbers") >= 0,
    r4: bosses.indexOf("baby-hospital") >= 0
  };
}

export function zoneOpen(state, model, zoneKey) {
  if (DAY_ONE[zoneKey]) return true;
  var region = model.regionOf[zoneKey];
  if (!region) return false;
  return !!regionOpenMap(state)[region];
}

export function chooseZone(state, model, regionId) {
  var region = null;
  (model.regions || []).some(function (r) { if (r.id === regionId) { region = r; return true; } return false; });
  if (!region) return null;
  var open = (region.zones || []).filter(function (z) {
    return z !== "soundDuel" && zoneOpen(state, model, z);
  });
  if (!open.length) return null;
  var last = state.lastZone && state.lastZone[regionId];
  var pool = open.slice();
  if (pool.length > 1 && last) pool = pool.filter(function (z) { return z !== last; });
  var best = pool[0];
  var bestN = (state.zoneRuns && state.zoneRuns[best]) || 0;
  for (var i = 1; i < pool.length; i++) {
    var n = (state.zoneRuns && state.zoneRuns[pool[i]]) || 0;
    if (n < bestN) { best = pool[i]; bestN = n; }
  }
  return best;
}

export function playableCards(model, zoneKey) {
  return model.cards.filter(function (c) { return c.zone === zoneKey && c.playable; });
}

function priorityRank(id) {
  var i = PRIORITY_IDS.indexOf(id);
  return i < 0 ? 100 : i;
}

function isSay(c) { return c.type === "say-it"; }
function isChoice(c) {
  return c.type !== "say-it" && c.type !== "two-answer" && (c.choices || []).length > 0;
}

export function buildRun(model, state, zoneKey, opts) {
  opts = opts || {};
  var rng = opts.rng || mulberry32(1);
  var pool = playableCards(model, zoneKey);
  var byId = {};
  pool.forEach(function (c) { byId[c.id] = c; });
  var used = {};
  var faith = 0;
  function canTake(c) {
    if (!c || used[c.id]) return false;
    if (c.faith && faith >= 2) return false;
    return true;
  }
  function take(c) {
    if (!canTake(c)) return false;
    used[c.id] = 1;
    if (c.faith) faith += 1;
    return true;
  }
  var ordered = [];
  var easy = pool.filter(function (c) { return c.easy; });
  if (easy.length && take(easy[0])) ordered.push(easy[0]);
  if (opts.newVisit && opts.reviewQueue) {
    var added = 0;
    for (var i = 0; i < opts.reviewQueue.length && added < 2; i++) {
      var rc = byId[opts.reviewQueue[i]];
      if (!rc || rc.type === "say-it" || rc.type === "two-answer") continue;
      if (rc.mode !== "picture-recall" && rc.type !== "picture") continue;
      if (take(rc)) { ordered.push(rc); added += 1; }
    }
  }
  var personals = pool.filter(function (c) { return c.personal; }).slice().sort(function (a, b) {
    var d = priorityRank(a.id) - priorityRank(b.id);
    if (d) return d;
    return a.order - b.order;
  });
  personals.forEach(function (c) { if (take(c)) ordered.push(c); });
  var seenPos = {};
  (state.seen || []).forEach(function (id, idx) { seenPos[id] = idx; });
  var zoneSeen = pool.filter(function (c) { return seenPos[c.id] != null; }).length;
  var neverCap = zoneSeen >= 7 ? 8 : 100000;
  var neverUsed = ordered.filter(function (c) { return seenPos[c.id] == null; }).length;
  var rest = pool.filter(function (c) { return !used[c.id]; });
  rest.sort(function (a, b) {
    var aN = seenPos[a.id] == null;
    var bN = seenPos[b.id] == null;
    if (neverUsed >= neverCap) {
      if (aN !== bN) return aN ? 1 : -1;
      if (!aN && !bN) return seenPos[a.id] - seenPos[b.id];
    } else if (aN !== bN) return aN ? -1 : 1;
    else if (aN && bN) return wordCount(a.en) - wordCount(b.en);
    else return seenPos[a.id] - seenPos[b.id];
    return a.order - b.order;
  });
  rest.forEach(function (c) {
    if (seenPos[c.id] == null && neverUsed >= neverCap) return;
    if (take(c)) {
      ordered.push(c);
      if (seenPos[c.id] == null) neverUsed += 1;
    }
  });
  var outings = (model.meta && model.meta.outings) || [];
  var outing = null;
  for (var o = 0; o < outings.length; o++) {
    if (byId[outings[o]]) { outing = byId[outings[o]]; break; }
  }
  if (outing && !used[outing.id] && take(outing)) {
    var at = ordered.length && ordered[0].easy ? 1 : 0;
    ordered.splice(at, 0, outing);
  }
  for (var s = 3; s < ordered.length; s++) {
    if (isSay(ordered[s]) && isSay(ordered[s - 1]) && isSay(ordered[s - 2]) && isSay(ordered[s - 3])) {
      var j = s + 1;
      while (j < ordered.length && !isChoice(ordered[j])) j += 1;
      if (j < ordered.length) {
        var swap = ordered[s];
        ordered[s] = ordered[j];
        ordered[j] = swap;
      }
    }
  }
  var unseenFaith = pool.filter(function (c) { return c.faith && !used[c.id] && seenPos[c.id] == null; });
  if (unseenFaith.length && faith >= 2) {
    var swapAt = -1;
    var fi;
    for (fi = ordered.length - 1; fi >= 0; fi--) {
      if (ordered[fi].faith && seenPos[ordered[fi].id] != null && priorityRank(ordered[fi].id) === 100) {
        swapAt = fi;
        break;
      }
    }
    if (swapAt >= 0) {
      var droppedFaith = ordered.splice(swapAt, 1)[0];
      delete used[droppedFaith.id];
      faith -= 1;
      unseenFaith.sort(function (a, b) { return a.order - b.order; });
      if (take(unseenFaith[0])) ordered.push(unseenFaith[0]);
    }
  }
  var pics = ordered.filter(function (c) { return !!c.pic; });
  var nopics = ordered.filter(function (c) { return !c.pic; });
  nopics.sort(function (a, b) {
    var aU = seenPos[a.id] == null ? 0 : 1;
    var bU = seenPos[b.id] == null ? 0 : 1;
    if (aU !== bU) return aU - bU;
    var d = priorityRank(a.id) - priorityRank(b.id);
    if (d) return d;
    return a.order - b.order;
  });
  var scenes = [[], [], [], [], []];
  var pi = 0;
  for (var sc = 0; sc < 5; sc++) {
    while (scenes[sc].length < 5 && pi < pics.length) {
      var card = pics[pi++];
      if (scenes[sc].some(function (x) { return x.id === card.id; })) continue;
      scenes[sc].push(card);
    }
  }
  function ago(c) { return seenPos[c.id] == null ? 9999 : seenPos[c.id]; }
  for (var sc2 = 0; sc2 < 5; sc2++) {
    var guard = 0;
    while (scenes[sc2].length < 5 && guard < 80) {
      guard += 1;
      var exclude = {};
      scenes[sc2].forEach(function (c) { exclude[c.id] = 1; });
      var prev = sc2 > 0 ? scenes[sc2 - 1].map(function (c) { return c.id; }) : [];
      var candidates = pics.filter(function (c) { return !exclude[c.id] && !c.faith; });
      if (!candidates.length) candidates = pics.filter(function (c) { return !exclude[c.id]; });
      if (scenes[sc2].length === 0 && prev.length) {
        var filtered = candidates.filter(function (c) { return prev.indexOf(c.id) < 0; });
        if (filtered.length) candidates = filtered;
      }
      candidates.sort(function (a, b) { return ago(a) - ago(b); });
      if (!candidates.length) break;
      scenes[sc2].push(candidates[0]);
    }
  }
  var steps = [];
  var ni = 0;
  var leadIds = {};
  nopics.forEach(function (c) {
    if (steps.length >= 3) return;
    if (priorityRank(c.id) < 100 && seenPos[c.id] == null) {
      leadIds[c.id] = 1;
      steps.push({
        id: c.id,
        kind: "ask",
        scene: null,
        listen: false,
        choices: shuffle((c.choices || []).map(function (ch) { return ch.en; }), rng)
      });
    }
  });
  var restNopics = nopics.filter(function (c) { return !leadIds[c.id]; });
  for (var sc3 = 0; sc3 < 5; sc3++) {
    scenes[sc3].forEach(function (c, idx) {
      var choices = shuffle(c.choices.map(function (ch) { return ch.en; }), rng);
      steps.push({
        id: c.id,
        kind: "scene",
        scene: sc3,
        listen: idx === 2 || idx === 4,
        choices: choices
      });
    });
    if (sc3 < 4 && ni < restNopics.length) {
      var ncard = restNopics[ni++];
      steps.push({
        id: ncard.id,
        kind: "ask",
        scene: null,
        listen: false,
        choices: shuffle(ncard.choices.map(function (ch) { return ch.en; }), rng)
      });
    }
  }
  var letterSet = false;
  var countSet = false;
  var sizeSet = false;
  steps.forEach(function (step, idx) {
    if (idx === 0) return;
    var c = byId[step.id] || model.byId[step.id];
    if (!c) return;
    if (!letterSet && zoneKey === "phonics" && step.kind === "scene" && /^[a-z]{3,5}$/.test(c.en || "")) {
      step.kind = "letter";
      step.listen = false;
      letterSet = true;
    } else if (!countSet && zoneKey === "numbers" && step.kind === "scene" && NUMBER_N[String(c.en || "").toLowerCase()]) {
      step.kind = "count";
      step.listen = false;
      step.countN = NUMBER_N[String(c.en).toLowerCase()];
      countSet = true;
    } else if (!sizeSet && zoneKey === "colors-shapes" && (c.id === "cs-23" || c.id === "cs-24")) {
      step.kind = "size";
      step.listen = false;
      sizeSet = true;
    }
  });
  var zone = model.zoneByKey[zoneKey];
  var bossIds = zone && zone.boss && zone.boss.cards ? zone.boss.cards.slice() : [];
  var runs = (state.zoneRuns && state.zoneRuns[zoneKey]) || 0;
  return {
    id: "run-" + zoneKey + "-" + runs,
    zone: zoneKey,
    regionId: model.regionOf[zoneKey] || "",
    tod: (runs % 5) + 1,
    steps: steps,
    scenes: scenes.map(function (sc) { return sc.map(function (c) { return c.id; }); }),
    index: 0,
    phase: "ask",
    bossIds: bossIds,
    bossIndex: 0,
    bossCleared: {},
    missReturns: {},
    wasMiss: false,
    rightRow: 0,
    retriesLeft: 0
  };
}

export function advanceAfterReveal(run, rng) {
  var next = clone(run);
  var rand = rng || Math.random;
  var step = next.steps[next.index];
  if (next.wasMiss && step && step.kind === "ask") {
    var times = next.missReturns[step.id] || 0;
    if (times < 2) {
      var gap = 3 + Math.floor(rand() * 3);
      var insertAt = Math.min(next.steps.length, next.index + 1 + gap);
      next.steps.splice(insertAt, 0, { id: step.id, kind: "ask", scene: null, listen: false, choices: step.choices || [] });
      next.missReturns[step.id] = times + 1;
    }
  }
  next.wasMiss = false;
  next.index += 1;
  if (next.index >= next.steps.length) next.phase = next.bossIds && next.bossIds.length ? "boss" : "done";
  else next.phase = "ask";
  return next;
}

export function finishZoneRun(state, model, run, dateStr) {
  var next = clone(state);
  var zoneKey = run.zone;
  var lid = "run:" + dateStr + ":" + zoneKey + ":" + run.id;
  if (!next.ledger[lid]) {
    next.ledger[lid] = 1;
    var bonus = (model.pantry && model.pantry.earn && model.pantry.earn.runDone) || 5;
    next.goldStars = (next.goldStars || 0) + bonus;
  }
  next.zoneRuns[zoneKey] = (next.zoneRuns[zoneKey] || 0) + 1;
  next.ledger["scenes5:" + zoneKey] = 1;
  if (!next.lastZone) next.lastZone = {};
  if (run.regionId) {
    next.lastZone[run.regionId] = zoneKey;
    if (next.regionsDone.indexOf(run.regionId) < 0) next.regionsDone.push(run.regionId);
  }
  next.run = null;
  checkTrophies(next, model).forEach(function (q) { next.rewardQueue.push(q); });
  return { state: next };
}

export function shouldRest(finishedSinceOpen) {
  return finishedSinceOpen > 0 && finishedSinceOpen % 3 === 0;
}

export function showsEnglishAnswer(card, kind) {
  if (!card) return false;
  if (kind === "boss") return false;
  if (kind === "ask" && (card.mode === "picture-recall" || card.type === "picture")) return false;
  return true;
}

export function promptFor(card, ui, listen) {
  if (listen) return { en: (ui.listenFind && ui.listenFind.en) || "", th: (ui.listenFind && ui.listenFind.th) || "", hidesAnswer: true };
  var en = card.en || "";
  var words = en.split(/\s+/).filter(Boolean);
  var lower = words.every(function (w) { return w === w.toLowerCase(); });
  var clean = en && words.length >= 1 && words.length <= 3 && lower && !/[.,?!]/.test(en) && en.indexOf("a ") !== 0;
  if (!card.pic || !clean || TAP_EXCLUDE[card.id] || card.mode !== "picture-recall") {
    return { en: card.en, th: card.thDef || card.th, hidesAnswer: false };
  }
  var template = (ui.tapPrompt && ui.tapPrompt.en) || "Can you find the {word}?";
  var th = (ui.tapPrompt && ui.tapPrompt.th) || "";
  var n = +(String(card.id).split("-")[1] || 0);
  if (card.id.indexOf("cs-") === 0 && n >= 8 && n <= 15) template = template.replace(" the ", " ");
  return { en: template.split("{word}").join(en), th: th.split("{word}").join(en), hidesAnswer: false };
}

export function verseForDate(model, dateStr) {
  var start = model.verses.weeklyStart;
  var d = dayDiff(start, dateStr);
  var index = ((d % 40) + 40) % 40;
  if (index < 10) {
    var w = model.verses.weekly[index];
    return {
      index: index,
      ref: w.ref,
      en: w.en,
      th: w.th,
      enSource: w.enSource,
      thSource: w.thSource,
      enGloss: w.enGloss || "",
      thGloss: w.thGloss || ""
    };
  }
  var v = (model.daily.verses || [])[index - 10] || {};
  return {
    index: index,
    ref: v.ref,
    en: v.en,
    th: v.th,
    enSource: "ESV",
    thSource: "THSV11",
    enGloss: v.enGloss || "",
    thGloss: v.thGloss || ""
  };
}

export function rollDay(state, today) {
  var next = clone(state);
  if (!next.streak) next.streak = { n: 0, last: null };
  var id = "day:" + today;
  if (next.ledger[id]) return { state: next, missed: false, first: false };
  var missed = false;
  if (next.streak.last && next.streak.last !== today) {
    var diff = dayDiff(next.streak.last, today);
    if (diff > 1) missed = true;
  }
  next.ledger[id] = 1;
  next.streak.n = (next.streak.n || 0) + 1;
  next.streak.last = today;
  return { state: next, missed: missed, first: true };
}

export function validateBackup(input, current) {
  var data = input;
  if (typeof input === "string") {
    if (!String(input).trim()) return { ok: false, reason: "empty", state: current };
    try { data = JSON.parse(input); } catch (e) { return { ok: false, reason: "json", state: current }; }
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) return { ok: false, reason: "type", state: current };
  if (data.schema !== SCHEMA) return { ok: false, reason: "schema", state: current };
  for (var i = 0; i < REQUIRED_KEYS.length; i++) {
    if (!Object.prototype.hasOwnProperty.call(data, REQUIRED_KEYS[i])) {
      return { ok: false, reason: "missing:" + REQUIRED_KEYS[i], state: current };
    }
  }
  var next = clone(data);
  if (!Object.prototype.hasOwnProperty.call(data, "giftGems")) next.giftGems = current.giftGems;
  if (!Object.prototype.hasOwnProperty.call(data, "hero")) next.hero = current.hero;
  if (!Object.prototype.hasOwnProperty.call(data, "zoneRuns")) next.zoneRuns = clone(current.zoneRuns || {});
  if (next.spoken == null) next.spoken = current.spoken || 0;
  if (!next.regionsDone) next.regionsDone = clone(current.regionsDone || []);
  if (!next.lastZone) next.lastZone = clone(current.lastZone || {});
  return { ok: true, state: next };
}

export function prepareRestore(current, input) {
  var check = validateBackup(input, current);
  if (!check.ok) return { ok: false, reason: check.reason, state: current, bak: null };
  return { ok: true, reason: "", state: check.state, bak: clone(current) };
}

export function ownsItem(state, id) {
  return (state.owned || []).indexOf(id) >= 0 || (state.pantryOwned || []).indexOf(id) >= 0;
}

function splitBar(value) {
  return String(value || "").split(/[|\s]+/).filter(Boolean);
}

export function weaponCatalog(model) {
  var rules = model.trophyRules || {};
  var rows = String(rules.rows || "sword1 sword2 axe1 mace1").split(/\s+/);
  var types = splitBar(rules.typeNames);
  var tiers = splitBar(rules.tierNames);
  var costs = rules.tierStars || [0, 45, 200];
  var list = [];
  rows.forEach(function (wt, ri) {
    for (var tier = 1; tier <= 3; tier++) {
      var named = null;
      (model.trophies || []).some(function (t) {
        if (t.wt === wt && t.tier === tier) { named = t; return true; }
        return false;
      });
      var id = named ? named.id : wt + "-t" + tier;
      if (wt === "sword1" && tier === 1) id = "sword-iron";
      list.push({
        id: id,
        wt: wt,
        tier: tier,
        row: types[ri] || wt,
        name: named ? named.en : ((tiers[tier - 1] || ("Tier " + tier)) + " " + (types[ri] || wt)),
        th: named ? (named.thGloss || named.th || "") : "",
        cost: costs[tier - 1] != null ? costs[tier - 1] : 0,
        named: !!named
      });
    }
  });
  return list;
}

export function buyItem(state, model, id) {
  var next = clone(state);
  var lid = "buy:" + id;
  if (next.ledger[lid] || ownsItem(next, id)) return { state: next, duplicate: true, error: "owned" };
  var item = ((model.pantry && model.pantry.items) || []).filter(function (it) { return it.id === id; })[0];
  var cost = 0;
  var slot = "";
  var kind = "";
  if (item) {
    cost = item.stars || 0;
    slot = item.slot || "";
    kind = "pantry";
  } else {
    var offer = weaponCatalog(model).filter(function (w) { return w.id === id; })[0];
    if (!offer) return { state: next, error: "missing" };
    if (!rowOpen(next, offer.wt)) return { state: next, error: "closed" };
    if (levelForXp(next.xp) < tierLevel(model, offer.tier)) return { state: next, error: "closed" };
    if (offer.tier === 1) return { state: next, error: "free" };
    cost = offer.cost;
    slot = "weapon";
    kind = "weapon";
  }
  if ((next.goldStars || 0) < cost) return { state: next, error: "stars" };
  next.goldStars -= cost;
  next.ledger[lid] = 1;
  if (kind === "pantry") {
    next.pantryOwned.push(id);
    if (slot) next.equipped[slot] = id;
  } else {
    next.owned.push(id);
    next.equipped.weapon = id;
  }
  return { state: next, ok: true, error: "" };
}

export function equipItem(state, model, id) {
  var next = clone(state);
  if (!ownsItem(next, id)) return { state: next, error: "not-owned" };
  var xp = next.xp;
  var stars = next.goldStars;
  var ownedN = next.owned.length;
  var t = null;
  (model.trophies || []).some(function (x) { if (x.id === id) { t = x; return true; } return false; });
  var p = null;
  ((model.pantry && model.pantry.items) || []).some(function (x) { if (x.id === id) { p = x; return true; } return false; });
  var slot = (t && t.slot) || (p && p.slot) || "";
  if (t && t.wt) slot = t.wt === "shield" ? "offHand" : "weapon";
  if (id === "shield-sunrise") slot = "offHand";
  if (!slot) return { state: next, error: "slot" };
  if (next.equipped[slot] === id && slot !== "weapon") next.equipped[slot] = null;
  else next.equipped[slot] = id;
  if (slot === "weapon" && t && (t.wt === "sword2" || t.wt === "crook")) next.equipped.offHand = null;
  next.xp = xp;
  next.goldStars = stars;
  if (next.owned.length !== ownedN) next.owned = next.owned.slice(0, ownedN);
  return { state: next, ok: true };
}

export function reviewOnMiss(queue, card) {
  var q = Array.isArray(queue) ? queue.slice() : [];
  if (!card || card.mode !== "picture-recall") return q;
  if (card.type === "say-it" || card.type === "two-answer") return q;
  if (q.indexOf(card.id) >= 0) return q;
  q.push(card.id);
  if (q.length > 20) q = q.slice(q.length - 20);
  return q;
}

export function reviewOnRight(queue, cardId) {
  return (queue || []).filter(function (id) { return id !== cardId; });
}

export function bonusWordsFor(model, id) {
  var map = (model.meta && model.meta.weaponBonus) || {};
  if (map[id]) return map[id];
  var item = weaponCatalog(model).filter(function (w) { return w.id === id; })[0];
  if (!item) return "";
  var themes = String((model.trophyRules && model.trophyRules.theme) || "").split(/\s+/).filter(Boolean);
  var rows = String((model.trophyRules && model.trophyRules.rows) || "").split(/\s+/).filter(Boolean);
  var theme = themes[rows.indexOf(item.wt)] || "";
  if (!theme) return "";
  if (item.tier === 1) return theme;
  var second = theme + "2";
  if (item.tier === 2) return second;
  if (second.indexOf("Star") >= 0) return second + " Hint";
  return second + " Star";
}

export function gearBonuses(state, model) {
  var bag = { hint: 0, retry: 0, star: 0, streakEvery: 0, slow: false, respell: false, words: [] };
  function add(words) {
    if (!words) return;
    bag.words.push(words);
    String(words).split(/\s+/).forEach(function (w) {
      if (w === "Hint") bag.hint += 1;
      if (w === "Hint2") bag.hint += 2;
      if (w === "Retry") bag.retry += 1;
      if (w === "Retry2") bag.retry += 2;
      if (w === "Star") bag.star += 1;
      if (w === "Star2") bag.star += 2;
      if (w === "Streak") bag.streakEvery = 3;
      if (w === "Streak2") bag.streakEvery = 2;
      if (w === "Slow") bag.slow = true;
      if (w === "Respell") bag.respell = true;
    });
  }
  add(bonusWordsFor(model, state.equipped && state.equipped.weapon));
  add(bonusWordsFor(model, state.equipped && state.equipped.offHand));
  return bag;
}

export function awardExtras(run, bonuses, spoken) {
  var rightRow = (run.rightRow || 0) + 1;
  var coinBonus = bonuses.streakEvery && rightRow % bonuses.streakEvery === 0 ? 1 : 0;
  return { rightRow: rightRow, coinBonus: coinBonus, starBonus: spoken ? (bonuses.star || 0) : 0 };
}

export function noteMiss(run) {
  var next = clone(run);
  if ((next.retriesLeft || 0) > 0) {
    next.retriesLeft -= 1;
    return { run: next, retry: true };
  }
  next.wasMiss = true;
  next.rightRow = 0;
  return { run: next, retry: false };
}

export function shopRows(state, model) {
  var level = levelForXp(state.xp || 0);
  var grouped = {};
  weaponCatalog(model).forEach(function (slot) {
    if (!grouped[slot.wt]) grouped[slot.wt] = [];
    grouped[slot.wt].push(slot);
  });
  return Object.keys(grouped).map(function (wt) {
    return {
      wt: wt,
      row: grouped[wt][0].row,
      open: rowOpen(state, wt),
      slots: grouped[wt].map(function (slot) {
        var tierOpen = level >= tierLevel(model, slot.tier);
        var owned = ownsItem(state, slot.id);
        var stars = state.goldStars || 0;
        return {
          id: slot.id,
          name: slot.name,
          th: slot.th,
          tier: slot.tier,
          cost: slot.cost,
          tierOpen: tierOpen,
          owned: owned,
          silhouette: slot.tier === 3 && !owned && !(tierOpen && stars >= slot.cost),
          equipped: (state.equipped && (state.equipped.weapon === slot.id || state.equipped.offHand === slot.id)) || false,
          bonus: bonusWordsFor(model, slot.id)
        };
      })
    };
  });
}

export function beginKneel(state, model, zoneKey) {
  var committed = commitBoss(state, model, zoneKey);
  return { state: committed.state, duplicate: !!committed.duplicate, zone: zoneKey };
}

export function thaiReviewQueue(model) {
  var nurse = [];
  var hints = [];
  model.cards.forEach(function (card) {
    if (card.nursePhrase) nurse.push(card.id);
    else if (card.thDef) hints.push(card.id);
  });
  return {
    needsMaxwell: (model.raw.needsMaxwell || []).slice(),
    nurse: nurse,
    thDef: hints
  };
}

export function sharedEnding(a, b) {
  var n = 0;
  var i = String(a || "").length - 1;
  var j = String(b || "").length - 1;
  while (i >= 0 && j >= 0 && a.charAt(i) === b.charAt(j)) {
    n += 1;
    i -= 1;
    j -= 1;
  }
  return n;
}

export function endingPairs(pairs) {
  return (pairs || []).filter(function (pair) { return sharedEnding(pair.a, pair.b) >= 3; });
}

export function endingDiscrepancy(pairs) {
  var found = endingPairs(pairs).map(function (pair) { return pair.a + "/" + pair.b; });
  return {
    specCount: 6,
    found: found,
    resolved: true,
    resolution: "No field names six word-ending pairs. The eight shared endings stay in the normal pool. The six picture pairs are three/tree, bath/bat, mouth/mouse, ship/sheep, card/car, and bread/bed."
  };
}

export function pendingMaxwell(ids, settled) {
  var skip = {};
  (settled || []).forEach(function (id) { skip[id] = 1; });
  return (ids || []).filter(function (id) { return !skip[id]; });
}

export function fillBackupCompare(template, a, b, c, d) {
  return String(template || "")
    .split("{a}").join(String(a))
    .split("{b}").join(String(b))
    .split("{c}").join(String(c))
    .split("{d}").join(String(d));
}

export function letterBank(word) {
  var letters = String(word || "").split("");
  var extra = ["a", "e", "i", "o", "s", "t", "n", "r"];
  var i = 0;
  while (letters.length < 6 && i < extra.length) {
    if (letters.indexOf(extra[i]) < 0) letters.push(extra[i]);
    i += 1;
  }
  return letters.slice(0, 6);
}

export function spellStep(word, got, letter) {
  var have = got || "";
  var next = String(word || "").charAt(have.length);
  if (letter !== next) return { got: have, correct: false, done: false, scale: have.length / Math.max(1, String(word || "").length) };
  var grown = have + letter;
  return { got: grown, correct: true, done: grown === word, scale: grown.length / Math.max(1, String(word || "").length) };
}

export function countPlates(answer) {
  var words = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];
  var right = String(answer || "").toLowerCase();
  var others = words.filter(function (word) { return word !== right; });
  return [right, others[0], others[1]];
}

export function countPrompt(card, ui) {
  var word = String((card && card.en) || "").toLowerCase();
  var n = { two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 }[word] || 0;
  var kinds = ["cows", "baskets", "hats"];
  var sum = 0;
  var id = String((card && card.id) || "");
  var i;
  for (i = 0; i < id.length; i++) sum += id.charCodeAt(i);
  var thing = kinds[sum % 3];
  var pack = ui || {};
  if (thing === "cows" && pack.howManyCows) {
    return { n: n, thing: thing, en: pack.howManyCows.en, th: pack.howManyCows.th };
  }
  var how = pack.howMany || { en: "", th: "" };
  return {
    n: n,
    thing: thing,
    en: String(how.en || "").split("{thing}").join(thing),
    th: String(how.th || "").split("{thing}").join(thing)
  };
}

export function trophiesByTab(model) {
  var tabs = { gems: [], themes: [], titles: [], gear: [] };
  (model.trophies || []).forEach(function (trophy) {
    if (trophy.cat === "gems" || trophy.cat === "themes" || trophy.cat === "titles") tabs[trophy.cat].push(trophy.id);
    else tabs.gear.push(trophy.id);
  });
  return tabs;
}

export function buildDuelSchedule(pairs) {
  var pics = [];
  var rest = [];
  (pairs || []).forEach(function (pair) {
    if (pair && pair.pics) pics.push(pair);
    else rest.push(pair);
  });
  var deck = pics.concat(rest);
  var rounds = [];
  var r;
  var k;
  for (r = 0; r < 4; r++) {
    var slice = [];
    for (k = 0; k < 8; k++) slice.push(deck[(r * 8 + k) % deck.length]);
    rounds.push(slice);
  }
  var recap = [];
  for (k = 0; k < 10; k++) recap.push(deck[k % deck.length]);
  return { rounds: rounds, recap: recap };
}

export function speakEnglish(text, synth) {
  try {
    if (!synth || !text) return false;
    if (synth.cancel) synth.cancel();
    synth.speak(text);
    return true;
  } catch (e) {
    return false;
  }
}

export function popReward(state) {
  var next = clone(state);
  var item = (next.rewardQueue || []).shift() || null;
  return { state: next, item: item };
}

export async function playClip(url, fetchFn) {
  try {
    var res = await fetchFn(url);
    if (!res || !res.ok) return false;
    return true;
  } catch (e) {
    return false;
  }
}

export function gateBossName(model, regionId) {
  var need = { r2: "sight-words", r3: "numbers", r4: "baby-hospital" }[regionId];
  if (!need) return null;
  var zone = model.zoneByKey[need];
  return zone && zone.boss && zone.boss.name ? zone.boss.name : null;
}

export function sceneKind(zoneKey, runs) {
  if (zoneKey === "phonics" || zoneKey === "sight-words") return (runs % 2 === 1) ? "pond" : "park";
  if (zoneKey === "colors-shapes" || zoneKey === "numbers") return "farm";
  if (zoneKey === "baby-hospital") return "home";
  if (zoneKey === "maxwell-says") return "desk";
  if (zoneKey === "kitchen") return "kitchen";
  return "forest";
}

export function todName(step) {
  return { 1: "m", 2: "d", 3: "a", 4: "e", 5: "n" }[step] || "m";
}
