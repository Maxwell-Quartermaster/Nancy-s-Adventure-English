import json,re,sys,collections
SRC="/workspace/qm/cards-fix-20261102-0704/new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md"
raw=open(SRC,encoding='utf-8').read()
L=raw.split('\n')
d=json.loads(L[426])
# key path index
paths=collections.defaultdict(set)  # leaf key -> full paths
allpaths=set()
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            q=f"{p}.{k}" if p else k
            paths[k].add(q); allpaths.add(q); walk(v,q)
    elif isinstance(o,list):
        for v in o: walk(v,p+"[]")
walk(d,"")
cardids={c['id'] for c in d['cards']}
trophyids={t['id'] for t in d['trophies']}
svgids=set(d['picPlan']['svg'])|set(d['picPlan']['trophySvg'])|set(d['picPlan']['uiSvg'])
prefixes={p:z['key'] for z in d['zones'] for p in z['prefix'].split()}
zonekeys={z['key'] for z in d['zones']}
def sec_of(n):
    s=None
    for i in range(n):
        if L[i].startswith('#'): s=L[i].lstrip('#').strip()
    return s
def resolve(tok):
    t=tok.strip()
    t2=re.sub(r'^(state|cards\.json)\.','',t)
    if t in cardids: return ('card id', f"cards[] id={t}")
    if t in trophyids: return ('trophy id', f"trophies[] id={t}")
    m=re.fullmatch(r'svg:([\w-]+)',t)
    if m and (t in svgids or m.group(1) in svgids or any(t==c.get('pic') for c in d['cards'])):
        return ('svg id', f"picPlan svg lists / pic value {t}")
    if t in prefixes: return ('zone prefix', f"zones[] key={prefixes[t]} prefix")
    if t in zonekeys: return ('zone key', f"zones[] key={t}")
    tp=t.replace('[]','')
    norm=re.sub(r'\[\]','[]',t)
    if norm in allpaths: return ('data path', norm)
    # dotted path where segments map with [] insertion
    segs=tp.split('.')
    cands=[p for p in allpaths if p.replace('[]','').split('.')==segs]
    if cands: return ('data path', ' | '.join(sorted(cands)))
    # relative: e.g. thsv11Tag under verses.attribution, or uiText key bare
    if len(segs)==1 and segs[0] in paths:
        ps=sorted(paths[segs[0]])
        cat='uiText key' if f"uiText.{segs[0]}" in ps and len(ps)==1 else ('top-level key' if segs[0] in d else 'data key')
        return (cat,' | '.join(ps[:6])+(' …' if len(ps)>6 else ''))
    if segs[0]=='.' or t.startswith('.'):
        return None
    # suffix match
    cands=[p for p in allpaths if p.replace('[]','').endswith('.'+tp)]
    if cands: return ('data path (partial)',' | '.join(sorted(cands)[:6]))
    return None
xrefs=[];unres=collections.Counter();unres_lines=collections.defaultdict(list)
for n in range(1,426):
    line=L[n-1]
    toks=re.findall(r'`([^`]+)`',line)
    # card ids anywhere in plain text too
    ids=set(re.findall(r'\b([a-z]{2}-\d{2})\b',line))
    seen=set()
    for t in toks:
        r=resolve(t)
        if r: xrefs.append((n,sec_of(n),t,r[0],r[1])); seen.add(t)
        else: unres[t]+=1; unres_lines[t].append(n)
    for i in sorted(ids-seen):
        if i in cardids: xrefs.append((n,sec_of(n),i,'card id (plain text)',f"cards[] id={i}"))
        else: xrefs.append((n,sec_of(n),i,'MISSING card id','NOT FOUND'))
json.dump({'xrefs':xrefs,'unresolved':{k:unres_lines[k] for k in unres}},open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
print(len(xrefs),'xref rows;',len({x[2] for x in xrefs}),'unique tokens;',len(unres),'unresolved backtick tokens')
print(collections.Counter(x[3] for x in xrefs))
print('MISSING:',[x for x in xrefs if 'MISSING' in x[3]])
print(sorted(unres))
