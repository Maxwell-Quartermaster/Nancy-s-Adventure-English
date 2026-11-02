# Builds part files, header variants, cross-reference table and self-check facts from the source PASTE.
# Read-only on SRC. Writes only inside this kit folder.
import json,re,hashlib,collections,os,sys
KIT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC="/workspace/qm/cards-fix-20261102-0704/new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md"
SB=open(SRC,'rb').read(); S=SB.decode('utf-8'); L=S.split('\n')
md5=lambda b: hashlib.md5(b if isinstance(b,bytes) else b.encode('utf-8')).hexdigest()
CUT=420  # part 2 starts at this 1-based line
off=sum(len(x)+1 for x in L[:CUT-1])
p1=S[:off]; p2=S[off:]
assert p1+p2==S
open(f"{KIT}/part1.md",'w',encoding='utf-8',newline='').write(p1)
open(f"{KIT}/part2.md",'w',encoding='utf-8',newline='').write(p2)
H1="<!-- Part 1 of 2 (spec, source lines 1-419). Read COMBINE-GUIDE.md first; delete this line before joining. -->\n"
H2="<!-- Part 2 of 2 (card file, source lines 420-428; cards.json is the JSON line). Read COMBINE-GUIDE.md first; delete this line before joining. -->\n"
open(f"{KIT}/part1-with-header.md",'w',encoding='utf-8',newline='').write(H1+p1)
open(f"{KIT}/part2-with-header.md",'w',encoding='utf-8',newline='').write(H2+p2)
J=L[426]; d=json.loads(J)
F={}
F['src']=dict(md5=md5(SB),chars=len(S),bytes=len(SB),lines=S.count('\n'))
F['p1']=dict(lines=f"1-{CUT-1}",chars=len(p1),bytes=len(p1.encode()),md5=md5(p1))
F['p2']=dict(lines=f"{CUT}-{S.count(chr(10))}",chars=len(p2),bytes=len(p2.encode()),md5=md5(p2))
F['h1']=dict(chars=len(H1),md5=md5(H1+p1)); F['h2']=dict(chars=len(H2),md5=md5(H2+p2))
F['json']=dict(line=427,chars=len(J),bytes=len(J.encode()),md5=md5(J),md5nl=md5(J+'\n'))
F['spec']=dict(chars=len(p1),lines_1_426_chars=len('\n'.join(L[:426])+'\n'))
# ---- self-check facts
cards=d['cards']; ids=[c['id'] for c in cards]
pref={p:z['key'] for z in d['zones'] for p in z['prefix'].split()}
def zone(c): return pref[c['id'].split('-')[0]]
D=d['meta']['cardDefaults']
def g(c,k): return c.get(k,D.get(k))
F['cards']=len(cards); F['unique']=len(set(ids)); F['dupes']=[i for i,n in collections.Counter(ids).items() if n>1]
F['byzone']=dict(collections.Counter(zone(c) for c in cards))
F['bytype']=dict(collections.Counter(c.get('type',d['meta']['typeByZone'].get(zone(c),'picture')) for c in cards))
F['personal']=sum(1 for c in cards if g(c,'personal'))
F['nurse']=sorted(c['id'] for c in cards if g(c,'nursePhrase'))
F['fill']=sorted(c['id'] for c in cards if g(c,'fill'))
F['thDef']=sum(1 for c in cards if 'thDef' in c)
F['signedoff']=sorted(c['id'] for c in cards if c.get('thStatus')=='SIGNED OFF')
F['zones']=[(z['order'],z['key'],z['name'],z['prefix'],bool(z.get('boss')),len(z['boss']['cards']) if z.get('boss') else 0, z['boss']['scroll']['ref'] if z.get('boss') else None) for z in d['zones']]
F['startZone']=[z['key'] for z in d['zones'] if z.get('startZone')]
vs=[('weekly',v) for v in d['verses']['weekly']]+[('rest',d['verses']['rest'])]+[('boss:'+z['key'],z['boss']['scroll']) for z in d['zones'] if z.get('boss')]
F['verses']=[(w,v['ref'],md5(v['en']),md5(v['th']),v.get('status')) for w,v in vs]
F['jw']=[(v['ref'],md5(v['en']),md5(v['th'])) for v in d['jesusWords']]
F['attr']={k:md5(d['verses']['attribution'][k]) for k in ('esv','thsv11','esvTag','thsv11Tag')}
F['needsMaxwell']=d['needsMaxwell']
F['ui']=len(d['uiText']); F['enc']=len(d['encouragement']); F['troph']=len(d['trophies'])
F['trophcat']=dict(collections.Counter(t.get('cat','(none)') for t in d['trophies']))
F['duel']=len(d['soundDuel']['pairs']); F['duelpics']=sum(1 for p in d['soundDuel']['pairs'] if p.get('pics'))
F['jwn']=len(d['jesusWords']); F['jwf']=len(d['jesusWordsFallback']); F['clips']=len(d['rewardClips'])
pp=d['picPlan']; F['pic']=dict(svg=len(pp['svg']),trophySvg=len(pp['trophySvg']),uiSvg=len(pp['uiSvg']),inline=sorted(pp['inlineSvg']),trophyInline=sorted(pp['trophyInlineSvg']),uiInline=sorted(pp['uiInlineSvg']),svgDrawn=pp['svgDrawnCount'],trophyDrawn=pp['trophySvgDrawnCount'])
F['regions']=[(r['id'],r['en'],r['zones']) for r in d['mapLayout']['regions']]
F['topkeys']=list(d.keys())
F['meta']={k:d['meta'][k] for k in ('totalCards','writtenCards','sayItTotal','sayItWritten','personalCards','personalWritten','pictureCards','thDefCards','uiTextEntries','needsMaxwellCount','versesVerified','jesusWords','trophies','encouragementLines','version')}
F['outings']=d['meta']['outings']
F['pantry']=len(d['pantry']['items'])
F['emoji']=sum(1 for c in cards if c.get('pic') and not str(c['pic']).startswith('svg:'))
F['svgcards']=sum(1 for c in cards if str(c.get('pic') or '').startswith('svg:'))
# ---- cross-reference scan
paths=collections.defaultdict(set); allp=set()
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            q=f"{p}.{k}" if p else k; paths[k].add(q); allp.add(q); walk(v,q)
    elif isinstance(o,list):
        for v in o: walk(v,p+"[]")
