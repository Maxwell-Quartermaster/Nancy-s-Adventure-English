# Updated inventory: the read-only scan (council-tools/scene_inventory.py -> /tmp/inv/rows.json) with this staging dir as CANDIDATE.
# Cell rule as scene_inventory_build.py; CANDIDATE ranks after IN-PROGRESS. Writes only into scene-fill-20261101/.
import json, collections as C, datetime
B = '/workspace/v608build/scene-fill-20261101/'; PFX = 'v608build/scene-fill-20261101/renders/'
R = json.load(open('/tmp/inv/rows.json'))
for r in R:
    if r['in_progress'] and r['status'] != 'BEFORE': r['status'] = 'IN-PROGRESS'
    if r['path'].startswith(PFX): r['status'] = 'CANDIDATE' if r['look_ok'] is not False else 'CANDIDATE-STALE-LOOK'
mine = [r for r in R if r['path'].startswith(PFX)]
for r in mine:   # loc/tod from the render sidecar (written at render time) where the scanner's name/HTML heuristics don't know the fill names
    sc = json.load(open('/workspace/' + r['path'][:-4] + '.json')); r['loc'] = sc['loc']; r['tod'] = {'base': 'e' if sc['loc'] == 'REST' else 'base'}.get(sc['tod'], sc['tod'])
    if r['kind'] == 'sheet': r['kind'] = 'screen'
RANK = ['CURRENT', 'IN-PROGRESS', 'CANDIDATE', 'CURRENT-LISTED-STALE-LOOK', 'CANDIDATE-STALE-LOOK', 'OLD']
LOCS = ['meadow-park', 'meadow-pond', 'lake-home', 'lake-kitchen', 'lake-front-desk', 'fields-farm', 'forest-woods']
def cell(loc, tod):
    rs = [r for r in R if r['loc'] == loc and r['tod'] == tod and r['kind'] != 'sheet']
    sizes = lambda st: sorted({r['size'] for r in rs if r['status'] in st})
    best = next((s for s in RANK if any(r['status'] == s for r in rs)), 'NEVER')
    cov = sizes(('CURRENT', 'IN-PROGRESS', 'CANDIDATE'))
    return dict(loc=loc, tod=tod, best=best, current=sizes(('CURRENT',)), in_progress=sizes(('IN-PROGRESS',)), candidate=sizes(('CANDIDATE',)),
                covered=cov, missing=[s for s in ('320x568', '390x844') if s not in cov])
cells = [cell(l, t) for l in LOCS for t in 'mdaen'] + [cell(l, 'base') for l in ('lake-front-desk',)]
extra = [cell('TITLE', t) for t in 'maen'] + [cell('MENU', t) for t in 'maen'] + [cell('REST', t) for t in ('e', 'sunset', 'starry')]
cnt = C.Counter(c['best'] for c in cells[:35])
gaps = [c for c in cells + extra if c['missing']]
out = dict(generated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M MDT'), candidate_dir=PFX, candidate_rows=len(mine),
           candidate_by=dict(C.Counter(f"{r['loc']}|{r['tod']}|{r['size']}" for r in mine)), cells=cells, extra=extra, best_counts_35=dict(cnt), gaps=gaps)
json.dump(out, open(B + 'scene-inventory-update.json', 'w'), indent=1)
P = '**Quartermaster:** '
L = [P + f'updated scene inventory {out["generated"]}: the read-only scan with scene-fill-20261101/renders as CANDIDATE ({len(mine)} candidate PNG rows). Base: snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce.',
     P + 'best status over the 35 spec cells (7 locations x 5 times): ' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items())),
     P + '| location | time | best | current | in-progress | candidate | still missing |', P + '|---|---|---|---|---|---|---|']
for c in cells + extra:
    L.append(P + f"| {c['loc']} | {c['tod']} | {c['best']} | {' '.join(c['current']) or '-'} | {' '.join(c['in_progress']) or '-'} | {' '.join(c['candidate']) or '-'} | {' '.join(c['missing']) or '-'} |")
L.append(P + 'cells still missing a size after the fill: ' + ('; '.join(f"{c['loc']} {c['tod']} {' '.join(c['missing'])}" for c in gaps) or 'none'))
open(B + 'scene-inventory-update.md', 'w').write('\n\n'.join(L) + '\n')
print(dict(cnt)); print('candidate rows', len(mine)); print('unclassified mine:', [r['path'] for r in mine if not r['loc'] or not r['tod']])
for c in gaps: print('GAP', c['loc'], c['tod'], c['best'], c['missing'])
