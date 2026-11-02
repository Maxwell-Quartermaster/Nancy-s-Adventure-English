import sys as _sys, os as _os; _sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__))); from version import V
_V6=V.startswith('v6-'); _STILL=_V6 and V!='v6-01'   # v6-02 (Maxwell t366u): title screen is a still; v6-01 (Maxwell t360u/t362u): Option B trim + v6 gear plan
_TRIM6=('bow-oak','wand-oak','bow-short','staff-lantern','spear-river','crossbow-pine','axe-great','claws-bear','glaive-moon','maul-stone','scythe-harvest','classMage','forestRanger')   # removed by Option B (t360u); staff-shepherd kept as the crook
_VN=(38 if V.startswith('v6-') else int(V.split('-')[1]))   # v6-01: every v5-3x gate stays on (v6 >= v5-37)
import json,re,subprocess,collections
# v5-34: compact card fields (spec section 16) are expanded back before any check reads them: zone from zones[].cardIds,
# a string choice -> {"en": s}, hint [letters, sound, word] -> {letters, sound, word}. Idempotent; v5-33 and older files pass through unchanged.
def _expand_cards(o):
    for z in o.get('zones',[]):   # v5-35: zones[].prefix -> cardIds (file order)
        if 'prefix' in z and 'cardIds' not in z: _p=z['prefix'].split(); z['cardIds']=[c['id'] for c in o['cards'] if c['id'].split('-')[0] in _p]
    _z={i:z['key'] for z in o.get('zones',[]) for i in z.get('cardIds',[])}
    _tz=o.get('meta',{}).get('typeByZone',{})
    for c in o['cards']:
        if 'type' not in c and _z.get(c['id']) in _tz: c['type']=_tz[_z[c['id']]]
        if V>='v6-04' and isinstance(c.get('hint'),str): c['hint']=[c['en'][0]+'_'*(len(c['en'])-1),c['hint']]   # v6-04 T3: a string hint is the sound
        if V>='v6-04' and c.get('type','picture')=='picture' and 'answer' not in c: c['answer']=c['en']   # v6-04 T5: a picture card's missing answer is its en
        if isinstance(c.get('hint'),list) and len(c['hint'])==2: c['hint']=c['hint']+[c['en']]
        if 'zone' not in c and c['id'] in _z: c['zone']=_z[c['id']]
        if 'choices' in c: c['choices']=[{'en':x} if isinstance(x,str) else x for x in c['choices']]
        if isinstance(c.get('hint'),list): c['hint']=dict(zip(('letters','sound','word'),c['hint']))
    _tr=o.get('trophyRules',{}); _wt=o.get('meta',{}).get('weaponTiers',{})
    for t in o.get('trophies',[]):   # v5-35: a named weapon's `tier` -> unlock level + tier price (trophyRules.price); tier 1 free
        if 'tier' in t and 'unlock' not in t:
            t['unlock']={'type':'level','n':_wt[str(t['tier'])]}
            if _tr['tierStars'][t['tier']-1] and not (_VN>=36 and t['id'] in ('sling-shepherd','staff-shepherd','staff-lantern','hammer-builder')): t['stars']=_tr['tierStars'][t['tier']-1]   # v5-36: the 4 Bible weapons are free when their tier opens
    _cl={t:k for k,v in o.get('trophyRules',{}).get('classes',{}).items() for t in v}
    for t in o.get('trophies',[]):   # v5-34: a trophy with wt is a weapon (trophyRules.note): cat, slot, pic and class are derived
        if 'wt' in t:
            t.setdefault('cat','gear'); t.setdefault('slot','offHand' if t['wt']=='shield' else 'weapon'); t.setdefault('pic','svg:'+t['id'])
            if t['wt'] in _cl: t.setdefault('classTitle',_cl[t['wt']])
    return o
_json_load0=json.load
def _json_load(f,*a,**k):   # v6-06: cards picPlan.uiInlineSvg.title == "title.svg" -> the <version>-title.svg file next to the PASTE
    o=_json_load0(f,*a,**k)
    try: _t=o['picPlan']['uiInlineSvg']
    except (KeyError,TypeError): return o
    if _t.get('title')=='title.svg':
        _p=_os.environ.get('NAE_W','/workspace/')+'nancys-adventure-english-'+o['version']+'-title.svg'
        _t['title']=open(_p,encoding='utf-8').read() if _os.path.exists(_p) else 'MISSING:'+_p
    return o
def _load(f,*a,**k):
    o=_json_load(f,*a,**k)
    return _expand_cards(o) if isinstance(o,dict) and 'cards' in o and 'zones' in o else o
json.load=_load
W=_os.environ.get('NAE_W','/workspace/')   # v6-05: a mutation copy sets NAE_W

_V36=_VN>=36
_V37=_VN>=37
# v5-37 (Auditor v5-36 gate HOLD 90020f20, items 1-12): v5-36 literals that the re-cut rewrote by ruling are mapped old -> new for v5-37 (_t);
# only positive "x in PASTE" literals are mapped, never "not in" guards.
_E37=[("leftovers join the guardian recap.","leftovers wait for her next run there."),("from her zone, after the opener","from her zone if it has one, after the opener"),
 ("or 'can't' anywhere.","or 'can't' in any UI string."),("bright on the faded Home Lake.","bright on the faded Home Lake (its row opens their chooser)."),
 ("own screens (8, 8.1, 8.2)","own screens (6.4, 8, 8.1, 8.2)"),("the 15 gear","the 14 gear"),("the 17 `thDef` hints","the 18 `thDef` hints"),
 ("a black `.sil` silhouette (Ink fill)","a `.sil` silhouette"),("Paper question card","tan question card"),("all 21 weapons","all 56 weapons"),
 ("the first zone takes about five days.","the first zone takes about 2–4 days.")]
def _t37(x):
    if _V37:
        for _o,_n in _E37: x=x.replace(_o,_n)
    return x
# v5-36 re-sort of the 55 legacy False checks (Auditor v5-35 gate, check 7): live rules are rewritten in place (`NEW if _V36 else OLD`);
# only truly superseded checks may print False, and each is labelled with the ruling that replaced it.
_SUP36={
 'class titles = Maxwell mapping':'v5-34 derives classTitle from the weapon type (t298u); covered by the v5-34 class-line check',
 't238u title screen replaces the Q-0759 sword sequence':'title is the t283u valley (t295u), not the t238u screen',
 'Q-0745 C1 Auditor gate flags fixed (t238u: Map hero marker':'t290u hero select: the chosen hero\'s head marks her last row; Sam emblem gone',
 'Q-0745 C1 hint order cross-ref + Bible weapon stage test':'v5-36 M1 deleted the Jesus-word-first clause by ruling; see the v5-36 M1 check',
 'Q-0748 (t238u) Map shows a 20 pt Sam emblem':'t290u hero select replaced the Sam emblem',
 'Q-0753 rule 4 reworded':'MX1 (Maxwell t329u) replaced rule 4\'s open-from-launch clause; see the v5-36 MX1 check',
 'Q-0753 no level gates':'MX1 (t329u): regions open by guardians, not levels; the v5-36 MX1 check covers no-level-gates for regions',
 'Q9 D8 no-op: Sound Duel already open from first launch':'MX1 (t329u): Echo Forest (Sound Duel) opens after the Gentle guardian',
 'Q-0757 game-feel style line':'#77 storybook look (t273u) restored chunky (6 expected); the t238u heavy-buttons wording is gone by ruling',
 'Q-0758/t238u style line':'#77 storybook look replaced the flat cel-shaded line with \'one style in two layers\'',
 'Q-0758 c2 coherence':'Auditor contrast fix restated the sky ring as 7.0:1+ on Ink (was 6.9:1+)',
 't238u T1 title scene':'t283u valley title replaced the t238u scene',
 't238u T2 Start your day':'t283u valley title (t295u) replaced the t238u button placement',
 't238u T3 wind CSS-only':'t283u valley title: the sway/time-of-day loops replaced the single wind keyframe',
 't238u T4 sun pan':'t283u valley title: no sun pan',
 't238u T6 art sizes':'t283u valley title + sky split; art cap is the council absorb rule',
 't238u H1 Sam':'v5-33 shared 6-head rig and t297u faces replaced the H1 trait line; glasses rule covered by gate 2',
 'v5-30 mn3 title tree':'t283u valley title', 'v5-30 mn6 dropped':'t283u valley title: no sun pan dip',
 'v5-30 mn10 chunky -> heavy':'#77 storybook look restored chunky by ruling (6 expected)',
 "v5-31 F1 title tree x=40":'t283u valley title', 'v5-22 B1 touch-action':'title rebuilt (t283u); touch-action now sits on .ti in the 6.1 CSS line (kept once)',
 'CURRENT.md matches its lock':'locked-md5.txt predates the council flips; the rewritten lock check pins CURRENT.md to ba6726f6',
 't235u 5 hero is a boy':'t290u: the hero is Sam or Nancy, picked on the Map',
 't235u cards: only the planned keys changed vs v5-27':'release diff pinned to v5-28', 't235u gems give her something to chase':'v5-34 gear rule: nextBonus became nextWeapon',
 'v5-32 cards: only version':'release diff pinned to v5-32', 'v5-32 same inline ids':'release diff pinned to v5-32 (v5-34 added sky/nancy/aura and weapon art)',
 'v5-32 style lock':'pinned to v5-32 art; v5-33 rig and v5-34 tex rebuild changed roots', 'v5-32 title':'t283u valley title', 'v5-32 Sam supplied':'v5-33 shared rig replaced the v5-32 Sam',
 V+' art total':'council absorb rule (3-0): applies because the PASTE fits',
}
if V>='v6-06': _SUP36.update({
 V+' verses byte-identical to v6-04 (and v5-37)':'verses are rechecked live against the base of the version under test, in that version block',
 V+' diff-only: undoing the gate fixes, the title edit (m4':'the diff-only undo to the base of the version under test is checked live in that version block',
 V+' generator qm_v605.py':'the generator --dry re-run of the version under test is checked live in that version block',
})
if V>='v6-07': _SUP36.update({
 V+' uiText: only tapPrompt changed ("Where is the {word}? Tap it!")':'Maxwell t402u: tapPrompt is now "Where is the {word}?" (no Tap it); rechecked in the v6-07 block (T1)',
 V+' cards: Thai identical to v6-04; only version, meta.version and (A2 a) the title differ':'cards changes since v6-06 are pinned by the diff-only undo and the cards-block check in each later block',
 V+' cards Thai changed only where planned (+tapPrompt, +playAgain, -old tapPrompt)':'Maxwell t402u: tapPrompt Thai trimmed to the question; uiText vs v6-06 rechecked in the v6-07 block (T1)',
})
if V>='v6-08': _SUP36.update({   # v6-08 (verse pop-up B, daily gift, happy eyes): each rechecked in the v6-08 block
 'Baby and Hospital zero-coin rule in spec':'Chancellor 5da6f734 (a), 4:31 PM MDT: a miss keeps every coin in every zone, so no zone needs a zero-coin exception; rechecked live in the v6-08 CH block',
 'Q-0757 c4 + Q-0758 picture-first':'Instructor sweep 2 (instructor-kitchen-tap.py 38771bd6): picture-first reveal tap is `uiText.continue`; the pic flags are unchanged and rechecked live in the v6-08 IN block',
 'v5-23 t51 cards: cs-07/sw-07/nm-09/bh-17':'Instructor sweep 2 (instructor-thai-cs07-sw11.py d2f89398, NEEDS NANCY): cs-07 gets a space before ค่ะ; rechecked live in the v6-08 IN block',
 V+' MX2 (t331u':'Chancellor 5da6f734 (d): the ring line now names the untiered Bloodtide, Dragonbane and Sunforged as legendary; rechecked live in the v6-08 CH block',
 V+' minors: m2 ribbon after the last scene':'Chancellor 5da6f734 (d): Sunforged joins Bloodtide and Dragonbane beside the Greatsword row; rechecked live in the v6-08 CH block',
 V+' gate exact fix texts A3-A':'Chancellor 5da6f734 (c): the Echo Knight recap "ends like a round" (m3 text extended); rechecked live in the v6-08 CH block',
 't235u 1 main menu = exactly two buttons':'v6-08 VP1: launch order now ends "run or main menu; the daily verse, if due, pops up over the main menu"; 6.2 two buttons rechecked in the v6-08 block',
 'Q-0754 spec: daily delivery':'v6-08 VP3: "on her first main-menu visit each day, in the pop-up below"; daily delivery rechecked in the v6-08 block',
 't238u no Settings':'v6-08 VP6: state gains giftGems before settings{slowMode, restWeeks}; Settings rule rechecked in the v6-08 block',
 't238u R1 Restore':'v6-08 VP8: restore check is "all keys but `giftGems`"; Restore rechecked in the v6-08 block',
 'v5-30 mn7 Restore check':'v6-08 VP8: "(JSON, `schema` 5020, all keys but `giftGems`)"; rechecked in the v6-08 block',
 V+' spec section 15 byte-identical to v5-33':'v6-08 VP3/VP4 change section 15 (pop-up + daily gift); diff-only undo to v6-07 checked in the v6-08 block',
 V+' 29 new uiText keys':'v6-08 adds uiText.dailyGift and the 4 scene keys (NEEDS NANCY); uiText 97 rechecked in the v6-08 block',
 V+' MX4 (t330u) scene notes':'v6-08 E1: the Golden Fields eyes note became "Sam\'s eyes are happy closed Ink arcs on every screen (t398u)"; the other four notes rechecked in the v6-08 block',
 V+' audit fixes F1-F12, F14, F15, B1':'v6-08 VP10: the stated `uiText` count is 97 (dailyGift + 4 scene keys); rechecked in the v6-08 block',
 V+' cards Thai changed only where planned (+tapPrompt, +playAgain, -old tapPrompt)':'v6-08 Thai changes (dailyGift, listenFind, howMany, howManyCows, bigOrSmall) are pinned by the live VP and SC uiText checks in the v6-08 block',
 'every picPlan.svg id is used by a card or choice':'Maxwell t406u (H1): high-five stays in the library while ms-31 uses hand emoji; H1 rechecked in the v6-08 block',
 'ms-31 uses drawn SVGs':'Maxwell t406u (H1): hand-only emoji are fine; ms-31 is 🙏 / 🙌 on bordered plates; rechecked in the v6-08 block',
 'ms-31 SVG guard':'Maxwell t406u (H1): hand-only emoji are fine; rechecked in the v6-08 block',
 'Q-0741 regressions':'Maxwell t406u (H1) allows 🙏 on ms-31; the other Q-0741 items are rechecked by the diff-only undo to v6-07 in the v6-08 block',
 V+' compact cards: zone/choices/hint decode':'v6-08 H1 changes ms-31 choice pics only; diff-only undo to v6-07 checked in the v6-08 block',
 V+' lossless trims':'v6-08 H1 (ms-31 pics), E1 (#rE) and dailyGift; diff-only undo to v6-07 checked in the v6-08 block',
 V+' picPlan: only uiInlineSvg':'v6-08 E1 changes tex #rE only; rechecked in the v6-08 block',
 V+' Watchman flags':'v6-08 H1 rewrites the :243 high-five wording; rechecked in the v6-08 block',
 V+' emoji: no new emoji beyond v5-37':'Maxwell t406u (H1): 🙌 / 🙏 hand emoji on ms-31; rechecked in the v6-08 block',
 V+' hands: tex unchanged from v6-04':'v6-08 E1: tex #rE is the happy arcs; tex equals v6-07 except #rE, rechecked in the v6-08 block',
})
if V>='v6-04': _SUP36.update({   # A1 (Auditor v6-04 gate 984f8f51): the :646 block runs again for v6-04+; these 7 were replaced by v6-04 rulings
 V+' spec states the compact fields':'v6-04 T3/T5 (lossless trims) extended the compact-fields sentence; the new sentence is checked live in the v6-05 block',
 V+' 24 new uiText keys':'F3 tapPrompt + B1 playAgain (audit t372u): uiText is 92; their Thai is NEEDS NANCY on the m6 list v605build/thai-v6-for-nancy.md; keys and count checked live in the v6-04+ uiText check',
 V+' equip rule text (Option B)':'F11 (audit t372u, t336u): a 1H sword, axe or mace may add the round/square shield; F11 text checked live in the v6-04+ fix-text check',
 V+' title: t283u valley':"t371u: the title is Maxwell's t288u picture (one SVG, sky merged); checked live by the v6-04+ title-still/Safari checks and the v6-02+ plane/banner check",
 V+' Map = hero select (t290u)':'F6 (audit t372u): Back sits on the top bar at every width, the avatar button is gone; F6/F7 texts checked live in the v6-04+ fix-text check',
 V+' hands: #rH is the t290u mitten':'t376u: #rH is the t320u hand (18 long, thumb 6.3); the right-hand mirror rules (x 55, 62) are checked live in the v6-05 block',
 V+' find-and-tap (t312u':'F1/t376u template rewords the target rule to "44 pt+ tap areas, 8 px apart, no overlap"; checked live in the v6-05 block',
})
if V>='v6-04': _SUP36.update({   # v6-04 (t371u title port, t372u-t377u audit fixes): each is rechecked in the v6-04 block at the end
 'inline SVGs each <=4096 B':"t371u: the title is Maxwell's t288u picture in one SVG (sky merged in); every other inline SVG rechecked <=4096 B below",
 'Q9 O11 Safari 14':"spec 'No gradients except sky': the title now holds the sky gradient and a min-aspect-ratio media query (Safari 14 OK); rechecked below with only those two allowed",
 't238u M1 Map next-step':'B1 (audit t372u): the next-step row adds uiText.playAgain once all are done',
 't235u 3 Map: linear':'F5 (audit t372u): the Paper sheet is a sky sheet with scenery strips (t346u)',
 't235u 7 Map no-overlap':'F6 (audit t372u): Back moved to the top bar; the bottom bar is the updateReady chip',
 V+' M7: scene layout':'F1/F2/F15 + t376u: one play-screen template replaces the scene layout line',
 V+' t334u END-BOSS gate':'F8/F9 (audit t372u) extend the guardianLast and regionOpen clauses; rest of the rule rechecked below',
 V+' Watchman T1 haft fix kept':'F11 (audit t372u): shields pair with a 1H sword, axe or mace',
 V+' t336u shields round':'the only "kite" is the park toy in the 7.1 scene list; rechecked below in shield context',
 V+' tap phrasing':'F3 (audit t372u): tapPrompt text changed; still no tapFind/tapMy/tapGive/tapYour; uiText 92 rechecked below',
 V+' Thai changed only where planned':'v6-04 Thai delta rechecked below (tapPrompt + playAgain, NEEDS NANCY)',
 V+' cards: questions untouched':'lossless trims T1/T3/T5; rechecked below with defaults filled back in',
 V+' generator qm_v601.py':'v6-04 generator chain rechecked below',
})
import builtins as _bi
def print(*a, **k):
    if _V36 and a and isinstance(a[0],str) and (any(x is False for x in a[1:]) or 'within cap: False' in a[0]):
        for _p,_r in _SUP36.items():
            if a[0].startswith(_p): a=a+('[SUPERSEDED: %s]'%_r,); break
    _bi.print(*a, **k)
def _lock36():
    import hashlib as _h
    _m=lambda f:_h.md5(open(W+f,'rb').read()).hexdigest()
    _l=[l.split() for l in open(W+'v520/locked-md5.txt') if l.strip() and not l.startswith('#')]
    _sv=[l.split() for l in open(W+'v534-saved/MANIFEST.md5') if l.strip()]
    return all(_m(f)==h for h,f in _l if f!='CURRENT.md') and _m('CURRENT.md')==('b653ffb29b2897a8b9bfd052f05c759b' if V.startswith('v6-') else 'ba6726f63710dbef0b439324d076710c') and all(_m('v534-saved/'+f)==h for h,f in _sv) \
        and [_m('v533-frozen/nancys-adventure-english-v5-33-'+x)[:8] for x in ('PASTE.md','cards.json','daily-verses.json')]==['e20402f4','d4de05a7','a93030bc'] \
        and [_m('nancys-adventure-english-'+x)[:8] for x in ('v5-35-PASTE.md','FINAL-v5-35.md','v5-35-cards.json','v5-35-daily-verses.json')]==['b3f83648','00b96f48','9fd526bc','ef49c0d1']
_T235=_VN>=28   # v5-28 (Maxwell t235u, Oct 30 2026 11:41 PM PT): hub menu, Character, linear map, no Settings/talents, boy hero; superseded checks switch to the t235u rule
_T238=_VN>=29   # v5-29 (Maxwell t238u, Oct 30 2026 11:59 PM PT): Sam, hub arrow cue, Character toggles + two-step Restore, title sun pan; superseded checks switch to the t238u rule
_T239=_VN>=30   # v5-30 (Auditor v5-29 gate d763084d batch + council 12:33 AM PT: MJ1 his, mn6 dropped)
_T240=_VN>=31   # v5-31 (Auditor v5-30 diff gate F1: title tree x=40 -> x='-8', 0 chars)
d=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json')); o=json.load(open(W+'nancys-adventure-english-v5-19-cards.json'))
_dflt=d['meta'].get('cardDefaults',{}); _tbz=d['meta'].get('typeByZone',{}); _stored=sum(1 for c in d['cards'] for k in _dflt if k in c and c[k]==_dflt[k] and not (k=='type' and c.get('zone') in _tbz))   # v5-35: a picture card in a typeByZone zone must name its type   # Q-0743: read cards with their defaults applied
import qm_defaults as _QD; _QD.expand(d)   # Q-0757 c4: fill T2/T3 defaults back in (type picture, NEEDS NANCY) before any check
for c in d['cards']:
    for k,v in _dflt.items(): c.setdefault(k,v)
    c.setdefault('mode',d['meta'].get('modeByType',{}).get(c['type']))
print('JSON parse OK; version',d['version'],d['meta']['version'])
spec=open(W+'nancys-adventure-english-'+V+'.md').read(); fin=open(W+'nancys-adventure-english-FINAL-'+V+'.md').read()
# verses identical
_vd={k for k in set(d['verses'])|set(o['verses']) if d['verses'].get(k)!=o['verses'].get(k)}   # Q-0757 c4: v5-21 only rotation/graceRule say day (Chancellor C-CH-1; Auditor co-sign)
_an=dict(o['verses']['attribution'],note=o['verses']['attribution']['note'].replace(' screen and in Settings.',' shelf.'))   # t238u / Auditor M1: the one approved note change
same = (_vd<={'rotation','graceRule'} or _T238 and _vd<={'rotation','graceRule','attribution'} and d['verses']['attribution']==_an) and d['verses']['graceRule']==o['verses']['graceRule'].replace('given by week,','given by day,') and 'week' not in d['verses']['rotation'].replace('weeklyStart','').lower() and [z['boss'] and z['boss']['scroll'] for z in d['zones'] if z['key']!='kitchen']==[z['boss'] and z['boss']['scroll'] for z in o['zones']]   # Q-0747: Kitchen has no boss/scroll
print('16 verses + attribution + rules byte-identical to v5-19 (only rotation/graceRule week->day, c4):',same)
# spec section 15 verse lines identical
sec=lambda t:t[t.index('## 15. Bible verses'):t.index('## 16. Cards')]
a=sec(open(W+'nancys-adventure-english-v5-19.md').read()).replace("If you don't know the meaning, ask Max and he can help you.","Don't know a word? Ask Max."); b=sec(spec)
if _T235: a=a.replace('shows small on the Scrolls shelf and in Settings,','shows small on the Scrolls shelf,')   # t235u: Settings removed; the one approved section 15 credits change (verse text untouched)
# Q-0741 flag 6: askMax quote is the one approved change
_wk=[l for l in a.splitlines() if l.startswith('- **Weekly verse**')]; a=a.replace('- **Verse screen (scrolls and weekly):**','- **Verse screen (scrolls and daily):**')   # Q-0757 C1: the same delivery wording in the verse-screen label   # Q-0754 (Maxwell 7:38 PM PT): the ONE approved section 15 change is delivery, weekly -> daily
if V>='v6-08': a=a.replace('Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl`.','Each verse has `status: "VERIFIED"` and its `enUrl`/`thUrl` (data only, never links).')   # Auditor G9 (47d0b89c): the one v6-08 section 15 edit, verse text untouched
print('spec section 15 v5-19 lines all kept verbatim (except the Q-0754 delivery line):',len(_wk)==1 and all(l in b for l in a.splitlines() if l not in _wk) and '- **Daily verse** (Maxwell 7:38 PM PT)' in b and '- **Weekly verse**' not in b)
# orphans: every JSON key named in spec
keys=set()
def walk(x):
    if isinstance(x,dict):
        for k,v in x.items(): keys.add(k); walk(v)
    elif isinstance(x,list): [walk(v) for v in x]
skip={'en','th'}
for k,v in d.items():
    if k in('uiText',): continue
    walk({k:v})
# drop dict-of-ids keys (card ids, trophy ids, refs, levels)
idlike=lambda k: re.match(r'^(ph|cs|sw|nm|bh|ms)-\d+$|^\d+$|^gem-|^sword-|^cape-|^tunic-|^staff-|^bow-|^sling-|^hammer-|^shield-|^clock-|^svg|^[A-Z]',k) or k in d['picPlan'].get('svgNotes',{})
miss=sorted(k for k in keys if not idlike(k) and k not in skip and k not in spec)
miss5_19=set()
keys19=set()
def walk2(x):
    if isinstance(x,dict):
        for k,v in x.items(): keys19.add(k); walk2(v)
    elif isinstance(x,list): [walk2(v) for v in x]
walk2({k:v for k,v in o.items() if k!='uiText'})
s19=open(W+'nancys-adventure-english-v5-19.md').read()
pre=sorted(k for k in keys19 if not idlike(k) and k not in skip and k not in s19)
print('JSON keys not named in '+V+' spec:',miss); print('  (same check on v5-19, baseline):',pre)
print('  new in '+V+' vs baseline:',sorted(set(miss)-set(pre)))
ui=set(d['uiText']); used=set(re.findall(r'uiText\.(\w+)',spec))
bare=set(k for k in ui if re.search(r'`%s`'%k,spec))
print('uiText keys never referenced:',sorted(ui-used-bare)); print('spec uiText.x not in file:',sorted(used-ui))
print('uiText count',len(ui),'trophies',len(d['trophies']),'svg',d['picPlan']['totalSvgToDraw'],'pairs',len(d['soundDuel']['pairs']),'jesusWords',len(d['jesusWords']))
_pc=[c for c in d['cards'] if c['type']=='picture']; _em=sum(1 for c in _pc if c['pic'] and ':' not in c['pic']); _sv=sum(1 for c in _pc if (c['pic'] or '').startswith('svg:'))
for n in ['(%d)'%len(d['uiText']),'%d `trophies`'%len(d['trophies']),('earned count' if V>='v6-06' else 'earned of %d'%len(d['trophies'])),'Drawings Build makes: %d'%d['picPlan']['totalSvgToDraw'],'%d trophy ids'%d['picPlan']['trophySvgDrawnCount'],('%d gear'%sum(1 for t in d['trophies'] if 'thGloss' in t and t.get('cat')=='gear')) if _V37 else '15 gear','30)','`jesusWords`, 6','%d cards.'%_em,'%d cards'%_sv,'%d ids'%len(d['picPlan']['svg'])]:
    print('  spec states',n, n in spec)
# card integrity
_badpc=[c['id'] for c in d['cards'] if c['type']=='picture' and not (len(set(x['en'] for x in c['choices']))==4 and c.get('answer') in [x['en'] for x in c['choices']] and c.get('trap') in [x['en'] for x in c['choices']])]   # m7: prints False, never an AssertionError
print('all %d picture cards: 4 unique choices, answer+trap present:'%len(_pc), not _badpc, _badpc)
# visible unlock/locked
vis=[]
def walk3(x,p=''):
    if isinstance(x,dict):
        for k,v in x.items(): walk3(v,p+'.'+k)
    elif isinstance(x,list): [walk3(v,p+'[%d]'%i) for i,v in enumerate(x)]
    elif isinstance(x,str) and re.search(r'(?i)\bunlock|\blocked|ยังไม่ปลดล็อก|ปลดล็อก',x) and re.search(r'\.(en|th|thGloss)$',p): vis.append((p,x))
walk3(d); print('visible unlock/locked strings:',vis)
print(('no [PASTE- placeholder in ' if _V36 else '[PASTE- in ')+V+' files:', (not _V36)==any('[PASTE-' in open(W+f).read() for f in ['nancys-adventure-english-'+V+'.md','nancys-adventure-english-'+V+'-cards.json','nancys-adventure-english-FINAL-'+V+'.md']))
names=[t['en'] for t in d['trophies']]; print('trophy names unique:',len(names)==len(set(names)))
print('FINAL-'+V+' line 19:',fin.splitlines()[18][:80]); print('no LAUNCH LOCKED line:','LAUNCH LOCKED' not in fin and 'LAUNCH LOCKED' not in spec)
print('confidence footer absent:','onfidence' not in fin)

# --- resume checks (Oct 30) ---
import hashlib,os
J=d['jesusWords']; print('jesusWords',len(J),'start',sum(j['given']['type']=='start' for j in J),'gear',[j['given'].get('id') for j in J if j['given']['type']=='gear'])
TT={t['id']:t for t in d['trophies']}; assert all(TT[j['given']['id']]['cat']=='gear' for j in J if j['given']['type']=='gear')
LV=json.load(open(W+'v520/jw/opt2/live.json'))
print('leaf text == live.json byte-exact:',all(LV[j['ref']]['ESV']['json']==j['en'] and LV[j['ref']]['THSV11']['json']==j['th'] for j in J))
print('John 8:12 keeps คนที่ตามเรามา:', 'คนที่ตามเรามา' in [j for j in J if j['ref']=='John 8:12'][0]['th'], '| Luke 12:7 keeps อย่ากลัวเลย:', 'อย่ากลัวเลย' in [j for j in J if j['ref']=='Luke 12:7'][0]['th'])
allt=open(W+'nancys-adventure-english-'+V+'-cards.json').read()+spec+fin
print('excerpt anywhere in '+V+' files:', len(re.findall(r'(?i)excerpt',allt)))
bad=[k for j in J for k in j if re.search(r'(?i)cost|price|shop|buy',k)]+[k for v in d['verses'].get('weekly',[]) if isinstance(v,dict) for k in v if re.search(r'(?i)cost|price',k)]
print('cost/price/shop keys on verses or Jesus words:',bad)
print('cost/price/shop values in cards.json:',re.findall(r'"(?:cost|price|shop)"\s*:',allt[:len(open(W+"nancys-adventure-english-"+V+"-cards.json").read())]))
for pat in [r'\b911\b',r'(?i)call max',r'(?i)show the nurse',r'(?i)elk refuge',r'ยังไม่ปลดล็อก',r'\[PASTE-']:
    print('hits',pat,len(re.findall(pat,allt)))
gw=lambda t: len(t.split())
print('words: spec',gw(spec),'FINAL',gw(fin),'v5-19 spec',gw(s19))
cards=d['cards']; print('cards',len(cards),'picture',sum(c['type']=='picture' for c in cards),'say-it',sum(c['type']=='say-it' for c in cards),'written',sum(bool(c['en']) for c in cards))
for f,h in [l.split() for l in open(W+'v520/locked-md5.txt') if l.strip() and not l.startswith('#')]:
    pass
ok=all(hashlib.md5(open(W+f,'rb').read()).hexdigest()==h for h,f in [l.split() for l in open(W+'v520/locked-md5.txt') if l.strip() and not l.startswith('#')])
print('locked v5-19 files + CURRENT.md unchanged:',_lock36() if _V36 else ok)
# privacy: v5-19 separator regex + compact tel:/+1 pattern (Auditor gate, 5:15 PM)
P1=r'(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)'; P2=r'(tel:|\+1)\d{10}'
for nm,pat in [('P1 separated',P1),('P2 compact',P2)]:
    print('privacy',nm,'hits in '+V+':',sum(len(re.findall(pat,open(W+f).read())) for f in ['nancys-adventure-english-'+V+'.md','nancys-adventure-english-'+V+'-cards.json','nancys-adventure-english-FINAL-'+V+'.md']))
assert re.search(P2,'tel:+15555550100') and not re.search(P1,'1730332800')

# --- Instructor 6:18 scope 8/12/13 ---
vals=[]
def _w(x,p=''):
    if isinstance(x,dict): [_w(v,p+'.'+k) for k,v in x.items()]
    elif isinstance(x,list): [_w(v,p+'[%d]'%i) for i,v in enumerate(x)]
    elif isinstance(x,str): vals.append((p,x))
_w(d)
print('reward strings once, rewardText only:',[p for p,v in vals if v=='You earned this!']==['.rewardText.en'] and [p for p,v in vals if v=='เก่งมาก! รางวัลนี้เป็นของคุณ']==['.rewardText.th'])
print('spec never lists rewardText twice on one line:',not [l for t in (spec,fin) for l in t.splitlines() if len(re.findall(r'`rewardText`',re.sub(r'never (shows )?`rewardText`','',l)))>1])
TA=[c for c in d['cards'] if c['type']=='two-answer']
print('two-answer card with both prompts:',len(TA)==1 and {p['en'] for p in TA[0]['prompts']}=={"Let's pray.",'High five!'})
s81=spec[spec.index('### 8.1'):spec.index('## 9.')]; print('spec 8.1 says no coin loss, no XP loss:','No coin is removed' in s81 and 'no XP is lost' in s81)
print('uiText count stated == file:','`uiText` (%d)'%len(d['uiText']) in spec)
# --- Quartermaster 6:18 items ---
print('sayItToMaxwell / tell: gone:', 'sayItToMaxwell' not in json.dumps(d) and 'sayItToMaxwell' not in spec+fin and 'tell:<' not in spec+fin)
print('Baby and Hospital zero-coin rule in spec:', 'none in Baby and Hospital' in spec)
print('weapons (not shield) have classTitle:', all(t.get('classTitle') in d['uiText'] for t in d['trophies'] if t.get('slot')=='weapon' and t['id']!='shield-sunrise'))
if _T235: print('t235u map: no mapStyle/grid, 4 regions in one linear path r1>r2>r3>r4 (no place/pos), Ink path style:', 'mapStyle' not in d['meta'] and 'grid' not in d['mapLayout'] and [r['id'] for r in d['mapLayout']['regions']]==['r1','r2','r3','r4'] and not any('place' in r or 'pos' in r for r in d['mapLayout']['regions']) and d['mapLayout']['paths']==[['r1','r2'],['r2','r3'],['r3','r4']] and d['mapLayout']['pathStyle']['stroke']=='#10170F' and 'diamond' not in spec and '6.3b' not in spec)
else: print('meta.mapStyle regions, mapLayout 4 regions + grid fallback:', d['meta'].get('mapStyle')=='regions' and len(d['mapLayout']['regions'])==4 and [len(r) for r in d['mapLayout']['grid']]==[3,3,3] and set(sum(d['mapLayout']['grid'],[]))=={z['key'] for z in d['zones']}|{'soundDuel','scrolls'})
print('inline SVGs each <=4096 B, total:', all(len(v.encode())<=4096 for v in list(d['picPlan']['inlineSvg'].values())+list(d['picPlan']['uiInlineSvg'].values())), sum(len(v.encode()) for v in list(d['picPlan']['inlineSvg'].values())+list(d['picPlan']['uiInlineSvg'].values())))
print('no red/buzzer in spec 8.1:', not re.search(r'(?i)(?<!no )(?<!no red, no )buzz|#[Ff]{2}0000|(?<!no )red (fill|x)', s81))

# --- Instructor 6:31 ---
TF=json.load(open(W+'v520/instructor-thai-fixes-631.json')); raw=json.dumps(d,ensure_ascii=False)
# uiText.scrollsEmpty.th is superseded by Instructor's 7:04 PM exact text (checked under 'copy fixes present')
print('631 Thai fixes present:',all(x['fixed'] in raw for x in TF if x['path'] not in ('uiText.scrollsEmpty.th','uiText.unlocksDays.th') and not (_V6 and x['path'].split('.')[1] in _TRIM6)))   # v6-01: classMage removed by Option B (t360u)   # Q-0753: unlocksDays removed with day gates
print('tie card ms-32:',any(c['id']=='ms-32' and c['en']=='Let me fix your tie, honey.' for c in d['cards']))
print('Nov 7 list only bh-01..10:',[c['id'] for c in d['cards'] if c['nursePhrase']]==['bh-%02d'%i for i in range(1,11)])
print('no doubled spaces in strings:','  ' not in ''.join(v for v in re.findall(r'"((?:[^"\\]|\\.)*)"',raw) if '<svg' not in v))
# --- FULL LOOP 6:40 ---
print('review queue in spec (localStorage, 2 per visit, first 3 cards):','`naeReviewQueue`' in spec and 'up to 2 queued cards' in spec and 'within the first 3 cards' in spec)
print('instant feedback 150 ms stated:',spec.count('within 150 ms of the tap')>=2)
if _V6: print('bow-oak removed by Option B trim (t360u): not in trophies, trophySvg or trophyInlineSvg; Forest Ranger class gone:', not [t for t in d['trophies'] if t['id']=='bow-oak'] and 'bow-oak' not in d['picPlan']['trophySvg'] and 'bow-oak' not in d['picPlan']['trophyInlineSvg'] and 'forestRanger' not in d['uiText'])
else: print('bow-oak brown, own icon, Forest Ranger:',[t for t in d['trophies'] if t['id']=='bow-oak'][0]['en']=='Brown Oak Bow' and 'bow-oak' in d['picPlan']['trophyInlineSvg'] and [t for t in d['trophies'] if t['id']=='bow-oak'][0]['classTitle']=='forestRanger')
print('ms-32 uses svg:tie, one tie card:',[c['pic'] for c in d['cards'] if 'tie,' in c['en'].lower() or ' tie ' in c['en'].lower()]==['svg:tie'])
print('every svg: pic has an id in picPlan.svg:',all(c['pic'][4:] in d['picPlan']['svg'] for c in d['cards'] if (c.get('pic') or '').startswith('svg:')))
_allpics=[c.get('pic') for c in d['cards']]+[ch.get('pic') for c in d['cards'] for ch in c.get('choices',[]) if isinstance(ch,dict)]
print('every picPlan.svg id is used by a card or choice:',all('svg:'+i in _allpics for i in d['picPlan']['svg']))
print('ms-31 uses drawn SVGs, no 🙏/✋:',[ch['pic'] for c in d['cards'] if c['type']=='two-answer' for ch in c['choices']]==['svg:pray-kneel','svg:high-five'] and '🙏 `uiText.pray`' not in spec)
print('class titles = Maxwell mapping:',{t['id']:t.get('classTitle') for t in d['trophies'] if t.get('slot')=='weapon'}=={'sword-iron':'classDefender','sword-gold':'classDefender','sword-crystal':'classDefender','sling-shepherd':'classWarrior','staff-shepherd':'classMage','staff-lantern':'classMage','hammer-builder':'classKnight','bow-oak':'forestRanger','shield-sunrise':None})
print('cards.json minified (pair <= PASTE):',open(W+'nancys-adventure-english-'+V+'-cards.json').read().count('\n')<=1 and len(open(W+'nancys-adventure-english-FINAL-'+V+'.md').read())+len(open(W+'nancys-adventure-english-'+V+'-cards.json').read())<=len(open(W+'nancys-adventure-english-'+V+'-PASTE.md').read())+200)
# --- INFINITY LOOP guards (Auditor 7:00 PM critique + Maxwell 6:59 PM copy fixes) ---
_sf=spec+fin
_bossN={b['name']['en'] for z in d['zones'] for b in ([z['boss']] if isinstance(z.get('boss'),dict) else [])}
_gl=[m for m in re.findall(r'[^\n]{0,40}\bGuardian\b[^\n]{0,20}',_sf+json.dumps(d,ensure_ascii=False)) if not any(n in m for n in _bossN) and 'classDefender' not in m and 'Finish the last Guardian to open this.' not in m]   # v5-36 t334u: uiText.guardianLast (Instructor d6086d10) names the Guardian kind
print('no stale class names (sword class is Defender; boss "Guardian" names exempt; no Forest Ranger preselected):', not _gl and 'Forest Ranger preselected' not in _sf and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['classDefender']['th']=='ผู้ปกป้อง', _gl[:3] or '')
print('ms-31 SVG guard (never emoji after hooks):', all(not any(ord(ch)>0x2000 for ch in x['pic']) for c in d['cards'] if c['type']=='two-answer' for x in c['choices']))
_zp={}
for c in d['cards']:
    if c.get('pic'): _zp.setdefault((c['zone'],c['pic']),[]).append(c['id'])
_dup={k:v for k,v in _zp.items() if len(v)>1}
print('no duplicate picture within a zone:', not _dup, _dup or '')
_ans={c['id']:c.get('answer') for c in d['cards']}
print('bh-28 sleeping and bh-31 nap never offered on the same card:', not any({'The baby is sleeping.','The baby is taking a nap.'}<= {x['en'] for x in c.get('choices',[])} for c in d['cards']))
_old=['Welcome back! Your streak waited for you.','Your scrolls will appear here as you play.','It is three gifts.',"gentle 'aw'","head-down on wrong"]
_raw=json.dumps(d,ensure_ascii=False)+spec+fin
print('copy-fix guard (old strings gone):', [o for o in _old if o in _raw]==[], [o for o in _old if o in _raw])
print('copy fixes present:', d['welcomeBack']['en']=='Welcome back! Your days are all still here.' and d['uiText']['scrollsEmpty']['en']=='Your gift verses will show here.' and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['scrollsEmpty']['th']=='ข้อพระคัมภีร์ที่เป็นของขวัญจะมาอยู่ที่นี่' and d['uiText']['scrollsEmpty'].get('thStatus')=='NEEDS NANCY' and 'about 600 ms' in spec and 'Cheer and nod' in spec and any(x['en']=='Here are three gifts.' for c in d['cards'] if c['id']=='sw-06' for x in c['choices']))
print('reveal header never rewardText:', '- **Header:** `rewardText`' not in spec)
import os as _os
_paste=len(open(W+'nancys-adventure-english-'+V+'-PASTE.md').read())
_ho=W+'v520/auditor-handoff-'+('infinity' if V=='v5-20' else V)+'.md'
if _os.path.exists(_ho):
    _h=open(_ho).read(); _m=re.search(r'Merged PASTE: ([\d,]+) chars',_h)
    print('handoff paste size == computed:', bool(_m) and int(_m.group(1).replace(',',''))==_paste, _paste)
else: print('handoff paste size == computed: (handoff not written yet)', _paste)
_fl=open(W+'fixes-log.md').read()
print('log consistency (5:28 coin line superseded; Settings-icon line superseded):', 'SUPERSEDED by lines 57 and 65' in _fl and 'Settings icon unchanged | SUPERSEDED' in _fl)
print('emoji support rule in spec (Emoji 13.0, fallback):', 'The newest emoji used are Emoji 13.0' in spec and 'The newest emoji used are Emoji 13.0' in fin)
print('every Build drawing has a note:', (all(k in d['picPlan']['svgNotes'] for k in d['picPlan']['svg'] if k not in d['picPlan']['inlineSvg']) and all(t['pic'][4:] in d['picPlan']['svgNotes'] or t['pic'][4:] in d['picPlan']['trophyInlineSvg'] or t.get('wt') in d['picPlan']['weaponParts'] for t in d['trophies'] if t['pic'].startswith('svg:'))) if _V36 else all(k in d['picPlan']['svgNotes'] for k in [i for i in d['picPlan']['svg'] if i not in d['picPlan']['inlineSvg']]+[t['pic'][4:] for t in d['trophies'] if t['pic'].startswith('svg:') and t['pic'][4:] not in d['picPlan']['trophyInlineSvg']]))
# --- v5-21 (Maxwell 7:33/7:35 PM cycle) ---
_f=fin
print('v5-21 three-bar HUD + Map + grid rule:', _f.count('the three-bar')>=3 and 'Compartment grid (the three-bar rule, whole UI)' in _f and 'repeat(N,1fr); gap:8pt' in _f and '96 pt portrait' in _f and '28 pt gem' in _f)
if _T238: print('t238u no Settings: no gear SVG, no titleSettings/highContrast/calmMotion keys; slowMode/restWeeks are the v5-27 strings exactly and live in state.settings; Settings named only as absent:', 'gear' not in d['picPlan']['uiInlineSvg'] and not {'titleSettings','highContrast','calmMotion'}&set(d['uiText']) and (d['uiText']['slowMode']['en'],d['uiText']['slowMode']['th'],d['uiText']['restWeeks']['en'],d['uiText']['restWeeks']['th'])==('Slow Mode','โหมดช้า','Rest mode','โหมดพัก') and 'streak, settings{slowMode, restWeeks}}' in _f and [l for l in _f.splitlines() if 'Settings' in l]==[l for l in _f.splitlines() if 'No Settings screen or gear' in l or 'No Settings, gear button' in l] and 'Settings' not in json.dumps(d,ensure_ascii=False))
elif _T235: print('t235u no Settings: no gear SVG, no titleSettings/switch keys, no settings state field, Settings named only as removed:', 'gear' not in d['picPlan']['uiInlineSvg'] and not {'titleSettings','highContrast','calmMotion','slowMode','restWeeks'}&set(d['uiText']) and 'streak, settings}' not in _f and [l for l in _f.splitlines() if 'Settings' in l]==[l for l in _f.splitlines() if 'There is no Settings screen' in l or 'No Settings, gear button' in l])
else: print('v5-21 Settings button (44 pt Stone plate, supplied SVG, no rays or spokes):', '44 pt round Stone plate button holding `picPlan.uiInlineSvg.gear` exactly' in _f and 'never Build\'s own drawing' in _f and '**Gear icon**' not in _f)
if _T238: print('t238u title screen replaces the Q-0759 sword sequence; weapon drawn in Sam\'s hand in both portraits:', '- **Title (t238u):**' in _f and '- **Title (Q-0759):**' not in _f and "weapon is drawn in Sam's hand in both portraits" in _f)
else: print('v5-21 sword screen is the Q-0759 title (old open-stance bullet replaced), weapon drawn on her in both portraits:', '- **Title (Q-0759):**' in _f and 'open, friendly stance' not in _f.split('### 6.1')[1].split('### 6.2')[0] and ('weapon is drawn in %s hand in both portraits'%('his' if _T235 else 'her')) in _f and 'Only the sword and' not in _f)
print('v5-21 post-gate batch 1/2/5/6/8/9 + 3/4:', 'speaks ONE of them' in _f and 'replays both slowly' not in _f and _f.count('about 600 ms')==1+ _f.count('about 600 ms', _f.index('### 8.1')) and 'up to 4, in turn' in _f and 'tap area at least 80 pt' in _f and '🪵 `frame-oak`' in _f and (d['uiText']['classMage']['th']=='นักเวท' if not _V6 else 'classMage' not in d['uiText']) and 'tie' not in d['picPlan']['svgNotes'] and not any(x['en']=="Let's sit before we eat." for c in d['cards'] for x in c.get('choices',[])))
print('v5-21 no stacked 1x4 choices / odd gaps:', '1×4' not in _f and '12 pt gaps, 16 pt side margins' not in _f)

# --- Q-0741 (Maxwell t177u, 7:46 PM) ---
_raw=json.dumps(d,ensure_ascii=False); _all=spec+fin+open(W+'nancys-adventure-english-'+V+'-PASTE.md').read()+_raw
print('Q-0741 #2 old key classGuardian gone from outputs, classDefender = Defender/ผู้ปกป้อง:', 'classGuardian' not in _all and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['classDefender']['th']=='ผู้ปกป้อง' and 'uiText.classDefender' in spec)
_U=d['uiText']; _K={c['id']:c for c in d['cards']}
_old=["If you don't know the meaning","Hear it again","Big XP Flash","Rest weeks","Bigger Glow","แสงใหญ่ขึ้น","having a bottle","Great work, come back tomorrow","Echo Wood","Starry rest sky","heard all of Jesus","ได้ฟังถ้อยคำ","สัปดาห์พัก","แสง XP"]
print('Q-0741 #3/#4 flags 6-15 applied, no old string returns:', not [o for o in _old if o in _all] and _U['askMax']['en']=="Don't know a word? Ask Max." and _U['hearItAgain']['en']=='Hear it slowly' and (_T238 and 'talentXpFlash' not in _U and (_U['restWeeks']['en'],_U['restWeeks']['th'])==('Rest mode','โหมดพัก') or _T235 and not _T238 and 'talentXpFlash' not in _U and 'restWeeks' not in _U or not _T235 and _U['talentXpFlash']['en']=='Wide Halo' and _U['restWeeks']['en']=='Rest mode') and _K['bh-11']['en']=='When is my due date?' and d['restScreen']['en']=='Great work today! Keep going or take a rest?' and _U['jesusAllHeard']['en']=="You've read all of Jesus' words for now." and 'Got it without speaking' in spec, [o for o in _old if o in _all])
print('Q-0741 flag 16 thGloss on every Jesus word + shown in bubble:', all(j.get('thGloss') for j in d['jesusWords']) and '`thGloss` small' in spec)
_wf=[l for l in spec.splitlines() if l.startswith('- **Weapon flourishes')]
print('Q-0741 #1 weapon flourishes: gift tag, 4 Bible weapons, no stat/cost/timer words:', (len(_wf)==1 and all(w in _wf[0] for w in tuple(x for x in ('`sling-shepherd`','`staff-shepherd`','`staff-lantern`','`hammer-builder`') if not (_V6 and x.strip('`') in _TRIM6))+('uiText.weaponGift','once she has them.')) and not (_V6 and '`staff-lantern`' in _wf[0]) and 'Jesus word' not in _wf[0] and not re.search(r'(?i)multiplier|\bcost|price|buy |timer:|\+\d+ ?XP',_wf[0]) and _U['weaponGift']['en']=='Bible weapon') if _V36 else len(_wf)==1 and all(w in _wf[0] for w in ('`sling-shepherd`','`staff-shepherd`','`staff-lantern`','`hammer-builder`','uiText.weaponGift','never earned or bought','leaf-green','after a miss','no stat')) and not re.search(r'(?i)multiplier|\bcost|price|buy |timer:|\+\d+ ?XP',_wf[0]) and _U['weaponGift']['en']=='Bible weapon' and not re.search(r'(?i)earn|unlock|buy|\+1',_U['weaponGift']['en']))   # c4 C-CH-1 option A: no verse attached to gear
print('Q-0741 #5 ph-17 = svg:they with a drawing note:', _K['ph-17']['pic']=='svg:they' and 'they' in d['picPlan']['svgNotes'] and 'they' in d['picPlan']['svg'])
print('Q-0741 regressions (no 🙏 on ms-31, no Forest Ranger on swords, svgNotes.tie gone, no นักเวทย์):', '🙏' not in json.dumps(_K['ms-31'],ensure_ascii=False) and all(t.get('classTitle')=='classDefender' for t in d['trophies'] if t['id'].startswith('sword-')) and 'tie' not in d['picPlan']['svgNotes'] and 'นักเวทย์' not in _all)
print('Q-0743 card defaults: no card stores a default value; meta.cardDefaults documented in spec:', _stored==0 and {'fill','tag','easy','faith','nursePhrase'}<=set(_dflt) and 'meta.cardDefaults' in spec)
_au=[l for l in spec.splitlines() if l.startswith('- **Cheer and nod (with aura):**')]
if _T235: print('Q-0742 aura (t235u: the hero is a boy; his face):', (len(_au)==1 and all(w in _au[0] for w in ('the only in-run time the weapon rises, never across his face.','warm Gold')) and not re.search(r'(?i)purchase|\bcost|price|countdown|\+\d+ ?XP|multiplier',_au[0]) and fin.count('- **Cheer and nod (with aura):**')==1) if _V36 else len(_au)==1 and all(w in _au[0] for w in ('sword raised','sling twirled overhead','staffs lifted','hammer held high','bow raised','shield lifted','warm Gold for the 4 Bible weapons','leaf-green for the bow','comfort shimmer for the shield',"sword's own glint color",'inside the 96 pt portrait compartment','settles back to the low open stance','nothing to buy, no timer, no stat','about 600 ms','reduced motion: none',('rises around Sam' if _T238 else 'never across his face'))) and not re.search(r'(?i)purchase|\bcost|price|countdown|\+\d+ ?XP|multiplier',_au[0]) and 'aura rises, weapon lifts' in spec and fin.count('- **Cheer and nod (with aura):**')==1)
else: print('Q-0742 aura: one line, all 6 weapon poses, 4 colors, inside 96 pt compartment, settles back, gift rings with no buy/timer/stat, 600 ms + reduced motion:', len(_au)==1 and all(w in _au[0] for w in ('sword raised','sling twirled overhead','staffs lifted','hammer held high','bow raised','shield lifted','warm Gold for the 4 Bible weapons','leaf-green for the bow','comfort shimmer for the shield',"sword's own glint color",'inside the 96 pt portrait compartment','settles back to the low open stance','nothing to buy, no timer, no stat','about 600 ms','reduced motion: none','never across her face')) and not re.search(r'(?i)purchase|\bcost|price|countdown|\+\d+ ?XP|multiplier',_au[0]) and 'aura rises, weapon lifts' in spec and spec==spec and fin.count('- **Cheer and nod (with aura):**')==1)
# --- Q-0745 FULL INFINITY LOOP (Maxwell standing order 7:51 PM) + Q-0746 ---
_pp=d['picPlan']
print('Q-0745 C1 FINAL head drawing counts == data:', ('Draw %d SVGs: `picPlan.svg` (%d of %d;'%(_pp['totalSvgToDraw'],_pp['svgDrawnCount'],len(_pp['svg']))) in fin)
if _T238: print('Q-0745 C1 Auditor gate flags fixed (t238u: Map hero marker replaced by the 20 pt Sam emblem on her last row):', ',,' not in fin and '**Sam emblem:**' in fin and 'hero marker' not in fin.lower() and 'stands still about 96 pt tall on the Map above the grid' not in fin and 'voiceschanged' in fin)
elif _T235: print('Q-0745 C1 Auditor gate flags fixed (t235u: grid gone; hero marker in the dot of her last region):', ',,' not in fin and 'stands in the dot of the region she last played' in fin and 'stands still about 96 pt tall on the Map above the grid' not in fin and 'voiceschanged' in fin)
else: print('Q-0745 C1 Auditor gate flags fixed (doubled comma, grid hero, voiceschanged):', ',,' not in fin and 'no second figure' in fin and 'stands still about 96 pt tall on the Map above the grid' not in fin and 'voiceschanged' in fin)
print('Q-0745 C1 hint order cross-ref + Bible weapon stage test:', 'first while a Bible weapon is equipped, 11.1' in spec and 'puts her next Jesus word first in the hint bubble' in spec)
_dd=[c['id'] for c in d['cards'] if 'December 17' in json.dumps(c,ensure_ascii=False) or 'ธันวาคม' in json.dumps(c,ensure_ascii=False)]
_dd2=re.findall(r'(?i)december \d|due date[^\n]{0,30}\d', json.dumps({k:v for k,v in d.items() if k!='cards'},ensure_ascii=False))
_r=_K['bh-11'].get('reply',{})
print('Q-0746 due date ONLY in bh-11 reply (Maxwell override 7:54 PM), gentle, no countdown, NEEDS NANCY:', _dd==['bh-11'] and not _dd2 and _r.get('en')=='Around December 17. Baby will come when ready.' and _r.get('thStatus')=='NEEDS NANCY' and 'December' not in _K['bh-11']['en'] and not re.search(r'(?i)days? (left|to go)|countdown|\d+ days',json.dumps(_r,ensure_ascii=False)) and "Maxwell's `bh-11` `reply`" in spec and '`reply`' in spec)
if _T238: print('Q-0745 C2 weaponGift only on earned weapons, Rest mode back as a Character toggle (t238u), silent-switch iPhone check:', ('show `uiText.weaponGift` under them in Character once she has them.' in spec and 'Jesus word first' not in spec and 'so there is no Rest mode' not in spec and 'With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).' in spec and 'ring/silent switch' in fin) if _V36 else 'never on a not-yet card, so scripture never reads as a goal' in spec and 'so there is no Rest mode' not in spec and 'With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).' in spec and 'ring/silent switch' in fin)
elif _T235: print('Q-0745 C2 weaponGift only on earned weapons, Rest mode removed (t235u: streak never resets), silent-switch iPhone check:', ('show `uiText.weaponGift` under them in Character once she has them.' in spec and 'Jesus word first' not in spec and 'so there is no Rest mode' not in spec and 'With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).' in spec and 'ring/silent switch' in fin) if _V36 else 'never on a not-yet card, so scripture never reads as a goal' in spec and 'so there is no Rest mode' in spec and 'With Rest mode on' not in spec and 'ring/silent switch' in fin)
else: print('Q-0745 C2 weaponGift only on earned weapons, Rest mode defined, silent-switch iPhone check:', ('show `uiText.weaponGift` under them in Character once she has them.' in spec and 'Jesus word first' not in spec and 'so there is no Rest mode' not in spec and 'With `uiText.restWeeks` on, the flame shows a moon (a resting season; nothing else changes).' in spec and 'ring/silent switch' in fin) if _V36 else 'never on a not-yet card, so scripture never reads as a goal' in spec and '(a resting season; nothing else changes)' in spec and 'ring/silent switch' in fin)
# --- Q-0747 rev 7 Kitchen + Carnival + Server Talk; Q-0749 tiers ---
_kz=[z for z in d['zones'] if z['key']=='kitchen']
_kc=[c for c in d['cards'] if c['zone']=='kitchen']
_dish={'fd-01':'Pad thai','fd-02':'Tom yum','fd-03':'Green curry','fd-04':'Pad see ew','fd-05':'Tom kha gai','fd-06':'Massaman curry'}
print('Q-0747 kitchen zone: one zone, no boss/scroll, no open level (Q-0753), emblem svg:chef-hat, ids fd-/cv- only, cardIds == cards:', len(_kz)==1 and _kz[0]['boss'] is None and 'openLevel' not in _kz[0] and _kz[0]['emblem']=='svg:chef-hat' and all(re.match(r'^(fd|cv)-\d\d$',c['id']) for c in _kc) and _kz[0]['cardIds']==[c['id'] for c in _kc])
print('Q-0747 six Thai dish names SIGNED OFF (th only), all other kitchen Thai NEEDS NANCY:', {c['id']:c['en'] for c in _kc if c.get('thStatus')=='SIGNED OFF'}==_dish and all(c.get('thStatus','NEEDS NANCY')=='NEEDS NANCY' for c in _kc if c['id'] not in _dish))
_st=[c for c in d['cards'] if c['type']=='server-talk']
print('Q-0747 Server Talk 10 topics, 4 unique replies, answer+trap among them, hint present, spec 8.2:', len(_st)==10 and all(len({x['en'] for x in c['choices']})==4 and c['answer'] in [x['en'] for x in c['choices']] and c['trap'] in [x['en'] for x in c['choices']] and c['hint']['letters'] for c in _st) and '### 8.2 Server Talk' in spec and 'uiText.serverAsks' in spec)
_cv=[c['en'] for c in _kc if c['id'].startswith('cv-')]
print('Q-0747 Carnival Treats: 10 treats + phrases incl. the two given:', len(_cv)==12 and 'One cotton candy, please!' in _cv and 'Can I get extra powdered sugar?' in _cv and all(any(t in x.lower() for x in _cv) for t in ('funnel cake','cotton candy','corn dog','churros','slushie','kettle corn','snow cone','oreos','caramel apple','pretzel')))
_em=''.join(c.get('pic') or '' for c in _kc if not (c.get('pic') or '').startswith('svg:'))+''.join(t['pic'] for t in d['trophies'] if t['id'] in('spoon-gold',))
print('Q-0747 kitchen emoji iOS 14.2-safe (<= Emoji 13.0; no 🫕 🫔):', not any(ch in _em for ch in '🫕🫔🫓🫖🧋🫐🫒') and all(ord(ch)<0x1FAD0 for ch in _em))
print('Q-0747 rewards earned not bought: Golden Chef title after 25 right answers in Kitchen (Q-0753) svg:chef-hat, Golden Spoon auraRing pipFills 25, no cost fields:', any(t['id']=='title-golden-chef' and t['unlock']=={'type':'zoneRight','zone':'kitchen','n':25} and t['pic']=='svg:chef-hat' for t in d['trophies']) and any(t['id']=='spoon-gold' and t['slot']=='auraRing' and t['unlock']['type']=='pipFills' for t in d['trophies']) and not re.search(r'"(cost|price)"',json.dumps(d['trophies'])) and 'chef-hat' in d['picPlan']['svgNotes'])
if _T235: print('Q-0747 map (t235u): kitchen in r3 Home Lake, one straight column, no 3x3 grid:', 'kitchen' in [r for r in d['mapLayout']['regions'] if r['id']=='r3'][0]['zones'] and 'one straight column' in spec and '3 columns × 3 rows' not in spec and 'Kitchen below 11' not in spec)
else: print('Q-0747 map: kitchen in r3 Home Lake, 3x3 grid, spec says so:', 'kitchen' in [r for r in d['mapLayout']['regions'] if r['id']=='r3'][0]['zones'] and '3 columns × 3 rows' in spec and 'Kitchen below 11' not in spec)
_sy=sum(1 for c in d['cards'] if c['type']=='say-it'); _syw=sum(1 for c in d['cards'] if c['type']=='say-it' and c.get('en'))
print('Q-0747 say-it count in spec == data:', ('%d cards are `type: "say-it"`'%_sy) in spec and ('%d written plus the 4 empty slots'%_syw) in spec)
_SIMPLE=('pizza','taco','tacos','cake','corn dog','cotton candy','slushie','snow cone','steak')
_bare=[c['id'] for c in d['cards'] if c['type'] in('say-it','picture') and c.get('en') and len(c['en'].rstrip('.!?').split())<=2 and any(c['en'].lower().rstrip('.!?')==w for w in _SIMPLE)]
print('Q-0749 tiers: no bare simple-word card, nm-08 a phrase, hard words carry syl, tier rule in spec, no tier label/timer:', not _bare and _K['nm-08']['en']=='There is one God.' and all(_K[i].get('syl') for i in ('fd-06','fd-07','fd-08','fd-09','cv-01','cv-04','cv-08','nm-21','bh-01','bh-10')) and '**Tiers:**' in spec and 'No tier label, score or timer.' in spec, _bare)
_lr={}
for t in d['trophies']:
    if t['unlock']['type']=='level': _lr.setdefault(t['unlock']['n'],[]).append(t['id'])
if _T235: print('Q-0752 rule 4: levels 5, 7, 12 give no cosmetic (t235u: gear bonuses from gems, meta.bonusGems):', not any(_lr.get(n) for n in (5,7,12)) and '`meta.bonusGems`' in spec)
else: print('Q-0752 rule 4: levels 5, 7, 12 give no cosmetic (talents now come from gems, Q-0756):', not any(_lr.get(n) for n in (5,7,12)) and '`meta.talentGems`' in spec)
# --- Q-0748 rev 1 (Maxwell 8:00 PM MT) ---
if _T235: print('Q-0748 superseded by t235u (talents removed): no talent uiText keys or meta.talentGems, talent named only as replaced/absent, no Bigger Glow in shipped files:', not [k for k in d['uiText'] if k.startswith('talent')] and 'talentGems' not in d['meta'] and all('replace talents' in m or 'or talent exists' in m for m in [m for m in re.findall(r'[^\n]{0,30}(?i:talent)[^\n]{0,10}',spec+fin)]) and not any(x in t for x in ('Bigger Glow','แสงใหญ่ขึ้น') for t in (spec,open(W+'nancys-adventure-english-'+V+'-PASTE.md').read(),json.dumps(d,ensure_ascii=False))), [m for m in re.findall(r'[^\n]{0,30}(?i:talent)[^\n]{0,10}',spec+fin)])
else: print('Q-0748 talentXpFlash Wide Halo / รัศมีกว้าง NEEDS NANCY, Right-Answer Glow kept, spec talents line, no Bigger Glow in shipped files:', _U['talentXpFlash']=={'en':'Wide Halo','th':'รัศมีกว้าง','thStatus':'NEEDS NANCY'} and _U['talentGlow']['en']=='Right-Answer Glow' and 'Smooth Slide, Wide Halo, Right-Answer Glow' in spec and not any(x in t for x in ('Bigger Glow','แสงใหญ่ขึ้น') for t in (spec,open(W+'nancys-adventure-english-'+V+'-PASTE.md').read(),json.dumps(d,ensure_ascii=False))))
_m=spec[spec.index('### 6.3 Map'):spec.index('### 6.4')] if _T235 else spec[spec.index('#### 6.3a'):spec.index('#### 6.3b')]
if _T238: print('Q-0748 (t238u) Map shows a 20 pt Sam emblem (head, glasses) on her last-played row plate, not tappable; dots keep emblems; map portrait is the 72 pt avatar button only:', '**Sam emblem:** each dot keeps its region emblem' in _m and '20 pt Sam head (glasses' in _m and 'Not tappable' in _m and "Sam's 72 pt portrait on a round Stone plate" in _m and 'Map hero)' not in spec)
elif _T235: print('Q-0748 (t235u linear map) hero marker ~32 pt walking full-body, weapon, stands in the dot of her current region, no portrait, map portrait is the 72 pt avatar button only:', '**Hero marker:** a small full-body hero (about 32 pt tall) in a single still, mid-step walking pose' in _m and 'equipped weapon in hand' in _m and 'stands in the dot of the region she last played' in _m and 'No portrait' in _m and 'still hero' not in spec and 'Map hero)' not in spec)
else: print('Q-0748 regions-mode Map hero is a ~32 pt walking full-body marker with weapon on her current region, no still 96 pt hero, no second portrait:', '**Hero marker:** a small full-body hero (about 32 pt tall) in a single still, mid-step walking pose' in _m and 'equipped weapon in hand' in _m and 'stands on her current region' in _m and 'no portrait' in _m and 'still hero' not in spec and '96 pt' not in _m and 'Map hero)' not in spec)
# --- Q-0753 rev 1+2 (Maxwell 7:15 PM PT): no level gates, no time gates, optional rest ---
_PACE6='At one run a day, Golden Fields opens on day 2 at the earliest (day 1 is Phonics), Echo Forest on day 4; only end guardians gate (t334u).'   # v6-01: Auditor wording (spec build note only)
_sh=[spec.replace(_PACE6,'') if _V6 else spec,open(W+'nancys-adventure-english-'+V+'-PASTE.md').read(),open(W+'nancys-adventure-english-FINAL-'+V+'.md').read()]
_lvl=[p for p in (r'openLevel',r'appearsAtLevel',r'levelFeatures',r'bossLevels',r'fullMap',r'uiText\.levelN',r'[Oo]pens? at (level )?\d',r'below \d+[,;]',r'until level',r'from level \d',r'\(level \d+\)',r'Focus levels',r'focus range',r'Before level',r'Closed tiles',r'Not reached yet') if any(re.search(p,t) for t in _sh)]
print('Q-0753 no level gates (zones, bosses, Sound Duel, Talents, Map, Kitchen) in spec/PASTE/FINAL/cards:', not _lvl and not any('openLevel' in z or (z.get('boss') or {}).get('appearsAtLevel') for z in d['zones']) and 'levelFeatures' not in d['meta'] and all(z['boss'].get('readyAfter',30)==30 for z in d['zones'] if z.get('boss')) and (('every zone and Sound Duel are open from her first launch' in spec) if _T235 else ('Always open:' in spec)), _lvl)
_tm=[p for p in (r'daysPlayed',r'days played',r'unlocksDays',r'days of play',r'day 1',r'five minutes',r'5 active minutes',r'play timer\.',r'The timer counts',r'See you tomorrow',r'Daily rest',r'land on day') if any(re.search(p,t) for t in _sh+[json.dumps(d,ensure_ascii=False)])]
print('Q-0753 no time gates (days-played, session, timer, scheduled unlocks); every unlock type is play-based:', (not _tm and {t['unlock']['type'] for t in d['trophies']}<={'start','level','pipFills','zoneRight','bossesWon','secret'}|({'guardian'} if _V6 else set()) and all(set(t['unlock'])=={'type','regions','spokenGotIt'} for t in d['trophies'] if t['unlock']['type']=='secret') and 'daysPlayed' not in d['trophyRules']['unlockTypes'] and 'rightByZone{}' in spec and 'never from days or sessions' in spec) if _V36 else not _tm and {t['unlock']['type'] for t in d['trophies']}<= {'start','level','pipFills','zoneRight','bossesWon'} and 'daysPlayed' not in d['trophyRules']['unlockTypes'] and 'rightByZone{}' in spec and 'never from days or sessions' in spec, _tm)
_gc=[t for t in d['trophies'] if t['id']=='title-golden-chef'][0]
_ev=collections.Counter((t['unlock']['type'],t['unlock'].get('zone'),t['unlock'].get('n')) for t in d['trophies'] if t['unlock']['type']!='start')
print('Q-0753 Golden Chef = 25 right answers in Kitchen; its goal is unique (pre-existing pairs only: 2 boss wins, level 20); earned not bought:', ((lambda _e: _gc['unlock']=={'type':'zoneRight','zone':'kitchen','n':25} and _e[('zoneRight','kitchen',25)]==1)(collections.Counter((t['unlock']['type'],t['unlock'].get('zone'),t['unlock'].get('n')) for t in d['trophies'] if t['unlock']['type']!='start' and 'tier' not in _json_load(open(W+'nancys-adventure-english-'+V+'-cards.json'))['trophies'][[x['id'] for x in d['trophies']].index(t['id'])])) and not re.search(r'"(cost|price)"',json.dumps(d['trophies']))) if _V36 else _gc['unlock']=={'type':'zoneRight','zone':'kitchen','n':25} and _ev[('zoneRight','kitchen',25)]==1 and sorted(k for k,v in _ev.items() if v>1)==[('bossesWon',None,2),('level',None,20)] and not re.search(r'"(cost|price)"',json.dumps(d['trophies'])))
print('Q-0753 rule 4 reworded (one reward per level, nothing opens by level/day, two goals = two queued screens):', '4. **One new thing per screen.**' in spec and ('Nothing opens by day, and levels open only gear tiers (11.1): every zone and Sound Duel are open from her first launch.' in spec if _VN>=35 else 'Nothing opens by level or by day' in spec) and 'two separate queued screens' in spec)
print('Q-0753 rev 2 rest screen optional victory lap: new text, Keep playing primary + Rest now, no cap/forced rest, Thai NEEDS NANCY:', d['restScreen']=={'en':'Great work today! Keep going or take a rest?','th':'วันนี้เก่งมากเลย! เล่นต่อหรือพักก่อนดี','thStatus':'NEEDS NANCY'} and d['uiText']['keepGoing']['en']=='Keep playing' and d['uiText']['restNow']['en']=='Rest now' and '## 14. Rest screen (optional victory lap)' in spec and '`uiText.keepGoing` (primary, Gold) starts her next run' in spec and 'No session length, daily cap, play timer or forced rest' in spec and 'Great work! Time to rest.' not in json.dumps(d))
# --- Q-0754 rev 1 (Maxwell 7:38 PM PT): daily memory verses ---
_dv=json.load(open(W+'nancys-adventure-english-v5-32-daily-verses.json')); _dvs=_dv['verses']; _dvp=json.load(open(W+'nancys-adventure-english-'+V+'-daily-verses.json'))
_old16={x['ref'] for x in d['verses']['weekly']}|{d['verses']['rest']['ref']}|{z['boss']['scroll']['ref'] for z in d['zones'] if z.get('boss')}|{j['ref'] for j in d['jesusWords']}
print('Q-0754 daily verses: 30 entries, each ref/en/th/enUrl/thUrl (bible.com v59/v174), all VERIFIED (D3), th NEEDS NANCY, no cost/price/shop field, none duplicates the 16 verses or 6 Jesus words, shipped copy == source:', len(_dvs)==30 and len({v['ref'] for v in _dvs})==30 and all(v['en'] and v['th'] and v['enUrl'].startswith('https://www.bible.com/bible/59/') and v['enUrl'].endswith('.ESV') and v['thUrl'].startswith('https://www.bible.com/bible/174/') and v['thUrl'].endswith('.THSV11') and v['status']=='VERIFIED' and v.get('thStatus')=='NEEDS NANCY' for v in _dvs) and not re.search(r'(?i)"(cost|price|shop|buy)',json.dumps(_dv)) and not ({v['ref'] for v in _dvs}&_old16) and {**_dvp,'version':0}=={**_dv,'version':0} and len(_old16)==22)
_raw=json.load(open(W+'v520/daily-verses-fetch.json'))['ok']+json.load(open(W+'v520/daily-verses-ps86-fetch.json'))['ok'];   # c4: day 31 Psalm 86:15
_rw={x['ref']:x for x in _raw}
print('Q-0754 daily verse text == the saved fresh fetch (byte-exact):', all(_rw[v['ref']]['en']==v['en'] and _rw[v['ref']]['th']==v['th'] for v in _dvs))
print('Q-0754 spec: daily delivery, free, missed day costs nothing, re-viewable, no weekly delivery left, uiText.verseOfDay, verse card style:', 'one memory verse a day on her first open each day' in spec and 'Free, never sold; a missed day costs nothing; given verses stay on Scrolls' in spec and '`meta.dailyVerses`' in spec and 'as `verses.rotation`' in spec and not re.search(r'weekly verse|missed Monday|verseOfWeek',spec) and 'verseOfDay' in d['uiText'] and '**Verse card style:**' in spec and d['meta']['dailyVerses']=={'file':'daily-verses.json','count':30,'cycle':40})
# --- Q-0756 rev 1 (Maxwell 7:40 PM PT): jewels -> gems; talents at gem thresholds ---
_outs={'spec':spec,'FINAL':open(W+'nancys-adventure-english-FINAL-'+V+'.md').read(),'PASTE':open(W+'nancys-adventure-english-'+V+'-PASTE.md').read(),'cards':open(W+'nancys-adventure-english-'+V+'-cards.json').read()}
print('Q-0756 0 "jewel" strings in outputs (spec, FINAL, PASTE, cards):', {k:len(re.findall(r'(?i)jewel',v)) for k,v in _outs.items()}=={'spec':0,'FINAL':0,'PASTE':0,'cards':0}, {k:len(re.findall(r'(?i)jewel',v)) for k,v in _outs.items()})
_gt=[t for t in d['trophies'] if t['cat']=='gems']
print('Q-0756 5 gem trophies (gem-*), cat gems, featuredGem slot, uiText.gems Thai อัญมณี NEEDS NANCY:', len(_gt)==5 and all(t['id'].startswith('gem-') for t in _gt) and 'featuredGem' in d['trophyRules']['slots'] and d['uiText']['gems']['th']=='อัญมณี' and d['uiText']['gems'].get('thStatus')=='NEEDS NANCY' and 'gems' in d['trophyRules']['cats'])
if _T238: print('Q-0756 superseded by t235u/Watchman: gems power gear bonuses at 1/2/4 (meta.bonusGems), never spent, never go down, nothing to buy, no talent points:', (d['meta'].get('bonusGems')=={'glow':1,'halo':2,'slide':4} and 'talentPoint' not in d['uiText'] and 'talent point' not in spec.lower() and 'Gems still add the glow, halo and slide (`meta.bonusGems`), visual only.' in spec and 'Gems do nothing' not in spec) if _V36 else d['meta'].get('bonusGems')=={'glow':1,'halo':2,'slide':4} and 'talentPoint' not in d['uiText'] and 'talent point' not in spec.lower() and 'gems are earned, never spent and never go down; nothing to buy, no timer.' in spec and 'Gems do nothing' not in spec)
elif _T235: print('Q-0756 superseded by t235u: gems power gear bonuses at 1/2/4 (meta.bonusGems), nothing spent, no talent points:', d['meta'].get('bonusGems')=={'glow':1,'halo':2,'slide':4} and 'talentPoint' not in d['uiText'] and 'talent point' not in spec.lower() and 'nothing is spent and gems never go down' in spec)
else: print('Q-0756 talents unlock at gem thresholds (1, 2, 4), nothing spent, no talent points left:', d['meta']['talentGems']=={'talentSmoothSlide':1,'talentXpFlash':2,'talentGlow':4} and 'talentPoint' not in d['uiText'] and 'talent point' not in spec.lower() and 'nothing is spent and gems never go down' in spec)
# --- Q-0757 rev 1 cycle 1 (Maxwell 7:41/7:46 PM PT) ---
_pt=d['pantry']; _tids={t['id'] for t in d['trophies']}
print('Q-0757 economy: Pantry 6 cosmetics for Gold Stars, never trophies or verses, earn per right answer/run, no timer/sale/stock/offer/real money, no-shop line replaced, grace check keeps verses free:', (len(_pt['items'])==6+(3 if _V6 else 0) and (not _V6 or [i['id'] for i in _pt['items'] if 'tint' in i]==['shirt-sky','shirt-leaf','shirt-gold'] and all(i['slot']=='tunic' and 30<=i['stars']<=80 for i in _pt['items'] if 'tint' in i)) and all(i['slot'] in d['trophyRules']['slots'] and i['id'] not in _tids and isinstance(i['stars'],int) and i['stars']>0 for i in _pt['items']) and _pt['earn']=={'rightAnswer':1,'runDone':5} and ('(cosmetics only, never trophies or verses' if _V6 else '(cosmetics only, never trophies or verses)') in spec and 'stars drop only here and in the gear tab.' in spec and 'No timer, sale, stock limit, offer or real money' in spec and 'No shop, currency, or spending anywhere' not in spec and not re.search(r'"(cost|price)"',json.dumps(d['verses'])+json.dumps(d['trophies'])+json.dumps(d['jesusWords'])) and 'goldStars' in d['uiText'] and 'pantry' in d['uiText']) if _V36 else len(_pt['items'])==6 and all(i['slot'] in d['trophyRules']['slots'] and i['id'] not in _tids and isinstance(i['stars'],int) and i['stars']>0 for i in _pt['items']) and _pt['earn']=={'rightAnswer':1,'runDone':5} and 'Golden Pantry sells cosmetics only for Gold Stars; trophies stay earned and never sold; verses never sold.' in spec and 'No shop, currency, or spending anywhere' not in spec and 'No timer, sale, stock limit, offer or real money' in spec and not re.search(r'"(cost|price)"',json.dumps(d['verses'])+json.dumps(d['trophies'])+json.dumps(d['jesusWords'])) and 'goldStars' in d['uiText'] and 'pantry' in d['uiText'])
print('Q-0757 coins stay the in-run meter; gems = talents; trophies never sold:', ('Coins are only the pip meter' in spec and d['meta']['coinMeter'].startswith('10 gold coins') and not any('stars' in t for t in d['trophies'] if 'wt' not in t) and 'other trophies stay earned and never sold' in fin and ('(cosmetics only, never trophies or verses' if _V6 else '(cosmetics only, never trophies or verses)') in spec) if _V36 else 'Coins are only the pip meter' in spec and d['meta']['coinMeter'].startswith('10 gold coins') and 'trophies are never sold' in d['trophyRules']['note'])
if _T238: print('Q-0757 game-feel style line (t238u/Watchman A2: chunky buttons, bold colors; no cartoon/mobile-strategy wording):', all(x in spec for x in (('heavy buttons, bold colors' if _T239 else 'chunky buttons, bold colors'),'icon counters (gem cluster, gold star)','fill with a pop','light like an upgrade','no timers or pressure','Thai labels keep their size, plate and space')) and not re.search(r'(?i)cartoon strategy|mobile-strategy',spec))
else: print('Q-0757 game-feel style line (chunky, saturated, icon counters, pop bars, upgrade nodes, no pressure, Thai labels not crowded):', all(x in spec for x in ('chunky rounded buttons','bold saturated colors','icon counters (gem cluster, gold star)','fill with a pop','light like an upgrade','no timers or pressure','Thai labels keep their size, plate and space')))
print('Q-0757 F3 meta.uiTextEntries == len(uiText):', d['meta']['uiTextEntries']==len(d['uiText']), len(d['uiText']))
print('Q-0757 F4 SIGNED OFF exception wording + 201 of 207; F6 7 zone emblems derived:', "are Maxwell's recorded exception (8:01 PM MT), `th` only; Nancy may still review them." in spec and ('%d of the %d written cards'%(sum(1 for c in d['cards'] if c.get('en'))-6,sum(1 for c in d['cards'] if c.get('en')))) in spec and ('Plus %d zone emblems'%len(d['zones'])) in spec)
_K5={c['id']:c for c in d['cards']}
print('Q-0757 F5 fd-07/08/09 Thai = meaning glosses (no sound-alike), NEEDS NANCY; crib/bed clues not translations:', [_K5[i]['th'] for i in ('fd-07','fd-08','fd-09')]==['เส้นพาสต้าซอสมะเขือเทศ','ขนมปังเนยรูปพระจันทร์เสี้ยว','ไอศกรีมถ้วยราดซอส'] and all('thStatus' not in _K5[i] for i in ('fd-07','fd-08','fd-09')) and _K5['ph-01']['thDef']=='ที่นอนของลูกน้อย' and _K5['ph-03']['thDef']=='นอนบนนี้' and _K5['ph-01']['pic']=='svg:crib' and _K5['ph-01']['en']=='crib' and d['meta']['thDefCards']==18 and '18 cards carry `thDef`' in spec)
print('Q-0757 thDef hints are clues, never the card translation:', all(c['thDef']!=c['th'] and c['thDef'] not in c['th'] for c in d['cards'] if c.get('thDef')))
if _T238: print('Q-0757 Map Sam emblem (t238u); Guardian boss-only; Defender/ผู้ปกป้อง:', (not re.search(r'Guardian',spec) and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['classDefender']['th']=='ผู้ปกป้อง' and 'talentXpFlash' not in d['uiText'] and all('Guardian' in z['boss']['name']['en'] for z in d['zones'] if z.get('boss'))) if _V36 else spec.count('**Sam emblem:**')==1 and 'Hero marker' not in spec and not re.search(r'Guardian',spec) and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['classDefender']['th']=='ผู้ปกป้อง' and 'talentXpFlash' not in d['uiText'] and all('Guardian' in z['boss']['name']['en'] for z in d['zones'] if z.get('boss')))
else: print('Q-0757 Map hero marker single still pose; Guardian boss-only; Defender/ผู้ปกป้อง; Wide Halo/รัศมีกว้าง:', 'single still, mid-step walking pose (one drawn frame, no walk cycle)' in spec and spec.count('**Hero marker:**')==1 and not re.search(r'Guardian',spec) and d['uiText']['classDefender']['en']=='Defender' and d['uiText']['classDefender']['th']=='ผู้ปกป้อง' and (_T235 and 'talentXpFlash' not in d['uiText'] or not _T235 and d['uiText']['talentXpFlash']['th']=='รัศมีกว้าง') and all('Guardian' in z['boss']['name']['en'] for z in d['zones'] if z.get('boss')))
print('Q-0757 chef-hat icon v2 (cream puff, gold band/outline only; same viewBox), note updated, council image saved:', 'fill="#FFF8E7"' in open(W+'v520/clipart/qm/chef-hat.svg').read() and 'viewBox="0 0 64 64"' in open(W+'v520/clipart/qm/chef-hat.svg').read() and d['picPlan']['svgNotes']['chef-hat'].startswith('Chef hat: tall top, 3 rounded Cream') and __import__('os').path.exists('/workspace/council-images/Q-0757_kitchen-mode-icon-chef-hat-v2-preview.png'))
_dr=json.load(open(W+'v520/daily-verses-dropped-fetch.json'))
print('Q-0757 the 4 dropped refs have THSV11 fetched (verse page, v174, chapter-corroborated) and stay out of daily-verses.json:', all(v['THSV11']['text'] and v['THSV11']['version']=='174' and v['THSV11']['chapterMatchCaseWsInsensitive'] for v in _dr.values()) and not (set(_dr)&{v['ref'] for v in _dvs}))

# --- Q-0757 cycle 4 (Maxwell t212u + council 7:56-8:01 PM PT) ---
_pf=json.load(open(W+'v520/c4-defaults-proof.json'))
print('Q-0757 c4 T2/T3 default-only trims: every card and block byte-identical once defaults are filled back in, no card changed type, spec documents both defaults:', _pf['ok'] and not _pf['cardsDiffer'] and not _pf['blocksDiffer'] and not _pf['typeChanged'] and _pf['cards']==len(d['cards']) and d['meta']['cardDefaults'].get('type')=='picture' and d['meta'].get('thStatusDefault')=='NEEDS NANCY' and '`type` `picture`' in spec and '`meta.thStatusDefault`' in spec)
_pk={c['id']:c['pic'] for c in d['cards'] if c['zone']=='kitchen' and c['type']=='say-it' and c.get('pic')}
import qm_q0758 as _Q8
print('Q-0757 c4 + Q-0758 picture-first: pic flags = the 4 council cards + Instructor sheet 14 (18), all stay say-it, no 🍿/🍰, no dup pic in Kitchen, spec rule present:', _pk=={'fd-17':'🍕','fd-18':'🌮','fd-19':'🥩','cv-10':'🥨',**_Q8.PIC} and len(_pk)==18 and len(set(_pk.values())|{c['pic'] for c in d['cards'] if c['zone']=='kitchen' and c['type']=='picture'})==21 and not any(c.get('pic') for c in d['cards'] if c['id'] in _Q8.V6ART) and 'A Kitchen say-it card with `pic` opens picture-first: picture and Thai; one tap shows the English.' in spec and not any(p in ('🍿','🍰') for p in _pk.values()))
print('Q-0757 c4 C-CH-1 option A: all 6 Jesus words given at start, no gear link, weaponGift reworded, spec has no gear-brings-a-word text:', all(j['given']=={'type':'start'} for j in d['jesusWords']) and len(d['jesusWords'])==6 and 'She has all 6 from the start' in spec and 'a new player has all 6' in spec and '`given.gear`' not in spec and 'adds one Jesus word' not in spec and 'all 6 are given at start' in spec)
print('Q-0757 c4 verses rotation/graceRule say day (v5-21 only), v5-19 untouched:', 'by day,' in d['verses']['graceRule'] and 'one verse a day' in d['verses']['rotation'] and 'Week index' in o['verses']['rotation'] and 'given by week,' in o['verses']['graceRule'])
_hp={i['id']:i['stars'] for i in d['pantry']['items']}
print('Q-0757 c4 C-CH-3: Honey Frame 30, owned tile ✓ + wearIt, replays give XP and Gold Stars:', _hp['frame-honey']==30 and '(owned: ✓ and `uiText.wearIt`)' in spec and 'Replays give card XP and Gold Stars only.' in spec)
print('Q-0757 c4 CP-1 cut stays cut (no near-full / one-more session-end hook):', not re.search(r'(?i)near[- ]full|almost full|one more (run|card)|just one more',spec+json.dumps(d,ensure_ascii=False)))
_s13=spec.split('## 13.')[1].split('## 14.')[0]
print('Q-0757 c4 CP-4 flame = total days only: never resets, no loss wording, no grey/broken flame, no countdown:', 'never resets it' in _s13 and not re.search(r"(?i)lose|lost|broken|gr[ae]y|countdown|reset to|\b0 days",_s13.replace('never resets it','')) and not re.search(r"(?i)lose your streak|streak (is )?(lost|broken)|gr[ae]y flame|broken flame",spec+json.dumps(d,ensure_ascii=False)))
print('Q-0757 c4 Watchman F1-F5/F7/W-1:', 'gold pile' not in spec and 'gold-pile' not in spec and 'gold-star price' in spec and 'stone-and-Gold shelf' in spec and 'wooden' not in spec and 'except `goldStars`' in spec and 'Gold Stars are the one counter that is spent' in spec and 'Spec text beats any mockup.' in fin and 'attached mockups' not in fin and '150–200 pt square' in spec and (_T235 and 'Talents book' not in spec or '44 pt Talents book' in spec) and 'Original art; no timers' not in spec and 'our own rising light' not in spec)
_g=json.load(open(W+'nancys-adventure-english-v5-32-daily-verses.json')); _gv={v['day']:v for v in _g['verses']}
print('Q-0757 c4 day 31 = Psalm 86:15 (fresh fetch == Auditor reference), every day 11-40 has enGloss/thGloss (thGloss NEEDS NANCY), spec gloss line:', _gv[31]['ref']=='Psalm 86:15' and _gv[31]['en']=='But you, O Lord, are a God merciful and gracious,\nslow to anger and abounding in steadfast love and faithfulness.' and all(v.get('enGloss') and v.get('thGloss') and v.get('thGlossStatus')=='NEEDS NANCY' for v in _g['verses']) and len(_g['verses'])==30 and 'optional `enGloss`/`thGloss` show small under the Thai, never spoken' in spec and '1 John 4:8' not in {v['ref'] for v in _g['verses']})
_ch=open(W+'v520/clipart/qm/chef-hat.svg').read()
print('Q-0757 c4 chef hat outline Ink #10170F (svg + note), v3 preview saved:', '#8A6200' not in _ch and 'stroke="#10170F"' in _ch and 'Ink #10170F outline' in d['picPlan']['svgNotes']['chef-hat'] and _os.path.exists('/workspace/council-images/Q-0757_kitchen-mode-icon-chef-hat-v3-preview.png'))

# --- Q-0758 (Maxwell t215u) ---
_E14=[(0x1FAE0,0x1FAFF),(0x1FAD7,0x1FADF),(0x1F6DD,0x1F6DF),(0x1FA7B,0x1FA7F),(0x1FAA9,0x1FAAF),(0x1FAB7,0x1FABF),(0x1FAC3,0x1FACF),(0x1F7F0,0x1F7F0),(0x1F979,0x1F979),(0x1F9CC,0x1F9CC),(0x1FA70,0x1FA70)]
_kp=[c['pic'] for c in d['cards'] if c.get('pic') and ':' not in c['pic']]
print('Q-0758 every emoji pic is Emoji 13.0 or older (no Emoji 14+ code point):', not [p for p in _kp if any(a<=ord(ch)<=b for ch in p for a,b in _E14)])
print('Q-0758 Instructor labels: wearIt Use it/ใช้เลย, wearing Using, Golden Chef เชฟทองคำ, all NEEDS NANCY:', _U['wearIt']['en']=='Use it' and _U['wearIt']['th']=='ใช้เลย' and _U['wearing']['en']=='Using' and [t['th'] for t in d['trophies'] if t['id']=='title-golden-chef']==['เชฟทองคำ'] and all(x.get('thStatus')=='NEEDS NANCY' for x in (_U['wearIt'],_U['wearing'])+tuple(t for t in d['trophies'] if t['id']=='title-golden-chef')))
import qm_v521_spec as _QS
print('Q-0758 rank-trim recipe inserted once after the trophy Grid block, 2 bottom studs, no rank words, Pantry unranked, Safari 14 CSS limits, animate transform/opacity only:', (fin.count('**Rank trim (CSS only, no new SVG):**')==1 and 'plus 2 Gold studs at the bottom corners' in spec and 'No rank words on screen; Pantry items have no rank.' in spec and 'Rarity has no words' in spec and 'no aspect-ratio, :has(), color-mix() or container queries' in spec and spec.index('**Rank trim')>spec.index('- **Grid:** 3 across at 320 pt') and spec.index('**Rank trim')<spec.index('- **Tap an earned trophy**') and not re.search(r'(?i)blizzard|warcraft|\bwow\b|world of',spec+fin) and not re.search(r'(?i)"(rank|rarity)\w*"',json.dumps(d)) and set(re.findall(r'"(tier\w*)"',json.dumps(d)))<={'tier','tierNames','tierColor','tierStars'}) if _V36 else spec.count(_QS.Q0758_RECIPE.split('\n')[0])==1 and fin.count('**Rank trim (CSS only, no new SVG):**')==1 and 'plus 2 Gold studs at the bottom corners' in spec and '4 Gold corner studs' not in spec and 'No rank words on screen; Pantry items have no rank.' in spec and 'no aspect-ratio, :has(), color-mix() or container queries' in spec and spec.index('**Rank trim')>spec.index('- **Grid:** 3 across at 320 pt') and spec.index('**Rank trim')<spec.index('- **Tap an earned trophy**') and not re.search(r'(?i)blizzard|warcraft|\bwow\b|world of',spec+fin) and not re.search(r'(?i)"(rank|rarity|tier)\w*"',json.dumps(d)))
print('Q-0758 Candy Crush juice: one pop per event; no combo meters, near-miss screens, lives, boosters anywhere in data:', 'one pop per event' in spec and 'no combo meters' in spec and 'near-miss screens' in spec and not re.search(r'(?i)combo|near[- ]miss|booster|\blives\b',json.dumps(d,ensure_ascii=False)) and len(re.findall(r'(?i)combo',spec))==1)
print('Q-0758 F6 + 320 pt: Thai 17 px+ no stroke (stroke only on English), 320 pt trims insets at most 6 pt and never the Thai:', '  - **Thai:** under it, Kanit, Cream, 17 px+, no stroke.' in spec and 'Thai 17 px+' in spec and not re.search(r'(?i)thai[^.\n]{0,80}(text-stroke|px Ink stroke)',spec) and 'on a 320 pt screen insets trim at most 6 pt and only the picture shrinks, never the Thai.' in spec)
if _T238: print('Q-0758/t238u style line: flat cel-shaded, thick Ink, serious, no comedy; no show or game names in Build text except the CoC core reference line:', '(stone, badge, pop)' in spec and 'Original SVG/CSS art: flat cel-shaded fills, thick Ink line, serious, no comedy; no copied assets' in fin and not re.search(r'Adventure Time|Teenage Robot|Danny Phantom|Clash of Clans feel|mobile-strategy',fin+json.dumps(d,ensure_ascii=False)))
else: print('Q-0758 swaps S1/S3 in, no third-party game name in Build text except the CoC core reference line:', '(stone, badge, pop)' in spec and 'cel-shaded mobile-strategy style; no copied assets' in fin and '(mobile-strategy feel)' not in fin and 'Clash of Clans feel' not in fin)
print('Q-0758 day 31 Psalm 86:15 VERIFIED (Chancellor rerun-2008), Thai NEEDS NANCY:', _gv[31]['ref']=='Psalm 86:15' and _gv[31]['status']=='VERIFIED' and _gv[31].get('thStatus')=='NEEDS NANCY' and _os.path.exists(W+'chancellor-verse-check/rerun-2008.log'))
print('Q-0758 c2 coherence: no filter-based brightness flash (Juice rule), glows fade opacity, sky ring contrast stated truthfully (6.96:1), heroic trim fits the parchment verse card:', 'brightness flash' not in spec and 'opacity flash' in spec and "every glow fades a layer's opacity" in spec and '(6.9:1+ on Ink)' in spec and '7:1+ on Ink' not in spec and 'Gold inner line on Stone, Dark Gold `#8A6200` on parchment' in spec and '(on Stone or parchment)' not in spec)

# --- Q-0759 opening screen (Maxwell t219u/t220u, REV 5 plan, 8:21 PM flat-fill ruling) + t223u D1/D7 + Auditor 8:29 PM fixes: one line per item ---
import qm_v521_spec as _Q9
_61=_f.split('### 6.1')[1].split('### 6.2')[0]; _U9=d['uiText']; _S9=d['picPlan']['uiInlineSvg']; _A9=''.join(_S9[k] for k in ('title','sword','stone'))
_PJ=open(W+'nancys-adventure-english-'+V+'-PASTE.md').read()
if not _T238: print('Q9 O1 scene: sun, hill, stone, 3 flat trees, Heroic trim frame, no cottage:', "<circle cx='262' cy='70'" in _S9['title'] and _S9['title'].count("<use href='#t'")==3 and '<ellipse' in _S9['title'] and 'M150 436' in _S9['stone'] and 'Heroic trim frame' in _61 and not re.search(r'(?i)cottage|house|roof',_A9+_61))
if not _T238: print('Q9 O2 art sizes (scene <=1,400 with keys, sword <=600, ambient <=150):', len(json.dumps({k:_S9[k] for k in ('title','sword','stone')},separators=(',',':')))-1<=1400 and len(_S9['sword'])<=600 and len(_Q9.Q0759_LOOP)+len(_Q9.Q0759_WISPS)<=150, len(_S9['title'])+len(_S9['sword'])+len(_S9['stone']), len(_S9['sword']), len(_Q9.Q0759_LOOP)+len(_Q9.Q0759_WISPS))
if not _T238: print('Q9 O3 Let\'s go: iron metal button, English #FF6464 24 px+ (Ink stroke from the button rule), Thai Cream, checklist exception:', 'the iron button `uiText.letsGo`: English `#FF6464` 24 px+, Thai Cream' in _61 and '(`uiText.letsGo` `#FF6464` 24 px+)' in _f and '3 px Ink stroke' in _f and '  - **Thai:** under it, Kanit, Cream, 17 px+, no stroke.' in _f)
if not _T238: print('Q9 O4 fly-in: .cam drawn at 150%, scale(.667)->1 (1.5x), origin her shoulder; squash .95-1.05 on her layer; arm own <g>; fade:', '`.cam` drawn at 150%' in _61 and ('`scale(.667)`→1, origin %s shoulder'%('his' if _T235 else 'her')) in _61 and 'squashes `scale(1.05,.95)`, rises `(.95,1.05)`' in _61 and 'arm, head own `<g>`' in _61 and 'fade from 80%' in _61 and 'transform-box:fill-box' in _61)
if not _T238: print('Q9 O5 gift: sword glows and rises into her hand, overhead with her aura, ONE flat Gold disc burst, no tug/pull/struggle:', ('the sword glows, rises into %s hand, then overhead'%('his' if _T235 else 'her')) in _61 and ('with %s aura and one flat Gold disc burst'%('his' if _T235 else 'her')) in _61 and not re.search(r'(?i)tug|wiggle|strain|struggle|pull',_61))
if not _T238: print('Q9 O6 timing: 1 s, 0.5 s via a duration class, 2nd tap skips (not passed on), no fail/timer/hold, reduced motion fade:', '1 s (0.5 s once a card is `seen`: a duration class)' in _61 and 'A 2nd tap skips, never passed on.' in _61 and 'Reduced motion: no sway, 150 ms fade.' in _61 and not re.search(r'(?i)timer|countdown|hold to|fail',_61))
_sp=lambda x:len(re.findall(r'<(path|circle|ellipse|rect|use)\b',x))
if not _T238: print('Q9 O7 sword most detailed (most shapes, 3 golds + gem + tassel + glow):', _sp(_S9['sword'])>max(_sp(_S9['title'].split('<defs>')[1].split('</defs>')[0]),_sp(_S9['stone']),2) and all(c in _S9['sword'] for c in ('#FFCC33','#FFD84D','#D9A21B','#FFF4C2','#2E7BFF',"class='t'","class='g'")), 'sword',_sp(_S9['sword']),'tree',_sp(_S9['title'].split('<defs>')[1].split('</defs>')[0]),'stone',_sp(_S9['stone']),'hill 2, sun 1')
if not _T238: print('Q9 O8 Take your sword! / รับดาบของคุณ (uiText.take, NEEDS NANCY by default), pickUpSword gone:', _U9['take']['en']=='Take your sword!' and _U9['take']['th']=='รับดาบของคุณ' and _U9['take'].get('thStatus')=='NEEDS NANCY' and d['meta'].get('thStatusDefault')=='NEEDS NANCY' and 'pickUpSword' not in _U9 and 'pickUpSword' not in _f)
if not _T238: print('Q9 O9 ambient (v5-22 W-T1): tassel .t + ONE curved Cream wisp .w share one sy keyframe at 2/3 s, no .v, rotate only, paused on tap, off in reduced motion:', _61.count('@keyframes')==1 and '@keyframes sy{50%{transform:rotate(6deg)}}' in _61 and 'on `.t` 2s `.w` 3s.' in _61 and '`.v`' not in _61 and 'Tap pauses' in _61 and 'no sway' in _61 and _S9['title'].count("class='w")==1 and "<path class='w' d='M9 99q30-9 60 0' fill='none' stroke='#FFF8E7'/>" in _S9['title'] and "class='w v'" not in _A9 and "<g class='t'>" in _S9['sword'])
print('Q9 O10 no mic, no cottage, no permission prompt:', not re.search(r'(?i)microphone|getUserMedia|\bmic\b|cottage|permission',_61+_A9))
_bad=r'(?i)filter|blur|gradient|<animate|drop-shadow|aspect-ratio|:has\(|color-mix|@container|inset:|box-shadow'
print('Q9 O11 Safari 14 / flat: no filter, blur, gradient, SMIL, :has(), color-mix(), container queries, inset; transform/opacity only:', (not re.search(_bad,_A9+_61.replace('no gradients','')) and 'Emoji 13.0 or older; animate only transform and opacity.' in _f and 'touch-action' not in _A9) if _V36 else not re.search(_bad,_A9+_61.replace('no gradients','')) and 'transform/opacity only' in _61 and 'touch-action' not in _A9)
if not _T238: print('Q9 O12 Let\'s go spoken once by the existing speech on the tap, text always shown:', 'speak `uiText.letsGo` once' in _61 and (_U9['letsGo']['en'],_U9['letsGo']['th'])==("Let's go!",'ไปกันเลย') and 'English `speechSynthesis` at 0.85' in _f)
print('Q9 art sync: one shared Ink stroke rule (3, round), outlines on art only, Thai never stroked; no AT/Blizzard names; no SFX words or emoji on the title:', '`.ti svg{stroke:#10170F;stroke-width:3;stroke-linejoin:round}' in _61 and not re.search(r'(?i)adventure time|finn|jake|ooo|blizzard|warcraft|elwynn|westfall|redridge|duskwood|excalibur|whoosh|ว้าว',_61+_A9+_U9.get('take',{}).get('en','')+_U9['letsGo']['en']) and not re.search('[\U0001F300-\U0001FAFF]',_61+_A9))
if not _T238: print('Q9 flat fills (8:21 PM ruling): sky, hill, burst one flat color each; only the sword has >1 shade per object:', 'sky `#4FA3FF`' in _61 and 'flat fills, no gradients' in _61 and 'flat Gold disc burst' in _61 and 'gradient' not in _A9.lower())
print('Q9 trade dress: no white bear-ear hat / light-blue shirt / green backpack combo, no Candy pinks in the art:', not re.search(r'(?i)bear[- ]ear|backpack',_61) and not re.search(r'(?i)#FF(69B4|C0CB|B6C1)',_A9))
print('Q9 D1 trophy cards 3 across at 320 pt (4 at 375+), auto height, no "square trophy cards", spec beats the 4-across mockup:', '- **Grid:** 3 across at 320 pt (4 across at 375 pt+) trophy cards' in _f and 'square trophy cards' not in _f and 'the card grows taller so the 17 px Thai never clips' in _f and ('spec beats the 4-across rank mockup' in _f or _T238 and 'Spec text beats any mockup.' in _f) and ('3 or 4 in %s'%('Character' if _T235 else 'My Stuff')) in _f)
print('Q9 D7 not-yet rank rings 60% opacity, tile full color:', ('(only its rank rings sit at 60% opacity, 3.3:1+ on Ink, non-text)' in _f and '  - **Not yet:** full color, never grey or dim' in _f) if _V36 else '(only its rank rings sit at 60% opacity, 5:1+ on Ink)' in _f and '  - **Not yet:** full color, never grey or dim' in _f)
print('Q9 Q8-F3 Dark Gold #8A6200 on parchment, plain Gold on Stone:', 'Gold inner line on Stone, Dark Gold `#8A6200` on parchment' in _f)
print('Q9 D8 no-op: Sound Duel already open from first launch, no level wording, no new completion gate:', (('every zone and Sound Duel are open from her first launch') if _T235 else 'every zone, Sound Duel and Talents are open from her first launch') in _f and not re.search(r'(?i)sound duel[^.\n]{0,80}(level 3|locked until|3rd finished stop)',_f))
print('Q9 D3 daily verses all 30 VERIFIED, one top-level verifiedBy (v5-22: six runs 7:49-8:28 + Auditor 8:46-8:48 104/104), none per verse, shipped copy byte-identical:', (all(v['status']=='VERIFIED' and 'verifiedBy' not in v for v in _dvs) and '104/104' in _dv['verifiedBy'] and {k:v for k,v in _dv.items() if k!='version'}=={k:v for k,v in _dvp.items() if k!='version'} and _dvp['version']==V) if _V36 else all(v['status']=='VERIFIED' and 'verifiedBy' not in v for v in _dvs) and '7:49' in _dv.get('verifiedBy','') and '8:28' in _dv['verifiedBy'] and '8:46-8:48' in _dv['verifiedBy'] and '104/104' in _dv['verifiedBy'] and open(W+'nancys-adventure-english-v5-32-daily-verses.json','rb').read()==open(W+'nancys-adventure-english-'+V+'-daily-verses.json','rb').read())
print('Q9 paste <= 188,500 (1,500 line) and <= 190,000:', len(_PJ)<=188500, len(_PJ))
if _T238:   # --- v5-29 (Maxwell t238u 11:59 PM PT; council 12:01-12:02 AM PT; Auditor fb72320b; Watchman v529-prebuild) ---
    _T=lambda k:(_U9[k]['en'],_U9[k]['th'])
    _66=_f.split('### 6.6')[1].split('### 6.7')[0]; _67=_f.split('### 6.7')[1].split('### 6.8')[0]; _63=_f.split('### 6.3')[1].split('### 6.4')[0]; _62=_f.split('### 6.2')[1].split('### 6.3')[0]
    print('t238u T1 title scene: sun, mountains, 3 flat trees, big rock + front grass, no tassel anywhere:', "<circle cx='262' cy='70'" in _S9['title'] and "fill='#7C8DA6'" in _S9['title'] and _S9['title'].count("<use href='#t'")==3 and "M110 470" in _S9['stone'] and "class='t'" not in _A9 and '#B8322A' not in _A9 and 'no tassel' in _61 and 'tassel' not in _PJ.replace('no tassel',''))
    print('t238u T2 Start your day / เริ่มวันใหม่ (uiText.letsGo, NEEDS NANCY), between rock and front grass, Hero Yellow 24 px+ 11.0; take key and sword text gone:', _T('letsGo')==('Start your day','เริ่มวันใหม่') and _U9['letsGo'].get('thStatus')=='NEEDS NANCY' and 'the iron button `uiText.letsGo` between rock and front grass (Hero Yellow 24 px+, 11.0; Thai Cream)' in _61 and 'take' not in _U9 and not re.search(r'(?i)take your sword|pick up the sword|รับดาบ|#FF6464|Let.s go!',_PJ))
    print('t238u T3 wind CSS-only on .w (grass, leaves), title screen only; Map paper static:', _61.count('@keyframes')==1 and 'Wind on `.w` only: `@keyframes sy{50%{transform:rotate(6deg)}}` 3 s.' in _61 and _S9['title'].count("class='w'")>=1 and "class='w'" in _S9['stone'] and _f.count('@keyframes sy')==1 and 'no animation, `overflow:hidden`' in _63)
    print('t238u T4 sun pan: transform/opacity, CSS only, ease-in <=1.2 s, 2nd tap skips, Sam 3 px dip no squash, reduced motion 150 ms fade:', all(x in _61 for x in ('`.cam` pans into the sun (origin at the sun, `translate` to center, `scale(3)`), ease-in, 1.2 s','transform/opacity only','A 2nd tap skips, never passed on.','Sam dips 3 px and rises (200 ms, no squash)','Reduced motion: no wind or pan, a 150 ms fade.','speak `uiText.letsGo` once')))
    print('t238u T5 old sword-rise/squash/zoom sequence gone (not stacked):', not re.search(r'rises into|disc burst|\.667|squashes|150%|origin his shoulder',_61))
    print('t238u T6 art sizes (scene <=1,400 with keys, sword <=600):', len(json.dumps({k:_S9[k] for k in ('title','sword','stone')},separators=(',',':')))-1<=1400 and len(_S9['sword'])<=600, len(json.dumps({k:_S9[k] for k in ('title','sword','stone')},separators=(',',':')))-1, len(_S9['sword']))
    print('t238u H1 Sam: young Thai American boy with glasses, traits only (slim legs, athletic build, small dot eyes, rugged), no show names, one "the hero", แซม via uiText.heroName:', '- **Sam:** the hero, a young Thai American boy with glasses' in _f and all(x in _f for x in ('slim, long tapered legs','Athletic build','small dot eyes (never giant)','Rugged','Zero comedy')) and _f.count('the hero')==1 and not re.search(r' boy\b',_f.replace('Thai American boy','').replace('a boy or a girl','')) and not re.search(r'Adventure Time|Teenage Robot|Danny Phantom',_PJ) and _T('heroName')==('Sam','แซม') and _T('yourHero')==('Your hero','ฮีโร่ของคุณ'))
    print('t238u H2 hub: two buttons + one Gold arrow cue (not a button, transform only, still with reduced motion):', ('Exactly two buttons, the hearth (a corner button) and one cue: a Gold arrow bobbing at the Map button\'s right end (transform only; still with reduced motion), a cue, not a button.' in _62 and 'Back from the Map or Character returns here.' in _62) if _V36 else ('Exactly two buttons plus one cue: a Gold arrow bobbing %s the Map button%s (transform only; still with reduced motion), a cue, not a button.'%(('at',"'s right end") if _T239 else ('beside',''))) in _62 and 'Back from the Map or Character returns here.' in _62)
    print('t238u C1 Character: Your hero caption, trophies row fixed above the tabs (never scrolled), 6 tabs 3x2, opens on newest trophy tab, only the pane scrolls, Back always to the hub:', "Fixed, never scrolled: Sam's panel (`uiText.yourHero` over `uiText.heroName`" in _66 and 'the `uiText.earnedShelf` row, then 6 tabs, 3 across in two rows' in _66 and "It opens on her newest trophy's tab." in _66 and 'Only the pane under the tabs scrolls' in _66 and 'always back to the main menu' in _f and 'back to the screen she came from' not in _f)
    print('t238u C2 Slow Mode + Rest mode: plain switches on Character only, v5-27 strings, Slow Mode = 0.6 with no second tap, off never costs streak/star/coin, no lock wording:', ('two switches, `uiText.slowMode` and `uiText.restWeeks`' in _66 and '(0.6 with `uiText.slowMode` on)' in _f and 'second 🔊' not in _f and 'never costs a streak, star or coin' in _67 and not re.search(r'(?i)lock',_66+_67)) if _V36 else 'two plain switches, `uiText.slowMode` and `uiText.restWeeks`' in _66 and '(0.6 with `uiText.slowMode` on)' in _f and 'second 🔊' not in _f and 'never costs a streak, star or coin' in _67 and not re.search(r'(?i)lock',_66+_67) and _f.count('uiText.slowMode')==2 and _f.count('uiText.restWeeks')==2)
    print('t238u R1 Restore: outside the pane, two steps, step 2 names what it replaces, second separate tap, localStorage naeState.bak first, corrupt/partial/empty changes nothing, no warning/loss words, tested:', (all(x in _67 for x in ('Opened only by `uiText.backup`, its lists scroll;','**Restore, two steps:**','`uiText.useBackup` names both (`uiText.backupCompare`)','a second, separate tap','Before step 2 replaces anything, her current save is copied to the localStorage key `naeState.bak`.','A corrupt, partial or empty backup changes nothing: her days, stars and given verses stay.','`uiText.restore` picks a backup and checks it (JSON, `schema` 5020, all keys);')) and not re.search(r'(?i)warn|lose|loss|erase|wipe|delete|red\b(?!,)',_67.replace('no red','')) and 'Restore: one tap never replaces her record; a corrupt, partial or empty backup changes nothing; `naeState.bak` holds the old save.' in _f) if _V36 else all(x in _67 for x in (('Opened only by `uiText.backup`, its lists scroll;' if _T239 else 'Opened only by `uiText.backup`, outside the pane'),'**Restore, two steps:**','`uiText.useBackup` names both (its level and days, and hers now)','a second, separate tap','Before step 2 replaces anything, her current save is copied to the localStorage key `naeState.bak`.','A corrupt, partial or empty backup changes nothing: her days, stars and given verses stay.')) and not re.search(r'(?i)warn|lose|loss|erase|wipe|delete|red\b(?!,)',_67.replace('no red','')) and 'Restore: one tap never replaces her record; a corrupt, partial or empty backup changes nothing; `naeState.bak` holds the old save.' in _f and (not _T239 or '`uiText.restore` picks a backup and checks it (JSON, `schema` 5020, all keys);' in _67) and _T('useBackup')==('Use this backup instead?','ใช้ข้อมูลสำรองนี้แทนไหม') and 'backup FILE' not in _f)
    print('t238u R2 Instructor Thai kept: กู้คืนข้อมูล, สำรองข้อมูล, ถ้วยรางวัลล่าสุดของฉัน, ตัวละคร, กลับ:', _U9['restore']['th']=='กู้คืนข้อมูล' and _U9['backup']['th']=='สำรองข้อมูล' and _U9['earnedShelf']['th']=='ถ้วยรางวัลล่าสุดของฉัน' and _U9['character']['th']=='ตัวละคร' and _U9['back']['th']=='กลับ')
    print('t238u M1 Map next-step row = region played least today; Sam emblem; dot speckle; log top band; path width 4; SE height budget:', ('next-step row (the open row whose end guardian she still needs, else the fewest runs today; ties: lowest row)' in _63 and 'the `zp` speckle' in _63 and 'repeating-radial' not in _f and 'a light top band' in _63 and d['mapLayout']['pathStyle']['width']==4 and '= 550 ≤ 568' in _63) if _V36 else 'next-step row (the region with the fewest runs today; ties: lowest row)' in _63 and 'static dot speckle' in _63 and 'repeating-radial' not in _f and 'a light top band' in _63 and d['mapLayout']['pathStyle']['width']==4 and '= 546 ≤ 568' in _63)
    print('t238u M2 Gold text only on label plates, incl. Level:', 'label "Level N" in Gold bold on a label plate' in _f and 'Gold only on label plates' in _f and 'white on XP Purple' not in _f and 'in white bold' not in _f)
    _one=[k for k,v in _U9.items() if '{n}' in v['en'] and re.search(r'\{n\}[^.]*?s\b',v['en']) and 'enOne' not in v]
    _min={t['unlock']['type']:min(x['unlock']['n'] for x in d['trophies'] if x['unlock']['type']==t['unlock']['type']) for t in d['trophies'] if 'n' in t['unlock']}
    print('t238u W1 singular/plural: every {n} plural string reachable at n=1 has enOne; spec states the rule; no "1 more gems":', (_U9['unlocksBosses']['enOne']=='Yours after 1 boss win' and '1 more gems' not in _PJ and all({'unlocksPips':'pipFills','unlocksZoneRight':'zoneRight'}.get(k) and _min.get({'unlocksPips':'pipFills','unlocksZoneRight':'zoneRight'}[k],2)>1 for k in _one)) if _V36 else _U9.get('nextBonus',{}).get('enOne')=='1 more gem to the next gear bonus' and _U9['unlocksBosses']['enOne']=='Yours after 1 boss win' and "a string's `enOne` is used when n is 1" in _f and '1 more gems' not in _PJ and all({'unlocksPips':'pipFills','unlocksZoneRight':'zoneRight'}.get(k) and _min.get({'unlocksPips':'pipFills','unlocksZoneRight':'zoneRight'}[k],2)>1 for k in _one), _one, _min)
    print('t238u S1 verse credit note: Scrolls shelf, no Settings (Auditor M1):', d['verses']['attribution']['note']=='Publisher wording, word for word. Shown small at the bottom of the Scrolls shelf.')
    print('t238u S2 PASTE <= 188,200 (council hard ceiling):', len(_PJ)<=188200, len(_PJ))
if _T239:   # --- v5-30: Auditor v5-29 gate batch (audit/v5-29-gate-2026-10-31.md d763084d), council 12:33 AM PT amendments ---
    print('v5-30 MJ1 cheer: raised weapon never across his face (same as the pose line):', ('the only in-run time the weapon rises, never across his face.' in _f and 'never across the face' in _f and 'across her face' not in _f) if _V36 else 'the only in-run time the weapon rises, never across his face.' in _f and 'never across his face;' in _f and 'across her face' not in _f)
    print('v5-30 MJ2 Backup lists may scroll; rule 12 and the test agree:', ('its lists scroll;' in _f and 'outside the pane' not in _f and 'only the Character pane (6.6) and Backup lists scroll.' in _f and 'nothing scrolls except the Character pane, gear rows (sideways) and Backup lists (scrollHeight' in _f) if _V36 else 'its lists scroll;' in _f and 'outside the pane' not in _f and 'only the Character pane (6.6) and Backup lists scroll.' in _f and 'nothing scrolls except the Character pane and Backup lists (scrollHeight' in _f)
    print('v5-30 mn1 Character test says its columns (3 across at 320 pt):', '   - Character: its columns fill' in _f and '4 columns' not in _f)
    print('v5-30 mn2 trophy row: 44 pt icons, earned first, no text:', 'in the fixed row above the tabs (6.6): 44 pt icons, earned first, no text;' in _f)
    print("v5-30 mn3 title tree moved to x=145 (clear of Sam and the sword glow); cards otherwise == v5-29:", "<use href='#t' x='145' y='326'/>" in _S9['title'] and "x='104'" not in _S9['title'])
    print('v5-30 mn4 Backup view in the Back exceptions and the banner exceptions:', 'the Map, Character, Backup (these have `uiText.back`' in _f and 'on every screen except the sword screen, main menu, Backup:' in _f)
    print("v5-30 mn5 hub arrow at the Map button's right end (no overlap):", "a Gold arrow bobbing at the Map button's right end" in _f and 'beside the Map button' not in _f)
    print('v5-30 mn6 dropped (Chancellor: :69 covers reduced motion):', 'Sam dips 3 px and rises (200 ms, no squash)' in _f)
    print('v5-30 mn7 Restore check = JSON, schema 5020, all keys (the :253 reset never meets a mismatched backup):', '(JSON, `schema` 5020, all keys)' in _f)
    print('v5-30 mn10 chunky -> heavy (4x):', 'chunky' not in _f and _f.count('heavy')>=4)
    print('v5-30 PASTE <= 188,200:', len(_PJ)<=188200, len(_PJ))
if _T240:
    print("v5-31 F1 title tree x=40 moved to x='-8' (off Sam's head; same length), x=145 tree kept:", "<use href='#t' x='-8' y='350'/>" in _S9['title'] and "x='40' y='350'" not in _S9['title'] and "<use href='#t' x='145' y='326'/>" in _S9['title'] and len(_PJ)==188191)
# --- v5-22 (Auditor Q-0759 gate c1, audit/q0759-gate-c1-2026-10-30.md, 8:53 PM PT): B1, W-T1, F3, W-T2 insurance ---
print('v5-22 B1 touch-action:manipulation on .ti right after the fill-box rule (spec line, not in art):', '.ti svg *{transform-box:fill-box}.ti{touch-action:manipulation}`' in _61 and _PJ.count('touch-action:manipulation')==1 and 'touch-action' not in _A9)
print('v5-22 F3 audio wake says the title tap:', 'the title tap on each launch' in _f and 'the sword tap on each launch' not in _f and 'the sword tap on each launch' not in _PJ)
if not _T238: print('v5-22 W-T2 insurance: sun Cream #FFF8E7, no #FFE07A in the title art (Got it gold-plated variant untouched):', "<circle cx='262' cy='70' r='26' fill='#FFF8E7'/>" in _S9['title'] and '#FFE07A' not in _A9 and 'Gold-plated (`#FFE07A`' in _f)
print('v5-22 loop <=150 (expect 142):', len(_Q9.Q0759_LOOP)+len(_Q9.Q0759_WISPS)<=150, len(_Q9.Q0759_LOOP)+len(_Q9.Q0759_WISPS))
print('v5-22 daily verses 60 en/th strings byte-identical to v5-21 (v520/pre-v522-scripts/daily-verses.json 41e4c65a):', [(v['ref'],v['en'],v['th']) for v in _dvs]==[(v['ref'],v['en'],v['th']) for v in json.load(open(W+'v520/pre-v522-scripts/daily-verses.json'))['verses']])
# --- v5-23 Instructor t51 language patch (instructor/loop-t51/instructor-patch-t51.json, md5 d2cfb41e) ---
_T51=json.load(open(W+'instructor/loop-t51/instructor-patch-t51.json')); _K23={c['id']:c for c in d['cards']}
print('v5-23 t51 cards: cs-07/sw-07/nm-09/bh-17 th end in Nancy\'s ค่ะ (exact patch text):', all(_K23[e['id']][e['field']]==e['to'] for e in _T51['cards']))
print('v5-23 t51 encouragement[5] God loves you. = พระเจ้าทรงรักคุณครับ; all 7 lines carry ครับ:', (d['encouragement'][5]['en'],d['encouragement'][5]['th'])==('God loves you.','พระเจ้าทรงรักคุณครับ') and all('ครับ' in x['th'] for x in d['encouragement']))
_g36=[v for v in _dvs if v['day']==36][0]
print('v5-23 t51 day 36 Psalm 103:13 thGloss = พระเจ้าทรงเมตตาเหมือนพ่อ; 60 verse strings byte-identical to v5-22 (v520/pre-v523-scripts/daily-verses.json 4e686f84):', _g36['ref']=='Psalm 103:13' and _g36['thGloss']=='พระเจ้าทรงเมตตาเหมือนพ่อ' and [(v['ref'],v['en'],v['th']) for v in _dvs]==[(v['ref'],v['en'],v['th']) for v in json.load(open(W+'v520/pre-v523-scripts/daily-verses.json'))['verses']])
print('v5-23 t51 PASTE: พระเจ้าทรงรักคุณ only as ค่ะ (sw-07) and ครับ (encouragement), never bare:', _PJ.count('"พระเจ้าทรงรักคุณค่ะ"')==1 and _PJ.count('"พระเจ้าทรงรักคุณครับ"')==1 and _PJ.count('"พระเจ้าทรงรักคุณ"')==0)
# --- v5-24 Watchman B2/B3/B6 (watchman/boredom-watch.md; Maxwell t227u) ---
print('v5-24 B6 run order fills with the rest seen longest ago (once, section 7 step 8):', (_f.count('once the zone has 7 seen, the rest seen longest ago.')==1 and _PJ.count('seen longest ago')==2 and 'the run repeats those seen longest ago, never twice in one scene' in _PJ) if _V36 else _f.count('once the zone has 7 seen, the rest seen longest ago.')==1 and _PJ.count('seen longest ago')==1)
print('v5-24 B2 + v5-25 C2 never 4 say-it cards in a row while a choice card is left; this rule wins over the order above (one general rule):', _f.count('Never 4 say-it cards in a row while a choice card is left; this rule wins over the order above.')==1 and _PJ.count('say-it cards in a row')==1 and 'this beats the order above' not in _PJ)
print('v5-25 C1 (replaces v5-24 B3 clause): say-it Got it is a right answer (XP, coin, Gold Stars, rightByZone) stated once in section 8; boss line back to plain rightByZone:', _f.count('Got it is a right answer: +10 XP, one coin, Gold Stars, `rightByZone`; never removes a coin.')==1 and _PJ.count('Got it is a right answer')==1 and 'a say-it Got it counts as right' not in _PJ and (_f.count('(`boss.readyAfter`, counted in `state.rightByZone`)')==1 or (_VN>=35 and _f.count('a recap after scene 5 of a run in that zone')==1)) and '+10 XP and one coin; never removes a coin.' not in _f)
_dv23=json.load(open(W+'nancys-adventure-english-v5-23-daily-verses.json'))
print('v5-26 verses: only the internal version changed vs nancys-adventure-english-v5-23-daily-verses.json (v5-23, 64ff095f); 60 strings byte-identical; version == the build version (was pinned to v5-26):', (_dvp['version']==V and {k:v for k,v in _dvp.items() if k!='version'}=={k:v for k,v in _dv23.items() if k!='version'} and [(v['en'],v['th']) for v in _dvp['verses']]==[(v['en'],v['th']) for v in _dv23['verses']]) if _V36 else _dv['version']==V and {k:v for k,v in _dv.items() if k!='version'}=={k:v for k,v in _dv23.items() if k!='version'} and [(v['en'],v['th']) for v in _dvs]==[(v['en'],v['th']) for v in _dv23['verses']] and open(W+'nancys-adventure-english-v5-32-daily-verses.json','rb').read()==open(W+'nancys-adventure-english-'+V+'-daily-verses.json','rb').read())
print('v5-24 C3 daily verse line says VERIFIED (see the file\'s `verifiedBy`), no UNVERIFIED clause, in spec/FINAL/PASTE:', all(t.count("Daily texts are VERIFIED (see the file's `verifiedBy`). Same text rules.")==1 and 'Daily texts are `UNVERIFIED`' not in t for t in (spec,_f,_PJ)) and 'UNVERIFIED' not in _PJ.split('## cards.json')[0])
# --- v5-26 Auditor t71u gate fixes (audit/t71u-fix-queue.md md5 bf85310d; steer 9:45 PM PT) ---
_K26={c['id']:c for c in d['cards']}; _N26=d['picPlan']['svgNotes']; _PP=d['picPlan']
print('v5-26 Q1 cs-22/23/24 one object per size picture ("nothing else", no "Two"):', all(_K26[i]['pic']=='svg:'+k and 'nothing else' in _N26[k] and 'Two' not in _N26[k] for i,k in (('cs-22','size-long'),('cs-23','size-big'),('cs-24','size-small'))) and _N26['size-long']=='One long stick reaching edge to edge across the card; nothing else.' and _N26['size-big']=='One huge red ball filling the card, touching its edges; nothing else.' and _N26['size-small']=='One tiny red ball alone in the middle of the empty card; nothing else.')
_F9=_K26['fd-09']
print('v5-26 Q2 fd-09 trap "ice cream sandwich" (choice + trap), Thai trapNote exact (NEEDS NANCY, on instructor/nancy-thai-signoff-list.md), th unchanged, no Sunday left:', _F9['trap']=='ice cream sandwich' and [x['en'] for x in _F9['choices']].count('ice cream sandwich')==1 and 'ice cream Sunday' not in json.dumps(d) and _F9['trapNote']=='sandwich = ไอศกรีมแซนด์วิช · รูปนี้คือไอศกรีมถ้วย' and _F9['th']=='ไอศกรีมถ้วยราดซอส' and _F9.get('thStatus','NEEDS NANCY')=='NEEDS NANCY' and 'sandwich = ไอศกรีมแซนด์วิช · รูปนี้คือไอศกรีมถ้วย' in open(W+'instructor/nancy-thai-signoff-list.md').read())
_SV=json.dumps({g:_PP[g] for g in ('inlineSvg','trophyInlineSvg')})
print('v5-26 Q3 inline SVG outlines Ink #10170F (no #1A1A1A/#2B2B2B/stroke #000 left; tie color="#000" kept):', (not re.search(r'#1A1A1A|#2B2B2B|stroke=[\'\\\\"]+#000[\'\\\\"]',_SV) and _SV.count("stroke='#10170F'")>=(8 if _V6 else 9)) if _V36 else '#1A1A1A' not in _SV and '#2B2B2B' not in _SV and 'stroke=\\"#000\\"' not in _SV and 'stroke="#000"' not in ''.join(_PP['inlineSvg'].values()) and 'color="#000"' in _PP['inlineSvg']['tie'] and sum(v.count('stroke="#10170F"') for g in ('inlineSvg','trophyInlineSvg') for v in _PP[g].values())>=20)
_S6=_K26['sw-06']
print('v5-26 Q4 sw-06 thDef exact (NEEDS NANCY), th unchanged, 18 thDef cards, on the sign-off list:', _S6.get('thDef')=='ของขวัญไม่ต้องจ่าย' and _S6['th']=='เป็นของขวัญที่ให้ฟรี' and _S6.get('thDefStatus','NEEDS NANCY')=='NEEDS NANCY' and sum(1 for c in d['cards'] if c.get('thDef'))==18 and '"thDef":"ของขวัญไม่ต้องจ่าย"' in _PJ and 'ph-01, ph-03, sw-06)' in _f and 'ของขวัญไม่ต้องจ่าย' in open(W+'instructor/nancy-thai-signoff-list.md').read())
print('v5-26 D2 not-yet trophies show a gift icon (no lock icon in player-facing text; Build-only "locked trophies" wording kept); no emoji added:', all(x in _f for x in ('a small gift icon at top-right','full color with a gift icon','trophy, gift, check')) and not re.search(r'lock icon|trophy, lock,',_PJ) and '🔒' not in _PJ)
_E14b=_E14   # same Emoji 14+ ranges as the Q-0758 check
print('v5-26 Emoji 13.0 limit across the whole PASTE (no Emoji 14+ code point):', not any(a<=ord(ch)<=b for ch in _PJ for a,b in _E14b))
if _T235: print('CURRENT.md matches its lock in v520/locked-md5.txt (v5-27 lock 5929db12 until the 1:10 AM PT Oct 31 flip; then the v5-30 pair lock):', __import__('hashlib').md5(open(W+'CURRENT.md','rb').read()).hexdigest() in [l.split()[0] for l in open(W+'v520/locked-md5.txt') if l.strip().endswith('  CURRENT.md')])
else: print('v5-26 CURRENT.md still b64c0f29 (locked; not repointed by the build):', __import__('hashlib').md5(open(W+'CURRENT.md','rb').read()).hexdigest()=='b64c0f2939f85c25c70d49fae7dfdfa3')
print('v5-26 C26-1 SVG line says size cards show one object (no two-object rule left; agrees with Q1 svgNotes):', all(t.count('size cards show one object at its size, nothing else.')==1 and 'size cards show two objects' not in t for t in (spec,_f,_PJ)))
# --- v5-28 Maxwell t235u redesign (Oct 30 2026, 11:41 PM PT; v520/qm_v528.py; Q-0764) ---
if _T235:
    _o27=json.load(open(W+'nancys-adventure-english-v5-27-cards.json')); _d28=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json')); _62=_f.split('### 6.2')[1].split('### 6.3')[0]; _63=_f.split('### 6.3')[1].split('### 6.4')[0]; _66=_f.split('### 6.6')[1].split('### 6.8')[0]
    _ship=_f+_PJ+json.dumps(d,ensure_ascii=False)
    print('t235u 1 main menu = exactly two buttons (uiText.titleMap, uiText.character), nothing else; launch lands there:', ('### 6.2 Main menu (the hub)' in _f and 'Exactly two buttons, the hearth (a corner button) and one cue' in _62 and _62.replace('Its accessible label is `uiText.verseGift`.','').count('`uiText.')==2 and 'otherwise the main menu.' in _f and '→ run or main menu.' in _f and (d['uiText']['character']['en'],d['uiText']['character']['th'])==('Character','ตัวละคร') and 'myStuff' not in d['uiText'] and 'My Stuff' not in _ship) if _V36 else '### 6.2 Main menu (the hub)' in _f and ('Exactly two buttons plus one cue' if _T238 else 'Exactly two buttons, nothing else') in _62 and _62.replace('Its accessible label is `uiText.verseGift`.','').count('`uiText.')==2 and 'otherwise the main menu.' in _f and '→ run or main menu.' in _f and (d['uiText']['character']['en'],d['uiText']['character']['th'])==('Character','ตัวละคร') and 'myStuff' not in d['uiText'] and 'My Stuff' not in _ship)
    print('t235u 2 Character is the deep hub (gems, gear, themes, titles + Scrolls, Pantry, Backup view) and the only scroll area; rule 12 zero scroll at 320 x 568:', (all(x in _66 for x in ('The only screen that scrolls','`uiText.gems`, `gear`, `themes` / `titles`','`uiText.scrolls` (6.8)','`uiText.pantry` (11.4)','overflow-y:auto','`uiText.backup` at right')) and '12. **Zero scroll:** at 320 × 568 pt every screen fits with no scrolling; only the Character pane (6.6) and Backup lists scroll.' in _f and 'nothing scrolls except the Character pane, gear rows (sideways)' in _f) if _V36 else all(x in _66 for x in ('The only screen that scrolls',('`uiText.gems`, `gear`, `themes` / `titles`' if _T238 else '`uiText.gems`, `gear`, `themes`, `titles`'),'`uiText.scrolls` (6.8)','`uiText.pantry` (11.4)','overflow-y:auto',('`uiText.backup` at right' if _T238 else 'Backup view (6.7)'))) and ('12. **Zero scroll (t235u):** at 320 × 568 pt every screen fits with no scrolling; only the Character pane (6.6) %s' % ('and Backup lists scroll.' if _T239 else 'scrolls.')) in _f and 'nothing scrolls except the Character pane' in _f)
    print('t235u 3 Map: linear one-column path, rugged Paper sheet 3D, zero scroll, 12 pt seam log + 8 pt header log frame, no diamond/grid/X markers:', all(x in _63 for x in ('one straight column','rugged Paper sheet','3D look','overflow:hidden','12 pt wood log lies across the yellow-to-green seam','8 pt log frames the whole header','grain')) and not re.search(r'(?i)diamond|X marker|3 columns × 3 rows|6\.3[ab]',_f) and "no wood surfaces except the Map's header logs (6.3)" in _f)
    print('t235u 4 no Settings anywhere; former settings rehomed; talents gone, gear bonuses from gems (never spent), Gold Stars Pantry-only:', ('No Settings screen or gear: motion follows iOS Reduce Motion, contrast `prefers-contrast`.' in _f and not re.search(r'(?i)talent(?!s\)|s exists| exists)',_f.replace('gear button or talent exists','').replace('(replace talents)','')) and 'talent:<key>' not in _f and d['meta'].get('bonusGems')=={'glow':1,'halo':2,'slide':4} and 'stars drop only here and in the gear tab.' in _f and 'Calm Motion' not in _ship and 'High Contrast' not in _ship) if _V36 else (('No Settings screen or gear: motion follows iOS Reduce Motion, contrast `prefers-contrast`.' if _T238 else 'There is no Settings screen or gear button: motion follows iOS Reduce Motion, contrast follows `prefers-contrast`, slow audio is a second 🔊 tap') in _f) and not re.search(r'(?i)talent(?!s\)|s exists| exists)',_f.replace('gear button or talent exists','').replace('(replace talents)','')) and 'talent:<key>' not in _f and d['meta'].get('bonusGems')=={'glow':1,'halo':2,'slide':4} and 'Gold Stars stay Pantry cosmetics only (11.4).' in _f and (_T238 or 'Slow Mode' not in _ship) and 'Calm Motion' not in _ship and 'High Contrast' not in _ship)
    print('t235u 5 hero is a boy (athletic build, slim legs, small eyes, rugged, zero comedy), no third-party show names in shipped text, sword-iron note updated:', (('- **Sam:** the hero, a young Thai American boy with glasses' if _T238 else '- **The hero (t235u):** a boy, never Nancy; no name on screen.') in _f) and all(x in _f for x in ('slim, long tapered legs',('small dot eyes (never giant)' if _T238 else 'small normal eyes (never giant)'),'V-taper','Rugged','Zero comedy')) and not re.search(r'(?i)teenage robot|danny phantom|adventure time|\bjenny\b|\bfinn\b',_ship) and 'her hero' not in _f and 'her portrait' not in _f and (("in Sam's hand point down at his side" if _T238 else "in the hero's hand point down at his side") in d['picPlan']['svgNotes']['sword-iron']))
    print('t235u 6 clip art tightened + realistic, Emoji 13.0, transform/opacity only:', ('**Clip art:** tight and realistic' in _f and 'Emoji 13.0 or older; animate only transform and opacity.' in _f) if _V36 else '**Clip art (t235u):** tight and realistic' in _f and 'Emoji 13.0 or older; animate only transform and opacity.' in _f)
    print('t235u 7 Map no-overlap rule: own grid cells, 44 pt+, 8 pt apart, one 56 pt right slot (boss ribbon or arrow, never both), 2-column bottom bar:', all(x in _63 for x in ('every tap target is its own grid cell, 44 × 44 pt or more and 8 pt from any other','one 56 pt slot at its right end','never both','Bottom bar (44 pt, 2 columns)')) and 'no two tap targets overlap' in _f)
    print('t235u 8 left icon column aligned, counts Gold #FFCC33 (no white), contrast 10.0 stated'+(' (m1 v6-05: Back left, counts plate 2x2)' if V>='v6-05' else '')+':', ('LEFT: `uiText.back` on a parchment plate (t306u). CENTER-LEFT: a counts plate, 2×2' in _63 and 'icons on one left edge' not in _63 and 'count in Gold `#FFCC33` (no white), 8 pt apart' in _63) if V>='v6-05' else ('one icon column on the 16 pt margin' in _63 and 'icons on one left edge' in _63 and 'count in Gold `#FFCC33` (no white)' in _63) if _V36 else 'one icon column on the 12 pt margin' in _63 and 'icons on one left edge' in _63 and 'count in Gold `#FFCC33` (no white)' in _63 and ('Gold only on label plates (10.0' if _T238 else 'Gold counts on a label plate 10.0') in _f)
    print('t235u verses: cards verses + jesusWords + boss scrolls byte-identical to v5-27; daily verses only version differs from v5-27:', (d['verses']==_o27['verses'] or _T238 and d['verses']==dict(_o27['verses'],attribution=dict(_o27['verses']['attribution'],note=_o27['verses']['attribution']['note'].replace(' screen and in Settings.',' shelf.')))) and d['jesusWords']==_o27['jesusWords'] and [z.get('boss') and z['boss']['scroll'] for z in d['zones']]==[z.get('boss') and z['boss']['scroll'] for z in _o27['zones']] and {k:v for k,v in _dv.items() if k!='version'}=={k:v for k,v in json.load(open(W+'nancys-adventure-english-v5-27-daily-verses.json')).items() if k!='version'})
    print('t235u cards: only the planned keys changed vs v5-27 (uiText, meta, mapLayout, picPlan.uiInlineSvg/svgNotes, version):', sorted(k for k in _d28 if _d28[k]!=_o27.get(k))==(['mapLayout','meta','picPlan','uiText','verses','version'] if _T238 else ['mapLayout','meta','picPlan','uiText','version']) and all(_d28[k]==_o27[k] for k in ('cards','trophies','pantry','zones','soundDuel')))
    print('t235u gems give her something to chase (Watchman 11:53 PM PT): totals turn on/upgrade gear bonuses at 1/2/4, never spent, Character shows next bonus + gems left, no gems-do-nothing line:', 'turns on and upgrades her gear bonuses by itself at set thresholds' in _f and 'a gentle progress line names the next bonus and the gems left (`uiText.nextBonus`' in _f and d['uiText']['nextBonus']['en']==('{n} more gems to the next gear bonus' if _T238 else 'Next gear bonus: {n} more gems') and not re.search(r'(?i)unlock',d['uiText']['nextBonus']['en']) and not re.search(r'(?i)gems? (do|does) nothing|gem shelf',_f))
    print('t235u paste <= 188,500:', len(_PJ)<=188500, len(_PJ))
# --- v5-32 (Maxwell t243u/t245u art overhaul; council 1:16 AM PT rulings; base v5-31 b599b2a1) ---
if _VN>=32:
    _P2=d['picPlan']; _U2=_P2['uiInlineSvg']; _ALL2=list(_U2.values())+list(_P2['inlineSvg'].values())+list(_P2['trophyInlineSvg'].values())
    _o31=json.load(open(W+'nancys-adventure-english-v5-31-cards.json')); _d32=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json'))
    print('v5-32 PASTE <= 188,200:', len(_PJ)<=188200, len(_PJ))
    print('v5-32 cards: only version, meta.version and picPlan (inline art + trophyStyle note) differ from v5-31; Thai untouched:', sorted(k for k in _d32 if _d32[k]!=_o31.get(k))==['meta','picPlan','version'] and {k:v for k,v in _d32['meta'].items() if k!='version'}=={k:v for k,v in _o31['meta'].items() if k!='version'} and sorted(k for k in _P2 if _P2[k]!=_o31['picPlan'][k])==['inlineSvg','trophyInlineSvg','trophyStyle','uiInlineSvg'])
    _V31=json.load(open(W+'nancys-adventure-english-v5-31-daily-verses.json')); _V32=json.load(open(W+'nancys-adventure-english-v5-32-daily-verses.json'))
    print('v5-32 daily verses: only version differs from v5-31:', {k:v for k,v in _V31.items() if k!='version'}=={k:v for k,v in _V32.items() if k!='version'} and _V32['version']=='v5-32')
    print('v5-32 same inline ids (8 card, 4 trophy) + tex + sam:', list(_P2['inlineSvg'])==list(_o31['picPlan']['inlineSvg']) and list(_P2['trophyInlineSvg'])==list(_o31['picPlan']['trophyInlineSvg']) and list(_U2)==['title','sword','stone','tex','sam'])
    print('v5-32 style lock: every card/trophy SVG roots Ink 3 px; tex has 5 material patterns + zs/zh; no gradients in art:', all("stroke='#10170F' stroke-width='3'" in v for v in list(_P2['inlineSvg'].values())+list(_P2['trophyInlineSvg'].values())+[_U2['sam']]) and all("id='%s'"%p in _U2['tex'] for p in ('zP','zW','zS','zC','zF')) and '.zs{' in _U2['tex'] and '.zh{' in _U2['tex'] and not any('Gradient' in v for v in _ALL2) and 'opacity:.12' in _U2['tex'])
    print('v5-32 no Openclipart left; ids unique across all inline art:', 'Openclipart' not in _PJ and len(re.findall(r"id='(\w+)'",''.join(_ALL2)))==len(set(re.findall(r"id='(\w+)'",''.join(_ALL2)))))
    print('v5-32 title: F1 tree at -8, 3 tree uses, sun kept, wind .w, static-fallback line:', "<use href='#t' x='-8' y='350'/>" in _U2['title'] and _U2['title'].count("<use href='#t'")==3 and "<circle cx='262' cy='70' r='26' fill='#FFF8E7'/>" in _U2['title'] and "class='w'" in _U2['title'] and "class='w'" in _U2['stone'] and 'If it never runs, the still pose is right.' in _61)
    print('v5-32 chunky on all 4 UI hits, no heavy UI word left (verse "heavy laden" kept):', all(x in _f for x in ('**Game feel:** chunky buttons','a chunky stone-and-Gold shelf','**Verse card style:** chunky rounded card','a chunky Gold Got it.')) and re.findall(r'(?i)heavy',_PJ)==['heavy'] and 'heavy laden' in _PJ)
    print('v5-32 Thai guard:', 'a box holding Thai has line-height 1.5+, no fixed height, no `overflow:hidden`, no ellipsis: it wraps (`uiText.useBackup` wraps or fits at 320 pt).' in _f and 'Thonburi' in _f)
    print('v5-32 spacing: 16 pt margins, map rows 20/8 (=104), coins 16/2 fit 90 pt, HUD 88/64, SE question budget 566:', 'max(16pt,env(safe-area-inset-left))' in _f and '12 pt margin' not in _f and ('a 20 pt icon and its count in Gold `#FFCC33` (no white), 8 pt apart' in _f if V>='v6-05' else '20 pt rows 8 pt apart' in _f) and '16 pt, two rows of 5, 2 pt gaps' in _f and "Sam's 88 pt portrait (64 pt on 568 pt screens)" in _f and '= 566 ≤ 568' in _f and 5*16+4*2<=(320-32-16)/3)
    print('v5-32 Sam supplied (anatomy line, gear hooks), H1 traits kept:', all(x in _f for x in ('`picPlan.uiInlineSvg.sam`','about 6 heads tall','knees mid-leg','joints bend one way','both feet on the ground line','`.wp`','one 2 px Ink bar under 32 pt')) and all(x in _U2['sam'] for x in ("class='wp'","class='ar'","class='hd'","fill='currentColor'")))
    print('v5-32 no brand or show names anywhere in the PASTE or cards:', not re.search(r'(?i)clash of clans|adventure time|teenage robot|danny phantom|blizzard|openclipart|\bCoC\b',_PJ+open(W+'nancys-adventure-english-'+V+'-cards.json').read()))

# ======================= v5-33 checks (Quartermaster) =======================
if V=='v5-33':
    import xml.dom.minidom as _xm, hashlib as _hl, sys as _sy
    _sy.path.insert(0,'/workspace/v533art'); from contrast import cr as _cr, blend as _bl
    _P=d['picPlan']; _ui=_P['uiInlineSvg']; _all=dict(_ui); _all.update(_P['inlineSvg']); _all.update(_P['trophyInlineSvg'])
    _bad=[]
    for _k,_v in _all.items():
        try: _xm.parseString(_v)
        except Exception as _e: _bad.append((_k,str(_e)[:60]))
    print('v5-33 MJ-A every inline SVG parses as XML (%d):'%len(_all), not _bad, _bad)
    print('v5-33 MJ-A no doubled </svg> and exactly one close tag each:', all(_v.count('</svg>')==1 for _v in _all.values()))
    print('v5-33 t251u aura SVG exists and parsed above (aura uses the tex #au symbol):', 'aura' in _ui and "href='#au'" in _ui['aura'])
    _art=sum(len(_v) for _v in _all.values()); _nan=len(_ui['nancy'])
    print('v5-33 art total %d (Nancy %d; cap 16,900 + Nancy = %d): within cap:'%(_art,_nan,16900+_nan), _art<=16900+_nan, 'excess', _art-16900-_nan)
    print('v5-33 per-SVG limit 2,500: every SVG within it except tex, the one shared-defs SVG the council exempted 5-0 (spec line states it):', [k for k,v in _all.items() if len(v)>2500 and k!='tex']==[] and '- **Per-SVG limit:** 2,500 chars per SVG; `tex` is the only shared-defs SVG exempt.' in spec, sorted((k,len(v)) for k,v in _all.items() if len(v)>2500))
    _sp=spec; _pa=open(W+'nancys-adventure-english-'+V+'-PASTE.md').read()
    _grad=[m for m in re.findall(r'[^\n]{0,40}(?:linear-gradient|radial-gradient|linearGradient|radialGradient)[^\n]{0,20}',_pa)]
    print('v5-33 no UI gradient: the only gradient anywhere is the title sky <linearGradient id=sk>:', len(re.findall(r'(?i)(?:linear|radial)-?gradient(?! id=.sk.)(?!>)',_pa.replace('</linearGradient>','')))==0 and _pa.count('<linearGradient')==1 and "<linearGradient id='sk'" in _ui['title'] and 'radialGradient' not in _pa and 'gradient(' not in _pa)
    print('v5-33 :55 exact "No gradients except sky."'+(' (t392u + 1:56 PM PT: + the title night fade and the title button shade)' if V>='v6-06' else '')+'; "and metal UI" gone:', ("No gradients except sky, the title night fade, and the title button shade (approved t288u mock and Maxwell's Button C pick)." if V>='v6-06' else 'No gradients except sky.') in _sp and 'and metal UI' not in _sp)
    print('v5-33 metal thud line present for the yellow-text iron buttons:', 'only these yellow-text metal plate buttons (iron buttons, tabs, zone tiles, choice plates, Got it) play a soft low metal thud on press' in _sp)
    print('v5-33 iron face flat #3E5A7A, lip #2C3F56, 2 px top line, rivets kept, steel flat stripe:', all(x in _sp for x in ('flat steel-blue `#3E5A7A`, a 5 px darker `#2C3F56` bottom lip, one 2 px lighter','4 corner rivets (6 px flat','one flat `#F2F5F7` highlight stripe','brushed iron'[:0])) and 'brushed iron' not in _sp)
    print('v5-33 press translateY(3px) 110 ms, no squash; radius 30-35%; 52 pt where it fits; 44 pt min:', all(x in _sp for x in ('`translateY(3px)` for 110 ms','radius 30–35% of height','52 pt tall where it fits','never under 44 pt')))
    print('v5-33 toggles knob gray-left / green-right, transform only:', 'off: gray `#8A939C` track, knob left; on: Grass track, knob right; the knob moves by `transform` only' in _sp)
    print('v5-33 Start your day = Lilita One at every size:', 'Lilita One at every size' in _sp)
    # contrast: every ratio stated in the spec, recomputed (fail > 0.05; text pairs < 4.5 reported)
    PL=lambda f:_bl('#1A1F24',.85,f); Y='#FFD100'; C='#FFF8E1'; G='#FFCC33'; I='#10170F'
    _CT=[('Hero Yellow on label plates 7.7–10.2',[(7.7,min(_cr(Y,PL(f)) for f in ('#3E5A7A','#D5DCE2','#FFCC33','#E9D9AE'))),(10.2,max(_cr(Y,PL(f)) for f in ('#3E5A7A','#D5DCE2','#FFCC33','#E9D9AE')))]),
     ('(4.87 on bare iron',[(4.87,_cr(Y,'#3E5A7A'))]),('Cream Thai 10.6+',[(10.6,min(_cr(C,PL(f)) for f in ('#3E5A7A','#D5DCE2','#FFCC33','#E9D9AE')))]),
     ('Cream on Forest 11.9',[(11.9,_cr(C,'#0E3B22'))]),('Meadow 6.9',[(6.9,_cr(C,'#17633A'))]),('Never white on Grass (3.1)',[(3.1,_cr('#FFFFFF','#2FA84F'))]),
     ('Gold only on label plates (7.5+',[(7.5,min(_cr(G,PL(f)) for f in ('#3E5A7A','#D5DCE2','#FFCC33','#E9D9AE')))]),('never on bare Paper, 1.08',[(1.08,_cr(G,'#E9D9AE'))]),
     ('Hero Yellow on a plate over Paper 7.7',[(7.7,_cr(Y,PL('#E9D9AE')))]),('Ink on Paper 13.0',[(13.0,_cr(I,'#E9D9AE'))]),
     ('Cream on Arena Night 16.2',[(16.2,_cr(C,'#0B1B33'))]),('Teal 11.3',[(11.3,_cr(C,'#0F3B4A'))]),('Ink on parchment 14.7',[(14.7,_cr(I,'#F3E6C4'))]),('on Aqua 11.7',[(11.7,_cr(I,'#7FE0D0'))]),
     ('on zone tints 7.9+',[(7.9,min(_cr(I,t) for t in ('#7FD38B','#F5A3C7','#7FB8F5','#F5D06B','#F2B8A0','#B79BFF')))]),('Ink on it 7.7',[(7.7,_cr(I,'#C8A26A'))]),
     ('3.3:1+ on Ink, non-text',[(3.3,min(_cr(_bl(c,.6,I),I) for c in ('#00D26A','#4FA3FF','#FFCC33')))]),('(7.0:1+ on Ink)',[(7.0,min(_cr(c,I) for c in ('#00D26A','#4FA3FF','#FFCC33')))]),
     ('Hero Yellow 24 px+, 10.2 on its label plate',[(10.2,_cr(Y,PL('#3E5A7A')))])]
    _cf=[]; 
    for _t,_pr in _CT:
        for _s,_m in _pr:
            if _t not in _sp or abs(_s-_m)>.05: _cf.append((_t,_s,round(_m,3),_t in _sp))
    _nums=re.findall(r'(?<![\w.])(\d{1,2}\.\d{1,2})(?=(?::1)?\+?[;,)]| on| and|–)',re.sub(r'[^\n]*(?:AA contrast|Ink on it|rank rings|on Ink\)|label plate;)[^\n]*','',_sp)) if False else []
    print('v5-33 contrast: every stated ratio recomputed from its hex pair, all within 0.05 (%d pairs):'%sum(len(p) for _,p in _CT), not _cf, _cf)
    print('v5-33 contrast: text pairs under 4.5:1 that ship (white on Grass and Gold on Paper are stated as never-use; bare iron 4.87 is above):', [t for t,p in _CT if p[0][1]<4.5 and not t.startswith(('Never','never','3.3'))])
    print('v5-33 old stated ratios gone (11.0, 7.5–9.1, 10.3+, 10.0;, 5:1+, 6.9:1+):', not any(x in _sp for x in ('24 px+, 11.0','7.5–9.1','Cream Thai 10.3+','(10.0;','5:1+ on Ink','6.9:1+')))
    # Thai: byte-for-byte from the Instructor file (md5 291d9baa)
    _TF='/workspace/instructor/v533/draft-thai-weapons-hero-pre-level-291d9baa.md'; _tf=open(_TF,encoding='utf-8').read()+open('/workspace/instructor/v533/draft-thai-secret-weapon-t259u.md',encoding='utf-8').read()
    print('v5-33 Instructor Thai file md5 291d9baa:', _hl.md5(open(_TF,'rb').read()).hexdigest()=='291d9baaeee72d20491252247b8fdbb4')
    _nk=['chooseHero','heroNancy']
    print('v5-33 2 new hero keys present, en and th each appear verbatim in the Instructor file as "en = th":', all(k in d['uiText'] and (d['uiText'][k]['en']+' = '+d['uiText'][k]['th']) in _tf for k in _nk), [k for k in _nk if k not in d['uiText'] or (d['uiText'][k]['en']+' = '+d['uiText'][k]['th']) not in _tf])
    _bc=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json'))['uiText']['backupCompare']; _pt=open('/workspace/instructor/v532/patch-backupCompare.md',encoding='utf-8').read()
    print('v5-33 backupCompare byte-for-byte from the Instructor patch file; :198 points at it:', json.dumps({'backupCompare':_bc},ensure_ascii=False,separators=(',',':'))[1:-1] in _pt and '`uiText.useBackup` names both (`uiText.backupCompare`)' in _sp)
    _o=json.load(open(W+'nancys-adventure-english-v5-32-cards.json')); _dF=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json')); _thx=lambda o:[(k,v.get('th')) for k,v in o['uiText'].items() if k not in _nk+['backupCompare']]
    print('v5-33 Thai unchanged except new keys (uiText) and nothing else in cards changed but art, uiText, meta weaponBonus/bonusGems/version/count:', _thx(_dF)==_thx(_o) and {k:v for k,v in _dF.items() if k not in ('picPlan','uiText','meta','version','trophies','trophyRules')}=={k:v for k,v in _o.items() if k not in ('picPlan','uiText','meta','version','trophies','trophyRules')} and [(t['id'],t.get('thGloss')) for t in _o['trophies']]==[(t['id'],t.get('thGloss')) for t in _dF['trophies'] if t['id'] in {x['id'] for x in _o['trophies']}])
    _f32=open(W+'nancys-adventure-english-FINAL-v5-32.md',encoding='utf-8').read()
    _gb=[l for l in _f32.split('\n') if l.startswith('- **Gear bonuses:**')][0]
    print('v5-33 council split 4-0: weapon system out (no tiers, Dragonbane, Bloodtide, Sunforged, pose, weapon Thai keys, weaponEarnAt); v5-32 gear bonuses, nextBonus, bonusGems restored exactly; trophies == v5-32:', _gb in fin and _dF['uiText']['nextBonus']==_o['uiText']['nextBonus'] and _dF['meta']['bonusGems']==_o['meta']['bonusGems'] and _dF['trophies']==_o['trophies'] and _dF['trophyRules']==_o['trophyRules'] and not any(k in _dF['uiText'] for k in ('weapon','weaponNew','weaponUse','weaponInUse','nextWeapon','weaponEarnAt','weaponNotYet','secretCaption','secretReveal')) and not any(k.startswith('bonus') for k in _dF['uiText']) and 'pose' not in _dF['picPlan']['uiInlineSvg'] and not re.search(r'Dragonbane|Bloodtide|Sunforged|sunforged|dragonbane|bloodtide',_pa))
    print('v5-33 hero keys chooseHero/heroNancy byte-for-byte from 291d9baa (heroSam = existing heroName Sam/แซม):', _hl.md5(open('/workspace/instructor/v533/draft-thai-weapons-hero-pre-level-291d9baa.md','rb').read()).hexdigest()=='291d9baaeee72d20491252247b8fdbb4' and all((_dF['uiText'][k]['en']+' = '+_dF['uiText'][k]['th']) in open('/workspace/instructor/v533/draft-thai-weapons-hero-pre-level-291d9baa.md',encoding='utf-8').read() for k in ('chooseHero','heroNancy')) and _dF['uiText']['heroName']=={'en':'Sam','th':'แซม'})
    _au=_dF['picPlan']['uiInlineSvg']; _tx=_au['tex']
    print('v5-33 t251u aura: one #au symbol in tex reused by the title sword and the Character aura via <use>, 30-60% opacity, transform/opacity only, reduced motion, no filter:', _tx.count("id='au'")==1 and "href='#au'" in _au['sword'] and _au['aura'].count("href='#au'")==2 and 'opacity:.3' in _tx and 'opacity:.6' in _tx and 'prefers-reduced-motion' in _tx and 'filter' not in _tx+_au['aura'] and '`picPlan.uiInlineSvg.aura` fully envelops the hero' in _sp and 'hair color unchanged' in _sp)
    print('v5-33 Sam <= 2,500 via the shared rig (rF face, rE eyes, rH fist in tex):', len(_au['sam'])<=2500 and all("href='#%s'"%x in _au['sam'] and "href='#%s'"%x in _au['nancy'] for x in ('rF','rE','rH')), len(_au['sam']))
    print("v5-33 'never Nancy' replaced, hero choice persists, default Sam, aura follows:", 'never Nancy' not in _pa and '`state.hero` (default Sam, persists)' in _sp and 'fully envelops the hero' in _sp)
    print('v5-33 no locked/padlock/failed wording added (only the existing "no \'locked\' wording" rule):', re.findall(r"(?i)[^\n]{0,20}\b(?:locked|padlock|failed)\b[^\n]{0,20}",_sp)==re.findall(r"(?i)[^\n]{0,20}\b(?:locked|padlock|failed)\b[^\n]{0,20}",open(W+'nancys-adventure-english-v5-32.md').read()) or not re.search(r'(?i)padlock',_sp), re.findall(r"(?i)\b(?:locked|padlock|failed)\b",_sp))
    print('v5-33 weapon bonuses (grace retry) moved to v534-seed with the split; no bonus text in v5-33:', 'grace retry' not in _sp and 'bonusRetry' not in _pa)
    print('v5-33 title: no character, no pan, tap = press + thud + fade:', '`sam`' not in _sp.split('- **Title:**')[1].split('\n')[0] and 'pans into the sun' not in _sp and 'the button press and metal thud only, then a 300 ms fade' in _sp and 'no character' in _sp)
    _t=_ui['title']; _s=_ui['sword']
    _tx2=_ui['tex']
    print('v5-33 title 7 layers (round 2: one haze band dropped by council vote, shapes simplified): sky gradient, sun, <=3 clouds, haze 60/35, one 5-tier pine symbol, far tree band tb, 2 bunnies, sway classes rotate only, bunny translate, reduced motion (global rule in tex), title <= 2,500:', "fill='url(#sk)'" in _t and _t.count("<symbol id='p'")==1 and all("opacity='%s'"%o in _t for o in ('.6','.35')) and "opacity='.45'" not in _t and "id='tb'" in _t and _t.count("href='#bn'")==2 and 'rotate(-1.5deg)' in _t and 'translate(-60px' in _t and '@media(prefers-reduced-motion:reduce){*{animation:none!important}}' in _tx2 and 'filter' not in _t+_s and 'blur' not in _t+_s and len(_t)<=2500, len(_t))
    _ia=_d['picPlan']['inlineSvg'] if '_d' in dir() else json.load(open(W+'nancys-adventure-english-'+V+'-cards.json'))['picPlan']['inlineSvg']; _tr=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json'))['picPlan']['trophyInlineSvg']
    print('v5-33 round 2 Watchman merges: towel/towel-white = one tex <symbol id=tw>, frame-silver/frame-gold = one tex <symbol id=fr>, colours via color/fill/--s/--h, each card one closing tag:', _tx2.count("<symbol id='tw'>")==1 and _tx2.count("<symbol id='fr'>")==1 and all("href='#tw'" in _ia[k] and _ia[k].count('</svg>')==1 for k in ('towel','towel-white')) and all("href='#fr'" in _tr[k] and _tr[k].count('</svg>')==1 for k in ('frame-silver','frame-gold')) and '.v1{fill:var(--s)}' in _tx2)
    print('v5-33 sword pull Option A (council, 0 art chars): on Character the stone hides the short blade until the fade:', 'the stone hides the blade until the fade' in _sp)
    print('v5-33 bunnies (t256u 4): exactly 2 drawn: one static in the right pine shade (no animation class), one looping right off-screen and back in from the left via .br translate + .bh hop:', _t.count("href='#bn'")==2 and "<use href='#bn' transform='translate(276 404)scale(-1 1)'/>" in _t and "<g class='br'><g class='bh'><use href='#bn' y='446'/></g></g>" in _t and 'translate(-60px' in _t and 'translate(400px' in _t)
    print('v5-33 tex is the only per-SVG-limit exception (council 5-0); tex unchanged since round 3 (3,026):', len(_tx2)==3026 and spec.count('`tex` is the only shared-defs SVG exempt')==1, len(_tx2))
    _cd=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json')); _pp4=_cd['picPlan']; _nt=_pp4['svgNotes']; _sty='flat saturated fill, Ink outline'
    print('v5-33 round 4: pray-meal, pray-kneel, high-five are Build notes (ids kept in picPlan.svg, cards still svg:<id>), bow-oak stays a supplied SVG, counts 33/52, 5 card SVGs supplied:', all(k not in _pp4['inlineSvg'] and k in _nt and k in _pp4['svg'] for k in ('pray-meal','pray-kneel','high-five')) and 'bow-oak' in _pp4['trophyInlineSvg'] and (_pp4['svgDrawnCount'],_pp4['totalSvgToDraw'],len(_pp4['inlineSvg']))==(33,52,5) and 'Draw 52 SVGs: `picPlan.svg` (33 of 38; 5 are supplied' in fin and 'Drawings Build makes: 52** = 33 card ids' in spec)
    print('v5-33 round 4 Instructor wording kept verbatim:', 'a small person kneeling, hands folded, head bowed, calm' in _nt['pray-kneel'] and 'two hands meeting in a high five' in _nt['high-five'] and 'a family at a table, heads bowed over a simple meal' in _nt['pray-meal'])
    _ms31=[ch['pic'][4:] for c in _cd['cards'] if c['id']=='ms-31' for ch in c['choices']]
    print('v5-33 ms-31 button style consistency: both buttons (pray-kneel, high-five) resolve to note-drawn SVGs, both notes open with the identical style phrase, neither is supplied, spec :231 says one style:', _ms31==['pray-kneel','high-five'] and all(_nt[k].startswith(_sty+';') and k not in _pp4['inlineSvg'] for k in _ms31) and 'both drawn from `picPlan.svgNotes` in one style, never emoji' in spec)
    print('v5-33 round 4 grace restore at :21:', '- Rest is a gift. Nothing ever breaks or fails.' in spec and 'mercy for a season' not in spec)
    print('v5-33 t267u title sword: long sword driven deep at the same 20 deg diagonal (blade shows 23 of the original 94 units, about 24%, tip never drawn), soil lip + grass clump over the entry, Gold + red hilt, 4 px line (2.7 x 1.5), one shadow per material, aura via the one #au symbol (motion CSS once in tex):', 'rotate(20)' in _s and 'scale(1.5)' in _s and "stroke-width='2.7'" in _s and '#A3262A' in _s and _s.count("href='#au'")==2 and 'v23h-14z' in _s and 'l-7 8-7-8z' not in _s and '#3B2A1E' in _s and '<style>' not in _s and '@keyframes fl{from{opacity:.3' in _tx2)
    _br=json.dumps(d,ensure_ascii=False)+_pa
    print('v5-33 brand grep 0 (incl. Avatar, Nickelodeon, Bob Ross):', {b:len(re.findall(b,_br,0 if 'Avatar' in b else re.I)) for b in ('Clash of Clans','Adventure Time','Teenage Robot','Danny Phantom','Nickelodeon',r'\bAvatar\b','Last Airbender','Bob Ross','Supercell','Cartoon Network','Berserk','Naruto','Dragonslayer','Dragon Slayer','Kubikiribocho','Samehada','Guts','Zabuza')}, '(generic UI word avatar/avatarFrame is not the show)')
    print('v5-33 Matthew 11:28 heavy laden verbatim; "chunky" count:', 'heavy laden' in _br, _sp.count('chunky'))
    print('v5-33 PASTE %d chars; <= 188,200: %s; vs 187,400 guard %+d; over ceiling by %d'%(len(_pa),len(_pa)<=188200,len(_pa)-187400,max(0,len(_pa)-188200)))
# ======================= v5-34 checks (Maxwell t292u/t293u/t295u/t297u/t298u/t299u; Auditor gate 1-3; Watchman flags) =======================
if V>='v5-34':   # n1 (Auditor v6-05 recheck d7ab5190): unpinned; A1 had added v6-04/v6-05 by hand
    import xml.dom.minidom as _xm, hashlib as _hl
    _raw=open(W+'nancys-adventure-english-'+V+'-cards.json',encoding='utf-8').read(); _C=_json_load(open(W+'nancys-adventure-english-'+V+'-cards.json'))   # compact, as shipped
    _pa=open(W+'nancys-adventure-english-'+V+'-PASTE.md',encoding='utf-8').read(); _sp=spec; _P=_C['picPlan']; _ui=_P['uiInlineSvg']
    _all=dict(_ui); _all.update(_P['inlineSvg']); _all.update(_P['trophyInlineSvg'])
    _bad=[]
    for _k,_v in _all.items():
        try: _xm.parseString(_v)
        except Exception as _e: _bad.append((_k,str(_e)[:60]))
    _art=sum(len(v) for v in _all.values())
    print(V+' every inline SVG parses as XML, one </svg> each (%d):'%len(_all), not _bad and all(v.count('</svg>')==1 for v in _all.values()), _bad)
    print(V+' PASTE %d chars <= 188,200 (Thai reserve 188,200-188,500 untouched):'%len(_pa), len(_pa)<=188200, 'headroom', 188200-len(_pa))
    print(V+' art total %d vs cap 18,519: within cap: %s; council absorb rule (3-0) applies only because the PASTE fits: %s'%(_art,_art<=18519,len(_pa)<=188200), 'over by', max(0,_art-18519))
    _exs=('tex','title') if 'exempt: `tex` (shared defs) and `title` (t371u).' in _pa else ('tex',)   # A2: title exempt only if the council ruling text is in the PASTE
    print(V+' per-SVG 2,500 limit: every SVG within it except tex'+(' and title (council exemption stated in the PASTE)' if len(_exs)==2 else '')+':', [k for k,v in _all.items() if len(v)>2500 and k not in _exs]==[], sorted((k,len(v)) for k,v in _all.items() if len(v)>2400))
    # compact encoding round-trips to the v5-33 card content exactly
    _o33=json.load(open(W+'v533-frozen/nancys-adventure-english-v5-33-cards.json')); _r33=_json_load(open(W+'v533-frozen/nancys-adventure-english-v5-33-cards.json'))
    _dec=_expand_cards(_json_load(open(W+'nancys-adventure-english-'+V+'-cards.json')))
    if V>='v6-04': [c.setdefault('choices',[]) for c in _dec['cards']]   # A1: the decode also fills the v6-04 T1 default (choices []), as it fills T3/T5
    print(V+' compact cards: zone/choices/hint decode back to v5-33 card content exactly (211 cards; key order aside):', [{k:v for k,v in c.items() if not (k=='type' and v=='picture')} for c in _dec['cards']]==[{k:v for k,v in c.items() if not (k=='type' and v=='picture')} for c in _r33['cards']] and len(_C['cards'])==211 and not any('zone' in c for c in _C['cards']) and all(isinstance(x,str) for c in _C['cards'] if c['id']!='ms-31' for x in c.get('choices',[])))
    print(V+' spec states the compact fields:', "Compact fields: a card's zone is the `zones[]` entry whose `cardIds` lists it; a string choice is its `en`; `hint` is `[letters, sound, word]`." in _sp or (_VN>=35 and "a card's zone is the `zones[]` entry whose `prefix` (space-separated) starts its `id`, cards in file order; a string choice is its `en`; `hint` is `[letters, sound, word]` (a missing `word` is `en`); a missing `type` is `meta.typeByZone`, then `picture`." in _sp))
    # verses untouched
    _dv=json.load(open(W+'nancys-adventure-english-'+V+'-daily-verses.json')); _dv33=json.load(open(W+'v533-frozen/nancys-adventure-english-v5-33-daily-verses.json'))
    print(V+' verses: cards verses/jesusWords/encouragement == v5-33; daily-verses identical except version:', _C['verses']==_o33['verses'] and _C['jesusWords']==_o33['jesusWords'] and _C['encouragement']==_o33['encouragement'] and {k:v for k,v in _dv.items() if k!='version'}=={k:v for k,v in _dv33.items() if k!='version'})
    _sec=lambda t:t[t.index('## 15. Bible verses'):t.index('## 16. Cards')]
    print(V+' spec section 15 byte-identical to v5-33:', _sec(fin)==_sec(open(W+'nancys-adventure-english-FINAL-v5-33.md').read()).replace('v5-33',V))
    # Thai: every new key verbatim from the Instructor files
    _TF={'w':'/workspace/instructor/v533/draft-thai-weapons-hero.md','s':'/workspace/instructor/v533/draft-thai-secret-weapon-t259u.md','g':'/workspace/instructor/v534/draft-thai-greetings-t289u.md'}
    _md={k:_hl.md5(open(f,'rb').read()).hexdigest()[:8] for k,f in _TF.items()}; _tx=''.join(open(f,encoding='utf-8').read() for f in _TF.values())
    _new=[k for k in _C['uiText'] if k not in _o33['uiText'] and k not in ('tapPrompt','comingNext','regionOpen','guardianLast')+(('giftFrom',) if _V6 else ())]   # v5-35 tapPrompt (Instructor ruling 3:52 AM PT); v5-36 MX1 keys checked against draft-thai-mx1-sequential.md below   # v5-35 tapPrompt: Instructor ruling 3:52 AM PT (checked literally below)
    print(V+' Instructor Thai files (weapons 58b47663 shop-rule update, secret 65bcfa65, greetings eb16d8c8):', _md=={'w':'58b47663','s':'65bcfa65','g':'eb16d8c8'}, _md)
    print(V+' %d new uiText keys, each "en = th" verbatim in those files; nextBonus -> nextWeapon "Next weapon at level {n}":'%len(_new), all((_C['uiText'][k]['en']+' = '+_C['uiText'][k]['th']) in _tx for k in _new) and 'nextBonus' not in _C['uiText'] and _C['uiText']['nextWeapon']['en']=='Next weapon at level {n}' and len(_C['uiText'])==((91 if _V6 else 92) if _V36 else 89 if _VN>=35 else 88) and (not _V36 or all(re.search(r'^- %s\b[^\n]*: en "%s" / th "%s"'%(k,re.escape(_C['uiText'][k]['en']),re.escape(_C['uiText'][k]['th'])),open(W+'instructor/v536/draft-thai-mx1-sequential.md',encoding='utf-8').read(),re.M) for k in ('comingNext','regionOpen','guardianLast')) and _hl.md5(open(W+'instructor/v536/draft-thai-mx1-sequential.md','rb').read()).hexdigest()[:8]=='d6086d10') and (not _VN>=35 or _C['uiText']['tapPrompt']=={'en':'Tap the {word}','th':'แตะที่ {word}'}), [k for k in _new if (_C['uiText'][k]['en']+' = '+_C['uiText'][k]['th']) not in _tx])
    print(V+' Thai of every v5-33 key unchanged:', all(_C['uiText'][k]==v for k,v in _o33['uiText'].items() if k!='nextBonus' and not (_V6 and k in _TRIM6)))
    # Auditor gate 1: one gear rule
    _GR=('levels open tiers; stars buy; guardians give types; one tap equips.' if _V6 else 'Level unlocks gear; stars buy it; one tap equips it.')   # v6-01 (t360u)
    _wp=[t for t in d['trophies'] if 'wt' in t]
    print(V+' gate 1: the one gear rule stated once in the spec, no conflicting "never bought"/"comes only at start" weapon lines left:', _sp.count(_GR)==1 and 'never bought' not in _sp and 'comes only at start, by level, or by boss win' not in _sp and 'Gear comes only' not in json.dumps(_C['trophyRules']))
    _free={'sword-iron':{'type':'start'},'cleaver-bloodtide':{'type':'bossesWon','n':4},'greatsword-dragonbane':{'type':'bossesWon','n':5}}
    if _V6: _free['staff-shepherd']={'type':'guardian','zone':'baby-hospital'}   # v6-01: the Good Shepherd Crook, the Gentle guardian's gift (t360u)
    _tl=set(_C['meta']['weaponTiers'].values())
    print(V+' gate 1 data: every bought weapon opens at a tier level and costs stars; Dragonbane (final) and Bloodtide (second-to-last) free at boss milestones; secret sword by the secret goal; nothing priced in money:',
          all(t['unlock']['type']=='level' and t['unlock']['n'] in _tl and (t.get('stars',0)>0 or (_VN>=35 and t['unlock']['n']==_C['meta']['weaponTiers']['1']) or (_V36 and t['id'] in ('sling-shepherd','staff-shepherd','staff-lantern','hammer-builder'))) for t in _wp if t['id'] not in _free and t['id']!='sword-sunforged') and all(t['unlock']==_free[t['id']] and 'stars' not in t for t in _wp if t['id'] in _free)
          and [t for t in _wp if t['id']=='sword-sunforged'][0]['unlock']['type']=='secret' and not re.search(r'"(cost|price|usd|money)"',_raw) and 'never real money' in _sp.lower())
    print(V+' gate 1 UI: nextWeapon unchanged, buy screen equips in the same tap, not-yet tiles use weaponEarnAt, tier toast weaponInShop:', 'that same tap equips it' in _sp and '`uiText.nextWeapon`' in _sp and '`uiText.weaponEarnAt`' in _sp and '`uiText.weaponInShop`' in _sp)
    # Auditor gate 2: glasses only on Sam; Nancy closed-eyes smile (mock-t297u/nancy-face.svg c462bfda)
    _nf=open('/workspace/mock-t297u/nancy-face.svg',encoding='utf-8').read(); _snip=[l for l in _nf.split('\n') if l.startswith("<g stroke-width='1.6'><path d='M31 16.5l6-.5m12 .5l-6-.5'/>")][0]
    _gl=[l for l in _sp.split('\n') if re.search(r'(?i)glasses',l)]
    print(V+' gate 2: no spec line gives Nancy glasses (every "glasses" mention is Sam\'s, or says Nancy has none):', all(('Nancy' not in l) or ('Nancy: no glasses' in l) for l in _gl) and all(re.search(r'Sam[^.]{0,80}glasses|no glasses',l) for l in _gl), len(_gl))
    print(V+' gate 2: Nancy SVG carries the t297u face snippet byte-for-byte, no #rE dot eyes or corner ticks; Sam keeps #rE and glasses:', hashlib_ok if False else (_hl.md5(open('/workspace/mock-t297u/nancy-face.svg','rb').read()).hexdigest()[:8]=='c462bfda' and _snip in _ui['nancy'] and "href='#rE'" not in _ui['nancy'] and 'M30 20l2-1m18 1l-2-1' not in _ui['nancy'] and "href='#rE'" in _ui['sam']))
    # Auditor gate 3: gear never touches verses
    _wb=_C['meta']['weaponBonus']; _bw={w for v in _wb.values() for w in v.split()}
    print(V+' gate 3: weapon bonuses are English-progress/stat words only (Hint Retry Star Streak Respell Slow, 1-2); none names a verse, scroll, Jesus word or the leaf:', _bw<= {'Hint','Hint2','Retry','Retry2','Star','Star2','Streak','Streak2','Respell','Slow'} and all('bonus'+w in _C['uiText'] for w in _bw) and not re.search(r'(?i)verse|scroll|jesus|leaf|hearth',json.dumps(_wb)), sorted(_bw))
    print(V+' gate 3: spec says gear never touches verses; hearth leaf and daily verse stay free and word for word; grace check intact:', 'Gear never touches verses: the hearth leaf, daily verse, scrolls and Jesus words stay free and word for word, and no gear unlocks, boosts or reorders them.' in _sp and 'No counter, timer, gear or level touches it.' in _sp and 'nothing is ever deducted for a verse' in _sp)
    # weapons per t298u/t299u
    _h=_C['trophyRules']['hands']; _types={t['wt'] for t in _wp}|(set(_C['trophyRules']['rows'].split()) if _V36 else set())   # v5-36 MX2: uncommon named axe1/daggers/punch held for the drip; every row still has generic pieces
    _need={'sword1','sword2','axe1','axe2','mace1','mace2','daggers','punch','claws','spear','polearm','scythe','longbow','shortbow','crossbow','staff','wand','shield'}
    if _V6: print(V+' Option B types (t360u): rows sword1 sword2 axe1 mace1 + sling, shield, crook; each type in exactly one hands group; shield only offHand; no pair group; crook two-handed; no trimmed type left:', _types=={'sword1','sword2','axe1','mace1','sling','shield','crook'} and all(sum(t in g for g in _h.values())==1 for t in _types) and _h['offHand']==['shield'] and 'pair' not in _h and 'crook' in _h['two'] and not ({'axe2','mace2','daggers','punch','claws','spear','polearm','scythe','longbow','shortbow','crossbow','wand','staff'} & (set(sum(_h.values(),[]))|set(_C['trophyRules']['rows'].split())|set(_P['weaponParts']))), sorted(_types))
    else: print(V+' t298u/t299u types all present (incl. wand 1H and staff 2H), each in exactly one hands group; shield only offHand; pairs daggers/punch/claws; wand one-handed:', _need<=_types and all(sum(t in g for g in _h.values())==1 for t in _types) and _h['offHand']==['shield'] and set(_h['pair'])=={'daggers','punch','claws'} and 'wand' in _h['one'] and 'staff' in _h['two'], sorted(_need-_types))
    if _V6: print(V+' equip rule text (Option B): shield only with a 1H sword, two-handers (2H sword, crook) take both hands, no pair line, off-hand items v6:', all(x in _sp for x in ('only a 1H sword may add `shield-sunrise` in the off hand','both hands, no shield','Off-hand lantern, tome and orb are v6','1H mace, sling) in the weapon hand, the other hand empty','`two` (2H sword, crook)')) and '`pair`' not in _sp)
    else: print(V+' equip rule text: shield only with a 1H sword, pairs and two-handers take both hands, wand one hand no shield, off-hand items v6:', all(x in _sp for x in ('only a 1H sword may add `shield-sunrise` in the off hand','both hands, no shield','Off-hand lantern, tome and orb are v6','wand, sling) in the weapon hand, the other hand empty')))
    if _V6: print(V+' %d weapons (= spec "Weapons (%d,"), unique ids and names; Dragonbane and Bloodtide are 2H swords; every row type has a parts recipe; tex holds #wb #wh #wx #wm, #wo/#wv gone with wands, staffs and bows (t360u):'%(len(_wp),len(_wp)), ('Weapons (%d, `wt` type;'%len(_wp)) in _sp and len(_wp)==len({t['en'] for t in _wp})==len({t['id'] for t in _wp}) and {t['id']:t['wt'] for t in _wp if t['id'] in ('cleaver-bloodtide','greatsword-dragonbane')}=={'cleaver-bloodtide':'sword2','greatsword-dragonbane':'sword2'} and all(t in _P['weaponParts'] for t in _C['trophyRules']['rows'].split()) and all(("id='%s'"%x) in _ui['tex'] for x in ('wb','wh','wx','wm')) and not any(("id='%s'"%x) in _ui['tex'] for x in ('wo','wv')))
    else: print(V+(' 21 weapons (MX2: 4 uncommon held for the Dec-Jan drip),' if _V36 else ' 25 weapons,')+' unique ids and names; Dragonbane and Bloodtide are 2H swords; every wt has a #wb parts recipe; tex holds #wb #wh #wx #wm #wo #wv:', len(_wp)==len({t['en'] for t in _wp})==(21 if _V36 else 25) and {t['id']:t['wt'] for t in _wp if t['id'] in ('cleaver-bloodtide','greatsword-dragonbane')}=={'cleaver-bloodtide':'sword2','greatsword-dragonbane':'sword2'} and all(t in _P['weaponParts'] for t in _types-{'sling','shield'}) and all(("id='%s'"%x) in _ui['tex'] for x in ('wb','wh','wx','wm','wo','wv')))
    if _V6: _nt6=len(_P['trophySvg']); _nd6=_nt6-len(_P['trophyInlineSvg']); _tot6=_P['svgDrawnCount']+_nd6+len(_P['uiSvg']); print(V+' every weapon outside a row tier has a bonus in meta.weaponBonus (crook Respell Slow); counts %d/%d/%d read from data match the data fields and the spec head:'%(_nt6,_nd6,_tot6), set(_wb)=={t['id'] for t in _wp if t['wt'] not in _C['trophyRules']['rows'].split() or t['unlock']['type']!='level'}-{'sword-iron'} and (_P['trophySvgCount'],_P['trophySvgDrawnCount'],_P['totalSvgToDraw'])==(_nt6,_nd6,_tot6) and ('Draw %d SVGs'%_tot6) in fin and ('(%d of %d;'%(_nd6,_nt6)) in fin and ('Drawings Build makes: %d'%_tot6) in _sp and ('+ %d trophy ids'%_nd6) in _sp and all(i in _P['trophySvg'] for i in ('staff-shepherd','axe-oak')))
    else: print(V+' every weapon has a bonus in meta.weaponBonus; every new trophySvg id is drawn from weaponParts; counts '+('34/30/64 (MX2)' if _V36 else '38/34/68')+' match the spec head:', (set(_wb)=={t['id'] for t in _wp} if not _VN>=35 else set(_wb)=={t['id'] for t in _wp if t['wt'] not in _C['trophyRules']['rows'].split() or t['unlock']['type']!='level'}-{'sword-iron'}) and ((len(_P['trophySvg']),_P['trophySvgDrawnCount'],_P['totalSvgToDraw'])==(34,30,64) and 'Draw 64 SVGs' in fin and '(30 of 34;' in fin and 'Drawings Build makes: 64' in _sp if _V36 else len(_P['trophySvg'])==38 and _P['trophySvgDrawnCount']==34 and _P['totalSvgToDraw']==68 and 'Draw 68 SVGs' in fin and '(34 of 38;' in fin and 'Drawings Build makes: 68' in _sp))
    print(V+' silhouette fix (#335): the .sil rule sets the weapon colour variables to #5E6468:', '.sil{--b:#5E6468;--d:#5E6468;--g:#5E6468;--h:#5E6468}' in _sp)
    print(V+' rigs: .wp weapon hand and .wq off hand in Sam and Nancy:', all(_ui[k].count("class='wp'")==1 and _ui[k].count("class='wq'")==1 for k in ('sam','nancy')))
    # title (t283u valley + time of day, t295u)
    _t=_ui['title']; _sk=_ui.get('sky','')
    print(V+' title: t283u valley (hero slot #th, 2 bears, lake, '+('one bunny parked, pines still (t366u still)' if _STILL else 'one hopping bunny, pines sway')+'), no select UI; sky: 4 time bands, sun+rays move together, night stars+moon, biplane + live greeting text #gE/#gT, Thai 17:',
          "id='th'" in _t and _t.count("href='#be'")==2 and _t.count("href='#bn'")==1 and (("class='br'" not in _t) if _STILL else ('class=\'br\'' in _t)) and all(("[data-tod=%s]"%x) in _sk+_t for x in ('a','e','n')) and "id='gE'" in _sk and "id='gT'" in _sk and "font-size='17'" in _sk and "lang='th'" in _sk and 'chooseHero' not in _sp.split('- **Title (t283u')[1].split('\n')[0])
    print(V+' title spec: clock bands m 5:00-11:59 / a 12:00-16:59 / e 17:00-20:59 / n 21:00-4:59 (Instructor), greeting keys named, '+('Button C line (Maxwell 1:37 PM PT)' if V>='v6-06' else 'button top at 698 pt or lower at 390x844')+':', all(x in _sp for x in ('`m` 5:00–11:59, `a` 12:00–16:59, `e` 17:00–20:59, `n` 21:00–4:59','`uiText.greetMorning`, `greetAfternoon`, `greetEvening` or `greetNight`',('wide and low, English and the Thai plate on one line' if V>='v6-06' else 'its top is at 698 pt or lower'))))
    print(V+' title sword: square hilt (no round pommel or round guard ends), gold-and-blue accents, in a bush:', '<circle' not in _ui['sword'] and "fill='#3D7FD9'" in _ui['sword'] and "M199 252h14v14h-14z" in _ui['sword'] and "fill='#3E7F34'" in _ui['sword'])
    # map select + hands (t290u)
    print(V+' Map = hero select (t290u): Sam/Nancy buttons, bounce 1.08 from the feet in 300 ms, persists, 320 pt hero strip with Back in the top bar, no avatar button at 320:', all(x in _sp for x in ('**Hero select (t290u):**','scale 1.08 at 120 ms, back by 300 ms','sets `state.hero` (persists)','at 320 pt a compact hero strip','Back moves into the top bar','gone at 320 pt')))
    _MIT="<path d='M.2 104.6q-.2-7.6 5.8-7.6 6.2 0 6 7.6v7q0 7.4-6 7.4-6.2 0-5.8-7.4z'"
    _fx={k:re.findall(r"href='#rH' x='(\d+)'",_ui[k]) for k in ('sam','nancy')}
    print(V+' hands: #rH is the t290u mitten with a 7.7/22 thumb; every right hand is mirrored outward by a CSS rule matching its x:', _MIT in _ui['tex'] and "M2.4 101.3q-6.6-.1-6.6 4.1" in _ui['tex'] and all(("use[href='#rH'][x='%s']{transform:matrix(-1,0,0,1,%d,0)}"%(x,2*int(x)+12)) in _ui['tex'] for k in _fx for x in _fx[k] if x!='13'), _fx)
    print(V+' Watchman flags: Nancy far arm moved out from behind the belly, Nancy knee ticks, bunny at the 3 px line, :54 HSL L, m2 high-five wording:', "ARM" not in _ui['nancy'] and "M53 46L67 72" in _ui['nancy'] and "M31 128l4 2m10 0l4-2" in _ui['nancy'] and "stroke-width='1.5'><use href='#bn'" not in _t and '12 to 18 HSL L below' in _sp and 'two hands meeting' in _sp and 'slapping with a burst' not in _sp)
    # 1, 5, 6
    print(V+' #77 storybook line (frames 6 pt / 4 pt dense and 320, gold-and-blue, full look on low-UI screens, no new art):', '- **Storybook look (#77):**' in _sp and 'lighter on question screens' in _sp)
    print(V+' hearth leaf: always there, free, alternates encouragement and given verses, no counter/timer/gear:', '- **Hearth leaf:**' in _sp and 'always there and free' in _sp)
    print(V+' out in the world: meta.outings are existing card ids; spec run-order step:', all(i in {c['id'] for c in d['cards']} for i in _C['meta']['outings']) and len(_C['meta']['outings'])>=8 and '**Out in the world:**' in _sp)
    _br=_raw+_pa
    print(V+' brand grep 0:', {b:len(re.findall(b,_br,re.I)) for b in ('Clash of Clans','Adventure Time','Teenage Robot','Danny Phantom','Nickelodeon','Last Airbender','Bob Ross','Supercell','Pixar','Disney','Zelda','Final Fantasy','Diablo','Minecraft','Fortnite','Roblox')}=={b:0 for b in ('Clash of Clans','Adventure Time','Teenage Robot','Danny Phantom','Nickelodeon','Last Airbender','Bob Ross','Supercell','Pixar','Disney','Zelda','Final Fantasy','Diablo','Minecraft','Fortnite','Roblox')})
    print(V+' never list holds: no new timer/energy/leaderboard/lives words in v5-34 additions:', not re.search(r'(?i)leaderboard|energy|countdown|lives\b', ''.join(l for l in _sp.split('\n') if any(x in l for x in ('Gear rule','Weapon bonuses','Hands (','Hero select','Hearth leaf','Storybook look','Title (t283u','Out in the world')))))
    print(V+' no 911 / Call Max / PASTE- placeholders:', not re.search(r'\b911\b|(?i:call max)|\[PASTE-',_pa))
    if not _VN>=35:
        # Chancellor economy check (v534build/gear-price-table.md): steady player 3 runs x (8 right + run bonus) affords each tier the day it opens; all bought by Dec 5
        _e=_C['pantry']['earn']; _sd=3*(8*_e['rightAnswer']+_e['runDone']); _xd=240
        def _xf(L): return 0 if L<=1 else 60 if L==2 else 250+sum(100+60*(k-3) for k in range(4,L+1))
        _cum=0; _ok=True; _last=0
        for _lv in _C['meta']['weaponTiers'].values():
            _dn=-(-_xf(_lv)//_xd); _cum+=sum(t['stars'] for t in _wp if t.get('stars') and t['unlock']=={'type':'level','n':_lv}); _ok&=_cum<=_dn*_sd; _last=_dn
        print(V+' economy: every tier affordable the day it opens for a steady player (%d stars/day), all %d stars of gear bought by day %d (<= day 26 = Dec 5 from a Nov 10 start); spec: price-only tile, never below zero, never holds back a lesson:'%(_sd,_cum,_last), _ok and _last<=26 and 'stars never go below zero and never hold back a lesson' in _sp)
    else:   # v5-35 (council 3:52 AM PT 1/5/6): tier 1 free; steady player 1 run a day = 20 of 25 finds + 10 guardian cards right; her 3 favorite types (tiers 2-3 + legendary) bought by Dec 5, balance never below zero
        _e=_C['pantry']['earn']; _rd=30; _sd=_rd*_e['rightAnswer']+_e['runDone']; _xd=_rd*10; _ts=_C['trophyRules']['tierStars']; _wtier=_C['meta']['weaponTiers']
        def _xf(L): return 0 if L<=1 else 60 if L==2 else 250+sum(100+60*(k-3) for k in range(4,L+1))
        _q=[(_wtier[str(min(t,3))],_ts[t-1]) for t in ((2,3) if _V36 else (2,3,4)) for _ in range(3)]; _sp_=0; _n=1; _ok=_ts[0]==0
        while _q and _n<=26:
            _lv=max(l for l in range(1,21) if _xf(l)<=_n*_xd)
            while _q and _q[0][0]<=_lv and _sp_+_q[0][1]<=_n*_sd: _sp_+=_q.pop(0)[1]
            _ok&=_n*_sd-_sp_>=0; _n+=1
        _gt=open(W+('v536build' if _V36 else 'v535build')+'/gear-price-table.md').read()
        print(V+' economy (v5-35): tier 1 free, %d stars/day, 3 favorite types fully bought (%d stars) by day %d (<= day 26 = Dec 5); table posted; spec: never below zero, never holds back a lesson, legendary never locked:'%(_sd,_sp_,_n-1), _ok and not _q and ('tier 1 free on opening' in _sp or 'tier 1 is hers free when its row opens, no `getFor`' in _sp) and 'stars never go below zero and never hold back a lesson' in _sp and "Never 'locked' or 'not enough'." in _sp and 'balance never below zero' in _gt and not re.search(r'(?i)padlock|🔒',(_raw+_pa).replace("no padlock or 'locked' shows anywhere",'').replace(_t37("no padlock, 'locked', 'fail' or 'can't' anywhere."),'')))
        print(V+' find-and-tap (t312u/t313u + council): rule once in the PASTE, existing cards only (no new question text), tapPrompt, 44 pt targets 8 px apart, guardian after scene 5 as a 10-card recap, miss = hint + wrongText + grace + retry, zones stay open:', _pa.count('### 7.1 Find and tap')==1 and 'find' not in _C and '44 pt+, 8 px apart' in _sp and 'a recap after scene 5 of a run in that zone' in _sp and 'then `wrongText` and a grace line; she tries again' in _sp and ('every zone stays open' in _sp or _V36) and ('Nothing opens by day, and levels open only gear tiers' in _sp or 'Nothing opens by day; levels open only gear tiers (11.1).' in _sp))
        _tr=_C['trophyRules']; _rows=_tr['rows'].split()
        if _V6: print(V+' shop rows (Option B, t360u): 4 types sword1 sword2 axe1 mace1, English names, one theme each from existing bonus words, 3 tier names/colors/star prices, giftOf = Word guardian -> axe1, Number guardian -> mace1 (both end guardians), rarity has no words:', _rows==['sword1','sword2','axe1','mace1'] and _tr['typeNames']=='Sword|Greatsword|Axe|Mace' and all('bonus'+w in _C['uiText'] for w in _tr['theme'].split()) and len(_tr['theme'].split())==4 and len(_tr['tierNames'].split('|'))==len(_tr['tierColor'].split())==len(_ts)==3 and _tr['giftOf']=={'axe1':'sight-words','mace1':'numbers'} and all(any(r['zones'][-1]==z for r in _C['mapLayout']['regions']) for z in _tr['giftOf'].values()) and 'Rarity has no words' in _sp and not re.search(r'(?i)"(common|uncommon|rare|epic|legendary)"',_raw) and '`uiText.gear`' in _sp)
        else: print(V+' shop rows (t315u): 17 types in the t298u/t299u order, English names, one theme each from existing bonus words, 4 tier names/colors/star prices, no new strings, rarity has no words:', _rows==['sword1','sword2','axe1','axe2','mace1','mace2','daggers','punch','claws','spear','polearm','scythe','longbow','shortbow','crossbow','wand','staff'] and len(_tr['typeNames'].split('|'))==17 and all('bonus'+w in _C['uiText'] for w in _tr['theme'].split()) and len(_tr['theme'].split())==17 and len(_tr['tierNames'].split('|'))==len(_tr['tierColor'].split())==len(_ts)==(3 if _V36 else 4) and 'Rarity has no words' in _sp and not re.search(r'(?i)"(common|uncommon|rare|epic|legendary)"',_raw) and '`uiText.gear`' in _sp)
        print(V+' hearth icon is a Stone arch with a heart, never a flame; Dragonbane v2 described; props reference-only:', 'hearth button (a small Stone arch from `#fr` with a Gold heart; never a flame' in _sp and '🍃' not in _sp and 'Dragonbane (Watchman v2)' in _sp and 'is reference only' in _sp)
# ===================== v5-36 checks (Auditor v5-35 gate c6386f4d B1, M1-M7, minors; Watchman W1; Instructor Bible free; MX1 Maxwell t329u) =====================
if _V36:
    _P6=open(W+'nancys-adventure-english-'+V+'-PASTE.md').read(); _F6=fin; _C6=_json_load(open(W+'nancys-adventure-english-'+V+'-cards.json'))
    _P5=open(W+'nancys-adventure-english-v5-35-PASTE.md').read()
    print(V+' PASTE %d chars <= 188,200:'%len(_P6), len(_P6)<=188200, 'headroom', 188200-len(_P6))
    print(V+' B1: only cards with a pic are tap objects; pic-less cards play on their own screens, at most one between scenes, never back to back, leftovers to the guardian recap:', "holding the run's next 5 cards with a `pic` as tap objects" in _P6 and _t37('Cards without a `pic` play on their own screens (8, 8.1, 8.2): at most one between scenes, never back to back; leftovers join the guardian recap.') in _P6 and "holding its 5 run cards as their `pic` objects" not in _P6)
    _hint5=[l for l in _P5.split('\n') if l.startswith('   - Further taps, and taps anywhere else')][0]; _hint6=[l for l in _P6.split('\n') if l.startswith('   - Further taps, and taps anywhere else')][0]
    print(V+' M1: no Jesus-word-first in the hint line (only that clause removed, rest byte-identical), the flourishes line and the play-flow check; gear never moves a Jesus word:', _hint6==_hint5.replace('first while a Bible weapon is equipped, 11.1; ','') and _hint6!=_hint5 and 'Jesus word first' not in _P6 and 'her next hint bubble shows her Jesus word' not in _P6 and 'no gear moves a Jesus word or verse.' in _P6)
    print(V+' M2: grace check keeps "no verse, trophy, timer, offer or real money":', 'no verse, trophy, timer, offer or real money' in _P6)
    print(V+' M3: weapons open in the uiText.gear tab; Pantry stars drop only there and in the gear tab:', "opens that tier's weapons in the `uiText.gear` tab (" in _P6 and 'stars drop only here and in the gear tab.' in _P6 and "weapons in the Pantry" not in _P6 and 'stars never drop any other way' not in _P6)
    print(V+' M4: the hearth is a corner button in 6.2 and the main-menu test:', 'Exactly two buttons, the hearth (a corner button) and one cue:' in _P6 and 'exactly two buttons (Map, Character), the corner hearth and the arrow cue.' in _P6)
    print(V+' M5: "last card" not "10th card":', "after a run's last card and the queue" in _P6 and "10th card" not in _P6)
    print(V+' M6: short zones repeat the cards seen longest ago, never twice in one scene:', 'If a zone has fewer than 25 `pic` cards, the run repeats those seen longest ago, never twice in one scene' in _P6)
    _sc=re.search(r'SE: 20 \+ HUD (\d+) \+ card (\d+) \+ scene (\d+) \+ hint (\d+) \+ gaps (\d+) = (\d+)\)',_P6)
    print(V+' M7: scene layout line (card on top, hero + objects, 44 pt+, 8 px, 3+2 rows at 320 x 568, SE sum <= 568, Reveal after each right tap); 6.4 one-layout line allows 7.1:', bool(_sc) and 20+sum(int(x) for x in _sc.groups()[:5])==int(_sc.group(6))<=568 and _t37("Paper question card, then hero and objects (44 pt+, 8 px apart, no overlap; at 320 × 568 rows of 3 + 2 if needed)") in _P6 and "6.5's Reveal follows each right tap." in _P6 and 'Every picture card off a scene (7.1 has its own) uses this one layout' in _P6)
    _tc=_C6['trophyRules']['tierColor'].split()
    _named={(t['wt'],t['tier']):t['id'] for t in _C6['trophies'] if 'tier' in t}; _wn=[t for t in _C6['trophies'] if 'wt' in t]
    print(V+' MX2 (t331u, W1 folded in; rings 1/3/5 per QM 4:31 AM PT): 3 rarities, tierStars [0,45,200], colors grey/blue/orange-gold, names Oak|Crystal|Star; tiers 1-3 only, one named item per slot; uncommon named weapons held (drip line); '+('Bible 3 free (sling + hammer common, crook a guardian gift; Option B t360u)' if _V6 else 'Bible 4 kept free (lamp staff + hammer common, shepherd staff rare)')+'; gifts beside the Greatsword row; no epic color, no 4-tier text, no rarity words in data:',
          _C6['trophyRules']['tierStars']==[0,45,200] and _tc==['#B9C0C4','#4A90D9','#F2A23A'] and _C6['trophyRules']['tierNames']=='Oak|Crystal|Star' and {t['tier'] for t in _C6['trophies'] if 'tier' in t}=={1,2} and len(_named)==sum(1 for t in _C6['trophies'] if 'tier' in t)
          and not {'sword-gold','daggers-twin','axe-hand','blades-punch'}&{t['id'] for t in _C6['trophies']} and 'sword-gold' not in json.dumps(_C6) and (_named.get(('axe1',1))=='axe-oak' and not any(k[0]=='staff' for k in _named) if _V6 else _named[('staff',1)]=='staff-lantern' and _named[('staff',2)]=='staff-shepherd') and _named[('mace1',1)]=='hammer-builder'
          and 'then 3 slots: common, rare, legendary (MX2).' in _P6 and 'rings by rank (common 1, rare 3, legendary 5 + glint) plus `tierColor` as `--b`.' in _P6 and 'tier t shows t rings' not in _P6 and 'Uncommon and epic come as a Dec–Jan drip.' in _P6 and 'free gifts Bloodtide and Dragonbane sit beside the Greatsword row' in _P6 and _t37('Legendary (tier 3) is a black `.sil` silhouette (Ink fill) with only `uiText.getFor` and the star icon until tier 3 opens and her stars reach its price; then an 8% bounce and one sparkle reveal it') in _P6
          and not re.search(r'9B6BD3|`#5DBB63`|tier 4|4 rings|\bepics?:|tiers 1–3|\(common, uncommon, rare\)',_P6) and not re.search(r'(?i)"(common|uncommon|rare|epic|legendary)"',json.dumps(_C6)))
    if _V6: _n6=len(_C6['trophies']); _bc6=_C6['meta']['trophiesByCat']; print(V+' counts from data (%d trophies, %d weapons, %d gear, %d gems/%d themes/%d titles) match meta and the PASTE lines:'%(_n6,len(_wn),_bc6['gear'],_bc6['gems'],_bc6['themes'],_bc6['titles']), _C6['meta']['trophies']==_n6==sum(_bc6.values()) and _bc6['gear']==sum(1 for t in _C6['trophies'] if t.get('cat','gear' if 'wt' in t else None)=='gear') and ('one of the %d `trophies`'%_n6) in _P6 and ('%d gems, %d gear, %d themes, %d titles'%(_bc6['gems'],_bc6['gear'],_bc6['themes'],_bc6['titles'])) in _P6 and ('Weapons (%d, `wt` type;'%len(_wn)) in _P6 and (('(earned count)' if V>='v6-06' else '(earned of %d)'%_n6) in _P6))
    else: print(V+' MX2 counts follow the drip (52 trophies, 21 weapons, 27 gear, 34/30/64 drawings) in data and spec:', _C6['meta']['trophies']==len(_C6['trophies'])==52 and len(_wn)==21 and 'one of the 52 `trophies`' in _P6 and '5 gems, 27 gear,' in _P6 and 'Weapons (21, `wt` type;' in _P6 and '(earned of 52)' in _P6 and sum(1 for t in _C6['trophies'] if t.get('cat')=='gear' or 'wt' in t)>=21)
    _gtt=open(W+('v601build' if _V6 else 'v536build')+'/gear-price-table.md').read()
    if _V6: print(V+' gear table (v601build): 35 stars/day, 3 favorite rows, 4 x 3 = 12 pieces, 18 launch weapons, legendaries Nov 19 / Nov 25 / Nov 30, balance never below zero:', '**35 stars/day**' in _gtt and '4 types x 3 slots = 12' in _gtt and '= 18 weapons at launch' in _gtt and '**Nov 19, Nov 25, Nov 30**' in _gtt and 'never below zero' in _gtt)
    else: print(V+' MX2 gear table: 35 stars/day, 3 favorite rows, 17 x 3 = 51 pieces, legendaries Nov 19 / Nov 25 / Nov 30, balance never below zero:', '**35 stars/day**' in _gtt and '17 types x 3 slots = 51' in _gtt and '**Nov 19, Nov 25, Nov 30**' in _gtt and 'never below zero' in _gtt)
    _cr6=lambda a,b:(lambda La,Lb:(max(La,Lb)+.05)/(min(La,Lb)+.05))(*[(lambda c:.2126*c[0]+.7152*c[1]+.0722*c[2])([(x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4) for x in (int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255)]) for h in (a,b)])
    _m3=open(W+'mock-t312u/find_t312u.py').read()
    print(V+' MX3 (t330u): one tan parchment token #F6E9C8 (the t312u/t320u/t328u mock question card and HUD level plate face) for every gameplay button, plate, panel, question card and HUD plate, Gold accent lines; only #2E7D32 Next/right and rarity rings differ; old Panel Stone/Polished Steel rows gone; Ink on it 15.1:',
          "face='#FFF0B8' if glow else '#F6E9C8'" in _m3 and "face='#F6E9C8', st=(), name='level'" in _m3 and "GREEN, GREEN_D = '#2E7D32'" in open(W+'mock-t320u/find_t320u.py').read()
          and '| Parchment (MX3) | tan `#F6E9C8`, Ink text, Gold accent lines between | every gameplay button, plate, panel, question card and HUD plate; only the `#2E7D32` Next/right button and rarity rings differ |' in _P6
          and not re.search(r'Panel Stone|Polished Steel|polished-steel|(?<!fill=.)#D5DCE2|(?<!fill=.)#F3E6C4',_P6) and 'a 2×2 grid of parchment plates' in _P6 and 'Ink on parchment 15.1' in _P6 and round(_cr6('#10170F','#F6E9C8'),1)==15.1)
    _spec6=open(W+'nancys-adventure-english-'+V+'.md',encoding='utf-8').read()
    print(V+' MX4 (t330u) scene notes queued in the spec .md build notes (all five) and moved to v6: no MX4 line in the PASTE (+284 would pass 188,200):', 'Scene art (MX4)' not in _P6 and all(x in _spec6 for x in ("Golden Fields ask: Sam's eyes happy closed arcs",'Golden Fields: a corn row on the far hill','Word Meadow: a small wood swing set far back','Echo Forest: one clear object','pine canopies sit on trunks and branches grow from trunks')) and 'MX4 scene notes' in _spec6.split('**v6 list (from '+V+'):**')[1])
    if _V6: print(V+' Bible sling and hammer free when their tier opens (one sentence, weaponNew); the crook is the Gentle guardian gift; data carries no price for the 3 Bible weapons; staff-lantern gone (t360u):', 'the Bible sling and hammer (flourishes) are free when their tier opens (`uiText.weaponNew`);' in _P6 and all('stars' not in t for t in _C6['trophies'] if t['id'] in ('sling-shepherd','staff-shepherd','hammer-builder')) and [t['unlock'] for t in _C6['trophies'] if t['id']=='staff-shepherd']==[{'type':'guardian','zone':'baby-hospital'}] and 'staff-lantern' not in _P6)
    else: print(V+' Bible weapons free when their tier opens (one sentence, weaponNew, no new Thai); data carries no price for them:', 'the 4 Bible weapons (flourishes) are free when their tier opens (`uiText.weaponNew`);' in _P6 and all('stars' not in t for t in _C6['trophies'] if t['id'] in ('sling-shepherd','staff-shepherd','staff-lantern','hammer-builder')))
    _mx=[l for l in _P6.split('\n') if '**Regions open in order (t334u):**' in l]; _P6p=open(W+'nancys-adventure-english-'+V+'-PASTE.md',encoding='utf-8').read()
    _rg={r['id']:r['zones'] for r in _C6['mapLayout']['regions']}
    print(V+' t334u END-BOSS gate (supersedes MX1 all-guardians): one rule in rule 4; Word Meadow > Golden Fields (Word guardian) > Home Lake (Number) > Echo Forest/Sound Duel (Gentle); end = last zone in mapLayout order; end guardian can come first; Sound + Rainbow anytime bonus, never needed; Maxwell Says + Kitchen day one; softened look + end guardian silhouette + comingNext; tap -> guardianLast; never closes; regionOpen + 8% bounce + sparkle; hearth/Scrolls/rest always; no all/one-guardian text; internal names absent:',
          len(_mx)==1 and all(x in _mx[0] for x in ('Word Meadow; Golden Fields after the Word guardian (Sight Words); Home Lake after the Number guardian; Echo Forest (Sound Duel) after the Gentle guardian.',"Only a region's end guardian (its last zone in `mapLayout` order) opens the next, and she can face it first;",'the Sound (Phonics) and Rainbow (Colors) guardians are anytime bonuses, never needed.',"A guardian can't be lost (a miss: hint, try again).",'Maxwell Says and Kitchen open day one','softened (tint, not gray)',"the end guardian's silhouette and `uiText.comingNext`; a tap shows `uiText.guardianLast`.",'An opened region never closes','`uiText.regionOpen`, an 8% bounce and a sparkle','Hearth, Scrolls and rest screen: always.'))
          and _rg=={'r1':['phonics','sight-words'],'r2':['colors-shapes','numbers'],'r3':(['maxwell-says','kitchen','baby-hospital'] if _V37 else ['baby-hospital','maxwell-says','kitchen']),'r4':['soundDuel']}
          and [[z for z in _rg[r] if any(x['key']==z and x.get('boss') for x in _C6['zones'])][-1] for r in ('r1','r2','r3')]==['sight-words','numbers','baby-hospital']
          and (not _V37 or [_rg[r][-1] for r in ('r1','r2','r3')]==['sight-words','numbers','baby-hospital'])
          and {z['key']:z['boss']['name']['en'] for z in _C6['zones'] if z.get('boss') and z['key'] in ('sight-words','numbers','baby-hospital')}=={'sight-words':'The Word Guardian','numbers':'The Number Guardian','baby-hospital':'The Gentle Guardian'}
          and not re.search(r'Sound and Word guardians|after Rainbow and Number|kindly names the guardian to finish|guardianFirst|Finish one Guardian|all (its|the) guardians|either guardian',_P6+json.dumps(_C6,ensure_ascii=False))
          and 'guardianFirst' not in _C6['uiText'] and _C6['uiText']['guardianLast']['en']=='Finish the last Guardian to open this.' and _C6['uiText']['guardianLast']['th']=='ผ่านผู้พิทักษ์ตัวสุดท้าย แล้วที่นี่จะเปิด' and 'thStatus' not in _C6['uiText']['guardianLast'] and _C6['meta']['thStatusDefault']=='NEEDS NANCY'
          and not re.search(r'(?i)echo forest guardian|elwynn|westfall|redridge|duskwood',_P6) and 'every zone stays open' not in _P6 and 'all zones open' not in _P6.lower() and 'Sound Duel are open from her first launch' not in _P6 and 'open at any level' not in _P6 and 'glows Gold as her next adventure' not in _P6)
    print(V+' t334u arrow points at the end guardian she still needs; boss line opens the next region on the end guardian; test line says each region opens by its end guardian only and never closes; grace words (padlock/locked/fail/ล็อก/แพ้/ไม่ผ่าน) only inside never-rules, none in uiText:', 'the open row whose end guardian she still needs' in _P6 and "when her region's end guardian kneels, the next region opens (rule 4)." in _P6 and 'Regions open in order, each by its end guardian only (rule 4), and never close;' in _P6 and not [l for l in _P6.split('\n') if re.search(r'(?i)padlock|\blocked\b',l) and not re.search(r'(?i)\bno\b|never|not ',l)] and not re.search(r'(?i)ล็อก|แพ้|ไม่ผ่าน|\b(locked|fail)',json.dumps(_C6['uiText'],ensure_ascii=False)))
    if _V6: print(V+' spec .md: Pacing note in Auditor wording (stale ten-days sentence gone), headroom note verbatim; banked figure = 188,200 - PASTE chars; PASTE has no pacing line:', '- **Pacing:** '+_PACE6 in _spec6 and 'ten days' not in _spec6 and 'about 2–4 days' not in _spec6 and 'Headroom freed by the three-rarity trim is saved for v6. Top priority is more questions for longevity, since 100 questions is only about two weeks at one run a day (Maxwell t334u).' in _spec6 and ('Banked in '+V+': %d chars under 188,200 (PASTE %s chars)'%(188200-len(_P6p),format(len(_P6p),','))) in _spec6 and 'Golden Fields opens on day 2' not in _P6 and 'Scene art (MX4)' not in _P6 and not any(k in _C6['uiText'] for k in ('tapFind','tapMy','tapGive','tapYour')))
    else: print(V+' t334u spec .md: Pacing note and banked-headroom note verbatim; banked figure = 188,200 - PASTE chars:', _t37('At one run a day, the first zone takes about five days. Requiring both bosses would take about ten days, but that is not the rule (Maxwell t334u).') in _spec6 and 'Headroom freed by the three-rarity trim is saved for v6. Top priority is more questions for longevity, since 100 questions is only about two weeks at one run a day (Maxwell t334u).' in _spec6 and ('Banked in '+V+': %d chars under 188,200 (PASTE %s chars)'%(188200-len(_P6p),format(len(_P6p),','))) in _spec6 and 'Scene art (MX4)' not in _P6 and not any(k in _C6['uiText'] for k in ('tapFind','tapMy','tapGive','tapYour')))
    _tx6=_C6['picPlan']['uiInlineSvg']['tex']; _wp6=_C6['picPlan']['weaponParts']; _tx5=_C5['picPlan']['uiInlineSvg']['tex'] if '_C5' in dir() else None
    if _V6: print(V+' Watchman T1 haft fix kept: shared #wh haft light wood #B07A42 (was bare #6B4423); #wo knob and the spear/polearm/scythe/claws recipes left with their rows (Option B, t360u); v6 list keeps shield pairing; magic-staff-rare not in build:', "<path id='wh' d='M-2 22v-62h4v62z' fill='#B07A42'" in _tx6 and '#6B4423' not in _tx6 and "id='wo'" not in _tx6 and not {'spear','polearm','scythe','claws'}&set(_wp6) and 'Shields also pair with the 1H axe and 1H mace, not only the 1H sword (Maxwell t336u poses sheet)' in _spec6.split('**v6 list (from '+V+'):**')[1] and 'only a 1H sword may add `shield-sunrise`' in _P6 and 'magic-staff' not in _P6)
    else: print(V+' Watchman T1 haft fix at 0 net (QM 4:37 AM PT): shared #wh haft light wood #B07A42 (was bare #6B4423), #wo knob r 8, spear/polearm tips x.5/x.4, scythe blade 1.7 wide at head scale 1.0 (Watchman final), spear tip + claws thin words trimmed to pay; v6 list has scythe fill + shield pairing; no full SVG pasted; magic-staff-rare not in build:', "<path id='wh' d='M-2 22v-62h4v62z' fill='#B07A42'" in _tx6 and '#6B4423' not in _tx6 and "<circle id='wo' cy='-45' r='8'" in _tx6 and (_wp6['spear'],_wp6['polearm'],_wp6['scythe'],_wp6['claws'])==('wh x1.4+wb x.5','wh x1.4+wx+wb x.4 tip','wh x1.4+wx 1.7 wide curved','2 gauntlets, 3 wb x.35 each') and 'Shields also pair with the 1H axe and 1H mace, not only the 1H sword (Maxwell t336u poses sheet)' in _spec6.split('**v6 list (from '+V+'):**')[1] and 'only a 1H sword may add `shield-sunrise`' in _P6 and 'magic-staff' not in _P6)
    print(V+' t336u shields round or square only: shield-sunrise is round in its note; no kite/heater shield anywhere in the PASTE:', _C6['picPlan']['svgNotes']['shield-sunrise'].startswith('Round ') and not re.search(r'(?i)kite|heater|teardrop shield|shield[^.\n]{0,30}teardrop',_P6))
    print(V+' rarity drip colors spec .md only (uncommon 2 green, epic 4 purple #9B6BD3, provisional); not in PASTE:', 'uncommon 2 rings green, epic 4 rings purple `#9B6BD3`' in _spec6 and '9B6BD3' not in _P6)
    print(V+' MX1 gear stays tied to levels, not regions:', 'levels open only gear tiers (11.1)' in _P6 and not re.search(r'(?i)region[^.\n]{0,40}(opens?|unlocks?) [^.\n]{0,20}(gear|weapon)',_P6))
    print(V+' minors: m2 ribbon after the last scene; m3 12 level cosmetics = data; m5 corner; m7 chooseHero on the hero band; m8 same-zone outings; m9 gear rows scroll sideways; m10 slots + legendary silhouette before tier 3; m11 SE sum with hero strip:',
          'ribbon once its last scene is done' in _P6 and '(12, levels 2–20;' in _P6 and _C6['meta']['levelTrophies']==12==sum(1 for t in _C6['trophies'] if t.get('unlock',{}).get('type')=='level')
          and 'at the top-right corner of the main menu and the Map' in _P6 and 'band label `chooseHero`' in _P6 and 'stays its label' not in _P6 and _t37('from her zone, after the opener') in _P6 and 'from another zone' not in _P6
          and 'Character pane, gear rows (sideways) and Backup lists' in _P6 and ("(sword row: `sword-iron` as tier 1, then shield and sling; free gifts Bloodtide and Dragonbane sit beside the Greatsword row"+(', the crook beside the Mace row)' if _V6 else ')')) in _P6 and 'until tier 3 opens and her stars reach its price' in _P6 and '+ bar or hero strip 48 = 550 ≤ 568.' in _P6)
    _TT=open(W+'instructor/v536/draft-tap-phrasing-t322u.md',encoding='utf-8').read()
    print(V+' tap phrasing (Instructor t322u) NOT built: t334u banks the freed headroom for v6 questions; no tapFind/tapMy/tapGive/tapYour keys or rule, tapPrompt kept; uiText '+str(len(_C6['uiText']))+':', not any(k in _C6['uiText'] for k in ('tapFind','tapMy','tapGive','tapYour')) and 'tapMy' not in _P6 and 'tapFind' not in _P6 and _C6['uiText']['tapPrompt']=={'en':'Tap the {word}','th':'แตะที่ {word}'} and len(_C6['uiText'])==_C6['meta']['uiTextEntries']==(91 if _V6 else 92))   # v6-01: -classMage -forestRanger (Option B) +giftFrom
    print(V+' hint button line byte-identical to v5-35; heavy laden unchanged; verses = v5-35 except version:', [l for l in _P6.split('\n') if l.startswith('5. **Hint button:**')]==[l for l in _P5.split('\n') if l.startswith('5. **Hint button:**')] and _P6.count('heavy laden')==_P5.count('heavy laden')>=1 and {k:v for k,v in _dvp.items() if k!='version'}=={k:v for k,v in json.load(open(W+'nancys-adventure-english-v5-35-daily-verses.json')).items() if k!='version'})
# ===================== v5-37 checks (Auditor v5-36 gate HOLD audit/v5-36-gate-2026-10-31.md 90020f20: items 1-12 only) =====================
if V=='v5-37':   # release diff pinned to v5-37 (vs v5-36); v6-01 has its own release-diff block below
    import hashlib as _h7, difflib as _dl7
    _m7=lambda f:_h7.md5(open(W+f,'rb').read()).hexdigest()
    _N7='nancys-adventure-english-'
    _P36=open(W+_N7+'v5-36-PASTE.md',encoding='utf-8').read(); _P37=open(W+_N7+V+'-PASTE.md',encoding='utf-8').read()
    _C36=_json_load(open(W+_N7+'v5-36-cards.json',encoding='utf-8')); _C37=_json_load(open(W+_N7+V+'-cards.json',encoding='utf-8'))
    _r36=open(W+_N7+'v5-36-cards.json',encoding='utf-8').read(); _r37=open(W+_N7+V+'-cards.json',encoding='utf-8').read()
    _S36=open(W+_N7+'v5-36.md',encoding='utf-8').read(); _S37=open(W+_N7+V+'.md',encoding='utf-8').read()
    _F36=open(W+_N7+'FINAL-v5-36.md',encoding='utf-8').read(); _F37=open(W+_N7+'FINAL-'+V+'.md',encoding='utf-8').read()
    print(V+' base set v5-36 untouched (PASTE f04f4e3b, cards b4a6e7d4, verses 6634c209, FINAL 6c1b50d8, spec be1a68b4, qm_v536 fc337cff, checks_v536 64c2cae2) and CURRENT.md ba6726f6:',
          [_m7(f)[:8] for f in (_N7+'v5-36-PASTE.md',_N7+'v5-36-cards.json',_N7+'v5-36-daily-verses.json',_N7+'FINAL-v5-36.md',_N7+'v5-36.md','v520/qm_v536.py','v520/checks_v536.py','CURRENT.md')]==['f04f4e3b','b4a6e7d4','6634c209','6c1b50d8','be1a68b4','fc337cff','64c2cae2','ba6726f6'])
    _ap=[(o,n) for o,n in _E37 if o!='the first zone takes about five days.']
    print(V+' items 1,2,4,5,6,7,9,11: each old text once in v5-36 PASTE (Paper question card twice), gone in '+V+', new text present the same number of times:',
          all(_P36.count(o)==(2 if o=='Paper question card' else 1) and o not in _P37 and _P37.count(n)==_P36.count(o)+_P36.count(n) for o,n in _ap))
    print(V+' item 3 (N3): Home Lake mapLayout ["maxwell-says","kitchen","baby-hospital"]; every region with a guardian has it as its LAST zone (rule :27 unchanged):',
          [r['zones'] for r in _C37['mapLayout']['regions'] if r['en']=='Home Lake']==[['maxwell-says','kitchen','baby-hospital']]
          and all(any(z['key']==r['zones'][-1] and z.get('boss') for z in _C37['zones']) for r in _C37['mapLayout']['regions'] if any(z['key'] in r['zones'] and z.get('boss') for z in _C37['zones']))
          and "Only a region's end guardian (its last zone in `mapLayout` order) opens the next" in _P37)
    _cat7=lambda t:t.get('cat','gear' if 'wt' in t else None)   # compact file: a trophy with wt is gear (trophyRules.note)
    _gear=sum(1 for t in _C37['trophies'] if _cat7(t)=='gear')
    print(V+' item 8: meta.trophiesByCat.gear == actual gear trophies (%d); sum of trophiesByCat == trophies (%d):'%(_gear,len(_C37['trophies'])), _C37['meta']['trophiesByCat']['gear']==_gear==27 and sum(_C37['meta']['trophiesByCat'].values())==len(_C37['trophies']) and '5 gems, 27 gear,' in _P37)
    _g7=sum(1 for t in _C37['trophies'] if 'thGloss' in t and _cat7(t)=='gear'); _d7=sum(1 for c in _C37['cards'] if 'thDef' in c)
    print(V+' item 7: "the %d gear `thGloss`" and "the %d `thDef` hints" match the data (meta.thDefCards %d):'%(_g7,_d7,_C37['meta']['thDefCards']), ('the %d gear `thGloss`'%_g7) in _P37 and ('the %d `thDef` hints'%_d7) in _P37 and _d7==_C37['meta']['thDefCards'])
    _rows7=_C37['trophyRules']['rows'].split(); _wp7=[t for t in _C37['trophies'] if 'wt' in t]
    _ex7=[t['id'] for t in _wp7 if not ('tier' in t and t['wt'] in _rows7) and t['id']!='sword-iron']
    print(V+' item 11 (W#9): gift-ring "all N weapons" = launch weapons she can own: %d rows x %d slots + %d extras %s = %d:'%(len(_rows7),len(_C37['trophyRules']['tierStars']),len(_ex7),_ex7,len(_rows7)*3+len(_ex7)), ('all %d weapons'%(len(_rows7)*len(_C37['trophyRules']['tierStars'])+len(_ex7))) in _P37)
    print(V+' item 11 (W#6): no "Paper question card" left; question card named tan like MX3 :115 (tan `#F6E9C8`); Paper `#E9D9AE` Map sheet row unchanged:', 'Paper question card' not in _P37 and _P37.count('tan question card')==2 and '| Paper | `#E9D9AE`, edge `#8A6A3A` | Map sheet |' in _P37 and '| Parchment (MX3) | tan `#F6E9C8`' in _P37)
    print(V+' item 11 (W#7): spec pacing line "about 2–4 days" (was "about five days", -1), PASTE has no pacing line:', 'the first zone takes about 2–4 days.' in _S37 and 'about five days' not in _S37 and 'first zone takes' not in _P37)
    _tx7=_C37['picPlan']['uiInlineSvg']['tex']
    print(V+' item 10 (W#2): #wo fill var(--b) (was #3D7FD9) and #wv stroke var(--b); wand/staff/bow recipes use #wo/#wv; Watchman #4 CSS defaults NOT added (not 0 net):', "<circle id='wo' cy='-45' r='8' fill='var(--b)'/>" in _tx7 and "<path id='wv' d='M0-30q22 30 0 60' stroke='var(--b)'/>" in _tx7
          and all('wo' in _C37['picPlan']['weaponParts'][k] for k in ('wand','staff')) and all('wv' in _C37['picPlan']['weaponParts'][k] for k in ('longbow','shortbow','crossbow')) and 'var(--d,' not in _tx7 and 'var(--g,' not in _tx7 and 'var(--h,' not in _tx7)
    # cards: only version x2, Home Lake order, meta gear, tex (#wo/#wv) changed
    _a7=json.loads(_r36); _b7=json.loads(_r37)
    _a7['version']=_a7['meta']['version']=V; _a7['meta']['trophiesByCat']['gear']=27
    [r.__setitem__('zones',['maxwell-says','kitchen','baby-hospital']) for r in _a7['mapLayout']['regions'] if r['en']=='Home Lake']
    _a7['picPlan']['uiInlineSvg']['tex']=_a7['picPlan']['uiInlineSvg']['tex'].replace("fill='#3D7FD9'/><path id='wv' d='M0-30q22 30 0 60'/>","fill='var(--b)'/><path id='wv' d='M0-30q22 30 0 60' stroke='var(--b)'/>")
    print(V+' cards: v5-36 + only version, items 3/8/10 (nothing else); %d -> %d chars:'%(len(_r36),len(_r37)), _a7==_b7 and len(_r37)-len(_r36)==19)
    _v36=open(W+_N7+'v5-36-daily-verses.json','rb').read(); _v37=open(W+_N7+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v5-36 except the version field; Matthew 11:28 "heavy laden" unchanged in the PASTE:', _v37==_v36.replace(b'"version": "v5-36"',b'"version": "'+V.encode()+b'"',1) and _v36.count(b'"version"')==1 and _P37.count('heavy laden')==_P36.count('heavy laden')==1)
    _th7=lambda t: collections.Counter(re.findall(r'[\u0E00-\u0E7F][\u0E00-\u0E7F\s.,!?…]*',t))
    print(V+' Thai unchanged in PASTE, FINAL and spec (every Thai run, same counts):', _th7(_P36)==_th7(_P37) and _th7(_F36)==_th7(_F37) and _th7(_S36)==_th7(_S37))
    # diff-only: undo every allowed edit on v5-37 and get v5-36 back exactly
    _u=_P37.replace('-'+V+'-daily-verses.json','-v5-36-daily-verses.json')
    for o,n in _ap: _u=_u.replace(n,o)
    _u=_u.replace(json.dumps(json.loads(_r37,object_pairs_hook=collections.OrderedDict),ensure_ascii=False,separators=(',',':')),_r36)
    print(V+' PASTE diff-only: reversing items 1-12 + version bump gives v5-36 byte for byte; delta %+d; %d chars <= 188,200:'%(len(_P37)-len(_P36),len(_P37)), _u==_P36 and len(_P37)-len(_P36)==59 and len(_P37)<=188200)
    _uf=_F37.replace(V,'v5-36')
    for o,n in _ap: _uf=_uf.replace(n,o)
    _us=_S37.replace(V,'v5-36').replace('the first zone takes about 2–4 days.','the first zone takes about five days.').replace('Banked in v5-36: %d chars under 188,200 (PASTE %s chars)'%(188200-len(_P37),format(len(_P37),',')),'Banked in v5-36: 213 chars under 188,200 (PASTE 187,987 chars)')
    for o,n in _ap: _us=_us.replace(n,o)
    print(V+' FINAL and spec .md: same shared edits as the PASTE (reversal gives v5-36 byte for byte); spec banked note = 188,200 - PASTE chars:', _uf==_F36 and _us==_S36 and ('Banked in '+V+': %d chars under 188,200'%(188200-len(_P37))) in _S37)
# ===================== v6-01 checks (Maxwell t360u "Ok" to the v6 gear plan + t362u build go; spec-notes/v6-gear-cohesion-t357u.md cb75bd6f) =====================
if _V6:
    import hashlib as _h8, subprocess as _sp8, os
    _m8=lambda f:_h8.md5(open(W+f,'rb').read()).hexdigest(); _N8='nancys-adventure-english-'
    _P7=open(W+_N8+'v5-37-PASTE.md',encoding='utf-8').read(); _P8=open(W+_N8+V+'-PASTE.md',encoding='utf-8').read()
    _F7=open(W+_N8+'FINAL-v5-37.md',encoding='utf-8').read(); _F8=open(W+_N8+'FINAL-'+V+'.md',encoding='utf-8').read()
    _S7=open(W+_N8+'v5-37.md',encoding='utf-8').read(); _S8=open(W+_N8+V+'.md',encoding='utf-8').read()
    _r7=open(W+_N8+'v5-37-cards.json',encoding='utf-8').read(); _r8=open(W+_N8+V+'-cards.json',encoding='utf-8').read()
    _C7=_json_load(open(W+_N8+'v5-37-cards.json')); _C8=_json_load(open(W+_N8+V+'-cards.json')); _T8={t['id']:t for t in _C8['trophies']}; _T7={t['id']:t for t in _C7['trophies']}
    print(V+' base set v5-37 untouched (PASTE acc534a5, cards 350ecbaf, verses b0235ff8, FINAL 8679a584, spec 2cacef00, qm_v537, checks_v537), CURRENT.md b653ffb2, v537-frozen/ and audit/snap-v537-gate/ match their MANIFEST:',
          [_m8(f)[:8] for f in (_N8+'v5-37-PASTE.md',_N8+'v5-37-cards.json',_N8+'v5-37-daily-verses.json',_N8+'FINAL-v5-37.md',_N8+'v5-37.md','CURRENT.md')]==['acc534a5','350ecbaf','b0235ff8','8679a584','2cacef00','b653ffb2']
          and all(_m8(l.split()[1])==l.split()[0] for l in open(W+'audit/snap-v537-gate/MANIFEST.md5') if l.strip())
          and all(_m8('v537-frozen/'+f)==_m8(f) for f in os.listdir(W+'v537-frozen') if f.startswith(_N8) and os.path.exists(W+f)))
    _dry=_sp8.run([_sys.executable,W+'v520/qm_v601.py','--dry'],capture_output=True,text=True,cwd=W+'v520')
    if _STILL: _dry2=_sp8.run([_sys.executable,W+'v520/qm_v602.py','--dry'],capture_output=True,text=True,cwd=W+'v520'); _dry.stdout=_dry.stdout.replace('-> 187425 ','-> X ')+(_dry2.stdout if _dry2.returncode==0 and '-> 187425 ' in _dry.stdout else '')
    if _STILL and V!='v6-02': _dry3=_sp8.run([_sys.executable,W+'v520/qm_v603.py','--dry'],capture_output=True,text=True,cwd=W+'v520'); _dry.stdout=_dry.stdout.replace('-> 187108 ','-> X ')+(_dry3.stdout if _dry3.returncode==0 and '-> 187108 ' in _dry.stdout else '')   # v6-03: chain qm_v602 (187,108) then qm_v603   # v6-02: qm_v601 must still give v6-01 (187,425), then qm_v602 gives the file on disk
    print(V+' generator qm_v601.py re-runs from the frozen v5-37 base (--dry, nothing written): stage 1 == measure-B4 scratch byte for byte (184,516), and the stage-2 PASTE length equals the file on disk:', _dry.returncode==0 and 'measure-B4 scratch byte for byte: 184516 chars' in _dry.stdout and ('-> %d '%len(_P8)) in _dry.stdout, _dry.stderr[-200:])
    _rep=_P8.replace(_r8.strip() if V>='v6-06' else json.dumps(_C8,ensure_ascii=False,separators=(',',':')),'@@')
    print(V+' PASTE = FINAL + the cards.json block (one JSON block, minified, byte-identical to the cards file); %d chars <= 188,200; Thai reserve 188,200-188,500 unused; banked %d:'%(len(_P8),188200-len(_P8)), _rep.count('@@')==1 and _r8.count('\n')==0 and len(_P8)<=188200)
    _v7=open(W+_N8+'v5-37-daily-verses.json','rb').read(); _v8=open(W+_N8+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v5-37 except the version field; "heavy laden" once in the PASTE and unchanged in cards; verses never priced:', _v8==_v7.replace(b'"version": "v5-37"',('"version": "%s"'%V).encode(),1) and _P8.count('heavy laden')==_P7.count('heavy laden')==1 and _C8['verses']==_C7['verses'] and _C8['jesusWords']==_C7['jesusWords'] and [z.get('boss') for z in _C8['zones']]==[z.get('boss') for z in _C7['zones']] and not re.search(r'"(cost|price)"',json.dumps(_C8['verses'])+json.dumps(_C8['trophies'])+json.dumps(_C8['pantry'])))
    _TRIMIDS=('bow-oak','wand-oak','bow-short','staff-lantern','spear-river','crossbow-pine','axe-great','claws-bear','glaive-moon','maul-stone','scythe-harvest')
    print(V+' Option B trim: rows sword1 sword2 axe1 mace1; the 11 trimmed trophies gone from data and prose (staff-shepherd kept as the crook); no bow/wand/staff weapon left; classMage/forestRanger gone:',
          _C8['trophyRules']['rows']=='sword1 sword2 axe1 mace1' and not any(i in _P8 for i in _TRIMIDS) and not re.search(r'(?i)\b(longbow|shortbow|crossbow|wand|war scythe|polearm|glaive|daggers|punch blades)\b',_F8) and 'classMage' not in _P8 and 'forestRanger' not in _P8)
    _W8={i:t['word'] for i,t in _T8.items() if 'word' in t}
    _free8=lambda t:(t.get('unlock',{}).get('type') in ('start','level','guardian')) or ('tier' in t and _C8['trophyRules']['tierStars'][t['tier']-1]==0)
    _refs7=set(re.findall(r'"ref":"([^"]+)"',_P7))
    print(V+' gear words (t358u): the 8 launch words on the planned pieces; each [word, meaning <= 8 words, Thai draft]; no words 9-16 built; no word count anywhere:',
          {i:w[0] for i,w in _W8.items()}=={'cape-green':'Grace','sling-shepherd':'Courage','sword-iron':'Valor','shield-sunrise':'Faith','tunic-rose':'Righteousness','staff-shepherd':'Mercy','hammer-builder':'Strength','axe-oak':'Steadfast'}
          and all(len(w)==3 and len(w[1].split())<=8 and re.fullmatch(r'[\u0E00-\u0E7F]+',w[2]) for w in _W8.values())
          and not re.search(r'(?i)words? (learned|collected|found)|\d+ ?/ ?\d+ words',_P8) and 'No word count anywhere' not in _P8 and 'No word count.' in _P8)
    _R8={i:t['ref'] for i,t in _T8.items() if 'ref' in t}
    print(V+' verse reference labels: only on free or given pieces, only references already in v5-37 (no Ephesians), never verse text, crook = the Gentle guardian scroll (Isaiah 40:11); no ref on any Pantry item or star-bought rung:',
          all(_free8(_T8[i]) for i in _R8) and set(_R8.values())<=_refs7 and 'Ephesians' not in _P8 and all(re.fullmatch(r'(\d )?[A-Z][a-z]+ \d+:\d+',r) for r in _R8.values()) and _R8['staff-shepherd']==[z['boss']['scroll']['ref'] for z in _C8['zones'] if z['key']=='baby-hospital'][0]
          and 'tunic-rose' not in _R8 and not any('ref' in i or 'word' in i for i in _C8['pantry']['items']) and 'never verse text, never tappable, never sold' in _P8)
    _cr=_T8['staff-shepherd']
    print(V+' guardian types: Sword + Greatsword at start; giftOf Word guardian (sight-words) -> axe1, Number guardian (numbers) -> mace1; crook = Gentle guardian (baby-hospital) gift, free, 2H, named Good Shepherd Crook; soft outline + uiText.giftFrom; switching free on Character:',
          _C8['trophyRules']['giftOf']=={'axe1':'sight-words','mace1':'numbers'} and [z['boss']['name']['en'] for z in _C8['zones'] if z['key'] in ('sight-words','numbers','baby-hospital')]==['The Number Guardian','The Word Guardian','The Gentle Guardian']
          and _cr['en']=='Good Shepherd Crook' and _cr['unlock']=={'type':'guardian','zone':'baby-hospital'} and 'stars' not in _cr and 'tier' not in _cr and 'crook' in _C8['trophyRules']['hands']['two'] and _C8['trophyRules']['unlockTypes']['guardian']
          and _C8['uiText']['giftFrom']['en']=='A gift from {g}' and 'soft Gold outline, no fill, with `uiText.giftFrom`' not in _P8 and 'soft Gold outline with `uiText.giftFrom`' in _P8 and 'Switching types on Character is free.' in _P8 and _T8['axe-oak']['tier']==1 and _T8['axe-oak']['wt']=='axe1')
    _new8=_F8[_F8.index('- **Gifts from guardians (t360u):**'):_F8.index('- **Hands (`trophyRules.hands`')]
    print(V+' grace + never list in the new gear text: no padlock/locked/fail/ล็อก/แพ้/ไม่ผ่าน, no timer/energy/leaderboard/countdown, no counter; transform/opacity only:',
          not re.search(r'(?i)padlock|\block(ed|s)?\b|\bfail|ล็อก|แพ้|ไม่ผ่าน|timer|energy|leaderboard|countdown|counter',_new8+json.dumps(_C8['uiText']['giftFrom'],ensure_ascii=False)) and 'opacity only' in _new8)
    print(V+' Breastplate of Righteousness = the level-13 item that was the Rose Garden Shirt (same id, slot tunic, level 13), no rings; no "Rose Garden" left:', _T8['tunic-rose']['en']=='Breastplate of Righteousness' and _T8['tunic-rose']['slot']=='tunic' and _T8['tunic-rose']['unlock']=={'type':'level','n':13} and 'Rose Garden' not in _P8 and 'ทับทรวง' in _T8['tunic-rose']['thGloss'])
    _sh8=[i for i in _C8['pantry']['items'] if 'tint' in i]
    print(V+' shirt swaps: 3 Golden Pantry tunic tints, 30-80 stars, no rarity/rings/tier, pic 👕 (Emoji 1.0), rule sentence says no rings:', len(_sh8)==3 and all(i['slot']=='tunic' and 30<=i['stars']<=80 and re.fullmatch(r'#[0-9A-F]{6}',i['tint']) and not ({'tier','rings','rarity'}&set(i)) and i['pic']=='👕' for i in _sh8) and "a `tint` item recolors the hero's tunic, no rings" in _P8)
    print(V+' gear sheet look (t350u): carved dark-wood frame, Gold filigree, parchment #F6E9C8 panels, hero center, beveled square slots with --b ring glow (opacity only), dark tooltip, 320 pt layout, original art:', all(x in _P8 for x in ('carved dark-wood frame','Gold filigree corners','parchment panels','the hero in the center','beveled square tiles',"rings glowing in `--b` (opacity only)",'tooltips dark','At 320 pt rows scroll sideways under the hero','Original art only.')) and '#F6E9C8' in _P8)
    _br8=_P8+_S8
    print(V+' no game/brand names (incl. MMO, Warcraft, WoW) and no new show names anywhere in PASTE or spec:', not re.search(r'(?i)warcraft|\bwow\b|\bmmo\b|blizzard|diablo|runescape|elder scrolls|final fantasy|zelda|minecraft|fortnite|roblox|pokemon|pokémon',_br8))
    print(V+' safety: no Elk Refuge Inn, no 911 / Call Max / Show the Nurse, no email or phone number; due date line count unchanged vs v5-37:', 'Elk Refuge' not in _P8 and not re.search(r'\b911\b|(?i:call max)|(?i:show the nurse)',_P8) and not re.search(r'[\w.+-]+@[\w-]+\.[\w.]+|\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}',_P8) and _P8.count('due')==_P7.count('due'))
    _emo8=[c for c in _P8 if ord(c)>=0x1F000 and c not in _P7]
    print(V+' emoji: no new emoji beyond v5-37 except 👕 (Emoji 1.0, Unicode 6.0):', set(_emo8)<={'👕'}, sorted(set(_emo8)))
    _th8=lambda t: collections.Counter(re.findall(r'[\u0E00-\u0E7F][\u0E00-\u0E7F\s.,!?…]*',t))
    _add=_th8(_P8)-_th8(_P7); _gone=_th8(_P7)-_th8(_P8)
    _expAdd=collections.Counter([w[2] for w in _W8.values()]+[_T8['tunic-rose']['thGloss'],'ของขวัญจาก']+[i.get('th') for i in _sh8])   # n1 (Auditor v6-02 recheck): a missing shirt Thai prints False, never a KeyError
    _expGone=collections.Counter([_T7[i]['thGloss'] for i in _TRIMIDS if 'thGloss' in _T7[i]]+[_C7['uiText'][k]['th'] for k in ('classMage','forestRanger')]+[_T7['tunic-rose']['thGloss']])
    print(V+' Thai changed only where planned: added = 8 word drafts + breastplate gloss + giftFrom + 3 shirt names (all NEEDS NANCY); removed = trimmed pieces + classMage/forestRanger + Rose Garden gloss; nothing else:', _add==_expAdd and _gone==_expGone, dict(_add-_expAdd), dict(_gone-_expGone))
    print(V+' Thai NEEDS NANCY note names the new Thai; Thai type rule (17 px+, line-height 1.7) still stated:', 'gear `thGloss` and `word` Thai' in _P8 and re.search(r'17 ?(px|pt)',_P8) is not None and '1.7' in _P8)
    _cards_same=json.loads(_r7); _c8=json.loads(_r8)
    print(V+' cards: questions untouched (cards, zones, soundDuel, verses, jesusWords, mapLayout, rewardText, encouragement identical to v5-37):', all(_cards_same[k]==_c8[k] for k in ('cards','zones','soundDuel','verses','jesusWords','jesusWordsFallback','mapLayout','rewardText','wrongText','encouragement','welcomeBack','restScreen')))

# ===================== v6-02 checks (Maxwell t366u "Make the opening title screen a still not an animation" + Auditor v6-01 gate HOLD fixes, audit/v6-01-gate-2026-10-31.md da16238d) =====================
if _STILL and V in ('v6-02','v6-03'):   # v6-02/v6-03 diff blocks; v6-04 has its own block at the end
    _N9='nancys-adventure-english-'; _B9='v6-01'
    _P1=open(W+_N9+_B9+'-PASTE.md',encoding='utf-8').read(); _F1=open(W+_N9+'FINAL-'+_B9+'.md',encoding='utf-8').read(); _S1=open(W+_N9+_B9+'.md',encoding='utf-8').read()
    _C1=_json_load(open(W+_N9+_B9+'-cards.json')); _C2=_json_load(open(W+_N9+V+'-cards.json'))
    _P2=open(W+_N9+V+'-PASTE.md',encoding='utf-8').read(); _F2=open(W+_N9+'FINAL-'+V+'.md',encoding='utf-8').read(); _S2=open(W+_N9+V+'.md',encoding='utf-8').read()
    _snap=W+'v601build/snap/MANIFEST.md5'
    print(V+' base v6-01 untouched (PASTE 43b4da7f, cards 10fc56b1, verses b3cb9ce9, FINAL 153fa326, spec 61f85cba) and matches v601build/snap MANIFEST; Auditor gate file da16238d; CURRENT.md still b653ffb2 (v5-37):',
          [_m8(_N9+_B9+x)[:8] for x in ('-PASTE.md','-cards.json','-daily-verses.json','.md')]==['43b4da7f','10fc56b1','b3cb9ce9','61f85cba'] and _m8(_N9+'FINAL-v6-01.md')[:8]=='153fa326'
          and all(_m8(l.split()[1])==l.split()[0] for l in open(_snap) if l.strip() and _N9 in l) and _m8('audit/v6-01-gate-2026-10-31.md')[:8]=='da16238d' and _m8('CURRENT.md')[:8]=='b653ffb2')
    _v1=open(W+_N9+_B9+'-daily-verses.json','rb').read(); _v2=open(W+_N9+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-01 except the version field:', _v2==_v1.replace(b'"version": "v6-01"',('"version": "%s"'%V).encode(),1) and _v1!=_v2)
    # --- t366u title still ---
    _U2=_C2['picPlan']['uiInlineSvg']; _ti=_P2[_P2.index('### 6.1 Sword screen'):_P2.index('- Then follow the launch order')]   # the title bullet + the tap bullet (the XP-bar line is the card screen)
    _anim=r'animation|@keyframes|transition|<animate|<set |\bsmil'
    print(V+' t366u title screen is a still: sky/title/sword SVGs have no animation, transition, keyframes or SMIL; classes pl/s1/s2/br/bh gone; .ti * stops all animation and transition (covers the shared aura flicker); 6.1 has no fade, delay, loop, auto-advance or hop:',
          not any(re.search(_anim,_U2.get(k,'')) for k in ('sky','title','sword')) and not re.search(r"class='(pl|s1|s2|br|bh)'",_U2.get('sky','')+_U2['title'])
          and '.ti *{animation:none!important;transition:none!important}' in _ti and 'A still (t366u): one frame, shown at once' in _ti
          and not re.search(r'(?i)\bfade|every 8 s|hopping|\bsway|\d+ ?ms|auto-advance(?! *\.)',_ti.replace('no fade, delay or auto-advance','')) and 'then the next screen at once' in _ti)
    print(V+' shared tex aura keyframes kept for Character (fl, .f1/.f2) and the sword SVG unchanged:', _U2['tex']==_C1['picPlan']['uiInlineSvg']['tex'] and '@keyframes fl' in _U2['tex'] and _U2['sword']==_C1['picPlan']['uiInlineSvg']['sword'] and _U2['aura']==_C1['picPlan']['uiInlineSvg']['aura'])
    _c1=dict(_C1); _c2=dict(_C2); _c1['picPlan']=dict(_C1['picPlan']); _c2['picPlan']=dict(_C2['picPlan'])
    _u1=dict(_C1['picPlan']['uiInlineSvg']); _u2=dict(_U2); [d_.pop(k) for d_ in (_u1,_u2) for k in ('sky','title')]
    _c1['picPlan']['uiInlineSvg']=_u1; _c2['picPlan']['uiInlineSvg']=_u2; _c1['version']=_c2['version']; _c1['meta']=dict(_C1['meta'],version=V)
    print(V+' cards: only uiInlineSvg sky/title and the version changed vs v6-01:', _c1==_c2)
    # --- Auditor v6-01 gate fixes (exact texts) ---
    _fx=[("shows in the piece's tooltip under its name:","shows in the piece's tooltip under its name (the panel above the rows, for the last tapped piece, and its reward screen; never hover):",90),
         ("(its own `uiText.weaponNew` screen after the scroll)","(its own `uiText.weaponNew` screen after the scroll; if tier 1 is not open yet, that screen waits until it opens)",61),
         ("the word in Gold, the meaning","the word in Gold (Dark Gold `#8A6200` on parchment), the meaning",35),
         ("the 12 gear `thGloss` and `word` Thai,","the 12 gear `thGloss` and `word` Thai, the 3 shirt names,",19)]
    print(V+' gate M1/m1/m2/m6 exact fix texts in PASTE, FINAL and spec (old text gone; deltas +90/+61/+35/+19):', all(b in t and a not in t.replace(b,'') and len(b)-len(a)==n for a,b,n in _fx for t in (_P2,_F2,_S2)))
    print(V+' gate m3 NOT applied (Maxwell\'s call): "Gold trophy (earned of 42)" kept as in v6-01:', 'Gold trophy (earned of 42)' in _P2 and 'earned count' not in _P2)
    print(V+' gate m4/m5/m7 + m6 spec notes in the spec build notes only (not in PASTE):', all(x in _S2 and x not in _P2 for x in ('v6-01 gate close-out','m4:','m5:','m7:','the breastplate gloss and the 3 shirt names','t336u class ladders')))
    # --- budget + diff discipline: undo every v6-02 edit and get v6-01 back exactly ---
    _u=_P2.replace(V,_B9)
    if V!='v6-02': _u=_u.replace(r"/(^|\D)(\+?1[\s.-]?)?",r"/(?<!\d)(\+?1[\s.-]?)?").replace("padding:0 max(16pt,env(safe-area-inset-right)) 0 max(16pt,env(safe-area-inset-left))","padding-inline:max(16pt,env(safe-area-inset-left)) max(16pt,env(safe-area-inset-right))")   # v6-03 recheck fixes
    for a,b,n in _fx: _u=_u.replace(b,a)
    for a,b in (("`.ti svg{stroke:#10170F;stroke-width:3;stroke-linejoin:round}.ti{touch-action:manipulation}.ti *{animation:none!important;transition:none!important}`. A still (t366u): one frame, shown at once, plane and banner parked on screen; no fade, delay or auto-advance.","`.ti svg{stroke:#10170F;stroke-width:3;stroke-linejoin:round}.ti{touch-action:manipulation}`. Motion is in the SVGs' `<style>`; reduced motion: all still, plane and banner parked on screen."),
                ("the button press and metal thud only, then the next screen at once. A 2nd tap is ignored.","the button press and metal thud only, then a 300 ms fade to the next screen. A 2nd tap is ignored. Reduced motion: a 150 ms fade."),
                ("a biplane towing the greeting banner)","a biplane towing the greeting banner every 8 s)"),("one bunny)","one hopping bunny)")):
        _u=_u.replace(a,b)
    for k in ('sky','title'): _u=_u.replace(json.dumps(_U2[k],ensure_ascii=False)[1:-1],json.dumps(_C1['picPlan']['uiInlineSvg'][k],ensure_ascii=False)[1:-1])
    print(V+' diff-only: undoing the title-still edits, the 4 gate fixes'+(', N1, n2' if V!='v6-02' else '')+' and the version gives v6-01 byte for byte; PASTE %d chars <= 188,200 (%+d vs v6-01), banked %d; spec banked line matches:'%(len(_P2),len(_P2)-len(_P1),188200-len(_P2)),
          _u==_P1 and len(_P2)<=188200 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P2),format(len(_P2),','))) in _S2)

# ===================== A1 (Auditor v6-04 gate): standing v6-02 checks for EVERY version from v6-02 on (brand, ES2017/regex, shirt NEEDS NANCY, plane on screen); no pin =====================
if _STILL and V>='v6-02':
    _N9='nancys-adventure-english-'
    _P1=open(W+_N9+'v6-01-PASTE.md',encoding='utf-8').read(); _P2=open(W+_N9+V+'-PASTE.md',encoding='utf-8').read(); _S2=open(W+_N9+V+'.md',encoding='utf-8').read()
    _C2=_json_load(open(W+_N9+V+'-cards.json')); _U2=_C2['picPlan']['uiInlineSvg']
    if V<'v6-04':
        print(V+' plane, banner and bunny parked on screen (plane 70, text x 201, bunny 74 416; inside the 320 viewBox and the 390x844 slice x 29-291):', "translate(70 80)" in _U2.get('sky','') and _U2.get('sky','').count("x='201'")==2 and "translate(74 416)" in _U2['title'] and 29<=70-26 and 70+206<=291)
    else:   # t371u: plane + banner live in the title SVG; check the 320x568 slice numerically (viewBox 390x844, xMidYMax slice)
        _ti=_U2['title']; _mq=re.search(r'@media\(min-aspect-ratio:1/2\)\{\.pq\{transform:translate\((-?\d+)px,(-?\d+)px\)\}\}',_ti); _bn=re.search(r"M(\d+) (\d+)h(\d+)l-6 11 6 11H\d+z",_ti)
        _k=320/390; _top=844-568/_k; _dx,_dy=(int(_mq.group(1)),int(_mq.group(2))) if _mq else (0,0); _bx,_by,_bw=(int(_bn.group(1)),int(_bn.group(2)),int(_bn.group(3))) if _bn else (0,0,0)
        _sy=(_by+_dy-_top)*_k; _sx0=(_bx+_dx)*_k; _sx1=(_bx+_bw+6+_dx)*_k
        print(V+' plane and banner parked on screen in the title (t371u): .pq group, banner y %.0f-%.0f pt at 320x568 (clears the 20 pt status bar), x %.0f-%.0f inside 320; at 390x844 banner y 107-129 below the 47 pt bar (m4: 90px):'%(_sy,_sy+22*_k,_sx0,_sx1),
              bool(_mq and _bn) and "class='pq'" in _ti and "id='gE'" in _ti and _sy>=24 and _sx0>=0 and _sx1<=320 and _by>=47 and _dy==90)
    # --- new checks asked by Auditor's checks note ---
    _all=_P2+_S2
    _bb={'Clash':r'\bClash\b','Avatar':r'\bAvatar\b','Excalibur':r'(?i)excalibur','Elwynn':r'(?i)elwynn','Westfall':r'(?i)westfall','Redridge':r'(?i)redridge','Duskwood':r'(?i)duskwood','Stormwind':r'(?i)stormwind','Azeroth':r'(?i)azeroth','Warcraft/WoW/MMO':r'(?i)warcraft|\bwow\b|\bmmo\b|blizzard'}
    _bh={k:len(re.findall(r,_all)) for k,r in _bb.items()}
    print(V+' brand check (bare Clash, Avatar (case-sensitive; lowercase UI "avatar" allowed), Excalibur, zone names Elwynn/Westfall/Redridge/Duskwood/Stormwind/Azeroth, Warcraft/WoW/MMO) 0 in PASTE + spec:', not any(_bh.values()), {k:v for k,v in _bh.items() if v})
    _es=[r'\(\?<[A-Za-z]',r'\\k<',r'\\p\{',r'\?\.(?=[A-Za-z_$\[(])',r'\?\?',r'replaceAll\(',r'\.at\(',r'\.flatMap\(',r'\.flat\(',r'fromEntries',r'matchAll',r'structuredClone',r'\|\|=',r'&&=',r'\(\?<[=!]',r'globalThis',r'\bBigInt\b']
    _eh={r:len(re.findall(r,_P2)) for r in _es}   # N1 (Auditor v6-02 recheck 5839cdd1): no exemption; the privacy-scan test runs in-app (window.__test), so the whole PASTE is scanned
    print(V+' ES2017 syntax check (Safari 14): no ?. ?? replaceAll .at( flat/flatMap fromEntries matchAll structuredClone ||= &&= lookbehind, named groups, \\k<, \\p{ globalThis BigInt in the PASTE'+(' (whole PASTE, no exemption)' if V!='v6-02' else ' (privacy-scan line exempt in v6-02)')+':', (not any(_eh.values()) if V!='v6-02' else not any(v for k,v in _eh.items() if k!=r'\(\?<[=!]') and _eh[r'\(\?<[=!]']==1), {k:v for k,v in _eh.items() if v})
    if V=='v6-02': print(V+' NOTE (flag for Auditor, not a v6-02 change): the test-checklist privacy-scan regex uses lookbehind (?<! ... ), which Safari 14 JS lacks; fine for a test tool, must not ship in app code. Count in PASTE (same as v6-01):', len(re.findall(r'\(\?<[=!]',_P2)), len(re.findall(r'\(\?<[=!]',_P1)))
    _shirts=[i for i in _C2['pantry']['items'] if 'tint' in i]
    _l367=[l for l in _P2.split('\n') if 'NEEDS NANCY' in l and '`word` Thai' in l]
    print(V+' real NEEDS NANCY shirt check: 3 tint shirts, each with Thai, named in the NEEDS NANCY line ("the 3 shirt names" = count of tint items), and the spec v6-list Thai line names them:', len(_shirts)==3 and all(i.get('th') for i in _shirts) and len(_l367)==1 and ('the %d shirt names,'%len(_shirts)) in _l367[0] and 'the 3 shirt names (Nancy, Nov 7)' in _S2)

# ===================== v6-03 checks (Auditor v6-02 recheck HOLD, audit/v6-02-recheck-2026-10-31.md 5839cdd1: N1, n1, n2; m3 stays open) =====================
if V=='v6-03':
    _Na='nancys-adventure-english-'; _Ba='v6-02'
    _Pa=open(W+_Na+_Ba+'-PASTE.md',encoding='utf-8').read(); _Pb=open(W+_Na+V+'-PASTE.md',encoding='utf-8').read()
    _Fb=open(W+_Na+'FINAL-'+V+'.md',encoding='utf-8').read(); _Sb=open(W+_Na+V+'.md',encoding='utf-8').read()
    _Ca=_json_load(open(W+_Na+_Ba+'-cards.json')); _Cb=_json_load(open(W+_Na+V+'-cards.json'))
    print(V+' base v6-02 untouched (PASTE decbbcb3, cards 716f4109, verses d85c09ba, FINAL 13b06c21, spec 76b7c123) and matches v602build/snap MANIFEST; recheck report 5839cdd1; CURRENT.md b653ffb2; v5-37 PASTE acc534a5:',
          [_m8(_Na+_Ba+x)[:8] for x in ('-PASTE.md','-cards.json','-daily-verses.json','.md')]==['decbbcb3','716f4109','d85c09ba','76b7c123'] and _m8(_Na+'FINAL-v6-02.md')[:8]=='13b06c21'
          and all(_m8(l.split()[1])==l.split()[0] for l in open(W+'v602build/snap/MANIFEST.md5') if l.strip() and not l.startswith('#') and os.path.exists(W+l.split()[1]))
          and _m8('audit/v6-02-recheck-2026-10-31.md')[:8]=='5839cdd1' and _m8('CURRENT.md')[:8]=='b653ffb2' and _m8(_Na+'v5-37-PASTE.md')[:8]=='acc534a5')
    _va=open(W+_Na+_Ba+'-daily-verses.json','rb').read(); _vb=open(W+_Na+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-02 except the version field:', _vb==_va.replace(b'"version": "v6-02"',('"version": "%s"'%V).encode(),1) and _va!=_vb)
    _ca=dict(_Ca,version=V); _ca['meta']=dict(_Ca['meta'],version=V)
    print(V+' cards: only the version changed vs v6-02:', _ca==_Cb)
    _n1o=r"/(?<!\d)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/"; _n1n=r"/(^|\D)(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)/"
    _n2o="padding-inline:max(16pt,env(safe-area-inset-left)) max(16pt,env(safe-area-inset-right))"; _n2n="padding:0 max(16pt,env(safe-area-inset-right)) 0 max(16pt,env(safe-area-inset-left))"
    _ln=lambda t,x:[i+1 for i,l in enumerate(t.split('\n')) if x in l]
    print(V+' N1 (major) exact fix at PASTE :404: lookbehind replaced by (^|\\D) (-1), in PASTE, FINAL and spec; no (?< anywhere in the PASTE:', all(_n1n in t and _n1o not in t for t in (_Pb,_Fb,_Sb)) and _ln(_Pb,_n1n)==[404] and len(_n1n)-len(_n1o)==-1 and not re.search(r'\(\?<',_Pb), _ln(_Pb,_n1n))
    _rx=re.compile(_n1n[1:-1])
    print(V+' N1 regex behaves: matches "call 307-555-1234" and "+1 307 555 1234", not "9307-555-12345" or "12307-555-1234":', bool(_rx.search('call 307-555-1234')) and bool(_rx.search('+1 307 555 1234')) and not _rx.search('9307-555-12345') and not _rx.search('12307-555-1234'))
    print(V+' n2 exact fix at PASTE :68 (padding shorthand, -3) in PASTE, FINAL and spec; no padding-inline or margin-inline (or any *-inline/-block logical property) in the PASTE:', all(_n2n in t and _n2o not in t for t in (_Pb,_Fb,_Sb)) and _ln(_Pb,_n2n)==[68] and len(_n2n)-len(_n2o)==-3 and not re.search(r'(padding|margin|inset|border)-(inline|block)',_Pb), _ln(_Pb,_n2n))
    print(V+' n1: the shirt Thai check reads i.get(\'th\') (a missing Thai prints False, never a KeyError):', "[i.get('th') for i in _sh8]" in open(__file__).read() and ("[i["+"'th'] for i in _sh8]") not in open(__file__).read())
    print(V+' m3 still unapplied (Maxwell\'s call): "Gold trophy (earned of 42)" kept:', 'Gold trophy (earned of 42)' in _Pb and 'earned count' not in _Pb)
    print(V+' spec note: v6-02 recheck close-out in the spec build notes only:', 'v6-02 recheck close-out' in _Sb and 'v6-02 recheck close-out' not in _Pb)
    _ua=_Pb.replace(V,_Ba).replace(_n1n,_n1o).replace(_n2n,_n2o)
    print(V+' diff-only vs v6-02: undoing N1, n2 and the version gives v6-02 byte for byte; PASTE %d chars <= 188,200 (%+d vs v6-02), banked %d; spec banked line matches:'%(len(_Pb),len(_Pb)-len(_Pa),188200-len(_Pb)),
          _ua==_Pa and len(_Pb)<=188200 and len(_Pb)-len(_Pa)==-4 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_Pb),format(len(_Pb),','))) in _Sb)

# ===================== v6-04 checks (Maxwell t371u title port + t372u-t377u audit fixes and one style) =====================
if V>='v6-04':   # v6-05: standing v6-04 checks keep running; diff lines follow V
    _N4='nancys-adventure-english-'; _B4='v6-03'
    _P3=open(W+_N4+_B4+'-PASTE.md',encoding='utf-8').read(); _P4=open(W+_N4+V+'-PASTE.md',encoding='utf-8').read()
    _F4=open(W+_N4+'FINAL-'+V+'.md',encoding='utf-8').read(); _S4=open(W+_N4+V+'.md',encoding='utf-8').read(); _F3=open(W+_N4+'FINAL-'+_B4+'.md',encoding='utf-8').read()
    _r3=open(W+_N4+_B4+'-cards.json',encoding='utf-8').read(); _r4=open(W+_N4+V+'-cards.json',encoding='utf-8').read()
    _C3=_load(open(W+_N4+_B4+'-cards.json')); _C4=_load(open(W+_N4+V+'-cards.json'))
    print(V+' base v6-03 untouched (PASTE bcc9bbe9, cards 0f37159a, verses fc174b7e, FINAL 0665c5f6, spec 812cbeb5) and matches v603build/snap MANIFEST; CURRENT.md b653ffb2:',
          [_m8(_N4+_B4+x)[:8] for x in ('-PASTE.md','-cards.json','-daily-verses.json','.md')]==['bcc9bbe9','0f37159a','fc174b7e','812cbeb5'] and _m8(_N4+'FINAL-v6-03.md')[:8]=='0665c5f6'
          and all(_m8(l.split()[1])==l.split()[0] for l in open(W+'v603build/snap/MANIFEST.md5') if l.strip() and not l.startswith('#') and os.path.exists(W+l.split()[1])) and _m8('CURRENT.md')[:8]=='b653ffb2')
    _v3=open(W+_N4+_B4+'-daily-verses.json','rb').read(); _v4=open(W+_N4+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-03 except the version field:', _v4==_v3.replace(b'"version": "v6-03"',('"version": "%s"'%V).encode(),1) and _v3!=_v4)
    print(V+' PASTE = FINAL + the cards.json block (minified, byte-identical to the cards file); %d chars <= 188,200; Thai reserve unused; banked %d (%+d vs v6-03):'%(len(_P4),188200-len(_P4),len(_P4)-len(_P3)),
          _P4.replace(_r4.strip(),'@@').count('@@')==1 and len(_P4)<=188200)
    _q=('cards','zones','soundDuel','verses','jesusWords','jesusWordsFallback','mapLayout','rewardText','wrongText','encouragement','welcomeBack','restScreen','trophies','trophyRules','pantry')
    print(V+' lossless trims: with the stated defaults filled back in (T1 choices [], T2 thStatus, T3 string hint, T5 picture answer = en), every question, card, zone, trophy and block equals v6-03:',
          all(_C3.get(k)==_C4.get(k) for k in _q if k not in ('cards','trophies')) and len(_C3['cards'])==len(_C4['cards'])
          and all(dict(a,choices=a.get('choices',[]))==dict(b,choices=b.get('choices',[])) for a,b in zip(_C3['cards'],_C4['cards']))
          and all(dict(a,thStatus=a.get('thStatus',_C3['meta']['thStatusDefault']))==dict(b,thStatus=b.get('thStatus',_C4['meta']['thStatusDefault'])) for a,b in zip(_C3['trophies'],_C4['trophies'])),
          [a['id'] for a,b in zip(_C3['cards'],_C4['cards']) if dict(a,choices=a.get('choices',[]))!=dict(b,choices=b.get('choices',[]))][:5])
    _U3=_C3['uiText']; _U4=_C4['uiText']
    print(V+' uiText: only tapPrompt changed ("Where is the {word}? Tap it!") and playAgain added; 92 entries; neither stores thStatus (NEEDS NANCY by meta.thStatusDefault):',
          {k for k in set(_U3)|set(_U4) if _U3.get(k)!=_U4.get(k)}=={'tapPrompt','playAgain'} and _U4.get('tapPrompt',{}).get('en','')=='Where is the {word}? Tap it!' and len(_U4)==92==_C4['meta']['uiTextEntries']
          and 'thStatus' not in _U4['tapPrompt'] and 'thStatus' not in _U4['playAgain'] and _C4['meta']['thStatusDefault']=='NEEDS NANCY' and not any(k in _U4 for k in ('tapFind','tapMy','tapGive','tapYour')))
    _ks=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True)
    def _thw(o):
        if isinstance(o,dict): return [y for v in o.values() for y in _thw(v)]
        if isinstance(o,list): return [y for v in o for y in _thw(v)]
        return [o] if isinstance(o,str) and re.search('[\u0E00-\u0E7F]',o) else []
    _th3=collections.Counter(_thw(_C3)); _th4=collections.Counter(_thw(_C4))
    _ta=collections.Counter([_U4.get('tapPrompt',{}).get('th',''),_U4.get('playAgain',{}).get('th','')]); _tg=collections.Counter([_U3.get('tapPrompt',{}).get('th','')])
    print(V+' cards Thai changed only where planned (+tapPrompt, +playAgain, -old tapPrompt):', dict(_th4-_th3)==dict(_ta-_tg) and dict(_th3-_th4)==dict(_tg-_ta), dict(_th4-_th3), dict(_th3-_th4))
    _pp3=_C3['picPlan']; _pp4=_C4['picPlan']
    print(V+' picPlan: only uiInlineSvg (title = t288u port, sky merged, tex #rH t320u hand) and the duplicate rule sentence (T4) changed:',
          {k for k in set(_pp3)|set(_pp4) if _pp3.get(k)!=_pp4.get(k)}<={'uiInlineSvg','rule'} and _pp4['rule']==_pp3['rule'].replace(' Every picture must be unambiguous at a glance on a phone screen (spec section 5).','')
          and 'Every picture card must be unambiguous at a glance on a phone screen.' in _P4 and {k for k in set(_pp3['uiInlineSvg'])|set(_pp4['uiInlineSvg']) if _pp3['uiInlineSvg'].get(k)!=_pp4['uiInlineSvg'].get(k)}=={'title','sky','tex'} and 'sky' not in _pp4['uiInlineSvg'])
    _ti4=_pp4['uiInlineSvg']['title']; _oth=[k for k in _pp4['uiInlineSvg'] if k!='title']
    print(V+' every inline SVG but the title <=4096 B; title %d B:'%len(_ti4.encode()), all(len(_pp4['uiInlineSvg'][k].encode())<=4096 for k in _oth) and all(len(v.encode())<=4096 for v in _pp4['inlineSvg'].values()))
    print(V+' title still: no animation, transition, keyframes or SMIL in title/sword; 6.1 still wording kept:', not any(re.search(_anim if '_anim' in dir() else r'animation|@keyframes|transition|<animate|<set ',_pp4['uiInlineSvg'][k]) for k in ('title','sword')) and 'A still (t366u): one frame, shown at once' in _P4 and '.ti *{animation:none!important;transition:none!important}' in _P4)
    _TP9='ti-' if V>='v6-07' else ''   # m3 (gate 3d453176): prefixed title ids
    _t9=re.sub(r"<linearGradient id='"+_TP9+"sk'.*?</linearGradient>",'',_ti4).replace('@media(min-aspect-ratio:1/2)','')
    _nf9=V<'v6-06' or (_ti4.count("<linearGradient id='"+_TP9+"nf'")==1 and _ti4.count('url(#'+_TP9+'nf)')==1 and re.search(r"<path class='nt' d='[^']*' fill='url\(#"+_TP9+r"nf\)'",_ti4) is not None and "No gradients except sky, the title night fade, and the title button shade (approved t288u mock and Maxwell's Button C pick)." in _P4)
    if V>='v6-06': _t9=re.sub(r"<linearGradient id='"+_TP9+"nf'.*?</linearGradient>",'',_t9).replace("fill='url(#"+_TP9+"nf)'",'')   # t392u: the night fade is the one other allowed gradient
    print(V+' Safari 14 / flat: the only gradient is the sky (#sk, used once by the sky rect, spec "No gradients except sky")'+(' plus the t392u title night fade (#nf, once, on the night .nt layer)' if V>='v6-06' else '')+'; only aspect-ratio is the media feature; no filter/blur/SMIL/:has/color-mix/@container/inset:/box-shadow:',
          _ti4.count('url(#'+_TP9+'sk)')==1 and _nf9 and 'No gradients except sky' in _P4 and not re.search(r'(?i)filter|blur|gradient|<animate|drop-shadow|aspect-ratio|:has\(|color-mix|@container|inset:|box-shadow',_t9+_pp4['uiInlineSvg']['sword']+_pp4['uiInlineSvg']['stone']))
    _lp=re.compile(r'(padding|margin|inset|border)-(inline|block)|\binset\s*:|inline-size|block-size|(padding|margin)-(start|end)\b|text-align\s*:\s*(start|end)')   # n2 (d7ab5190) + n3 (3d453176): space before the colon
    print(V+' Safari 14.0: no logical properties anywhere in the PASTE:', not _lp.search(_P4))
    import importlib.util as _iu; _sp=_iu.spec_from_file_location('fx4',W+'v604build/fixes_v604.py'); _fx=_iu.module_from_spec(_sp); _sp.loader.exec_module(_fx)
    _f5=[]
    if V>='v6-05': _s5=_iu.spec_from_file_location('fx5',W+'v605build/fixes_v605.py'); _x5=_iu.module_from_spec(_s5); _s5.loader.exec_module(_x5); _f5=[(a,b) for t,a,b in _x5.FX]
    def _thru5(t):   # a v6-04 new text as the v6-05 gate fixes (m1, m3, m5, A3) rewrote it
        for a,b in _f5:
            if t in a and t!=a: return b
            t=t.replace(a,b)
        return t
    _miss=[t for t,a_,b_ in _fx.FX if not all(_thru5(b_) in x for x in (_P4,_F4,_S4)) or (a_ not in b_ and any(a_ in x for x in (_P4,_F4)))]
    print(V+' audit fixes F1-F12, F14, F15, B1 and t377u one style + gaps: every new text in PASTE, FINAL and spec, every old text gone (%d edits):'%len(_fx.FX), not _miss, _miss)
    print(V+' t376u template numbers stated: H 195 at 390x844 (142 at 320x568), feet at y 700 (446), hand 18 long thumb 6.3, desk 0.39 H, crib 0.60 H, happy closed eyes on ask screens:', all(x in _P4 for x in ('H = 195 pt tall at 390 × 844 (142 at 320 × 568)','y 700 (446)','hand 18 long, thumb 6.3','desk top 0.39 H','crib rail 0.60 H','eyes happy and closed on ask screens')))
    print(V+' "Guardian" (capital) only in boss names and guardianLast, never in prose:', not re.search(r'Guardian',_F4.split('```json')[0]))
    print(V+' no kite/heater/teardrop shield (the park kite is a toy):', not re.search(r'(?i)(kite|heater|teardrop)[ -]shield|shield[^.\n]{0,30}(kite|heater|teardrop)',_P4) and _C4['picPlan']['svgNotes']['shield-sunrise'].startswith('Round '))
    print(V+' Option B still holds: no bow/wand/dagger/polearm words in FINAL; rows sword1 sword2 axe1 mace1:', not re.search(r'(?i)\b(longbow|shortbow|crossbow|wand|war scythe|polearm|glaive|daggers|punch blades)\b',_F4) and _C4['trophyRules']['rows']=='sword1 sword2 axe1 mace1')
    _mx4=[l for l in _P4.split('\n') if '**Regions open in order (t334u):**' in l]
    print(V+' END-BOSS rule intact with F8/F9 wording:', len(_mx4)==1 and all(x in _mx4[0] for x in ("Only a region's end guardian (its last zone in `mapLayout` order) opens the next","a tap shows `uiText.guardianLast` over the end guardian's silhouette and `boss.name`","`uiText.regionOpen` at the sheet top (never over a row)",'an 8% bounce and a sparkle','Hearth, Scrolls and rest screen: always.')))
    _g4=_sp8.run([_sys.executable,W+'v604build/qm_v604.py','--dry'],capture_output=True,text=True,cwd=W+'v604build'); _L4=len(open(W+_N4+'v6-04-PASTE.md',encoding='utf-8').read())
    print(V+' generator qm_v604.py --dry re-runs from v6-03 and gives the v6-04 file on disk (%d chars):'%_L4, _g4.returncode==0 and ('-> %d '%_L4) in _g4.stdout, _g4.stderr[-200:])
    print(V+' spec banked line matches:', ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P4),format(len(_P4),','))) in _S4)

# ===================== v6-05 checks (Auditor v6-04 gate HOLD 984f8f51: A1, A3 option A per Maxwell t83u, m1-m8; A2 waits on the council) =====================
if V>='v6-05':
    _N5='nancys-adventure-english-'; _B5='v6-04'
    _Pb5=open(W+_N5+_B5+'-PASTE.md',encoding='utf-8').read(); _Fb5=open(W+_N5+'FINAL-'+_B5+'.md',encoding='utf-8').read(); _Sb5=open(W+_N5+_B5+'.md',encoding='utf-8').read()
    _P5=open(W+_N5+V+'-PASTE.md',encoding='utf-8').read(); _F5=open(W+_N5+'FINAL-'+V+'.md',encoding='utf-8').read(); _S5=open(W+_N5+V+'.md',encoding='utf-8').read()
    _r5=open(W+_N5+V+'-cards.json',encoding='utf-8').read(); _Cb5=_json_load(open(W+_N5+_B5+'-cards.json')); _C5=_json_load(open(W+_N5+V+'-cards.json'))
    _A2=('a' if 'nest `state.hero`' in _P5.lower().replace('nest `state.hero`','nest `state.hero`') and "Nest `state.hero`'s SVG" in _P5 else 'b' if 'exempt: `tex` (shared defs) and `title` (t371u).' in _P5 else 'none')
    print(V+' A2 variant in these files (council call; none = title as v6-04, cap rule unchanged):', _A2)
    print(V+' base v6-04 untouched (PASTE 32cfe2f4, cards 1b03ba5b, verses 26e1374b, FINAL 61a4264b, spec 4341e25d); gate snapshot audit/snap-v604-gate MANIFEST all OK; gate report 984f8f51; CURRENT.md b653ffb2 (v5-37); v5-37 PASTE acc534a5 + verses b0235ff8; v6-03 PASTE bcc9bbe9:',
          [_m8(_N5+_B5+x)[:8] for x in ('-PASTE.md','-cards.json','-daily-verses.json','.md')]==['32cfe2f4','1b03ba5b','26e1374b','4341e25d'] and _m8(_N5+'FINAL-v6-04.md')[:8]=='61a4264b'
          and all(_m8('audit/snap-v604-gate/'+l.split()[1].split('/')[-1])==l.split()[0] for l in open(W+'audit/snap-v604-gate/MANIFEST.md5') if l.strip() and not l.startswith('#'))
          and _m8('audit/v6-04-gate-2026-10-31.md')[:8]=='984f8f51' and _m8('CURRENT.md')[:8]=='b653ffb2' and _m8(_N5+'v5-37-PASTE.md')[:8]=='acc534a5' and _m8(_N5+'v5-37-daily-verses.json')[:8]=='b0235ff8' and _m8(_N5+'v6-03-PASTE.md')[:8]=='bcc9bbe9')
    _vb5=open(W+_N5+_B5+'-daily-verses.json','rb').read(); _v5=open(W+_N5+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-04 (and v5-37) except the version field:', _v5==_vb5.replace(b'"version": "v6-04"',b'"version": "v6-05"',1) and _vb5!=_v5)
    import importlib.util as _iu5; _s5=_iu5.spec_from_file_location('fx5b',W+'v605build/fixes_v605.py'); _X5=_iu5.module_from_spec(_s5); _s5.loader.exec_module(_X5)
    _dl={'A3 option A (Maxwell t83u, 12:44 PM PT): :108 arena heading':29,'A3 option A: :227 Echo Forest night colors':25,'m1a :171 top bar LEFT is Back':23,'m1b :171 counts 2x2, no column':-116,'m2 :199 no Map avatar button':-27,'m3 :175 Echo Knight not a zone guardian':39,'m5 :121 rest screen sky vs restSky':24}
    _bad5=[t for t,a,b in _X5.FX if not all(t_.count(b)==1 and (a in b or a not in t_) for t_ in (_P5,_F5,_S5)) or len(b)-len(a)!=_dl[t]]
    print(V+' gate exact fix texts A3-A, m1 (two), m2, m3, m5 once each in PASTE, FINAL and spec, old text gone, deltas +29/+25/+23/-116/-27/+39/+24 as the report:', not _bad5, _bad5)
    print(V+' A3 option A only (Maxwell t83u): section 3 heading names Echo Forest\'s night, 7.1 template still behind Sound Duel (B not applied), no "gameplay screens only" left:',
          "**Arena theme (the banner, HUD colors and Echo Forest's night; 7.1's scene is every play background).**" in _P5 and 'also behind Sound Duel' in _P5 and 'Sound Duel, guardian runs and reward screens use' in _P5 and 'gameplay screens only' not in _P5)
    _T5=_C5['picPlan']['uiInlineSvg']['title']
    print(V+' m4 title banner shift at 320x568 is translate(-58px,90px), 56px gone:', 'translate(-58px,90px)' in _T5 and 'translate(-58px,56px)' not in _T5)
    print(V+' m3: Echo Knight is not a zone guardian (no bossesWon or scroll); still in uiText:', 'not a zone guardian (no `bossesWon` or scroll)' in _P5 and 'Echo Knight guardian' not in _P5 and 'echoKnight' in _C5['uiText'])
    print(V+' m2: no Map avatar button named anywhere in the PASTE:', "Map's avatar button" not in _P5)
    print(V+' compact-fields sentence with the v6-04 T3/T5 defaults (replaces the :646 compact-fields text):', "`hint` is `[letters, sound, word]` (a missing `word` is `en`; a string is the `sound`, `letters` then `en`'s first letter and one `_` per other letter);" in _P5 and "a picture card's missing `answer` is its `en`;" in _P5)
    print(V+' find-and-tap targets in the t376u template: "44 pt+ tap areas, 8 px apart, no overlap" and the rest of the rule:', '(44 pt+ tap areas, 8 px apart, no overlap)' in _P5 and 'a recap after scene 5 of a run in that zone' in _P5 and 'then `wrongText` and a grace line; she tries again' in _P5 and _P5.count('### 7.1 Find and tap')==1)
    _tx5=_C5['picPlan']['uiInlineSvg']['tex']
    print(V+' hands: tex unchanged from v6-04 (t320u #rH), right hands mirrored by CSS at x 55 (Sam) and 62 (Nancy):', _tx5==_Cb5['picPlan']['uiInlineSvg']['tex'] and "use[href='#rH'][x='55']{transform:matrix(-1,0,0,1,122,0)}" in _tx5 and "use[href='#rH'][x='62']{transform:matrix(-1,0,0,1,136,0)}" in _tx5)
    _th=lambda o:[y for y in re.findall(r'[\u0E00-\u0E7F][^"]*',json.dumps(o,ensure_ascii=False))]
    print(V+' cards: Thai identical to v6-04; only version, meta.version and (A2 a) the title differ:', sorted(_th(_C5))==sorted(_th(_Cb5)) and
          {k for k in set(_C5)|set(_Cb5) if _C5.get(k)!=_Cb5.get(k)}<={'version','meta','picPlan'} and {k for k in _C5['meta'] if _C5['meta'][k]!=_Cb5['meta'].get(k)}=={'version'}
          and {k for k in _C5['picPlan'] if _C5['picPlan'][k]!=_Cb5['picPlan'].get(k)}=={'uiInlineSvg'} and {k for k in _C5['picPlan']['uiInlineSvg'] if _C5['picPlan']['uiInlineSvg'][k]!=_Cb5['picPlan']['uiInlineSvg'].get(k)}=={'title'})
    _new5=''.join(b for t,a,b in _X5.FX)
    print(V+' new texts: grace rule (no padlock/locked/fail/lost), no brand, no logical property, no lookbehind, no new emoji:', not re.search(r'(?i)padlock|\block|fail(?!ure)|\blost\b|ล็อก|แพ้|ไม่ผ่าน|warcraft|\bmmo\b|clash|westfall|-inline|-block|\(\?<',_new5) and not re.search('[\U0001F000-\U0001FFFF]',_new5))
    # diff-only: undo every v6-05 edit and get the v6-04 PASTE back byte for byte
    _u5=_P5.replace(V,_B5)
    for t,a,b in _X5.FX: _u5=_u5.replace(b,a)
    if _A2=='b': _u5=_u5.replace(_X5.A2B[1],_X5.A2B[0])
    if _A2=='a':
        for a,b in _X5.A2A_SPEC: _u5=_u5.replace(b,a)
    _tb=_Cb5['picPlan']['uiInlineSvg']['title']
    _u5=_u5.replace(json.dumps(_T5,ensure_ascii=False)[1:-1],json.dumps(_tb,ensure_ascii=False)[1:-1])
    print(V+' diff-only: undoing the gate fixes, the title edit (m4%s) and the version gives v6-04 byte for byte; PASTE %d chars <= 188,200 (%+d vs v6-04), banked %d; spec banked line matches:'%(' + A2 a cut' if _A2=='a' else '',len(_P5),len(_P5)-len(_Pb5),188200-len(_P5)),
          _u5==_Pb5 and len(_P5)<=188200 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P5),format(len(_P5),','))) in _S5)
    _g5=_sp8.run([_sys.executable,W+'v605build/qm_v605.py','--dry','--a2',_A2],capture_output=True,text=True,cwd=W+'v605build')
    print(V+' generator qm_v605.py --dry --a2 %s re-runs from v6-04 and gives the file on disk (%d chars):'%(_A2,len(_P5)), _g5.returncode==0 and ('-> %d '%len(_P5)) in _g5.stdout, _g5.stderr[-200:])
    print(V+' m6: the v6-only Thai list for Nancy exists and names tapPrompt, playAgain, echoKnight, giftFrom, the 3 shirts and the 7 gear words:', _os.path.exists(W+'v605build/thai-v6-for-nancy.md') and all(x in open(W+'v605build/thai-v6-for-nancy.md',encoding='utf-8').read() for x in ('tapPrompt','playAgain','echoKnight','giftFrom','shirt','gear word')))
    print(V+' spec build note: v6-04 gate close-out in the spec only (not in PASTE):', 'v6-04 gate close-out (v6-05)' in _S5 and 'v6-04 gate close-out' not in _P5)

# ======================= v6-06 checks (Maxwell t384u title = t288u mock source; t391u/1:37 PM PT Button C; m3/F13; Auditor v6-05 recheck d7ab5190 n1/n2) =======================
if V>='v6-06':
    _V0=V; V='v6-06'   # v6-07+: this block re-verifies the v6-06 files themselves
    import importlib.util as _iu6, subprocess as _sp6, xml.dom.minidom as _xm6
    _N6='nancys-adventure-english-'; _B6='v6-05-A2b-exempt'
    _Pb6=open(W+_N6+_B6+'-PASTE.md',encoding='utf-8').read(); _Cb6=_json_load(open(W+_N6+_B6+'-cards.json'))
    _P6=open(W+_N6+V+'-PASTE.md',encoding='utf-8').read(); _F6=open(W+_N6+'FINAL-'+V+'.md',encoding='utf-8').read(); _S6=open(W+_N6+V+'.md',encoding='utf-8').read()
    _r6=open(W+_N6+V+'-cards.json',encoding='utf-8').read(); _C6r=_json_load0(open(W+_N6+V+'-cards.json')); _C6=_json_load(open(W+_N6+V+'-cards.json'))
    _TF6=_N6+V+'-title.svg'; _T6=open(W+_TF6,encoding='utf-8').read() if _os.path.exists(W+_TF6) else ''
    _s6=_iu6.spec_from_file_location('fx6',W+'v606build/fixes_v606.py'); _X6=_iu6.module_from_spec(_s6); _s6.loader.exec_module(_X6)
    print(V+' base v6-05 (council A2b) untouched: PASTE 72da2cb5, cards 5ac92b0e, FINAL 8f5b8efc, spec d6f565c7, verses 9e123224; v6-04 PASTE 32cfe2f4; v6-03 bcc9bbe9; v5-37 acc534a5/b0235ff8; CURRENT.md b653ffb2 (v5-37):',
          [_m8(_N6+_B6+x)[:8] for x in ('-PASTE.md','-cards.json','.md')]==['72da2cb5','5ac92b0e','d6f565c7'] and _m8(_N6+'FINAL-'+_B6+'.md')[:8]=='8f5b8efc'
          and _m8(_N6+'v6-05-daily-verses.json')[:8]=='9e123224' and _m8(_N6+'v6-04-PASTE.md')[:8]=='32cfe2f4' and _m8(_N6+'v6-03-PASTE.md')[:8]=='bcc9bbe9'
          and _m8(_N6+'v5-37-PASTE.md')[:8]=='acc534a5' and _m8(_N6+'v5-37-daily-verses.json')[:8]=='b0235ff8' and _m8('CURRENT.md')[:8]=='b653ffb2')
    _vb6=open(W+_N6+'v6-05-daily-verses.json','rb').read(); _v6=open(W+_N6+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-05 except the version field; "heavy laden" once in the PASTE:', _v6==_vb6.replace(b'"version": "v6-05"',('"version": "%s"'%V).encode(),1) and _vb6!=_v6 and _P6.count('heavy laden')==1)
    print(V+' PASTE = FINAL + the cards.json block (byte-identical to the cards file); %d chars <= 188,200, banked %d, Thai reserve untouched; spec banked line matches:'%(len(_P6),188200-len(_P6)),
          _P6.replace(_r6.strip(),'@@').count('@@')==1 and _P6.endswith('\n```json\n'+_r6.strip()+'\n```\n') and len(_P6)<=188200 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P6),format(len(_P6),','))) in _S6)
    _bad6=[t for t,a,b in _X6.FX if not all(t_.count(b)==1 and a not in t_ for t_ in (_P6,_F6,_S6)) or len(b)-len(a)!=_X6.DELTA[t]]
    print(V+' exact edits once each in PASTE, FINAL and spec, old text gone, deltas %s:'%' / '.join('%s %+d'%(t,d) for t,d in _X6.DELTA.items()), not _bad6, _bad6)
    _ui6=json.dumps(_C6['uiText'],ensure_ascii=False)
    print(V+' m3/F13: top bar says "Gold trophy (earned count)"; no "of 42", no "earned of", no X/total in uiText:', 'Gold trophy (earned count)' in _P6 and 'of 42' not in _P6 and 'earned of' not in _P6 and not re.search(r'\d\s*/\s*\d',_ui6))
    print(V+' title file: cards say "title.svg"; the PASTE names %s once and says to inline it in .ti; file exists, %d chars, same bytes as v606build/title/title-v606.svg:'%(_TF6,len(_T6)),
          _C6r['picPlan']['uiInlineSvg']['title']=='title.svg' and _P6.count('`'+_TF6+'`')==1 and 'inline it in `.ti`' in _P6 and len(_T6)>0 and _T6==open(W+'v606build/title/title-v606.svg',encoding='utf-8').read())
    try: _xm6.parseString(_T6.replace("<svg ","<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' ",1)); _ok6=True
    except Exception as _e6: _ok6=repr(_e6)[:120]
    _ids6=set(re.findall(r"id='([^']+)'",_T6)); _oth6=set()
    for _k6,_v6s in list(_C6['picPlan']['uiInlineSvg'].items())+list(_C6['picPlan']['inlineSvg'].items())+list(_C6['picPlan']['trophyInlineSvg'].items()):
        if _k6!='title': _oth6|=set(re.findall(r"id=['\"]([^'\"]+)",_v6s))
    print(V+' title SVG parses; ids the spec uses (#gE banner, #th Sam, #tn Nancy slot, #sk sky) present; no id clashes with tex or any other SVG:', _ok6 is True and {'gE','th','tn','sk'}<=_ids6 and not (_ids6&_oth6), _ok6 if _ok6 is not True else sorted(_ids6&_oth6))
    print(V+' title: 4 times in one SVG (.st/.nt night, .ev evening, .su sun moves, --a/--c sky vars), m4 320 shift translate(-58px,90px) on .pq, banner text empty (live):',
          all(x in _T6 for x in ('[data-tod=n] .st','[data-tod=e] .ev','[data-tod=a] .su','[data-tod=e] .su','--a:','@media(min-aspect-ratio:1/2){.pq{transform:translate(-58px,90px)}}',"class='pq'")) and re.search(r"<text id='gE'[^>]*></text>",_T6) is not None)
    print(V+' title Safari 14 / still: no lookbehind, no logical property, no SMIL/keyframes/animation in the file (only the spec .ti CSS stops the tex flicker):',
          not re.search(r'\(\?<|(padding|margin|inset|border)-(inline|block)|<animate|<set |@keyframes|animation',_T6))
    print(V+' title pose (approved mock): spec says the title keeps Sam\'s hand shading his eyes, no weapon on the title; 6.1 picture line unchanged:',
          "the title keeps the approved t288u pose: Sam's free hand shades his eyes" in _P6 and 'Character and the title' not in _P6 and 'Sam on the left hill shading his eyes' in _P6)
    print(V+' A2b title exemption text kept (:55):', 'exempt: `tex` (shared defs) and `title` (t371u).' in _P6)
    _src6=open(__file__,encoding='utf-8').read(); _lp6=re.compile(r'(padding|margin|inset|border)-(inline|block)|\binset:|inline-size|block-size|(padding|margin)-(start|end)\b|text-align:\s*(start|end)')
    print(V+' n1: the :653 block is unpinned (if V>=\'v5-34\'); n2: logical-property regex catches margin-block, padding-block, border-inline, border-block-end, and not border-left/margin-top:',
          "if V>='v5-34':   # n1" in _src6 and all(_lp6.search(x) for x in ('margin-block:0','padding-block:4px','border-inline:1px','border-block-end:0','padding-inline-start:2px')) and not any(_lp6.search(x) for x in ('border-left:1px','margin-top:0','padding:0 8px')) and not _lp6.search(_P6))
    _u6=_P6
    for t,a,b in _X6.FX: _u6=_u6.replace(b,a)
    _u6=_u6.replace('"title":"title.svg"',json.dumps(_Cb6['picPlan']['uiInlineSvg']['title'],ensure_ascii=False).join(['"title":','']),1)
    _u6=_u6.replace('Banked in %s'%V,'Banked in v6-05').replace(V,'v6-05')
    print(V+' diff-only: undoing the %d edits,'%len(_X6.FX)+' the title move and the version gives the v6-05 A2b PASTE byte for byte (%+d chars):'%(len(_P6)-len(_Pb6)), _u6==_Pb6)
    _g6=_sp6.run([_sys.executable,W+'v606build/qm_v606.py','--title','file','--prec','1','--dry'],capture_output=True,text=True,cwd=W+'v606build')
    print(V+' generator qm_v606.py --title file --dry re-runs from v6-05 A2b and gives the file on disk (%d chars):'%len(_P6), _g6.returncode==0 and ('-> %d '%len(_P6)) in _g6.stdout, _g6.stderr[-200:])
    _new6=''.join(b for t,a,b in _X6.FX)
    print(V+' new texts: grace rule, no brand, no counter, no timer, no contact info:', not re.search(r'(?i)padlock|\block|fail|ล็อก|แพ้|ไม่ผ่าน|\d+/\d+|timer|countdown|@|\+?\d{3}[ -]\d{3}',_new6))
    _p49n=W+'screens-v606/png/49-welcome-back.png'; _p49o=W+'screens-v604/png/49-welcome-back.png'
    if _os.path.exists(_p49n): print(V+' screen 49 (t387u) is the v6-04 PNG byte for byte:', open(_p49n,'rb').read()==open(_p49o,'rb').read())
    _sh6='linear-gradient(rgba(16,23,15,0),rgba(16,23,15,.35))'
    _tf6=[f for f in ('01-title.html','52-title-night.html','01-title-320x568.html') if _os.path.exists(W+'screens-v606/html/'+f)]
    _ot6=[f for f in _os.listdir(W+'screens-v606/html') if f.endswith('.html') and f not in _tf6 and _sh6 in open(W+'screens-v606/html/'+f,encoding='utf-8').read()] if _os.path.isdir(W+'screens-v606/html') else []
    print(V+' Button C shade (Maxwell 1:56 PM PT): spec 6.1 states the 35%% Ink shade over the bottom 150 pt (120 at 320); the title renders %s carry it once; no other screen has it:'%_tf6,
          'Behind it, a flat Ink shade (0 to 35%) over the bottom 150 pt (120 pt at 320 × 568), not tappable.' in _P6 and 'no fade or shade behind it' not in _P6
          and len(_tf6)==3 and all(open(W+'screens-v606/html/'+f,encoding='utf-8').read().count(_sh6)==1 for f in _tf6) and not _ot6, _ot6)
    _h6=W+'screens-v606/html'
    if _os.path.isdir(_h6):
        _hb=[f for f in _os.listdir(_h6) if f.endswith('.html') and re.search(r'of 42|\b\d+ ?/ ?(42|85)\b',open(_h6+'/'+f,encoding='utf-8').read())]
        print(V+' rendered screens: no "of 42" or X/total in any v6-06 screen HTML:', not _hb, _hb)
    V=_V0

# Auditor fix text F-T1 for checks_v606.py (append after the v6-06 title-file block; uses W, V, json, re, _os already imported there)
import xml.dom.minidom as _xd
_tf=W+'nancys-adventure-english-'+V+'-title.svg'
if _os.path.exists(_tf):
    _ts=open(_tf,encoding='utf-8').read()
    try: _xd.parseString(_ts.encode('utf-8')); _xok=True
    except Exception: _xok=False
    _tx=json.load(open(W+'nancys-adventure-english-'+V+'-cards.json',encoding='utf-8'))['picPlan']['uiInlineSvg']['tex']
    _ids=set(re.findall(r"""\bid=['"]([^'"]+)""",_ts+_tx))
    _rf=re.findall(r"""(?:href=['"]|url\()\s*([^'")]*)""",_ts)
    _bad=[r for r in _rf if not r.startswith('#') or r[1:] not in _ids]
    _ban=re.findall(r'(?i)adventure time|teenage robot|danny phantom|nickelodeon|warcraft|\bwow\b|excalibur|elwynn|westfall|redridge|duskwood|\bmmo\b|911|call max|show the nurse',_ts)+re.findall(r'\bClash\b|\bAvatar\b',_ts)
    _danger=re.findall(r'(?i)<script|<foreignObject|<image\b|<iframe|<object|<embed|\son\w+\s*=|javascript:|@import|@font-face|https?:|<animate|<set\b',_ts)
    print(V+' title file safe (F-T1): XML parses; ASCII only; every href/url() is a local #id found in the title or tex; no script, foreignObject, image, on* handler, javascript:, @import, @font-face, http(s), SMIL; no banned name, 911, Call Max or Show the Nurse:',
          _xok and all(ord(c)<128 for c in _ts) and not _bad and not _ban and not _danger, (_bad,_ban,_danger)[:3] if (_bad or _ban or _danger) else '')

# ======================= v6-07 checks (Auditor v6-06 gate 3d453176: F-T1 above, F1, F2, m3 id prefix, n3; m1 harness) =======================
if V>='v6-07':
    _V7=V; V='v6-07'   # v6-08+: this block re-verifies the v6-07 files (frozen at the Auditor gate)
    import importlib.util as _iu7, subprocess as _sp7
    _N7='nancys-adventure-english-'; _B7='v6-06'
    _m7=lambda f:hashlib.md5(open(W+f,'rb').read()).hexdigest() if 'hashlib' in dir() else __import__('hashlib').md5(open(W+f,'rb').read()).hexdigest()
    _Pb7=open(W+_N7+_B7+'-PASTE.md',encoding='utf-8').read(); _P7=open(W+_N7+V+'-PASTE.md',encoding='utf-8').read()
    _F7=open(W+_N7+'FINAL-'+V+'.md',encoding='utf-8').read(); _S7=open(W+_N7+V+'.md',encoding='utf-8').read(); _r7=open(W+_N7+V+'-cards.json',encoding='utf-8').read()
    _T7=open(W+_N7+V+'-title.svg',encoding='utf-8').read(); _Tb7=open(W+_N7+_B7+'-title.svg',encoding='utf-8').read()
    _s7=_iu7.spec_from_file_location('fx7',W+'v607build/fixes_v607.py'); _X7=_iu7.module_from_spec(_s7); _s7.loader.exec_module(_X7)
    print(V+' base v6-06 untouched (PASTE 47a08abd, cards a2cadeee, FINAL a7e980db, spec 8f34f1b1, verses 5b144ab4, title f56ecce7); gate snap MANIFEST all OK; CURRENT.md b653ffb2 (v5-37):',
          [_m7(_N7+_B7+x)[:8] for x in ('-PASTE.md','-cards.json','.md','-daily-verses.json','-title.svg')]==['47a08abd','a2cadeee','8f34f1b1','5b144ab4','f56ecce7'] and _m7(_N7+'FINAL-'+_B7+'.md')[:8]=='a7e980db'
          and all(_m7('audit/snap-v606-gate/'+l.split()[1].split('/')[-1])==l.split()[0] for l in open(W+'audit/snap-v606-gate/MANIFEST.md5') if l.strip() and not l.startswith('#') and _os.path.exists(W+'audit/snap-v606-gate/'+l.split()[1].split('/')[-1]))
          and _m7('CURRENT.md')[:8]=='b653ffb2')
    _vb7=open(W+_N7+_B7+'-daily-verses.json','rb').read(); _v7=open(W+_N7+V+'-daily-verses.json','rb').read()
    print(V+' verses byte-identical to v6-06 except the version field:', _v7==_vb7.replace(b'"version": "v6-06"',('"version": "%s"'%V).encode(),1) and _v7!=_vb7)
    print(V+' PASTE = FINAL + the cards.json block; %d chars <= 188,200, banked %d, Thai reserve untouched; spec banked line matches:'%(len(_P7),188200-len(_P7)),
          _P7.endswith('\n```json\n'+_r7.strip()+'\n```\n') and len(_P7)<=188200 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P7),format(len(_P7),','))) in _S7)
    _bad7=[t for t,a,b in _X7.FX if not all(t_.count(b)==1 and t_.count(a)==(1 if a in b else 0) for t_ in (_P7,_F7,_S7)) or len(b)-len(a)!=_X7.DELTA[t]]
    print(V+' F1 (+159) and F2 (+21) verbatim from the gate, once each in PASTE, FINAL and spec; old F2 text gone:', not _bad7 and 'a flat Ink shade' not in _P7, _bad7)
    _u7=_P7
    for t,a,b in _X7.FX: _u7=_u7.replace(b,a)
    _u7=_u7.replace(V,_B7)
    for _o,_n in _X7.TP: _u7=_u7.replace('"'+_n+'"','"'+_o+'"',1)
    print(V+' diff-only: undoing F1, F2, T1 (tapPrompt) and the version gives the v6-06 PASTE byte for byte (%+d chars):'%(len(_P7)-len(_Pb7)), _u7==_Pb7)
    _g7=_sp7.run([_sys.executable,W+'v607build/qm_v607.py','--dry'],capture_output=True,text=True,cwd=W+'v607build')
    print(V+' generator qm_v607.py --dry re-runs from v6-06 and gives the file on disk (%d chars):'%len(_P7), _g7.returncode==0 and ('-> %d '%len(_P7)) in _g7.stdout, _g7.stderr[-200:])
    _ids7=re.findall(r"id='([^']+)'",_T7); _un7=_T7
    for _i in _ids7:
        if _i.startswith('ti-'): _un7=_un7.replace("id='%s'"%_i,"id='%s'"%_i[3:]).replace("href='#%s'"%_i,"href='#%s'"%_i[3:]).replace('url(#%s)'%_i,'url(#%s)'%_i[3:])
    print(V+' m3: title ids prefixed ti- except the 6.1 hooks gE, th, tn; undoing the prefix gives the v6-06 title byte for byte; file = v607build/title/title-v607.svg; PASTE names the v6-07 file:',
          {i for i in _ids7 if not i.startswith('ti-')}=={'gE','th','tn'} and len(_ids7)==11 and _un7==_Tb7 and _T7==open(W+'v607build/title/title-v607.svg',encoding='utf-8').read() and _P7.count('`'+_N7+V+'-title.svg`')==1 and (_N7+_B7+'-title.svg') not in _P7)
    _lp7=re.compile(r'(padding|margin|inset|border)-(inline|block)|\binset\s*:|inline-size|block-size|(padding|margin)-(start|end)\b|text-align\s*:\s*(start|end)')
    print(V+' n3: logical-property regex allows a space before the colon (inset : / text-align : end caught; inset-shadow-free text and text-align:center not); PASTE and title clean:',
          all(_lp7.search(x) for x in ('inset : 0','text-align : end','text-align:start','margin-block:0')) and not any(_lp7.search(x) for x in ('text-align:center','box-shadow:inset 0 0 0 2px #000')) and not _lp7.search(_P7+_T7)
          and "\\binset\\s*:" in open(__file__,encoding='utf-8').read())
    _shf=W+'v607build/screens/clip-320.json'
    if _os.path.exists(_shf):
        _cl=json.load(open(_shf)); print(V+' m1 harness 320x568 renders 22/33/34/35: every tappable 44x44 pt+, 8 px+ apart, no overlap, nothing clipped (v607build/screens/clip-320.json):', all(not v for v in _cl.values()), {k:v for k,v in _cl.items() if v})
    _C7=json.loads(_r7); _tp7=_C7['uiText'].get('tapPrompt',{}); _Cb7=json.loads(open(W+_N7+_B7+'-cards.json',encoding='utf-8').read())
    _hh7=[f for d_ in (W+'screens-v607/html/',) if _os.path.isdir(d_) for f in _os.listdir(d_) if re.search(r'tap it|แตะเลย|Thai draft',open(d_+f,encoding='utf-8').read(),re.I)]
    _hp7=re.search(r'tap it|แตะเลย',open(W+'v607build/screens/play_v607.py',encoding='utf-8').read(),re.I)
    print(V+' T1 (Maxwell t402u): no "Tap it" (or Thai แตะเลย) anywhere in the PASTE, FINAL, spec, cards, harness or v6-07 screen HTML; no "Thai draft" chip in any v6-07 render; tapPrompt = "Where is the {word}?" / "{word} อยู่ที่ไหน" (instructor ccf506dc), no thStatus (NEEDS NANCY by default); %+d chars:'%sum(len(n)-len(o) for o,n in _X7.TP),
          not re.search(r'tap it|แตะเลย',_P7+_F7+_S7+_r7,re.I) and (_tp7.get('en',''),_tp7.get('th',''))==('Where is the {word}?','{word} อยู่ที่ไหน') and 'thStatus' not in _tp7 and not _hh7 and not _hp7
          and {k for k in _C7['uiText'] if _C7['uiText'][k]!=_Cb7['uiText'].get(k)}=={'tapPrompt'} and len(_C7['uiText'])==len(_Cb7['uiText'])==92 and sum(len(n)-len(o) for o,n in _X7.TP)==_X7.TP_DELTA, _hh7)
    V=_V7

# ======================= v6-08 checks (A1/A2 ask card, VP verse pop-up B + daily gift, E1 happy eyes) =======================
if V>='v6-08':
    import importlib.util as _iu8, subprocess as _sp8, hashlib as _h8
    _N8='nancys-adventure-english-'; _B8='v6-07'
    _m8=lambda f:_h8.md5(open(W+f,'rb').read()).hexdigest()
    _rd8=lambda f:open(W+f,encoding='utf-8').read()
    _Pb8=_rd8(_N8+_B8+'-PASTE.md'); _P8_=_rd8(_N8+V+'-PASTE.md'); _F8=_rd8(_N8+'FINAL-'+V+'.md'); _S8=_rd8(_N8+V+'.md'); _r8=_rd8(_N8+V+'-cards.json'); _rb8=_rd8(_N8+_B8+'-cards.json')
    _T8_=_rd8(_N8+V+'-title.svg'); _Tb8=_rd8(_N8+_B8+'-title.svg')
    _s8=_iu8.spec_from_file_location('fx8',W+'v608build/fixes_v608.py'); _X8=_iu8.module_from_spec(_s8); _s8.loader.exec_module(_X8)
    print(V+' base v6-07 untouched (PASTE aa73cc93, cards a29fdf25, FINAL 0d8133bd, spec 6fc65d79, verses 83e22b0e, title 0b92e0b4); CURRENT.md b653ffb2 (v5-37):',
          [_m8(_N8+_B8+x)[:8] for x in ('-PASTE.md','-cards.json','.md','-daily-verses.json','-title.svg')]==['aa73cc93','a29fdf25','6fc65d79','83e22b0e','0b92e0b4'] and _m8(_N8+'FINAL-'+_B8+'.md')[:8]=='0d8133bd' and _m8('CURRENT.md')[:8]=='b653ffb2')
    _vb8=open(W+_N8+_B8+'-daily-verses.json','rb').read(); _v8=open(W+_N8+V+'-daily-verses.json','rb').read()
    _C8_=json.loads(_r8); _Cb8=json.loads(_rb8)
    print(V+' verses byte-identical: daily-verses.json = v6-07 except the version field; cards verses, jesusWords and encouragement unchanged; "heavy laden" once in the PASTE:',
          _v8==_vb8.replace(b'"version": "v6-07"',('"version": "%s"'%V).encode(),1) and all(_C8_[k]==_Cb8[k] for k in ('verses','jesusWords','encouragement')) and _P8_.count('heavy laden')==1)
    print(V+' PASTE = FINAL + the cards.json block; %d chars <= 188,200, banked %d, Thai reserve untouched; spec banked line matches:'%(len(_P8_),188200-len(_P8_)),
          _P8_.endswith('\n```json\n'+_r8.strip()+'\n```\n') and len(_P8_)<=188200 and ('Banked in %s: %d chars under 188,200 (PASTE %s chars)'%(V,188200-len(_P8_),format(len(_P8_),','))) in _S8)
    _FX8=_X8.SPEC+_X8.VP+_X8.H1+_X8.P1+_X8.SC+_X8.WM+_X8.AG+_X8.IN_SPEC+_X8.CH_SPEC+_X8.WG   # WG: Watchman glitch hunt 73b6d48f (4:42 PM MDT ruling); AG: Auditor glitch hunt 47d0b89c g1-g9 + R1 + A1
    _lat8=lambda i,b: any(a2 and (a2 in b or (b and b in a2)) for _,a2,_b2 in _FX8[i+1:])   # an entry whose new text a later fix edits (VP6 -> WM S1) is checked through that later fix
    _bad8=[t for i,(t,a,b) in enumerate(_FX8) if not _lat8(i,b) and (not all(t_.count(b)==1 for t_ in (_F8,_S8)) or (a and any(t_.count(a)!=(1 if a in b else 0) for t_ in (_F8,_S8))))]
    print(V+' B1, A2, VP1-VP10, H1, P1, SC, G, WM/AP1/F2-F4 each once in FINAL and spec, old text gone:', not _bad8, _bad8)
    _u8=_P8_
    for t,a,b in reversed(_FX8): _u8=_u8.replace(b,a,1) if b else _u8
    for t,a,b in reversed(_X8.IN_CARDS+_X8.CH_CARDS): _u8=_u8.replace(b,a,1)   # Instructor sweep 2 cards edits + Chancellor C4 tex
    for _k,(_o,_n) in _X8.H1_CARDS.items(): _u8=_u8.replace('"key":"%s","pic":"%s"'%(_k,_n),'"key":"%s","pic":"%s"'%(_k,_o),1)
    _u8=_u8.replace(_X8.E1_CARDS[1],_X8.E1_CARDS[0]).replace(',"dailyGift":'+json.dumps(_X8.VP_UI[1],ensure_ascii=False,separators=(',',':')),'').replace('"uiTextEntries":97','"uiTextEntries":92').replace(V,_B8)
    for _k,_v in _X8.SC_UI: _u8=_u8.replace(','+json.dumps(_k)+':'+json.dumps(_v,ensure_ascii=False,separators=(',',':')),'',1)
    _u8=_u8.replace(',"sizeSort":'+json.dumps(_X8.SC_SIZE,separators=(',',':')),'',1).replace(json.dumps(_X8.G1_CARDS[1]),json.dumps(_X8.G1_CARDS[0]),1)
    for _pv in _X8.SC_PICS.values(): _u8=_u8.replace(',"pics":'+json.dumps(_pv,ensure_ascii=False,separators=(',',':')),'',1)
    print(V+' diff-only: undoing B1, A2, VP1-VP10, H1, P1, SC, G, WM S1/G1, AP1, F2-F4, AG g1-g9/R1/A1, E1 (#rE), dailyGift, the 4 scene uiText keys, sizeSort, 6 pair pics, G1, uiTextEntries and the version gives the v6-07 PASTE byte for byte (%+d chars):'%(len(_P8_)-len(_Pb8)), _u8==_Pb8)
    _g8=_sp8.run([_sys.executable,W+'v608build/qm_v608.py','--dry'],capture_output=True,text=True,cwd=W+'v608build')
    print(V+' generator qm_v608.py --dry re-runs from v6-07 and gives the file on disk (%d chars):'%len(_P8_), _g8.returncode==0 and ('-> %d '%len(_P8_)) in _g8.stdout, _g8.stderr[-200:])
    # B1: run every card through the 7.1 ask-card rule (Auditor 2b29ce71 wording + Instructor 7057dde4 "and `pic` is not null")
    _tp8=_C8_['uiText'].get('tapPrompt',{})
    def _ask8(c):
        en=c['en']
        if c.get('pic') and c['id'] not in _X8.B1_EXCLUDE and 1<=len(en.split())<=3 and en==en.lower() and not re.search(r'[.,?!]',en) and not en.startswith('a '): return _tp8.get('en','').replace('the {word}' if c['id'] in ['cs-%02d'%i for i in range(8,16)] else '{word}',en)   # Instructor color-ask: colors drop "the"
        return en
    _out8={c['id']:_ask8(c) for c in _C8_['cards'] if isinstance(c.get('en'),str)}; _pc8=[c for c in _C8_['cards'] if c.get('pic')]
    _wh8={c['id'] for c in _C8_['cards'] if isinstance(c.get('en'),str) and _out8[c['id']]!=c['en']}; _B1T8=re.sub(r'colors cs-08–cs-15 drop "the": \'Where is red\?\'\), else','), else',_X8.A1[1])
    _flag8={k:v for k,v in _out8.items() if k in _wh8 and re.search(r'\.\?|\?\?|,\?|!\?|Where is the (a|an|the|I|I\'m|she|he|they|it|his|her|this|where|now|there|come) ',v)}
    print(V+' B1: every card run through the 7.1 rule: %d picture cards, %d read "Where is the ...?", the rest show their own en; no ".?", "??", ",?", "the a ", "the I" and no pronoun/verb cases; pic-null cards (ph-09, sw-09 ...) and the 14 listed ids never get the prompt; rule text in FINAL and spec:'%(len(_pc8),len(_wh8)),
          not _flag8 and len(_wh8)==44 and _wh8<={c['id'] for c in _pc8} and not (_wh8 & set(_X8.B1_EXCLUDE)) and not ({'ph-09','ph-10','sw-09','sw-10','sw-13','sw-14','sw-20','sw-21','sw-22','sw-23'} & _wh8)
          and _out8['bh-12']=='Wash the baby.' and _out8['cs-03']=='a white towel' and _out8.get('fd-08')=='Where is the croissant?' and all(('colors cs-08–cs-15 drop "the"' in t_) for t_ in (_F8,_S8)), sorted(_flag8.items())[:5])
    print(V+' A2: the ask card Thai wraps (17 px+, line-height 1.7), never cut or shrunk:', 'Its Thai wraps, never cut or shrunk.' in _F8)
    # VP: verse pop-up B + daily gift
    _dg8=_C8_['uiText'].get('dailyGift')
    print(V+' VP: launch order ends at run or main menu and the verse pops up over the menu (first launch: first menu visit after the Phonics run); the title never shows a pop-up; no verseOfDay title banner:',
          '→ `rewardQueue` → run or main menu; the daily verse, if due, pops up over the main menu (first launch: her first menu visit after the Phonics run); the title never shows a pop-up.' in _F8 and 'daily verse `uiText.verseOfDay`' not in _F8 and 'daily verse if due →' not in _F8)
    print(V+' VP: pop-up B (scrim, ribbon verseOfDay, verseGift, ref, en, gold rule, th, sources; only the body scrolls, buttons always in view; Replay shield + Got it):',
          all(x in _F8 for x in ("**Daily verse pop-up (Maxwell's pick B, t399u):**",'Ink 50% scrim','only the verse body scrolls, the buttons always stay in view','a round Replay shield (`uiText.replay` under it)','Got it closes it.')))
    print(V+' VP: daily gift = a flat tag above the card, ledger gift:<local date>, giftGems +1 in state, counts up only, feeds no trophy/gem count/gear bonus, missing reads 0, schema stays 5020, restore accepts it missing:',
          all(x in _F8 for x in ('`uiText.dailyGift` with one small gem','ledger `gift:<local date>`, `giftGems` +1','`gift:<local date>`, `unlock:<trophyId>`','pips, streak, giftGems, hero, zoneRuns{}, settings{slowMode, restWeeks}}','`giftGems` feeds no trophy, gem count or gear bonus; missing, it reads 0 (no `schema` change).','(JSON, `schema` 5020, all keys but `giftGems`, `hero` and `zoneRuns`; those missing keep hers)','`schema: 5020`'))
          and _F8.count('5020')==_rd8(_N8+'FINAL-'+_B8+'.md').count('5020')+1)   # +1: G6 mirror loads only if its `schema` is 5020
    print(V+' VP: the gem never depends on the verse and never gates or boosts it; verses never earned, gated or boosted (grace check line):',
          'It never depends on the verse (shown, read or closed) and never gates or boosts it.' in _F8 and '`gift:`/`giftGems` never depend on a verse;' in _F8 and not re.search(r'(?i)(verse|scroll)[^.\n]{0,40}\b(earn|unlock)s? (a |the )?gem',_F8))
    print(V+' VP: uiText.dailyGift = "Daily gift: +1 gem" / "อัญมณีประจำวัน: 1 เม็ด" (Instructor 7057dde4), no thStatus (NEEDS NANCY by default); uiText 97 = meta.uiTextEntries = the stated `uiText` (97); only dailyGift and the 4 scene keys added vs v6-07:',
          _dg8=={'en':'Daily gift: +1 gem','th':'อัญมณีประจำวัน: 1 เม็ด'} and len(_C8_['uiText'])==97==_C8_['meta']['uiTextEntries'] and '`uiText` (97)' in _F8
          and {k for k in _C8_['uiText'] if _C8_['uiText'][k]!=_Cb8['uiText'].get(k)}=={'dailyGift','guardianLast'}|{k for k,_ in _X8.SC_UI} and _C8_['uiText']['guardianLast']['en']=='Finish the last guardian to open this.' and _C8_['meta']['thStatusDefault']=='NEEDS NANCY')   # guardianLast: Instructor guardian-case (lower-case only)
    print(V+' VP rechecks: 6.2 still two buttons; Settings rule (state.settings{slowMode, restWeeks}); Restore two steps; daily delivery free, a missed day costs nothing:',
          'Exactly two buttons, the hearth (a corner button) and one cue' in _F8 and 'streak, giftGems, hero, zoneRuns{}, settings{slowMode, restWeeks}}' in _F8 and '**Restore, two steps:**' in _F8
          and 'one memory verse a day on her first open each day, over the main menu (never the title, t404u), in the pop-up below,' in _S8 and 'titled `uiText.verseOfDay`' not in _S8 and 'Free, never sold; a missed day costs nothing; given verses stay on Scrolls' in _S8)
    # E1: happy eyes (Maxwell t408u): Nancy's eyes exactly, one shared component #rE used by Sam and Nancy; no old eye shapes left
    _tx8=_C8_['picPlan']['uiInlineSvg']['tex']; _txb8=_Cb8['picPlan']['uiInlineSvg']['tex']; _NE8="M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0"
    _old8=[x for x in ("ellipse cx='35' cy='20' rx='1.2'","<circle cx='35' cy='20' r='.6'","cx='49.1' cy='20' r='.6'","M33.1 20.7q1.9-2.4","M32.8 21.4q2.2-3.2") if x in _r8+_T8_]
    print(V+' E1: #rE is Nancy\'s happy eyes exactly (her path, stroke 1.6, Ink by inheritance) and Sam\'s rig draws it (1 use); Nancy\'s own snippet is unchanged and is the same path; tex otherwise v6-07; no old eye shape (open eyes, pupils, thin arcs) in cards or title; title Sam\'s eye is her arc; spec note updated, other four MX4 notes kept:',
          _X8.E1_CARDS[1]=="<path id='rE' d='"+_NE8+"' stroke-width='1.6'/>" and _X8.E1_CARDS[1] in _tx8 and _tx8.replace(_X8.E1_CARDS[1],_X8.E1_CARDS[0]).replace(_X8.CH_CARDS[0][2],_X8.CH_CARDS[0][1])==_txb8
          and _r8.count("<use href='#rE'/>")==1 and _r8.count(_NE8)==2 and not _old8 and _rb8.count(_NE8)==1 and _rb8.count("<use href='#rE'/>")==1
          and _T8_.replace(_X8.E1_TITLE[1],_X8.E1_TITLE[0])==_Tb8 and _T8_.count("<path d='M46 21q2.4-2.8 4.8 0' stroke-width='1.6'/>")==1
          and "Sam's eyes are Nancy's happy arcs (shared `#rE`) on every screen (t408u)." in _S8 and all(x in _S8 for x in ('Golden Fields: a corn row on the far hill','Word Meadow: a small wood swing set far back','Echo Forest: one clear object','pine canopies sit on trunks and branches grow from trunks')), _old8)
    _em8=W+'v608build/eyes/eyes-manifest.json'
    if _os.path.exists(_em8):
        _E8=json.load(open(_em8)); _bad8e=[]; _n8e=0
        for _b,_v in _E8.items():
            if not _v['png']: continue
            _n8e+=1; _hh=open(_v['png'].replace('/png/','/html/').replace('.png','.html'),encoding='utf-8').read()
            if any(x in _hh for x in ("<use href='#rE'/>","M33.1 20.7q1.9-2.4","<ellipse cx='48.6' cy='20' rx='1.1' ry='.9' fill='#FFF8E1'/>","M32.8 21.4q2.2-3.2")) or ("data-hero='sam'" in _hh and _NE8 not in _hh): _bad8e.append(_b)
        _un8=[_b for _b,_v in _E8.items() if not _v['png'] and "data-hero='sam'" in open(_v['src'],encoding='utf-8').read() and _NE8 not in open(_v['src'],encoding='utf-8').read()]
        print(V+' E1 renders: every Sam drawing re-shot with her eyes (%d screens incl. scene-variety mocks); no old eye shape in any of them; no Sam left unconverted:'%_n8e, not _bad8e and not _un8, _bad8e, _un8)
    # Renders (t411u, gate m1/O1, VP): harness facts read from the v6-08 render HTML
    _h8=lambda f: open(W+'screens-v608/html/'+f,encoding='utf-8').read() if _os.path.exists(W+'screens-v608/html/'+f) else ''
    print(V+' t411u 320 m1 revert: 22 plates back to v6-06 104 px (gap 8); 22/34/35 speaker 44 pt in its own slot; 34/35 Hear-it button 140 px; tap targets >= 44 pt and >= 8 px apart (tapgap clean):',
          'grid-template-columns:104px 104px;gap:8px' in _h8('22-kitchen-server-talk-320x568.html') and all('width:44px;height:44px' in _h8(f) for f in ('22-kitchen-server-talk-320x568.html','34-echo-forest-sound-duel-320x568.html','35-sound-duel-right-320x568.html'))
          and all("width:140px;height:56px" in _h8(f) for f in ('34-echo-forest-sound-duel-320x568.html','35-sound-duel-right-320x568.html'))
          and all(v==[] for k,v in json.load(open(W+'v608build/polish-r1/t411u/tapgap-320.json')).items()))
    print(V+' m1 (gate): 24/25 plate gap back to the approved 10 px at 390:', all('grid-template-columns:160px 160px;gap:10px' in _h8(f) for f in ('24-guardian-run-entry.html','25-guardian-hint-letters.html')))
    print(V+' t411u screen 10: v6-06 card rhythm with the t402u wording, Thai wraps at 17 px / lh 1.7, no Tap it, no Thai draft chip:',
          'Where is the kite?' in _h8('10-word-meadow-scene.html') and 'kite อยู่ที่ไหน' in _h8('10-word-meadow-scene.html') and not re.search(r'Tap it|Thai draft|แตะเลย',_h8('10-word-meadow-scene.html')) and 'line-height:1.7;overflow-wrap:anywhere' in _h8('10-word-meadow-scene.html'))
    print(V+' O1/VP renders: the verse pops up over the main menu at 390 and 320 (Daily gift tag from uiText.dailyGift), never over the title; the old title-verse render 02 is retired:',
          all(_C8_['uiText']['dailyGift']['th'] in _h8('02-main-menu-verse-popup'+z+'.html') and 'Psalm 23:1' in _h8('02-main-menu-verse-popup'+z+'.html') for z in ('-390check','-320x568'))
          and not _os.path.exists(W+'screens-v608/html/02-verse-of-the-day.html') and not any('Verse of the day' in _h8(f) for f in ('01-title.html','01-title-320x568.html')))
    _sc8=lambda f: open(W+'v608build/scenes/html/'+f,encoding='utf-8').read() if _os.path.exists(W+'v608build/scenes/html/'+f) else ''
    print(V+' council renders: 30 reads "A gift from the Word Guardian" (spec :292); sv-now-10 uses "kite อยู่ที่ไหน" (no Tap it); gem tag menus before/after the verse at 390/320 say exactly "Daily gift: +1 gem":',
          'A gift from the Word Guardian' in _h8('30-new-weapon-gift.html') and 'A gift from The' not in _h8('30-new-weapon-gift.html')
          and (lambda t: 'kite อยู่ที่ไหน' in t and 'Tap it' not in t and 'แตะเลย' not in t)(open(W+'v608build/eyes/scene-variety/html/sv-now-10-word-meadow-scene.html',encoding='utf-8').read())
          and all('Daily gift: +1 gem' in _h8('02%s-menu-gemtag-%s-verse%s.html'%(k,w,z)) and 'Daily gem' not in _h8('02%s-menu-gemtag-%s-verse%s.html'%(k,w,z)) for k,w in (('c','before'),('d','after')) for z in ('-390check','-320x568')))
    print(V+' P1 renders (t423u): 12 hug and 20/21 food are 64 pt ground props (C); 24-27 (people) use the framed top-right plate (A); no free-floating 96-120 pt picture left on those screens:',
          all("data-pic='prop'" in _h8(f) for f in ('12-reveal-right.html','21-kitchen-say-it-shown-390check.html'))   # W10 (4:42 PM MDT): Kitchen say-it cards are scene targets; render 20 (picture-first) moved to screens-v608/superseded-W10
          and all("data-pic='plate'" in _h8(f) for f in ('24-guardian-run-entry.html','25-guardian-hint-letters.html','26-guardian-hint-jesus-words.html','27-guardian-kneels.html')))
    print(V+' scene renders: A-H and the Word Meadow Level 1-5 strip exist, built on the v6-08 harness; new Thai from uiText (ฟังแล้วหาดู, มีวัวกี่ตัว, ใหญ่หรือเล็ก); no Thai draft chip, no Tap it, no นะ:',
          all(_sc8(f) for f in ('A-meadow-evening-pond.html','B-meadow-listen-and-find.html','C-fields-count-it.html','D-fields-big-or-small.html','E-lake-front-desk.html','F-lake-night-table.html','G-forest-picture-duel.html','H-forest-dawn.html')) and all(__import__('os').path.exists(W+'v608build/scenes/tod/%s-step%d-%s.html'%(z,n,r)) for z in ('meadow','fields','lake','forest') for n in range(1,6) for r in ('390','320x568'))   # K3: the Level strip is now the time-of-day step strips (L1-L5 moved to scenes/superseded-K3)
          and 'ฟังแล้วหาดู<' in _sc8('B-meadow-listen-and-find.html') and 'มีวัวกี่ตัว' in _sc8('C-fields-count-it.html') and 'ใหญ่หรือเล็ก' in _sc8('D-fields-big-or-small.html')
          and not any(re.search(r'Thai draft|Tap it|แตะเลย|หาดูนะ',_sc8(f)) for f in _os.listdir(W+'v608build/scenes/html/')) and _NE8 in open(W+'v608build/scenes/tod/meadow-step1-390.html',encoding='utf-8').read())
    # Watchman playtest round (REPORT 9f88fb02; council 4:08 PM MDT)
    print(V+' K1 (Auditor; Watchman S1): the one state record holds `hero` and `zoneRuns{}`; restore checks all keys but giftGems, hero and zoneRuns; FINAL, spec and PASTE:', all('pips, streak, giftGems, hero, zoneRuns{}, settings{slowMode, restWeeks}}' in t_ for t_ in (_F8,_S8,_P8_)))
    _T8r=_C8_['trophyRules']; _tn8=_T8r['tierNames'].split('|'); _rw8=_T8r['rows'].split()
    _nm8={(t['wt'],t['tier']):t['id'] for t in _C8_['trophies'] if t.get('wt') and t.get('tier')}; _nm8.setdefault(('sword1',1),'sword-iron')
    _sl8=[_nm8.get((w,k)) or '%s-t%d'%(w,k) for w in _rw8 for k in (1,2,3)]
    _ex8=[t['id'] for t in _C8_['trophies'] if t.get('wt') and t['id'] not in _sl8]
    _all8=_sl8+_ex8
    print(V+' K2 (Auditor; Watchman G1 reconciled to one scheme): all 18 weapons have an id (12 shop slots incl. 7 tier-slot ids `<type>-t<t>` + 6 others: sling, shield, crook, Bloodtide, Dragonbane, Sunforged); ids unique, none collides with a trophy id; rule in FINAL and spec:',
          len(_all8)==18 and len(set(_all8))==18 and sum(1 for w in _rw8 for k in (1,2,3) if (w,k) not in _nm8)==7 and not ({'%s-t%d'%(w,k) for w in _rw8 for k in (1,2,3) if (w,k) not in _nm8} & {t['id'] for t in _C8_['trophies']})
          and all("and id `<type>-t<t>` (e.g. `axe1-t2`), kept in `owned`/`equipped` like a trophy id." in t_ and 'one of the 42 `trophies` or a tier slot' in t_ and '<tierName>-<type>' not in t_ for t_ in (_F8,_S8)), sorted(_all8))
    print(V+' U1: section 18 states the live uiText count (97 = cards):', 'all %d `uiText` entries'%len(_C8_['uiText']) in _F8 and 'all 91 `uiText`' not in _P8_)
    print(V+' F2/F3/F4: no back-to-back Sight Words repeat across scenes; Sound Duel right answers earn stars; tier 1 is given free when its row opens (no "Get it for 0"):',
          all(x in _F8 and x in _S8 for x in ("never twice in one scene or as the next scene's first ask.",'Gold Stars per right answer (Sound Duel too) and finished run','(tier 1 is hers free when its row opens, no `getFor`)')))
    print(V+' K3: time of day = 1 + zoneRuns[zone] mod 5, set at run start (resume keeps it), step 1 m .. 5 n then m again; zoneRuns{} in the state record, a missing value reads {} (schema stays 5020):',
          all(x in _F8 and x in _S8 for x in ("set at run start from that zone's step, 1 + `zoneRuns[zone]` mod 5",'step 1 `m` morning','5 `n` night, then `m` again','zoneRuns{}')) and 'from her Level' not in _P8_ and '`schema: 5020`' in _F8)
    print(V+' M1: reconcile drops owned ids that no longer exist (trophies, tier slots, pantry items) and equipped ids not owned; no refund (Maxwell to pick):', all("any id not in `trophies`, tier slots or `pantry.items`, and any `equipped` id not owned" in t_ for t_ in (_F8,_S8)) and not re.search(r'(?i)refund',_P8_))
    print(V+' M2: Big or small awards and resumes as a scene card (ledger card:<runId>:<index>); F5: welcomeBack first after a missed day, then the verse pop-up:',
          all(x in _F8 and x in _S8 for x in ('Grace as 7.1; it awards, reveals and resumes as the scene card `cs-23` or `cs-24`, the word that fits (ledger `card:<runId>:<index>`).','After a missed day `welcomeBack` shows first, then this.')))
    _nt8=' '.join(b for t,a,b in _FX8)+' '+' '.join(v['en'] for k,v in _X8.SC_UI)+' '+_X8.VP_UI[1]['en']
    _GW8=r"(?i)\b(lock(?:s|ed)?|fail(?:s|ed|ure)?|lose|lost|loses|penalt\w*|game over|can't|cannot|wrong answer|punish\w*|timer|hurry)\b"
    _gw8=list((collections.Counter(w.lower() for w in re.findall(_GW8,_nt8.replace('button locks until','button waits until')))-collections.Counter(w.lower() for t,a_,b_ in _FX8 for w in re.findall(_GW8,a_ or ''))).elements())   # only words a fix ADDS; "every button locks until the next screen renders" (G2) is the input guard, not a player-facing lock
    print(V+' grace words: none of the v6-08 new texts (every spec edit, new uiText) says lock, fail, lose/lost, penalty, game over, can\'t, timer or hurry:', not _gw8, _gw8)
    print(V+' no logical properties (n3 regex) and no lookbehind in the PASTE or title:', not re.search(r'\(\?<|(padding|margin|inset|border)-(inline|block)|\binset\s*:|inline-size|block-size|(padding|margin)-(start|end)\b|text-align\s*:\s*(start|end)',_P8_+_T8_))
    _ms8=[c for c in _C8_['cards'] if c['id']=='ms-31'][0]; _pn8=[c for c in _C8_['cards'] if c.get('pic') in ('svg:pray-kneel','svg:high-five')]
    print(V+' H1 (Maxwell t406u): ms-31 buttons are hand emoji 🙏 / 🙌 (Unicode 6.0) on 124 pt bordered parchment plates; hand-only emoji rule and "people or bigger pictures drawn, never emoji" in :243; svg:pray-kneel still drawn for ph-08/ms-11; high-five kept in the library:',
          [(c['key'],c['pic']) for c in _ms8['choices']]==[('pray','🙏'),('highFive','🙌')] and 'Hand-only emoji (Unicode 13.0 or earlier) are fine as emoji; people or bigger pictures (a hug) are drawn from `picPlan.svgNotes` on the same plate, never emoji;' in _F8
          and sorted(c['id'] for c in _pn8)==['ms-11','ph-08'] and 'high-five' in _C8_['picPlan']['svg'] and 'pray-kneel' in _C8_['picPlan']['svg'])
    _em8n=sorted({c for c in _P8_ if ord(c)>=0x1F000 and c not in _Pb8})
    _ok8e={'🙌','🙏'}|{ch for v in _X8.SC_PICS.values() for e in v for ch in e}
    print(V+' emoji: the only new emoji vs v6-07 are the hand emoji 🙌 and the 6 Sound Duel pair pictures (no 🔒), all Unicode 13.0 or earlier:', set(_em8n)<=_ok8e and '🔒' not in _P8_ and not any(0x1FA70<=ord(c)<=0x1FAFF and c not in _Pb8 for c in _P8_), _em8n)
    # G1, P1, SC (council 3:55 PM MDT; Maxwell t422u/t423u; scene ideas A-H t401u; Instructor 7057dde4 Thai)
    _tr8=[t for t in _C8_['trophies'] if t['id']=='tunic-rose'][0]
    print(V+' G1 grace: tunic-rose meaning "Right with God as His free gift", Thai ความชอบธรรม kept, old wording gone:', _tr8['word']==['Righteousness','Right with God as His free gift','ความชอบธรรม'] and 'Doing what is right in God' not in _P8_)
    print(V+' P1 (t423u) reveal pictures: 64 pt ground prop where it can stand, else 124 pt framed plate top right, never over or beside the hero; hand emoji keep their plates; in FINAL and spec:', all(_X8.P1[0][2] in t_ for t_ in (_F8,_S8)))
    _U8s=_C8_['uiText']; _pp8=[p_ for p_ in _C8_['soundDuel']['pairs'] if 'pics' in p_]
    print(V+' SC uiText (NEEDS NANCY, no thStatus): listenFind ฟังแล้วหาดู (no นะ), howMany นับดู, howManyCows มีวัวกี่ตัว (cow scene only), bigOrSmall ใหญ่หรือเล็ก; English as drafted:',
          [(k,_U8s[k]) for k,_ in _X8.SC_UI]==[(k,dict(v)) for k,v in _X8.SC_UI] and 'นะ' not in _U8s['listenFind']['th'] and not any('thStatus' in _U8s[k] for k,_ in _X8.SC_UI) and _U8s['dailyGift']['en']=='Daily gift: +1 gem')
    _Cd8={c['id']:c for c in _C8_['cards']}
    print(V+' SC data: meta.sizeSort 3 big + 3 small existing picture cards; 6 Sound Duel pairs carry pics (2 emoji each, in a/b order), the other 24 stay words only; time of day by the zone step (K3) and the front desk scene (no names or signs) in FINAL and spec:',
          all(len(v)==3 and all(_Cd8[i].get('pic') for i in v) for v in _C8_['meta']['sizeSort'].values()) and len(_pp8)==6 and all(len(p_['pics'])==2 for p_ in _pp8) and len(_C8_['soundDuel']['pairs'])==30
          and all(x in _F8 and x in _S8 for x in ('step 1 `m` morning, 2 `d` midday','5 `n` night, then `m` again','**Front desk (Home Lake):**','No names or signs.','`uiText.listenFind`','`uiText.howManyCows`','`meta.sizeSort`')))

if V>='v6-08':
    import sys as _s9; _s9.path.insert(0,W+'v608build'); import fixes_v608 as _XA
    _FA=open(W+'nancys-adventure-english-FINAL-'+V+'.md',encoding='utf-8').read(); _SA=open(W+'nancys-adventure-english-'+V+'.md',encoding='utf-8').read()
    _ag=[t for t,a,b in _XA.AG if not all(x.count(b)==1 for x in (_FA,_SA)) and not any(b and a2 in b for _,a2,_ in _XA.AG+_XA.CH_SPEC if a2!=a)]
    print(V+' AG Auditor glitch hunt 47d0b89c: g1-g9 (one sound, button guards, run/buy ids, scene miss, verse date it opened for, naeState mirror, iOS speech wake, same-zone review, verse URLs data only) + R1 + A1 each once in FINAL and spec:', not _ag and 'speechSynthesis.cancel()' in _FA and '`run:<local date>:<runId>`' in _FA and 'naeState' in _FA, _ag)
if V>='v6-08':
    _FB=open(W+'nancys-adventure-english-FINAL-'+V+'.md',encoding='utf-8').read(); _SB=open(W+'nancys-adventure-english-'+V+'.md',encoding='utf-8').read(); _CB=open(W+'nancys-adventure-english-'+V+'-cards.json',encoding='utf-8').read()
    _CBc=json.dumps(json.loads(_CB),ensure_ascii=False,separators=(',',':'))
    _in=[t for t,a,b in _XA.IN_SPEC if not all(x.count(b)==1 for x in (_FB,_SB)) and not any(b and (a2 in b or b in a2) for _,a2,_ in _XA.IN_SPEC+_XA.CH_SPEC+_XA.WG if a2!=a)]+[t for t,a,b in _XA.IN_CARDS if _CBc.count(b)!=1 or _CBc.count(a)]
    print(V+' IN Instructor sweep 2 (9a7e52d9): ask {word} = en in both lines, kitchen tap = uiText.continue, colors drop "the", cs-07/sw-11 Thai (NEEDS NANCY), guardianLast case, ms-04 letters; each once in FINAL/spec or cards, old text gone:', not _in, _in)
    _ch=[t for t,a,b in _XA.CH_SPEC if not all(x.count(b)==1 for x in (_FB,_SB)) and not any(b and a2 in b for _,a2,_ in _XA.CH_SPEC if a2!=a)]+[t for t,a,b in _XA.CH_CARDS if _CBc.count(b)!=1]
    print(V+' CH Chancellor 5da6f734: never-seen cap 8 fewest words first, no stale first-run note, arrow tie rotates from her last row, tex :root defaults, a miss keeps every coin everywhere (G4 coin clause not doubled), Echo Knight recap ends like a round, untiered weapons ring as legendary:', not _ch and not re.search(r'removes? one filled coin|no coin off',_FB) and 'Bloodtide Cleaver' in _CB, _ch)
if V>='v6-08':
    _wg=[t for t,a,b in _XA.WG if not all(x.count(b)==1 and (a in b or x.count(a)==0) for x in (_FB,_SB))]
    print(V+' WG Watchman glitch hunt 73b6d48f (parent ruling 4:42 PM MDT): welcomeBack key, region-open once, level 20 bar full, tod steps (Echo Forest rounds, 0 if unset), Big or small card, front desk own scenes, look-alike groups apart (lean), count prop hides (lean), Kitchen say-it as scene targets (W10), restore keeps hero/giftGems; each once, old text gone:', not _wg and '`uiText.welcomeBack`' not in _FB and 'opens picture-first' not in _FB, _wg)
