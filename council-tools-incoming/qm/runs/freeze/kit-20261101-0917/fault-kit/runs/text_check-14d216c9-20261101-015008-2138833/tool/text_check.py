#!/usr/bin/env python3
"""text-check: retired wording, fail words and Thai size on sheets/ and showcase/ (owner: Instructor; QM split, Nov 1 2026).
No OCR on the box, so an image is checked through the text it was built from: its sidecar <img>.sources.txt, a same-name .html,
the showcase tour (tour.py SHEETS), or the sheet builder script found in the snapshot (captions, and every render it pastes).
An image whose text can't be traced is TEXT UNVERIFIED (blocks a send), never a quiet pass.
Usage:
  python3 text_check.py [--snap DIR] PATH [PATH ...]   files or folders (a folder is walked)
  python3 text_check.py --selftest
API: check(path) -> list of blocking problems (strings), like ground_check.check; check_full(path) -> dict(block, warn, sources, status).
Exit 0 = clear (warnings may print); 1 = BLOCK (problems listed); 2 = bad input. Writes to stdout only (selftest scratch in ./runs/selftest-*)."""
import ast, json, os, re, sys, hashlib, subprocess, tempfile, shutil, glob
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, 'text_check_words.json')
CODE_EXT = ('.py', '.sh', '.js', '.css', '.diff', '.patch')
HASH_EXT = ('.md5', '.sha1', '.sha256')
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.gif'); DOC_EXT = ('.md', '.txt', '.json', '.log'); HTML_EXT = ('.html', '.htm')
THAI = re.compile(r'[\u0E00-\u0E7F]')
MTIME_SLACK = 5.0   # seconds: html written just after its png in the same render pass is normal
BURST_MAX = 120.0   # seconds: a snapshot whose files' mtimes all fall inside this span was written in one plain-copy pass (cp / shutil.copy), so their order means nothing
SIDECAR_KEYS = ('source_md5', 'html_md5', 'src_md5', 'source_sha256', 'html_sha256', 'source_sha1', 'html_sha1', 'source_hash', 'html_hash')   # flat keys in QM's per-PNG <name>.json
SIDECAR_NEST = (('source', 'html', 'src'), ('md5', 'sha256', 'sha1', 'sha', 'hash', 'md5sum'))   # or nested: {"source": {"md5": ...}}
CHROME = shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def hash_as(p, ref):
    """hash p with the algorithm a recorded hex digest's length implies (32 md5, 40 sha1, 64 sha256)"""
    f = {32: hashlib.md5, 40: hashlib.sha1, 64: hashlib.sha256}.get(len(ref))
    if f is None: return None
    h = f()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
HEXD = re.compile(r'^(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$')
def png_sidecar(png):
    """QM renderer's per-PNG sidecar <name>.json -> (path, dict or None, recorded source hash or None, key or reason), or None if there is none"""
    sc = os.path.splitext(png)[0] + '.json'
    if not os.path.isfile(sc) or os.path.abspath(sc) == os.path.abspath(png): return None
    try: d = json.load(open(sc, encoding='utf-8'))
    except (OSError, ValueError) as e: return (sc, None, None, f'unreadable: {type(e).__name__}')
    if not isinstance(d, dict): return (sc, None, None, 'not a JSON object')
    for k in SIDECAR_KEYS:
        v = d.get(k)
        if isinstance(v, str) and HEXD.match(v.strip()): return (sc, d, v.strip().lower(), k)
    for par in SIDECAR_NEST[0]:
        o = d.get(par)
        if isinstance(o, dict):
            for k in SIDECAR_NEST[1]:
                v = o.get(k)
                if isinstance(v, str) and HEXD.match(v.strip()): return (sc, d, v.strip().lower(), f'{par}.{k}')
    return (sc, d, None, None)
def is_image(p):
    try: h = open(p, 'rb').read(12)
    except OSError: return False
    return p.lower().endswith(IMG_EXT) or h.startswith(b'\x89PNG') or h.startswith(b'\xff\xd8\xff') or h.startswith(b'GIF8') or (h[:4] == b'RIFF' and h[8:12] == b'WEBP')
def rel(p, ctx=None):
    p = os.path.abspath(p)
    if ctx and ctx.snap_dir and p.startswith(ctx.snap_dir + os.sep): return p[len(ctx.snap_dir) + 1:]
    return p.replace('/workspace/', '') if p.startswith('/workspace/') else p
def wh_from_name(p, default=(390, 844)):
    m = re.search(r'(\d{3})x(\d{3,4})', os.path.basename(p)); return (int(m.group(1)), int(m.group(2))) if m else default

# ---------------------------------------------------------------- context: pointer, PASTE, word lists
class Ctx:
    def __init__(self, pointer=None, snap=None, paste=None, data=DATA):
        self.notes, self.warn = [], []
        self.words = json.load(open(data, encoding='utf-8'))
        self.fatal = None
        if not self.words.get('retired') or not self.words.get('fail_words', {}).get('en') or not self.words.get('fail_words', {}).get('th'):
            self.fatal = f'word list {data} has an empty retired/fail_words list; refusing to pass anything'
        miss = [i for i in NEVER_IDS if not any(e.get('id') == i for e in self.words.get('fail_words', {}).get('en', []))]
        if miss and not self.fatal: self.fatal = f'word list {data} is missing never-word entries {", ".join(miss)}; refusing to pass anything'
        self.pointer_md5 = self.snap = None; self.snap_dir = os.path.abspath(snap) if snap else None; self.paste = paste
        if pointer is None: pointer = os.environ.get('CURRENT_SNAP', '/workspace/v608build/CURRENT-SNAP.txt')
        if pointer and os.path.isfile(pointer):
            d = {}
            for line in open(pointer, encoding='utf-8'):
                if '=' in line: k, v = line.rstrip('\n').split('=', 1); d[k.strip()] = v.strip()
            self.pointer_md5 = md5(pointer); self.snap = d.get('snap')
            if not self.snap_dir and self.snap: self.snap_dir = os.path.join(os.path.dirname(os.path.abspath(pointer)), self.snap)
            if not self.paste and d.get('paste_1b_path'):
                self.paste = os.path.join(os.path.dirname(os.path.abspath(pointer)), d['paste_1b_path'])
                if not re.fullmatch(r'[0-9a-f]{32}', d.get('paste_1b_md5', '')): self.fatal = self.fatal or f'pointer {pointer} has no valid paste_1b_md5, so the paste can\'t be tied to it'
                elif os.path.isfile(self.paste) and md5(self.paste) != d['paste_1b_md5']:
                    self.fatal = self.fatal or f'paste_1b {rel(self.paste)} md5 {md5(self.paste)[:8]} != pointer {d["paste_1b_md5"][:8]}'
            self.ptr_manifest = d.get('manifest_md5', ''); self.ptr_renders = d.get('renders_manifest_md5', '')
        if self.snap_dir and not self.snap: self.snap = os.path.basename(self.snap_dir.rstrip('/'))
        if not self.paste or not os.path.isfile(self.paste): self.fatal = self.fatal or f'no paste_1b to read live wording from (pointer {pointer})'
        self.paste_md5 = md5(self.paste) if self.paste and os.path.isfile(self.paste) else None
        self.ui, self.content = {}, set()
        if not self.fatal: self._load_paste()
        self.retired = [(e, re.compile(e['regex'], re.I)) for e in self.words['retired']]
        self.fail = [(e, re.compile(e['regex'], re.I), 'en') for e in self.words['fail_words']['en']] + [(e, re.compile(e['regex']), 'th') for e in self.words['fail_words']['th']]
        self.min_cover = self.words['allow'].get('min_cover_len', 12); self.min_px = self.words['thai_size']['min_px']
        self.man = {}; self.man_path = {}; self.man_from = {}; self._window = False
        if self.snap_dir:
            for name in ('MANIFEST.md5', 'renders-MANIFEST.md5'):
                p = os.path.join(self.snap_dir, name)
                if os.path.isfile(p):
                    for line in open(p, encoding='utf-8', errors='replace'):
                        m = re.match(r'^([0-9a-f]{32})\s+\*?(.+)$', line.strip())
                        if m: self.man.setdefault(m.group(1), []).append(m.group(2).lstrip('./') if name == 'MANIFEST.md5' else None)
                        if m:   # path -> recorded md5 (for the copy-burst rule); MANIFEST.md5 paths are snapshot-relative, renders-MANIFEST ones snapshot- or /workspace-relative
                            q = m.group(2); q = q[2:] if q.startswith('./') else q
                            for base in ((self.snap_dir,) if name == 'MANIFEST.md5' else (self.snap_dir, '/workspace')):
                                ap = os.path.normpath(os.path.join(base, q))
                                if name == 'MANIFEST.md5' or os.path.isfile(ap): self.man_path.setdefault(ap, m.group(1)); self.man_from.setdefault(ap, name); break
        self._thai_cache = {}
    def _load_paste(self):
        data = None
        for line in open(self.paste, encoding='utf-8'):
            if line.startswith('{"version"'):
                try: data = json.loads(line); break
                except ValueError: pass
        if data is None: self.fatal = f'no JSON data line in {rel(self.paste)}'; return
        self.data = data; self.ui = data.get('uiText', {})
        def walk(o):
            if isinstance(o, dict):
                for v in o.values(): yield from walk(v)
            elif isinstance(o, list):
                for v in o: yield from walk(v)
            elif isinstance(o, str): yield o
        for k in self.words['allow']['content_keys']:
            for s in walk(data.get(k, [])):
                s = ' '.join(s.split())
                if s: self.content.add(s)
        for e in self.words['retired']:   # the list is checked against the live PASTE every run
            v = self.get(e['now_path'])
            if v is None: self.warn.append(f'STALE-LIST {e["id"]}: {e["now_path"]} not found in paste_1b')
            elif re.search(e['regex'], v, re.I): self.warn.append(f'STALE-LIST {e["id"]}: retired pattern is LIVE in paste_1b {e["now_path"]} = {v!r}; update the list')
        for e in self.words.get('not_retired', []):
            v = self.get(e['path'])
            if v is None or not re.search(e['must_match'], v): self.warn.append(f'STALE-LIST {e["id"]}: paste_1b {e["path"]} = {v!r}, expected /{e["must_match"]}/')
            else: self.notes.append(f'live {e["path"]} = {v!r}')
    def get(self, path):
        o = self.data
        for k in path.split('.'):
            if not isinstance(o, dict) or k not in o: return None
            o = o[k]
        return o if isinstance(o, str) else None
    def manifest_ok(self):
        """the copy-burst rule leans on MANIFEST md5s, so the MANIFEST itself must be the one the pointer names"""
        mf = os.path.join(self.snap_dir or '/nonexistent', 'MANIFEST.md5'); pm = getattr(self, 'ptr_manifest', '')
        return bool(re.fullmatch(r'[0-9a-f]{32}', pm or '')) and os.path.isfile(mf) and md5(mf) == pm
    def manifest_trusted(self, ap):
        """the MANIFEST that recorded ap counts only if its own md5 is the one the pointer names (a rewritten MANIFEST must not launder an edit)"""
        name = self.man_from.get(ap)
        if not name: return False
        want = getattr(self, 'ptr_manifest', '') if name == 'MANIFEST.md5' else getattr(self, 'ptr_renders', '')
        mf = os.path.join(self.snap_dir or '/nonexistent', name)
        return bool(re.fullmatch(r'[0-9a-f]{32}', want or '')) and os.path.isfile(mf) and md5(mf) == want
    def copy_window(self):
        """(first, last, MANIFEST mtime) when every MANIFEST-listed snapshot file (and the MANIFEST) was written within BURST_MAX s: a plain-copy
        freeze, where an html can look newer than its png only because it was copied later. None for a preserved-mtime (cp -p / copy2) snapshot."""
        if self._window is not False: return self._window
        self._window = None; mf = os.path.join(self.snap_dir or '/nonexistent', 'MANIFEST.md5')
        if os.path.isfile(mf):
            fs = [p for p in self.man_path if p.startswith(self.snap_dir + os.sep) and os.path.isfile(p)]
            if not fs: fs = [os.path.join(r_, f) for r_, _, fl in os.walk(self.snap_dir) for f in fl]   # MANIFEST lists nothing: time the files on disk
            ts = [os.path.getmtime(mf)] + [os.path.getmtime(p) for p in fs if os.path.isfile(p)]
            if len(ts) > 1 and max(ts) - min(ts) <= BURST_MAX: self._window = (min(ts), max(ts), ts[0])
        return self._window
    def stamp(self):
        return (f'text-check {md5(os.path.abspath(__file__))[:8]} words {md5(DATA)[:8] if os.path.isfile(DATA) else "none"} pointer {(self.pointer_md5 or "none")[:8]} '
                f'snap {self.snap or "?"} paste_1b {(self.paste_md5 or "none")[:8]} chrome {"yes" if CHROME else "no"}')

