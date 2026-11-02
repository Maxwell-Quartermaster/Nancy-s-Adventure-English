# Auditor: deep diff of the PASTE JSON line, base vs new; integrity checks
import json, collections
def J(p): return [json.loads(l) for l in open(p,encoding='utf-8') if l.startswith('{"version"')][0]
a=J('p/base.md'); b=J('p/new.md')
out=[]
def walk(x,y,path):
    if type(x)!=type(y): out.append((path,x,y)); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x: out.append((path+'.'+k,'<absent>',y[k]))
            elif k not in y: out.append((path+'.'+k,x[k],'<absent>'))
            else: walk(x[k],y[k],path+'.'+k)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append((path+'[len]',len(x),len(y)))
        for i,(u,v) in enumerate(zip(x,y)): walk(u,v,'%s[%d]'%(path,i))
    elif x!=y: out.append((path,x,y))
walk(a,b,'')
for p,x,y in out: print('CHANGE',p,'|',json.dumps(x,ensure_ascii=False)[:200],'->',json.dumps(y,ensure_ascii=False)[:200])
for k in ('verses','jesusWords','jesusWordsFallback','bosses','boss','guardians'):
    if k in a: print('equal',k,a[k]==b[k])
print('top keys',sorted(b.keys()))
ids=[c['id'] for c in b['cards']]; print('cards',len(ids),'unique',len(set(ids)))
c=collections.Counter(); 
for x in b['cards']:
    if x.get('en'): c['written']+=1
    if x.get('type')=='say-it' and x.get('en'): c['sayItWritten']+=1
    if x.get('personal') and x.get('en'): c['personalWritten']+=1
    if x.get('type')=='say-it': c['sayit']+=1
    if not x.get('en'): c['empty']+=1
print('recount',dict(c)); print('meta', {k:b['meta'].get(k) for k in ('writtenCards','sayItWritten','personalWritten','emptySlots','cardThStatusDefault','needsMaxwell')})
for i in ('bh-30','ms-28','ms-29','ms-30','ms-04','ms-05','ms-06','nm-04'):
    o=[x for x in b['cards'] if x['id']==i]; ob=[x for x in a['cards'] if x['id']==i]
    print(i,'same' if o==ob else 'CHANGED',json.dumps(o[0],ensure_ascii=False)[:400])
print('fill true remaining',[x['id'] for x in b['cards'] if x.get('fill')]); print('slot remaining',[x['id'] for x in b['cards'] if 'slot' in x])
