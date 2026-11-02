# v6-08 generator: v6-07 (frozen at the Auditor gate) + A1/A2 ask-card rule and Thai wrap, VP verse pop-up B + daily gift (FINAL/spec/cards), E1 happy eyes (cards #rE, title Sam, spec note), version.
import json, hashlib, collections, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open('/workspace/v605build/qm_v605.py').read(); i = src.index('def paste'); j = src.index("W = '/workspace/'")
exec(src[src.index('import'):src.index('\n', src.index('import'))]); exec(src[i:j])
import fixes_v608 as X
W = '/workspace/'; B = 'v6-07'; V = 'v6-08'; N = 'nancys-adventure-english-'
def md5(p): return hashlib.md5(open(W + p, 'rb').read()).hexdigest()
SRC = {N+B+'-PASTE.md': 'aa73cc93', N+B+'-cards.json': 'a29fdf25', N+'FINAL-'+B+'.md': '0d8133bd', N+B+'.md': '6fc65d79', N+B+'-daily-verses.json': '83e22b0e',
       N+B+'-title.svg': '0b92e0b4', 'CURRENT.md': 'b653ffb2'}
for p, h in SRC.items(): assert md5(p).startswith(h), (p, md5(p), h)
rd = lambda p: open(W + p, encoding='utf-8').read()
P1 = rd(N+B+'-PASTE.md'); F = rd(N+'FINAL-'+B+'.md'); S = rd(N+B+'.md')
OD = collections.OrderedDict; d = json.loads(rd(N+B+'-cards.json'), object_pairs_hook=OD); rawv = rd(N+B+'-daily-verses.json')
assert paste(F, d, B) == P1, 'paste assembly does not reproduce v6-07'
D = []
def R(tag, a, b):
    global F, S
    assert F.count(a) == 1 and S.count(a) == 1, (tag, F.count(a), S.count(a), a[:80])
    F = F.replace(a, b); S = S.replace(a, b); D.append((tag, len(b) - len(a)))
for t, a, b in X.SPEC + X.VP + X.H1 + X.P1 + X.SC: R(t, a, b)
assert S.count(X.E1_SPEC[0]) == 1 and F.count(X.E1_SPEC[0]) == 0; S = S.replace(*X.E1_SPEC)   # spec-only note (not in FINAL)
TT = rd(N+B+'-title.svg'); assert TT.count(X.E1_TITLE[0]) == 1; TT = TT.replace(*X.E1_TITLE)
nF = F.count(B); F = F.replace(B, V)
for a in ('`' + N + B + '-cards.json`', '`' + N + B + '-daily-verses.json`', '**v6 list (from ' + B + '):**'): assert S.count(a) == 1, a; S = S.replace(a, a.replace(B, V))
assert S.count('`' + N + B + '-title.svg`') == 1; S = S.replace('`' + N + B + '-title.svg`', '`' + N + V + '-title.svg`')
D.append(('version v6-07 -> v6-08 (%d in FINAL)' % nF, 0))
assert d['version'] == B and d['meta']['version'] == B; d['version'] = V; d['meta']['version'] = V
n0 = len(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
def _sub(o):
    if isinstance(o, dict): return o.__class__((k, _sub(v)) for k, v in o.items())
    if isinstance(o, list): return [_sub(v) for v in o]
    return o.replace(*X.E1_CARDS) if isinstance(o, str) else o
_raw = json.dumps(d, ensure_ascii=False); assert _raw.count(X.E1_CARDS[0]) == 1
def _sub(o):
    if isinstance(o, dict): return o.__class__((k, _sub(v)) for k, v in o.items())
    if isinstance(o, list): return [_sub(v) for v in o]
    return o.replace(*X.E1_CARDS) if isinstance(o, str) else o
d = _sub(d)
D.append(('E1 happy eyes: #rE = Nancy\'s exact arcs (Sam\'s shared eye component) (cards)', len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) - n0))
n2 = len(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
_ms31 = [c for c in d['cards'] if c['id'] == 'ms-31'][0]
for ch in _ms31['choices']: o, n_ = X.H1_CARDS[ch['key']]; assert ch['pic'] == o; ch['pic'] = n_
D.append(('H1 ms-31 choices: hand emoji (cards)', len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) - n2))
n1 = len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))); assert X.VP_UI[0] not in d['uiText'] and d['meta']['uiTextEntries'] == len(d['uiText']) == 92
d['uiText'][X.VP_UI[0]] = OD(X.VP_UI[1]); d['meta']['uiTextEntries'] = 93
D.append(('VP uiText.dailyGift (NEEDS NANCY) + uiTextEntries 93', len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) - n1))
n4 = len(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
_tr = [t for t in d['trophies'] if t.get('id') == 'tunic-rose'][0]; assert _tr['word'][1] == X.G1_CARDS[0] and _tr['word'][2] == 'ความชอบธรรม'; _tr['word'][1] = X.G1_CARDS[1]
D.append(('G1 tunic-rose meaning: Right with God as His free gift (cards)', len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) - n4))
n5 = len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))); assert len(d['uiText']) == 93 and d['meta']['uiTextEntries'] == 93
for k_, v_ in X.SC_UI: assert k_ not in d['uiText']; d['uiText'][k_] = OD(v_)
d['meta']['uiTextEntries'] = len(d['uiText']); assert d['meta']['uiTextEntries'] == 97
_C = {c['id']: c for c in d['cards']}; assert all(_C[i].get('pic') for v_ in X.SC_SIZE.values() for i in v_); assert 'sizeSort' not in d['meta']; d['meta']['sizeSort'] = X.SC_SIZE
_np = 0
for pr in d['soundDuel']['pairs']:
    k_ = (pr['a'], pr['b'])
    if k_ in X.SC_PICS: pr['pics'] = X.SC_PICS[k_]; _np += 1
