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

async function shot(cdp, name) {
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
writeFileSync(outDir + "/layout-report.json", JSON.stringify(reports, null, 2));
console.log(JSON.stringify(reports, null, 2));
var failed = reports.some(function (r) {
  var audits = ["titleAudit", "playAudit", "mapAudit", "menuAudit", "characterAudit", "shopAudit", "letterAudit", "countAudit", "sizeAudit"];
  var badNet = (r.net || []).some(function (url) { return /^https?:\/\//.test(url) && url.indexOf("127.0.0.1") !== 0 && url.indexOf("localhost") !== 0; });
  var flowBad = r.hit && r.hit.want && r.hit.want !== r.hit.hit;
  flowBad = flowBad || r.shopLiteral;
  flowBad = flowBad || (r.home && r.home.join(",") !== "ms-28,ms-29,ms-30");
  flowBad = flowBad || (r.listen && (!r.listen.replay || !r.listen.spoken));
  flowBad = flowBad || (r.pausedProbe && r.pausedProbe.screen !== "continue");
  return audits.some(function (k) { return r[k] && r[k].ok === false; }) || (r.errors && r.errors.length) || badNet || flowBad || String(r.xpAfterReload) !== String(r.xp) || (r.reduced && r.motion !== "fade150");
});
cdp.close();
server.kill();
chrome.kill();
process.exit(failed ? 1 : 0);