_CTX = {}
def context(pointer=None):
    key = pointer or os.environ.get('CURRENT_SNAP', '/workspace/v608build/CURRENT-SNAP.txt')
    pm = md5(key) if os.path.isfile(key) else None
    if (key, pm) not in _CTX: _CTX[(key, pm)] = Ctx(key)
    return _CTX[(key, pm)]

# ---------------------------------------------------------------- text extraction and matching
INVIS = re.compile('[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff]')   # zero-width / format chars: invisible, so the eye reads straight through them
def norm(s): return ' '.join(INVIS.sub('', s).split())
# never-words (standing council rules: never '911', 'Call Max', 'Show the Nurse'): BLOCK wherever they can be seen, captions included;
# no PASTE-content allow and no warn-only path (caption, data-*, script string) exempts them. Council notes (.md/.txt) still only warn.
NEVER_IDS = ('F-911', 'F-callmax', 'F-nurse')
def is_never(e): return bool(e.get('never')) or e.get('id') in NEVER_IDS
INLINE = {'span', 'b', 'i', 'em', 'strong', 'a', 'small', 'sup', 'sub', 'u', 'font', 'mark', 'abbr', 'code', 'q', 's', 'wbr', 'tspan', 'label', 'bdi', 'bdo', 'ruby', 'rt'}
class _Text(HTMLParser):
    SKIP = {'script', 'style', 'template', 'noscript'}; ATTRS = ('alt', 'aria-label', 'aria-description', 'aria-roledescription', 'aria-valuetext', 'title', 'placeholder', 'value', 'label', 'summary')
    def __init__(self): super().__init__(convert_charrefs=True); self.segs, self.skip, self.run, self.css, self.js, self.intag = [], 0, [], [], [], None
    def _flush(self):
        if len(self.run) > 1: self.segs.append(('text across tags', ''.join(self.run)))
        self.run = []
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP: self.skip += 1; self.intag = tag
        if tag == 'br': self.run.append(' ')
        elif tag not in INLINE: self._flush()
        for k, v in attrs:
            if k in self.ATTRS and v and v.strip(): self.segs.append(('attr ' + k, v))
            elif k == 'style' and v and 'content' in v: self.css.append(v)
            elif k.startswith('data-') and v and v.strip(): self.segs.append(('attr ' + k + ' (warn)', v))
    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip: self.skip -= 1
        if tag not in INLINE and tag != 'br': self._flush()
    def handle_data(self, d):
        if self.skip:
            (self.css if self.intag == 'style' else self.js).append(d); return
        if d.strip(): self.segs.append(('text', d))
        self.run.append(d)
    def close(self): super().close(); self._flush()
CSS_CONTENT = re.compile(r'content\s*:\s*(["\'])(.*?)\1', re.S); JS_STR = re.compile(r'(["\'`])((?:\\.|(?!\1).){2,200}?)\1')
def html_segments(path):
    p = _Text(); p.feed(open(path, encoding='utf-8', errors='replace').read()); p.close()
    segs = [(k, norm(s)) for k, s in p.segs]
    segs += [('css content', norm(m.group(2))) for c in p.css for m in CSS_CONTENT.finditer(c)]
    segs += [('script string (warn)', norm(m.group(2))) for c in p.js for m in JS_STR.finditer(c)]
    return [x for x in segs if x[1]]

def allowed(ctx, seg, m):
    if seg in ctx.content: return f'is a current PASTE content string'
    for c in ctx.content:
        if len(c) >= ctx.min_cover:
            i = seg.find(c)
            while i >= 0:
                if i <= m.start() and m.end() <= i + len(c): return f'inside PASTE content string "{c[:40]}"'
                i = seg.find(c, i + 1)
    return None
def scan(ctx, segs, where):
    """segs: [(kind, text)] -> (retired hits, fail hits, allowed notes); each hit (entry, match text, segment, where)"""
    ret, fail, ok = [], [], []
    for kind, s in segs:
        for e, rx in ctx.retired:
            for m in rx.finditer(s):
                a = allowed(ctx, s, m)
                (ok.append(f'{e["id"]} "{m.group(0)}" in "{s[:60]}" ({where}): {a}') if a else ret.append((e, m.group(0), s, where, kind)))
        for e, rx, lang in ctx.fail:
            for m in rx.finditer(s):
                a = None if is_never(e) else allowed(ctx, s, m)
                (ok.append(f'{e["id"]} "{m.group(0)}" in "{s[:60]}" ({where}): {a}') if a else fail.append((e, m.group(0), s, where, kind)))
    return ret, fail, ok
def fmt_hit(tag, h):
    e, mt, s, where, kind = h
    cite = e.get('decision', '').split(':')[0] if tag == 'RETIRED' else ('never-word, standing council rule' if tag == 'NEVER-WORD' else 'fail word' + (f' ({e["gloss"]})' if e.get('gloss') else ''))
    return f'{tag} {e["id"]} "{mt}" in {where} [{kind}]: "{s[:90]}"' + (f' ({cite})' if cite else '')

# ---------------------------------------------------------------- Thai size (headless Chrome, as domcheck_r2 / stage_v608 run it)
THAI_JS = r"""<script>addEventListener('load',()=>{setTimeout(()=>{const out=[];
const vis=e=>{const s=getComputedStyle(e);if(s.display=='none'||s.visibility=='hidden'||+s.opacity==0)return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
for(const e of document.querySelectorAll('body *')){if(e.id=='__tcx')continue;const own=[...e.childNodes].filter(n=>n.nodeType==3).map(n=>n.textContent).join('');if(!/[\u0E00-\u0E7F]/.test(own))continue;
 const v=vis(e);const fs=parseFloat(getComputedStyle(e).fontSize);let k=1;for(let p=e;p&&p.nodeType==1;p=p.parentElement){const cs=getComputedStyle(p);if(cs.transform&&cs.transform!='none'){const m=new DOMMatrixReadOnly(cs.transform);k*=Math.hypot(m.a,m.b)}if(cs.zoom&&cs.zoom!='1'&&cs.zoom!='normal')k*=parseFloat(cs.zoom)||1}
 out.push([own.trim().replace(/\s+/g,' ').slice(0,40),fs,Math.round(fs*k*100)/100,v?1:0])}
const pre=document.createElement('pre');pre.id='__tcx';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},300)})</script>"""
def thai_sizes(ctx, html, w, h):
    """[(text, css px, effective px, visible)] or None when it can't be measured"""
    key = (os.path.abspath(html), os.path.getmtime(html), w, h)
    if key in ctx._thai_cache: return ctx._thai_cache[key]
    res = None
    if CHROME:
        s = open(html, encoding='utf-8', errors='replace').read(); s = s.replace('</body>', THAI_JS + '</body>') if '</body>' in s else s + THAI_JS
        d = tempfile.mkdtemp(prefix='tc-', dir='/tmp'); src = os.path.join(d, 'm.html')
        base = '<base href="file://' + os.path.dirname(os.path.abspath(html)) + '/">'   # relative assets resolve; nothing is written next to the source
        s = re.sub(r'(<head[^>]*>)', lambda m_: m_.group(1) + base, s, count=1) if re.search(r'<head[^>]*>', s) else base + s
        try:
            open(src, 'w', encoding='utf-8').write(s)
            o = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--virtual-time-budget=3000', f'--window-size={w},{h}', '--dump-dom', 'file://' + src],
                               capture_output=True, text=True, timeout=120, env=dict(os.environ, TMPDIR=d)).stdout
            m = re.search(r'<pre id="__tcx">(.*?)</pre>', o, re.S)
            if m:
                import html as H; res = json.loads(H.unescape(m.group(1)))
        except Exception: res = None
        finally: shutil.rmtree(d, ignore_errors=True)   # our own /tmp scratch only
    ctx._thai_cache[key] = res; return res

