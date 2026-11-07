import * as E from "./engine.mjs";
import { sceneSvg, pictureHtml, escapeText, coinRow, guardianKneel } from "./art.mjs";

var D = null;
var S = null;
var today = "";
var sessionRuns = 0;
var hintMode = 0;
var jesusI = 0;
var jesusSeen = {};
var jesusAnnounced = false;
var advanceAt = 0;
var inline = {};
var titleSvg = "";
var paused = false;
var encI = 0;

window.__errors = [];
window.addEventListener("error", function (event) {
  window.__errors.push(String(event.message || "error"));
});

function pad(n) { return (n < 10 ? "0" : "") + n; }
function todayStamp(d) {
  return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
}
function reduced() {
  return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}
function bi(en, th, cls) {
  return "<span class='en'>" + escapeText(en || "") + "</span><span class='th" + (cls ? " " + cls : "") + "' lang='th'>" + escapeText(th || "") + "</span>";
}
function plate(en, th) {
  return "<span class='plate'>" + bi(en, th) + "</span>";
}
function ui(key) {
  return (D && D.ui && D.ui[key]) || { en: "", th: "" };
}
function heroSvg() {
  var pack = D.picPlan.uiInlineSvg || {};
  return S.hero === "nancy" ? (pack.nancy || "") : (pack.sam || "");
}
function wake() {
  try {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!window.__ac) window.__ac = new AC();
    if (window.__ac.state === "suspended") window.__ac.resume();
    var buf = window.__ac.createBuffer(1, 1, 22050);
    var src = window.__ac.createBufferSource();
    src.buffer = buf;
    src.connect(window.__ac.destination);
    src.start();
    if (window.speechSynthesis) {
      var u = new SpeechSynthesisUtterance("");
      window.speechSynthesis.speak(u);
    }
  } catch (e) { /* audio is optional */ }
}
function thud() {
  try {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!window.__ac) window.__ac = new AC();
    var ctx = window.__ac;
    if (ctx.state === "suspended") ctx.resume();
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    var t = ctx.currentTime;
    o.frequency.setValueAtTime(90, t);
    o.frequency.exponentialRampToValueAtTime(55, t + 0.12);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.25, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
    o.connect(g);
    g.connect(ctx.destination);
    o.start(t);
    o.stop(t + 0.17);
  } catch (e) { /* missing audio never blocks */ }
}
function speak(text, slow) {
  var bonus = D ? E.gearBonuses(S, D) : { slow: false };
  var rate = bonus.slow ? 0.5 : (S && S.settings && S.settings.slowMode ? 0.6 : 0.85);
  if (slow) rate = Math.min(rate, 0.6);
  var synth = window.speechSynthesis ? {
    cancel: function () { window.speechSynthesis.cancel(); },
    speak: function (line) {
      var u = new SpeechSynthesisUtterance(line);
      u.lang = "en-US";
      u.rate = rate;
      window.speechSynthesis.speak(u);
    }
  } : null;
  return E.speakEnglish(text, synth);
}
function playFile(rel) {
  E.playClip(rel, function (url) { return fetch(url); }).then(function (ok) {
    if (!ok) return;
    return fetch(rel).then(function (res) { return res.arrayBuffer(); }).then(function (buf) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      if (!window.__ac) window.__ac = new AC();
      return window.__ac.decodeAudioData(buf).then(function (audio) {
        var src = window.__ac.createBufferSource();
        src.buffer = audio;
        src.connect(window.__ac.destination);
        src.start();
      });
    });
  }).catch(function () { /* missing clip */ });
}

function idb() {
  return new Promise(function (resolve, reject) {
    try {
      var req = indexedDB.open("nae", 1);
      req.onupgradeneeded = function () {
        if (!req.result.objectStoreNames.contains("kv")) req.result.createObjectStore("kv");
      };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error); };
    } catch (e) { reject(e); }
  });
}
function persistable(state) {
  var copy = E.clone(state);
  ["screen", "verseDue", "welcomeShow", "showGift", "bubble", "glowId", "wiggleId", "cheerUntil", "nodUntil", "lock", "backupOk", "backupText", "backupReason", "moonChoice", "pipGlow", "_rest", "_next", "gateMessage"].forEach(function (k) {
    delete copy[k];
  });
  return copy;
}
function save() {
  var copy = persistable(S);
  try { localStorage.setItem("naeState", JSON.stringify(copy)); } catch (e) { /* mirror skipped */ }
  idb().then(function (db) {
    return new Promise(function (resolve, reject) {
      var tx = db.transaction("kv", "readwrite");
      tx.objectStore("kv").put(copy, "state");
      tx.oncomplete = function () { resolve(); };
      tx.onerror = function () { reject(tx.error); };
    });
  }).catch(function () { /* write skipped */ });
}
function loadState() {
  return idb().then(function (db) {
    return new Promise(function (resolve) {
      var tx = db.transaction("kv", "readonly");
      var rq = tx.objectStore("kv").get("state");
      rq.onsuccess = function () { resolve(rq.result || null); };
      rq.onerror = function () { resolve(null); };
    });
  }).catch(function () { return null; }).then(function (rec) {
    if (rec && rec.schema === 5020) return rec;
    try {
      var mirror = JSON.parse(localStorage.getItem("naeState") || "null");
      if (mirror && mirror.schema === 5020) return mirror;
    } catch (e) { /* unreadable mirror */ }
    return null;
  });
}

function xpFrac(xp) {
  var level = E.levelForXp(xp || 0);
  if (level >= 20) return 100;
  var a = E.xpToReach(level);
  var b = E.xpToReach(level + 1);
  if (b <= a) return 100;
  return Math.max(0, Math.min(100, Math.round(((xp || 0) - a) / (b - a) * 100)));
}
function hud(scene) {
  var gems = E.gemCount(S, D);
  var cheer = S.cheerUntil && Date.now() < S.cheerUntil ? " cheer" : "";
  var nod = S.nodUntil && Date.now() < S.nodUntil ? " nod" : "";
  return "<header class='hud' data-xp='" + S.xp + "' data-stars='" + S.goldStars + "' data-pips='" + S.pips + "' data-gems='" + gems + "'>" +
    "<div class='hud-side'><div class='count'>◆ " + gems + "</div>" + coinRow(S.pips || 0) + "</div>" +
    "<div class='portrait" + cheer + nod + "'>" + heroSvg() + "</div>" +
    "<div class='hud-side' style='align-items:flex-end'><div class='level-label'>Level " + S.level + "</div>" +
    "<div class='xpbar" + (S.pipGlow ? " pip-glow" : "") + "'><span style='width:" + xpFrac(S.xp) + "%'></span></div>" +
    "<div class='count'>" + S.goldStars + "</div></div></header>";
}
function banner(en, th) {
  return "<div class='banner'>" + bi(en, th) + "</div>";
}
function bubbleHtml() {
  if (!S.bubble) return "";
  return "<div class='bubble'><div class='en'>" + escapeText(S.bubble.en || "") + "</div><div class='th' lang='th'>" + escapeText(S.bubble.th || "") + "</div></div>";
}

