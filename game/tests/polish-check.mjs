import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, readFileSync } from "node:fs";
import { setTimeout as delay } from "node:timers/promises";
import { weaponSvg } from "../js/art.mjs";

var port = 8765;
var outDir = "/opt/cursor/artifacts";
mkdirSync(outDir, { recursive: true });
mkdirSync("/tmp/nae-chrome", { recursive: true });

var cards = JSON.parse(readFileSync(new URL("../data/cards.json", import.meta.url), "utf8"));
var tex = cards.picPlan.uiInlineSvg.tex;
var blades = ["#B9C0C4", "#4A90D9", "#F2A23A"];
var shades = ["#8A939C", "#2C5A8A", "#C47A1A"];
function box(title, svg) {
  return "<div class='box'><div class='art'>" + svg + "</div><div class='lab'>" + title + "</div></div>";
}
var raw = function (inner) {
  return "<svg class='drawn' viewBox='-28 -84 56 118'>" + inner + "</svg>";
};
var html = "<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;background:#fff;font:14px sans-serif}.row{display:flex;gap:12px;padding:12px;align-items:flex-end}.box{width:120px;text-align:center}.art{width:72px;height:72px;margin:0 auto;overflow:hidden;border:2px solid #10170F;background:#fff8e7;display:flex;align-items:center;justify-content:center}.art svg{width:72px;height:72px}.lab{margin-top:4px}</style></head><body>" +
  tex +
  "<div class='row'><b>approved parts</b>" +
  box("#wb", raw("<use href='#wb'></use>")) +
  box("#wh+#wx", raw("<use href='#wh'></use><use href='#wx'></use>")) +
  box("#wh+#wm", raw("<use href='#wh'></use><use href='#wm'></use>")) +
  "</div><div class='row'><b>shop framing</b>" +
  box("sword", weaponSvg("wb", blades[0], shades[0])) +
  box("great", weaponSvg("wb x1.4, long grip", blades[1], shades[1])) +
  box("axe", weaponSvg("wh+wx", blades[2], shades[2])) +
  box("mace", weaponSvg("wh+wm", blades[0], shades[0])) +
  "</div></body></html>";
writeFileSync("/tmp/parts.html", html);