# ---------------------------------------------------------------- tracing an image to its text
class Trace:
    def __init__(self): self.html, self.captions, self.unverified, self.warn, self.sources, self.unfrozen = [], [], [], [], [], []
    def add_html(self, path, wh, label, frozen):
        self.html.append((path, wh, label)); self.sources.append(f'html {rel(path)} {wh[0]}x{wh[1]} ({label})' + ('' if frozen else ' [outside snapshot]'))
        if not frozen: self.unfrozen.append(rel(path))

def r2tp_copy(html, outdirs):
    b = os.path.basename(os.path.dirname(os.path.dirname(html))) + '--' + os.path.basename(html)
    for d in outdirs:
        if d and os.path.isfile(os.path.join(d, b)): return os.path.join(d, b)
    return None
def png_to_html(png):
    d, b = os.path.split(png); stem = os.path.splitext(b)[0]
    c = [os.path.join(d, stem + '.html')]
    if os.path.basename(d) in ('png', 'renders'): c.append(os.path.join(os.path.dirname(d), 'html', stem + '.html'))   # renders/: scene-fill layout
    return [x for x in c if os.path.isfile(x)]

def fresh(ctx, src, img, t, label, msg, sidecar=True):
    """is src still the text img was made from?  1) QM's per-PNG sidecar <img>.json with a recorded source hash: match = VERIFIED whatever the
    mtimes say, mismatch = TEXT UNVERIFIED.  2) no hash: mtime (src newer than img by > MTIME_SLACK = edited).  An mtime gap inside a plain-copy
    snapshot pass is accepted as a copy only when src (and img, if listed) still match the snapshot MANIFEST md5, and that is always printed."""
    if sidecar:
        sc = png_sidecar(img)
        if sc:
            path, d, ref, key = sc
            if ref:
                cur = hash_as(src, ref); hn = d.get('html') if isinstance(d, dict) else None
                if isinstance(hn, str) and os.path.basename(hn) != os.path.basename(src):
                    t.warn.append(f'SIDECAR-NAME {label}: {rel(path, ctx)} says the render came from {hn}, but the source traced is {os.path.basename(src)}')
                if cur == ref:
                    prov = d.get('html_md5_src'); pref = d.get('png_md5')
                    if d.get('html_md5_backfill') is True: prov = 'backfill'   # an explicit backfill flag outranks any src label
                    if isinstance(pref, str) and HEXD.match(pref.strip()) and hash_as(img, pref.strip().lower()) != pref.strip().lower():
                        t.unverified.append(f'{label}: {rel(img, ctx)} is not the png its sidecar {rel(path, ctx)} recorded (png_md5 {pref[:8]}), so it may be another render'); return False
                    if prov == 'render' and isinstance(pref, str) and HEXD.match(pref.strip()):
                        t.sources.append(f'sidecar {rel(path, ctx)} {key} {ref[:8]} = {rel(src, ctx)} (html_md5_src=render, png_md5 match): VERIFIED by hash (mtime not used)'); return True
                    # backfilled or unlabelled hash: it proves the html hasn't changed since the hash was written, not since the render.
                    # Then the snapshot MANIFEST (only if the pointer names that MANIFEST's md5): a different md5 there = UNVERIFIED. A match proves the html is
                    # unchanged since the FREEZE, not since the render (an edit before the freeze is in the MANIFEST too: V08), so the time check still decides
                    # (its copy-burst rule covers plain-cp snapshots). No timing window on the sidecar's own mtime.
                    sa_ = os.path.abspath(src); rec_ = ctx.man_path.get(sa_)
                    if rec_ and ctx.manifest_trusted(sa_):
                        if rec_ == cur:
                            t.sources.append(f'sidecar {rel(path, ctx)} {key} {ref[:8]} (html_md5_src={prov!r}) = {rel(src, ctx)} = pointer-named {ctx.man_from[sa_]} {rec_[:8]}: unchanged since the freeze; time check still used (not render-time VERIFIED)')
                        else: t.unverified.append(f'{label}: render sidecar {rel(path, ctx)} {key} {ref[:8]} matches today\'s {rel(src, ctx)}, but the pointer-named {ctx.man_from[sa_]} recorded {rec_[:8]} for it, so the html (and the sidecar hash) changed after the freeze'); return False
                    elif rec_: t.warn.append(f'MANIFEST-NOT-POINTER {label}: {ctx.man_from[sa_]} lists {rel(src, ctx)} but its md5 is not the one the pointer names, so it is not used')
                    t.warn.append(f'SIDECAR-NOT-RENDER-TIME {label}: {rel(path, ctx)} {key} matches, but html_md5_src={prov!r}' + ('' if isinstance(pref, str) else ' and no png_md5') + '; hash taken as a floor only, time check still used')
                    sidecar = False
                else:
                    t.unverified.append(f'{label}: {rel(src, ctx)} is {(cur or "?")[:8]} but its render sidecar {rel(path, ctx)} recorded {key} {ref[:8]}, so the html was edited after its render {rel(img, ctx)}'); return False
            elif d is None: t.warn.append(f'SIDECAR-UNREADABLE {label}: {rel(path, ctx)} ({key}); used the time check instead')
            else:
                t.sources.append(f'sidecar {rel(path, ctx)} has no source hash (fields: {", ".join(sorted(d))}); time check used')
                hn = d.get('html')
                if isinstance(hn, str) and os.path.basename(hn) != os.path.basename(src):
                    t.warn.append(f'SIDECAR-NAME {label}: {rel(path, ctx)} says the render came from {hn}, but the source traced is {os.path.basename(src)}')
    ms, mi = os.path.getmtime(src), os.path.getmtime(img)
    if ms <= mi + MTIME_SLACK: return True
    w = ctx.copy_window() if ctx.manifest_ok() else None
    if ctx.copy_window() and not w: t.warn.append(f'COPY-BURST-OFF {label}: snapshot MANIFEST.md5 is not the one the pointer names (or the pointer has no manifest_md5), so a copy pass can\'t be told from an edit')
    sa, ia = os.path.abspath(src), os.path.abspath(img)
    if w and all(w[0] - 0.5 <= x <= w[1] + 0.5 for x in (ms, mi)):
        rec, reci = ctx.man_path.get(sa), ctx.man_path.get(ia)
        why = None
        if not rec: why = 'the snapshot MANIFEST has no md5 for it'
        elif md5(src) != rec: why = f'it no longer matches the MANIFEST ({md5(src)[:8]} != {rec[:8]})'
        elif reci and md5(img) != reci: why = f'its render no longer matches the MANIFEST ({md5(img)[:8]} != {reci[:8]})'
        if why is None:
            t.warn.append(f'COPY-BURST {label}: {rel(src, ctx)} is {ms - mi:.0f} s newer than {rel(img, ctx)}, but the whole snapshot was written in one {w[1] - w[0]:.0f} s copy pass and the html still matches MANIFEST {rec[:8]}; treated as a copy, not an edit')
            return True
        t.unverified.append(f'{label}: {rel(src, ctx)} is {ms - mi:.0f} s newer than its render {rel(img, ctx)}; the times look like a snapshot copy pass, but {why}, so an edit can\'t be ruled out')
        return False
    t.unverified.append(msg.replace('{dt:.0f}', f'{ms - mi:.0f}')); return False

def trace_render(ctx, png, t, label, depth, frozen_root):
    """a render pasted into a sheet: find its html (or its own sources) and add it to the trace"""
    if png.lower().endswith(HTML_EXT):
        if not os.path.isfile(png): t.unverified.append(f'{label}: source {rel(png)} not found'); return
        t.add_html(png, wh_from_name(png), label, png.startswith(frozen_root)); return
    if not os.path.isfile(png): t.unverified.append(f'{label}: render {rel(png)} not found, so its text can\'t be read'); return
    if trace_sidecar(ctx, png, t, label, depth, frozen_root): return
    hs = png_to_html(png)
    if hs:
        h = hs[0]
        fresh(ctx, h, png, t, label, f'{label}: {rel(h)} was edited after its render {rel(png)} (html newer by {{dt:.0f}} s), so the render may show other text')
        t.add_html(h, wh_from_name(h, wh_from_name(png)), label, h.startswith(frozen_root)); return
    if depth < 2 and trace_builder(ctx, png, t, label, depth + 1): return
    t.unverified.append(f'{label}: no html, sidecar or builder found for {rel(png)}')

def trace_sidecar(ctx, img, t, label, depth, frozen_root):
    for sc in (img + '.sources.txt', os.path.splitext(img)[0] + '.sources.txt'):
        if os.path.isfile(sc):
            t.sources.append(f'sidecar {rel(sc, ctx)}')
            n = ncap = 0
            for line in open(sc, encoding='utf-8', errors='replace'):
                c = re.match(r'^caption\s*[:\t ]\s*(\S.*)$', line.strip())   # optional: text the sheet builder drew (titles, tile captions, footer), one per line
                if c: ncap += 1; t.captions.append((c.group(1), f'{rel(sc, ctx)} caption', 'caption')); continue
                m = re.match(r'^([0-9a-f]{32})\s+(\S.*)$', line.strip())
                if not m: continue
                n += 1; p = m.group(2)
                if not os.path.isfile(p): t.unverified.append(f'{label}: sidecar source {rel(p)} missing'); continue
                if md5(p) != m.group(1): t.unverified.append(f'{label}: sidecar source {rel(p)} changed since the sheet was made ({md5(p)[:8]} != {m.group(1)[:8]})'); continue
                trace_render(ctx, p, t, f'{label} / {os.path.basename(p)}', depth, frozen_root)
            if not n: t.unverified.append(f'{label}: sidecar {rel(sc)} lists no sources')
            if n > 1 and not ncap: t.warn.append(f'CAPTIONS-UNCHECKED {label}: sidecar {rel(sc, ctx)} lists {n} sources but no "caption" lines, so text the sheet builder drew (titles, tile captions, footer) is not scanned')
            return True
    return False

# --- builder scripts (AST, never executed)
def _env(tree):
    env = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            if len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                v = _res(n.value, env)
                if v is not None: env[n.targets[0].id] = v
                elif isinstance(n.value, ast.Tuple) and all(isinstance(x, ast.Constant) for x in n.value.elts): env[n.targets[0].id] = tuple(x.value for x in n.value.elts)
            elif len(n.targets) == 1 and isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, ast.Tuple) and len(n.targets[0].elts) == len(n.value.elts):
                for a, b in zip(n.targets[0].elts, n.value.elts):
                    if isinstance(a, ast.Name):
                        v = _res(b, env)
                        if v is not None: env[a.id] = v
                        elif isinstance(b, ast.Tuple) and all(isinstance(x, ast.Constant) for x in b.elts): env[a.id] = tuple(x.value for x in b.elts)
    return env