function sceneSlots(ids) {
  var pos = [
    { left: "38%", surface: "ground" },
    { left: "54%", surface: "ground" },
    { left: "70%", surface: "ground" },
    { left: "50%", surface: "bench" },
    { left: "72%", surface: "bench" }
  ];
  var props = ids.map(function (id, i) {
    var card = D.byId[id];
    var p = pos[i] || pos[0];
    var cls = "prop on-" + p.surface;
    if (S.glowId === id) cls += " glow-gold";
    if (S.wiggleId === id) cls += " wiggle";
    return "<button class='" + cls + "' data-tap data-prop data-surface='" + p.surface + "' data-act='prop' data-arg='" + escapeText(id) + "' data-correct='" + (id === (currentStep() && currentStep().id) ? "1" : "0") + "' style='left:" + p.left + "'>" +
      pictureHtml(card && card.pic, inline) + "<i class='shadow'></i></button>";
  }).join("");
  return "<div class='bench-seat' data-seat='1'></div>" + props;
}
function currentStep() {
  if (!S.run || !S.run.steps) return null;
  return S.run.steps[S.run.index] || null;
}
function currentCard() {
  var step = currentStep();
  return step ? D.byId[step.id] : null;
}
function sceneMates(step) {
  if (!S.run || step.scene == null) return [step.id];
  var ids = [];
  S.run.steps.forEach(function (s) {
    if (s.scene === step.scene && s.kind !== "ask") ids.push(s.id);
  });
  var seen = {};
  return ids.filter(function (id) {
    if (seen[id]) return false;
    seen[id] = 1;
    return true;
  }).slice(0, 5);
}

function renderPlay() {
  var step = currentStep();
  var card = currentCard();
  if (!step || !card) { S.screen = "map"; return renderMap(); }
  if (step.kind === "ask") return renderAsk(step, card);
  document.body.setAttribute("data-theme", "arena");
  var zone = D.zoneByKey[S.run.zone];
  var kind = E.sceneKind(S.run.zone, (S.zoneRuns && S.zoneRuns[S.run.zone]) || 0);
  var tod = E.todName(S.run.tod || 1);
  var bonuses = E.gearBonuses(S, D);
  if (S.run.index < bonuses.hint && !(S.run.autoHints || {})[S.run.index]) {
    if (!S.run.autoHints) S.run.autoHints = {};
    S.run.autoHints[S.run.index] = 1;
    S.bubble = { en: (card.hint && card.hint.letters) || "", th: ui("itStartsWith").th };
  }
  var prompt = E.promptFor(card, D.ui, step.listen && step.kind === "scene");
  var respellLine = bonuses.respell && card.respell ? "<div class='en' style='color:#8A6200'>" + escapeText(card.respell) + "</div>" : "";
  if (step.kind === "letter") prompt = { en: ui("spellIt").en, th: ui("spellIt").th };
  if (step.kind === "count") prompt = { en: ui("howMany").en, th: ui("howMany").th };
  if (step.kind === "size") prompt = { en: ui("bigOrSmall").en, th: ui("bigOrSmall").th };
  var extra = "";
  if (step.kind === "letter") extra = letterPads(card);
  if (step.kind === "count") extra = countPads(card, step);
  if (step.kind === "size") extra = sizePads(card);
  return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='stage'><div class='scene-frame' data-tod='" + tod + "'>" + sceneSvg(kind, tod) +
    "<div class='hero-fig'>" + heroSvg() + "<i class='shadow'></i></div>" +
    sceneSlots(sceneMates(step)) + "</div></div>" +
    "<div class='qcard'><div class='prompt'>" + bi(prompt.en, prompt.th) + respellLine + bubbleHtml() + extra + "</div>" +
    "<button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>🍃<span class='hint-label th' lang='th'>" + escapeText(ui("wordsForYou").th) + "</span></button></div></div>";
}
function letterPads(card) {
  var word = String(card.en || "");
  var got = (S.run.spell && S.run.spell.id === card.id) ? S.run.spell.got : "";
  var blanks = word.split("").map(function (ch, i) { return got.charAt(i) || "_"; }).join(" ");
  var letters = word.split("");
  "aeiost".split("").forEach(function (ch) { if (letters.length < 6 && letters.indexOf(ch) < 0) letters.push(ch); });
  letters = E.shuffle(letters, E.mulberry32(word.length + 3)).slice(0, 6);
  return "<div class='letters'>" + escapeText(blanks) + "</div><div class='choices'>" + letters.map(function (ch) {
    return "<button class='choice' data-tap data-act='letter' data-arg='" + escapeText(ch) + "'>" + escapeText(ch) + "</button>";
  }).join("") + "</div>";
}
function countPads(card, step) {
  var right = card.en;
  var opts = (step.choices || []).slice(0, 3);
  if (opts.indexOf(right) < 0) opts[0] = right;
  while (opts.length < 3) opts.push(["two", "four", "six"][opts.length]);
  return "<div class='choices'>" + opts.map(function (en) {
    return "<button class='choice" + (S.glowId === en ? " glow-gold" : "") + (S.moonChoice === en ? " glow-moon" : "") + "' data-tap data-act='count' data-arg='" + escapeText(en) + "'>" + escapeText(en) + "</button>";
  }).join("") + "</div>";
}
function sizePads(card) {
  var a = D.byId["cs-23"];
  var b = D.byId["cs-24"];
  var opts = [a && a.en, b && b.en].filter(Boolean);
  if (!opts.length) opts = [card.en];
  return "<div class='choices'>" + opts.map(function (en) {
    return "<button class='choice' data-tap data-act='size' data-arg='" + escapeText(en) + "'>" + escapeText(en) + "</button>";
  }).join("") + "</div>";
}

function renderAsk(step, card) {
  document.body.setAttribute("data-theme", "arena");
  var zone = D.zoneByKey[card.zone] || { name: "", nameTh: "" };
  if (card.type === "say-it") {
    return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
      "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
      "<div class='ask'><div class='pic-frame'>" + (card.pic ? pictureHtml(card.pic, inline) : "") + "</div>" +
      "<div class='prompt' style='text-align:center'>" + bi(card.en, card.th) +
      "<div class='en' style='color:#8A6200'>" + escapeText(card.respell || "") + "</div></div>" +
      bubbleHtml() +
      "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint'>🍃</button>" +
      "<button class='gold-btn' data-tap data-act='sayit'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div></div>";
  }
  if (card.type === "two-answer") {
    if (!S.run.twoKey) {
      var prompts = card.prompts || [];
      var pick = prompts[Math.floor(Math.random() * prompts.length)] || prompts[0];
      S.run.twoKey = pick ? pick.key : "";
      S.run.two = pick;
    }
    var pr = S.run.two || { en: "", th: "" };
    var buttons = (card.choices || []).map(function (ch) {
      var mark = S.moonChoice === ch.key ? " glow-moon" : "";
      var gold = S.glowId === ch.key ? " glow-gold" : "";
      return "<button class='choice" + mark + gold + "' data-tap data-act='two' data-arg='" + escapeText(ch.key) + "'>" +
        pictureHtml(ch.pic && String(ch.pic).indexOf("svg:") === 0 ? ch.pic : null, inline) +
        "<div>" + escapeText(ch.pic && String(ch.pic).indexOf("svg:") !== 0 ? ch.pic : "") + "</div>" +
        plate(ch.en, ui(ch.key).th || "") + "</button>";
    }).join("");
    var done = S.run.twoDone ? "<button class='gold-btn' data-tap data-act='twodone'>" + plate(ui("done").en, ui("done").th) + "</button>" : "";
    return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
      "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
      "<div class='ask'><div class='prompt' style='text-align:center'>" + bi(pr.en, pr.th) + "</div>" +
      "<div class='choices'>" + buttons + "</div>" + done + "</div></div>";
  }
  var showEn = E.showsEnglishAnswer(card, step.kind);
  var stemEn = showEn ? card.en : "";
  var stemTh = card.thDef || card.th;
  if (card.type === "server-talk") {
    stemEn = ui("serverAsks").en;
    stemTh = ui("serverAsks").th;
  }
  var choices = (step.choices || []).map(function (en) {
    var cls = "choice";
    if (S.glowId === en) cls += " glow-gold";
    if (S.moonChoice === en) cls += " glow-moon";
    return "<button class='" + cls + "' data-tap data-act='choice' data-arg='" + escapeText(en) + "'>" + escapeText(en) + "</button>";
  }).join("");
  var pic = card.pic ? pictureHtml(card.pic, inline) : "<div class='emoji-pic' style='opacity:.4'>📘</div><div class='th' lang='th'>" + escapeText(stemTh) + "</div>";
  var serverLine = card.type === "server-talk" ? "<div class='prompt'>" + bi(card.en, card.th) + "</div>" : "";
  return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='ask'><div class='pic-frame'>" + pic + "</div>" +
    (stemEn || card.type !== "server-talk" ? "<div class='ask-thai th' lang='th'>" + escapeText(card.type === "server-talk" ? stemTh : stemTh) + "</div>" : "") +
    serverLine +
    "<div class='choices'>" + choices + "</div>" + bubbleHtml() +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>🍃<span class='hint-label th' lang='th'>" + escapeText(ui("wordsForYou").th) + "</span></button><div></div></div></div></div>";
}

