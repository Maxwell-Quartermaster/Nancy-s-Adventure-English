// Auditor cdp2.mjs <w> <h> <outdir> <html...>: headless Chrome via CDP (profile/TMPDIR in this folder, nothing deleted); per page geometry JSON + 3 PNGs (normal, plate hidden, plate+knight svgs hidden)
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path';
const D = '/workspace/council-tools/incoming/auditor-gate-fix320-acf48ca2', prof = D + '/render/prof2';
const [w, h, od, ...files] = process.argv.slice(2); const W = +w, H = +h;
const ch = spawn('google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--no-first-run', '--disable-extensions', '--hide-scrollbars', '--disable-dev-shm-usage', '--user-data-dir=' + prof, '--remote-debugging-port=0', 'about:blank'], { env: { ...process.env, TMPDIR: D + '/tmp' }, stdio: 'ignore' });
let port; for (let i = 0; i < 150 && !port; i++) { await new Promise(r => setTimeout(r, 100)); try { port = fs.readFileSync(prof + '/DevToolsActivePort', 'utf8').split('\n')[0]; } catch {} }
const tl = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const pg = tl.find(t => t.type === 'page');
const ws = new WebSocket(pg.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; const evw = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d); delete pend[d.id]; } else if (d.method) evw.forEach(f => f(d)); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.result.value;
const shot = async f => { const s = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } }); fs.writeFileSync(f, Buffer.from(s.result.data, 'base64')); };
const M = `(()=>{const o={};const R=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom].map(v=>Math.round(v*10)/10)};
const pl=[...document.querySelectorAll('div[data-txt]')].filter(d=>d.children.length&&/Echo Knight/.test(d.textContent));o.plate=pl.map(R);const P=pl[0].getBoundingClientRect();
o.plateText=[...pl[0].children].map(c=>[c.textContent,R(c)]);
o.helm=[...document.querySelectorAll('path')].filter(p=>p.getAttribute('fill')=='#8E99A6'||p.getAttribute('d')=='M40 4v-6').map(R);
o.helmTop=Math.min(...o.helm.map(r=>r[1]));o.helmLeft=Math.min(...o.helm.map(r=>r[0]));
const K=[...document.querySelectorAll('svg')].filter(s=>{const r=s.getBoundingClientRect();return r.left>150&&r.left<P.right&&r.top<P.bottom&&r.bottom>P.top});
K.forEach(s=>s.setAttribute('data-aud','k'));o.knightSvgs=K.map(R);o.crossX=K.map(s=>Math.round((P.right-s.getBoundingClientRect().left)*10)/10);
const th=[...document.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&/[\\u0E00-\\u0E7F]/.test(n.textContent)));
o.thai=th.map(e=>{const c=getComputedStyle(e);return [e.textContent.trim().slice(0,20),parseFloat(c.fontSize),c.lineHeight=='normal'?'normal':Math.round(parseFloat(c.lineHeight)/parseFloat(c.fontSize)*100)/100]});
o.scrollW=document.documentElement.scrollWidth;o.bodyScrollW=document.body.scrollWidth;o.innerW=innerWidth;return o})()`;
await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: false });
for (const f of files) {
  const b = path.basename(f, '.html'); const loaded = new Promise(r => evw.push(d => { if (d.method === 'Page.loadEventFired') r(); }));
  await send('Page.navigate', { url: 'file://' + path.resolve(f) }); await loaded; evw.length = 0; await ev('document.fonts.ready.then(()=>1)');
  const m = await ev(M); console.log(JSON.stringify({ file: f, m }));
  await shot(`${od}/${b}.png`);
  await ev(`[...document.querySelectorAll('div[data-txt]')].filter(d=>d.children.length&&/Echo Knight/.test(d.textContent))[0].parentElement.style.visibility='hidden';1`); await shot(`${od}/${b}-noplate.png`);
  await ev(`document.querySelectorAll('svg[data-aud=k]').forEach(s=>s.style.visibility='hidden');1`); await shot(`${od}/${b}-noplate-noknight.png`);
}
ws.close(); ch.kill(); process.exit(0);
