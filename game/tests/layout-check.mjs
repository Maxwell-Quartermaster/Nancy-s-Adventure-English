import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { setTimeout as delay } from "node:timers/promises";

var port = 8765;
var outDir = "/opt/cursor/artifacts";
mkdirSync(outDir, { recursive: true });
mkdirSync("/tmp/nae-chrome", { recursive: true });

var server = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"], {
  cwd: new URL("..", import.meta.url).pathname,
  stdio: "ignore"
});
var chrome = spawn("google-chrome", [
  "--headless=new",
  "--disable-gpu",
  "--no-sandbox",
  "--disable-dev-shm-usage",
  "--remote-debugging-port=9222",
  "--user-data-dir=/tmp/nae-chrome",
  "--window-size=390,844",
  "about:blank"
], { stdio: "ignore" });

function die(message) {
  console.error(message);
  server.kill();
  chrome.kill();
  process.exit(1);
}

async function waitPort() {
  for (var i = 0; i < 50; i++) {
    try {
      var res = await fetch("http://127.0.0.1:9222/json/version");
      if (res.ok) return;
    } catch (e) { /* retry */ }
    await delay(200);
  }
  die("chrome debug port did not open");
}

function connect(url) {
  var ws = new WebSocket(url);
  var next = 1;
  var pending = {};
  var consoleNotes = [];
  ws.addEventListener("message", function (event) {
    var msg = JSON.parse(event.data);
    if (msg.id && pending[msg.id]) {
      pending[msg.id](msg);
      delete pending[msg.id];
    }
    if (msg.method === "Runtime.exceptionThrown") {
      consoleNotes.push("exception " + (msg.params.exceptionDetails && msg.params.exceptionDetails.text));
    }
    if (msg.method === "Runtime.consoleAPICalled" && msg.params.type === "error") {
      consoleNotes.push("console " + msg.params.args.map(function (a) { return a.value || a.description || ""; }).join(" "));
    }
  });
  return new Promise(function (resolve, reject) {
    ws.addEventListener("open", function () {
      resolve({
        notes: consoleNotes,
        send: function (method, params) {
          var id = next++;
          return new Promise(function (res) {
            pending[id] = res;
            ws.send(JSON.stringify({ id: id, method: method, params: params || {} }));
          });
        },
        close: function () { ws.close(); }
      });
    });
    ws.addEventListener("error", function () { reject(new Error("websocket failed")); });
  });
}

async function evaluate(cdp, expression) {
  var msg = await cdp.send("Runtime.evaluate", { expression: expression, returnByValue: true, awaitPromise: true });
  if (msg.result && msg.result.exceptionDetails) {
    throw new Error(JSON.stringify(msg.result.exceptionDetails));
  }
  return msg.result && msg.result.result ? msg.result.result.value : undefined;
}

async function settle(cdp) {
  await evaluate(cdp, "Promise.race([Promise.all((document.getAnimations ? document.getAnimations() : []).map(function (a) { return a.finished.catch(function () {}); })), new Promise(function (resolve) { setTimeout(resolve, 500); })]).then(function () { return 1; })");
  await delay(30);
}
async function shot(cdp, name) {
  await settle(cdp);
  var text = await evaluate(cdp, "document.body.innerText");
  var banned = ["kicking", "husband", "Check-out", "one hundred twenty", "Your room is ready"];
  banned.forEach(function (word) {
    if (String(text).indexOf(word) >= 0) throw new Error("screenshot blocked, sensitive text: " + word);
  });
  var msg = await cdp.send("Page.captureScreenshot", { format: "png" });
  writeFileSync(outDir + "/" + name + ".png", Buffer.from(msg.result.data, "base64"));
}

async function waitScreen(cdp) {
  for (var i = 0; i < 40; i++) {
    var screen = await evaluate(cdp, "var s=document.querySelector('.screen'); s?s.getAttribute('data-screen'):''");
    if (screen) return screen;
    await delay(150);
  }
  return "";
}

async function click(cdp, selector) {
  var ok = await evaluate(cdp, "(function(){var el=document.querySelector(" + JSON.stringify(selector) + "); if(!el) return false; el.click(); return true;})()");
  if (!ok) throw new Error("missing " + selector);
  await delay(200);
}