def _res(n, env):
    if isinstance(n, ast.Constant) and isinstance(n.value, str): return n.value
    if isinstance(n, ast.Name) and isinstance(env.get(n.id), str): return env[n.id]
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        a, b = _res(n.left, env), _res(n.right, env); return a + b if a is not None and b is not None else None
    if isinstance(n, ast.JoinedStr):
        out = []
        for v in n.values:
            if isinstance(v, ast.Constant): out.append(v.value)
            elif isinstance(v, ast.FormattedValue) and v.format_spec is None:
                r = _res(v.value, env)
                if r is None: return None
                out.append(r)
            else: return None
        return ''.join(out)
    return None
def _fname(c):
    f = c.func; return f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else '')
def _parents(tree):
    par = {}
    for n in ast.walk(tree):
        for ch in ast.iter_child_nodes(n): par[ch] = n
    return par
PATHY = re.compile(r'^[^\s]*(/|\.(png|html?|py|ttf|md|txt|json|svg|md5|sh)$|^#[0-9a-fA-F]{3,8}$)')
def _docstrings(tree):
    ds = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant): ds.add(n.body[0].value)
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant): ds.add(n.value)
    return ds
def text_constants(path, tree=None, roots=None):
    """every string an image builder could draw: AST constants and f-string text, minus docstrings, regex/re.* arguments and paths.
    roots: only these top-level statements (one output's part of a multi-output builder)"""
    tree = tree or ast.parse(open(path, encoding='utf-8').read()); par = _parents(tree); ds = _docstrings(tree); out = []
    nodes = [x for r in (roots if roots is not None else [tree]) for x in ast.walk(r)]
    for n in nodes:
        if not (isinstance(n, ast.Constant) and isinstance(n.value, str)) or n in ds: continue
        p, inre = par.get(n), False
        while p is not None:
            if isinstance(p, ast.Call) and isinstance(p.func, ast.Attribute) and isinstance(p.func.value, ast.Name) and p.func.value.id.lstrip('_') in ('re',): inre = True; break
            if isinstance(p, ast.Call) and _fname(p) in ('open', 'insert', 'truetype', 'glob', 'join', 'run', 'Popen', 'startswith', 'endswith', 'split', 'replace', 'new', 'convert'): inre = True; break
            p = par.get(p)
        s = ' '.join(n.value.split())
        if inre or not s or PATHY.match(s) or not re.search(r'[A-Za-z\u0E00-\u0E7F]', s): continue
        out.append((s, n.lineno))
    return out
def _local_imports(tree, script, ctx):
    """helper modules a builder imports from the build tree (round_totals, r2_fit_table, sheetkit ...): frozen snapshot copy first"""
    dirs = [os.path.dirname(script)]
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and _fname(n) == 'insert' and len(n.args) == 2 and isinstance(n.args[1], ast.Constant) and isinstance(n.args[1].value, str): dirs.append(n.args[1].value)
    names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import): names |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level: names.add(n.module)
    found = []
    for nm in sorted(names):
        snapc = sorted(glob.glob(os.path.join(ctx.snap_dir or '/nonexistent', '**', nm + '.py'), recursive=True)) if ctx.snap_dir else []
        live = [os.path.join(d if d != '.' else os.path.dirname(script), nm + '.py') for d in dirs]
        live = [p for p in live if os.path.isfile(p)]
        if snapc: found.append((nm, snapc[0], True))
        elif live: found.append((nm, live[0], False))
    return found
def _outputs(tree, env):
    """[(top-level statement index, output path)] for every save()/sheet() call whose first argument resolves to an image path"""
    outs = []
    for i, st in enumerate(tree.body):
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): continue
        for n in ast.walk(st):
            if isinstance(n, ast.Call) and _fname(n) in ('save', 'sheet') and n.args:
                a = n.args[0]; v = _res(a, env)
                if v is None and isinstance(a, ast.Name):   # out = '...png'; S.save(out)
                    for m in ast.walk(tree):
                        if isinstance(m, ast.Assign) and any(isinstance(x, ast.Name) and x.id == a.id for x in m.targets): v = _res(m.value, env) or v
                if v and v.lower().endswith(IMG_EXT): outs.append((i, v))
    return outs
def find_builders(ctx, img_base, roots):
    out = []
    for root in roots:
        for py in sorted(glob.glob(os.path.join(root, '**', '*.py'), recursive=True)):
            if '__pycache__' in py: continue
            try: src = open(py, encoding='utf-8').read()
            except OSError: continue
            if img_base not in src: continue
            try: tree = ast.parse(src)
            except SyntaxError: continue
            env = _env(tree); outs = _outputs(tree, env); mine = [o for o in outs if os.path.basename(o[1]) == img_base]
            if mine: out.append((py, tree, env, mine[0][1], mine[0][0], outs))
    return out
def trace_builder(ctx, img, t, label, depth):
    base = os.path.basename(img); roots = [ctx.snap_dir] if ctx.snap_dir else []
    bs = find_builders(ctx, base, roots); frozen = True
    if not bs:
        bs = find_builders(ctx, base, ['/workspace/v608build/round2']) if depth > 1 else []; frozen = False
    if not bs: return False
    py, tree, env, outp, k, outs = bs[0]
    allout = {o[1] for o in outs}; prev = max([i for i, _ in outs if i < k], default=-1)
    shared = [st for st in tree.body if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))]
    seg = shared + [st for i, st in enumerate(tree.body) if prev < i <= k and st not in shared]
    if len(outs) > 1: t.sources.append(f'builder makes {len(outs)} images; used its statements {prev + 2}-{k + 1} (top level) for this one')
    segnodes = [x for r in seg for x in ast.walk(r)]
    segnames = {x.id for x in segnodes if isinstance(x, ast.Name)}
    if len(bs) > 1: t.warn.append(f'MULTI-BUILDER {label}: {len(bs)} scripts write {base}; used {rel(py, ctx)} (others: {", ".join(rel(b[0], ctx) for b in bs[1:])})')
    t.sources.append(f'builder {rel(py, ctx)} (writes {rel(outp)})' + ('' if frozen else ' [outside snapshot]'))
    if not frozen: t.warn.append(f'UNFROZEN-SOURCE {label}: builder {rel(py)} is outside the snapshot')
    if os.path.isfile(outp) and os.path.abspath(outp) != os.path.abspath(img) and md5(outp) != md5(img):
        t.warn.append(f'BUILDER-OUTPUT-DIFFERS {label}: {rel(outp)} is now {md5(outp)[:8]}, this copy is {md5(img)[:8]} (builder re-run since; its captions may be newer than this image)')
    if not (os.path.isfile(outp) and md5(outp) == md5(img)):
        fresh(ctx, py, img, t, label, f'{label}: builder {rel(py, ctx)} was edited after this image was made, and its output no longer matches this image', sidecar=False)
    frozen_root = (ctx.snap_dir or '/nonexistent') + os.sep
    for s, ln in text_constants(py, tree, seg): t.captions.append((s, f'{rel(py, ctx)}:{ln}', 'caption'))
    alias = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a_ in n.names: alias[a_.name] = a_.asname or a_.name
    for nm, hp, fr in _local_imports(tree, py, ctx):
        if alias.get(nm, nm) not in segnames and nm != 'sheetkit': continue
        if nm in ('sheetkit',):   # sheetkit draws only its arguments, plus round_totals.for_sheet() as a footer
            continue
        for s, ln in text_constants(hp): t.captions.append((s, f'{rel(hp, ctx)}:{ln}', 'helper text (may be drawn)'))
        t.sources.append(f'helper {rel(hp, ctx)}' + ('' if fr else ' [outside snapshot]'))
    if 'sheet' in segnames and any(nm == 'sheetkit' for nm, _, _ in _local_imports(tree, py, ctx)) and not any(nm == 'round_totals' and alias.get(nm, nm) in segnames for nm, _, _ in _local_imports(tree, py, ctx)):
        rt = os.path.join(ctx.snap_dir or '', 'round_totals.py')
        if os.path.isfile(rt):
            for s, ln in text_constants(rt): t.captions.append((s, f'{rel(rt, ctx)}:{ln}', 'helper text (may be drawn)'))
            t.sources.append(f'helper {rel(rt, ctx)} (sheetkit footer)')
        else: t.unverified.append(f'{label}: sheetkit footer text (round_totals.for_sheet) has no source in the snapshot')
    par = _parents(tree); seen = set(); i = 0; od_dyn = None
    for n in segnodes:
        if isinstance(n, ast.Call) and _fname(n) == 'r2tp' and n.args:
            h = _res(n.args[0], env)
            if h is None:
                od_dyn = next((_res(k_.value, env) for k_ in n.keywords if k_.arg == 'outdir'), None) or '/workspace/v608build/round2/sheets/r2tp/'
                if not isinstance(n.args[0], ast.Name): t.unverified.append(f'{label}: r2tp() input built at run time ({rel(py, ctx)}:{n.lineno}: {ast.unparse(n.args[0])[:60]})')
                continue
            od = next((_res(k.value, env) for k in n.keywords if k.arg == 'outdir'), None) or '/workspace/v608build/round2/sheets/r2tp/'
            cp = r2tp_copy(h, [os.path.join(ctx.snap_dir or '', 'showcase', 'tiles'), od]); src = cp or h
            seen.add(id(n.args[0])); i += 1
            if src not in [x[0] for x in t.html]: trace_render(ctx, src, t, f'{label} / {os.path.basename(src)}', depth, frozen_root)
    for n in segnodes:
        if not isinstance(n, (ast.Constant, ast.BinOp, ast.JoinedStr)) or isinstance(par.get(n), (ast.BinOp, ast.JoinedStr, ast.FormattedValue)) or id(n) in seen: continue
        p = par.get(n)
        if isinstance(p, ast.Call) and _fname(p) == 'r2tp': continue
        consts = [c.value for c in ast.walk(n) if isinstance(c, ast.Constant) and isinstance(c.value, str)]
        if not any(re.search(r'\.(png|jpe?g|html?)$', c) for c in consts): continue
        v = _res(n, env)
        if v is None:
            if isinstance(n, (ast.BinOp, ast.JoinedStr)): t.unverified.append(f'{label}: an input path is built at run time ({rel(py, ctx)}:{n.lineno}: {ast.unparse(n)[:70]})')
            continue
        if not v.startswith('/') or os.path.basename(v) == base or v in allout: continue
        if isinstance(p, ast.Call) and _fname(p) == 'save': continue
        if od_dyn and v.lower().endswith(HTML_EXT):   # this part of the builder sends html through r2tp(): use its sheet copy when r2tp made one
            v = r2tp_copy(v, [od_dyn]) or v
        if v not in [x[0] for x in t.html]: trace_render(ctx, v, t, f'{label} / {os.path.basename(v)}', depth, frozen_root)
    return True

