# Re-shoot Watchman's D1/D2 source html (glitch-hunt-v608/decision, read-only) with the staged XP Purple bar; nothing else changes.
import sys, re; sys.path.insert(0, '/workspace/v608build/screens'); sys.argv = ['x']
import play_v608 as P
SRC = '/workspace/watchman/glitch-hunt-v608/decision/'
for f in ('html2/D1-A-cardth', 'html2/D1-B-readfind', 'html/L1-written', 'html/L1-listen', 'html/L3-written', 'html/L3-listen', 'html/L5-written', 'html/L5-listen'):
    s = open(SRC + f + '.html', encoding='utf-8').read(); s2, n = re.subn(r"(width:\d+%;background:)#5DBB63", r"\g<1>#6D3CC9", s); assert n == 1
    nm = f.split('/')[1]; open(nm + '.html', 'w').write(s2); P.S.shot(s2, nm + '.png', 390, 844, 'wrs-' + nm); print(nm)
