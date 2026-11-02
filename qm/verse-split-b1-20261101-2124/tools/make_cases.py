# QM: write negative PASTE copies into scratch/cases/ from the real PASTE 317e91ce (read only). Only the JSON line changes.
import json, hashlib, os, copy
P = '/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
raw = open(P, 'rb').read(); assert hashlib.md5(raw).hexdigest() == '317e91ce86f073c961f8169183d2bbd3'
lines = raw.decode('utf-8').split('\n'); i = [n for n, l in enumerate(lines) if l.startswith('{"version"')]; assert len(i) == 1; i = i[0]
J = json.loads(lines[i]); out = 'scratch/cases'
def w(name, j):
    L = list(lines); L[i] = json.dumps(j, ensure_ascii=False); open(f'{out}/{name}.md', 'w', encoding='utf-8').write('\n'.join(L))
open(f'{out}/control.md', 'wb').write(raw)   # byte copy
for grp, get in (('rest', lambda j: j['verses']['rest']), ('jw', lambda j: j['jesusWords'][0])):
    keys = ('ref', 'en', 'th', 'enSource', 'thSource') if grp == 'rest' else ('ref', 'en', 'th')
    for k in keys:
        for kind, val in (('empty', ''), ('space', '   '), ('wsmix', ' \n\t '), ('null', None), ('missing', KeyError)):
            j = copy.deepcopy(J); d = get(j)
            if val is KeyError: del d[k]
            else: d[k] = val
            w(f'{grp}-{k}-{kind}', j)
j = copy.deepcopy(J); j['jesusWords'] = []; w('jw-empty-list', j)
j = copy.deepcopy(J); del j['verses']['rest']; w('rest-missing', j)
j = copy.deepcopy(J); j['verses']['rest']['en'] = 123; w('rest-en-number', j)
print(len(os.listdir(out)), 'cases')
