#!/usr/bin/env python3
"""Auditor's planted-fault kit (owner: Auditor). Every council tool must pass its case set here before Chancellor installs it.

  python3 run_kit.py <tool-name> <path-to-tool> [--only ID,ID] [--keep]
  python3 run_kit.py --self-test          # the kit must FAIL deliberately broken stubs (stubs/)
  python3 run_kit.py --list               # tools and case counts

tool-name: text_check | ground_check | tuft_check | freeze | quote_check | conflict_check
A case with expect RECORD is a recorded edge case: its result is printed as REC and never counts.
Prints PASS/FAIL per case, a total, and exits 0 only if every REQUIRED case gives its expected verdict
(advisory cases are reported but never decide the exit). Exit 1 = a required case failed, 2 = bad usage / tool not found.
Safety: the tool is COPIED into runs/<run>/tool/ and only the copy is run. Scratch lives only under this kit's runs/.
freeze is only ever run with --sandbox inside runs/; the live /workspace/v608build/CURRENT-SNAP.txt md5 is checked
before and after. Nothing outside /workspace/audit/fault-kit/ is written or deleted."""
import datetime, hashlib, json, os, re, shutil, subprocess, sys, time
KIT = os.path.dirname(os.path.abspath(__file__)); CASES = os.path.join(KIT, 'cases'); RUNS = os.path.join(KIT, 'runs')
VERSION = 'fault-kit v1.1'
LIVE_PTR = '/workspace/v608build/CURRENT-SNAP.txt'
TOOLS = ('text_check', 'ground_check', 'tuft_check', 'freeze', 'quote_check', 'conflict_check')
SIBLINGS = {'text_check': ['text_check_words.json'], 'freeze': ['hold_check.py']}
sys.dont_write_bytecode = True

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def now_mt():
    try:
        from zoneinfo import ZoneInfo; d = datetime.datetime.now(ZoneInfo('America/Denver'))
    except Exception: d = datetime.datetime.now()
    return d
def load_cases(tool): return json.load(open(os.path.join(CASES, tool, 'cases.json'), encoding='utf-8'))
def safe_rm(p):
    p = os.path.realpath(p)
    if not p.startswith(RUNS + os.sep): raise RuntimeError(f'refusing to delete outside kit runs/: {p}')
    subprocess.run(['chmod', '-R', 'u+w', p]); shutil.rmtree(p, ignore_errors=True)

# ------------------------------------------------------------------ text_check
def tc_fixture(fx):
    B = f'{fx}/v608build'; SNAP = f'{B}/snap-t'; REND = f'{fx}/renders'
    for p in (f'{SNAP}/showcase', f'{SNAP}/sheets', f'{SNAP}/code', f'{B}/r2h-build', f'{REND}/png'): os.makedirs(p)
    data = {"version": "t", "wrongText": {"en": "Now you know it", "th": "ตอนนี้รู้แล้วนะ"},
            "uiText": {"tapPrompt": {"en": "Can you find the {word}?", "th": "หา {word} เจอไหม"}, "pantry": {"en": "Shop", "th": "ร้านดาวทอง"}},
            "cards": [{"id": "bh-24", "en": "Where is the bathroom?", "th": "ห้องน้ำอยู่ที่ไหนคะ"}, {"id": "cs-22", "en": "long", "choices": [{"en": "wrong"}]},
                      {"id": "px-1", "en": "Call Max"}, {"id": "px-2", "en": "Please show the nurse my card"}, {"id": "px-3", "en": "Dial 911"}]}
    paste = f'{B}/r2h-build/p.md'; open(paste, 'w', encoding='utf-8').write('# spec (fault-kit fixture)\n' + json.dumps(data, ensure_ascii=False) + '\n')
    open(f'{SNAP}/MANIFEST.md5', 'w').write('')
    ptr = f'{B}/CURRENT-SNAP.txt'; open(ptr, 'w').write(f'snap=snap-t\nmanifest_md5=x\npaste_1b_md5={md5(paste)}\npaste_1b_path=r2h-build/p.md\n')
    return B, SNAP, REND, ptr
