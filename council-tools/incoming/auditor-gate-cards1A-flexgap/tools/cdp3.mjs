// Auditor cdp3.mjs <w> <h> <pngdir> <html...>: headless Chrome via CDP, profile/TMPDIR in this folder, nothing deleted.
// Per page: animations paused at t=0 (and SVG SMIL at 0), PNG at DPR 2, plus a sweep of flex boxes with a non-normal gap and all element rects.
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path';
const D = '/workspace/council-tools/incoming/auditor-gate-cards1A-flexgap', prof = D + '/render/' + (process.env.PROF || 'prof');
const [w, h, od, ...files] = process.argv.slice(2); const W = +w, H = +h;
const ch = spawn('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-first-run', '--disable-extensions', '--hide-scrollbars', '--disable-dev-shm-usage', '--user-data-dir=' + prof, '--remote-debugging-port=0', 'about:blank'], { env: { ...process.env, TMPDIR: D + '/tmp' }, stdio: 'ignore' });
let port; for (let i = 0; i < 150 && !port; i++) { await new Promise(r => setTimeout(r, 100)); try { port = fs.readFileSync(prof + '/DevToolsActivePort', 'utf8').split('\n')[0]; } catch {} }
const tl = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const pg = tl.find(t => t.type === 'page');
const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; const evw = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d); delete pend[d.id]; } else if (d.method) evw.forEach(f => f(d)); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.result.value;
await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: false });
for (const f of files) {
  const loaded = new Promise(r => evw.push(d => { if (d.method === 'Page.loadEventFired') r(); }));
  await send('Page.navigate', { url: 'file://' + path.resolve(f) }); await loaded; evw.length = 0; await ev('document.fonts.ready.then(()=>1)');
  await ev('document.getAnimations().forEach(a=>{a.pause();a.currentTime=0});document.querySelectorAll("svg").forEach(v=>{if(v.pauseAnimations){v.pauseAnimations();v.setCurrentTime(0)}});1');
  const m = await ev(`(()=>{const g=[...document.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return /flex/.test(c.display)&&(c.rowGap!='normal'&&c.rowGap!='0px'||c.columnGap!='normal'&&c.columnGap!='0px')}).map(e=>(e.getAttribute('style')||'').slice(0,70));
   const r=[...document.querySelectorAll('body *')].map(e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height].map(v=>Math.round(v*100)/100).join(',')});
   return {flexGap:g, nEl:r.length, rects:r, scrollW:document.documentElement.scrollWidth}})()`);
  const s = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  const out = od + '/' + path.basename(path.dirname(f)) + '__' + path.basename(f).replace(/\.html$/, '.png'); fs.writeFileSync(out, Buffer.from(s.result.data, 'base64'));
  console.log(JSON.stringify({ file: f, png: out, ...m }));
}
ws.close(); ch.kill(); process.exit(0);