# --- the showcase tour (tour.py: SHEETS -> showcase-<key>.png, tiles through r2tp(outdir=TL))
def trace_tour(ctx, img, tour, t, label):
    tree = ast.parse(open(tour, encoding='utf-8').read()); env = _env(tree)
    key = re.match(r'showcase-(.+)\.png$', os.path.basename(img)).group(1)
    sheets = next((n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'SHEETS' for x in n.targets)), None)
    if sheets is None: return False
    t.sources.append(f'tour {rel(tour, ctx)} (SHEETS)')
    frozen_root = (ctx.snap_dir or '/nonexistent') + os.sep; tiles_frozen = os.path.join(os.path.dirname(tour), 'tiles'); hit = False; num = 0
    made = os.path.getmtime(img); o = os.path.join(env.get('O', ''), os.path.basename(img))
    if env.get('O') and os.path.isfile(o) and md5(o) == md5(img): made = min(made, os.path.getmtime(o))
    for sh in sheets.elts:
        k, title, tl = sh.elts; k = _res(k, env); title_s = _res(title, env)
        tiles = []
        for tile in tl.elts:
            n_, cap, h, wh = tile.elts; n_ = _res(n_, env)
            if not n_.endswith('s'): num += 1
            tiles.append((f'{num}s' if n_.endswith('s') else str(num), _res(cap, env), _res(h, env), env.get(wh.id) if isinstance(wh, ast.Name) else None))
        if k != key: continue
        hit = True
        t.captions.append((f"Nancy's eyes, sheet {k[0]}: {title_s}", f'{rel(tour, ctx)} sheet title', 'caption'))
        for tn, cap, h, wh in tiles:
            lab = f'{label} tile {tn}'
            if cap: t.captions.append((cap, f'{rel(tour, ctx)} tile {tn} caption', 'caption'))
            if h is None: t.unverified.append(f'{lab}: html path not resolvable in tour.py'); continue
            wh = wh or wh_from_name(h)
            cp = r2tp_copy(h, [tiles_frozen, env.get('TL')])
            if cp: src = cp
            else: src = h
            pngp = (cp[:-5] + '.png') if cp else h.replace('/html/', '/png/')[:-5] + '.png'
            if not os.path.isfile(src): t.unverified.append(f'{lab}: source {rel(src)} not found'); continue
            if os.path.isfile(pngp):
                fresh(ctx, src, pngp, t, lab, f'{lab}: {rel(src)} was edited after its render {rel(pngp)}, so the tile may show other text')
            if os.path.getmtime(src) > made + MTIME_SLACK and not src.startswith(frozen_root):
                t.unverified.append(f'{lab}: {rel(src)} changed after this sheet was made, so it may not be what the sheet shows')
            t.add_html(src, tuple(wh), lab, src.startswith(frozen_root))
    for n in ast.walk(tree):   # the fixed question and footer of the sheet() call
        if isinstance(n, ast.Call) and _fname(n) == 'sheet':
            for a in n.args[2:3] + n.args[4:5]:
                v = _res(a, env)
                if v: t.captions.append((v, f'{rel(tour, ctx)}:{n.lineno} sheet() text', 'caption'))
                elif not isinstance(a, ast.Name): t.unverified.append(f'{label}: sheet() text built at run time ({rel(tour, ctx)}:{n.lineno})')
    rt = os.path.join(ctx.snap_dir or '', 'round_totals.py')
    if os.path.isfile(rt):
        for s, ln in text_constants(rt): t.captions.append((s, f'{rel(rt, ctx)}:{ln}', 'helper text (may be drawn)'))
        t.sources.append(f'helper {rel(rt, ctx)} (sheetkit footer)')
    if not hit: t.unverified.append(f'{label}: tour.py has no sheet "{key}"'); return True
    return True

def trace_image(ctx, img):
    t = Trace(); real = os.path.abspath(img); label = os.path.basename(img)
    if not (ctx.snap_dir and real.startswith(ctx.snap_dir + os.sep)):
        locs = [l for l in ctx.man.get(md5(img), []) if l]
        if locs and ctx.snap_dir: real = os.path.join(ctx.snap_dir, locs[0]); t.sources.append(f'attachment = snapshot {locs[0]} (by md5)')
    frozen_root = (ctx.snap_dir or '/nonexistent') + os.sep
    if trace_sidecar(ctx, real, t, label, 0, frozen_root): return t
    tour = os.path.join(os.path.dirname(real), 'tour.py')
    if re.match(r'showcase-.+\.png$', os.path.basename(real)) and os.path.isfile(tour) and trace_tour(ctx, real, tour, t, label): return t
    hs = [h for h in png_to_html(real)]
    if hs:
        h = hs[0]
        fresh(ctx, h, real, t, label, f'{label}: {rel(h, ctx)} was edited after this render, so the image may show other text')
        t.add_html(h, wh_from_name(h), label, h.startswith(frozen_root) or not ctx.snap_dir); return t
    if trace_builder(ctx, real, t, label, 1): return t
    t.unverified.append(f'{label}: no sidecar .sources.txt, same-name .html, tour entry or builder script found in {ctx.snap or "the snapshot"}')
    return t

# ---------------------------------------------------------------- per-file check
def check_full(path, ctx=None):
    ctx = ctx or context(); r = {'block': [], 'warn': list(), 'sources': [], 'allowed': [], 'status': 'PASS', 'thai_measured': 0}
    if ctx.fatal: r['block'].append(f'TEXT UNVERIFIED: {ctx.fatal}'); r['status'] = 'TEXT UNVERIFIED'; return r
    if not os.path.isfile(path): r['block'].append(f'TEXT UNVERIFIED: {path} not found'); r['status'] = 'TEXT UNVERIFIED'; return r
    low = path.lower()
    if is_image(path):
        t = trace_image(ctx, path); r['sources'] = t.sources; r['warn'] += t.warn
        if t.unfrozen: r['warn'].append(f'UNFROZEN-SOURCE {len(t.unfrozen)} of {len(t.html)} render sources are outside the snapshot (marked [outside snapshot] above); they are checked as they are now, guarded only by the edited-after-render time check')
        for u in t.unverified: r['block'].append(f'TEXT UNVERIFIED {u}')
        htmls = t.html
        cret, cfail, ok = scan(ctx, [(k, s) for s, w, k in t.captions], 'caption')
        # captions carry their own place: rescan per caption for a precise location
        for s, where, kind in t.captions:
            rr, ff, oo = scan(ctx, [(kind, norm(s))], where); r['allowed'] += oo
            r['block'] += [fmt_hit('RETIRED', h) for h in rr]
            r['block'] += [fmt_hit('NEVER-WORD', h) for h in ff if is_never(h[0])]
            r['warn'] += ['CAPTION-MENTION ' + fmt_hit('FAIL-WORD', h) + ' (sheet caption, not game UI)' for h in ff if not is_never(h[0])]
            if THAI.search(s): r['warn'].append(f'THAI SIZE UNMEASURED caption at {where}: "{s[:40]}" (drawn by the sheet builder, not app UI; no DOM to measure)')
        if not t.html and not t.captions and not t.unverified: r['block'].append(f'TEXT UNVERIFIED {os.path.basename(path)}: traced, but no text source at all')
    elif low.endswith(HTML_EXT + ('.svg',)):
        htmls = [(path, wh_from_name(path), os.path.basename(path))]; r['sources'] = [f'html {rel(path, ctx)}']
    elif low.endswith(DOC_EXT):
        lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
        for i, l in enumerate(lines, 1):
            rr, ff, oo = scan(ctx, [('line', norm(l))], f'{os.path.basename(path)}:{i}'); r['allowed'] += oo
            r['warn'] += ['DOC-MENTION ' + fmt_hit('RETIRED', h) for h in rr] + ['DOC-MENTION ' + fmt_hit('NEVER-WORD' if is_never(h[0]) else 'FAIL-WORD', h) for h in ff]
        r['sources'] = [f'doc {rel(path, ctx)} (council notes: mentions warn, never block)']; htmls = []
    elif low.endswith(CODE_EXT):
        r['status'] = 'SKIP'; r['warn'].append(f'SKIP {os.path.basename(path)}: code file, not something Maxwell sees'); return r
    elif low.endswith(HASH_EXT):   # MANIFEST.md5 / renders-MANIFEST.md5 / *.sha256: checksum lists the tool itself reads, not something Maxwell sees
        r['status'] = 'SKIP'; r['warn'].append(f'SKIP {os.path.basename(path)}: checksum list, not something Maxwell sees'); return r
    else:   # bmp/tiff/pdf/heic/video/anything unknown: its text can't be read, so it can't pass
        r['block'].append(f'TEXT UNVERIFIED {os.path.basename(path)}: file type not readable by text-check (not png/jpg/webp/gif, html, svg or a text doc)'); r['status'] = 'TEXT UNVERIFIED'; return r
    for h, wh, lab in htmls:
        segs = html_segments(h); rr, ff, oo = scan(ctx, segs, f'{lab} source {rel(h, ctx)}'); r['allowed'] += oo
        wk = lambda x: x[4].endswith('(warn)')   # data-* attributes and script string literals: maybe visible, maybe code keys -> warn
        r['block'] += [fmt_hit('RETIRED', x) for x in rr if not wk(x)] + [fmt_hit('NEVER-WORD' if is_never(x[0]) else 'FAIL-WORD', x) for x in ff if not wk(x) or is_never(x[0])]
        r['warn'] += ['MAYBE-VISIBLE ' + fmt_hit('RETIRED', x) for x in rr if wk(x)] + ['MAYBE-VISIBLE ' + fmt_hit('FAIL-WORD', x) for x in ff if wk(x) and not is_never(x[0])]
        if any(THAI.search(s) for _, s in segs):
            m = thai_sizes(ctx, h, *wh)
            if m is None: r['warn'].append(f'THAI SIZE UNMEASURED {lab}: {rel(h, ctx)} ({"no headless Chrome on this box" if not CHROME else "Chrome gave no measurement"})')
            else:
                r['thai_measured'] += 1
                for txt, css, eff, vis in m:
                    if not vis: continue
                    if css < ctx.min_px - 0.01: r['block'].append(f'THAI<17 {lab}: "{txt}" is {css:g} px at {wh[0]}x{wh[1]} ({rel(h, ctx)})')
                    elif eff < ctx.min_px - 0.05: r['warn'].append(f'THAI SCALED<17 {lab}: "{txt}" is {css:g} px CSS but {eff:g} px after a transform scale at {wh[0]}x{wh[1]} ({rel(h, ctx)})')
                if not any(v for *_, v in m): r['warn'].append(f'THAI SIZE UNMEASURED {lab}: Thai is only in hidden elements of {rel(h, ctx)}')
    r['warn'] = list(dict.fromkeys(r['warn'])); r['block'] = list(dict.fromkeys(r['block']))
    if r['block']: r['status'] = 'TEXT UNVERIFIED' if all(b.startswith('TEXT UNVERIFIED') for b in r['block']) else 'BLOCK'
    return r