function renderReveal() {
  var step = currentStep();
  var card = currentCard();
  if (!card) { S.screen = "map"; return renderMap(); }
  document.body.setAttribute("data-theme", "arena");
  var head = S.run && S.run.wasMiss ? D.wrongText : (D.encouragement[encI % D.encouragement.length] || D.rewardText);
  if (!S.run.wasMiss) encI += 1;
  var trap = S.run && S.run.wasMiss && card.trapNote ? "<div class='th' lang='th'>" + escapeText(card.trapNote) + "</div>" : "";
  var say = (S.run && S.run.index < 10) ? "<div class='th' lang='th'>" + escapeText(ui("sayItOutLoud").th) + "</div><div class='en'>" + escapeText(ui("sayItOutLoud").en) + "</div>" : "";
  return "<div class='screen' data-screen='reveal'>" + banner(head.en, head.th) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='ask'><div class='pic-frame'>" + pictureHtml(card.pic, inline) + "</div>" +
    "<div class='prompt' style='text-align:center'><div class='en' style='font-size:36px;color:#10170F'>" + escapeText(card.en) + "</div>" +
    "<div class='en' style='color:#8A6200'>" + escapeText(card.respell || "") + "</div>" +
    "<div class='th' lang='th'>" + escapeText(card.th) + "</div>" + trap + say + "</div>" +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='replay'>🔊<span class='hint-label th' lang='th'>" + escapeText(ui("replay").th) + "</span></button>" +
    "<button class='gold-btn' data-tap data-act='got'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div></div>";
}

function renderBoss() {
  var run = S.run;
  var id = run.bossIds[run.bossIndex];
  var card = D.byId[id];
  var zone = D.zoneByKey[run.zone];
  var name = zone && zone.boss && zone.boss.name ? zone.boss.name : { en: "", th: "" };
  if (!run.bossChoices) run.bossChoices = {};
  if (card && !run.bossChoices[id]) {
    run.bossChoices[id] = E.shuffle((card.choices || []).map(function (c) { return c.en; }), E.mulberry32(id.length * 17));
  }
  var choices = ((run.bossChoices && run.bossChoices[id]) || []).map(function (en) {
    var cls = "choice";
    if (S.glowId === en) cls += " glow-gold";
    if (S.moonChoice === en) cls += " glow-moon";
    return "<button class='" + cls + "' data-tap data-act='boss' data-arg='" + escapeText(en) + "'>" + escapeText(en) + "</button>";
  }).join("");
  var cleared = 0;
  Object.keys(run.bossCleared || {}).forEach(function (k) { if (run.bossCleared[k]) cleared += 1; });
  var remain = Math.max(0, 100 - cleared * 10);
  document.body.setAttribute("data-theme", "arena");
  return "<div class='screen' data-screen='boss'>" + banner(name.en, name.th) + hud(true) +
    "<div class='ask'><div class='boss-meter' aria-hidden='true'><span style='width:" + remain + "%'></span></div>" +
    "<div class='pic-frame'>" + pictureHtml(card && card.pic, inline) + "</div>" +
    "<div class='ask-thai th' lang='th'>" + escapeText((card && (card.thDef || card.th)) || "") + "</div>" +
    "<div class='choices'>" + choices + "</div>" + bubbleHtml() +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint'>🍃</button>" +
    "<button class='metal' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button></div></div></div>";
}

function renderTitle() {
  document.body.setAttribute("data-theme", "menu");
  var g = ui(greetKey());
  var overlay = "";
  if (S.welcomeShow) {
    overlay = "<div class='scrim'><div class='panel'><div class='prompt'>" + bi(D.welcomeBack.en, D.welcomeBack.th) + "</div>" +
      "<button class='gold-btn' data-tap data-act='welcome'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div>";
  } else if (S.verseDue) {
    var verse = E.verseForDate(D, today);
    overlay = "<div class='scrim verse-pop'><div class='verse-card'>" +
      banner(ui("verseOfDay").en, ui("verseOfDay").th) +
      "<div class='en'>" + escapeText(ui("verseGift").en) + "</div><div class='th' lang='th'>" + escapeText(ui("verseGift").th) + "</div>" +
      "<div class='verse-body' data-scroll-ok><div class='en'>" + escapeText(verse.ref) + "</div>" +
      "<div class='verse-en en'>" + escapeText(verse.en).split("\n").join("<br>") + "</div><div class='tag'>(ESV)</div>" +
      "<div class='th' lang='th'>" + escapeText(verse.th).split("\n").join("<br>") + "</div><div class='tag'>(THSV11)</div></div>" +
      "<div class='row-actions'><button class='hint-btn' data-tap data-act='replayverse'>🔊</button>" +
      "<button class='title-go' data-tap data-act='versegot' style='position:static'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div></div>";
  }
  return "<div class='screen title-screen' data-screen='title'><div class='ti' data-tod='" + titleTod() + "'>" + titleSvg + "</div><div class='fade-bottom'></div>" +
    "<button class='title-go' data-tap data-act='letsgo'>" + plate(ui("letsGo").en, ui("letsGo").th) + "</button>" + overlay + "</div>";
}
function greetKey() {
  var h = new Date().getHours();
  if (h >= 5 && h < 12) return "greetMorning";
  if (h >= 12 && h < 17) return "greetAfternoon";
  if (h >= 17 && h < 21) return "greetEvening";
  return "greetNight";
}
function titleTod() {
  var h = new Date().getHours();
  if (h >= 5 && h < 12) return "m";
  if (h >= 12 && h < 17) return "a";
  if (h >= 17 && h < 21) return "e";
  return "n";
}
function paintTitle() {
  var svg = document.querySelector(".ti svg");
  if (!svg) return;
  var g = ui(greetKey());
  var node = document.getElementById("gE");
  if (node) node.textContent = g.en || "";
  svg.setAttribute("aria-label", (g.en || "") + " " + (g.th || ""));
  if (S.hero === "nancy") {
    var th = document.getElementById("th");
    if (th) th.setAttribute("display", "none");
    var tn = document.getElementById("tn");
    var nancy = D.picPlan.uiInlineSvg && D.picPlan.uiInlineSvg.nancy;
    if (tn && nancy && !tn.firstChild) tn.innerHTML = nancy;
  }
}

