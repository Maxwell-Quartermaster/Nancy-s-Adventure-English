# **Quartermaster:** html_md5 in r2h sidecars. Kept only if (a) the sidecar was written by sidecar.py at render time (hash of the html actually used), or
# (b) the snapshot MANIFEST.md5 / renders-MANIFEST.md5 (snap-r2h-0021MDT, renders 62e41535) records a hash for that same html path and it equals the value.
# Otherwise the key is removed, so text_check falls back to mtime. Never hashes today's html for a backfill.
import json, os, sys, re, glob
SNAP = '/workspace/v608build/snap-r2h-0021MDT/'; SC = '/workspace/v608build/round2/r2h/sidecar.py'
frozen = {}
for m in ('MANIFEST.md5', 'renders-MANIFEST.md5'):
    for l in open(SNAP + m, encoding='utf-8', errors='replace'):
        g = re.match(r'^([0-9a-f]{32})\s+\*?(.+)$', l.strip())
        if g and g.group(2).endswith('.html') and '/r2h/html/' in g.group(2): frozen.setdefault(os.path.basename(g.group(2)), set()).add(g.group(1))
for root in sys.argv[1:]:
    at_render = kept = blank = 0
    for j in sorted(glob.glob(root + '/png/*.json')):
        d = json.load(open(j)); st = os.stat(j)
        if os.path.getmtime(j) > os.path.getmtime(SC) and root.startswith('/workspace/v608build/round2/r2h'): at_render += 1; continue
        hm = d.get('html_md5'); fz = frozen.get(d['html'], set())
        if hm and hm in fz: kept += 1; continue
        if len(fz) == 1 and not hm: v = next(iter(fz))
        elif hm and fz: v = None
        else: v = None
        new = {k: x for k, x in d.items() if k != 'html_md5'}
        if v:   # frozen hash exists but the earlier backfill had none
            new2 = {}
            for k, x in new.items():
                new2[k] = x
                if k == 'html': new2['html_md5'] = v
            new = new2; kept += 1
        else: blank += 1
        open(j, 'w').write(json.dumps(new, ensure_ascii=False, separators=(',', ':'))); os.utime(j, (st.st_atime, st.st_mtime))
    print(root, 'html_md5 at render time', at_render, 'backfilled from frozen manifest', kept, 'left blank', blank)