def tc_build(c, SNAP, REND, T0):
    page = lambda body: f"<html><head><style>body{{margin:0;width:390px}} .th{{font-size:18px;line-height:1.7}}</style></head><body>{body}</body></html>"
    def pair(name, body, where):
        h = f'{where}/{name}.html'; p = f'{where}/{name}.png'
        open(p, 'wb').write(b'\x89PNG\r\n\x1a\n' + name.encode()); open(h, 'w', encoding='utf-8').write(page(body))
        os.utime(p, (T0, T0)); os.utime(h, (T0, T0)); return p
    k, n = c['kind'], c['name']
    if k == 'pair': return pair(n, c['body'], f'{SNAP}/showcase')
    if k == 'sidecar_sheet':
        p1 = pair(f'{n}-a', '<div>Can you find the kite?</div>', f'{REND}/png'); p2 = pair(f'{n}-b', '<div>Can you find the kite?</div>', f'{REND}/png')
        sp = f'{SNAP}/showcase/{n}.png'; open(sp, 'wb').write(b'\x89PNG\r\n\x1a\n' + n.encode()); os.utime(sp, (T0 + 20, T0 + 20))
        open(sp + '.sources.txt', 'w', encoding='utf-8').write(f'{md5(p1)}  {p1}\n{md5(p2)}  {p2}\n' + ''.join(f'caption {x}\n' for x in c['captions'])); return sp
    if k == 'builder':
        sp = f'{SNAP}/sheets/{n}.png'; open(sp, 'wb').write(b'\x89PNG\r\n\x1a\n' + n.encode()); os.utime(sp, (T0 + 10, T0 + 10))
        py = f'{SNAP}/code/mk_{n}.py'; open(py, 'w', encoding='utf-8').write(f"from PIL import Image\nS = Image.new('RGB', (9, 9))\ncap = {c['caption']!r}\nS.save('/nonexistent/{n}.png')\n"); os.utime(py, (T0 + 5, T0 + 5))
        return sp
    dst = f'{SNAP}/{n}'; os.makedirs(os.path.dirname(dst), exist_ok=True)
    if k == 'copy': shutil.copy2(os.path.join(CASES, 'text_check', 'inputs', c['input']), dst); return dst
    if k == 'png_nosource': open(dst, 'wb').write(b'\x89PNG\r\n\x1a\n' + b'orphan'); os.utime(dst, (T0, T0)); return dst
    if k == 'file': open(dst, 'w', encoding='utf-8').write(c['content']); return dst
    raise ValueError(f'unknown case kind {k}')
def run_text_check(tool, run, cs, only):
    B, SNAP, REND, ptr = tc_fixture(f'{run}/fx'); T0 = time.time() - 3600; out = []
    env = dict(os.environ, CURRENT_SNAP=ptr, PYTHONDONTWRITEBYTECODE='1')
    for c in cs:
        try: p = tc_build(c, SNAP, REND, T0)
        except Exception as e: out.append((c, 'BUILD-ERROR', str(e), False)); continue
        r = subprocess.run([sys.executable, tool, p], capture_output=True, text=True, env=env, timeout=300, cwd=run)
        txt = r.stdout + r.stderr
        m = re.search(r'^(PASS|BLOCK|TEXT UNVERIFIED|SKIP) +\S', txt, re.M); st = m.group(1) if m else f'NO-STATUS(exit {r.returncode})'
        warns = [l.strip() for l in txt.splitlines() if l.startswith('    WARN')]; blocks = [l.strip() for l in txt.splitlines() if l.startswith('    BLOCK')]
        e = c['expect']
        if e == 'BLOCK': ok = st == 'BLOCK' and r.returncode == 1
        elif e == 'UNVERIFIED': ok = st == 'TEXT UNVERIFIED' and r.returncode == 1
        elif e == 'BLOCK|UNVERIFIED': ok = st in ('BLOCK', 'TEXT UNVERIFIED') and r.returncode == 1
        elif e == 'NOT-BLOCK': ok = r.returncode == 0 and st in ('PASS', 'SKIP')
        elif e.startswith('WARN:'): ok = r.returncode == 0 and st == 'PASS' and any(e[5:] in w for w in warns)
        else: raise ValueError(e)
        detail = (blocks or warns or [''])[0][:150]
        out.append((c, f'{st} exit {r.returncode}', detail, ok))
    return out

