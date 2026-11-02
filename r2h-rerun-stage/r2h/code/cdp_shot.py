# One headless Chrome for all r2h shots, driven over CDP with a tiny stdlib websocket client (no per-shot temp sprawl).
import socket, json, os, base64, struct, subprocess, time, urllib.request, sys
PORT = 9339
def start():
    d = '/tmp/qmtmp/r2h/tmp/cdp'; os.makedirs(d + '/tmp', exist_ok=True)
    p = subprocess.Popen(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--disable-dev-shm-usage', f'--remote-debugging-port={PORT}',
                          f'--user-data-dir={d}/prof', 'about:blank'], env=dict(os.environ, TMPDIR=d + '/tmp'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        try: urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=1); return p
        except Exception: time.sleep(.2)
    raise SystemExit('chrome did not start')
class WS:
    def __init__(self, url):
        host, path = url[5:].split('/', 1); h, pt = host.split(':'); self.s = socket.create_connection((h, int(pt)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(f'GET /{path} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
        b = b''
        while b'\r\n\r\n' not in b: b += self.s.recv(4096)
        self.buf = b.split(b'\r\n\r\n', 1)[1]; self.id = 0
    def _read(self, n):
        while len(self.buf) < n: self.buf += self.s.recv(1 << 20)
        r, self.buf = self.buf[:n], self.buf[n:]; return r
    def recv(self):
        out = b''
        while True:
            h = self._read(2); fin = h[0] & 0x80; ln = h[1] & 0x7f
            if ln == 126: ln = struct.unpack('>H', self._read(2))[0]
            elif ln == 127: ln = struct.unpack('>Q', self._read(8))[0]
            out += self._read(ln)
            if fin: return json.loads(out)
    def call(self, method, **params):
        self.id += 1; m = json.dumps({'id': self.id, 'method': method, 'params': params}).encode(); mask = os.urandom(4)
        hdr = bytes([0x81]) + (bytes([0x80 | len(m)]) if len(m) < 126 else bytes([0x80 | 126]) + struct.pack('>H', len(m)) if len(m) < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', len(m)))
        self.s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(m)))
        while True:
            r = self.recv()
            if r.get('id') == self.id: return r
def session():
    tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
    t = next(t for t in tabs if t.get('type') == 'page'); ws = WS(t['webSocketDebuggerUrl']); ws.call('Page.enable'); return ws
def shot(ws, html, png, w, h, wait=1.2, js=None):
    ws.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=2, mobile=False)
    ws.call('Page.navigate', url='file://' + html); time.sleep(wait)
    ws.call('Runtime.evaluate', expression='document.fonts.ready.then(()=>1)', awaitPromise=True)
    out = None
    if js: out = ws.call('Runtime.evaluate', expression=js, returnByValue=True)['result']['result'].get('value')
    if png:
        r = ws.call('Page.captureScreenshot', format='png', clip=dict(x=0, y=0, width=w, height=h, scale=1))
        open(png, 'wb').write(base64.b64decode(r['result']['data']))
    return out
