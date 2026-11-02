# Auditor: write PASTE copies with one verse field broken (cases/ only)
import json
P='/workspace/v608build/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md'
L=open(P,encoding='utf-8').read().split('\n')
i=[n for n,l in enumerate(L) if l.startswith('{"version"')][0]
def mk(name,f):
    pj=json.loads(L[i]); f(pj); M=list(L); M[i]=json.dumps(pj,ensure_ascii=False)
    open('cases/%s.md'%name,'w',encoding='utf-8').write('\n'.join(M))
def s(path,val):
    def f(pj):
        o=pj
        for k in path[:-1]: o=o[k]
        o[path[-1]]=val
    return f
def d(path):
    def f(pj):
        o=pj
        for k in path[:-1]: o=o[k]
        del o[path[-1]]
    return f
mk('control-redump',lambda pj:None)
mk('wk0-en-blank',s(['verses','weekly',0,'en'],''))
mk('wk3-th-space',s(['verses','weekly',3,'th'],'  '))
mk('wk9-enSource-null',s(['verses','weekly',9,'enSource'],None))
mk('wk0-ref-missing',d(['verses','weekly',0,'ref']))
mk('wk5-thSource-missing',d(['verses','weekly',5,'thSource']))
mk('wk-empty-list',s(['verses','weekly'],[]))
mk('wk-key-missing',d(['verses','weekly']))
mk('wk0-null-entry',s(['verses','weekly',0],None))
mk('rest-ref-blank',s(['verses','rest','ref'],''))
mk('jw0-ref-space',s(['jesusWords',0,'ref'],' '))
mk('rest-th-missing',d(['verses','rest','th']))
