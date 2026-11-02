import json,hashlib,re,os,collections
KIT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F=json.load(open(f"{KIT}/tmp/facts.json")); XR=json.load(open(f"{KIT}/tmp/xref.json")); X=XR['X']
SRC="/workspace/qm/cards-fix-20261102-0704/new/nancys-adventure-english-v6-08-1B-v32-cards1A-fix-PASTE.md"
L=open(SRC,encoding='utf-8').read().split('\n'); d=json.loads(L[426])
sha=lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
QM="**Quartermaster:** "
BASE="snap-r2h-0021MDT, pointer f6dac2d0, PASTE 317e91ce (CURRENT-SNAP); kit built on candidate 5e1666fe (not yet frozen as pointer)"
p1,p2,h1,h2,js,src=F['p1'],F['p2'],F['h1'],F['h2'],F['json'],F['src']
def secnum(s):
    if not s: return '?'
    m=re.match(r'(\d+(?:\.\d+)?)',s); return '§'+m.group(1) if m else s[:24]
def lines(v):
    out=[];seen=set()
    for n,s in zip(v['lines'],v['secs']):
        if n in seen: continue
        seen.add(n); out.append(f"{n}")
    secs=[]; [secs.append(secnum(s)) for s in v['secs'] if secnum(s) not in secs]
    return ','.join(out), ' '.join(secs)
ORDER=['card id','trophy id','svg id','zone prefix','zone key','top-level key','uiText key','data path','data key','data value','defaulted field','derived','id pattern','attached file','must-not-exist']
TITLE={'card id':'Card ids (cards[] in Part 2)','trophy id':'Trophy ids (trophies[])','svg id':'SVG / picture ids (picPlan, cards[].pic)','zone prefix':'Zone prefixes (zones[].prefix)','zone key':'Zone keys (zones[].key)','top-level key':'Top-level data keys and lists (needsMaxwell, zones, uiText, verses …)','uiText key':'uiText keys (labels; Build never hardcodes label text)','data path':'Dotted data paths (picPlan.*, verses.*, meta.*, zones[].*, trophyRules.*, mapLayout.*)','data key':'Field names (resolve inside the object the sentence is about)','data value':'Field = value statements','defaulted field':'Fields that are often ABSENT in the file and take a default','derived':'Derived values (computed from other data, not stored)','id pattern':'Id patterns','attached file':'Attached files and clip paths (outside the two parts)','must-not-exist':'Names that must NOT exist anywhere'}
by=collections.defaultdict(list)
for t,v in X.items(): by[v['cat']].append((t,v))
xt=[]
for c in ORDER:
    if not by.get(c): continue
    xt.append(f"\n### {TITLE[c]} ({len(by[c])})\n\n| Spec names | Lives in Part 2 at | Part 1 lines | Sections |\n|---|---|---|---|")
    for t,v in sorted(by[c],key=lambda x:(x[1]['lines'][0],x[0])):
        ln,sc=lines(v); w=v['where'].replace('|','/')
        xt.append(f"| `{t.replace('|','/')}` | {w} | {ln} | {sc} |")