function renderMenu() {
  document.body.setAttribute("data-theme", "menu");
  var pack = D.picPlan.uiInlineSvg || {};
  var gift = S.showGift ? "<div class='gift-tag'><div class='en'>" + escapeText(ui("dailyGift").en) + "</div><div class='th' lang='th'>" + escapeText(ui("dailyGift").th) + "</div></div>" : "";
  var home = window.matchMedia && window.matchMedia("(display-mode: standalone)").matches ? "" :
    "<div class='th' lang='th' style='text-align:center'>" + escapeText(ui("openFromHome").th) + "</div>";
  return "<div class='screen' data-screen='menu'><div class='menu'>" +
    "<div class='top-tools'><button class='hearth' data-tap data-act='hearth' aria-label='" + escapeText(ui("verseGift").en) + "'>♥</button></div>" +
    "<div class='logs'></div>" + gift +
    "<div class='hero-band' aria-label='" + escapeText(ui("chooseHero").en) + "'>" +
    heroButton("sam", pack.sam, ui("heroName")) + heroButton("nancy", pack.nancy, ui("heroNancy")) + "</div>" +
    "<div class='stack'>" +
    "<button class='metal' data-tap data-act='gear'>" + plate(ui("gear").en, ui("gear").th) + "</button>" +
    "<button class='metal' data-tap data-act='shop'>" + plate(ui("pantry").en, ui("pantry").th) + "</button>" +
    "<button class='metal' data-tap data-act='map'>" + plate(ui("titleMap").en, ui("titleMap").th) + "<span class='arrow-cue'>➤</span></button>" +
    "</div>" + home + bubbleHtml() + "</div></div>";
}
function heroButton(id, svg, name) {
  var on = S.hero === id;
  return "<button class='hero-card" + (on ? " on" : " off") + "' data-tap data-act='hero' data-arg='" + id + "'>" +
    "<div class='mini'>" + (svg || "") + "</div>" + bi(name.en, name.th) + "</button>";
}

function renderMap() {
  document.body.setAttribute("data-theme", "menu");
  var open = E.regionOpenMap(S);
  var ends = { r1: "sight-words", r2: "numbers", r3: "baby-hospital" };
  var arrow = null;
  ["r1", "r2", "r3"].forEach(function (id) {
    if (!arrow && open[id] && (S.bossesWon || []).indexOf(ends[id]) < 0 && !S.ledger["scenes5:" + ends[id]]) arrow = id;
  });
  var rows = D.regions.map(function (r) {
    var end = ends[r.id];
    var ribbon = end && S.ledger["scenes5:" + end] && D.zoneByKey[end] && D.zoneByKey[end].boss;
    var soft = r.id !== "r1" && !open[r.id];
    var cue = "";
    if (ribbon) cue = "<span class='ribbon en'>" + escapeText(ui("boss").en) + "</span>";
    else if (arrow === r.id) cue = "<span class='arrow-cue'>➤</span>";
    return "<button class='map-row" + (soft ? " soft" : "") + "' data-tap data-act='region' data-arg='" + r.id + "'>" +
      "<span class='dot' style='background:" + r.color + "'></span><span class='label'>" + bi(r.en, r.th) +
      (soft ? "<span class='th next' lang='th'>" + escapeText(ui("comingNext").th) + "</span>" : "") + "</span>" + cue + "</button>";
  }).join("");
  return "<div class='screen' data-screen='map'><div class='map'>" +
    banner(ui("titleMap").en, ui("titleMap").th) +
    "<div class='logs'></div>" +
    "<div class='hud' data-xp='" + S.xp + "' data-stars='" + S.goldStars + "'><button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button>" +
    "<div class='count'>◆ " + E.gemCount(S, D) + " ★ " + S.goldStars + " Level " + S.level + "</div>" +
    "<button class='hearth' data-tap data-act='hearth' aria-label='" + escapeText(ui("verseGift").en) + "'>♥</button></div>" +
    "<div class='rows'>" + rows + "</div>" + bubbleHtml() + "</div></div>";
}

function renderReward() {
  var item = (S.rewardQueue || [])[0];
  if (!item) { S.screen = "map"; return renderMap(); }
  document.body.setAttribute("data-theme", "menu");
  var key = E.bannerKey(item);
  var title = key === "verseGift" ? ui("verseGift") : key === "regionOpen" ? ui("regionOpen") : D.rewardText;
  var body = "";
  if (item.kind === "verse") {
    var scroll = (S.scrolls || []).filter(function (s) { return s.id === item.scrollId; })[0];
    if (scroll) {
      body = "<div class='en'>" + escapeText(scroll.ref) + "</div><div class='verse-en en'>" + escapeText(scroll.en).split("\n").join("<br>") + "</div><div class='tag'>(ESV)</div>" +
        "<div class='th' lang='th'>" + escapeText(scroll.th).split("\n").join("<br>") + "</div><div class='tag'>(THSV11)</div>" +
        "<div class='th' lang='th'>" + escapeText(ui("askMax").th) + "</div>";
    }
  } else if (item.kind === "region") {
    var region = D.regions.filter(function (r) { return r.id === item.regionId; })[0];
    body = region ? bi(region.en, region.th) : "";
  } else if (item.kind === "bossWin") {
    var zone = D.zoneByKey[item.zone];
    var name = zone && zone.boss ? zone.boss.name : { en: "", th: "" };
    body = bi(name.en, name.th);
  } else {
    body = bi(item.en || "", item.th || "");
  }
  var bits = reduced() ? "" : "<div class='confetti' aria-hidden='true'>" + [0, 1, 2, 3, 4, 5].map(function (i) {
    return "<i style='left:" + (8 + i * 15) + "%;background:" + (i % 2 ? "#FFCC33" : "#7FE0D0") + ";animation-delay:" + (i * 0.05) + "s'></i>";
  }).join("") + "</div>";
  return "<div class='screen' data-screen='reward'>" + banner(title.en, title.th) + bits +
    "<div class='ask'><div class='panel' style='margin:auto'>" + body +
    "<button class='gold-btn' data-tap data-act='got'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div></div>";
}

function renderRest() {
  document.body.setAttribute("data-theme", "menu");
  var verse = D.verses.rest;
  var first = !(S.scrolls || []).some(function (s) { return s.id === "scroll:rest"; });
  if (first) {
    var got = E.commitRestVerse(S, verse);
    S = got.state;
    save();
  }
  return "<div class='screen' data-screen='rest'>" + banner(ui("verseGift").en, ui("verseGift").th) +
    "<div class='ask'><div class='panel'>" + bi(D.restScreen.en, D.restScreen.th) +
    "<div class='verse-body' data-scroll-ok><div class='en'>" + escapeText(verse.ref) + "</div>" +
    "<div class='verse-en en'>" + escapeText(verse.en).split("\n").join("<br>") + "</div><div class='tag'>(ESV)</div>" +
    "<div class='th' lang='th'>" + escapeText(verse.th).split("\n").join("<br>") + "</div><div class='tag'>(THSV11)</div>" +
    "<div class='th' lang='th'>" + escapeText(ui("askMax").th) + "</div></div>" +
    "<button class='gold-btn' data-tap data-act='keep'>" + plate(ui("keepGoing").en, ui("keepGoing").th) + "</button>" +
    "<button class='metal' data-tap data-act='restnow'>" + plate(ui("restNow").en, ui("restNow").th) + "</button></div></div></div>";
}

function renderKneel() {
  var zone = D.zoneByKey[S.kneelZone] || {};
  var name = zone.boss && zone.boss.name ? zone.boss.name : { en: "", th: "" };
  var tint = { phonics: "#7FD38B", "colors-shapes": "#F5A3C7", numbers: "#7FB8F5", "sight-words": "#F5D06B", "baby-hospital": "#F2B8A0" }[S.kneelZone] || "#7FD38B";
  document.body.setAttribute("data-theme", "arena");
  return "<div class='screen' data-screen='kneel'>" + banner(name.en, name.th) +
    "<div class='stage'><div class='scene-frame'>" + sceneSvg("park", "a") +
    "<div class='hero-fig' style='left:8%'>" + heroSvg() + "</div>" +
    "<div style='position:absolute;left:46%;bottom:8%'>" + guardianKneel(tint) + "</div></div></div>" +
    "<div class='qcard'><div class='prompt'>" + bi(name.en, name.th) + "</div>" +
    "<button class='gold-btn' data-tap data-act='kneelgot'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div>";
}