# ------------------------------------------------------------------ ground_check
GC_DRIVER = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True
s = importlib.util.spec_from_file_location('gc_under_test', sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
res = {}
for p in sys.argv[2:]:
    try: r = m.check(p); res[p] = {'block': bool(r), 'msg': ' ; '.join(map(str, r))[:200] if r else ''}
    except Exception as e: res[p] = {'block': None, 'msg': f'EXCEPTION {e.__class__.__name__}: {e}'}
print('@@JSON@@' + json.dumps(res))
'''
def gc_judge(tool, run, items):   # items: list of image paths -> {path: {'block', 'msg'}}
    drv = f'{run}/gc_driver.py'; open(drv, 'w').write(GC_DRIVER)
    r = subprocess.run([sys.executable, drv, tool] + items, capture_output=True, text=True, timeout=3600, cwd=run)
    m = re.search(r'@@JSON@@(.*)$', r.stdout, re.M)
    if not m: return None, (r.stderr or r.stdout)[-200:]
    return json.loads(m.group(1)), ''
def run_ground_check(tool, run, cs, only):
    sys.path.insert(0, os.path.join(CASES, 'ground_check')); import panels
    G = os.path.join(CASES, 'ground_check'); jobs = {}; os.makedirs(f'{run}/panels', exist_ok=True)
    for c in cs:
        src = os.path.join(G, c['path']) if c.get('path') else os.path.join(G, 'images', c['file'])
        if c.get('mode') == 'panels':   # kit-side split at the cream gaps; each panel judged on its own
            im, boxes = panels.split(src); ps = []
            for i, b in enumerate(boxes, 1):
                pp = f'{run}/panels/{c["id"]}-panel{i}.png'; im.crop(b).save(pp); ps.append(pp)
            jobs[c['id']] = ps
        else: jobs[c['id']] = [src]
    res, err = gc_judge(tool, run, sorted({p for v in jobs.values() for p in v}))
    out = []
    for c in cs:
        if res is None: out.append((c, 'TOOL-ERROR', err, False)); continue
        xs = [res[p] for p in jobs[c['id']]]
        if any(x['block'] is None for x in xs): got = 'ERROR'
        else: got = 'BLOCK' if any(x['block'] for x in xs) else 'PASS'
        msg = ' | '.join(f'p{i}: {x["msg"][:70]}' for i, x in enumerate(xs, 1) if x['msg']) if len(xs) > 1 else xs[0]['msg']
        if len(xs) > 1: got += ' (per panel: ' + ''.join('B' if x['block'] else '.' for x in xs) + ')'
        out.append((c, got, msg[:220], None if c['expect'] == 'RECORD' else got.split()[0] == c['expect']))
    return out

# ------------------------------------------------------------------ tuft_check (Watchman; t545u scope)
def run_tuft_check(tool, run, cs, only):
    T = os.path.join(CASES, 'tuft_check', 'images'); imgs = [os.path.join(T, c['file']) for c in cs]
    res, err = gc_judge(tool, run, imgs)   # same module interface: check(path) -> list of reasons
    out = []
    for c, p in zip(cs, imgs):
        if res is None: out.append((c, 'TOOL-ERROR', err, False)); continue
        x = res[p]; reasons = x['msg']
        if x['block'] is None: got = 'ERROR'
        else: got = 'FLAG' if any(r.strip().startswith('rock') for r in reasons.split(' ; ') if r) else 'PASS'
        if got == 'PASS' and reasons: got = 'PASS (+note)'
        out.append((c, got, reasons[:200], None if c['expect'] == 'RECORD' else got.split()[0] == c['expect']))
    return out

# ------------------------------------------------------------------ freeze
CS_ANCHOR = "    probs = []\n"
CS_PLANT = "    if os.environ.get('GATE_STEP6_FAIL') == '1' and sys.argv[:1] == ['-c'] and d.get('snap') != 'snap-r2h-0021MDT': probs.append('planted step-6 verify failure (Auditor fault kit)')\n"
SG_WRAP = ("# Auditor fault-kit hook wrapper (kit copy only): optional planted action, then the real send_guard (send_guard_real.py, byte-identical copy).\n"
           "import os, sys, runpy\n_h = os.environ.get('GATE_HOOK')\nif _h: exec(open(_h).read())\n"
           "_real = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'send_guard_real.py')\nsys.argv[0] = _real; runpy.run_path(_real, run_name='__main__')\n")
def freeze_env(run):
    dst = f'{run}/env/council-tools'
    shutil.copytree('/workspace/council-tools', dst, symlinks=True, ignore=shutil.ignore_patterns('__pycache__', 'incoming', 'runs', '*.bak'))
    sg = f'{dst}/send-guard'; os.rename(f'{sg}/send_guard.py', f'{sg}/send_guard_real.py'); open(f'{sg}/send_guard.py', 'w').write(SG_WRAP)
    cs = open(f'{dst}/current_snap.py').read(); notes = []
    if CS_ANCHOR in cs and 'def verify' in cs:
        i = cs.index('def verify'); j = cs.index(CS_ANCHOR, i) + len(CS_ANCHOR); cs = cs[:j] + CS_PLANT + cs[j:]
        cs = cs.replace('import os, hashlib', 'import os, sys, hashlib', 1) if 'import os, sys' not in cs else cs
        open(f'{dst}/current_snap.py', 'w').write(cs)
    else: notes.append('current_snap.py anchor not found: F7b plant not installed (F7b will fail as ENV)')
    return dst, notes
def run_freeze(tool, run, cs, only):
    hc = os.path.join(os.path.dirname(tool), 'hold_check.py')
    if not os.path.isfile(hc): return [(c, 'NO hold_check.py next to the tool', '', False) for c in cs]
    env_tools, notes = freeze_env(run)
    for n in notes: print('note', n)
    outj = f'{run}/freeze-results.json'
    env = dict(os.environ, FK_FZ=tool, FK_HC=hc, FK_TOOLS=env_tools, FK_ROOT=f'{run}/sbx', FK_STAGE=os.path.join(CASES, 'freeze', 'stage'),
               FK_HOOKS=os.path.join(CASES, 'freeze', 'hooks'), FK_OUT=outj, PYTHONDONTWRITEBYTECODE='1')
    if only: env['FK_ONLY'] = ','.join(sorted(only_parent_ids(only)))
    p = subprocess.run([sys.executable, os.path.join(CASES, 'freeze', 'freeze_cases.py')], env=env, capture_output=True, text=True, timeout=7200)
    open(f'{run}/freeze-cases.out', 'w').write(p.stdout + p.stderr)
    res = json.load(open(outj)) if os.path.isfile(outj) else {'rows': []}
    rows = {r['id']: r for r in res['rows']}; out = []
    for c in cs:
        r = rows.get(c['id'])
        if not r: out.append((c, 'NOT RUN', (p.stderr or '')[-150:], False)); continue
        out.append((c, f'{r["verdict"]} exit {r["exit"]}', r['actual'][:150], r['verdict'] == 'PASS'))
    if res.get('live_pointer_before') and res['live_pointer_before'] != res['live_pointer_after']:
        print(f'WARNING live pointer changed during the run ({res["live_pointer_before"]} -> {res["live_pointer_after"]}); the kit only uses --sandbox, so another process moved it. Affected cases are marked FAIL.')
    safe_rm(f'{run}/env')
    return out
def only_parent_ids(only):
    m = {'F0a-clean-dry-run': 'F0-clean', 'F9-pass-copy2-clean-run': 'F0-clean', 'F8e-pointer-restored-then-force-clear': 'F8d-manual-HOLD-moved-force-clear'}
    return {m.get(x, x) for x in only}

# ------------------------------------------------------------------ quote_check / conflict_check
def run_quote_check(tool, run, cs, only):
    d = os.path.join(CASES, 'quote_check'); out = []
    for c in cs:
        r = subprocess.run([sys.executable, tool, os.path.join(d, c['post']), os.path.join(d, 'ledger-excerpt.md'), os.path.join(d, 'spec-317e91ce-excerpt.md')], capture_output=True, text=True, timeout=120, cwd=run)
        flags = re.findall(r'^\s*FLAG\s+([A-Z_-]+)', r.stdout, re.M); e = c['expect']
        if e == 'CLEAN': ok = r.returncode == 0 and not flags
        else:
            m = re.match(r'FLAG:([A-Z_-]+)(?:x(\d+))?$', e); kind, n = m.group(1), int(m.group(2) or 1)
            ok = r.returncode == 1 and flags.count(kind) >= n
        out.append((c, f'exit {r.returncode} flags {flags or "none"}', (r.stdout + r.stderr).strip().splitlines()[-1][:150] if (r.stdout + r.stderr).strip() else '', ok))
    return out
def run_conflict_check(tool, run, cs, only):
    paste = os.path.join(CASES, 'conflict_check', 'paste-317e91ce-excerpt.md'); before = md5(paste); out = []
    for c in cs:
        r = subprocess.run([sys.executable, tool, paste, str(c['line']), c['new']], capture_output=True, text=True, timeout=120, cwd=run)
        hits = sorted({int(x) for x in re.findall(r'(?:^|\s):(\d+)\s', r.stdout, re.M)} - {c['line']})
        miss = [x for x in c['flag'] if x not in hits]; wrong = [x for x in c['not_flag'] if x in hits]
        ok = r.returncode == c['exit'] and not miss and not wrong
        out.append((c, f'exit {r.returncode} hits {hits}', f'missed {miss} wrongly flagged {wrong}', ok))
    if md5(paste) != before: print('FAIL tool modified the PASTE excerpt (must be read-only)'); out.append(({'id': 'RO', 'required': True, 'expect': 'read-only', 'why': 'tool must not edit the PASTE'}, 'MODIFIED', '', False))
    return out

RUNNERS = {'text_check': run_text_check, 'ground_check': run_ground_check, 'tuft_check': run_tuft_check, 'freeze': run_freeze, 'quote_check': run_quote_check, 'conflict_check': run_conflict_check}

def run_kit(tool_name, path, only=None, keep=False, quiet=False):
    if tool_name not in RUNNERS: print(f'ERROR unknown tool {tool_name}; one of {", ".join(TOOLS)}'); return 2
    if not os.path.isfile(path): print(f'ERROR {tool_name}: {path} not found (tool NOT BUILT or wrong path); 0 cases run'); return 2
    spec = load_cases(tool_name); cs = [c for c in spec['cases'] if not only or c['id'] in only]
    tmd5 = md5(path); stamp = now_mt().strftime('%Y%m%d-%H%M%S')
    run = os.path.join(RUNS, f'{tool_name}-{tmd5[:8]}-{stamp}-{os.getpid()}'); os.makedirs(f'{run}/tool')
    copy = os.path.join(run, 'tool', os.path.basename(path)); shutil.copy2(path, copy)
    for s in SIBLINGS.get(tool_name, []):
        sp = os.path.join(os.path.dirname(os.path.abspath(path)), s)
        if os.path.isfile(sp): shutil.copy2(sp, os.path.join(run, 'tool', s))
    live0 = md5(LIVE_PTR) if os.path.isfile(LIVE_PTR) else None
    print(f'{VERSION} | run_kit {md5(os.path.abspath(__file__))} | tool {tool_name} {path} md5 {tmd5} (run on copy {copy})')
    print(f'cases {os.path.join(CASES, tool_name, "cases.json")} md5 {md5(os.path.join(CASES, tool_name, "cases.json"))} | {len(cs)} cases | {now_mt().strftime("%Y-%m-%d %H:%M %Z")}')
    for s in SIBLINGS.get(tool_name, []):
        sp = os.path.join(run, 'tool', s); print(f'sibling {s} md5 {md5(sp) if os.path.isfile(sp) else "MISSING"}')
    t0 = time.time(); res = RUNNERS[tool_name](copy, run, cs, only)
    rows = []
    for c, got, detail, ok in res:
        req = c.get('required', True); exp = c.get('expect') or f"exit {c.get('exit')} flag {c.get('flag')} not {c.get('not_flag')}"
        rec_ = ok is None; req = req and not rec_
        rows.append(dict(id=c['id'], required=req, recorded=rec_, expect=exp, got=got, ok=None if rec_ else bool(ok), detail=detail, why=c.get('why', ''), source=c.get('source', '')))
        if not quiet: print(f'{"REC " if rec_ else ("PASS" if ok else "FAIL")} | {c["id"]:<48} | {"recorded" if rec_ else ("required" if req else "advisory")} | want {exp} | got {got} | {detail}')
    rq = [r for r in rows if r['required']]; ad = [r for r in rows if not r['required'] and not r['recorded']]; nrec = sum(r['recorded'] for r in rows)
    nreq = sum(r['ok'] for r in rq); nad = sum(r['ok'] for r in ad)
    live1 = md5(LIVE_PTR) if os.path.isfile(LIVE_PTR) else None
    code = 0 if nreq == len(rq) and rq else 1
    print(f'TOTAL {tool_name} {tmd5[:8]}: required {nreq}/{len(rq)} PASS, advisory {nad}/{len(ad)} PASS, {nrec} recorded -> {"KIT PASS" if code == 0 else "KIT FAIL"} (exit {code}); {time.time()-t0:.0f} s; live pointer {"unchanged" if live0 == live1 else f"CHANGED {live0} -> {live1} (not by the kit)"}')
    if code: print('failed required: ' + ', '.join(r['id'] for r in rq if not r['ok']))
    json.dump(dict(kit=VERSION, tool=tool_name, path=path, md5=tmd5, exit=code, required=[nreq, len(rq)], advisory=[nad, len(ad)], rows=rows), open(f'{run}/results.json', 'w'), indent=1, ensure_ascii=False)
    print(f'results {run}/results.json')
    if not keep:   # keep results, drop bulky scratch (inside runs/ only)
        for sub in ('fx', 'sbx', 'env'):
            if os.path.isdir(f'{run}/{sub}'): safe_rm(f'{run}/{sub}')
    return code

def self_test():
    st = os.path.join(KIT, 'stubs'); checks = []
    stubs = [('text_check', 'text_check_stub_alwayspass.py'), ('text_check', 'text_check_stub_alwaysblock.py'), ('ground_check', 'ground_check_stub_alwayspass.py'),
             ('ground_check', 'ground_check_stub_alwaysblock.py'), ('tuft_check', 'tuft_check_stub_neverflag.py'), ('tuft_check', 'tuft_check_stub_alwaysflag.py'), ('freeze', 'freeze/freeze.py'), ('quote_check', 'quote_check_stub_neverflag.py'),
             ('quote_check', 'quote_check_stub_alwaysflag.py'), ('conflict_check', 'conflict_check_stub_nohits.py'), ('conflict_check', 'conflict_check_stub_flagall.py')]
    print(f'{VERSION} self-test: the kit must report FAILURE (exit 1) on every deliberately broken stub')
    for tool, s in stubs:
        r = subprocess.run([sys.executable, os.path.abspath(__file__), tool, os.path.join(st, s)], capture_output=True, text=True, timeout=1800)
        nf = len(re.findall(r'^FAIL \|', r.stdout, re.M)); ok = r.returncode == 1 and nf > 0
        checks.append(ok); print(f'{"PASS" if ok else "FAIL"} | stub {tool:<14} {s:<40} md5 {md5(os.path.join(st, s))[:8]} | kit exit {r.returncode}, {nf} case FAILs reported')
    r = subprocess.run([sys.executable, os.path.abspath(__file__), 'quote_check', os.path.join(st, 'does-not-exist.py')], capture_output=True, text=True)
    ok = r.returncode == 2; checks.append(ok); print(f'{"PASS" if ok else "FAIL"} | missing tool path -> kit exit 2 (got {r.returncode})')
    for t in TOOLS:   # every case set loads and every case names why + source
        cs = load_cases(t)['cases']; ok = bool(cs) and all(c.get('why') and c.get('source') for c in cs) and len({c['id'] for c in cs}) == len(cs)
        checks.append(ok); print(f'{"PASS" if ok else "FAIL"} | {t} case set: {len(cs)} cases, unique ids, each has why + source')
    n = sum(checks); print(f'SELF-TEST {"PASS" if n == len(checks) else "FAIL"} {n}/{len(checks)}'); return 0 if n == len(checks) else 1

if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--self-test']: sys.exit(self_test())
    if a == ['--list']:
        for t in TOOLS:
            cs = load_cases(t)['cases']; print(f'{t:<15} {len(cs):>3} cases ({sum(c.get("required", True) and c.get("expect") != "RECORD" for c in cs)} required, {sum(c.get("expect") == "RECORD" for c in cs)} recorded)')
        sys.exit(0)
    only = None; keep = '--keep' in a; a = [x for x in a if x != '--keep']
    if '--only' in a: i = a.index('--only'); only = set(a[i + 1].split(',')); del a[i:i + 2]
    if len(a) != 2: print(__doc__); sys.exit(2)
    sys.exit(run_kit(a[0], a[1], only, keep))