walk(d,"")
cid=set(ids); tid={t['id'] for t in d['trophies']}
svgs=set(pp['svg'])|set(pp['trophySvg'])|set(pp['uiSvg'])
DEFAULTED={'mode':'meta.modeByType (from type)','nameThStatus':'meta.thStatusDefault (absent in file = default)','thDefStatus':'meta.thStatusDefault (absent in file = default)','thStatus':'cards[].thStatus (6 SIGNED OFF) else meta.cardThStatusDefault'}
DERIVED={'classTitle':'derived: trophyRules.classes by weapon wt -> uiText.class*','hint.letters':'cards[].hint (compact: string=sound, list=[letters,sound,word])','hint.sound':'cards[].hint (compact)','hint.word':'cards[].hint (compact; data only)','letters':'cards[].hint (compact)','sound':'cards[].hint (compact)','tierNames[t]':'trophyRules.tierNames'}
EXTERNAL={'daily-verses.json':'2nd attached file nancys-adventure-english-v6-08-daily-verses.json','nancys-adventure-english-v6-08-daily-verses.json':'2nd attached file','title.svg':'3rd attached file nancys-adventure-english-v6-08-title.svg','nancys-adventure-english-v6-08-title.svg':'3rd attached file','enGloss':'daily-verses.json verses[] (optional)','maxwell-<zone>.m4a':'zones[].zoneClip','maxwell-boss-<zone>.m4a':'zones[].boss.clip','maxwell-reward-1..5.m4a':'rewardClips','/audio/':'zones[].zoneClip, boss.clip, rewardClips paths','cards.json':'Part 2 JSON line (save as cards.json)'}
PATTERN={'svg:<id>':'cards[].pic / picPlan.svg ids','uiText.bonus<word>':'uiText.bonus* (10 keys)','<type>-t<t>':'trophies[].id pattern'}
MUSTNOT={'cost':'must NOT exist anywhere (grace check)','price':'must NOT exist anywhere (grace check)'}
def res(t):
    t=t.strip()
    if t in cid: return 'card id','cards[] id='+t
    if t in tid: return 'trophy id','trophies[] id='+t
    if t in svgs or (t.startswith('svg:') and any(c.get('pic')==t for c in cards)) or t in {f'svg:{s}' for s in svgs}: return 'svg id','picPlan / cards[].pic '+t
    if t in pref: return 'zone prefix',f'zones[key={pref[t]}].prefix'
    if t in {z['key'] for z in d['zones']}: return 'zone key',f'zones[key={t}]'
    for tab,cat in ((DERIVED,'derived'),(DEFAULTED,'defaulted field'),(EXTERNAL,'attached file'),(PATTERN,'id pattern'),(MUSTNOT,'must-not-exist')):
        if t in tab: return cat,tab[t]
    if re.fullmatch(r'[\w]+:<[^>]*>',t): return None  # ledger key pattern (state), not data
    if t=='"two-answer"': return 'data value','cards[].type = "two-answer" (ms-31)'
    if t=='NEEDS NANCY': return 'data value','meta.cardThStatusDefault / meta.thStatusDefault = "NEEDS NANCY"'
    m=re.fullmatch(r'([\w.]+)\s*:\s*(.+)',t)
    if m and not t.startswith(('display','line-height','paint-order','prefers','schema')):
        r=res(m.group(1))
        if r: return 'data value',r[1]+' = '+m.group(2)
    segs=t.replace('[]','').split('.')
    if segs[0]=='' : segs=['verses','attribution']+segs[1:]
    c=[p for p in allp if p.replace('[]','').split('.')==segs]
    if c: return ('uiText key' if segs[0]=='uiText' else 'data path'),' | '.join(sorted(c))
    if len(segs)==1 and segs[0] in paths:
        ps=sorted(paths[segs[0]])
        if segs[0] in d: return 'top-level key',segs[0]
        if ps==[f'uiText.{segs[0]}']: return 'uiText key',ps[0]
        return 'data key',' | '.join(ps[:5])+(f' (+{len(ps)-5} more)' if len(ps)>5 else '')
    c=[p for p in allp if p.replace('[]','').endswith('.'+'.'.join(segs))]
    if c: return 'data path',' | '.join(sorted(c)[:5])
    return None
