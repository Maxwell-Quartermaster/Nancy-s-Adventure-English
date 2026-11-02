#!/usr/bin/env python3
"""Round 2 STAGED patches on top of snap-1748MDT (read-only). NOT FROZEN, not applied to the build (qm_v608.py) or any snapshot.
Writes patched copies to round2/staged/ and diffs to round2/. Each patch: exact-text edits, each anchor must occur once (else REFUSED).
Base: snap-1748MDT PASTE 95a4d0fce48affdf1541cb862e6d56e5 (187,208), FINAL d467d659, spec 351a4ce6, cards 149dfc59. Verses and title untouched.
Usage: python3 round2.py   (idempotent; never writes into snap-1748MDT)"""
import hashlib, os, sys, difflib, json
SNAP = '/workspace/v608build/snap-1748MDT/'; OUT = '/workspace/v608build/round2/'
MD = ['nancys-adventure-english-v6-08-PASTE.md', 'nancys-adventure-english-FINAL-v6-08.md', 'nancys-adventure-english-v6-08.md']
CARDS = 'nancys-adventure-english-v6-08-cards.json'
BASE = {MD[0]: '95a4d0fce48affdf1541cb862e6d56e5', MD[1]: 'd467d659c009a40edbfb526a295ad1a6', MD[2]: '351a4ce637db58276bacaf55ff59f0e7', CARDS: '149dfc599655daa7fb3f34b458931d6a'}
PATCHES = [
 # P1 Maxwell t440u: ONE ask phrasing for the 44 tapPrompt cards (the :226 B1 filter, exclusion list and colour rule kept; sentence cards keep their own en/th).
 # Thai is Instructor's line, NEEDS NANCY (uiText Thai is a NEEDS NANCY draft by meta.thStatusDefault; nothing marks it otherwise).
 ('maxwell-t440u-ask-phrasing', MD + [CARDS], [
   ('"tapPrompt":{"en":"Where is the {word}?","th":"{word} อยู่ที่ไหน"}', '"tapPrompt":{"en":"Can you find the {word}?","th":"หา {word} เจอไหม"}'),
   ("colors cs-08–cs-15 drop \"the\": 'Where is red?')", "colors cs-08–cs-15 drop \"the\": 'Can you find red?')")]),
 # P2 Maxwell t441u: screen 24 walk B, the walker woven into the park (replaces the top-right plate for a person picture that can stand).
 ('maxwell-t441u-walk24-B', MD, [
   ('a reveal picture (t423u) that can stand is a 64 pt prop on the ground with a contact shadow,',
    'a reveal picture (t423u) that can stand is a 64 pt prop on the ground with a contact shadow (an emoji person: 52 pt, centred between the screen edge and the hero),')]),   # D4: an emoji person
 # P3 Maxwell t439u: one scene layout for every phone, fit to the width (D2, Auditor HOLD e5129779), HUD/card/taps full size (replaces the 320 x 568 hero numbers).
 # ', each on its furniture or ground' is the t426u rule (D3), written in here with P3.
 ('maxwell-t439u-scene-one-layout', MD, [
   ('H = 195 pt tall at 390 × 844 (142 at 320 × 568), feet on the floor or ground at y 700 (446) with', 'H = 195 pt tall at 390 × 844, feet on the floor or ground at y 700 with'),
   ('Objects are drawn in the scene, never on tiles (44 pt+ tap areas, 8 px apart, no overlap).',
    'Objects are drawn in the scene, never on tiles, each on its furniture or ground (44 pt+ tap areas, 8 px apart, no overlap); a scene is one 390 × 844 layout, scaled as one piece to the screen width, bottom pinned, sky cropped; the HUD, card and 44 pt tap areas stay full size.')]),
 # P4 round2b (Auditor 48295eae item 4; Maxwell t445u (QM-relayed) "scale it down" at 320, 390 locked): option B, the crop is capped and the scene shrinks
 # to fit (+79), plus the 16 pt edge clause (+41); then Maxwell t444u (QM-relayed): taller phones trim a room's ceiling to the 320 x 568 framing.
 ('round2b-sky-B-edges-t444u', MD, [
   ('bottom pinned, sky cropped; the HUD, card and 44 pt tap areas stay full size.',
    'bottom pinned, sky cropped; the crop never puts a target under the HUD (the scene shrinks to fit instead); targets keep 16 pt from the screen edge'
    '; on taller phones a room crops its ceiling to the 320 × 568 framing; the HUD, card and 44 pt tap areas stay full size.')]),
 # P5 round2b item 3 (Maxwell t445u (QM-relayed): the banner up top on walk 24): the Guardian name rides the zone-chip line (+50);
 # Auditor eb2674be H2: the PASTE itself makes the walk scene shrink below that banner at 320/375 (+38), not only the render code.
 ('round2b-guardian-chip-t445u', MD, [
   ('the zone chip (`mapLayout` name, en and th).', 'the zone chip (`mapLayout` name, en and th); on guardian runs the zone chip shows `boss.name` and the scene shrinks to sit below it.')]),
 # P6 round2b, a QM-relayed staged fix (council ruling; QM relayed an owner's yes at 8:08 PM MDT, superseding the 7:53 PM MDT "don't change hints on 13 or 25",
 # also QM-relayed; neither is verified): sw-19's hint "t____ /th/" fitted only "think". Auditor eb2674be H1: "run" -> "three" (nm-10's own word, 5 letters, /th/), +2.
 ('round2b-sw19-second-t-choice', MD + [CARDS], [
   ('"choices":["eat","sink","run","think"]', '"choices":["eat","sink","three","think"]')]),
 # P7 Auditor eb2674be H4 (02b longest verse at 320: Thai cut to 1 of 6 lines, breaks :131/:35): the verse text scrolls in its card (+52). Verses unchanged.
 ('auditor-eb2674be-verse-scroll', MD, [
   ('A long verse drops its English to 18 px; Thai stays 17 px+.', 'A long verse drops its English to 18 px; Thai stays 17 px+; still too long, the verse text scrolls in its card.')]),
]
# Trim pick (council 7:56 PM MDT, neutral, for Maxwell; t444u QM-relayed): 1A = all rooms (+68, staged/), 1B = front desk and kitchen only (+89, trim-1B/staged/).
# Auditor eb2674be H3: "night table" named no PASTE scene; the F room is the kitchen meal room ("Kitchen runs use the home room set for a meal"), so 1B says kitchen (-4).
TRIM = os.environ.get('NAE_TRIM', '1A')
if TRIM == '1B':
    PATCHES = [(n, f, [(o, x.replace('; on taller phones a room crops its ceiling to the 320 × 568 framing', '; on taller phones the front desk and kitchen crop their ceiling to the 320 × 568 framing')) for o, x in e]) for n, f, e in PATCHES]
    OUT = OUT + 'trim-1B/'