function renderShop() {
  document.body.setAttribute("data-theme", "menu");
  var items = (D.pantry.items || []).map(function (item) {
    var owned = (S.pantryOwned || []).indexOf(item.id) >= 0;
    var label = owned ? ui("wearIt") : ui("getFor");
    return "<button class='trophy' data-tap data-act='buy' data-arg='" + item.id + "'>" +
      "<div>" + (String(item.pic || "").indexOf("svg:") === 0 ? pictureHtml(item.pic, inline) : escapeText(item.pic || "")) + "</div>" +
      bi(item.en, item.th) + "<div class='en'>" + (owned ? "✓" : ("★ " + item.stars)) + "</div><div class='th' lang='th'>" + escapeText(label.th) + "</div></button>";
  }).join("");
  var gear = E.shopRows(S, D).map(function (row) {
    var slots = row.slots.map(function (slot) {
      var price = slot.owned ? "✓" : (slot.tier === 1 ? "" : ("★ " + slot.cost));
      var cls = "trophy" + (slot.silhouette ? " sil" : "");
      var label = slot.silhouette ? ui("getFor").en : slot.name;
      return "<button class='" + cls + "' data-tap data-act='buy' data-arg='" + slot.id + "' data-open='" + (slot.tierOpen && row.open ? "1" : "0") + "'>" +
        "<div class='en'>" + escapeText(label) + "</div><div class='th' lang='th'>" + escapeText(slot.th || "") + "</div>" +
        "<div class='en'>" + price + "</div><div class='th' lang='th'>" + escapeText(slot.bonus || "") + "</div></button>";
    }).join("");
    return "<div class='en'>" + escapeText(row.row) + "</div><div class='shop-row' data-scroll-ok>" + slots + "</div>";
  }).join("");
  return "<div class='screen' data-screen='shop'>" + banner(ui("pantry").en, ui("pantry").th) +
    "<div class='sheet'><div class='count'>★ " + S.goldStars + "</div><div class='pane' data-scroll-ok><div class='grid3'>" + items + gear + "</div></div>" +
    "<button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button></div></div>";
}

function renderGear() {
  document.body.setAttribute("data-theme", "menu");
  var list = (D.trophies || []).slice(0, 18).map(function (t) {
    var owned = (S.owned || []).indexOf(t.id) >= 0;
    return "<button class='trophy' data-tap data-act='equip' data-arg='" + t.id + "'>" +
      bi(t.en, t.th || t.thGloss || "") + "<div class='en'>" + (owned ? "✓" : "✦") + "</div></button>";
  }).join("");
  return "<div class='screen' data-screen='gear'>" + banner(ui("character").en, ui("character").th) +
    "<div class='sheet'><div class='portrait' style='margin:0 auto'>" + heroSvg() + "</div>" +
    "<div class='pane' data-scroll-ok><div class='grid3'>" + list + "</div>" +
    "<button class='metal' data-tap data-act='shop'>" + plate(ui("pantry").en, ui("pantry").th) + "</button>" +
    "<button class='metal' data-tap data-act='backup'>" + plate(ui("backup").en, ui("backup").th) + "</button>" +
    "<button class='metal' data-tap data-act='toggle' data-arg='slowMode'>" + plate(ui("slowMode").en, (S.settings.slowMode ? "on" : "off")) + "</button>" +
    "<button class='metal' data-tap data-act='toggle' data-arg='restWeeks'>" + plate(ui("restWeeks").en, (S.settings.restWeeks ? "on" : "off")) + "</button></div>" +
    "<button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button></div></div>";
}

function renderBackup() {
  document.body.setAttribute("data-theme", "menu");
  var review = E.thaiReviewQueue(D);
  var ids = review.needsMaxwell.map(function (id) { return "<li class='th' lang='th'>" + escapeText(id) + "</li>"; }).join("");
  var queue = review.nurse.concat(review.thDef).map(function (id) {
    var mark = S.thaiMarks && S.thaiMarks[id] ? "✓" : "·";
    return "<button class='trophy' data-tap data-act='thaiok' data-arg='" + escapeText(id) + "'><span class='en'>" + mark + " " + escapeText(id) + "</span></button>";
  }).join("");
  var note = S.backupReason ? "<div class='th' lang='th'>" + escapeText(S.backupReason) + "</div>" : "";
  return "<div class='screen' data-screen='backup'>" + banner(ui("backup").en, ui("backup").th) +
    "<div class='sheet'><div class='pane' data-scroll-ok>" +
    "<button class='metal' data-tap data-act='export'>" + plate(ui("backup").en, ui("backup").th) + "</button>" +
    "<input id='bakefile' type='file' accept='application/json'>" +
    "<button class='metal' data-tap data-act='readbak'>" + plate(ui("restore").en, ui("restore").th) + "</button>" +
    note +
    "<button class='gold-btn' data-tap data-act='usebak'>" + plate(ui("useBackup").en, ui("useBackup").th) + "</button>" +
    "<div class='en'>" + escapeText(ui("needsMaxwell").en) + "</div><ul>" + ids + "</ul>" +
    "<div class='th' lang='th'>" + escapeText(ui("thaiReview").th || ui("thaiReview").en) + "</div><div class='grid3'>" + queue + "</div></div>" +
    "<button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button></div></div>";
}

function renderDuel() {
  document.body.setAttribute("data-theme", "arena");
  if (!S.duel) {
    var plan = E.buildDuelSchedule(D.soundDuel.pairs || []);
    var round = S.duelRounds || 0;
    var echo = round >= 4;
    S.duel = { index: 0, round: round, echo: echo, pairs: echo ? plan.recap : plan.rounds[round] || plan.rounds[0], heard: "" };
  }
  var pair = S.duel.pairs[S.duel.index];
  if (!pair) {
    return "<div class='screen' data-screen='duel'>" + banner(ui("roundDone").en, ui("roundDone").th) +
      "<div class='ask'><div class='en'>+30</div>" +
      "<button class='gold-btn' data-tap data-act='duelnext'>" + plate(D.gotItText.en, D.gotItText.th) + "</button>" +
      "<button class='metal' data-tap data-act='map'>" + plate(ui("toMap").en, ui("toMap").th) + "</button></div></div>";
  }
  if (!S.duel.heard) {
    S.duel.heard = Math.random() < 0.5 ? pair.a : pair.b;
    speak(S.duel.heard);
  }
  var pics = pair.pics || [];
  return "<div class='screen' data-screen='duel'>" + banner(ui("soundDuel").en, ui("soundDuel").th) + hud(false) +
    "<div class='ask'><div class='th' lang='th'>" + escapeText(S.duel.echo ? ui("echoKnight").en : ui("echoKnight").th) + "</div>" +
    "<div class='choices'>" +
    "<button class='choice' data-tap data-act='duel' data-arg='" + escapeText(pair.a) + "'>" + (pics[0] ? "<span class='emoji-pic'>" + escapeText(pics[0]) + "</span>" : "") + escapeText(pair.a) + "</button>" +
    "<button class='choice' data-tap data-act='duel' data-arg='" + escapeText(pair.b) + "'>" + (pics[1] ? "<span class='emoji-pic'>" + escapeText(pics[1]) + "</span>" : "") + escapeText(pair.b) + "</button></div>" +
    "<button class='hint-btn' data-tap data-act='hear'>" + plate(ui("hearItAgain").en, ui("hearItAgain").th) + "</button>" +
    bubbleHtml() + "</div></div>";
}

function render() {
  if (!D || !S) return;
  var html = "";
  if (paused && S.screen !== "title") {
    html = "<div class='screen' data-screen='continue'><div class='scrim continue-pop'><div class='panel'>" +
      "<button class='gold-btn' data-tap data-act='resume'>" + plate(ui("continue").en, ui("continue").th) + "</button></div></div></div>";
  } else if (S.screen === "title") html = renderTitle();
  else if (S.screen === "menu") html = renderMenu();
  else if (S.screen === "map") html = renderMap();
  else if (S.screen === "play") html = renderPlay();
  else if (S.screen === "reveal") html = renderReveal();
  else if (S.screen === "boss") html = renderBoss();
  else if (S.screen === "reward") html = renderReward();
  else if (S.screen === "rest") html = renderRest();
  else if (S.screen === "shop") html = renderShop();
  else if (S.screen === "gear") html = renderGear();
  else if (S.screen === "backup") html = renderBackup();
  else if (S.screen === "kneel") html = renderKneel();
  else if (S.screen === "duel") html = renderDuel();
  else html = renderMenu();
  document.getElementById("app").innerHTML = html;
  if (S.screen === "title") paintTitle();
  document.body.classList.toggle("short", window.innerHeight <= 600);
}

