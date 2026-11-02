// cdp.mjs <w> <h> <pngdir|-> <html...> : one headless Chrome (profile in scratch/), per page: geometry JSON line (+ PNG at 2x if pngdir)
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path';
const D = '/workspace/qm/cards-flexgap-20261102-0519', prof = D + '/scratch/prof';
const [w, h, pngdir, ...files] = process.argv.slice(2); const W = +w, H = +h;
try { fs.unlinkSync(prof + '/DevToolsActivePort'); } catch {}
const ch = spawn('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-first-run', '--disable-extensions', '--hide-scrollbars', '--disable-dev-shm-usage', '--user-data-dir=' + prof, '--remote-debugging-port=0', 'about:blank'], { env: { ...process.env, TMPDIR: D + '/scratch/tmp' }, stdio: 'ignore' });
let port; for (let i = 0; i < 100 && !port; i++) { await new Promise(r => setTimeout(r, 100)); try { port = fs.readFileSync(prof + '/DevToolsActivePort', 'utf8').split('\n')[0]; } catch {} }
const tl = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const pg = tl.find(t => t.type === 'page');
const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; const evw = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d); delete pend[d.id]; } else if (d.method) evw.forEach(f => f(d)); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const MJS = fs.readFileSync(process.env.MJS || (D + '/tools/measure.js'), 'utf8');
await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: false });
for (const f of files) {
  const loaded = new Promise(r => evw.push(d => { if (d.method === 'Page.loadEventFired') r(); }));
  await send('Page.navigate', { url: 'file://' + path.resolve(f) }); await loaded; evw.length = 0;
  await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true });
  if (process.env.FREEZE) await send('Runtime.evaluate', { expression: 'document.getAnimations().forEach(a => { a.pause(); a.currentTime = 0; }); document.querySelectorAll("svg").forEach(v => v.pauseAnimations && (v.pauseAnimations(), v.setCurrentTime(0))); new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))', awaitPromise: true });
  const r = await send('Runtime.evaluate', { expression: MJS, returnByValue: true });
  console.log(JSON.stringify({ file: path.basename(f), w: W, h: H, m: r.result.result.value }));
  if (pngdir !== '-') { const s = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } }); fs.writeFileSync(pngdir + '/' + path.basename(f).replace(/\.html$/, '.png'), Buffer.from(s.result.data, 'base64')); }
}
ws.close(); ch.kill(); process.exit(0);