def md5(t): return hashlib.md5(t.encode()).hexdigest()
def main():
    rc = 0; text = {}
    for f in MD + [CARDS]:
        t = open(SNAP + f, encoding='utf-8').read()
        if md5(t) != BASE[f]: print(f, 'REFUSED: base md5', md5(t)); return 2
        text[f] = t
    led = []
    for name, files, edits in PATCHES:
        d0 = len(text[MD[0]])
        for f in files:
            for o, n in edits:
                c = text[f].count(o)
                if c == 0 and (f == CARDS or (f != MD[0] and o.startswith('"'))): continue   # the uiText json is in the PASTE and cards.json only; the :226 wording in the md files only
                if c != 1: print(name, f, 'REFUSED: anchor count', c, o[:70]); rc = 2; continue
                text[f] = text[f].replace(o, n)
        led.append((name, len(text[MD[0]]) - d0, len(text[MD[0]])))
    # D1 (Auditor HOLD): the spec :417 banked line states the real numbers after all edits (spec only; same digit count, 0 chars)
    n = len(text[MD[0]]); o = 'Banked in v6-08: 992 chars under 188,200 (PASTE 187,208 chars)'; nw = f'Banked in v6-08: {188200 - n} chars under 188,200 (PASTE {n:,} chars)'
    assert len(nw) == len(o) and text[MD[2]].count(o) == 1, nw
    text[MD[2]] = text[MD[2]].replace(o, nw); led.append(('auditor-D1-banked-line (spec only)', 0, n))
    os.makedirs(OUT + 'staged', exist_ok=True)
    for f in MD + [CARDS]: open(OUT + 'staged/' + f, 'w', encoding='utf-8').write(text[f])
    j = json.loads(text[CARDS]); assert j['uiText']['tapPrompt'] == {'en': 'Can you find the {word}?', 'th': 'หา {word} เจอไหม'}, j['uiText']['tapPrompt']
    for f, tag in ((MD[0], 'PASTE'), (MD[2], 'spec'), (CARDS, 'cards')):
        a = open(SNAP + f, encoding='utf-8').read().splitlines(True); b = text[f].splitlines(True)
        open(OUT + f'diff-{tag}-snap-1748MDT-to-round2.diff', 'w', encoding='utf-8').writelines(difflib.unified_diff(a, b, 'snap-1748MDT/' + f, 'round2/staged/' + f, n=0))
    print('PASTE snap-1748MDT 187,208')
    for n, d, t in led: print(f'{n}: {d:+d} -> {t:,}')
    print('PASTE', len(text[MD[0]]), md5(text[MD[0]]), 'banked left', 188200 - len(text[MD[0]]))
    for f in MD[1:] + [CARDS]: print(f, md5(text[f])[:8], len(text[f]))
    return rc
if __name__ == '__main__': sys.exit(main())