def check(path):
    """blocking problems for one attachment ([] = clear); mirrors ground_check.check(path)"""
    return check_full(path)['block']

# ---------------------------------------------------------------- CLI
def expand(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for d, ds, fs in os.walk(p):
                ds[:] = sorted(x for x in ds if x != '__pycache__')
                out += [os.path.join(d, f) for f in sorted(fs)]
        else: out.append(p)
    return out
def run(paths, ctx, out=print):
    out(ctx.stamp())
    for n in ctx.notes: out(f'note {n}')
    for w in ctx.warn: out(f'WARN {w}')
    files = expand(paths)
    if not files: out('ERROR nothing to check'); return 2
    cnt = {}; nb = nw = 0
    for f in files:
        r = check_full(f, ctx); st = r['status']; cnt[st] = cnt.get(st, 0) + 1
        out(f'{st:<15} {rel(f, ctx)}  ({len(r["block"])} problems, {len(r["warn"])} warnings, Thai pages measured {r["thai_measured"]})')
        for s in r['sources']: out(f'    source  {s}')
        for b in r['block']: out(f'    BLOCK   {b}')
        for w in r['warn']: out(f'    WARN    {w}')
        for a in r['allowed'][:6]: out(f'    allowed {a}')
        nb += len(r['block']); nw += len(r['warn'])
    bad = cnt.get('BLOCK', 0) + cnt.get('TEXT UNVERIFIED', 0)
    out(f'RESULT {"BLOCK" if bad else "CLEAR"}: {len(files)} files, ' + ', '.join(f'{v} {k}' for k, v in sorted(cnt.items())) + f'; {nb} problems, {nw} warnings')
    return 1 if bad else 0

# ---------------------------------------------------------------- selftest (planted faults)
def selftest():
    base = os.path.join(HERE, 'runs'); os.makedirs(base, exist_ok=True); d = tempfile.mkdtemp(prefix='selftest-', dir=base)
    try:
        b = os.path.join(d, 'v608build'); snap = os.path.join(b, 'snap-t'); os.makedirs(os.path.join(snap, 'sheets')); os.makedirs(os.path.join(snap, 'showcase'))
        os.makedirs(os.path.join(snap, 'code')); os.makedirs(os.path.join(b, 'r2h-build')); rend = os.path.join(d, 'renders'); os.makedirs(os.path.join(rend, 'html')); os.makedirs(os.path.join(rend, 'png'))
        data = {"version": "t", "wrongText": {"en": "Now you know it", "th": "ตอนนี้รู้แล้วนะ"},
                "uiText": {"tapPrompt": {"en": "Can you find the {word}?", "th": "หา {word} เจอไหม"}, "pantry": {"en": "Shop", "th": "ร้านดาวทอง"}},
                "cards": [{"id": "bh-24", "en": "Where is the bathroom?", "th": "ห้องน้ำอยู่ที่ไหนคะ"}, {"id": "cs-22", "en": "long", "choices": [{"en": "wrong"}]}]}
        paste = os.path.join(b, 'r2h-build', 'p.md'); open(paste, 'w', encoding='utf-8').write('# spec prose: no fail wording, no lives, no timers; wrong taps are graced\n' + json.dumps(data, ensure_ascii=False) + '\n')
        open(os.path.join(snap, 'MANIFEST.md5'), 'w').write('')
        ptr = os.path.join(b, 'CURRENT-SNAP.txt'); open(ptr, 'w').write(f'snap=snap-t\nmanifest_md5=x\npaste_1b_md5={md5(paste)}\npaste_1b_path=r2h-build/p.md\n')
        page = lambda body, px=18: f"<html><head><style>body{{margin:0;width:390px}} .th{{font-size:{px}px;line-height:1.7}}</style></head><body>{body}</body></html>"
        def pair(name, body, px=18, where=None):
            where = where or os.path.join(snap, 'showcase'); h = os.path.join(where, name + '.html'); p = os.path.join(where, name + '.png')
            open(p, 'wb').write(b'\x89PNG\r\n\x1a\n' + name.encode()); time_ = os.path.getmtime(p); open(h, 'w', encoding='utf-8').write(page(body, px)); os.utime(h, (time_, time_)); return p, h
        clean, _ = pair('clean', '<div>Can you find the kite?</div><div class="th">หา kite เจอไหม</div><div>Now you know it</div><button>Shop</button>')
        retired, _ = pair('retired', '<div>Where is the kite?</div><div class="th">kite อยู่ที่ไหน</div>')
        fail_en, _ = pair('fail-en', '<div>Game over! Try again?</div>')
        fail_th, _ = pair('fail-th', '<div class="th">ผิด ลองใหม่</div>')
        thai15, _ = pair('thai15', '<div class="th">หา kite เจอไหม</div>', px=15)
        legit, _ = pair('legit', '<div>Where is the bathroom?</div><div class="th">ห้องน้ำอยู่ที่ไหนคะ</div><button>wrong</button>')
        listen, _ = pair('listen', '<div>Listen. Where is it?</div><div class="th">ฟังแล้วหาดู</div><div>Spell it.</div><div class="th">สะกดคำนี้</div>')   # current listenFind/spellIt (QM 12:59 AM MT)
        pantry, _ = pair('pantry', '<h1>GOLDEN PANTRY</h1><div class="th">ตู้กับข้าวทองคำ</div>')
        orphan = os.path.join(snap, 'sheets', 'orphan.png'); open(orphan, 'wb').write(b'\x89PNG\r\n\x1a\norphan')
        rp, rh = pair('r1', '<div>Where is the kite?</div>', where=os.path.join(rend, 'png'))   # a render whose html sits in ../html/
        shutil.move(rh, os.path.join(rend, 'html', 'r1.html')); os.utime(os.path.join(rend, 'html', 'r1.html'), (os.path.getmtime(rp),) * 2)
        sheetp = os.path.join(snap, 'sheets', 'built.png'); open(sheetp, 'wb').write(b'\x89PNG\r\n\x1a\nbuilt')
        open(os.path.join(snap, 'code', 'mk.py'), 'w').write(f"R = {json.dumps(rend + '/png/')}\nfrom PIL import Image\nS = Image.new('RGB', (9, 9))\nd = None\n# d.text((0, 0), 'Pick one: the golden pantry tile')\ncap = 'Option A shows the shop'\nim = Image.open(R + 'r1.png')\nS.save({json.dumps('/nonexistent/' + 'built.png')})\n")
        os.utime(os.path.join(snap, 'code', 'mk.py'), (os.path.getmtime(sheetp) - 60,) * 2)
        capsheet = os.path.join(snap, 'sheets', 'capsheet.png'); open(capsheet, 'wb').write(b'\x89PNG\r\n\x1a\ncap')
        open(os.path.join(snap, 'code', 'mk2.py'), 'w').write(f"from PIL import Image\nS = Image.new('RGB', (9, 9))\ncap = 'Tile 25: The golden pantry.'\nS.save({json.dumps('/nonexistent/capsheet.png')})\n")
        os.utime(os.path.join(snap, 'code', 'mk2.py'), (os.path.getmtime(capsheet) - 60,) * 2)
        capnv = os.path.join(snap, 'sheets', 'capnv.png'); open(capnv, 'wb').write(b'\x89PNG\r\n\x1a\ncapnv')
        open(os.path.join(snap, 'code', 'mk5.py'), 'w').write(f"from PIL import Image\nS = Image.new('RGB', (9, 9))\ncap = 'Tile 9: Call Max'\nS.save({json.dumps('/nonexistent/capnv.png')})\n")
        os.utime(os.path.join(snap, 'code', 'mk5.py'), (os.path.getmtime(capnv) - 60,) * 2)
        dyn = os.path.join(snap, 'sheets', 'dyn.png'); open(dyn, 'wb').write(b'\x89PNG\r\n\x1a\ndyn')
        open(os.path.join(snap, 'code', 'mk3.py'), 'w').write(f"from PIL import Image\nR = '/x/'\nS = Image.new('RGB', (9, 9))\nfor r in ['a', 'b']: S.paste(Image.open(R + r + '.png'))\nS.save({json.dumps('/nonexistent/dyn.png')})\n")
        os.utime(os.path.join(snap, 'code', 'mk3.py'), (os.path.getmtime(dyn) - 60,) * 2)
        two_a = os.path.join(snap, 'sheets', 'two-a.png'); two_b = os.path.join(snap, 'sheets', 'two-b.png')
        for x in (two_a, two_b): open(x, 'wb').write(b'\x89PNG\r\n\x1a\n' + x.encode())
        open(os.path.join(snap, 'code', 'mk4.py'), 'w').write("from PIL import Image\nS = Image.new('RGB', (9, 9))\ncap = 'Back after a pause'\nS.save('/nonexistent/two-a.png')\nT = Image.new('RGB', (9, 9))\ncap2 = 'Game over screen'\nT.save('/nonexistent/two-b.png')\n")
        os.utime(os.path.join(snap, 'code', 'mk4.py'), (os.path.getmtime(two_a) - 60,) * 2)
        sc = os.path.join(snap, 'sheets', 'side.png'); open(sc, 'wb').write(b'\x89PNG\r\n\x1a\nside')
        open(sc[:-4] + '.sources.txt', 'w').write(f'{md5(clean)}  {clean}\n{"0" * 32}  {retired}\n')   # second source drifted
        doc = os.path.join(snap, 'sheets', 'notes.md'); open(doc, 'w').write('We checked that "Where is the kite?" is gone.\n')
        ctx = Ctx(ptr)
        st = lambda p: check_full(p, ctx)
        res = {k: st(p) for k, p in [('clean', clean), ('retired', retired), ('fail-en', fail_en), ('fail-th', fail_th), ('thai15', thai15), ('legit', legit), ('listen', listen), ('pantry', pantry),
                                      ('orphan', orphan), ('builder', sheetp), ('caption', capsheet), ('capnv', capnv), ('dynamic', dyn), ('sidecar', sc), ('doc', doc), ('two-a', two_a), ('two-b', two_b)]}
        has = lambda k, tag: any(x.startswith(tag) for x in res[k]['block'])
        cases = [('clean passes (Thai 18 px measured)', res['clean']['status'] == 'PASS' and res['clean']['thai_measured'] == 1),
                 ('retired EN "Where is the kite?"', any('R1-ask-en' in x for x in res['retired']['block'])),
                 ('retired TH "อยู่ที่ไหน"', any('R2-ask-th' in x for x in res['retired']['block'])),
                 ('fail word EN (game over, try again)', sum('FAIL-WORD' in x for x in res['fail-en']['block']) == 2),
                 ('fail word TH (ผิด)', any('F-th-wrong' in x for x in res['fail-th']['block'])),
                 ('Thai at 15 px', has('thai15', 'THAI<17')),
                 ('untraceable image', res['orphan']['status'] == 'TEXT UNVERIFIED'),
                 ('legit card sentences + choice not flagged', res['legit']['status'] == 'PASS' and len(res['legit']['allowed']) >= 3),
                 ('current listenFind "Listen. Where is it?" + spellIt not flagged', res['listen']['status'] == 'PASS' and not res['listen']['block']),
                 ('Golden Pantry EN + TH', sum(('R3-shop-en' in x or 'R4-shop-th' in x) for x in res['pantry']['block']) == 2),
                 ('builder -> png/ -> html/ retired ask', any('R1-ask-en' in x for x in res['builder']['block']) and not any('golden pantry' in x.lower() for x in res['builder']['block'])),
                 ('builder caption retired', any('R3-shop-en' in x and 'mk2.py' in x for x in res['caption']['block'])),
                 ('never-word in a builder caption BLOCKs (Call Max)', has('capnv', 'NEVER-WORD F-callmax')),
                 ('dynamic builder path = UNVERIFIED', has('dynamic', 'TEXT UNVERIFIED')),
                 ('sidecar drift = UNVERIFIED', has('sidecar', 'TEXT UNVERIFIED') and not any('R1' in x for x in res['sidecar']['block'])),
                 ('two-image builder: each image gets only its own part', res['two-a']['status'] == 'PASS' and any('CAPTION-MENTION' in w and 'Game over' in w for w in res['two-b']['warn']) and not any('Game over' in w for w in res['two-a']['warn'])),
                 ('doc mention warns, never blocks', res['doc']['status'] == 'PASS' and any('DOC-MENTION' in w for w in res['doc']['warn'])),
                 ('live list check (tapPrompt/Shop) clean', not ctx.warn and len(ctx.notes) == 3)]
        bad_ptr = os.path.join(b, 'bad.txt'); open(bad_ptr, 'w').write(f'snap=snap-t\npaste_1b_md5={"0" * 32}\npaste_1b_path=r2h-build/p.md\n')
        cases.append(('pointer paste md5 mismatch = UNVERIFIED', Ctx(bad_ptr).fatal is not None and check_full(clean, Ctx(bad_ptr))['status'] == 'TEXT UNVERIFIED'))
        stale = os.path.join(d, 'w.json'); w = json.load(open(DATA, encoding='utf-8')); w['retired'].append({"id": "RX", "lang": "en", "regex": "Can you find", "now_path": "uiText.tapPrompt.en", "decision": "test"}); json.dump(w, open(stale, 'w'))
        cases.append(('retired entry that is live = STALE-LIST warning', any('STALE-LIST RX' in x for x in Ctx(ptr, data=stale).warn)))
        cli = lambda *a: subprocess.run([sys.executable, os.path.abspath(__file__), *a], env=dict(os.environ, CURRENT_SNAP=ptr), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        cases += [('cli clean = 0', cli(clean) == 0), ('cli planted = 1', cli(retired) == 1), ('cli folder with faults = 1', cli(os.path.join(snap, 'showcase')) == 1), ('cli missing = 1', cli(os.path.join(d, 'nope.png')) == 1),
                  ('cli abbreviation rejected = 2', cli('--sel') == 2)]
        # --- freeze copies (Watchman, Nov 1): plain cp refreshes mtimes, so an html copied after its png looks newer than its render
        src = os.path.join(d, 'stage'); os.makedirs(os.path.join(src, 'png')); os.makedirs(os.path.join(src, 'html'))
        T0 = os.path.getmtime(clean) - 3600; body = '<div>Can you find the kite?</div><div class="th">หา kite เจอไหม</div>'
        def staged(name, edit=False):   # a clean render pair in the stage: png and html written in the same second (html edited 10 min later if edit)
            p_ = os.path.join(src, 'png', name + '.png'); h_ = os.path.join(src, 'html', name + '.html')
            open(p_, 'wb').write(b'\x89PNG\r\n\x1a\n' + name.encode()); open(h_, 'w', encoding='utf-8').write(page(body)); os.utime(p_, (T0,) * 2); os.utime(h_, (T0 + (600 if edit else 0),) * 2)
            return p_, h_
        def freeze(name, files, preserve, gap=30.0, man=True):   # copy into a new snapshot: png first, html `gap` s later (a slow plain cp), then MANIFEST
            sd = os.path.join(b, name); os.makedirs(os.path.join(sd, 'showcase'))
            t_ = T0 + 7200; lines = []
            for i, (p_, h_, extra) in enumerate(files):
                for k_, f_ in enumerate((p_, h_)):
                    dst = os.path.join(sd, 'showcase', os.path.basename(f_)); (shutil.copy2 if preserve else shutil.copy)(f_, dst)
                    if not preserve: os.utime(dst, (t_ + i + k_ * gap,) * 2)
                    lines.append(f'{md5(dst)}  ./showcase/{os.path.basename(dst)}')
                if extra: extra(os.path.join(sd, 'showcase'))
            mf = os.path.join(sd, 'MANIFEST.md5'); open(mf, 'w').write('\n'.join(lines if man else []) + '\n')
            if not preserve: os.utime(mf, (t_ + len(files) + gap + 1,) * 2)
            pp = os.path.join(b, name + '.txt'); open(pp, 'w').write(f'snap={name}\nmanifest_md5={md5(mf)}\npaste_1b_md5={md5(paste)}\npaste_1b_path=r2h-build/p.md\n'); return Ctx(pp), sd
        def side(key, good=True, nest=False):   # QM renderer sidecar next to the png, recording the source html hash
            def f(dir_):
                nm = [x for x in os.listdir(dir_) if x.endswith('.png')][-1]; h_ = os.path.join(dir_, nm[:-4] + '.html')
                v = md5(h_) if good else '0' * 32
                js = {"vw": 390, "vh": 844, "html": nm[:-4] + '.html', "png": nm, "html_md5_src": "render", "png_md5": md5(os.path.join(dir_, nm)), **({"source": {"md5": v}} if nest else {key: v})}
                json.dump(js, open(os.path.join(dir_, nm[:-4] + '.json'), 'w'))
            return f
        pa = staged('fa'); pb = staged('fb'); pcx = staged('fc', edit=True); pd = staged('fd'); pe = staged('fe'); pf = staged('ff'); pg = staged('fg', edit=True)
        ca, sa = freeze('snap-ca', [(*pa, side('html_md5'))], False, man=False)                    # (a) plain cp + sidecar md5 match, no manifest md5
        cb, sb = freeze('snap-cb', [(*pb, None)], False, man=False)                                # (b) plain cp, no sidecar, no manifest md5
        cc, sc_ = freeze('snap-cc', [(*pcx, side('source_md5', good=False))], False, man=False)    # (c) sidecar md5 mismatch (real edit)
        cd, sd_ = freeze('snap-cd', [(*pd, None)], True)                                           # (d) cp -p / copy2: preserved mtimes
        ce, se = freeze('snap-ce', [(*pe, None)], False)                                           # (e) plain cp, no sidecar, manifest md5 matches
        cf, sf = freeze('snap-cf', [(*pf, side('x', nest=True))], False, man=False)               # (f) nested source.md5 sidecar key
        cg, sg = freeze('snap-cg', [(*pg, None)], True)                                            # (g) cp -p keeps a real edit-after-render
        rr_ = lambda c, sdir, n: check_full(os.path.join(sdir, 'showcase', n + '.png'), c)
        ra, rb, rc, rd, re_, rf, rg = rr_(ca, sa, 'fa'), rr_(cb, sb, 'fb'), rr_(cc, sc_, 'fc'), rr_(cd, sd_, 'fd'), rr_(ce, se, 'fe'), rr_(cf, sf, 'ff'), rr_(cg, sg, 'fg')
        hd = os.path.join(se, 'showcase', 'fe.html'); os.chmod(hd, 0o644); open(hd, 'a').write('<div>Game over</div>'); os.utime(hd, (os.path.getmtime(os.path.join(se, 'showcase', 'fe.png')) + 30,) * 2)
        rh = check_full(os.path.join(se, 'showcase', 'fe.png'), Ctx(os.path.join(b, 'snap-ce.txt')))   # (h) burst times but the html no longer matches the MANIFEST
        real = {"vw": 390, "vh": 844, "snap": "pointer x", "paste_md5": "0" * 32, "html": "fb.html", "png": "fb.png", "el": []}
        json.dump(real, open(os.path.join(sb, 'showcase', 'fb.json'), 'w')); ri = check_full(os.path.join(sb, 'showcase', 'fb.png'), Ctx(os.path.join(b, 'snap-cb.txt')))   # (i) today's real sidecar shape
        # --- merged sidecar-trust plants (Instructor's (j)-(m) re-keyed to html_md5_src/png_md5; (k2), (n), (o) Auditor): only src=render + matching png_md5 is VERIFIED
        sj = lambda p_, **kw: json.dump({"vw": 390, "vh": 844, "html": os.path.basename(p_[1]), "png": os.path.basename(p_[0]), **kw}, open(p_[0][:-4] + '.json', 'w'))
        pj = staged('fj', edit=True); sj(pj, html_md5=md5(pj[1])); rj = check_full(pj[0], ctx)                                              # (j) edit after render, today's hash written later, no src
        pj2 = staged('fj2', edit=True); sj(pj2, html_md5=md5(pj2[1]), html_md5_src='backfill', png_md5=md5(pj2[0])); rj2 = check_full(pj2[0], ctx)   # (j2) same, src=backfill + true png_md5
        pk = staged('fk'); _, sk = freeze('snap-ck', [(*pk, None)], True); hk = os.path.join(sk, 'showcase', 'fk.html'); pkp = os.path.join(sk, 'showcase', 'fk.png')
        open(hk, 'a', encoding='utf-8').write('<div>Can you find the kitten?</div>'); sj((pkp, hk), html_md5=md5(hk))
        os.utime(pkp[:-4] + '.json', (os.path.getmtime(pkp),) * 2); os.utime(hk, (os.path.getmtime(pkp),) * 2)                                 # (k) render-looking times, pointer-named MANIFEST disagrees
        rk = check_full(pkp, Ctx(os.path.join(b, 'snap-ck.txt')))
        pk2 = staged('fk2'); _, sk2 = freeze('snap-ck2', [(*pk2, None)], True); hk2 = os.path.join(sk2, 'showcase', 'fk2.html'); pk2p = os.path.join(sk2, 'showcase', 'fk2.png')
        old_ = md5(hk2); open(hk2, 'a', encoding='utf-8').write('<div>Can you find the kitten?</div>'); sj((pk2p, hk2), html_md5=md5(hk2)); os.utime(hk2, (os.path.getmtime(pk2p) + 600,) * 2)
        mf2 = os.path.join(sk2, 'MANIFEST.md5'); mt_ = open(mf2).read(); assert old_ in mt_; open(mf2, 'w').write(mt_.replace(old_, md5(hk2)))                               # (k2) MANIFEST rewritten to the edited md5; pointer still names the old one
        rk2 = check_full(pk2p, Ctx(os.path.join(b, 'snap-ck2.txt')))
        pl = staged('fl'); sj(pl, html_md5=md5(pl[1]), html_md5_src='render', png_md5=md5(pl[0])); os.utime(pl[1], (T0 + 30,) * 2); rl = check_full(pl[0], ctx)   # (l) real render-time sidecar, html touched later
        pl2 = staged('fl2'); sj(pl2, html_md5=md5(pl2[1]), html_md5_src='render', png_md5='1' * 32); rl2 = check_full(pl2[0], ctx)                             # (l2) src=render, png_md5 mismatch
        pm_ = staged('fm'); sj(pm_, html_md5=md5(pm_[1]), html_md5_backfill=True, html_md5_src='render', png_md5=md5(pm_[0])); os.utime(pm_[1], (T0 + 30,) * 2); rm_ = check_full(pm_[0], ctx)   # (m) backfill flag outranks src
        pn = staged('fn'); _, sn = freeze('snap-cn', [(*pn, None)], True); hn_ = os.path.join(sn, 'showcase', 'fn.html'); pnp = os.path.join(sn, 'showcase', 'fn.png')
        sj((pnp, hn_), html_md5=md5(hn_)); os.utime(hn_, (os.path.getmtime(pnp) + 600,) * 2); rn = check_full(pnp, Ctx(os.path.join(b, 'snap-cn.txt')))   # (n) no src, html newer, bytes = pointer-named MANIFEST
        pn2 = staged('fn2'); _, sn2 = freeze('snap-cn2', [(*pn2, None)], True); hn2 = os.path.join(sn2, 'showcase', 'fn2.html'); pn2p = os.path.join(sn2, 'showcase', 'fn2.png')
        sj((pn2p, hn2), html_md5=md5(hn2)); rn2 = check_full(pn2p, Ctx(os.path.join(b, 'snap-cn2.txt')))                                   # (n2) no src, cp -p, untouched, = MANIFEST
        fo = os.path.join(d, 'fill'); os.makedirs(os.path.join(fo, 'renders')); os.makedirs(os.path.join(fo, 'html'))
        po = os.path.join(fo, 'renders', 'fo.png'); ho = os.path.join(fo, 'html', 'fo.html'); open(po, 'wb').write(b'\x89PNG\r\n\x1a\nfo'); open(ho, 'w', encoding='utf-8').write(page(body)); os.utime(po, (T0,) * 2); os.utime(ho, (T0,) * 2)
        ro = check_full(po, ctx)                                                                                                             # (o) scene-fill layout renders/ + ../html/
        vb = lambda r: any('VERIFIED by hash' in x for x in r['sources'])
        cases += [('freeze (a) plain cp, html copied after png + sidecar html_md5 match = PASS', ra['status'] == 'PASS' and vb(ra)),
                  ('freeze (b) plain cp, no sidecar, no MANIFEST md5 = UNVERIFIED', rb['status'] == 'TEXT UNVERIFIED' and any('no md5' in x for x in rb['block'])),
                  ('freeze (c) sidecar md5 mismatch (real edit) = UNVERIFIED/BLOCK', rc['status'] == 'TEXT UNVERIFIED' and any('recorded source_md5' in x for x in rc['block'])),
                  ('freeze (d) cp -p preserved mtimes = PASS', rd['status'] == 'PASS' and not rd['warn'] and cd.copy_window() is None),
                  ('freeze (e) plain cp, no sidecar, MANIFEST md5 match = PASS + COPY-BURST warning', re_['status'] == 'PASS' and any(w.startswith('COPY-BURST') for w in re_['warn'])),
                  ('freeze (f) nested sidecar source.md5 = PASS', rf['status'] == 'PASS' and vb(rf)),
                  ('freeze (g) cp -p keeps a real edit-after-render = UNVERIFIED', rg['status'] == 'TEXT UNVERIFIED' and any('edited after' in x for x in rg['block'])),
                  ('freeze (h) copy-pass times but html != MANIFEST = BLOCK', rh['status'] == 'BLOCK' and any('no longer matches the MANIFEST' in x for x in rh['block'])),
                  ('freeze (i) real sidecar without a hash falls back to time check = UNVERIFIED', ri['status'] == 'TEXT UNVERIFIED' and any('has no source hash' in x for x in ri['sources'])),
                  ('trust (j) edit after render + today\'s hash written later, no src = UNVERIFIED, not VERIFIED', rj['status'] == 'TEXT UNVERIFIED' and not vb(rj)),
                  ('trust (j2) same, html_md5_src=backfill + true png_md5 = UNVERIFIED, not VERIFIED', rj2['status'] == 'TEXT UNVERIFIED' and not vb(rj2)),
                  ('trust (k) sidecar hash = today\'s html, pointer-named MANIFEST disagrees = UNVERIFIED', rk['status'] == 'TEXT UNVERIFIED' and not vb(rk) and any('recorded' in x and 'MANIFEST' in x for x in rk['block'])),
                  ('trust (k2) MANIFEST rewritten to the edited md5 (pointer names the old one) = not used, UNVERIFIED', rk2['status'] == 'TEXT UNVERIFIED' and not vb(rk2) and any(w.startswith('MANIFEST-NOT-POINTER') for w in rk2['warn'])),
                  ('trust (l) real render-time sidecar (src=render, png_md5 match), html touched later = PASS, VERIFIED', rl['status'] == 'PASS' and vb(rl)),
                  ('trust (l2) src=render but png_md5 mismatch = UNVERIFIED, not VERIFIED', rl2['status'] == 'TEXT UNVERIFIED' and not vb(rl2)),
                  ('trust (m) html_md5_backfill: true outranks src=render = not VERIFIED, time check UNVERIFIED', rm_['status'] == 'TEXT UNVERIFIED' and not vb(rm_)),
                  ('trust (n) no src, html newer than png, bytes = pointer-named MANIFEST = still UNVERIFIED (MANIFEST proves since-freeze only)', rn['status'] == 'TEXT UNVERIFIED' and not vb(rn) and any('unchanged since the freeze' in x for x in rn['sources'])),
                  ('trust (n2) no src, cp -p snapshot, untouched, = pointer-named MANIFEST = PASS, not VERIFIED', rn2['status'] == 'PASS' and not vb(rn2) and any('unchanged since the freeze' in x for x in rn2['sources'])),
                  ('trust (o) scene-fill renders/ png pairs with ../html/ = PASS', ro['status'] == 'PASS' and any('fo.html' in x for x in ro['sources']))]
        ok = all(v for _, v in cases)
        for n, v in cases: print(f'  {"ok  " if v else "FAIL"} {n}')
        if not ok:
            for k, v in res.items(): print('   ', k, v['status'], v['block'][:3], v['warn'][:2])
        print(f'selftest {"PASS" if ok else "FAIL"} {sum(v for _, v in cases)}/{len(cases)}')
        return 0 if ok else 1
    finally:
        print(f'note: selftest scratch kept at {d} (no-delete rule; a few KB)')

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument('--snap', help='snapshot dir (must be the pointer snap; default: the pointer)'); ap.add_argument('--selftest', action='store_true'); ap.add_argument('paths', nargs='*')
    a = ap.parse_args()
    if a.selftest:
        print(f'text-check {md5(os.path.abspath(__file__))[:8]} words {md5(DATA)[:8]} selftest chrome {"yes" if CHROME else "no"}'); sys.exit(selftest())
    ctx = context()
    if a.snap and ctx.snap_dir and os.path.realpath(a.snap) != os.path.realpath(ctx.snap_dir):
        print(ctx.stamp()); print(f'STALE-SNAP {a.snap} is not the pointer snap dir {ctx.snap_dir}'); sys.exit(2)
    if not a.paths: print(ctx.stamp()); print('ERROR no files given'); sys.exit(2)
    sys.exit(run(a.paths, ctx))
