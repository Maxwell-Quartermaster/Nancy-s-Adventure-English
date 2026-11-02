# Chancellor's pacing sim (chancellor/v608sim/sim.py, read-only) run on the staged cards; mode B moves Bloodtide to level 12 and Dragonbane to level 16.
import sys, json, io, contextlib
src = open('/workspace/chancellor/v608sim/sim.py').read()
src = src.replace("/workspace/v608build/snap-1604MDT/nancys-adventure-english-v6-08-cards.json", "/workspace/nancys-adventure-english-v6-08-cards.json")
def run(mode):
    s = src
    if mode == 'B':
        s = s.replace("tro=c['trophies']", "tro=c['trophies']\nfor t in tro:\n    if t['id']=='cleaver-bloodtide': t['unlock']={'type':'level','n':12}\n    if t['id']=='greatsword-dragonbane': t['unlock']={'type':'level','n':16}")
    g = {'__name__': 'sim'}; buf = io.StringIO()
    sys.argv = ['sim']
    with contextlib.redirect_stdout(buf): exec(compile(s, 'sim', 'exec'), g)
    return g['out']
if __name__ == '__main__':
    for m in 'AB':
        o = run(m)
        print(m, [(d, ev) for d, z, xp, L, pf, st, ev in o if any('bloodtide' in e or 'dragonbane' in e for e in ev)], sum(1 for r in o[:34] if not r[6]))