assert _np == 6
D.append(('SC uiText listenFind/howMany/howManyCows/bigOrSmall (NEEDS NANCY) + meta.sizeSort + 6 soundDuel pics (cards)', len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) - n5))
out = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
dv = json.loads(rawv, object_pairs_hook=OD); dv['version'] = V
vout = json.dumps(dv, ensure_ascii=False, indent=2); assert vout == rawv.replace('"version": "%s"' % B, '"version": "%s"' % V, 1)
P2 = paste(F, d, V)
bk = re.search(r'Banked in v6-07: 6350 chars under 188,200 \(PASTE 181,850 chars\)', S); assert bk, 'banked line'
S = S.replace(bk.group(0), 'Banked in %s: %d chars under 188,200 (PASTE %s chars)' % (V, 188200 - len(P2), format(len(P2), ',')))
assert B not in F and P2.count('heavy laden') == 1 and 'of 42' not in P2 and len(P2) <= 188200
assert not re.search(r'\(\?<|(padding|margin|inset|border)-(inline|block)|(min-|max-)?(inline|block)-size|(padding|margin)-(start|end)\b|text-align\s*:\s*(start|end)|\binset\s*:', P2)
assert len(P2) - len(P1) == sum(x[1] for x in D), (len(P2) - len(P1), D)
if '--dry' not in sys.argv:
    for p, t in [(N+'FINAL-'+V+'.md', F), (N+V+'-cards.json', out), (N+V+'-PASTE.md', P2), (N+V+'.md', S), (N+V+'-daily-verses.json', vout), (N+V+'-title.svg', TT)]:
        assert V in p and (not os.path.exists(W + p) or '--force' in sys.argv), 'exists: ' + p
        open(W + p, 'w', encoding='utf-8').write(t)
for x in D: print(x)
print(V, '| PASTE', len(P1), '->', len(P2), '%+d' % (len(P2) - len(P1)), '| banked', 188200 - len(P2), '| title', len(TT), '%+d' % (len(TT) - len(rd(N+B+'-title.svg'))), hashlib.md5(TT.encode()).hexdigest()[:8])