function enterMenu() {
  if (!S.ledger["gift:" + today]) {
    var gift = E.commitGift(S, today);
    S = gift.state;
    S.showGift = true;
    save();
  }
}
function startZone(zone, regionId) {
  var queue = [];
  try {
    queue = JSON.parse(localStorage.getItem("naeReviewQueue") || "[]");
    if (!Array.isArray(queue)) queue = [];
  } catch (e) { queue = []; }
  var run = E.buildRun(D, S, zone, { newVisit: !S.ledger.visited, reviewQueue: queue, rng: E.mulberry32((Date.now() % 997) + 1) });
  if (regionId) run.regionId = regionId;
  S.ledger.visited = 1;
  S.ledger.started = 1;
  run.retriesLeft = E.gearBonuses(S, D).retry || 0;
  S.run = run;
  if (!S.lastZone) S.lastZone = {};
  if (run.regionId) S.lastZone[run.regionId] = zone;
  S.screen = "play";
  hintMode = 0;
  S.glowId = "";
  S.wiggleId = "";
  S.moonChoice = "";
  save();
  render();
}
function afterRewards() {
  if (S.rewardQueue && S.rewardQueue.length) { S.screen = "reward"; render(); return; }
  if (S._rest) { S._rest = false; S.screen = "rest"; render(); return; }
  S.screen = "map";
  render();
}
function finishRun() {
  var run = S.run;
  if (!run) { S.screen = "map"; render(); return; }
  var fin = E.finishZoneRun(S, D, run, today);
  S = fin.state;
  sessionRuns += 1;
  S._rest = E.shouldRest(sessionRuns);
  save();
  afterRewards();
}
function advanceGate() {
  var now = Date.now();
  if (now - advanceAt < 400) return false;
  advanceAt = now;
  return true;
}
function nextBubble() {
  var useJesus = hintMode % 2 === 0;
  hintMode += 1;
  if (!useJesus) {
    var line = D.encouragement[encI % D.encouragement.length];
    encI += 1;
    S.bubble = { en: line.en, th: line.th };
    return;
  }
  var words = D.jesusWords || [];
  if (!words.length) return;
  if (!jesusAnnounced && words.every(function (w) { return jesusSeen[w.ref]; })) {
    jesusAnnounced = true;
    S.bubble = { en: ui("jesusAllHeard").en, th: ui("jesusAllHeard").th };
    jesusSeen = {};
    return;
  }
  var word = words[jesusI % words.length];
  jesusI += 1;
  jesusSeen[word.ref] = 1;
  S.bubble = { en: word.ref + " " + word.en, th: word.th };
}

function onCorrect(card, ledgerId, spoken) {
  var bonus = E.gearBonuses(S, D);
  var track = S.run || { rightRow: 0 };
  var extras = E.awardExtras(track, bonus, !!spoken);
  if (S.run) S.run.rightRow = extras.rightRow;
  var res = E.commitCorrect(S, D, {
    ledgerId: ledgerId,
    zone: card.zone,
    cardId: card.id,
    spoken: !!spoken,
    starBonus: extras.starBonus,
    coinBonus: extras.coinBonus
  });
  S = res.state;
  if (res.pipGlow) S.pipGlow = true;
  S.cheerUntil = Date.now() + 600;
  try {
    var q = JSON.parse(localStorage.getItem("naeReviewQueue") || "[]");
    localStorage.setItem("naeReviewQueue", JSON.stringify(E.reviewOnRight(q, card.id)));
  } catch (e) { /* queue is optional */ }
  return res;
}

