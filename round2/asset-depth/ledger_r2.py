# Ledger from the post-HOLD bank (staged PASTE 19321a59, 187,446 chars, 754 under 188,200). Every new text below is drafted and len() measured;
# card and SVG sizes come from the staged cards (word card 209 avg, svgNotes ~93 per drawn item incl. its picPlan.svg id).
import json, hashlib
P = open('/workspace/v608build/round2/staged/nancys-adventure-english-v6-08-PASTE.md', encoding='utf-8').read()
BANK = 188200 - len(P); NL = 1   # a new spec list line costs its newline too
J = lambda d: len(json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + 1   # ,"key":{...} in uiText (the comma)
LG_LEAN = ("- **Letter game (Phonics, once per run; Maxwell t430u):** one 3–5 letter `pic` word from the run is spelled: blanks on the card, 6 letter plates "
           "(its letters and 2 decoys); a right letter fills the next blank and the picture, small on the ground, grows a step; a wrong plate just greys, nothing lost. "
           "`uiText.spellIt`. Right = that card's usual reward; grace as 7.1.")
LG_UI = {'"spellIt"': 0}; LG_UI_T = len(',"spellIt":') + J({'en': 'Spell it.', 'th': 'สะกดคำนี้'}) - 1
LG_FULL_ADD = " From that zone's step 3: 8 plates (4 decoys); each right letter says its sound; Sight Words runs get one too."
SP_LEAN = ("- **State pairs (once per run; Maxwell t428u/t429u):** one scene target shows as two of the same object, apart on their surfaces, in two states "
           "(book open 📖 / closed 📕); the card reads `uiText.findState` and she taps the one named. Same reveal and grace.")
SP_UI_T = len(',"findState":') + J({'en': 'Find the {state} {word}.', 'th': 'หา{word}ที่{state}'}) - 1
SP_META = len(',"states":') + J({'open': 'เปิด', 'closed': 'ปิด'}) - 1
SP_FULL_ADD = ", cup full/empty, door open/closed, light on/off, box open/closed, window open/closed"   # into the pair list
SP_FULL_META = len(',"full":"เต็ม","empty":"ว่าง","on":"เปิดอยู่","off":"ปิดอยู่"')
SVG_NOTE = 93; SP_FULL_SVG = 4 * SVG_NOTE   # empty cup, open door, open box, open window (no honest emoji for the second state)
rows = [
 ("Maxwell: letter game (t430u), lean = A picture grows", len(LG_LEAN) + NL + LG_UI_T),
 ("Maxwell: letter game, full = lean + step-3 ramp, letter sounds, Sight Words", len(LG_LEAN) + NL + LG_UI_T + len(LG_FULL_ADD)),
 ("Maxwell: state pairs (t428u/t429u), lean = 1 pair (book 📖/📕), emoji only", len(SP_LEAN) + NL + SP_UI_T + SP_META),
 ("Maxwell: state pairs, full = 6 pairs + 4 drawn second states", len(SP_LEAN) + NL + SP_UI_T + SP_META + len(SP_FULL_ADD) + SP_FULL_META + SP_FULL_SVG),
 ("Maxwell: difficulty ramp (t432u), lean = D2 B", 40),
 ("Maxwell: difficulty ramp, full = D2 C + D1 C", 63 + 128),
]
if __name__ == '__main__':
    print('bank', BANK, 'PASTE', len(P), hashlib.md5(P.encode()).hexdigest())
    for t, c in rows: print(f'{c:5d}  {t}')
    print('LG lean text', len(LG_LEAN), 'ui', LG_UI_T, '| SP lean text', len(SP_LEAN), 'ui', SP_UI_T, 'meta', SP_META, '| full adds', len(LG_FULL_ADD), len(SP_FULL_ADD) + SP_FULL_META + SP_FULL_SVG)
