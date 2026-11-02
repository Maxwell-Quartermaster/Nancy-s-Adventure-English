# Quartermaster hotel-steps draft builder. Copies only; never edits src.
import json,hashlib,sys
SRC='src/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md'
CAP=188200
base=open(SRC,encoding='utf-8').read()
assert hashlib.md5(base.encode()).hexdigest()=='5e1666fe6f7189d3886686749335b3ee'
def rep(s,old,new,line=None):
    L=s.split('\n')
    if line is not None:
        assert L[line-1].count(old)==1,(old,line); L[line-1]=L[line-1].replace(old,new); return '\n'.join(L)
    assert s.count(old)==1,old; return s.replace(old,new)
INN='until Maxwell confirms them.'
ORDER1A=' Hotel cards in one run keep stay order: `ms-06`, `ms-03`, `ms-28`, `ms-05`, `ms-04`.'
ORDER1B=' Hotel cards in one run keep stay order: `ms-06`, `ms-03`, `ms-28`, `ms-33`, `ms-05`, `ms-04`.'
OLD03='{"id":"ms-03","en":"Welcome to our hotel.","th":"ยินดีต้อนรับสู่โรงแรมของเราค่ะ","respell":"WEL-kum too OW-er hoh-TEL","personal":true,"type":"say-it"}'
NEW03='{"id":"ms-03","en":"I have a reservation.","th":"ฉันจองห้องไว้ค่ะ","respell":"ai HAV uh rez-er-VAY-shun","personal":true,"type":"say-it","syl":"res·er·va·tion"}'
# ---- 1A: order rule only
a=rep(base,INN,INN+ORDER1A,363)
# ---- 1B: order rule + ms-06 to 6 words + new courtesy-call card ms-33
b=rep(base,INN,INN+ORDER1B,363)
b=rep(b,'- **Approved 7-word exceptions:** `ms-06` and `bh-14`','- **Approved 7-word exception:** `bh-14`',364)
old06=json.dumps([c for c in json.loads(base.split('\n')[426])['cards'] if c['id']=='ms-06'][0],ensure_ascii=False,separators=(',',':'))
assert base.split('\n')[426].count(old06)==1
new06=old06
for o,n in [('"en":"One night is one hundred twenty dollars."','"en":"One hundred twenty dollars a night."'),
            ('"respell":"WUN NAIT iz WUN HUN-dred TWEN-tee DOL-erz"','"respell":"WUN HUN-dred TWEN-tee DOL-erz uh NAIT"'),
            ('"One night is one hundred twelve dollars."','"One hundred twelve dollars a night."'),
            ('"One night is two hundred twenty dollars."','"Two hundred twenty dollars a night."'),
            ('"One night is one hundred twenty dollars."','"One hundred twenty dollars a night."'),
            ('"One night is one hundred dollars."','"One hundred dollars a night."'),
            ('"O__ n____ i_ o__ h______ t_____ d______."','"O__ h______ t_____ d______ a n____."')]:
    assert o in new06,o; new06=new06.replace(o,n)
assert 'One night' not in new06
b=rep(b,old06,new06,427)
ms32end='"hint":["L__ m_ f__ y___ t__, h____.","f","fix"]}'
ms33='{"id":"ms-33","type":"say-it","en":"I need more towels.","th":"ขอผ้าเช็ดตัวเพิ่มค่ะ","respell":"ai NEED mor TOW-ulz","personal":true}'
b=rep(b,OLD03,NEW03,427)
b=rep(b,ms32end,ms32end+','+ms33,427)
for o,n,ln in [('"totalCards":211,"writtenCards":211','"totalCards":212,"writtenCards":212',427),
               ('"sayItWritten":37,"sayItTotal":37','"sayItWritten":38,"sayItTotal":38',427),
               ('"personalCards":80,"personalWritten":80','"personalCards":81,"personalWritten":81',427),
               ('74 cards are `type: "say-it"`','75 cards are `type: "say-it"`',236),
               ('- **211 cards** in `cards.json`','- **212 cards** in `cards.json`',350),
               ('**Personal cards:** 80 are','**Personal cards:** 81 are',362),
               ('205 of the 211 written cards','206 of the 212 written cards',375)]:
    b=rep(b,o,n,ln)
out={'1A':a,'1B':b}
for k,s in out.items():
    fn=f'{k}/nancys-adventure-english-v6-08-1B-v32-hotel{k}-PASTE.md'
    open(fn,'w',encoding='utf-8').write(s)
    print(k,fn,len(s),'delta',len(s)-len(base),'bank',CAP-len(s),hashlib.md5(s.encode()).hexdigest())