async function pass(cdp, label, reduce) {
  await cdp.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: reduce ? "reduce" : "" }]
  });
  var suffix = reduce ? "-reduced" : "";
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: label === "320x568" ? 320 : label === "393x852" ? 393 : 390,
    height: label === "320x568" ? 568 : label === "393x852" ? 852 : 844,
    deviceScaleFactor: 1,
    mobile: true
  });
  await cdp.send("Page.navigate", { url: "http://127.0.0.1:" + port + "/index.html" });
  await delay(500);
  await waitScreen(cdp);
  await evaluate(cdp, "(function(){try{localStorage.clear();indexedDB.deleteDatabase('nae');}catch(e){}})()");
  await cdp.send("Page.reload", { ignoreCache: true });
  await delay(500);
  var screen = await waitScreen(cdp);
  if (screen !== "title") throw new Error(label + " boot screen " + screen);
  if (await evaluate(cdp, "!!document.querySelector('[data-act=welcome]')")) await click(cdp, "[data-act=welcome]");
  if (await evaluate(cdp, "!!document.querySelector('[data-act=versegot]')")) await click(cdp, "[data-act=versegot]");
  await shot(cdp, "title-" + label + suffix);
  var titleAudit = await evaluate(cdp, "window.__layoutAudit()");
  await click(cdp, "[data-act=letsgo]");
  screen = await waitScreen(cdp);
  if (screen !== "play") throw new Error(label + " expected play, got " + screen);
  await shot(cdp, "question-" + label + suffix);
  var playAudit = await evaluate(cdp, "window.__layoutAudit()");
  var hit = await evaluate(cdp, "(function(){var correct=document.querySelector('[data-correct=\"1\"]'); if(!correct) return {missing:true}; var r=correct.getBoundingClientRect(); var top=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); var owner=top&&top.closest?top.closest('[data-prop]'):null; return {want:correct.getAttribute('data-arg'), hit:owner&&owner.getAttribute('data-arg')};})()");
  await click(cdp, "[data-correct='1']");
  screen = await waitScreen(cdp);
  if (screen !== "reveal") throw new Error(label + " expected reveal, got " + screen);
  var xp = await evaluate(cdp, "document.querySelector('[data-xp]') && document.querySelector('[data-xp]').getAttribute('data-xp')");
  await click(cdp, "[data-act=got]");
  await click(cdp, "[data-act=tomap]");
  screen = await waitScreen(cdp);
  if (screen !== "map") throw new Error(label + " expected map, got " + screen);
  await shot(cdp, "map-" + label + suffix);
  var mapAudit = await evaluate(cdp, "window.__layoutAudit()");
  await click(cdp, "[data-act=back]");
  screen = await waitScreen(cdp);
  if (screen !== "menu") throw new Error(label + " expected menu, got " + screen);
  await shot(cdp, "menu-" + label + suffix);
  var menuAudit = await evaluate(cdp, "window.__layoutAudit()");
  await click(cdp, "[data-act=gear]");
  await shot(cdp, "character-" + label + suffix);
  var characterAudit = await evaluate(cdp, "window.__layoutAudit()");
  await click(cdp, "[data-act=back]");
  await click(cdp, "[data-act=shop]");
  await shot(cdp, "shop-" + label + suffix);
  var shopAudit = await evaluate(cdp, "window.__layoutAudit()");
  var shopText = await evaluate(cdp, "document.body.innerText");
  var shopLiteral = String(shopText).indexOf("{n}") >= 0;
  await evaluate(cdp, "window.__previewMode('letter')");
  await delay(200);
  await shot(cdp, "letter-" + label + suffix);
  var letterAudit = await evaluate(cdp, "window.__layoutAudit()");
  await evaluate(cdp, "window.__previewMode('count')");
  await delay(200);
  await shot(cdp, "count-" + label + suffix);
  var countAudit = await evaluate(cdp, "window.__layoutAudit()");
  await evaluate(cdp, "window.__previewMode('size')");
  await delay(200);
  await shot(cdp, "size-" + label + suffix);
  var sizeAudit = await evaluate(cdp, "window.__layoutAudit()");
  await cdp.send("Page.reload", { ignoreCache: false });
  await delay(500);
  await waitScreen(cdp);
  if (await evaluate(cdp, "!!document.querySelector('[data-act=versegot]')")) await click(cdp, "[data-act=versegot]");
  await click(cdp, "[data-act=letsgo]");
  var xp2 = await evaluate(cdp, "document.querySelector('[data-xp]') && document.querySelector('[data-xp]').getAttribute('data-xp')");
  var errors = await evaluate(cdp, "window.__errors");
  var listen = null;
  var pausedProbe = null;
  var home = null;
  if (!reduce) {
    home = await evaluate(cdp, "window.__homeLake()");
    listen = await evaluate(cdp, "window.__listenProbe()");
    pausedProbe = await evaluate(cdp, "window.__pauseProbe()");
  }
  var motion = await evaluate(cdp, "getComputedStyle(document.querySelector('.screen')).animationName");
  var net = await evaluate(cdp, "window.__net");
  return { label: label, reduced: !!reduce, motion: motion, xp: xp, xpAfterReload: xp2, errors: errors, net: net, hit: hit, shopLiteral: shopLiteral, home: home, listen: listen, pausedProbe: pausedProbe, titleAudit: titleAudit, playAudit: playAudit, mapAudit: mapAudit, menuAudit: menuAudit, characterAudit: characterAudit, shopAudit: shopAudit, letterAudit: letterAudit, countAudit: countAudit, sizeAudit: sizeAudit, console: cdp.notes.slice() };
}

