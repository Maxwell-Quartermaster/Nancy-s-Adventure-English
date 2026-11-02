# Coverage-gap scan for Nancy's game (Maxwell t461u, QM-relayed). Read-only: reads the frozen snap-r2d-2233MDT, renders and council files; writes only this tool's outputs.
import os, re, json, glob, collections
SN = '/workspace/v608build/snap-r2d-2233MDT/'
PASTE = open(SN + 'nancys-adventure-english-v6-08-PASTE.md').read()
CARDS = json.load(open(SN + 'nancys-adventure-english-v6-08-cards.json'))
CHECKS = open(SN + 'checks/checks_v608.py').read().splitlines()
# council text corpus (reports, notes, sheet scripts' captions), skipping frozen copies and big logs
ROOTS = ['/workspace/audit', '/workspace/instructor', '/workspace/watchman', '/workspace/chancellor', '/workspace/decisions', '/workspace/v608build/decisions']
DOCS = []
for r in ROOTS:
    for d, dn, fn in os.walk(r):
      dn[:] = [x for x in dn if not re.match(r'(snap-|live-|_scratch|oc$|node_modules)', x)]
      for p in (os.path.join(d, f) for f in fn):
        if not p.endswith(('.md', '.txt')) or os.path.islink(p) or os.path.getsize(p) > 600_000: continue
        try: DOCS.append((p, open(p, errors='ignore').read()))
        except Exception: pass
WALK = [(p, t) for p, t in DOCS if re.search(r'walk|play.?flow|playthrough|tap.?through|run.?through', p + t[:3000], re.I)]
def pngs(r):
    o = []
    for d, dn, fn in os.walk(r):
        dn[:] = [x for x in dn if not x.startswith(('snap-', 'live-'))]
        o += [f for f in fn if f.endswith('.png')]
    return o
SHOWN = ' '.join(f for r in ['/workspace/v608build/decisions', '/workspace/v608build/round2/sheets', '/workspace/v608build/round2/showcase'] for f in pngs(r)) + ' ' + open(SN + 'showcase/INDEX.md').read() + ' ' + open(SN + 'QUEUE.md').read()
PNG = [os.path.basename(p) for p in glob.glob('/workspace/screens-v608/png/*.png') + glob.glob('/workspace/v608build/scenes/stage/png/*.png') ] + pngs('/workspace/v608build/round2')
def renders(scr):
    if not scr: return 0, {}
    hit = [b for b in PNG if re.match(r'(%s)\b' % scr, b)]
    sz = collections.Counter((re.search(r'(320x568|375x667|375x812|390x844|390check)', b) or [None, '390'])[1].replace('390check', '390').replace('390x844', '390') for b in hit)
    return len(hit), dict(sz)
