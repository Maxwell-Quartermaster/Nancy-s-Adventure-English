# cards_render.py <390|320> <outdir>: the 4 new 1A cards read from the candidate PASTE line 427, drawn with play_v608.sayit (lake say-it card, as page 16)
import sys, os, json; sys.dont_write_bytecode = True
size, od = sys.argv[1], sys.argv[2]; sys.argv = ['x']; D = '/workspace/qm/cards-flexgap-20261102-0519'
sys.path.insert(0, D + '/new'); import play_v608 as PV
assert PV.SE == (size == '320'); W, H = (320, 568) if PV.SE else (390, 844)
J = json.loads(open(D + '/new/nancys-adventure-english-v6-08-1B-v32-cards1A-PASTE.md', encoding='utf-8').read().split('\n')[426])
os.makedirs(od, exist_ok=True)
for c in J['cards']:
    if c['id'] in ('bh-30', 'ms-28', 'ms-29', 'ms-30'):
        PV.C[c['id']] = c
        d = PV.page(W, H, PV.flexgap(PV.sayit(c['id'], 'lake')))
        open(f"{od}/card-{c['id']}-{W}x{H}.html", 'w', encoding='utf-8').write(d); print(c['id'], c['en'], c['th'], c['respell'])
