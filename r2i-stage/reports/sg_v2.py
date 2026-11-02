# informational: run send_guard 80615576 with the staged ground_check v2 (13fc304c) loaded as `ground_check`; no council-tools file is changed
import sys, importlib.util, runpy
spec = importlib.util.spec_from_file_location('ground_check', '/workspace/council-tools/ground-check/ground_check.v2-13fc304c.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); sys.modules['ground_check'] = m
sys.argv = ['/workspace/council-tools/send-guard/send_guard.py'] + sys.argv[1:]
runpy.run_path('/workspace/council-tools/send-guard/send_guard.py', run_name='__main__')