await waitPort();
var list = await (await fetch("http://127.0.0.1:9222/json/list")).json();
var page = list.filter(function (t) { return t.type === "page"; })[0];
if (!page) die("no chrome page");
var cdp = await connect(page.webSocketDebuggerUrl);
await cdp.send("Runtime.enable");
await cdp.send("Page.enable");
var reports = [];
try {
  reports.push(await pass(cdp, "390x844", false));
  reports.push(await pass(cdp, "320x568", false));
  reports.push(await pass(cdp, "393x852", false));
  reports.push(await pass(cdp, "390x844", true));
  reports.push(await pass(cdp, "320x568", true));
} catch (err) {
  console.error(String(err && err.stack || err));
  try { reports.push({ fatal: String(err.message || err), notes: cdp.notes }); } catch (e) { /* ignore */ }
  writeFileSync(outDir + "/layout-report.json", JSON.stringify(reports, null, 2));
  cdp.close();
  server.kill();
  chrome.kill();
  process.exit(1);
}
var modeReport = [];
for (var mi = 0; mi < 2; mi++) {
  var mlabel = mi === 0 ? "390x844" : "320x568";
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: mi === 0 ? 390 : 320,
    height: mi === 0 ? 844 : 568,
    deviceScaleFactor: 1,
    mobile: true
  });
  var modes = ["count", "letter", "size"];
  var played = [];
  var lastXp = "";
  for (var mk = 0; mk < modes.length; mk++) {
    var kind = modes[mk];
    await evaluate(cdp, "window.__previewMode(" + JSON.stringify(kind) + ")");
    await delay(250);
    var before = await evaluate(cdp, "window.__modeFacts()");
    var xp0 = before.xp;
    if (kind === "count") {
      var wrong = before.answer === "two" ? "three" : "two";
      await click(cdp, "[data-act=count][data-arg=" + JSON.stringify(wrong) + "]");
      var mid = await evaluate(cdp, "window.__modeFacts()");
      await click(cdp, "[data-act=count][data-arg=" + JSON.stringify(before.answer) + "]");
      var after = await evaluate(cdp, "window.__modeFacts()");
      lastXp = String(after.xp);
      await delay(450);
      await click(cdp, "[data-act=got]");
      var afterGot = await evaluate(cdp, "window.__modeFacts()");
      played.push({ kind: kind, items: before.items, n: before.n, braced: before.braced, xp0: xp0, xpMiss: mid.xp, xpHit: after.xp, xpAfterGot: afterGot.xp, screen: after.screen, screenAfter: afterGot.screen });
    } else if (kind === "letter") {
      var word = before.answer;
      var wrongLetter = "a";
      var bi;
      for (bi = 0; bi < (before.bank || []).length; bi++) {
        if (before.bank[bi] !== word.charAt(0)) wrongLetter = before.bank[bi];
      }
      await click(cdp, "[data-act=letter][data-arg=" + JSON.stringify(wrongLetter) + "]");
      var missed = await evaluate(cdp, "window.__modeFacts()");
      var li;
      for (li = 0; li < word.length; li++) {
        await click(cdp, "[data-act=letter][data-arg=" + JSON.stringify(word.charAt(li)) + "]");
      }
      var done = await evaluate(cdp, "window.__modeFacts()");
      await delay(450);
      await click(cdp, "[data-act=got]");
      var afterLetter = await evaluate(cdp, "window.__modeFacts()");
      lastXp = String(done.xp);
      played.push({ kind: kind, word: word, gotMiss: missed.got, xp0: xp0, xpMiss: missed.xp, xpHit: done.xp, xpAfterGot: afterLetter.xp, screen: done.screen, screenAfter: afterLetter.screen });
    } else {
      var other = before.answer === "big" ? "small" : "big";
      await click(cdp, "[data-act=size][data-arg=" + JSON.stringify(other) + "]");
      var missSize = await evaluate(cdp, "window.__modeFacts()");
      await click(cdp, "[data-act=size][data-arg=" + JSON.stringify(before.answer) + "]");
      var hitSize = await evaluate(cdp, "window.__modeFacts()");
      await delay(450);
      await click(cdp, "[data-act=got]");
      var afterSize = await evaluate(cdp, "window.__modeFacts()");
      lastXp = String(hitSize.xp);
      played.push({ kind: kind, answer: before.answer, targets: before.targets, braced: before.braced, xp0: xp0, xpMiss: missSize.xp, xpHit: hitSize.xp, xpAfterGot: afterSize.xp, screen: hitSize.screen, screenAfter: afterSize.screen });
    }
  }
  await cdp.send("Page.reload", { ignoreCache: true });
  await waitScreen(cdp);
  if (await evaluate(cdp, "document.querySelector('.screen') && document.querySelector('.screen').getAttribute('data-screen')==='continue'")) {
    await click(cdp, "[data-act=resume]");
  }
  if (await evaluate(cdp, "!!document.querySelector('[data-act=versegot]')")) await click(cdp, "[data-act=versegot]");
  var xpKeep = await evaluate(cdp, "window.__xp ? window.__xp() : ''");
  var opened = await evaluate(cdp, "window.__openCharacter()");
  console.log("opened", JSON.stringify(opened));
  var trophies = [];
  var tabs = ["gems", "themes", "titles", "gear"];
  var ti;
  for (ti = 0; ti < tabs.length; ti++) {
    await click(cdp, "[data-act=tab][data-arg=" + JSON.stringify(tabs[ti]) + "]");
    var ids = await evaluate(cdp, "window.__trophyIds()");
    trophies = trophies.concat(ids || []);
  }
  var seenTrophy = {};
  trophies.forEach(function (id) { if (id) seenTrophy[id] = 1; });
  var listenOff = await evaluate(cdp, "window.__listenOff()");
  var gearIds = ["cape-green", "cape-purple", "sparkle", "tunic-rose", "cape-sky", "splash-golden-sword"];
  var gearSeen = gearIds.filter(function (id) { return seenTrophy[id]; }).length;
  modeReport.push({ label: mlabel, played: played, xpBeforeReload: lastXp, xpAfterReload: xpKeep, trophies: Object.keys(seenTrophy).length, gear: gearSeen, listenOff: listenOff, opened: opened });
}
var story = { boss: [], duel: null, reply: null };
await cdp.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
var bossCount = await evaluate(cdp, "window.__startBoss()");
var bossXp = await evaluate(cdp, "window.__bossFacts()");
var bossStart = bossXp.xp;
for (var bi2 = 0; bi2 < bossCount; bi2++) {
  var fact = await evaluate(cdp, "window.__bossFacts()");
  if (bi2 === 0) {
    var wrongBoss = await evaluate(cdp, "(function(){var nodes=document.querySelectorAll('[data-act=boss]'); var i; for(i=0;i<nodes.length;i++){ if(nodes[i].getAttribute('data-arg')!==" + JSON.stringify(bossXp.answer) + ") return nodes[i].getAttribute('data-arg'); } return '';})()");
    if (wrongBoss) await click(cdp, "[data-act=boss][data-arg=" + JSON.stringify(wrongBoss) + "]");
    var missedBoss = await evaluate(cdp, "window.__bossFacts()");
    story.boss.push({ miss: missedBoss.xp === bossStart, screen: missedBoss.screen });
  }
  await click(cdp, "[data-act=boss][data-arg=" + JSON.stringify(fact.answer) + "]");
  var revealed = await evaluate(cdp, "window.__bossFacts()");
  await delay(450);
  await click(cdp, "[data-act=got]");
  story.boss.push({ reveal: revealed.screen, answer: fact.answer });
}
var knelt = await evaluate(cdp, "window.__bossFacts()");
story.kneel = knelt.screen;
if (knelt.screen === "kneel") {
  await delay(450);
  await click(cdp, "[data-act=kneelgot]");
}
var rewards = [];
var guard = 0;
while (guard < 8) {
  var now = await evaluate(cdp, "window.__bossFacts()");
  rewards.push(now.screen);
  if (now.screen !== "reward" && now.screen !== "rest") break;
  await delay(450);
  var nextAct = now.screen === "rest" ? "keep" : "got";
  await click(cdp, "[data-act=" + nextAct + "]");
  guard += 1;
}
var bossEnd = await evaluate(cdp, "window.__bossFacts()");
story.rewards = rewards;
story.bosses = bossEnd.bosses;
story.bossXp = { start: bossStart, end: bossEnd.xp };
await evaluate(cdp, "window.__openForest()");
await click(cdp, "[data-act=region][data-arg=\"r4\"]");
var duel0 = await evaluate(cdp, "window.__duelFacts()");
var otherWord = await evaluate(cdp, "(function(){var nodes=document.querySelectorAll('[data-act=duel]'); var i; for(i=0;i<nodes.length;i++){ if(nodes[i].getAttribute('data-arg')!==" + JSON.stringify(duel0.heard) + ") return nodes[i].getAttribute('data-arg'); } return '';})()");
if (otherWord) await click(cdp, "[data-act=duel][data-arg=" + JSON.stringify(otherWord) + "]");
var duelMiss = await evaluate(cdp, "window.__duelFacts()");
await click(cdp, "[data-act=duel][data-arg=" + JSON.stringify(duel0.heard) + "]");
var duelHit = await evaluate(cdp, "window.__duelFacts()");
await click(cdp, "[data-act=tomap]");
var left = await evaluate(cdp, "window.__duelFacts()");
await click(cdp, "[data-act=region][data-arg=\"r4\"]");
var back = await evaluate(cdp, "window.__duelFacts()");
await evaluate(cdp, "window.dispatchEvent(new Event('pagehide'))");
var pausedDuel = await evaluate(cdp, "document.querySelector('.screen').getAttribute('data-screen')");
await click(cdp, "[data-act=resume]");
var resumed = await evaluate(cdp, "window.__duelFacts()");
var safety = 0;
while (safety < 12) {
  var cur = await evaluate(cdp, "window.__duelFacts()");
  if (!cur.heard) break;
  await click(cdp, "[data-act=duel][data-arg=" + JSON.stringify(cur.heard) + "]");
  safety += 1;
}
var beforeMap = await evaluate(cdp, "window.__duelFacts()");
await delay(450);
await click(cdp, "[data-act=duelmap]");
var afterMap = await evaluate(cdp, "window.__duelFacts()");
await cdp.send("Page.reload", { ignoreCache: true });
await waitScreen(cdp);
if (await evaluate(cdp, "document.querySelector('.screen') && document.querySelector('.screen').getAttribute('data-screen')==='continue'")) await click(cdp, "[data-act=resume]");
if (await evaluate(cdp, "!!document.querySelector('[data-act=versegot]')")) await click(cdp, "[data-act=versegot]");
var duelKept = await evaluate(cdp, "window.__xp ? window.__xp() : ''");
var reply = await evaluate(cdp, "window.__bhReply()");
story.duel = {
  startXp: duel0.xp, missXp: duelMiss.xp, hitIndex: duelHit.index, left: left.screen, backIndex: back.index,
  paused: pausedDuel, resumed: resumed.screen, before: beforeMap.xp, after: afterMap.xp, afterScreen: afterMap.screen, kept: duelKept
};
story.reply = reply;
await cdp.send("Emulation.setDeviceMetricsOverride", { width: 320, height: 568, deviceScaleFactor: 1, mobile: true });
await click(cdp, "[data-act=tomap]");
await click(cdp, "[data-act=back]");
await click(cdp, "[data-act=gear]");
await click(cdp, "[data-act=backup]");
var backupAudit = await evaluate(cdp, "window.__layoutAudit()");
await shot(cdp, "backup-320x568");
await cdp.send("Emulation.setDeviceMetricsOverride", { width: 844, height: 390, deviceScaleFactor: 1, mobile: true });
await click(cdp, "[data-act=back]");
await click(cdp, "[data-act=shop]");
var shopLand = await evaluate(cdp, "window.__reflow()");
await shot(cdp, "shop-844x390");
await cdp.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
await click(cdp, "[data-act=back]");
await click(cdp, "[data-act=map]");
var chipBefore = await evaluate(cdp, "!!document.querySelector('[data-act=update]')");
await evaluate(cdp, "navigator.serviceWorker && navigator.serviceWorker.dispatchEvent(new MessageEvent('message', { data: { type: 'update' } }))");
await delay(100);
var chipAfter = await evaluate(cdp, "!!document.querySelector('[data-act=update]')");
await shot(cdp, "map-update-390x844");
await evaluate(cdp, "window.__previewMode('count')");
var lockProbe = await evaluate(cdp, "(function(){var facts=window.__modeFacts(); var before=window.__xp(); var btn=document.querySelector('[data-act=count][data-arg='+JSON.stringify(facts.answer)+']'); if(!btn) return {missing:true, answer:facts.answer}; btn.click(); btn.click(); return {before:before, after:window.__xp(), locked:!!(window.__lockDuring), screen:document.querySelector('.screen').getAttribute('data-screen')};})()");
var storedXp = await evaluate(cdp, "window.__xp()");
var mirrorXp = await evaluate(cdp, "(function(){var mirror=JSON.parse(localStorage.getItem('naeState')); var next=storedXp+30; mirror.xp=next; mirror.rev=(Number(mirror.rev)||0)+4; mirror.savedAt=Date.now(); mirror.ledger['round:race:1']=1; localStorage.setItem('naeState', JSON.stringify(mirror)); return next;})()".replace("storedXp", String(storedXp)));
await cdp.send("Page.reload", { ignoreCache: true });
await waitScreen(cdp);
var raced = await evaluate(cdp, "window.__xp()");
var indexedNewer = await evaluate(cdp, "(function(){return new Promise(function(resolve){var done=false; function finish(v){ if(done) return; done=true; resolve(v); } setTimeout(function(){finish(0);}, 2000); var mirror=JSON.parse(localStorage.getItem('naeState')); mirror.rev=40; mirror.xp=111; localStorage.setItem('naeState', JSON.stringify(mirror)); var req=indexedDB.open('nae',1); req.onerror=function(){finish(0);}; req.onsuccess=function(){try{var tx=req.result.transaction('kv','readwrite'); var copy=JSON.parse(JSON.stringify(mirror)); copy.rev=50; copy.xp=999; copy.ledger['round:race:1']=1; tx.objectStore('kv').put(copy,'state'); tx.oncomplete=function(){finish(999);}; tx.onerror=function(){finish(0);};}catch(e){finish(0);}};});})()");
await cdp.send("Page.reload", { ignoreCache: true });
await waitScreen(cdp);
var indexedKept = await evaluate(cdp, "window.__xp()");
var dup = await evaluate(cdp, "(function(){var before=window.__xp(); var state=JSON.parse(localStorage.getItem('naeState')); var again=state.ledger && state.ledger['round:race:1'] ? before : before+30; return {before:before, ledger:!!(state.ledger&&state.ledger['round:race:1']), again:again};})()");
var restSteps = 0;
var restScreen = await evaluate(cdp, "document.querySelector('.screen').getAttribute('data-screen')");
while (restScreen !== "rest" && restSteps < 280) {
  var sel = await evaluate(cdp, "window.__nextAct()");
  if (!sel) break;
  if (sel.indexOf("got") >= 0 || sel.indexOf("sayit") >= 0 || sel.indexOf("twodone") >= 0 || sel.indexOf("kneel") >= 0) await delay(430);
  try { await click(cdp, sel); } catch (err) { story.restError = String(err.message || err) + " " + sel; break; }
  restScreen = await evaluate(cdp, "document.querySelector('.screen') ? document.querySelector('.screen').getAttribute('data-screen') : ''");
  restSteps += 1;
}
if (restScreen === "rest") {
  var restText = await evaluate(cdp, "document.body.innerText");
  var restAudit = await evaluate(cdp, "window.__layoutAudit()");
  story.rest = { steps: restSteps, repeated: (restText.match(/Great work today/g) || []).length, audit: !!(restAudit && restAudit.ok), gap: restAudit && restAudit.titleGap };
} else story.rest = { steps: restSteps, screen: restScreen };
story.extra = {
  backup: !!(backupAudit && backupAudit.ok && !backupAudit.titleOverlap),
  backupGap: backupAudit && backupAudit.titleGap,
  shopLand: !!(shopLand && shopLand.ok && !shopLand.shopClip.length && !shopLand.titleOverlap),
  shopGap: shopLand && shopLand.titleGap,
  chipBefore: chipBefore,
  chipAfter: chipAfter,
  lock: lockProbe,
  mirrorXp: mirrorXp,
  raced: raced,
  indexedNewer: indexedNewer,
  indexedKept: indexedKept,
  dup: dup
};
reports.push({ modeReport: modeReport, story: story });
writeFileSync(outDir + "/layout-report.json", JSON.stringify(reports, null, 2));
console.log(JSON.stringify(reports, null, 2));
var failed = reports.some(function (r) {
  var audits = ["titleAudit", "playAudit", "mapAudit", "menuAudit", "characterAudit", "shopAudit", "letterAudit", "countAudit", "sizeAudit"];
  var badNet = (r.net || []).some(function (url) { return /^https?:\/\//.test(url) && url.indexOf("127.0.0.1") !== 0 && url.indexOf("localhost") !== 0; });
  var flowBad = r.hit && r.hit.want && r.hit.want !== r.hit.hit;
  flowBad = flowBad || r.shopLiteral;
  flowBad = flowBad || (r.home && r.home.join(",") !== "ms-28,ms-29,ms-30");
  flowBad = flowBad || (r.listen && !r.listen.replay);
  flowBad = flowBad || (r.listen && r.listen.spoken && !r.listen.hidden);
  flowBad = flowBad || (r.listen && !r.listen.spoken && r.listen.hidden);
  flowBad = flowBad || (r.pausedProbe && r.pausedProbe.screen !== "continue");
  var modeBad = false;
  if (r.modeReport) {
    modeBad = r.modeReport.some(function (row) {
      var playBad = (row.played || []).some(function (step) {
        if (step.braced) return true;
        if (step.kind === "count" && step.items !== step.n) return true;
        if (step.kind === "size" && step.targets !== 2) return true;
        if (String(step.xpMiss) !== String(step.xp0)) return true;
        var gained = Number(step.xpHit) - Number(step.xp0);
        if (row.label === "390x844" && gained !== 10) return true;
        if (gained !== 0 && gained !== 10) return true;
        if (step.xpAfterGot != null && String(step.xpAfterGot) !== String(step.xpHit)) return true;
        if (step.screenAfter === "reveal") return true;
        if (step.screen !== "reveal") return true;
        return false;
      });
      return playBad || String(row.xpAfterReload) !== String(row.xpBeforeReload) || row.trophies !== 42 || row.gear !== 6 || !row.listenOff || !row.listenOff.shown;
    });
  }
  var storyBad = false;
  if (r.story) {
    var d = r.story.duel || {};
    storyBad = r.story.kneel !== "kneel" || (r.story.bosses || []).indexOf("phonics") < 0 || !(r.story.rewards || []).some(function (s) { return s === "reward"; });
    storyBad = storyBad || !r.story.reply || !r.story.reply.shown;
    storyBad = storyBad || d.left !== "map" || d.backIndex !== d.hitIndex || d.paused !== "continue" || d.resumed !== "duel";
    storyBad = storyBad || Number(d.missXp) !== Number(d.startXp) || Number(d.after) !== Number(d.before) + 30 || String(d.kept) !== String(d.after);
    var extra = r.story.extra || {};
    storyBad = storyBad || !extra.backup || !extra.shopLand || !extra.chipAfter;
    var lockGain = extra.lock ? Number(extra.lock.after) - Number(extra.lock.before) : 99;
    storyBad = storyBad || !extra.lock || extra.lock.missing || extra.lock.locked !== true || (lockGain !== 0 && lockGain !== 10);
    storyBad = storyBad || Number(extra.raced) !== Number(extra.mirrorXp);
    storyBad = storyBad || Number(extra.indexedKept) !== 999 || !extra.dup || !extra.dup.ledger || Number(extra.dup.again) !== Number(extra.dup.before);
    storyBad = storyBad || !r.story.rest || r.story.rest.repeated !== 1;
  }
  return audits.some(function (k) { return r[k] && r[k].ok === false; }) || (r.errors && r.errors.length) || badNet || flowBad || (r.xp != null && String(r.xpAfterReload) !== String(r.xp)) || (r.reduced && r.motion !== "fade150") || modeBad || storyBad;
});
cdp.close();
server.kill();
chrome.kill();
process.exit(failed ? 1 : 0);