# areas: (id, name, spec ref, mention regex, screen-file regex, Nancy reaches it on her first run?)
A = [
 ('title', 'Title / sword screen', '6.1', r'sword screen|title screen|\btitle\b', r'01-|52-', 1),
 ('menu', 'Main menu, hub, verse pop-up', '6.2, 15', r'main menu|verse pop|hearth|gemtag|daily gift', r'0[234]|51-', 1),
 ('map', 'Map and zone choosers', '6.3', r'\bmap\b|chooser', r'0[5-9]-|53-', 1),
 ('ask', 'Find-and-tap scenes (asks)', '6.4, 7.1', r'find.and.tap|word meadow|Can you find|ask wording|zone-\w+-ask|tapPrompt', r'1[013]-|3[12]-|zone-|[A-H]-\w|W24', 1),
 ('reveal', 'Reveal screen', '6.5', r'\breveal', r'1[24]-', 1),
 ('sayit', 'Say-it cards', '8', r'say.it|phrase.ask', r'1[56]-|2[01]-|33-|54-', 1),
 ('twoans', 'Two-answer (pray / high five)', '8.1', r'two.answer|high.?five|pray', r'1[789]-', 1),
 ('kitchen', 'Kitchen / Server Talk', '8.2', r'server.talk|kitchen', r'2[012]-', 0),
 ('xp', 'XP, levels, level-up', '9', r'level.?up|\bXP\b', r'23-', 1),
 ('guardian', 'Guardian runs (boss)', '7, 12', r'guardian', r'2[4-8]-|W24', 0),
 ('gifts', 'Reward gifts (verse scroll, weapon)', '9, 15', r'verse.scroll.gift|weapon.gift|new weapon|scroll.reopen', r'29-|30-|44-', 0),
 ('duel', 'Sound Duel', '12', r'sound duel|echo knight', r'3[456]-', 0),
 ('rest', 'Rest screen (victory lap)', '14', r'rest screen|victory lap|restScreen', r'37-', 0),
 ('char', 'Character, gear, themes, gems', '6.6, 11.1', r'character|gear|\bthemes?\b|\bgems?\b', r'3[89]-|4[01]-', 0),
 ('scrolls', 'Scrolls pane', '6.8', r'scrolls? pane|character-scrolls|\bScrolls\b', r'4[23]-', 0),
 ('pantry', 'Golden Pantry / buying', '11.4', r'pantry|getFor|tier.?3|\bbuy', r'45-', 0),
 ('backup', 'Backup view / restore (Maxwell)', '6.7', r'backup|restore', r'4[67]-', 0),
 ('resume', 'Pause, resume, welcome back', '10', r'resume|pause|welcome back|continue after', r'4[89]-', 1),
 ('pwa', 'Home-screen launch, offline, PWA', '2, 4', r'home screen|\bPWA\b|offline|service worker|manifest\.json', r'50-', 1),
 ('streak', 'Day streak', '13', r'streak', None, 0),
 ('unlock', 'Unlocks and reconcile on launch', '11.2, 11.3', r'unlock|reconcile', None, 0),
 ('trophy', 'Trophies', '9, 11', r'troph', None, 0),
 ('personal', 'Personal card slots', '17', r'personal card|personal slot', None, 0),
 ('thaiq', 'Thai Review Queue / NEEDS NANCY flow', '18', r'review queue|thStatus', None, 0),
 ('verses', 'Bible verses and Jesus words', '15', r'\bverses?\b|jesus', r'02b|26-|29-', 1),
 ('audio', 'Audio, speech, pronunciation', '4, 7', r'audio|speech|speechSynthesis|\bTTS\b|pronunc|\bvoice\b|respell', None, 1),
 ('a11y', 'Accessibility: text size, VoiceOver, motion', '2', r'dynamic type|text size|larger text|accessib|VoiceOver|reduce.?motion|aria', None, 1),
 ('rotate', 'Landscape / rotate', '2', r'landscape|rotat|orientation', None, 1),
 ('device', 'Real iPhone / Safari behaviour', '4, 20', r'real (device|phone|iphone)|on (a|her) (real )?(iphone|device)|iPhone check|Safari 1[45]|webkit', None, 1),
 ('sizes', 'Other phone sizes (375, 414/430, Plus/Max)', '2', r'\b414\b|\b430\b|Pro Max|\bPlus\b', None, 1),
 ('endgame', 'End of game / after the last level', '9, 11', r'last level|after the last|end of the game|all zones|finale|max level|level cap', None, 0),
 ('longrun', 'Long-term flow (weeks of play, repetition)', '7, 9', r'week \d|day \d\d|30 days|long session|v608sim|sim\.py|repeats', None, 0),
 ('edge', 'Error and edge states (storage, empty, fallback)', '10, 15', r'localStorage|storage full|quota|fallback|empty entry|corrupt', None, 1),
 ('firstrun', 'First run / onboarding (day 1)', '6.1-6.3, 10', r'first run|first launch|onboard|day.?1\b|day one', r'05-|08-|16-', 1),
]
rows = []
for aid, name, ref, rx, scr, first in A:
    R = re.compile(rx, re.I)
    men = sum(1 for p, t in DOCS if R.search(t)); hits = sum(len(R.findall(t)) for p, t in DOCS)
    chk = sum(1 for l in CHECKS if R.search(l) and re.search(r'print|True|False|ok\(', l))
    wk = sum(1 for p, t in WALK if R.search(t))
    sh = len(R.findall(SHOWN)) + (sum(1 for b in re.findall(r'[\w.-]+\.png', SHOWN) if scr and re.match(r'(%s)' % scr, b)))
    nr, sz = renders(scr); spec = len(R.findall(PASTE))
    rows.append(dict(id=aid, name=name, ref=ref, first=first, spec=spec, files=men, hits=hits, checks=chk, walked=wk, shown=sh, renders=nr, sizes=sz))
# cards: rendered or mentioned at all
ids = [c['id'] for c in CARDS['cards']]
HTML = ' '.join(re.sub(r'data:[^"\')]{200,}', '', open(p, errors='ignore').read()) for p in glob.glob('/workspace/screens-v608/html/*.html') + glob.glob('/workspace/v608build/scenes/stage/html/*.html'))
ALL = ' '.join(t for p, t in DOCS)
words = {c['id']: c['en'] for c in CARDS['cards']}
rendered = [i for i in ids if re.search(r'\b%s\b' % re.escape(words[i]), HTML)]
mentioned = [i for i in ids if i in ALL]
pref = collections.Counter(i.split('-')[0] for i in ids)
pref_r = collections.Counter(i.split('-')[0] for i in rendered); pref_m = collections.Counter(i.split('-')[0] for i in mentioned)
out = dict(rows=rows, docs=len(DOCS), walkdocs=len(WALK), cards=len(ids), rendered=len(rendered), mentioned=len(mentioned),
           by_prefix={k: [pref[k], pref_r[k], pref_m[k]] for k in pref}, zones=[z['key'] for z in CARDS['zones']],
           settings_in_spec=len(re.findall(r'settings', PASTE, re.I)), levels=re.findall(r'[Ll]evel (\d+)', PASTE))
json.dump(out, open('/workspace/council-tools/coverage-data.json', 'w'), ensure_ascii=False, indent=1)
for r in sorted(rows, key=lambda r: r['files']): print(f"{r['id']:9s} spec {r['spec']:3d} files {r['files']:4d} hits {r['hits']:5d} checks {r['checks']:3d} walked {r['walked']:3d} shown {r['shown']:3d} renders {r['renders']:3d} {r['sizes']}")
print('docs', len(DOCS), 'walkdocs', len(WALK), 'cards', len(ids), 'rendered', len(rendered), 'mentioned', len(mentioned)); print(out['by_prefix']); print('settings', out['settings_in_spec'], 'levels', sorted(set(map(int, out['levels']))))
