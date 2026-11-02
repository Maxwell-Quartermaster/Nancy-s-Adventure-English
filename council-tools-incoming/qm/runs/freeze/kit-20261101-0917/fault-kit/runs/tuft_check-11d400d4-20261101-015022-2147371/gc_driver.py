
import sys, json, importlib.util
sys.dont_write_bytecode = True
s = importlib.util.spec_from_file_location('gc_under_test', sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
res = {}
for p in sys.argv[2:]:
    try: r = m.check(p); res[p] = {'block': bool(r), 'msg': ' ; '.join(map(str, r))[:200] if r else ''}
    except Exception as e: res[p] = {'block': None, 'msg': f'EXCEPTION {e.__class__.__name__}: {e}'}
print('@@JSON@@' + json.dumps(res))
