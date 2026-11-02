# Quartermaster self-check for hotel-steps drafts (read-only)
import json,re,sys,collections
SRC='src/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md'
B=open(SRC,encoding='utf-8').read(); BL=B.split('\n'); bd=json.loads(BL[426])
def hint_ok(c):
    h=c.get('hint'); 
    if not isinstance(h,list): return True
    exp=re.sub(r"(?<=[A-Za-z])[A-Za-z]",'_',c['en'])
    return h[0]==exp
ok=True
for k in ('1A','1B'):
    fn=f'{k}/nancys-adventure-english-v6-08-1B-v32-hotel{k}-PASTE.md'
    S=open(fn,encoding='utf-8').read(); L=S.split('\n'); d=json.loads(L[426])
    ids=[c['id'] for c in d['cards']]
    chk={}
    chk['json_parses']=True
    chk['lines_equal_count']=len(L)==len(BL)
    chk['diff_lines']=[i+1 for i,(x,y) in enumerate(zip(BL,L)) if x!=y]
    chk['unique_ids']=len(ids)==len(set(ids))
    chk['meta_total']=d['meta']['totalCards']==len(ids)==d['meta']['writtenCards']
    chk['meta_sayit']=d['meta']['sayItTotal']==sum(1 for c in d['cards'] if c.get('type')=='say-it')
    chk['meta_personal']=d['meta']['personalCards']==sum(1 for c in d['cards'] if c.get('personal'))
    chk['verses_equal']=d['verses']==bd['verses']
    chk['jesusWords_equal']=d['jesusWords']==bd['jesusWords'] and d['jesusWordsFallback']==bd['jesusWordsFallback']
    chk['boss_scrolls_equal']=[z['boss']['scroll'] for z in d['zones'] if z.get('boss')]==[z['boss']['scroll'] for z in bd['zones'] if z.get('boss')]
    chk['other_top_keys_equal']=[x for x in d if x not in ('cards','meta') and d[x]!=bd[x]]
    bc={c['id']:c for c in bd['cards']}; nc={c['id']:c for c in d['cards']}
    chk['cards_changed']=[i for i in nc if bc.get(i)!=nc[i]]
    for i in chk['cards_changed']:
        c=nc[i]; w=len(c['en'].split())
        r=[f'{i} words={w}']
        if c.get('choices'):
            r.append('4choices' if len(c['choices'])==4 and len(set(c['choices']))==4 else 'BADchoices')
            r.append('answer_in' if c['en'] in c['choices'] else 'NOanswer')
            r.append('trap_in' if c.get('trap') in c['choices'] else 'NOtrap')
            r.append('hint_ok' if hint_ok(c) else 'HINTbad')
        chk[i]=r
    chk['needsMaxwell']=d['needsMaxwell']
    chk['spec_counts']=[l[:60] for l in L if re.search(r'21[12] cards\*\*|Personal cards:\*\* 8\d|7[45] cards are|of the 21[12] written',l)]
    chk['no_contact_or_inn_name']=not re.search(r'(?i)elk refuge|@\w+\.\w|\b\d{3}[-.]\d{3}[-.]\d{4}\b',S) 
    for a,v in chk.items(): print(k,a,v)
