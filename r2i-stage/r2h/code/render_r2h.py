# r2h renders: one headless Chrome per batch (iframes stacked), then PIL crops. TMPDIR=/dev/shm/qm-r2h; nothing deleted.
import os, sys, json, subprocess, hashlib, uuid
from PIL import Image
import fix_r2h as F
R = '/workspace/v608build/round2/r2h/'; os.makedirs(R+'html', exist_ok=True); os.makedirs(R+'png', exist_ok=True); os.makedirs(R+'batch', exist_ok=True)
S = '/workspace/screens-v608/html/'; HL = '/workspace/v608build/round2/ceiling-cap/home-lake/html/'; SB = '/workspace/v608build/round2/sky-options/B/html/'
def job(tag, src_before, src_after, w, h): return dict(tag=tag, b=src_before, a=src_after, w=w, h=h)
J = []
for n in ('10-word-meadow-scene', '11-word-meadow-scene-right', '12-reveal-right', '13-word-meadow-scene-retry', '15-say-it-sight-words', '23-level-up-reward', '24-guardian-run-entry', '25-guardian-hint-letters',
          '26-guardian-hint-jesus-words', '27-guardian-kneels', '28-guardian-win', '29-verse-scroll-gift', '30-new-weapon-gift', '37-rest-screen', '44-scroll-reopened', '48-continue-after-pause'):
    J.append(job(n+'-390x844', S+n+'.html', S+n+'.html', 390, 844))
    for wh in ('320x568', '375x667'):
        if os.path.exists(S+f'{n}-{wh}.html'): w, h = map(int, wh.split('x')); J.append(job(f'{n}-{wh}', S+f'{n}-{wh}.html', S+f'{n}-{wh}.html', w, h))
for n in ('14-reveal-gentle-retry', '16-say-it-maxwell-says-day1', '17-two-answer-pray-high-five', '18-two-answer-wrong-tap', '19-two-answer-right-done', '21-kitchen-say-it-shown', '22-kitchen-server-talk',
          '32-home-lake-scene', '33-say-it-baby-hospital-reply', '54-phrase-ask-card'):
    J.append(job(n+'-390x844', (HL+n+'-390x844.html') if n[:3] in ('20-', '21-', '22-') else S+n+'.html', S+n+'.html', 390, 844))   # 1B base: before = the 1B trim render (kitchen) or the untrimmed approved render; after = untrimmed + fixes
    if os.path.exists(S+n+'-320x568.html'): J.append(job(n+'-320x568', S+n+'-320x568.html', S+n+'-320x568.html', 320, 568))
J.append(job('zone-lake-ask-320x568', S+'zone-lake-ask-320x568.html', S+'zone-lake-ask-320x568.html', 320, 568))
for wh in ('390x844', '320x568', '375x812'): w, h = map(int, wh.split('x')); J.append(job('zone-forest-ask-'+wh, SB+f'zone-forest-ask-{wh}.html', SB+f'zone-forest-ask-{wh}.html', w, h))
J.append(job('zone-meadow-ask-320x568', S+'zone-meadow-ask-320x568.html', S+'zone-meadow-ask-320x568.html', 320, 568))   # Watchman 2c
for wh in ('390x844', '320x568', '375x812'): w, h = map(int, wh.split('x')); J.append(job('zone-meadow-ask-'+wh+'-skyB', SB+f'zone-meadow-ask-{wh}.html', SB+f'zone-meadow-ask-{wh}.html', w, h))
ST = '/workspace/v608build/scenes/stage/html/'
# (36 jobs dropped: its Echo Knight chip is already there) J.append(job('36-sound-duel-round-done-390x844', S+'36-sound-duel-round-done.html', S+'36-sound-duel-round-done.html', 390, 844)); J.append(job('36-sound-duel-round-done-320x568', S+'36-sound-duel-round-done-320x568.html', S+'36-sound-duel-round-done-320x568.html', 320, 568))
for n in ('A-meadow-evening-pond', 'B-meadow-listen-and-find'):
    for wh in ('390x844', '320x568', '375x667'): w, h = map(int, wh.split('x')); J.append(job(f'stage-{n}-{wh}', ST+f'{n}-{wh}.html', ST+f'{n}-{wh}.html', w, h))
# r2h: the rest of the tour path, rendered here so every sheet tile is an r2h render (fix() is a no-op unless the scene matches)
for n in ('01-title', '02-main-menu-verse-popup', '03-main-menu', '07-map-word-meadow-chooser', '31-golden-fields-scene', '36-sound-duel-round-done', '38-character-gear-mmo-tooltip', '45-character-golden-pantry'):
    J.append(job(n+'-390x844', S+n+'.html', S+n+'.html', 390, 844))
AS_IS = {'W24-walk-B-390x844', 'W24-walk-B-320x568'}   # tile 16/16S approved: rendered as-is, no fix (pixel check vs the approved png)
for t in AS_IS: w, h = map(int, t.rsplit('-', 1)[1].split('x')); J.append(job('stage-' + t, ST + t + '.html', None, w, h))
for n in ('05-map-day1', '08-map-home-lake-chooser-day1', '09-map-later'): J.append(job(n+'-390x844', S+n+'.html', S+n+'.html', 390, 844))
LOG = []
def wr(p, d):
    if not (os.path.exists(p) and open(p).read() == d): open(p, 'w').write(d)
def build():
    out = []
    for j in J:
        if not os.path.exists(j['b']): LOG.append(f"MISSING {j['b']}"); continue
        db = open(j['b']).read(); wr(R+f"html/{j['tag']}-before.html", db); out.append((j['tag']+'-before', j['w'], j['h']))
        if j['a']:
            da, lg = F.fix(open(j['a']).read(), j['tag'], j['w']); LOG.extend(lg)
            if da != db or j['a'] != j['b']: wr(R+f"html/{j['tag']}.html", da); out.append((j['tag'], j['w'], j['h']))
    return out
def shoot(items):
    import cdp_shot as C, sidecar as SC
    ws = C.session()
    for t, w, h in items:
        png = R+f'png/{t}.png'
        js = os.path.splitext(png)[0] + '.json'
        if os.path.exists(png) and os.path.exists(js) and os.path.getmtime(png) > os.path.getmtime(R+f'html/{t}.html'): continue
        SC.shot(ws, R+f'html/{t}.html', R+f'png/{t}.png', w, h); print(t, flush=True)
if __name__ == '__main__':
    items = build(); open(R+'FIXLOG.md', 'w').write('# r2h render fixes\n' + '\n'.join('- '+l for l in LOG) + '\n'); print(len(items), 'pages'); 
    if 'noshot' not in sys.argv: shoot(items)
