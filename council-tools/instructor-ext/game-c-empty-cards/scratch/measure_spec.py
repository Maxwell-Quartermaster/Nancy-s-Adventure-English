#!/usr/bin/env python3
"""Instructor scratch: spec-prose follow-on edits (QM's call) on top of the lean-meta variants. Same metric as fit_table."""
import sys,os,json,hashlib
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'council-tools','fit-table'))
import fit_table as ft
C=dict(json.load(open(os.path.join(H,'council-tools','fit-table','costs.json'))),bank=None)
E=[('74 cards are `type: "say-it"`, `mode: "english-first"`: 70 written plus the 4 empty slots (section 17).','74 cards are `type: "say-it"`, `mode: "english-first"`.'),
 ('- **211 cards** in `cards.json`: 207 written plus 4 empty personal slots. Format:','- **211 cards** in `cards.json`. Format:'),
 (', personal, slot?, prompts?',', personal, prompts?'),
 (' `slot` names an empty slot\'s topic.',''),
 ('Four empty say-it cards wait for Maxwell (`fill:true`, `personal:true`, empty `en`, `th`, `respell`), skipped until written, then sorted first:','Four personal say-it cards, Instructor drafts for Maxwell to confirm or edit, sorted first:')]
base=len(open(os.path.join(H,'PASTE-317e91ce-copy.md'),encoding='utf-8').read())
for v in ('variant-1A-lean-meta','variant-1B-lean-meta'):
    t=open(os.path.join(H,v+'.md'),encoding='utf-8').read(); L1=len(t)
    for a,b in E:
        assert t.count(a)==1,(v,a); t=t.replace(a,b); print(' edit',len(b)-len(a),'|',a[:60])
    json.loads(t.split('\n')[426]); p=os.path.join(H,v+'-spec.md'); open(p,'w',encoding='utf-8').write(t)
    print(v+'-spec','len',len(t),'delta vs 317e91ce',len(t)-base,'spec-only',len(t)-L1,'bank_left',ft.check_bank(C,len(t)),'md5',hashlib.md5(t.encode()).hexdigest()[:8])
