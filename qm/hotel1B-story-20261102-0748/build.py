# Quartermaster: hotel 1B + zone story order (MAP 1A) combined candidate. Copies only; never edits sources. No deletes.
import json,hashlib
BASE='/workspace/qm/cards-fix-20261102-0704/new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md'
PROOF='/workspace/qm/zone-map-20261102-0736/PROOF-line427-reordered.json'
OUT='nancys-adventure-english-v6-08-1B-v32-hotel1B-story-PASTE.md'
CAP=188200
md=lambda s:hashlib.md5(s.encode()).hexdigest()
base=open(BASE,encoding='utf-8').read(); assert md(base)=='5e1666fe6f7189d3886686749335b3ee' and len(base)==188007
proof=open(PROOF,encoding='utf-8').read(); assert hashlib.md5(open(PROOF,'rb').read()).hexdigest()=='321ddb1a3561c6e0ce5400a405a76669'
L=base.split('\n'); n0=len(L)
def rep(i,old,new):   # i = 1-based line
    assert L[i-1].count(old)==1,(i,old); L[i-1]=L[i-1].replace(old,new)
dump=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
# ---- line 427: round-trip guard
d=json.loads(L[426]); assert dump(d)==L[426]
# (a) story order from PROOF ids, ms-33 slotted right after ms-28
order=[c['id'] for c in json.loads(proof)['cards']]
assert sorted(order)==sorted(c['id'] for c in d['cards'])
byid={c['id']:c for c in d['cards']}
d['cards']=[byid[i] for i in order]
assert dump(d)==proof.strip(), 'reorder != PROOF'
# (a) X6 outings swap in place
o=d['meta']['outings']; assert o==['ms-01','ms-02','ms-05','fd-29','fd-30','fd-31','bh-01','bh-02','bh-05','ms-11','ms-12']
d['meta']['outings']=[{'ms-01':'ms-13','ms-02':'ms-29','ms-11':'ms-28'}.get(x,x) for x in o]
# (b) hotel 1B card edits (same strings as hotel-steps build.py 3cec4953)
c3=byid['ms-03']; assert dump(c3)=='{"id":"ms-03","en":"Welcome to our hotel.","th":"ยินดีต้อนรับสู่โรงแรมของเราค่ะ","respell":"WEL-kum too OW-er hoh-TEL","personal":true,"type":"say-it"}'
c3.update(en='I have a reservation.',th='ฉันจองห้องไว้ค่ะ',respell='ai HAV uh rez-er-VAY-shun'); c3['syl']='res·er·va·tion'
c6=byid['ms-06']; s6=dump(c6)
for a,b in [('"en":"One night is one hundred twenty dollars."','"en":"One hundred twenty dollars a night."'),
            ('"respell":"WUN NAIT iz WUN HUN-dred TWEN-tee DOL-erz"','"respell":"WUN HUN-dred TWEN-tee DOL-erz uh NAIT"'),
            ('"One night is one hundred twelve dollars."','"One hundred twelve dollars a night."'),
            ('"One night is two hundred twenty dollars."','"Two hundred twenty dollars a night."'),
            ('"One night is one hundred twenty dollars."','"One hundred twenty dollars a night."'),
            ('"One night is one hundred dollars."','"One hundred dollars a night."'),
            ('"O__ n____ i_ o__ h______ t_____ d______."','"O__ h______ t_____ d______ a n____."')]:
    assert a in s6,a; s6=s6.replace(a,b)
assert 'One night' not in s6
n6=json.loads(s6); c6.clear(); c6.update(n6)
ms33=json.loads('{"id":"ms-33","type":"say-it","en":"I need more towels.","th":"ขอผ้าเช็ดตัวเพิ่มค่ะ","respell":"ai NEED mor TOW-ulz","personal":true}')
ids=[c['id'] for c in d['cards']]; d['cards'].insert(ids.index('ms-28')+1,ms33)
m=d['meta']
for k,a,b in [('totalCards',211,212),('writtenCards',211,212),('sayItWritten',37,38),('sayItTotal',37,38),('personalCards',80,81),('personalWritten',80,81)]:
    assert m[k]==a,(k,m[k]); m[k]=b
L[426]=dump(d)
# spec lines
rep(223,' seen longest ago. Never 4 say-it',' seen longest ago. In `bh` and `ms`, file order (places in time) replaces personal-first and fewest-words order. Never 4 say-it')
rep(227,' and `ms-21`–`ms-23`','')
rep(364,'- **Approved 7-word exceptions:** `ms-06` and `bh-14`','- **Approved 7-word exception:** `bh-14`')
rep(236,'74 cards are `type: "say-it"`','75 cards are `type: "say-it"`')
rep(350,'- **211 cards** in `cards.json`','- **212 cards** in `cards.json`')
rep(362,'**Personal cards:** 80 are','**Personal cards:** 81 are')
rep(375,'205 of the 211 written cards','206 of the 212 written cards')
s='\n'.join(L); assert len(L)==n0
open(OUT,'x',encoding='utf-8').write(s)
print(OUT,len(s),'delta',len(s)-len(base),'bank',CAP-len(s),md(s))
