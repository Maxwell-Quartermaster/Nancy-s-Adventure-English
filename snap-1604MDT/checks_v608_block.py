
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
    _FX8=_X8.SPEC+_X8.VP+_X8.H1+_X8.P1+_X8.SC
    _bad8=[t for t,a,b in _FX8 if not all(t_.count(b)==1 for t_ in (_F8,_S8)) or (a and any(t_.count(a)!=(1 if a in b else 0) for t_ in (_F8,_S8)))]
    print(V+' B1, A2, VP1-VP10, H1, P1, SC, G each once in FINAL and spec, old text gone:', not _bad8, _bad8)
    _u8=_P8_
    for t,a,b in reversed(_FX8): _u8=_u8.replace(b,a,1) if b else _u8
    for _k,(_o,_n) in _X8.H1_CARDS.items(): _u8=_u8.replace('"key":"%s","pic":"%s"'%(_k,_n),'"key":"%s","pic":"%s"'%(_k,_o),1)
    _u8=_u8.replace(_X8.E1_CARDS[1],_X8.E1_CARDS[0]).replace(',"dailyGift":'+json.dumps(_X8.VP_UI[1],ensure_ascii=False,separators=(',',':')),'').replace('"uiTextEntries":97','"uiTextEntries":92').replace(V,_B8)
    for _k,_v in _X8.SC_UI: _u8=_u8.replace(','+json.dumps(_k)+':'+json.dumps(_v,ensure_ascii=False,separators=(',',':')),'',1)
    _u8=_u8.replace(',"sizeSort":'+json.dumps(_X8.SC_SIZE,separators=(',',':')),'',1).replace(json.dumps(_X8.G1_CARDS[1]),json.dumps(_X8.G1_CARDS[0]),1)
    for _pv in _X8.SC_PICS.values(): _u8=_u8.replace(',"pics":'+json.dumps(_pv,ensure_ascii=False,separators=(',',':')),'',1)
    print(V+' diff-only: undoing B1, A2, VP1-VP10, H1, P1, SC, G, E1 (#rE), dailyGift, the 4 scene uiText keys, sizeSort, 6 pair pics, G1, uiTextEntries and the version gives the v6-07 PASTE byte for byte (%+d chars):'%(len(_P8_)-len(_Pb8)), _u8==_Pb8)
    _g8=_sp8.run([_sys.executable,W+'v608build/qm_v608.py','--dry'],capture_output=True,text=True,cwd=W+'v608build')
    print(V+' generator qm_v608.py --dry re-runs from v6-07 and gives the file on disk (%d chars):'%len(_P8_), _g8.returncode==0 and ('-> %d '%len(_P8_)) in _g8.stdout, _g8.stderr[-200:])
    # B1: run every card through the 7.1 ask-card rule (Auditor 2b29ce71 wording + Instructor 7057dde4 "and `pic` is not null")
    _tp8=_C8_['uiText'].get('tapPrompt',{})
    def _ask8(c):
        en=c['en']
        if c.get('pic') and c['id'] not in _X8.B1_EXCLUDE and 1<=len(en.split())<=3 and en==en.lower() and not re.search(r'[.,?!]',en) and not en.startswith('a '): return _tp8.get('en','').replace('{word}',en)
        return en
    _out8={c['id']:_ask8(c) for c in _C8_['cards'] if isinstance(c.get('en'),str)}; _pc8=[c for c in _C8_['cards'] if c.get('pic')]
    _wh8={c['id'] for c in _C8_['cards'] if isinstance(c.get('en'),str) and _out8[c['id']]!=c['en']}
    _flag8={k:v for k,v in _out8.items() if k in _wh8 and re.search(r'\.\?|\?\?|,\?|!\?|Where is the (a|an|the|I|I\'m|she|he|they|it|his|her|this|where|now|there|come) ',v)}
    print(V+' B1: every card run through the 7.1 rule: %d picture cards, %d read "Where is the ...?", the rest show their own en; no ".?", "??", ",?", "the a ", "the I" and no pronoun/verb cases; pic-null cards (ph-09, sw-09 ...) and the 14 listed ids never get the prompt; rule text in FINAL and spec:'%(len(_pc8),len(_wh8)),
          not _flag8 and len(_wh8)==44 and _wh8<={c['id'] for c in _pc8} and not (_wh8 & set(_X8.B1_EXCLUDE)) and not ({'ph-09','ph-10','sw-09','sw-10','sw-13','sw-14','sw-20','sw-21','sw-22','sw-23'} & _wh8)
          and _out8['bh-12']=='Wash the baby.' and _out8['cs-03']=='a white towel' and _out8.get('fd-08')=='Where is the croissant?' and _X8.A1[1] in _F8 and _X8.A1[1] in _S8, sorted(_flag8.items())[:5])
    print(V+' A2: the ask card Thai wraps (17 px+, line-height 1.7), never cut or shrunk:', 'Its Thai wraps, never cut or shrunk.' in _F8)
    # VP: verse pop-up B + daily gift
    _dg8=_C8_['uiText'].get('dailyGift')
    print(V+' VP: launch order ends at run or main menu and the verse pops up over the menu (first launch: first menu visit after the Phonics run); the title never shows a pop-up; no verseOfDay title banner:',
          '→ `rewardQueue` → run or main menu; the daily verse, if due, pops up over the main menu (first launch: her first menu visit after the Phonics run); the title never shows a pop-up.' in _F8 and 'daily verse `uiText.verseOfDay`' not in _F8 and 'daily verse if due →' not in _F8)
    print(V+' VP: pop-up B (scrim, ribbon verseOfDay, verseGift, ref, en, gold rule, th, sources; only the body scrolls, buttons always in view; Replay shield + Got it):',
          all(x in _F8 for x in ("**Daily verse pop-up (Maxwell's pick B, t399u):**",'Ink 50% scrim','only the verse body scrolls, the buttons always stay in view','a round Replay shield (`uiText.replay` under it)','Got it closes it.')))
    print(V+' VP: daily gift = a flat tag above the card, ledger gift:<local date>, giftGems +1 in state, counts up only, feeds no trophy/gem count/gear bonus, missing reads 0, schema stays 5020, restore accepts it missing:',
          all(x in _F8 for x in ('`uiText.dailyGift` with one small gem','ledger `gift:<local date>`, `giftGems` +1','`gift:<local date>`, `unlock:<trophyId>`','pips, streak, giftGems, settings{slowMode, restWeeks}}','`giftGems` feeds no trophy, gem count or gear bonus; missing, it reads 0 (no `schema` change).','(JSON, `schema` 5020, all keys but `giftGems`)','`schema: 5020`'))
          and _F8.count('5020')==_rd8(_N8+'FINAL-'+_B8+'.md').count('5020'))
    print(V+' VP: the gem never depends on the verse and never gates or boosts it; verses never earned, gated or boosted (grace check line):',
          'It never depends on the verse (shown, read or closed) and never gates or boosts it.' in _F8 and '`gift:`/`giftGems` never depend on a verse;' in _F8 and not re.search(r'(?i)(verse|scroll)[^.\n]{0,40}\b(earn|unlock)s? (a |the )?gem',_F8))
    print(V+' VP: uiText.dailyGift = "Daily gift: +1 gem" / "อัญมณีประจำวัน: 1 เม็ด" (Instructor 7057dde4), no thStatus (NEEDS NANCY by default); uiText 97 = meta.uiTextEntries = the stated `uiText` (97); only dailyGift and the 4 scene keys added vs v6-07:',
          _dg8=={'en':'Daily gift: +1 gem','th':'อัญมณีประจำวัน: 1 เม็ด'} and len(_C8_['uiText'])==97==_C8_['meta']['uiTextEntries'] and '`uiText` (97)' in _F8
          and {k for k in _C8_['uiText'] if _C8_['uiText'][k]!=_Cb8['uiText'].get(k)}=={'dailyGift'}|{k for k,_ in _X8.SC_UI} and _C8_['meta']['thStatusDefault']=='NEEDS NANCY')
    print(V+' VP rechecks: 6.2 still two buttons; Settings rule (state.settings{slowMode, restWeeks}); Restore two steps; daily delivery free, a missed day costs nothing:',
          'Exactly two buttons, the hearth (a corner button) and one cue' in _F8 and 'streak, giftGems, settings{slowMode, restWeeks}}' in _F8 and '**Restore, two steps:**' in _F8
          and 'one memory verse a day on her first open each day, over the main menu (never the title, t404u), in the pop-up below,' in _S8 and 'titled `uiText.verseOfDay`' not in _S8 and 'Free, never sold; a missed day costs nothing; given verses stay on Scrolls' in _S8)
    # E1: happy eyes (Maxwell t408u): Nancy's eyes exactly, one shared component #rE used by Sam and Nancy; no old eye shapes left
    _tx8=_C8_['picPlan']['uiInlineSvg']['tex']; _txb8=_Cb8['picPlan']['uiInlineSvg']['tex']; _NE8="M32.6 21q2.4-2.8 4.8 0M42.6 21q2.4-2.8 4.8 0"
    _old8=[x for x in ("ellipse cx='35' cy='20' rx='1.2'","<circle cx='35' cy='20' r='.6'","cx='49.1' cy='20' r='.6'","M33.1 20.7q1.9-2.4","M32.8 21.4q2.2-3.2") if x in _r8+_T8_]
    print(V+' E1: #rE is Nancy\'s happy eyes exactly (her path, stroke 1.6, Ink by inheritance) and Sam\'s rig draws it (1 use); Nancy\'s own snippet is unchanged and is the same path; tex otherwise v6-07; no old eye shape (open eyes, pupils, thin arcs) in cards or title; title Sam\'s eye is her arc; spec note updated, other four MX4 notes kept:',
          _X8.E1_CARDS[1]=="<path id='rE' d='"+_NE8+"' stroke-width='1.6'/>" and _X8.E1_CARDS[1] in _tx8 and _tx8.replace(_X8.E1_CARDS[1],_X8.E1_CARDS[0])==_txb8
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
          all("data-pic='prop'" in _h8(f) for f in ('12-reveal-right.html','20-kitchen-say-it-picture-first-390check.html','21-kitchen-say-it-shown-390check.html'))
          and all("data-pic='plate'" in _h8(f) for f in ('24-guardian-run-entry.html','25-guardian-hint-letters.html','26-guardian-hint-jesus-words.html','27-guardian-kneels.html')))
    print(V+' scene renders: A-H and the Word Meadow Level 1-5 strip exist, built on the v6-08 harness; new Thai from uiText (ฟังแล้วหาดู, มีวัวกี่ตัว, ใหญ่หรือเล็ก); no Thai draft chip, no Tap it, no นะ:',
          all(_sc8(f) for f in ('A-meadow-evening-pond.html','B-meadow-listen-and-find.html','C-fields-count-it.html','D-fields-big-or-small.html','E-lake-front-desk.html','F-lake-night-table.html','G-forest-picture-duel.html','H-forest-dawn.html','L1-meadow.html','L5-meadow.html'))
          and 'ฟังแล้วหาดู<' in _sc8('B-meadow-listen-and-find.html') and 'มีวัวกี่ตัว' in _sc8('C-fields-count-it.html') and 'ใหญ่หรือเล็ก' in _sc8('D-fields-big-or-small.html')
          and not any(re.search(r'Thai draft|Tap it|แตะเลย|หาดูนะ',_sc8(f)) for f in _os.listdir(W+'v608build/scenes/html/')) and _NE8 in _sc8('L1-meadow.html'))
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
    print(V+' SC data: meta.sizeSort 3 big + 3 small existing picture cards; 6 Sound Duel pairs carry pics (2 emoji each, in a/b order), the other 24 stay words only; time-of-day by level rule (1 m .. 5 n, repeats) and the front desk scene (no names or signs) in FINAL and spec:',
          all(len(v)==3 and all(_Cd8[i].get('pic') for i in v) for v in _C8_['meta']['sizeSort'].values()) and len(_pp8)==6 and all(len(p_['pics'])==2 for p_ in _pp8) and len(_C8_['soundDuel']['pairs'])==30
          and all(x in _F8 and x in _S8 for x in ('Level 1 `m` morning, 2 `d` midday','5 `n` night, then it repeats','**Front desk (Home Lake):**','No names or signs.','`uiText.listenFind`','`uiText.howManyCows`','`meta.sizeSort`')))

