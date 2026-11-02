#!/usr/bin/env python3
"""Instructor scratch: char cost of filling bh-30, ms-28..30 on a COPY of PASTE 317e91ce.
Metric = fit_table's own: len(PASTE text, utf-8 decoded); bank = fit_table.check_bank (ceiling 188200 - len).
Writes variant copies only into this scratch folder."""
import sys,os,json,hashlib
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'council-tools','fit-table'))
import fit_table as ft
C=json.load(open(os.path.join(H,'council-tools','fit-table','costs.json'))); C=dict(C,bank=None)
src=os.path.join(H,'PASTE-317e91ce-copy.md'); base=open(src,encoding='utf-8').read()
assert hashlib.md5(base.encode()).hexdigest().startswith('317e91ce')
OLD={'bh-30':'{"id":"bh-30","type":"say-it","en":"","th":"","respell":"","fill":true,"slot":"baby","personal":true}',
 'ms-28':'{"id":"ms-28","type":"say-it","en":"","th":"","respell":"","fill":true,"slot":"hotel","personal":true}',
 'ms-29':'{"id":"ms-29","type":"say-it","en":"","th":"","respell":"","fill":true,"slot":"husband","personal":true}',
 'ms-30':'{"id":"ms-30","type":"say-it","en":"","th":"","respell":"","fill":true,"slot":"faith","faith":true,"personal":true}'}
SL={'bh-30':'baby','ms-28':'hotel','ms-29':'husband','ms-30':'faith'}
D={'1A':{'bh-30':("The baby is kicking.","ลูกดิ้นค่ะ","thuh BAY-bee iz KIK-ing"),
 'ms-28':("Here is your key.","นี่กุญแจของคุณค่ะ","HEER iz yor KEE"),
 'ms-29':("This is my husband.","นี่สามีของฉันค่ะ","THIS iz mai HUZ-bund"),
 'ms-30':("God is good.","พระเจ้าทรงดีครับ","GOD iz GUD")},
 '1B':{'bh-30':("My baby is healthy.","ลูกของฉันแข็งแรงดีค่ะ","mai BAY-bee iz HEL-thee"),
 'ms-28':("Do you need more towels?","ต้องการผ้าเช็ดตัวเพิ่มไหมคะ","doo yoo NEED mor TOW-elz"),
 'ms-29':("You are my wife.","คุณเป็นภรรยาของผมครับ","yoo ar mai WAIF"),
 'ms-30':("God takes care of us.","พระเจ้าทรงดูแลเราครับ","GOD tayks KAIR uv us")}}
def frag(cid,t,lean):
    en,th,rs=t; s=OLD[cid].replace('"en":"","th":"","respell":""','"en":%s,"th":%s,"respell":%s'%tuple(json.dumps(x,ensure_ascii=False) for x in t))
    if lean: s=s.replace('"fill":true,','').replace('"slot":"%s",'%SL[cid],'')
    return s
L0=len(base); print('base',L0,'bank',ft.check_bank(C,L0))
out={}
for opt in ('1A','1B'):
  for lean in (False,True):
    txt=base; per={}
    for cid in OLD:
        assert txt.count(OLD[cid])==1
        f=frag(cid,D[opt][cid],lean); per[cid]=len(f)-len(OLD[cid]); txt=txt.replace(OLD[cid],f)
    meta=False
    for m in ((False,),(True,)) if lean else ((False,),):
      t2=txt
      if m[0]:
        o='"emptySlots":["bh-30","ms-28","ms-29","ms-30"]'; assert t2.count(o)==1; t2=t2.replace(o,'"emptySlots":[]')
        for a,b in (('"writtenCards":207','"writtenCards":211'),('"sayItWritten":33','"sayItWritten":37'),('"personalWritten":76','"personalWritten":80')):
            assert t2.count(a)==1; t2=t2.replace(a,b)
      j=json.loads(t2.split('\n')[426]); cards={c['id']:c for c in j['cards']}
      for cid in OLD: assert cards[cid]['en']==D[opt][cid][0] and cards[cid]['th']==D[opt][cid][1]
      name=f"variant-{opt}-{'lean' if lean else 'min'}{'-meta' if m[0] else ''}"
      p=os.path.join(H,name+'.md'); open(p,'w',encoding='utf-8').write(t2)
      L=len(t2); print(name,'per-card',per,'sum',sum(per.values()),'len',L,'delta',L-L0,'bank_left',ft.check_bank(C,L),'md5',hashlib.md5(t2.encode()).hexdigest()[:8])
for opt in D:
  for cid,(en,th,rs) in D[opt].items(): print(opt,cid,'en',len(en),'th',len(th),'respell',len(rs),'words',len(en.split()),'| bytes th',len(th.encode()))