XT='\n'.join(xt)
ui_named=len(by['uiText key'])
zones=F['zones']
ztab='\n'.join(f"| {o} | `{k}` | {n} | `{p}` | {F['byzone'][k]} | {'yes, '+str(bc)+' cards, scroll '+sr if b else 'none'} |" for o,k,n,p,b,bc,sr in zones)
G=f"""**Quartermaster:** I wrote this guide for Build. It is a draft kit for a two-part paste of Nancy's Adventure English, made from PASTE {src['md5'][:8]} on 2026-11-02 (UTC 07:52).

# COMBINE GUIDE — for Build

**If you can reach Quartermaster, ask. Otherwise follow this guide.**

You have been given the game prompt in two parts because it is long. Join them back into one document, then build from the joined document exactly as if it had come as one paste. Nothing in the game changes because of the split.

## 1. What the two parts are

| Part | What it holds | Source lines | Characters | Bytes (UTF-8) | md5 (no header) |
|---|---|---|---|---|---|
| Part 1 (`part1.md`) | The full spec: HOW TO USE, sections 0 to 20 | {p1['lines']} | {p1['chars']:,} | {p1['bytes']:,} | `{p1['md5']}` |
| Part 2 (`part2.md`) | The CARD FILE: authority paragraph, heading, and the `cards.json` block (one JSON line, line 427) | {p2['lines']} | {p2['chars']:,} | {p2['bytes']:,} | `{p2['md5']}` |
| Joined | The original single prompt | 1-{src['lines']} | {src['chars']:,} | {src['bytes']:,} | `{src['md5']}` |

Also attached, as before, and **not** part of either part: `nancys-adventure-english-v6-08-title.svg` (the title picture) and `nancys-adventure-english-v6-08-daily-verses.json` (30 daily verses). Part 1 names both.

The JSON line on its own (Part 2, the line between ` ```json ` and ` ``` `): {js['chars']:,} characters, {js['bytes']:,} bytes, md5 `{js['md5']}` (with one trailing newline: `{js['md5nl']}`), SHA-256 `{sha(L[426])}`. Save it as `cards.json` exactly, byte for byte.

## 2. Read order

1. This guide.
2. Part 1 in full. Do not start coding.
3. Part 2 in full. Parse the JSON and confirm it is valid.
4. Join (section 3), then run the checks in section 4 of this guide.
5. Only then build, in the four stages of Part 1 section 19.

If the parts come with a first line that starts `<!-- Part N of 2`, that line is a label from Quartermaster. Delete it before joining. It is not part of the game.

## 3. Join into one logical spec before coding

- Joined text = Part 1 + Part 2, in that order, with nothing added or removed between them. Part 1 already ends with `---` and a blank line, and Part 2 starts at `## CARD FILE`.
- After joining, every place in Part 1 that says "this prompt", "this document", "the JSON block at the end of this prompt", "Paste this entire document" or "one paste" means the joined document. The split does not change the build order: still four stages, each printing `PASS` (section 19).
- Treat every name Part 1 gives in backticks as a pointer into Part 2. Section 5 lists all of them.
- Never build from Part 1 alone, and never treat Part 2 as optional. If Part 2 has not arrived, stop and ask for it.

## 4. Join checks (run before stage 1)

1. `cards.json` parses as JSON. It has {len(F['topkeys'])} top-level keys: {', '.join('`'+k+'`' for k in F['topkeys'])}.
2. The md5 of `cards.json` is `{js['md5']}` (or `{js['md5nl']}` if you saved it with one trailing newline). SHA-256 without newline: `{sha(L[426])}`.
3. `cards` has {F['cards']} entries with {F['unique']} unique ids, matching "**{F['cards']} cards**" in Part 1 section 16 and `meta.totalCards` = {F['meta']['totalCards']}.
4. Every name in section 5 resolves. The scan below found **0** names in Part 1 that point at a card id missing from Part 2.
5. If you can hash the joined text, it should be md5 `{src['md5']}`. If your input box trimmed whitespace and the joined md5 differs, the build is still fine as long as checks 1 to 3 pass. Tell Quartermaster or Maxwell the md5 you got.

## 5. Rules that override

1. **The card file wins on all card content** (Part 1 line 12 and Part 2 line 422): text, Thai, respellings, answers, pictures, hints, zones, bosses, trophies, labels, verses and slots. If Part 1 and Part 2 disagree on card content, Part 2 wins.
2. **File strings win over any Thai here** (Part 1 line 358). Any Thai quoted in Part 1 is only for reference. Use the Thai in Part 2.
3. **Do not generate, write or edit Thai** (lines 6 and 361). Every Thai string is a `NEEDS NANCY` draft. Use it exactly as written.
4. **Verse text is exact** (lines 6, 344, 345, 404, 410). The 16 verses, the 6 Jesus words and `verses.attribution` must be byte-identical to the file. Never trim, capitalize, re-punctuate, or add or remove a quote mark. `\\n` is a line break.
5. **Supplied art is exact** (line 147). Inline `picPlan.inlineSvg`, `picPlan.trophyInlineSvg` and `picPlan.uiInlineSvg` as given. Never redraw them.
6. **Labels come from the file** (rule 7, line 30). Never hardcode label text. Take it from `uiText` and the other string keys.
7. **No orphans** (rule 11, line 34). Every `cards.json` field and every `uiText` key gets used, and every field the spec names exists in the file. This includes the four `uiText` keys that Part 1 covers only through the pattern `uiText.bonus<word>`: {', '.join('`'+k+'`' for k in F['ui_unnamed'])}.
8. **Spec text beats any mockup** (line 52).
9. **Defaults fill absent fields** (line 352). A field missing from a card takes `meta.cardDefaults`, `meta.modeByType`, `meta.typeByZone`, `meta.cardThStatusDefault` or `meta.thStatusDefault`. A missing field is not an error when a default covers it. See the "defaulted" and "derived" tables in section 7.

## 6. If something is missing or does not match

- **Stop and ask. Never invent.** Don't invent a card, a Thai string, a verse, a key, an id or a count to make something fit.
- Ask Quartermaster if you can reach him. If not, ask Maxwell, and name the exact item, for example: "Part 1 line 371 names `ms-28` but I can't find it in Part 2."
- A missing `title.svg`: stop and ask for it. Never redraw it (line 157).
- A missing voice clip is skipped silently (lines 135 and 365). That one is by design, not an error.
- Never build from only one part. If Part 2 looks cut off, for example the JSON doesn't parse or doesn't end with `}}`, ask for it to be pasted again.

## 7. Every cross-reference from Part 1 into Part 2

I produced this list by scanning every backticked name, and every card id written as plain text, in Part 1 (lines 1-426) and resolving each one against the JSON in Part 2.

**{F['xref_unique']} unique names, {F['xref_occ']} mentions.** By kind: {', '.join(f"{k} {v}" for k,v in sorted(F['xref_cats'].items(), key=lambda x:-x[1]))}. Missing from Part 2: **{len(F['missing'])}**.

Every one of them crosses the split: the rule lives in Part 1 and the data lives in Part 2.

Not listed here: {F['spec_only']} backticked items that are not data. They are CSS, HTML, colors, regexes, browser APIs, and runtime `state` or ledger names such as `state.hero`, `naeState` and `region:<id>`. Part 1 defines those, and you create them. There are also {F['secrefs']} section cross-references inside Part 1 (for example "section 10" and "(6.4)"). They stay inside Part 1 and don't cross the split.

### Zones at a glance (`zones[]`, Part 2)

| order | key | name | prefix | cards | boss |
|---|---|---|---|---|---|
{ztab}

Region order (`mapLayout.regions`): {'; '.join(f"{i} {n} = {', '.join(z)}" for i,n,z in F['regions'])}. `startZone` = `{F['startZone'][0]}`.
{XT}
"""
open(f"{KIT}/COMBINE-GUIDE.md",'w',encoding='utf-8').write(G)

