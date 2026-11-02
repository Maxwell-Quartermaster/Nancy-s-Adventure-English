# Auditor r2b-2051 occlusion (4) / council 9:19 PM MDT: on 52-title-night the "Good night!" banner text was flagged as covered by the sky.
# The png shows it (svg <text> is not hit-testable, so its own flag path is what elementsFromPoint returns). Fix, 0 chars, picture unchanged:
# the plane banner group (tow line, flag, text) is one named item, data-name='night-banner', so the text and its own flag count as one.
import re, sys
f = '/workspace/screens-v608/html/52-title-night.html'; s = open(f).read()
if "data-name='night-banner'" not in s:
  k = s.index("<text id='gE'"); depth = 0; j = k
  for m in reversed(list(re.finditer(r'<g\b[^>]*>|</g>', s[:k]))):
    if m.group(0) == '</g>': depth += 1
    elif depth: depth -= 1
    else: j = m.start(); break
  s = s[:j] + s[j:].replace('<g', "<g data-name='night-banner'", 1)
  open(f, 'w').write(s); print('named the banner group at', j)
# Step 2: the hit-test showed a full-screen night tint (class nt, gradient #nf, 0 opacity above 36 % of the height) drawn over the banner.
# Move the banner group after that tint at the same nesting level: the banner paints last; the picture is pixel-identical (the tint is clear there).
s = open(f).read()
if s.index("<g data-name='night-banner'") < s.index("fill='url(#nf)'"):
    j = s.index("<g data-name='night-banner'"); d = 0
    for m in re.finditer(r'<g\b[^>]*>|</g>', s[j:]):
        d += 1 if m.group(0) != '</g>' else -1
        if d == 0: e = j + m.end(); break
    grp = s[j:e]; s = s[:j] + s[e:]
    t = s.index("<path class='nt' d='M-20 0h430v844H-20z' fill='url(#nf)' stroke='none'/>"); t = s.index('/>', t) + 2
    s = s[:t] + grp + s[t:]; open(f, 'w').write(s); print('banner group moved above the night tint')