sec=None; X=collections.OrderedDict(); spec_only=collections.defaultdict(list); secrefs=0
for n in range(1,427):
    line=L[n-1]
    if line.startswith('#'): sec=line.lstrip('#').strip()
    secrefs+=len(re.findall(r'\b(?:section|sections) \d+|\(\d+\.\d+\)|\b\d+\.\d+\'s\b',line))
    found=set()
    for t in re.findall(r'`([^`]+)`',line):
        r=res(t)
        if r:
            X.setdefault(t,{'cat':r[0],'where':r[1],'lines':[], 'secs':[]}); X[t]['lines'].append(n); X[t]['secs'].append(sec); found.add(t)
        else: spec_only[t].append(n)
    for i in set(re.findall(r'\b([a-z]{2}-\d{2})\b',line))-found:
        k=i; X.setdefault(k,{'cat':'card id' if i in cid else 'MISSING','where':'cards[] id='+i if i in cid else 'NOT IN FILE','lines':[],'secs':[]}); X[k]['lines'].append(n); X[k]['secs'].append(sec)
F['xref_unique']=len(X); F['xref_occ']=sum(len(v['lines']) for v in X.values())
F['xref_cats']=dict(collections.Counter(v['cat'] for v in X.values()))
F['missing']=[k for k,v in X.items() if v['cat']=='MISSING']
F['spec_only']=len(spec_only); F['secrefs']=secrefs
uinamed={k for k in d['uiText'] if f'uiText.{k}' in S[:off] or re.search(r'`'+re.escape(k)+r'`',S[:off])}
F['ui_unnamed']=sorted(set(d['uiText'])-uinamed)
json.dump({'X':X,'spec_only':spec_only},open(f"{KIT}/tmp/xref.json",'w'),ensure_ascii=False)
json.dump(F,open(f"{KIT}/tmp/facts.json",'w'),ensure_ascii=False,indent=1)
print(json.dumps({k:F[k] for k in ('src','p1','p2','h1','h2','json','xref_unique','xref_occ','xref_cats','missing','spec_only','secrefs')},indent=0))
print('ui unnamed',len(F['ui_unnamed']),F['ui_unnamed'])