# ---------- SELF-CHECK
vrows='\n'.join(f"| {i+1} | {w} | {r} | `{sha_en}` | `{sha_th}` |" for i,(w,r,sha_en,sha_th) in enumerate(
    [(w,v['ref'],sha(v['en']),sha(v['th'])) for w,v in [('weekly',x) for x in d['verses']['weekly']]+[('rest',d['verses']['rest'])]+[('boss:'+z['key'],z['boss']['scroll']) for z in d['zones'] if z.get('boss')]]))
jrows='\n'.join(f"| {i+1} | {v['ref']} | `{sha(v['en'])}` | `{sha(v['th'])}` |" for i,v in enumerate(d['jesusWords']))
at=d['verses']['attribution']
m=F['meta']; pic=F['pic']; bt=F['bytype']
S=f"""{QM}SELF-CHECK for Build. Run these after generating each stage, and all of them after stage 4. The expected numbers below come from the file (PASTE `{src['md5']}`, `cards.json` md5 `{js['md5']}`). Any mismatch is a stop-and-ask, never a silent fix.
{QM}Hashes are SHA-256 of the UTF-8 string with nothing added, so `crypto.subtle.digest('SHA-256', …)` can check them in `window.__test()`. A `\\n` inside a verse is a real newline character.

## A. Card data

| # | Check | Expected |
|---|---|---|
| A1 | `cards.json` byte check | md5 `{js['md5']}` (with trailing newline: `{js['md5nl']}`); SHA-256 `{sha(L[426])}` |
| A2 | `cards.length` | {F['cards']} (= `meta.totalCards` {m['totalCards']}, `meta.writtenCards` {m['writtenCards']}) |
| A3 | unique `id`s | {F['unique']}, duplicates 0 |
| A4 | cards per zone (by prefix) | {', '.join(f"{k} {v}" for k,v in F['byzone'].items())} |
| A5 | resolved `type` (after `meta.typeByZone`, then `picture`) | picture {bt['picture']}, say-it {bt['say-it']}, server-talk {bt['server-talk']}, two-answer {bt['two-answer']} (sum {sum(bt.values())}) |
| A6 | explicit `type:"say-it"` cards | {m['sayItTotal']} (= `meta.sayItTotal`; the other {bt['say-it']-m['sayItTotal']} say-it cards are Kitchen cards via `meta.typeByZone`) |
| A7 | picture cards | {m['pictureCards']}: emoji 73, `svg:` 39, `null` fallback 14 (= `meta.pics`) |
| A8 | `personal` true (after defaults) | {F['personal']} (= `meta.personalCards`) |
| A9 | `nursePhrase` true | {len(F['nurse'])}: {F['nurse'][0]} to {F['nurse'][-1]} |
| A10 | `thDef` present | {F['thDef']} (= `meta.thDefCards`) |
| A11 | `fill:true` (Inn examples, Example tag) | {', '.join(F['fill'])} |
| A12 | `thStatus:"SIGNED OFF"` | {', '.join(F['signedoff'])}; every other card resolves to `NEEDS NANCY` |
| A13 | two-answer card | `ms-31` only, 2 `choices`, 2 `prompts` |
| A14 | `needsMaxwell` | {len(F['needsMaxwell'])}: {', '.join(F['needsMaxwell'])} (= `meta.needsMaxwellCount` {m['needsMaxwellCount']}) |
| A15 | `meta.outings` | {len(F['outings'])}: {', '.join(F['outings'])} |
| A16 | every card id in Part 1 exists in `cards` | 0 missing |

## B. Zones, map, bosses

| # | Check | Expected |
|---|---|---|
| B1 | `zones.length`, order | 7: {', '.join(z[1] for z in zones)} |
| B2 | prefixes | {', '.join(f"{z[1]} `{z[3]}`" for z in zones)} |
| B3 | `startZone` | `phonics` only |
| B4 | bosses | 5 zones with 10 cards each (phonics, colors-shapes, numbers, sight-words, baby-hospital); maxwell-says and kitchen `boss: null` |
| B5 | `mapLayout.regions` | 4: {'; '.join(f"{i} {n} [{', '.join(z)}]" for i,n,z in F['regions'])} |
| B6 | zone clips + boss clips + reward clips | 7 + 5 + {F['clips']} = 17 (skipped silently if missing) |

## C. Verses (16) and Jesus words (6): text must be byte-identical

| # | Check | Expected |
|---|---|---|
| C1 | verse count | 16 = 10 `verses.weekly` + 1 `verses.rest` + 5 `zones[].boss.scroll` (= `meta.versesVerified` {m['versesVerified']}); all `status:"VERIFIED"` |
| C2 | daily cycle | 40 = 10 weekly + 30 in `daily-verses.json`; day 41 shows verse 1 |
| C3 | Jesus words | {F['jwn']} in `jesusWords`, all given at start; `jesusWordsFallback` {F['jwf']} |
| C4 | attribution | `verses.attribution.esv` SHA-256 `{sha(at['esv'])}`; `.thsv11` `{sha(at['thsv11'])}`; `esvTag` "{at['esvTag']}", `thsv11Tag` "{at['thsv11Tag']}" |
| C5 | no `cost`/`price` field anywhere | 0 (also none in `state`) |

| # | Where | Ref | SHA-256 `en` | SHA-256 `th` |
|---|---|---|---|---|
{vrows}

| # | Jesus words | SHA-256 `en` | SHA-256 `th` |
|---|---|---|---|
{jrows}

## D. Strings, art, trophies

| # | Check | Expected |
|---|---|---|
| D1 | `uiText` keys | {F['ui']} (= `meta.uiTextEntries`); every key used somewhere in the UI |
| D2 | `encouragement` lines | {F['enc']} |
| D3 | `trophies` | {F['troph']} (= `meta.trophies`; by `meta.trophiesByCat`: {', '.join(f"{k} {v}" for k,v in d['meta']['trophiesByCat'].items())}) |
| D4 | `soundDuel.pairs` | {F['duel']}, of which {F['duelpics']} carry `pics` |
| D5 | `picPlan.svg` / `trophySvg` / `uiSvg` | {pic['svg']} / {pic['trophySvg']} / {pic['uiSvg']} |
| D6 | supplied inline art (inline exactly, never redraw) | `inlineSvg` {len(pic['inline'])} ({', '.join(pic['inline'])}); `trophyInlineSvg` {len(pic['trophyInline'])} ({', '.join(pic['trophyInline'])}); `uiInlineSvg` {len(pic['uiInline'])} ({', '.join(pic['uiInline'])}) |
| D7 | drawings Build makes | 55 = `svgDrawnCount` {pic['svgDrawn']} + `trophySvgDrawnCount` {pic['trophyDrawn']} + 1 coin |
| D8 | `pantry.items` | {F['pantry']} |
| D9 | `version` / `meta.version` | `{d['version']}` / `{m['version']}` |
| D10 | Thai untouched | every Thai string in the build equals its `cards.json` string byte for byte |

## E. Join-specific

| # | Check | Expected |
|---|---|---|
| E1 | no `<!-- Part N of 2` header text anywhere in the build | 0 |
| E2 | the build used both parts | every section 7 row in COMBINE-GUIDE resolves; 0 missing |
| E3 | joined prompt (if hashable) | md5 `{src['md5']}`, {src['chars']:,} chars |

{QM}Based on: {BASE}.
{QM}Ready to paste: none. This is a draft kit, and CURRENT stays v5-37.
"""
open(f"{KIT}/SELF-CHECK.md",'w',encoding='utf-8').write(S)
json.dump({'p1':p1,'p2':p2,'h1':h1,'h2':h2,'src':src,'json':js},open(f"{KIT}/tmp/sizes.json",'w'))
print('ok', len(G), len(S))