var server = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"], {
  cwd: new URL("..", import.meta.url).pathname,
  stdio: "ignore"
});
var chrome = spawn("google-chrome", [
  "--headless=new", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
  "--remote-debugging-port=9222", "--user-data-dir=/tmp/nae-chrome", "--window-size=1280,800", "about:blank"
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
  ws.addEventListener("message", function (event) {
    var msg = JSON.parse(event.data);
    if (msg.id && pending[msg.id]) {
      pending[msg.id](msg);
      delete pending[msg.id];
    }
  });
  return new Promise(function (resolve, reject) {
    ws.addEventListener("open", function () {
      resolve({
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
  if (msg.result && msg.result.exceptionDetails) throw new Error(JSON.stringify(msg.result.exceptionDetails.exception || msg.result.exceptionDetails));
  return msg.result && msg.result.result ? msg.result.result.value : undefined;
}

async function shot(cdp, name) {
  await delay(120);
  var msg = await cdp.send("Page.captureScreenshot", { format: "png" });
  writeFileSync(outDir + "/" + name + ".png", Buffer.from(msg.result.data, "base64"));
}

async function size(cdp, w, h, mobile) {
  await cdp.send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: !!mobile });
}

var overlapProbe = "(function(sel){var root=document.querySelector(sel); if(!root) return {missing:true}; var cards=[].slice.call(root.querySelectorAll('.weapon-card, [data-trophy]')); var bad=[]; cards.forEach(function(card){var art=card.querySelector('.weapon-art'); if(!art) return; var a=art.getBoundingClientRect(); [].slice.call(card.querySelectorAll('.en,.th,.price-line')).forEach(function(el){var r=el.getBoundingClientRect(); if(r.width<2||r.height<2) return; var hit=!(r.right<a.left+1||r.left>a.right-1||r.bottom<a.top+1||r.top>a.bottom-1); var x=Math.min(Math.max(r.left+4,0), window.innerWidth-1); var y=Math.min(Math.max(r.top+4,0), window.innerHeight-1); var top=document.elementFromPoint(x,y); var covered=!!(top&&art.contains(top)); if(hit||covered) bad.push((card.getAttribute('data-trophy')||card.getAttribute('data-arg')||'')+':'+el.textContent.slice(0,24)); }); }); var hrefs=[]; [].slice.call(root.querySelectorAll('.weapon-svg use')).forEach(function(n){hrefs.push(n.getAttribute('href'));}); var drawn=0; [].slice.call(root.querySelectorAll('.weapon-art svg.drawn')).forEach(function(svg){ if(svg.classList.contains('weapon-svg')) return; if(svg.querySelector('path,circle,rect,ellipse,polygon')) drawn+=1; }); var beige=root.querySelectorAll('rect[fill=\"#E9D9AE\"]').length; return {bad:bad, hrefs:hrefs.join(','), beige:beige, drawn:drawn};})";

await waitPort();
var list = await (await fetch("http://127.0.0.1:9222/json/list")).json();
var page = list.filter(function (t) { return t.type === "page"; })[0];
if (!page) die("no chrome page");
var cdp = await connect(page.webSocketDebuggerUrl);
await cdp.send("Runtime.enable");
await cdp.send("Page.enable");
var problems = [];

async function boot() {
  await cdp.send("Page.navigate", { url: "http://127.0.0.1:" + port + "/index.html" });
  for (var i = 0; i < 40; i++) {
    if (await evaluate(cdp, "!!document.querySelector('.screen')")) break;
    await delay(150);
  }
  if (await evaluate(cdp, "!!document.querySelector('[data-act=versegot]')")) {
    await evaluate(cdp, "document.querySelector('[data-act=versegot]').click()");
    await delay(200);
  }
  if (await evaluate(cdp, "!!document.querySelector('[data-act=letsgo]')")) {
    await evaluate(cdp, "document.querySelector('[data-act=letsgo]').click()");
    await delay(200);
  }
}

var CUSTOM_DRAWN = { "hammer-builder": 1, "sling-shepherd": 1, "staff-shepherd": 1, "tunic-rose": 1 };

function isCustomDrawn(label) {
  if (label.indexOf("character-") !== 0 || label.indexOf("row-") >= 0) return false;
  return !!CUSTOM_DRAWN[label.slice("character-".length)];
}

function record(label, facts) {
  if (!facts || facts.missing) problems.push(label + " missing");
  else if ((facts.bad || []).length || facts.beige) problems.push(label + " " + JSON.stringify(facts));
  else if (isCustomDrawn(label)) {
    if (!(facts.drawn > 0)) problems.push(label + " no drawn svg");
  } else if (label.indexOf("character-") === 0 && label.indexOf("row-") < 0 && !(facts.hrefs || "").length) problems.push(label + " no parts");
  else if (label.indexOf("mace") >= 0 && String(facts.hrefs || "").indexOf("#wm") < 0) problems.push(label + " no mace part");
  else if (label.indexOf("axe") >= 0 && String(facts.hrefs || "").indexOf("#wx") < 0) problems.push(label + " no axe part");
  console.log(label, JSON.stringify(facts));
}

try {
  await boot();
  await size(cdp, 428, 926, true);
  await evaluate(cdp, "window.__showShop('locked')");
  for (var locked of ["axe1", "mace1"]) {
    await evaluate(cdp, "(function(){var row=document.querySelector('[data-weapon-row=\"" + locked + "\"]'); if(row) row.scrollIntoView({block:'center'});})()");
    await shot(cdp, "shop-428-" + locked + "-locked");
    record("shop428-locked-" + locked, await evaluate(cdp, overlapProbe + "('[data-weapon-row=\"" + locked + "\"]')"));
  }
  await evaluate(cdp, "window.__showShop('open')");
  for (var open of ["sword1", "sword2", "axe1", "mace1"]) {
    await evaluate(cdp, "(function(){var row=document.querySelector('[data-weapon-row=\"" + open + "\"]'); if(row) row.scrollIntoView({block:'center'});})()");
    await shot(cdp, "shop-428-" + open + "-open");
    record("shop428-open-" + open, await evaluate(cdp, overlapProbe + "('[data-weapon-row=\"" + open + "\"]')"));
  }
  await size(cdp, 390, 844, true);
  await evaluate(cdp, "window.__showShop('locked')");
  for (var narrow of ["axe1", "mace1"]) {
    await evaluate(cdp, "(function(){var row=document.querySelector('[data-weapon-row=\"" + narrow + "\"]'); if(row) row.scrollIntoView({block:'center'});})()");
    await shot(cdp, "shop-390-" + narrow + "-locked");
    record("shop390-locked-" + narrow, await evaluate(cdp, overlapProbe + "('[data-weapon-row=\"" + narrow + "\"]')"));
  }
  await size(cdp, 428, 926, true);
  await evaluate(cdp, "window.__openCharacter()");
  await evaluate(cdp, "document.querySelector('[data-act=tab][data-arg=gear]').click()");
  await delay(200);
  var names = ["sword-iron", "sword-crystal", "sword-sunforged", "axe-oak", "hammer-builder", "mace-dawn", "cleaver-bloodtide", "greatsword-dragonbane"];
  for (var id of names) {
    await evaluate(cdp, "(function(){var el=document.querySelector('[data-trophy=\"" + id + "\"]'); if(el) el.scrollIntoView({block:'center'});})()");
    await shot(cdp, "character-428-" + id);
    record("character-" + id, await evaluate(cdp, overlapProbe + "('[data-trophy=\"" + id + "\"]')"));
  }
  for (var rowName of ["sword1", "sword2", "axe1", "mace1"]) {
    await evaluate(cdp, "(function(){var row=document.querySelector('[data-weapon-row=\"" + rowName + "\"]'); if(row) row.scrollIntoView({block:'center'});})()");
    await shot(cdp, "character-428-row-" + rowName);
    record("character-row-" + rowName, await evaluate(cdp, overlapProbe + "('[data-weapon-row=\"" + rowName + "\"]')"));
  }
  var modes = await evaluate(cdp, "(function(){var foot=document.querySelector('.footer').getBoundingClientRect(); function one(sel){var el=document.querySelector(sel); var r=el.getBoundingClientRect(); var th=el.querySelector('.th'); var tr=th?th.getBoundingClientRect():r; return {bottom:Math.round(r.bottom), text:Math.round(tr.bottom), foot:Math.round(foot.top), clear:tr.bottom<=foot.top+0.5}; } return {slow:one('[data-arg=slowMode]'), rest:one('[data-arg=restWeeks]')};})()");
  console.log("modes", JSON.stringify(modes));
  if (!modes.slow.clear || !modes.rest.clear) problems.push("modes " + JSON.stringify(modes));
  await shot(cdp, "character-428-modes");

  await size(cdp, 1280, 800, false);
  var gift = await evaluate(cdp, "window.__showGift(1)");
  console.log("gift", JSON.stringify(gift));
  if (!gift || gift.gifts !== "1" || Number(gift.gems) !== 0 || gift.tag.indexOf("Daily gift: +1 gem") < 0 || gift.tag.indexOf("อัญมณีประจำวัน: 1 เม็ด") < 0) problems.push("gift " + JSON.stringify(gift));
  await shot(cdp, "desktop-gift");
  var map = await evaluate(cdp, "window.__mapGems()");
  console.log("map", JSON.stringify(map));
  if (!map || map.gems !== "0" || map.gifts !== "1") problems.push("map " + JSON.stringify(map));
  await shot(cdp, "desktop-map-gems");

  await cdp.send("Page.navigate", { url: "file:///tmp/parts.html" });
  await delay(400);
  await size(cdp, 1100, 280, false);
  await shot(cdp, "weapon-parts-reference");
} catch (err) {
  problems.push(String(err && err.stack || err));
}
console.log(problems.length ? "PROBLEMS\n" + problems.join("\n") : "POLISH_OK");
cdp.close();
server.kill();
chrome.kill();
process.exit(problems.length ? 1 : 0);