function handle(act, arg) {
  if (!S || S.lock) return;
  if (act === "letsgo" || act === "resume" || act === "got" || act === "sayit" || act === "choice" || act === "prop" || act === "boss" || act === "region" || act === "map" || act === "gear" || act === "shop" || act === "back") thud();
  if (act === "letsgo") {
    wake();
    if (S.verseDue || S.welcomeShow) return;
    if (S.rewardQueue && S.rewardQueue.length) { S.screen = "reward"; render(); return; }
    if (S.run && S.run.phase !== "done") {
      S.screen = S.run.phase === "reveal" ? "reveal" : (S.run.phase === "boss" ? "boss" : "play");
      render();
      return;
    }
    if (!S.ledger.started) { startZone("phonics", D.regionOf.phonics); return; }
    S.screen = "menu";
    enterMenu();
    render();
    return;
  }
  if (act === "welcome") { S.welcomeShow = false; render(); return; }
  if (act === "versegot") {
    if (!advanceGate()) return;
    var verse = E.verseForDate(D, today);
    var got = E.commitVerseSeen(S, verse, today);
    S = got.state;
    S.verseDue = false;
    save();
    render();
    return;
  }
  if (act === "replayverse") {
    var v = E.verseForDate(D, today);
    speak(v.en);
    return;
  }
  if (act === "resume") {
    paused = false;
    wake();
    if (S.screen === "reveal") {
      var c = currentCard();
      if (c) speak(c.en);
    } else if (S.screen === "duel" && S.duel && S.duel.heard) speak(S.duel.heard);
    render();
    return;
  }
  if (act === "hero") {
    S.hero = arg === "nancy" ? "nancy" : "sam";
    save();
    render();
    return;
  }
  if (act === "map") { S.screen = "map"; S.duel = null; render(); return; }
  if (act === "back") { S.screen = "menu"; enterMenu(); render(); return; }
  if (act === "gear") { S.screen = "gear"; render(); return; }
  if (act === "shop") { S.screen = "shop"; render(); return; }
  if (act === "backup") { S.screen = "backup"; render(); return; }
  if (act === "tomap") {
    S.screen = "map";
    save();
    render();
    return;
  }
  if (act === "hearth") {
    var line = D.encouragement[encI % D.encouragement.length];
    encI += 1;
    S.bubble = { en: line.en, th: line.th };
    render();
    return;
  }
  if (act === "region") {
    var open = E.regionOpenMap(S);
    if (arg === "r4") {
      if (!open.r4) {
        var boss = E.gateBossName(D, "r4");
        S.bubble = { en: ui("guardianLast").en + " " + (boss ? boss.en : ""), th: ui("guardianLast").th + " " + (boss ? boss.th : "") };
        render();
        return;
      }
      S.screen = "duel";
      S.duel = null;
      render();
      return;
    }
    if (!open[arg] && arg !== "r3") {
      var gate = E.gateBossName(D, arg);
      S.bubble = { en: ui("guardianLast").en + " " + (gate ? gate.en : ""), th: ui("guardianLast").th + " " + (gate ? gate.th : "") };
      render();
      return;
    }
    if (S.run && S.run.regionId === arg && S.run.phase !== "done") {
      S.screen = S.run.phase === "boss" ? "boss" : (S.run.phase === "reveal" ? "reveal" : "play");
      render();
      return;
    }
    var zone = E.chooseZone(S, D, arg);
    if (!zone) return;
    var end = { r1: "sight-words", r2: "numbers", r3: "baby-hospital" }[arg];
    if (end && S.ledger["scenes5:" + end] && (S.bossesWon || []).indexOf(end) < 0 && zone === end) {
      var replay = E.buildRun(D, S, end, { rng: E.mulberry32(5) });
      replay.phase = "boss";
      replay.index = replay.steps.length;
      S.run = replay;
      S.screen = "boss";
      save();
      render();
      return;
    }
    startZone(zone, arg);
    return;
  }
  if (act === "prop") {
    var step = currentStep();
    var card = currentCard();
    if (!step || !card) return;
    if (arg !== step.id) {
      E.applyMiss(S);
      S.wiggleId = arg;
      S.glowId = step.id;
      S.nodUntil = Date.now() + 600;
      S.run.rightRow = 0;
      S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
      render();
      return;
    }
    if (step.kind === "letter" || step.kind === "count" || step.kind === "size") return;
    onCorrect(card, "card:" + S.run.id + ":" + S.run.index, card.type === "say-it");
    S.run.wasMiss = false;
    S.run.phase = "reveal";
    S.screen = "reveal";
    S.glowId = "";
    save();
    speak(card.en);
    render();
    return;
  }
  if (act === "letter") {
    var lcard = currentCard();
    var word = String(lcard.en || "");
    if (!S.run.spell || S.run.spell.id !== lcard.id) S.run.spell = { id: lcard.id, got: "" };
    var nextCh = word.charAt(S.run.spell.got.length);
    if (arg !== nextCh) {
      S.wiggleId = lcard.id;
      S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
      render();
      return;
    }
    S.run.spell.got += arg;
    if (S.run.spell.got === word) {
      onCorrect(lcard, "card:" + S.run.id + ":" + S.run.index, false);
      S.run.phase = "reveal";
      S.screen = "reveal";
      save();
      speak(word);
    }
    render();
    return;
  }
  if (act === "count" || act === "size") {
    var qcard = currentCard();
    if (arg !== qcard.en && !(act === "size" && arg === qcard.en)) {
      if (arg !== qcard.answer && arg !== qcard.en) {
        S.moonChoice = arg;
        S.glowId = qcard.en;
        S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
        render();
        return;
      }
    }
    onCorrect(qcard, "card:" + S.run.id + ":" + S.run.index, false);
    S.run.phase = "reveal";
    S.screen = "reveal";
    save();
    render();
    return;
  }
  if (act === "choice") {
    var acard = currentCard();
    var astep = currentStep();
    if (!acard) return;
    if (arg !== acard.answer) {
      var missed = E.noteMiss(S.run);
      S.run = missed.run;
      if (missed.retry) {
        S.moonChoice = arg;
        S.glowId = acard.answer;
        S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
        render();
        return;
      }
      E.applyMiss(S);
      S.run.wasMiss = true;
      S.run.rightRow = 0;
      S.moonChoice = arg;
      S.glowId = acard.answer;
      S.nodUntil = Date.now() + 600;
      try {
        var rq = JSON.parse(localStorage.getItem("naeReviewQueue") || "[]");
        localStorage.setItem("naeReviewQueue", JSON.stringify(E.reviewOnMiss(rq, acard)));
      } catch (e) { /* ignore */ }
      S.run.phase = "reveal";
      S.screen = "reveal";
      save();
      render();
      return;
    }
    onCorrect(acard, "card:" + S.run.id + ":" + S.run.index, false);
    S.run.wasMiss = false;
    S.run.phase = "reveal";
    S.screen = "reveal";
    save();
    speak(acard.en);
    render();
    return;
  }
  if (act === "sayit") {
    if (!advanceGate()) return;
    var scard = currentCard();
    onCorrect(scard, "say:" + S.run.id + ":" + S.run.index, true);
    S.run.wasMiss = false;
    S.run = E.advanceAfterReveal(S.run, Math.random);
    save();
    if (S.run.phase === "done") finishRun();
    else if (S.run.phase === "boss") { S.screen = "boss"; render(); }
    else { S.screen = "play"; hintMode = 0; render(); }
    return;
  }
  if (act === "two") {
    var tcard = currentCard();
    var prompt = S.run.two || {};
    if (arg !== prompt.answer) {
      S.moonChoice = arg;
      S.glowId = prompt.answer;
      S.nodUntil = Date.now() + 600;
      render();
      return;
    }
    if (!S.run.twoAwarded) {
      onCorrect(tcard, "card:" + S.run.id + ":" + S.run.index, false);
      S.run.twoAwarded = true;
      save();
    }
    S.glowId = arg;
    S.run.twoDone = true;
    render();
    return;
  }
  if (act === "twodone") {
    if (!advanceGate()) return;
    S.run.twoKey = "";
    S.run.two = null;
    S.run.twoDone = false;
    S.run.twoAwarded = false;
    S.run.wasMiss = false;
    S.run = E.advanceAfterReveal(S.run, Math.random);
    save();
    if (S.run.phase === "done") finishRun();
    else { S.screen = "play"; render(); }
    return;
  }
  if (act === "boss") {
    var bid = S.run.bossIds[S.run.bossIndex];
    var bcard = D.byId[bid];
    if (!bcard) return;
    if (arg !== bcard.answer) {
      var grace = D.encouragement[encI % D.encouragement.length];
      S.moonChoice = arg;
      S.glowId = bcard.answer;
      S.bubble = { en: D.wrongText.en + " " + grace.en, th: D.wrongText.th };
      S.nodUntil = Date.now() + 600;
      render();
      return;
    }
    if (!S.run.bossCleared[bid]) {
      onCorrect(bcard, "card:" + S.run.id + ":boss:" + S.run.bossIndex, false);
      S.run.bossCleared[bid] = 1;
    }
    S.moonChoice = "";
    S.glowId = "";
    S.bubble = null;
    var all = S.run.bossIds.every(function (cid) { return S.run.bossCleared[cid]; });
    if (!all) {
      S.run.bossIndex += 1;
      save();
      render();
      return;
    }
    var zoneKey = S.run.zone;
    var snap = S.run;
    var committed = E.beginKneel(S, D, zoneKey);
    S = committed.state;
    S.run = snap;
    var fin = E.finishZoneRun(S, D, snap, today);
    S = fin.state;
    sessionRuns += 1;
    S._rest = E.shouldRest(sessionRuns);
    S.screen = "kneel";
    S.kneelZone = zoneKey;
    playFile("audio/maxwell-boss-" + zoneKey + ".m4a");
    save();
    render();
    return;
  }
  if (act === "kneelgot") {
    if (!advanceGate()) return;
    S.kneelZone = "";
    save();
    afterRewards();
    return;
  }
  if (act === "got") {
    if (!advanceGate()) return;
    if (S.screen === "reveal" && S.run) {
      S.moonChoice = "";
      S.glowId = "";
      S.bubble = null;
      S.run = E.advanceAfterReveal(S.run, Math.random);
      hintMode = 0;
      save();
      if (S.run.phase === "done") { finishRun(); return; }
      if (S.run.phase === "boss") { S.screen = "boss"; render(); return; }
      S.screen = "play";
      render();
      return;
    }
    if (S.screen === "reward") {
      var pop = E.popReward(S);
      S = pop.state;
      save();
      afterRewards();
    }
    return;
  }
  if (act === "hint") {
    var hcard = currentCard() || (S.screen === "boss" && D.byId[S.run.bossIds[S.run.bossIndex]]);
    if (hcard && hintMode === 0 && (S.screen === "play" || S.screen === "boss")) {
      hintMode = 1;
      S.bubble = { en: (hcard.hint && hcard.hint.letters) || "", th: ui("itStartsWith").th };
      speak((ui("itStartsWith").en || "") + " " + ((hcard.hint && hcard.hint.sound) || ""));
      render();
      return;
    }
    nextBubble();
    render();
    return;
  }
  if (act === "replay") {
    var rc = currentCard();
    if (rc) speak(rc.en, true);
    return;
  }
  if (act === "keep") {
    var region = (S.lastZone && Object.keys(S.lastZone)[0]) || "r1";
    var z = E.chooseZone(S, D, region) || "phonics";
    startZone(z, region);
    return;
  }
  if (act === "restnow") { S.screen = "map"; render(); return; }
  if (act === "thaiok") {
    if (!S.thaiMarks) S.thaiMarks = {};
    S.thaiMarks[arg] = 1;
    save();
    render();
    return;
  }
  if (act === "buy") {
    var bought = E.buyItem(S, D, arg);
    S = bought.state;
    save();
    render();
    return;
  }
  if (act === "equip") {
    var eq = E.equipItem(S, D, arg);
    if (eq.ok) S = eq.state;
    save();
    render();
    return;
  }
  if (act === "toggle") {
    if (!S.settings) S.settings = { slowMode: false, restWeeks: false };
    S.settings[arg] = !S.settings[arg];
    save();
    render();
    return;
  }
  if (act === "export") {
    try {
      var blob = new Blob([JSON.stringify(persistable(S))], { type: "application/json" });
      var link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "nae-backup.json";
      link.click();
    } catch (e) { /* local only */ }
    return;
  }
  if (act === "readbak") {
    var input = document.getElementById("bakefile");
    if (!input || !input.files || !input.files[0]) return;
    var reader = new FileReader();
    reader.onload = function () {
      S.backupText = String(reader.result || "");
      var check = E.validateBackup(S.backupText, S);
      S.backupOk = check.ok;
      S.backupReason = check.ok ? ui("backupCompare").en : check.reason;
      render();
    };
    reader.readAsText(input.files[0]);
    return;
  }
  if (act === "usebak") {
    if (!S.backupText) return;
    var prep = E.prepareRestore(S, S.backupText);
    if (!prep.ok) { S.backupReason = prep.reason; render(); return; }
    try { localStorage.setItem("naeState.bak", JSON.stringify(prep.bak)); } catch (e) { /* skip */ }
    S = prep.state;
    S.screen = "menu";
    S.backupText = "";
    save();
    render();
    return;
  }
  if (act === "duel") {
    if (!S.duel) return;
    if (arg !== S.duel.heard) {
      var duelMiss = E.applyMiss(S);
      S.xp = duelMiss.state.xp;
      S.pips = duelMiss.state.pips;
      S.goldStars = duelMiss.state.goldStars;
      S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
      S.nodUntil = Date.now() + 600;
      save();
      render();
      return;
    }
    if (arg === S.duel.heard) {
      onCorrect({ id: "duel", zone: "soundDuel", mode: "picture-recall", type: "picture" }, "duel:" + (S.duel.round || 0) + ":" + S.duel.index, false);
      S.duel.index += 1;
      S.duel.heard = "";
      S.cheerUntil = Date.now() + 600;
    }
    save();
    render();
    return;
  }
  if (act === "hear") {
    if (S.duel && S.duel.heard) speak(S.duel.heard, true);
    return;
  }
  if (act === "duelnext") {
    if (!advanceGate()) return;
    var roundId = "round:" + today + ":" + (S.duelRounds || 0);
    if (!S.ledger[roundId]) {
      var xp = E.applyXp(S, D, 30, roundId);
      S = xp.state;
    }
    S.duelRounds = (S.duelRounds || 0) + 1;
    S.duel = null;
    save();
    render();
  }
}

