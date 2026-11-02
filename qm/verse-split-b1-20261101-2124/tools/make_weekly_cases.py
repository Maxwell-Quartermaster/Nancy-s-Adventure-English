# QM: weekly[] negative PASTE copies from the real PASTE 317e91ce (read only). Only the JSON line changes.
import json, hashlib, copy
P = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
raw = open(P, 'rb').read(); assert hashlib.md5(raw).hexdigest() == '317e91ce86f073c961f8169183d2bbd3'
lines = raw.decode('utf-8').split('\n'); i = [n for n, l in enumerate(lines) if l.startswith('{"version"')][0]; J = json.loads(lines[i]); c = 0
for wi in (0, 9):
    for k in ('ref', 'en', 'th', 'enSource', 'thSource'):
        for kind, val in (('empty', ''), ('space', '   '), ('null', None), ('missing', KeyError)):
            j = copy.deepcopy(J); d = j['verses']['weekly'][wi]
            if val is KeyError: del d[k]
            else: d[k] = val
            L = list(lines); L[i] = json.dumps(j, ensure_ascii=False); open(f'scratch/cases/weekly{wi}-{k}-{kind}.md', 'w', encoding='utf-8').write('\n'.join(L)); c += 1
print(c, 'weekly cases')
