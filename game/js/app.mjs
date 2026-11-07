import * as E from "./engine.mjs";
import { sceneSvg, pictureHtml, escapeText, coinRow, guardianKneel, zoneEmblem } from "./art.mjs";

window.__net = [];
var nativeFetch = window.fetch ? window.fetch.bind(window) : null;
if (nativeFetch) {
  window.fetch = function (url) {
    window.__net.push(String(url));
    return nativeFetch.apply(window, arguments);
  };
}
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
function icon(name) {
  var paths = {
    leaf: "<path d='M32 8c12 8 16 20 12 32-10 2-20-2-24-12 8-2 14-6 12-20z' fill='#17633A'/><path d='M20 36c8 8 16 10 28 8' fill='none' stroke='#10170F' stroke-width='3'/>",
    replay: "<path d='M18 32a14 14 0 1 0 4-10' fill='none' stroke='#10170F' stroke-width='3'/><path d='M16 14v10h10' fill='none' stroke='#10170F' stroke-width='3'/>",
    emblem: "<circle cx='32' cy='32' r='18' fill='#FFCC33' stroke='#10170F' stroke-width='3'/>",
    heart: "<path d='M32 50l-14-14a10 10 0 0 1 14-14 10 10 0 0 1 14 14z' fill='#FFCC33' stroke='#10170F' stroke-width='3'/>",
    arrow: "<path d='M8 24h28l-8-8M36 24l-8 8' fill='none' stroke='#B7860B' stroke-width='4'/>",
    gem: "<path d='M32 8l14 12-14 32L18 20z' fill='#3D7FD9' stroke='#10170F' stroke-width='3'/>",
    star: "<path d='M32 8l5 14h14l-11 8 4 14-12-8-12 8 4-14-11-8h14z' fill='#FFCC33' stroke='#10170F' stroke-width='2'/>",
    flame: "<path d='M32 6c8 10 4 16 8 24 6 10-2 24-8 26-10-2-16-12-12-22 4-2 6-8 4-14 4 4 6 6 8-14z' fill='#F08A5A' stroke='#10170F' stroke-width='3'/>",
    gift: "<rect x='14' y='24' width='36' height='28' fill='#FFCC33' stroke='#10170F' stroke-width='3'/><path d='M32 24v28M14 34h36' stroke='#10170F' stroke-width='3'/>"
  };
  return "<svg class='ico' viewBox='0 0 64 64' aria-hidden='true'>" + (paths[name] || paths.emblem) + "</svg>";
}
function bonusLine(words) {
  var map = { Hint: "bonusHint", Hint2: "bonusHint2", Retry: "bonusRetry", Retry2: "bonusRetry2", Star: "bonusStar", Star2: "bonusStar2", Streak: "bonusStreak", Streak2: "bonusStreak2", Slow: "bonusSlow", Respell: "bonusRespell" };
  return String(words || "").split(/\s+/).filter(Boolean).map(function (word) {
    var row = map[word] ? ui(map[word]) : { en: "", th: "" };
    return "<div class='en'>" + escapeText(row.en) + "</div><div class='th' lang='th'>" + escapeText(row.th) + "</div>";
  }).join("");
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
function resumeCtx(ctx) {
  try {
    if (!ctx || typeof ctx.resume !== "function") return;
    if (ctx.state && ctx.state !== "suspended" && ctx.state !== "interrupted") return;
    var pending = ctx.resume();
    if (pending && typeof pending.catch === "function") pending.catch(function () {});
  } catch (e) { /* a rejected resume must not surface */ }
}
function wake() {
  try {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!window.__ac) window.__ac = new AC();
    resumeCtx(window.__ac);
    var buf = window.__ac.createBuffer(1, 1, 22050);
    var src = window.__ac.createBufferSource();
    src.buffer = buf;
    src.connect(window.__ac.destination);
    src.start();
    try {
      if (window.speechSynthesis && window.SpeechSynthesisUtterance) {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
      }
    } catch (speakErr) { /* empty wake utterance is optional */ }
  } catch (e) { /* audio is optional */ }
}
function thud() {
  try {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!window.__ac) window.__ac = new AC();
    var ctx = window.__ac;
    resumeCtx(ctx);
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
function voiceReady() {
  try {
    if (window.__forceSilent) return false;
    if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) return false;
    if (typeof window.speechSynthesis.getVoices !== "function") return false;
    var voices = window.speechSynthesis.getVoices() || [];
    return voices.length > 0;
  } catch (e) { return false; }
}
function speak(text, slow) {
  var bonus = D ? E.gearBonuses(S, D) : { slow: false };
  var rate = bonus.slow ? 0.5 : (S && S.settings && S.settings.slowMode ? 0.6 : 0.85);
  if (slow) rate = Math.min(rate, 0.6);
  var synth = null;
  try {
    if (voiceReady()) {
      synth = {
        cancel: function () { window.speechSynthesis.cancel(); },
        speak: function (line) {
          var u = new SpeechSynthesisUtterance(line);
          u.lang = "en-US";
          u.rate = rate;
          u.onerror = function () {
            if (S && S.run && S.run.heardIndex === S.run.index) {
              S.run.listenFallback = true;
              render();
            }
          };
          window.speechSynthesis.speak(u);
        }
      };
    }
  } catch (e) { synth = null; }
  var ok = E.speakEnglish(text, synth);
  if (ok && text) {
    if (!window.__spoken) window.__spoken = [];
    window.__spoken.push(text);
  }
  return ok;
}
function playFile(rel) {
  E.playClip(rel, function (url) { return fetch(url); }).then(function (ok) {
    if (!ok) return;
    return fetch(rel).then(function (res) { return res.arrayBuffer(); }).then(function (buf) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      if (!window.__ac) window.__ac = new AC();
      resumeCtx(window.__ac);
      return window.__ac.decodeAudioData(buf).then(function (audio) {
        resumeCtx(window.__ac);
        var src = window.__ac.createBufferSource();
        src.buffer = audio;
        src.connect(window.__ac.destination);
        src.start();
      }).catch(function () { /* clip decode never blocks */ });
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
var saveChain = Promise.resolve();
function save() {
  S.rev = (Number(S.rev) || 0) + 1;
  S.savedAt = Date.now();
  var copy = persistable(S);
  var rev = copy.rev;
  try { localStorage.setItem("naeState", JSON.stringify(copy)); } catch (e) { /* mirror skipped */ }
  saveChain = saveChain.then(function () {
    return idb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction("kv", "readwrite");
        var store = tx.objectStore("kv");
        var rq = store.get("state");
        rq.onsuccess = function () {
          var current = rq.result;
          if (!current || (Number(current.rev) || 0) <= rev) store.put(copy, "state");
        };
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }).catch(function () { /* a late write must not replace a newer one */ });
}
function readMirror() {
  try { return JSON.parse(localStorage.getItem("naeState") || "null"); } catch (e) { return null; }
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
    return E.pickNewerState(rec, readMirror());
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
    "<div class='hud-side'><div class='count nowrap'>" + icon("gem") + " " + gems + "</div>" + coinRow(S.pips || 0) + "</div>" +
    "<div class='portrait" + cheer + nod + "'>" + heroSvg() + "</div>" +
    "<div class='hud-side level-side' style='align-items:flex-end'><div class='level-label nowrap'>Level " + S.level + "</div>" +
    "<div class='xpbar" + (S.pipGlow ? " pip-glow" : "") + "'><span style='width:" + xpFrac(S.xp) + "%'></span></div>" +
    "<div class='count nowrap'>" + icon("star") + " " + S.goldStars + "</div></div></header>";
}
function banner(en, th) {
  return "<div class='banner'><div class='en banner-en'>" + escapeText(en || "") + "</div><div class='th banner-th' lang='th'>" + escapeText(th || "") + "</div></div>";
}
function bubbleHtml() {
  if (!S.bubble) return "";
  return "<div class='bubble'><div class='en'>" + escapeText(S.bubble.en || "") + "</div><div class='th' lang='th'>" + escapeText(S.bubble.th || "") + "</div></div>";
}

function countProp(thing) {
  if (thing === "cows") {
    return "<svg class='drawn' viewBox='0 0 64 40' aria-hidden='true'><ellipse cx='30' cy='24' rx='16' ry='10' fill='#F6E9C8' stroke='#10170F' stroke-width='3'/><circle cx='46' cy='18' r='7' fill='#F6E9C8' stroke='#10170F' stroke-width='3'/><path d='M18 28v8M34 28v8' stroke='#10170F' stroke-width='3'/></svg>";
  }
  if (thing === "hats") {
    return "<svg class='drawn' viewBox='0 0 64 40' aria-hidden='true'><path d='M8 28h48l-6 6H14z' fill='#C46B4A' stroke='#10170F' stroke-width='3'/><path d='M22 28c0-12 20-12 20 0' fill='#E8B84A' stroke='#10170F' stroke-width='3'/></svg>";
  }
  return "<svg class='drawn' viewBox='0 0 64 40' aria-hidden='true'><path d='M8 14h48l-4 8H12z' fill='#C8A26A' stroke='#10170F' stroke-width='3'/><path d='M14 22h36l-4 14H18z' fill='#E8B84A' stroke='#10170F' stroke-width='3'/><path d='M24 14c0-8 16-8 16 0' fill='none' stroke='#10170F' stroke-width='3'/></svg>";
}
function propButton(id, surface, left, correct, inner, act) {
  var cls = "prop on-" + surface;
    if (S.glowId === id) cls += " glow-gold";
    if (S.moonChoice === id) cls += " glow-moon";
    if (S.wiggleId === id) cls += " wiggle";
  return "<button class='" + cls + "' data-tap data-prop data-surface='" + surface + "' data-act='" + (act || "prop") + "' data-arg='" + escapeText(id) + "' data-correct='" + (correct ? "1" : "0") + "' style='left:" + left + "'>" +
    inner + "<i class='shadow'></i></button>";
}
function sceneSlots(step) {
  var ids = sceneMates(step);
  if (step.kind === "letter") {
    var word = String((D.byId[step.id] || {}).en || "");
    var gotN = S.run.spell && S.run.spell.id === step.id ? S.run.spell.got.length : 0;
    var px = Math.max(28, Math.round(28 + 16 * (word ? gotN / word.length : 0)));
    var card = D.byId[step.id];
    return "<div class='bench-seat' data-seat='1'><span class='grown' style='width:" + px + "px;height:" + px + "px'>" + pictureHtml(card && card.pic, inline) + "</span></div>";
  }
  if (step.kind === "count") {
    var counted = E.countPrompt(D.byId[step.id], D.ui);
    var n = counted.n || step.countN || 0;
    var prop = countProp(counted.thing);
    var html = "";
    var i;
    for (i = 0; i < n; i++) {
      var col = i % 5;
      var cols = Math.min(n, 5);
      var left = 30 + (cols === 1 ? 18 : col * (58 / cols));
      var bottom = i < 5 ? "6%" : "16%";
      html += "<span class='count-item' data-count-item='1' data-thing='" + escapeText(counted.thing) + "' style='left:" + left + "%;bottom:" + bottom + "'>" + prop + "<i class='shadow'></i></span>";
    }
    return html;
  }
  if (step.kind === "size") {
    var which = String((D.byId[step.id] || {}).en || "").toLowerCase() === "small" ? "small" : "big";
    var sort = (D.meta && D.meta.sizeSort && D.meta.sizeSort[which]) || [];
    var held = D.byId[sort[0]] || D.byId[step.id];
    return "<div class='bench-seat' data-seat='1'></div><span class='held-pic " + which + "' data-held='1'>" + pictureHtml(held && held.pic, inline) + "</span>";
  }
  var pos = [
    { left: "38%", surface: "ground" },
    { left: "54%", surface: "ground" },
    { left: "70%", surface: "ground" },
    { left: "50%", surface: "bench" },
    { left: "72%", surface: "bench" }
  ];
  var props = ids.map(function (id, index) {
    var card = D.byId[id];
    var p = pos[index] || pos[0];
    return propButton(id, p.surface, p.left, id === step.id, pictureHtml(card && card.pic, inline), "prop");
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
  if (step.listen && S.run.heardIndex !== S.run.index) {
    S.run.heardIndex = S.run.index;
    S.run.listenFallback = !speak(card.en);
  }
  var prompt = E.promptFor(card, D.ui, step.listen && step.kind === "scene" && !S.run.listenFallback);
  if (step.listen && S.run.listenFallback) {
    var find = ui("listenFind");
    prompt = { en: (find.en ? find.en + " " : "") + card.en, th: (find.th ? find.th + " " : "") + (card.thDef || card.th) };
  }
  var respellLine = bonuses.respell && card.respell ? "<div class='en' style='color:#8A6200'>" + escapeText(card.respell) + "</div>" : "";
  if (step.kind === "letter") prompt = { en: ui("spellIt").en, th: ui("spellIt").th };
  if (step.kind === "count") prompt = E.countPrompt(card, D.ui);
  if (step.kind === "size") prompt = { en: ui("bigOrSmall").en, th: ui("bigOrSmall").th };
  var extra = "";
  if (step.kind === "letter") extra = letterPads(card);
  if (step.kind === "count") extra = countPads(card, step);
  if (step.kind === "size") extra = sizePads(card);
  return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='stage'><div class='scene-frame' data-tod='" + tod + "'>" + sceneSvg(kind, tod) +
    "<div class='hero-fig'>" + heroSvg() + "<i class='shadow'></i></div>" +
    sceneSlots(step) + "</div></div>" +
    "<div class='qcard'><div class='prompt'>" + bi(prompt.en, prompt.th) + respellLine + bubbleHtml() + extra +
    (step.listen && !S.run.listenFallback ? "<button class='choice' data-tap data-act='showword'>" + bi(ui("listenFind").en, ui("listenFind").th) + "</button>" : "") + "</div>" +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='replay' aria-label='" + escapeText(ui("replay").en) + "'>" + icon("replay") + "</button>" +
    "<button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>" + icon("leaf") + "<span class='hint-label th' lang='th'>" + escapeText(ui("wordsForYou").th) + "</span></button></div></div></div>";
}
function letterPads(card) {
  var word = String(card.en || "");
  if (!S.run.spell || S.run.spell.id !== card.id) S.run.spell = { id: card.id, got: "", bank: E.letterBank(word) };
  var got = S.run.spell.got;
  var blanks = word.split("").map(function (ch, i) { return got.charAt(i) || "_"; }).join(" ");
  var cursor = 0;
  return "<div class='letters'>" + escapeText(blanks) + "</div><div class='choices letter-choices'>" + S.run.spell.bank.map(function (ch) {
    var spent = got.charAt(cursor) === ch;
    if (spent) cursor += 1;
    return "<button class='choice" + (spent ? " spent" : "") + "' data-tap data-act='letter' data-arg='" + escapeText(ch) + "'" + (spent ? " disabled" : "") + ">" + escapeText(ch) + "</button>";
  }).join("") + "</div>";
}
function countPads(card) {
  var opts = E.countPlates(card.en);
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
      "<div class='en' style='color:#8A6200'>" + escapeText(card.respell || "") + "</div>" +
      (card.reply ? "<div class='reply'><div class='en'>" + escapeText(card.reply.en || "") + "</div><div class='th' lang='th'>" + escapeText(card.reply.th || "") + "</div></div>" : "") + "</div>" +
      bubbleHtml() +
      "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>" + icon("leaf") + "</button>" +
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
  var pic = card.pic ? pictureHtml(card.pic, inline) : "<div class='emblem zone-emblem'>" + zoneEmblem(zone) + "<div class='th emblem-th' lang='th'>" + escapeText(stemTh) + "</div></div>";
  var serverLine = card.type === "server-talk" ? "<div class='prompt'>" + bi(card.en, card.th) + "</div>" : "";
  return "<div class='screen' data-screen='play'>" + banner(zone.name, zone.nameTh) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='ask'><div class='pic-frame'>" + pic + "</div>" +
    (stemEn || card.type !== "server-talk" ? "<div class='ask-thai th' lang='th'>" + escapeText(card.type === "server-talk" ? stemTh : stemTh) + "</div>" : "") +
    serverLine +
    "<div class='choices'>" + choices + "</div>" + bubbleHtml() +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>" + icon("leaf") + "<span class='hint-label th' lang='th'>" + escapeText(ui("wordsForYou").th) + "</span></button><div></div></div></div></div>";
}

function renderReveal() {
  var card = S.revealOverride ? D.byId[S.revealOverride] : currentCard();
  if (!card) { S.screen = "map"; return renderMap(); }
  if (S.spokeReveal !== card.id + ":" + (S.revealOverride || (S.run && S.run.index))) {
    S.spokeReveal = card.id + ":" + (S.revealOverride || (S.run && S.run.index));
    speak(card.en);
  }
  document.body.setAttribute("data-theme", "arena");
  var head = S.run && S.run.wasMiss ? D.wrongText : (D.encouragement[encI % D.encouragement.length] || D.rewardText);
  if (!S.run.wasMiss) encI += 1;
  var trap = S.run && S.run.wasMiss && card.trapNote ? "<div class='th' lang='th'>" + escapeText(card.trapNote) + "</div>" : "";
  var say = (S.run && !S.revealOverride && S.run.index < 10) ? "<div class='en'>" + escapeText(ui("sayItOutLoud").en) + "</div><div class='th' lang='th'>" + escapeText(ui("sayItOutLoud").th) + "</div>" : "";
  return "<div class='screen' data-screen='reveal'>" + banner(head.en, head.th) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='ask'><div class='pic-frame'>" + pictureHtml(card.pic, inline) + "</div>" +
    "<div class='prompt' style='text-align:center'><div class='en' style='font-size:36px;color:#10170F'>" + escapeText(card.en) + "</div>" +
    "<div class='en' style='color:#8A6200'>" + escapeText(card.respell || "") + "</div>" +
    "<div class='th' lang='th'>" + escapeText(card.th) + "</div>" + trap + say + "</div>" +
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='replay' aria-label='" + escapeText(ui("replay").en) + "'>" + icon("replay") + "<span class='hint-label th' lang='th'>" + escapeText(ui("replay").th) + "</span></button>" +
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
    "<div class='row-actions'><button class='hint-btn' data-tap data-act='hint' aria-label='" + escapeText(ui("hintButton").en) + "'>" + icon("leaf") + "</button>" +
    "<button class='metal' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button></div></div></div>";
}

function verseBits(verse) {
  var gloss = "";
  if (verse.enGloss) gloss += "<div class='tag'>" + escapeText(verse.enGloss) + "</div>";
  if (verse.thGloss) gloss += "<div class='tag th' lang='th'>" + escapeText(verse.thGloss) + "</div>";
  return "<div class='en'>" + escapeText(verse.ref || "") + "</div>" +
    "<div class='verse-en en'>" + escapeText(verse.en || "").split("\n").join("<br>") + "</div><div class='tag'>(ESV)</div>" +
    "<div class='th' lang='th'>" + escapeText(verse.th || "").split("\n").join("<br>") + "</div><div class='tag'>(THSV11)</div>" +
    gloss +
    "<div class='en'>" + escapeText(ui("askMax").en) + "</div><div class='th' lang='th'>" + escapeText(ui("askMax").th) + "</div>";
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
      "<div class='verse-body' data-scroll-ok>" + verseBits(verse) + "</div>" +
      "<div class='row-actions'><button class='hint-btn' data-tap data-act='replayverse' aria-label='" + escapeText(ui("replay").en) + "'>" + icon("replay") + "</button>" +
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
    "<div class='top-tools'><button class='hearth' data-tap data-act='hearth' aria-label='" + escapeText(ui("verseGift").en) + "'>" + icon("heart") + "</button></div>" +
    "<div class='logs'></div>" + gift +
    "<div class='hero-band' aria-label='" + escapeText(ui("chooseHero").en) + "'>" +
    heroButton("sam", pack.sam, ui("heroName")) + heroButton("nancy", pack.nancy, ui("heroNancy")) + "</div>" +
    "<div class='stack'>" +
    "<button class='metal' data-tap data-act='gear'>" + plate(ui("gear").en, ui("gear").th) + "</button>" +
    "<button class='metal' data-tap data-act='shop'>" + plate(ui("pantry").en, ui("pantry").th) + "</button>" +
    "<button class='metal' data-tap data-act='map'>" + plate(ui("titleMap").en, ui("titleMap").th) + "<span class='arrow-cue'>" + icon("arrow") + "</span></button>" +
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
    else if (arrow === r.id) cue = "<span class='arrow-cue'>" + icon("arrow") + "</span>";
    return "<button class='map-row" + (soft ? " soft" : "") + "' data-tap data-act='region' data-arg='" + r.id + "'>" +
      "<span class='dot' style='background:" + r.color + "'></span><span class='label'>" + bi(r.en, r.th) +
      (soft ? "<span class='th next' lang='th'>" + escapeText(ui("comingNext").th) + "</span>" : "") + "</span>" + cue + "</button>";
  }).join("");
  return "<div class='screen' data-screen='map'><div class='map'>" +
    banner(ui("titleMap").en, ui("titleMap").th) +
    "<div class='logs'></div>" +
    "<div class='hud' data-xp='" + S.xp + "' data-stars='" + S.goldStars + "'><button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button>" +
    "<div class='count'>" + icon("gem") + E.gemCount(S, D) + " " + icon("star") + S.goldStars + " " + icon("flame") + (S.streak && S.streak.n || 0) + " Level " + S.level + "</div>" +
    "<button class='hearth' data-tap data-act='hearth' aria-label='" + escapeText(ui("verseGift").en) + "'>" + icon("heart") + "</button></div>" +
    (S.updateReady ? "<button class='metal' data-tap data-act='update'>" + plate(ui("updateReady").en, ui("updateReady").th) + "</button>" : "") +
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
      body = verseBits(scroll);
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
  return "<div class='screen' data-screen='rest'>" + banner(D.restScreen.en, D.restScreen.th) +
    "<div class='ask'><div class='panel'>" +
    "<div class='verse-body' data-scroll-ok>" + verseBits(verse) + "</div>" +
    "<button class='gold-btn' data-tap data-act='keep'>" + plate(ui("keepGoing").en, ui("keepGoing").th) + "</button>" +
    "<button class='metal' data-tap data-act='restnow'>" + plate(ui("restNow").en, ui("restNow").th) + "</button></div></div></div>";
}

function renderScroll() {
  var scroll = S.openScroll;
  if (!scroll) { S.screen = "character"; return renderGear(); }
  document.body.setAttribute("data-theme", "menu");
  return "<div class='screen' data-screen='scroll'>" + banner(ui("scrolls").en, ui("scrolls").th) +
    "<div class='ask'><div class='panel' data-scroll-ok>" + verseBits(scroll) +
    "<button class='gold-btn' data-tap data-act='scrollback'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div></div>";
}
function renderKneel() {
  var zone = D.zoneByKey[S.kneelZone] || {};
  var name = zone.boss && zone.boss.name ? zone.boss.name : { en: "", th: "" };
  var tint = { phonics: "#7FD38B", "colors-shapes": "#F5A3C7", numbers: "#7FB8F5", "sight-words": "#F5D06B", "baby-hospital": "#F2B8A0" }[S.kneelZone] || "#7FD38B";
  document.body.setAttribute("data-theme", "arena");
  return "<div class='screen' data-screen='kneel'>" + banner(name.en, name.th) +
    "<div class='stage'><div class='scene-frame'>" + sceneSvg(E.sceneKind(S.kneelZone, 0), "a") +
    "<div class='hero-fig' style='left:8%'>" + heroSvg() + "</div>" +
    "<div class='kneel-fig'>" + guardianKneel(tint) + "</div></div></div>" +
    "<div class='qcard'><div class='prompt'>" + bi(name.en, name.th) + "</div>" +
    "<button class='gold-btn' data-tap data-act='kneelgot'>" + plate(D.gotItText.en, D.gotItText.th) + "</button></div></div>";
}

function renderShop() {
  document.body.setAttribute("data-theme", "menu");
  var items = (D.pantry.items || []).map(function (item) {
    var owned = (S.pantryOwned || []).indexOf(item.id) >= 0;
    var label = owned ? ui("wearIt") : ui("getFor");
    function fill(s) { return String(s || "").split("{n}").join(String(item.stars)); }
    var art = String(item.pic || "").indexOf("svg:") === 0 ? pictureHtml(item.pic, inline) : "<div class='emoji-pic'>" + escapeText(item.pic || "") + "</div>";
    return "<button class='trophy' data-tap data-act='buy' data-arg='" + item.id + "'>" + art +
      bi(item.en, item.th) + "<div class='en'>" + escapeText(owned ? label.en : fill(label.en)) + "</div><div class='th' lang='th'>" + escapeText(owned ? label.th : fill(label.th)) + "</div></button>";
  }).join("");
  var gear = E.shopRows(S, D).map(function (row) {
    var slots = row.slots.map(function (slot) {
      var price = slot.owned ? "✓" : (slot.tier === 1 ? "" : (icon("star") + " " + slot.cost));
      var cls = "trophy" + (slot.silhouette ? " sil" : "");
      var ask = ui("getFor");
      var label = slot.silhouette ? String(ask.en || "").split("{n}").join(String(slot.cost)) : slot.name;
      var labelTh = slot.silhouette ? String(ask.th || "").split("{n}").join(String(slot.cost)) : (slot.th || "");
      return "<button class='" + cls + "' data-tap data-act='buy' data-arg='" + slot.id + "' data-open='" + (slot.tierOpen && row.open ? "1" : "0") + "'>" +
        "<div class='en'>" + escapeText(label) + "</div><div class='th' lang='th'>" + escapeText(labelTh) + "</div>" +
        "<div class='en'>" + price + "</div>" + bonusLine(slot.bonus) + "</button>";
    }).join("");
    return "<div class='en'>" + escapeText(row.row) + "</div><div class='weapon-row'>" + slots + "</div>";
  }).join("");
  return "<div class='screen' data-screen='shop'>" + banner(ui("pantry").en, ui("pantry").th) +
    "<div class='sheet'><div class='count star-count' data-star-count='" + S.goldStars + "'>" + icon("star") + "<span>" + S.goldStars + "</span></div><div class='pane' data-scroll-ok><div class='grid3'>" + items + "</div>" + gear + "</div></div>" +
    "<div class='footer'><button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button></div></div>";
}

function goalLine(t) {
  var u = t.unlock || {};
  var pack = null;
  if (u.type === "level") pack = ui("unlocksAtLevel");
  else if (u.type === "pipFills") pack = ui("unlocksPips");
  else if (u.type === "bossesWon") pack = ui("unlocksBosses");
  else if (u.type === "zoneRight") pack = ui("unlocksZoneRight");
  if (!pack) return "";
  function fill(s) { return String(s || "").split("{n}").join(String(u.n || "")).split("{zone}").join(String(u.zone || "")); }
  return "<div class='en'>" + escapeText(fill(pack.en)) + "</div><div class='th' lang='th'>" + escapeText(fill(pack.th)) + "</div>";
}
function renderGear() {
  document.body.setAttribute("data-theme", "menu");
  var tab = S.charTab || "gems";
  var tabs = ["gems", "gear", "themes", "titles", "scrolls", "pantry"];
  var tabButtons = tabs.map(function (name) {
    var label = ui(name === "pantry" ? "pantry" : name);
    return "<button class='metal" + (tab === name ? " on" : "") + "' data-tap data-act='tab' data-arg='" + name + "'>" + plate(label.en, label.th) + "</button>";
  }).join("");
  var shelfIds = [];
  (D.trophies || []).forEach(function (item) {
    if (item.cat === "gear" && (S.owned || []).indexOf(item.id) >= 0 && shelfIds.indexOf(item.id) < 0) shelfIds.push(item.id);
  });
  (S.owned || []).slice(-4).forEach(function (id) { if (shelfIds.indexOf(id) < 0) shelfIds.push(id); });
  var shelf = shelfIds.map(function (id) {
    var t = null;
    (D.trophies || []).some(function (item) { if (item.id === id) { t = item; return true; } return false; });
    if (!t) return "";
    return "<span class='trophy' data-prop='shelf'>" + pictureHtml(t.pic || ("svg:" + t.id), inline) + "</span>";
  }).join("");
  var body = "";
  if (tab === "gear") {
    var gearCards = (D.trophies || []).filter(function (t) { return t.cat === "gear" || !t.cat; }).map(function (t) {
      var owned = (S.owned || []).indexOf(t.id) >= 0;
      return "<button class='trophy' data-tap data-act='equip' data-arg='" + t.id + "' data-trophy='" + t.id + "'>" +
        pictureHtml(t.pic || ("svg:" + t.id), inline) + bi(t.en, t.th || t.thGloss || "") +
        (owned ? "<div class='en'>✓</div>" : goalLine(t)) + "</button>";
    }).join("");
    body = "<div class='grid3'>" + gearCards + "</div>" + E.shopRows(S, D).map(function (row) {
      return "<div class='en'>" + escapeText(row.row) + "</div><div class='weapon-row'>" + row.slots.map(function (slot) {
        var ask = ui("getFor");
        var gname = slot.silhouette ? String(ask.en || "").split("{n}").join(String(slot.cost)) : slot.name;
        var gth = slot.silhouette ? String(ask.th || "").split("{n}").join(String(slot.cost)) : slot.th;
        return "<button class='trophy" + (slot.silhouette ? " sil" : "") + "' data-tap data-act='buy' data-arg='" + slot.id + "'>" +
          pictureHtml("svg:" + slot.id, inline) + bi(gname, gth) +
          "<div class='en'>" + (slot.owned ? "✓" : (slot.tier === 1 ? "" : (icon("star") + " " + slot.cost))) + "</div></button>";
      }).join("") + "</div>";
    }).join("");
  } else if (tab === "scrolls") {
    var credit = (D.verses && D.verses.attribution) || {};
    body = (S.scrolls || []).length ? (S.scrolls || []).map(function (scroll) {
      var tag = scroll.enSource || scroll.thSource ? "<div class='tag'>" + escapeText(scroll.enSource || "") + " " + escapeText(scroll.thSource || "") + "</div>" : "";
      return "<button class='trophy' data-tap data-act='readscroll' data-arg='" + escapeText(scroll.id) + "'>" + bi(scroll.ref, "") + tag + "</button>";
    }).join("") : "<div class='th' lang='th'>" + escapeText(ui("scrollsEmpty").th) + "</div>";
    body += "<div class='tag' data-attribution='1'>" + escapeText(credit.esv || "") + "</div><div class='tag' data-attribution='1'>" + escapeText(credit.thsv11 || "") + "</div>";
  } else if (tab === "pantry") {
    body = "<button class='metal' data-tap data-act='shop'>" + plate(ui("pantry").en, ui("pantry").th) + "</button>";
  } else {
    var cat = tab === "titles" ? "titles" : tab === "themes" ? "themes" : "gems";
    body = "<div class='grid3'>" + (D.trophies || []).filter(function (t) { return t.cat === cat; }).map(function (t) {
      var owned = (S.owned || []).indexOf(t.id) >= 0;
      return "<button class='trophy' data-tap data-act='equip' data-arg='" + t.id + "' data-trophy='" + t.id + "'>" + pictureHtml(t.pic, inline) +
        bi(t.en, t.th || t.thGloss || "") + (owned ? "<div class='en'>✓</div>" : goalLine(t)) + "</button>";
    }).join("") + "</div>";
  }
  return "<div class='screen' data-screen='character'>" + banner(ui("character").en, ui("character").th) +
    "<div class='sheet'><div class='portrait' style='margin:0 auto'>" + heroSvg() + "</div>" +
    "<div class='en'>" + escapeText(ui("earnedShelf").en) + "</div><div class='shop-row'>" + shelf + "</div>" +
    "<div class='grid3'>" + tabButtons + "</div>" +
    "<div class='pane' data-scroll-ok>" + body +
    "<button class='metal' data-tap data-act='backup'>" + plate(ui("backup").en, ui("backup").th) + "</button>" +
    "<button class='metal' data-tap data-act='toggle' data-arg='slowMode' aria-pressed='" + (S.settings.slowMode ? "true" : "false") + "'>" + plate(ui("slowMode").en, ui("slowMode").th) + "</button>" +
    "<button class='metal' data-tap data-act='toggle' data-arg='restWeeks' aria-pressed='" + (S.settings.restWeeks ? "true" : "false") + "'>" + plate(ui("restWeeks").en, ui("restWeeks").th) + "</button></div></div>" +
    "<div class='footer'><button class='metal' data-tap data-act='back'>" + plate(ui("back").en, ui("back").th) + "</button></div></div>";
}

function renderBackup() {
  document.body.setAttribute("data-theme", "menu");
  var review = E.thaiReviewQueue(D);
  var pending = E.pendingMaxwell(review.needsMaxwell, E.SETTLED_APPROVALS.needsMaxwell);
  var ids = pending.map(function (id) {
    return "<li class='th' data-settled='0' lang='th'>" + escapeText(id) + "</li>";
  }).join("");
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
    (pending.length ? "<div class='en'>" + escapeText(ui("needsMaxwell").en) + "</div><ul data-pending='1'>" + ids + "</ul>" : "") +
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
      "<button class='metal' data-tap data-act='duelmap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button></div></div>";
  }
  if (!S.duel.heard) {
    S.duel.heard = Math.random() < 0.5 ? pair.a : pair.b;
    speak(S.duel.heard);
  }
  var pics = pair.pics || [];
  return "<div class='screen' data-screen='duel'>" + banner(ui("soundDuel").en, ui("soundDuel").th) + hud(false) +
    "<button class='metal back-slim' data-tap data-act='tomap'>" + plate(ui("toMap").en, ui("toMap").th) + "</button>" +
    "<div class='ask'><div class='prompt'>" + bi(ui("echoKnight").en, ui("echoKnight").th) + "</div>" +
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
  else if (S.screen === "scroll") html = renderScroll();
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
  if (paused && act !== "resume") return;
  S.lock = true;
  window.__lockDuring = true;
  try {
    dispatch(act, arg);
  } finally {
    var held = S;
    requestAnimationFrame(function () { if (held) held.lock = false; });
  }
}
function dispatch(act, arg) {
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
    S.hearthFlip = !S.hearthFlip;
    if (S.hearthFlip && S.scrolls && S.scrolls.length) {
      var verse = S.scrolls[0];
      S.bubble = { en: verse.en, th: verse.th };
    } else {
      var line = D.encouragement[encI % D.encouragement.length];
      encI += 1;
      S.bubble = { en: line.en, th: line.th };
    }
    render();
    return;
  }
  if (act === "scrollback") {
    var same = (S.xp + ":" + S.goldStars + ":" + S.giftGems) === S._counters;
    S.openScroll = null;
    S.screen = "character";
    S.charTab = "scrolls";
    if (!same) S.xp = S.xp;
    render();
    return;
  }
  if (act === "readscroll") {
    var scroll = (S.scrolls || []).filter(function (item) { return item.id === arg; })[0];
    if (!scroll) return;
    var before = S.xp + ":" + S.goldStars + ":" + S.giftGems;
    S.openScroll = scroll;
    S.screen = "scroll";
    S._counters = before;
    render();
    return;
  }
  if (act === "update") {
    save();
    if (navigator.serviceWorker && navigator.serviceWorker.getRegistration) {
      navigator.serviceWorker.getRegistration().then(function (reg) {
        if (reg && reg.waiting) reg.waiting.postMessage({ type: "skip" });
        window.location.reload();
      }).catch(function () { window.location.reload(); });
    }
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
      if (S.duel && S.duel.pairs) {
        S.screen = "duel";
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
      var grace = D.encouragement[encI % D.encouragement.length];
      encI += 1;
      S.wiggleId = arg;
      S.moonChoice = arg;
      S.glowId = step.id;
      S.nodUntil = Date.now() + 600;
      S.run.rightRow = 0;
      S.bubble = { en: D.wrongText.en + " " + grace.en, th: D.wrongText.th + " " + grace.th };
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
    if (!S.run.spell || S.run.spell.id !== lcard.id) S.run.spell = { id: lcard.id, got: "", bank: E.letterBank(word) };
    var stepped = E.spellStep(word, S.run.spell.got, arg);
    if (!stepped.correct) {
      S.wiggleId = lcard.id;
      S.bubble = { en: D.wrongText.en, th: D.wrongText.th };
      render();
      return;
    }
    S.run.spell.got = stepped.got;
    if (stepped.done) {
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
    S.revealOverride = bid;
    S.screen = "reveal";
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
    if (S.revealOverride && S.run && S.run.bossIds) {
      var finishedId = S.revealOverride;
      S.revealOverride = "";
      var allBoss = S.run.bossIds.every(function (cid) { return S.run.bossCleared[cid]; });
      if (!allBoss) {
        S.run.bossIndex += 1;
        S.screen = "boss";
        save();
        render();
        return;
      }
      var zoneKey = S.run.zone;
      var snap = S.run;
      var committed = E.beginKneel(S, D, zoneKey);
      S = committed.state;
      S.run = snap;
      var finBoss = E.finishZoneRun(S, D, snap, today);
      S = finBoss.state;
      sessionRuns += 1;
      S._rest = E.shouldRest(sessionRuns);
      S.screen = "kneel";
      S.kneelZone = zoneKey;
      playFile("audio/maxwell-boss-" + zoneKey + ".m4a");
      save();
      render();
      return;
    }
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
  if (act === "tab") { S.charTab = arg; render(); return; }
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
      var cmp = ui("backupCompare");
      var nowLevel = S.level;
      var nowDays = S.streak && S.streak.n || 0;
      var bakLevel = check.ok ? check.state.level : "";
      var bakDays = check.ok && check.state.streak ? check.state.streak.n : "";
      var filled = check.ok ? E.fillBackupCompare(cmp.en, bakLevel, bakDays, nowLevel, nowDays) + " / " + E.fillBackupCompare(cmp.th, bakLevel, bakDays, nowLevel, nowDays) : check.reason;
      S.backupReason = String(filled).indexOf("{") >= 0 ? "" : filled;
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
  if (act === "showword") {
    if (S.run) S.run.listenFallback = true;
    render();
    return;
  }
  if (act === "hear") {
    if (S.duel && S.duel.heard) speak(S.duel.heard, true);
    return;
  }
  if (act === "duelnext" || act === "duelmap") {
    if (!advanceGate()) return;
    var roundId = "round:" + today + ":" + (S.duelRounds || 0);
    if (!S.ledger[roundId]) {
      var xp = E.applyXp(S, D, 30, roundId);
      S = xp.state;
    }
    S.duelRounds = (S.duelRounds || 0) + 1;
    S.duel = null;
    S.screen = act === "duelmap" ? "map" : "duel";
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

function pauseRun() {
  paused = true;
  try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) { /* ignore */ }
  try {
    if (window.__ac && window.__ac.suspend) {
      var pending = window.__ac.suspend();
      if (pending && pending.catch) pending.catch(function () {});
    }
  } catch (e2) { /* ignore */ }
  render();
}
document.addEventListener("visibilitychange", function () {
  if (document.visibilityState === "hidden") pauseRun();
});
window.addEventListener("pagehide", pauseRun);

window.__layoutAudit = function () {
  var out = { overlaps: [], small: [], thai: [], floating: [], scroll: [], screen: "" };
  var screen = document.querySelector(".screen");
  out.screen = screen ? screen.getAttribute("data-screen") : "";
  function clipToScroll(el, r) {
    var box = { left: Math.max(0, r.left), top: Math.max(0, r.top), right: Math.min(window.innerWidth, r.right), bottom: Math.min(window.innerHeight, r.bottom) };
    var parent = el.parentNode;
    while (parent && parent !== document.body) {
      var style = window.getComputedStyle(parent);
      if (style.overflowY === "auto" || style.overflowY === "scroll" || style.overflowX === "auto" || style.overflow === "hidden") {
        var p = parent.getBoundingClientRect();
        box.left = Math.max(box.left, p.left);
        box.top = Math.max(box.top, p.top);
        box.right = Math.min(box.right, p.right);
        box.bottom = Math.min(box.bottom, p.bottom);
      }
      parent = parent.parentNode;
    }
    box.width = Math.max(0, box.right - box.left);
    box.height = Math.max(0, box.bottom - box.top);
    return box;
  }
  var taps = Array.prototype.slice.call(document.querySelectorAll("[data-tap]"));
  var rects = taps.map(function (el) {
    var raw = el.getBoundingClientRect();
    var visible = clipToScroll(el, raw);
    return { r: visible, raw: raw, act: el.getAttribute("data-act") || "" };
  }).filter(function (x) { return x.r.width >= 8 && x.r.height >= 8 && x.r.height > x.raw.height * 0.7; });
  for (var i = 0; i < rects.length; i++) {
    if (rects[i].raw.width < 43.5 || rects[i].raw.height < 43.5) out.small.push(rects[i].act);
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
  out.raw = (document.body.innerText.match(/\{[A-Za-z]+\}/g) || []);
  function inkBox(el) {
    if (!el) return null;
    var range = document.createRange();
    range.selectNodeContents(el);
    var rects = range.getClientRects();
    var box = { left: Infinity, top: Infinity, right: -Infinity, bottom: -Infinity };
    var i;
    if (!rects.length) {
      var fallback = el.getBoundingClientRect();
      box = { left: fallback.left, top: fallback.top, right: fallback.right, bottom: fallback.bottom };
    } else {
      for (i = 0; i < rects.length; i++) {
        box.left = Math.min(box.left, rects[i].left);
        box.top = Math.min(box.top, rects[i].top);
        box.right = Math.max(box.right, rects[i].right);
        box.bottom = Math.max(box.bottom, rects[i].bottom);
      }
    }
    var stroke = parseFloat(window.getComputedStyle(el).webkitTextStrokeWidth || "0") || 0;
    box.left -= stroke;
    box.top -= stroke;
    box.right += stroke;
    box.bottom += stroke;
    return box;
  }
  var titleEn = document.querySelector(".banner .banner-en") || document.querySelector(".banner .en");
  var titleTh = document.querySelector(".banner .banner-th") || document.querySelector(".banner .th");
  out.titleOverlap = false;
  out.titleGap = null;
  if (titleEn && titleTh) {
    var inkEn = inkBox(titleEn);
    var inkTh = inkBox(titleTh);
    out.titleGap = Math.round(inkTh.top - inkEn.bottom);
    var sharesX = inkEn.left < inkTh.right - 1 && inkEn.right > inkTh.left + 1;
    out.titleOverlap = sharesX && inkEn.bottom + 4 > inkTh.top;
  }
  out.shopClip = [];
  var pane = document.querySelector(".pane");
  if (pane) {
    var paneBox = pane.getBoundingClientRect();
    Array.prototype.slice.call(document.querySelectorAll(".weapon-row .trophy")).forEach(function (el) {
      var box = el.getBoundingClientRect();
      if (box.width < 8) return;
      if (box.right > paneBox.right + 1 || box.left < paneBox.left - 1) out.shopClip.push("edge:" + (el.getAttribute("data-arg") || ""));
      var range = document.createRange();
      range.selectNodeContents(el);
      var rects = range.getClientRects();
      var r;
      for (r = 0; r < rects.length; r++) {
        if (rects[r].width < 1 || rects[r].height < 1) continue;
        if (rects[r].right > box.right + 1 || rects[r].left < box.left - 1 || rects[r].bottom > box.bottom + 1 || rects[r].top < box.top - 1) {
          out.shopClip.push("text:" + (el.getAttribute("data-arg") || ""));
          break;
        }
      }
    });
  }
  var starCount = document.querySelector("[data-star-count]");
  out.starGlyph = !!(starCount && /[★☆]/.test(starCount.textContent || ""));
  var level = document.querySelector(".level-label");
  out.levelText = level ? level.textContent : "";
  out.levelClipped = false;
  if (level) {
    var box = level.getBoundingClientRect();
    out.levelClipped = level.scrollWidth > level.clientWidth + 2 || box.height > 28 || String(level.textContent || "").indexOf("Level") < 0;
  }
  out.ok = !out.overlaps.length && !out.small.length && !out.thai.length && !out.floating.length && !out.scroll.length && !out.errors.length && !out.raw.length && !out.titleOverlap && !out.levelClipped && !out.shopClip.length && !out.starGlyph;
  return out;
};

window.__homeLake = function () {
  var run = E.buildRun(D, E.freshState(D), "maxwell-says", { rng: function () { return 0.2; } });
  return run.steps.slice(0, 3).map(function (step) { return step.id; });
};
window.__listenOff = function () {
  window.__forceSilent = true;
  var run = E.buildRun(D, E.freshState(D), "phonics", { rng: E.mulberry32(4) });
  var i;
  var found = false;
  for (i = 0; i < run.steps.length; i++) if (run.steps[i].listen) { run.index = i; found = true; break; }
  S.run = run;
  S.screen = "play";
  render();
  var word = D.byId[run.steps[run.index].id].en;
  var shown = document.body.innerText.indexOf(word) >= 0;
  window.__forceSilent = false;
  return { shown: shown, found: found };
};
window.__modeFacts = function () {
  var step = S.run && S.run.steps[S.run.index];
  var card = step && D.byId[step.id];
  return {
    kind: step && step.kind,
    n: step && step.countN,
    items: document.querySelectorAll("[data-count-item]").length,
    answer: card ? card.en : "",
    xp: S.xp,
    stars: S.goldStars,
    got: S.run && S.run.spell ? S.run.spell.got : "",
    bank: S.run && S.run.spell ? S.run.spell.bank.slice() : [],
    screen: document.querySelector(".screen") ? document.querySelector(".screen").getAttribute("data-screen") : "",
    targets: document.querySelectorAll("[data-act='" + (step && step.kind || "") + "']").length,
    braced: (document.body.innerText.match(/\{[A-Za-z]+\}/g) || []).length
  };
};
window.__openCharacter = function () {
  try {
    paused = false;
    S.screen = "gear";
    S.charTab = "gems";
    render();
    return {
      screen: document.querySelector(".screen") ? document.querySelector(".screen").getAttribute("data-screen") : "",
      tabs: document.querySelectorAll("[data-act=tab]").length
    };
  } catch (e) {
    return { error: String(e && e.message || e) };
  }
};
window.__startBoss = function () {
  var run = E.buildRun(D, S, "phonics", { rng: E.mulberry32(4) });
  run.phase = "boss";
  run.bossIndex = 0;
  run.regionId = "r1";
  S.run = run;
  S.screen = "boss";
  render();
  return run.bossIds.length;
};
window.__bossFacts = function () {
  var run = S.run;
  var id = run && run.bossIds ? run.bossIds[run.bossIndex] : "";
  var card = id ? D.byId[id] : null;
  var screen = document.querySelector(".screen");
  return {
    screen: screen ? screen.getAttribute("data-screen") : "",
    answer: card ? card.answer : "",
    xp: S.xp,
    bosses: (S.bossesWon || []).slice(),
    title: document.querySelector(".banner .en") ? document.querySelector(".banner .en").textContent : ""
  };
};
window.__openForest = function () {
  if ((S.bossesWon || []).indexOf("baby-hospital") < 0) S.bossesWon.push("baby-hospital");
  S.screen = "map";
  render();
};
window.__xp = function () { return S ? S.xp : ""; };
window.__reflow = function () { render(); return window.__layoutAudit(); };
window.__nextAct = function () {
  var screen = document.querySelector(".screen");
  var name = screen ? screen.getAttribute("data-screen") : "";
  if (document.querySelector("[data-act=versegot]")) return "[data-act=versegot]";
  if (document.querySelector("[data-act=welcome]")) return "[data-act=welcome]";
  if (name === "title") return "[data-act=letsgo]";
  if (name === "menu") return "[data-act=map]";
  if (name === "continue") return "[data-act=resume]";
  if (name === "rest") return "";
  if (name === "map") return "[data-act=region][data-arg=\"r3\"]";
  if (name === "reveal" || name === "reward") return "[data-act=got]";
  if (name === "kneel") return "[data-act=kneelgot]";
  if (document.querySelector("[data-act=twodone]")) return "[data-act=twodone]";
  if (document.querySelector("[data-act=sayit]")) return "[data-act=sayit]";
  if (document.querySelector("[data-act=two]") && S.run && S.run.two) {
    return "[data-act=two][data-arg=" + JSON.stringify(S.run.two.answer || "") + "]";
  }
  if (document.querySelector("[data-correct='1']")) return "[data-correct='1']";
  var step = S.run && S.run.steps && S.run.steps[S.run.index];
  var card = step && D.byId[step.id];
  if (step && step.kind === "letter" && card) {
    var got = S.run.spell && S.run.spell.id === card.id ? S.run.spell.got : "";
    return "[data-act=letter][data-arg=" + JSON.stringify(String(card.en || "").charAt(got.length)) + "]";
  }
  if (step && (step.kind === "count" || step.kind === "size") && card) {
    return "[data-act=" + step.kind + "][data-arg=" + JSON.stringify(card.en) + "]";
  }
  if (name === "boss" && card) return "[data-act=boss][data-arg=" + JSON.stringify(card.answer || "") + "]";
  if (card && card.answer && document.querySelector("[data-act=choice]")) {
    return "[data-act=choice][data-arg=" + JSON.stringify(card.answer) + "]";
  }
  return "";
};
window.__duelFacts = function () {
  var screen = document.querySelector(".screen");
  return {
    screen: screen ? screen.getAttribute("data-screen") : "",
    heard: S.duel && S.duel.heard || "",
    index: S.duel ? S.duel.index : -1,
    left: S.duel && S.duel.pairs ? S.duel.pairs.length - S.duel.index : 0,
    xp: S.xp,
    rounds: S.duelRounds || 0
  };
};
window.__bhReply = function () {
  var card = D.byId["bh-11"];
  S.run = { id: "reply-check", zone: "baby-hospital", index: 0, steps: [{ id: "bh-11", kind: "ask" }], phase: "play", retriesLeft: 0 };
  S.screen = "play";
  render();
  var text = document.body.innerText;
  return { shown: !!(card && card.reply && text.indexOf(card.reply.en) >= 0 && text.indexOf(card.reply.th) >= 0) };
};
window.__trophyIds = function () {
  return Array.prototype.map.call(document.querySelectorAll("[data-trophy]"), function (el) { return el.getAttribute("data-trophy"); });
};
window.__listenProbe = function () {
  var run = E.buildRun(D, E.freshState(D), "phonics", { rng: E.mulberry32(4) });
  var i;
  for (i = 0; i < run.steps.length; i++) if (run.steps[i].listen) { run.index = i; break; }
  window.__spoken = [];
  S.run = run;
  S.screen = "play";
  render();
  var word = D.byId[run.steps[run.index].id].en;
  return {
    replay: !!document.querySelector("[data-act=replay]"),
    spoken: (window.__spoken || []).indexOf(word) >= 0,
    hidden: document.body.innerText.indexOf(word) < 0
  };
};
window.__pauseProbe = function () {
  var xp = document.querySelector("[data-xp]") ? document.querySelector("[data-xp]").getAttribute("data-xp") : "";
  window.dispatchEvent(new Event("pagehide"));
  var prop = document.querySelector("[data-act=prop]");
  if (prop) prop.click();
  return { screen: document.querySelector(".screen").getAttribute("data-screen"), xp: xp };
};
window.__previewMode = function (kind) {
  var zone = kind === "count" ? "numbers" : kind === "size" ? "colors-shapes" : "phonics";
  var run = E.buildRun(D, S, zone, { rng: E.mulberry32(4) });
  var i;
  for (i = 0; i < run.steps.length; i++) {
    if (run.steps[i].kind === kind && (kind !== "count" || run.steps[i].countN >= 3)) { run.index = i; break; }
  }
  if (kind === "count" && run.steps[run.index] && run.steps[run.index].kind !== "count") {
    for (i = 0; i < run.steps.length; i++) {
      if (run.steps[i].kind === "count") { run.index = i; break; }
    }
  }
  S.run = run;
  S.screen = "play";
  S.ledger.started = 1;
  render();
  return run.steps[run.index] && run.steps[run.index].kind;
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
      navigator.serviceWorker.addEventListener("message", function (event) {
        if (!event.data || event.data.type !== "update") return;
        S.updateReady = true;
        if (S.screen === "map") render();
      });
    }
  }).catch(function (err) {
    window.__errors.push(String(err && err.message || err));
    document.getElementById("app").innerHTML = "<div class='screen' data-screen='error'><p class='th' lang='th'>The game files did not load.</p></div>";
  });
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
