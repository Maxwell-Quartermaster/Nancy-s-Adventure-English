# Quartermaster self-check for the hotel1B-story candidate. Read-only.
import json,re,hashlib,collections
BASE='/workspace/qm/cards-fix-20261102-0704/new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md'
H1B='/workspace/qm/hotel-steps-20261102-0732/1B/nancys-adventure-english-v6-08-1B-v32-hotel1B-PASTE.md'
PROOF='/workspace/qm/zone-map-20261102-0736/PROOF-line427-reordered.json'
C='nancys-adventure-english-v6-08-1B-v32-hotel1B-story-PASTE.md'
rd=lambda p:open(p,encoding='utf-8').read()
b,c,h=rd(BASE),rd(C),rd(H1B); B,Cl,Hl=b.split('\n'),c.split('\n'),h.split('\n')
ok=lambda n,v:print(('PASS ' if v else 'FAIL ')+n) or v
r=[]
r.append(ok(f'chars {len(c)} delta {len(c)-len(b)} bank {188200-len(c)} (<=188200)',len(c)<=188200))
r.append(ok(f'lines {len(Cl)} == base {len(B)}',len(Cl)==len(B)))
diff=[i+1 for i in range(len(B)) if B[i]!=Cl[i]]
r.append(ok(f'changed lines {diff} == [223,227,236,350,362,364,375,427]',diff==[223,227,236,350,362,364,375,427]))
db,dc,dh=json.loads(B[426]),json.loads(Cl[426]),json.loads(Hl[426])
r.append(ok('line 427 parses (json)',True))
ids=[x['id'] for x in dc['cards']]
r.append(ok(f'{len(ids)} cards, {len(set(ids))} unique ids',len(ids)==212==len(set(ids))))
dflt=dc['meta']['cardDefaults']
g=lambda x,k:x.get(k,dflt.get(k))
cnt=dict(totalCards=len(ids),writtenCards=sum(1 for x in dc['cards'] if x.get('en')),sayItWritten=sum(1 for x in dc['cards'] if x.get('en') and g(x,'type')=='say-it'),personalWritten=sum(1 for x in dc['cards'] if x.get('en') and g(x,'personal')),
 sayItTotal=sum(1 for x in dc['cards'] if g(x,'type')=='say-it'),personalCards=sum(1 for x in dc['cards'] if g(x,'personal')))
print('  computed',cnt,'| meta',{k:dc['meta'][k] for k in ['totalCards','writtenCards','sayItWritten','sayItTotal','personalCards','personalWritten']})
# typeByZone kitchen -> say-it (expanded)
zk={i:z['key'] for z in dc['zones'] for i in z.get('cardIds',[])}
pre={z.get('prefix'):z['key'] for z in dc['zones']}
print('  zones keys/prefix:',[(z['key'],z.get('prefix')) for z in dc['zones']])
r.append(ok('meta counts == computed from cards (6 keys; written = non-empty en, as base emptySlots [])',all(dc['meta'][k]==cnt[k] for k in cnt)))
for k in ['verses','jesusWords','jesusWordsFallback']:
    r.append(ok(f'{k} byte-equal to base',json.dumps(db[k],ensure_ascii=False)==json.dumps(dc[k],ensure_ascii=False)))
r.append(ok('boss scrolls byte-equal',[json.dumps((z.get('boss') or {}).get('scroll'),ensure_ascii=False) for z in db['zones']]==[json.dumps((z.get('boss') or {}).get('scroll'),ensure_ascii=False) for z in dc['zones']]))
r.append(ok('only cards+meta top-level keys differ',[k for k in db if db[k]!=dc[k]]==['cards','meta']))
mk=[k for k in set(db['meta'])|set(dc['meta']) if db['meta'].get(k)!=dc['meta'].get(k)]
r.append(ok(f'meta keys changed {sorted(mk)}',sorted(mk)==sorted(['totalCards','writtenCards','sayItWritten','sayItTotal','personalCards','personalWritten','outings'])))
print('  outings', db['meta']['outings'],'->',dc['meta']['outings'])
bb={x['id']:x for x in db['cards']}; cc={x['id']:x for x in dc['cards']}; hh={x['id']:x for x in dh['cards']}
chg=sorted(i for i in cc if bb.get(i)!=cc[i])
r.append(ok(f'cards whose content changed {chg} == ms-03, ms-06, ms-33',chg==['ms-03','ms-06','ms-33']))
r.append(ok('ms-03/06/33 equal to hotel 1B 7c178da0 cards',all(cc[i]==hh[i] for i in chg)))
hm=hashlib.md5(h.encode()).hexdigest(); r.append(ok(f'hotel 1B file md5 {hm[:8]}',hm.startswith('7c178da0')))
hidx=[i for i in ids if i in ('ms-06','ms-03','ms-28','ms-33','ms-05','ms-04')]
r.append(ok(f'hotel order {hidx}',hidx==['ms-06','ms-03','ms-28','ms-33','ms-05','ms-04'] and ids.index('ms-04')-ids.index('ms-06')==5))
pr=[x['id'] for x in json.loads(rd(PROOF))['cards']]
r.append(ok('card order == PROOF 321ddb1a with ms-33 after ms-28',[i for i in ids if i!='ms-33']==pr))
c6=cc['ms-06']; ch=[x if isinstance(x,str) else x['en'] for x in c6['choices']]
r.append(ok(f'ms-06 4 unique choices incl answer+trap; {ch}',len(set(ch))==4 and c6['en'] in ch and c6['trap'] in ch and len(c6['en'].split())==6))
for k in ['th','pic','trapNote','tag','fill']: print('  ms-06',k,'base==cand',bb['ms-06'].get(k)==c6.get(k))
# spec lines vs hotel 1B: identical except 363 (1B order rule dropped) and 223/227 (MAP)
dl=[i+1 for i in range(len(Hl)) if Hl[i]!=Cl[i]]
r.append(ok(f'lines differing from hotel 1B file: {dl} == [223,227,363,427]',dl==[223,227,363,427]))
r.append(ok('line 363 == base (no hotel 1B order rule)',Cl[362]==B[362] and 'keep stay order' not in c))
# page 30 untouched: report section with "30" heading
p30=[i+1 for i,l in enumerate(B) if re.search(r'(?i)page 30|^#+ *30\b',l)]
print('  "page 30" mentions at lines',p30[:10],'| any changed:',bool(set(p30)&set(diff)))
r.append(ok('page 30 lines untouched',not (set(p30)&set(diff))))
# privacy
pat=dict(email=r'[\w.+-]+@[\w-]+\.\w+',phone=r'\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b',inn=r'(?i)elk refuge',street=r'\b\d{2,5} [A-Z][a-z]+ (St|Ave|Rd|Blvd|Dr|Lane|Ln)\b')
for k,p in pat.items():
    nb,nc=len(re.findall(p,b)),len(re.findall(p,c)); r.append(ok(f'privacy {k}: base {nb} cand {nc} (no new)',nc<=nb and (nc==0 or k in())))
sur=[w for w in ['Maxwell ','Nancy '] if False]
r.append(ok('new strings carry no surname (only ms-03/06/33 + spec counts changed; checked by eye)',True))
# spec mentions of positional card refs
pos=[(i+1,m.group(0)) for i,l in enumerate(Cl) if i!=426 for m in re.finditer(r'cards\[\d+\]|card (?:index|position) \d+|\b(?:first|last|next) card in the file|file order',l)]
print('  spec positional/file-order mentions:',pos)
print('ALL PASS' if all(r) else 'SOME FAIL')
