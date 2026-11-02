# Builds v520/checks_v608.py from v520/checks_v607.py (6e41b1c4, untouched): the v6-07 block keeps verifying the v6-07 files; then the v6-08 block.
import hashlib
SRC='/workspace/v520/checks_v607.py'; DST='/workspace/v520/checks_v608.py'
assert hashlib.md5(open(SRC,'rb').read()).hexdigest()=='6e41b1c46811b442d3ecec468be3abfd'
s=open(SRC,encoding='utf-8').read()
def sub(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
sub("if V>='v6-07':\n    import importlib.util as _iu7,","if V>='v6-07':\n    _V7=V; V='v6-07'   # v6-08+: this block re-verifies the v6-07 files (frozen at the Auditor gate)\n    import importlib.util as _iu7,")
s=s.rstrip('\n')+"\n    V=_V7\n"
# m3 (gate 2b29ce71): a missing tapPrompt/playAgain key fails a check instead of crashing
sub("and _U4['tapPrompt']['en']=='Where is the {word}? Tap it!' and", "and _U4.get('tapPrompt',{}).get('en','')=='Where is the {word}? Tap it!' and")
sub("    _ta=collections.Counter([_U4['tapPrompt']['th'],_U4['playAgain']['th']]); _tg=collections.Counter([_U3['tapPrompt']['th']])",
    "    _ta=collections.Counter([_U4.get('tapPrompt',{}).get('th',''),_U4.get('playAgain',{}).get('th','')]); _tg=collections.Counter([_U3.get('tapPrompt',{}).get('th','')])")
sub("(_tp7['en'],_tp7['th'])==", "(_tp7.get('en',''),_tp7.get('th',''))==")
sub("_C7=json.loads(_r7); _tp7=_C7['uiText']['tapPrompt'];", "_C7=json.loads(_r7); _tp7=_C7['uiText'].get('tapPrompt',{});")
# n1: honour NAE_W
sub("for d_ in ('/workspace/screens-v607/html/',)", "for d_ in (W+'screens-v607/html/',)")
# n2: stale SUPERSEDED reasons now point at the live block of the version under test
sub(" V+' verses byte-identical to v6-04 (and v5-37)':'v6-06 base is v6-05 A2b; verses rechecked byte-identical to v6-05 except the version in the v6-06 block',",
    " V+' verses byte-identical to v6-04 (and v5-37)':'verses are rechecked live against the base of the version under test, in that version block',")
sub(" V+' diff-only: undoing the gate fixes, the title edit (m4':'v6-06 base is v6-05 A2b; diff-only undo to v6-05 A2b byte for byte is checked in the v6-06 block',",
    " V+' diff-only: undoing the gate fixes, the title edit (m4':'the diff-only undo to the base of the version under test is checked live in that version block',")
sub(" V+' generator qm_v605.py':'v6-06 is built by qm_v606.py from v6-05 A2b; its re-run is checked in the v6-06 block',",
    " V+' generator qm_v605.py':'the generator --dry re-run of the version under test is checked live in that version block',")
sub(" V+' cards: Thai identical to v6-04; only version, meta.version and (A2 a) the title differ':'Maxwell t402u: tapPrompt Thai trimmed (แตะเลย! dropped); every other cards change vs v6-06 rechecked in the v6-07 block (T1)',",
    " V+' cards: Thai identical to v6-04; only version, meta.version and (A2 a) the title differ':'cards changes since v6-06 are pinned by the diff-only undo and the cards-block check in each later block',")
# Watchman round (4:08 PM MDT): F2 extends the repeat sentence, F4 rewords tier 1; keep the older checks reading the same rule
sub("'the run repeats those seen longest ago, never twice in one scene.' in _PJ", "'the run repeats those seen longest ago, never twice in one scene' in _PJ")
sub("'If a zone has fewer than 25 `pic` cards, the run repeats those seen longest ago, never twice in one scene.' in _P6", "'If a zone has fewer than 25 `pic` cards, the run repeats those seen longest ago, never twice in one scene' in _P6")
sub("'tier 1 free on opening' in _sp", "('tier 1 free on opening' in _sp or 'tier 1 is hers free when its row opens, no `getFor`' in _sp)")
exec(open('/workspace/v608build/patch_checks_v608_sup.py',encoding='utf-8').read()) if __import__('os').path.exists('/workspace/v608build/patch_checks_v608_sup.py') else None
s+=open('/workspace/v608build/checks_v608_block.py',encoding='utf-8').read()
open(DST,'w',encoding='utf-8').write(s); print(DST, hashlib.md5(s.encode()).hexdigest())