document.getElementById("app").addEventListener("click", function (event) {
  var node = event.target;
  while (node && node !== event.currentTarget) {
    if (node.getAttribute && node.getAttribute("data-act")) {
      handle(node.getAttribute("data-act"), node.getAttribute("data-arg") || "");
      return;
    }
    node = node.parentNode;
  }
});

document.addEventListener("visibilitychange", function () {
  if (document.visibilityState === "hidden") {
    paused = true;
    try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) { /* ignore */ }
  }
});

window.__layoutAudit = function () {
  var out = { overlaps: [], small: [], thai: [], floating: [], scroll: [], screen: "" };
  var screen = document.querySelector(".screen");
  out.screen = screen ? screen.getAttribute("data-screen") : "";
  var taps = Array.prototype.slice.call(document.querySelectorAll("[data-tap]"));
  var rects = taps.map(function (el) {
    var r = el.getBoundingClientRect();
    return { r: r, act: el.getAttribute("data-act") || "" };
  }).filter(function (x) { return x.r.width > 0 && x.r.height > 0; });
  for (var i = 0; i < rects.length; i++) {
    if (rects[i].r.width < 43.5 || rects[i].r.height < 43.5) out.small.push(rects[i].act);
    for (var j = i + 1; j < rects.length; j++) {
      var a = rects[i].r;
      var b = rects[j].r;
      var overlap = a.left < b.right - 1 && a.right > b.left + 1 && a.top < b.bottom - 1 && a.bottom > b.top + 1;
      if (overlap) out.overlaps.push(rects[i].act + "|" + rects[j].act);
    }
  }
  Array.prototype.slice.call(document.querySelectorAll(".th")).forEach(function (el) {
    var size = parseFloat(window.getComputedStyle(el).fontSize);
    if (size < 16.9) out.thai.push(size);
  });
  var frame = document.querySelector(".scene-frame");
  if (frame) {
    var sb = frame.getBoundingClientRect();
    var seat = document.querySelector("[data-seat]");
    Array.prototype.slice.call(document.querySelectorAll("[data-prop]")).forEach(function (el) {
      var r = el.getBoundingClientRect();
      var mid = (r.top + r.bottom) / 2;
      if (mid < sb.top + sb.height * 0.38) out.floating.push(el.getAttribute("data-arg"));
      if (el.getAttribute("data-surface") === "bench" && seat) {
        var gap = seat.getBoundingClientRect().top - r.bottom;
        if (Math.abs(gap) > 6) out.floating.push("bench-gap:" + Math.round(gap));
      }
    });
  }
  if (screen && !screen.querySelector("[data-scroll-ok]")) {
    if (screen.scrollHeight > screen.clientHeight + 6) out.scroll.push(screen.scrollHeight - screen.clientHeight);
  }
  out.errors = window.__errors.slice();
  out.ok = !out.overlaps.length && !out.small.length && !out.thai.length && !out.floating.length && !out.scroll.length && !out.errors.length;
  return out;
};

window.__test = function () {
  var problems = [];
  if (!D || D.cards.length !== 211) problems.push("cards");
  ["ms-04", "ms-05", "ms-06"].forEach(function (id) {
    var card = D.byId[id];
    if (!card || !card.playable || card.showExample) problems.push(id);
  });
  if (problems.length) {
    console.log("FAIL " + problems.join(","));
    return "FAIL";
  }
  console.log("PASS");
  return "PASS";
};

function boot() {
  today = todayStamp(new Date());
  Promise.all([
    fetch("data/cards.json").then(function (r) { return r.json(); }),
    fetch("data/daily-verses.json").then(function (r) { return r.json(); }),
    fetch("assets/title.svg").then(function (r) { return r.text(); })
  ]).then(function (all) {
    D = E.loadModel(all[0], all[1]);
    titleSvg = all[2];
    inline = Object.assign({}, (D.picPlan && D.picPlan.inlineSvg) || {}, (D.picPlan && D.picPlan.trophyInlineSvg) || {});
    var tex = D.picPlan.uiInlineSvg && D.picPlan.uiInlineSvg.tex;
    if (tex) document.getElementById("texMount").innerHTML = tex;
    return loadState();
  }).then(function (saved) {
    S = saved && saved.schema === 5020 ? E.reconcile(saved, D) : E.freshState(D);
    var day = E.rollDay(S, today);
    S = day.state;
    S.welcomeShow = !!(day.missed && day.first);
    S.verseDue = !S.ledger["verse:" + today];
    S.screen = "title";
    save();
    render();
    try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e) { /* ignore */ }
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("sw.js").catch(function () { /* offline shell is optional */ });
    }
  }).catch(function (err) {
    window.__errors.push(String(err && err.message || err));
    document.getElementById("app").innerHTML = "<div class='screen' data-screen='error'><p class='th' lang='th'>The game files did not load.</p></div>";
  });
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
