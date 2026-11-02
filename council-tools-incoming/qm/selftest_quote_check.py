#!/usr/bin/env python3
import os, re, sys
from _selftest_lib import T, run, scratch
t = T("quote_check selftest"); d = scratch("quote_check")
# (label, post text, expected exit, substring that must appear in the verdict line)
cases = [
    # --- the real slips from the brief
    ("REAL SLIP: spec rule 9 quoted without 'but boss bars.' -> flag",
     '**Watchman:** Spec rule 9 says "Nothing red or alarming anywhere".', 1, "SPEC-CUT"),
    ("REAL SLIP: rule 9 cut quoted in single quotes -> flag",
     "**Chancellor:** per spec rule 9, 'Nothing red or alarming anywhere'", 1, "SPEC-CUT"),
    ("REAL SLIP: Watchman t141u filed as **Maxwell:** -> RELAY",
     "**Maxwell (t141u):** Put the bot name on every note.", 1, "RELAY: "),
    ("REAL SLIP: t142u filed as **Maxwell:** -> RELAY",
     '**Maxwell (t142u, Watchman DM):** "The prefix must be bold."', 1, "RELAY: "),
    ("REAL SLIP: t143u filed as **Maxwell:** -> RELAY",
     "**Maxwell:** (t143u) Act as Quartermaster's extensions.", 1, "RELAY: "),
    ("REAL SLIP: t102u labelled Maxwell -> RELAY",
     "**Maxwell (t102u):** I don't remember saying anything about trophies.", 1, "RELAY: "),
    ("REAL SLIP: '0/85' rule credited to Maxwell, no t-number -> UNKNOWN",
     '**Maxwell:** "Trophies show a 0/85 counter."', 1, "UNKNOWN"),
    ("REAL SLIP: '0/85' via 'Maxwell said' -> UNKNOWN",
     '**Chancellor:** Maxwell said "the trophy tally is 0/85" on the Character pane.', 1, "UNKNOWN"),
    # --- verbatim passes
    ("own words exact (t402u) -> VERBATIM",
     "**Maxwell (t402u, QM chat):** \"You don't have to say tap it! She'll get it\"", 0, "VERBATIM"),
    ("own words, one full sentence of t421u -> VERBATIM",
     '**Maxwell (t421u, QM chat):** "Old news is confusing."', 0, "VERBATIM"),
    ("own words with […QM cut…] marker (t542u) -> VERBATIM",
     "**Maxwell (t542u, Council room):** \"Let's do that, […QM cut…] ask you, then me?\"", 0, "VERBATIM"),
    ("'Maxwell said' + t152u exact -> VERBATIM",
     '**Watchman:** Maxwell said "Red is fine, not a hard rule." (t152u)', 0, "VERBATIM"),
    ("own words, no t-number -> VERBATIM with t-number hint",
     '**Maxwell:** "Title screen should be clean and pretty"', 0, "add the t-number t405u"),
    ("t527u matches but record is UNVERIFIED -> says so",
     '**Maxwell (t527u, QM chat):** "Remove the circles entirely."', 0, "UNVERIFIED"),
    # --- altered
    ("words changed (don't -> do not) -> ALTERED with diff",
     '**Maxwell (t402u):** "You do not have to say tap it! She will get it"', 1, "+[do not]"),
    ("cut mid-sentence with no marker (t409u) -> ALTERED",
     '**Maxwell (t409u):** "multiple choice option for the photos"', 1, "without a […cut…] marker"),
    ("words dropped from t411u without marker -> ALTERED",
     '**Maxwell (t411u):** "when you put it down on a smaller phone, the items start to not line up"', 1, "ALTERED"),
    ("no t-number, near match to t405u -> ALTERED",
     '**Maxwell:** "Title screen should be clean and very pretty"', 1, "ALTERED"),
    # --- relay / paraphrase / other
    ("Ara relay text quoted as Maxwell, no t-number -> RELAY",
     '**Maxwell:** "Photo 7: Looks perfect. No changes."', 1, "RELAY: "),
    ("t482u relay as Maxwell -> RELAY",
     "**Maxwell (t482u):** make sure everyone syncs with you.", 1, "RELAY: "),
    ("t336u paraphrase-only -> PARAPHRASE",
     '**Maxwell (t336u):** "Shields round or square only."', 1, "PARAPHRASE"),
    ("t235u paraphrase-only -> PARAPHRASE",
     "**Maxwell (t235u):** No Settings screen.", 1, "PARAPHRASE"),
    ("Chancellor's own t76u row as Maxwell -> UNKNOWN",
     "**Maxwell (t76u):** No quote exists.", 1, "bot's own row"),
    ("t999u never recorded -> UNKNOWN",
     '**Maxwell (t999u):** "Make it purple."', 1, "UNKNOWN"),
    # --- spec checks
    ("full rule 9 -> SPEC-VERBATIM",
     '**Auditor:** Rule 9 is "Nothing red or alarming anywhere but boss bars."', 0, "SPEC-VERBATIM"),
    ("rule 9 with […cut…] marker -> SPEC-VERBATIM",
     '**Auditor:** spec rule 9: "Nothing red or alarming […QM cut…] but boss bars."', 0, "SPEC-VERBATIM"),
    ("rule 9 word changed -> SPEC-ALTERED",
     '**Auditor:** rule 9 says "Nothing red or scary anywhere but boss bars."', 1, "SPEC-ALTERED"),
    ("line 388 sentence exact, no rule number -> SPEC-VERBATIM",
     '**Chancellor:** the PASTE says "No red fills but boss bars."', 0, "SPEC-VERBATIM"),
    ("made-up spec rule -> SPEC-NOTFOUND",
     '**Watchman:** spec says "Trophy tally shows 0/85 at all times."', 1, "SPEC-NOTFOUND"),
    ("rule 5 exact -> SPEC-VERBATIM",
     '**Instructor:** rule 5: "No voice recognition."', 0, "SPEC-VERBATIM"),
    # --- nothing to check
    ("plain bot line -> NONE, exit 0",
     "**Quartermaster:** Freeze on hold.", 0, "NONE"),
]
for label, text, want_rc, want in cases:
    rc, o = run("quote_check.py", text)
    t.ok(rc == want_rc and want in o, label, o)
# multi-line --file run: one bad line makes the whole post exit 1
p = os.path.join(d, "post.md")
open(p, "w").write("**Quartermaster:** x\n**Maxwell (t402u, QM chat):** \"You don't have to say tap it! She'll get it\"\n**Maxwell (t141u):** prefix\n")
rc, o = run("quote_check.py", "--file", p)
t.ok(rc == 1 and "2 checked, 1 flagged" in o, "--file post: 2 checked, 1 flagged, exit 1", o)
# --- v2: Auditor gate L1-0141 cases
GEN = "ในปฐมกาล พระเจ้าทรงเนรมิตสร้างฟ้าและแผ่นดิน"
v2 = [
    ("KIT-QD2 (gate): rule 9 quoted exactly as PASTE :32 prints it, with '9.' -> SPEC-VERBATIM",
     '**Auditor:** Rule 9 in full (PASTE :32): "9. **Nothing red or alarming** anywhere but boss bars."', 0, "SPEC-VERBATIM"),
    ("PASTE :32 with '9.' but no rule number named -> SPEC-VERBATIM",
     '**Auditor:** the PASTE says "9. **Nothing red or alarming** anywhere but boss bars."', 0, "SPEC-VERBATIM"),
    ("'- ' list marker stripped -> SPEC-VERBATIM",
     '**Auditor:** spec rule 9: "- Nothing red or alarming anywhere but boss bars."', 0, "SPEC-VERBATIM"),
    ("'9.' kept but a word changed -> still SPEC-ALTERED",
     '**Auditor:** Rule 9: "9. Nothing red or scary anywhere but boss bars."', 1, "SPEC-ALTERED"),
    ("'9.' kept but cut -> still SPEC-CUT",
     '**Auditor:** Rule 9: "9. Nothing red or alarming anywhere"', 1, "SPEC-CUT"),
    ("Q04 (gate): t402u words labelled t403u -> WRONG-TNUM",
     "**Maxwell (t403u, QM chat):** \"You don't have to say tap it! She'll get it\"", 1, "WRONG-TNUM"),
    ("Q04b: t402u words labelled t405u (another own row) -> WRONG-TNUM, cites t402u",
     "**Maxwell (t405u, QM chat):** \"You don't have to say tap it! She'll get it\"", 1, "cite t402u"),
    ("Q04c: 'Maxwell said' with wrong t-number -> WRONG-TNUM",
     '**Watchman:** Maxwell said "Red is fine, not a hard rule." (t153u)', 1, "WRONG-TNUM"),
    ("Q04 control: right t-number -> VERBATIM",
     "**Maxwell (t402u, QM chat):** \"You don't have to say tap it! She'll get it\"", 0, "VERBATIM"),
    ("Q06b (gate): Thai Gen 1:1 with ฟ้า -> ฝ้า -> SPEC-ALTERED",
     f'**Instructor:** the PASTE Genesis 1:1 Thai is "{GEN.replace("ฟ้า", "ฝ้า")}"', 1, "SPEC-ALTERED"),
    ("Q06b: altered Thai diff names the changed character",
     f'**Instructor:** the PASTE Genesis 1:1 Thai is "{GEN.replace("ฟ้า", "ฝ้า")}"', 1, "-[ฟ] +[ฝ]"),
    ("Q06b control: exact Thai Gen 1:1 -> SPEC-VERBATIM",
     f'**Instructor:** the PASTE Genesis 1:1 Thai is "{GEN}"', 0, "SPEC-VERBATIM"),
    ("short Thai run (6+ chars) not in PASTE -> SPEC-NOTFOUND",
     '**Instructor:** the PASTE has "ช้างเผือกสีม่วงบินได้"', 1, "SPEC-NOTFOUND"),
    ("Thai under 6 characters -> not checked (NONE)",
     '**Instructor:** the PASTE word "ฟ้า"', 0, "NONE"),
]
for label, text, want_rc, want in v2:
    rc, o = run("quote_check.py", text)
    t.ok(rc == want_rc and want in o, label, o)
# --- v3: Auditor gate L1-0200 T6 (every match tried, not just the first)
v3 = [
    ("T6 (gate 0200): Thai whole value \"ขนมปัง\" whose FIRST match is inside a verse word -> SPEC-VERBATIM",
     '**Instructor:** the PASTE says "ขนมปัง"', 0, "SPEC-VERBATIM"),
    ("T6b control: \"ขนมปัน\" (ง->น) still flagged SPEC-ALTERED",
     '**Instructor:** the PASTE says "ขนมปัน"', 1, "SPEC-ALTERED"),
    ("T6c control: Thai that only ever sits inside a longer verse word -> still SPEC-CUT",
     '**Instructor:** the PASTE says "ขนมปังบาร์"', 1, "SPEC-CUT"),
    ("T6-ASCII: \"Thai Review Queue\" first mid-sentence (PASTE :246), later a whole value -> SPEC-VERBATIM",
     '**Auditor:** the PASTE says "Thai Review Queue"', 0, "SPEC-VERBATIM"),
    ("T6-ASCII-2: \"Colors and Shapes\" first inside the zone-tint row, later a whole value -> SPEC-VERBATIM",
     '**Auditor:** the PASTE says "Colors and Shapes"', 0, "SPEC-VERBATIM"),
    ("T6 control: rule 9 cut still SPEC-CUT after the every-match change",
     '**Watchman:** Spec rule 9 says "Nothing red or alarming anywhere".', 1, "SPEC-CUT"),
]
for label, text, want_rc, want in v3:
    rc, o = run("quote_check.py", text)
    t.ok(rc == want_rc and want in o, label, o)
# E3c (README fix): own-words row beats a paraphrase row for the same t-number
syn = os.path.join(d, "SYN-RULINGS.md")
open(syn, "w").write('| X3 | c | **Maxwell (t901u, QM chat):** "Keep the sword small" | SETTLED |\n'
                     '| X4 | d | **Watchman (paraphrase, Watchman DM):** t901u sword stays small. NO VERBATIM ON RECORD | SETTLED |\n')
empty = os.path.join(d, "EMPTY.md"); open(empty, "w").write("")
rc, o = run("quote_check.py", "--rulings", syn, "--ledger", empty, '**Maxwell (t901u):** "Keep the sword small"')
t.ok(rc == 0 and "VERBATIM" in o, "E3c: own row + paraphrase row on one t-number -> own words win (VERBATIM), as README says", o)
# --- v4: Auditor gate L1-0207 A2/A3 (every own text tried; order never depends on PYTHONHASHSEED)
import subprocess
syn4 = os.path.join(d, "SYN-RULINGS-v4.md")
open(syn4, "w").write('| Y1 | a | **Maxwell (t910u, QM chat):** "Players love the soft blue tiles. Soft blue tiles!" | SETTLED |\n'
                      '| Y2 | b | **Maxwell (t911u, QM chat):** "Make the gate glow gold when the level ends" | SETTLED |\n'
                      '| Y3 | c | **Maxwell (t911u, QM chat):** "Make the gate glow gold" | SETTLED |\n'
                      '| Y4 | d | **Maxwell (t912u, QM chat):** "Keep the shop small and quiet for now" and later "Keep the shop small" | SETTLED |\n'
                      '| Y5 | e | **Maxwell (t913u, QM chat):** "Keep the shop small" | SETTLED |\n'
                      '| Y6 | f | **Maxwell (t913u, QM chat):** "Keep the shop small and quiet for now" | SETTLED |\n')
SEEDS = ["0", "1", "2", "7", "13", "40"]
def run_seeds(post):
    outs = set()
    for sd in SEEDS:
        env = dict(os.environ, PYTHONHASHSEED=sd, PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "quote_check.py"),
                            "--rulings", syn4, "--ledger", empty, post], capture_output=True, text=True, env=env)
        outs.add((p.returncode, p.stdout + p.stderr))
    return outs
v4 = [
    ("A2 (gate 0207): two own rows on t911u, quote = the short row whole -> VERBATIM on every seed",
     '**Maxwell (t911u, QM chat):** "Make the gate glow gold"', 0, "VERBATIM"),
    ("A3 (gate 0207): one row with two quotes, quote = the short one whole -> VERBATIM on every seed",
     '**Maxwell (t912u, QM chat):** "Keep the shop small"', 0, "VERBATIM"),
    ("A3b: same two texts on two rows, short row listed FIRST -> VERBATIM on every seed",
     '**Maxwell (t913u, QM chat):** "Keep the shop small"', 0, "VERBATIM"),
    ("A1 control: one text, first match mid-sentence, later match whole -> VERBATIM",
     '**Maxwell (t910u, QM chat):** "Soft blue tiles"', 0, "VERBATIM"),
    ("A2 control: cut of both t911u rows (no marker) -> still ALTERED, names the shortest row",
     '**Maxwell (t911u, QM chat):** "Make the gate glow"', 1, 'Record: "Make the gate glow gold"'),
    ("A3 control: cut of both t912u texts -> still ALTERED on every seed",
     '**Maxwell (t912u, QM chat):** "Keep the shop"', 1, "without a […cut…] marker"),
    ("A4 control: word changed (gold -> green) on t911u -> ALTERED",
     '**Maxwell (t911u, QM chat):** "Make the gate glow green"', 1, "ALTERED"),
    ("A7 control: whole short text, no t-number -> VERBATIM",
     '**Maxwell:** "Make the gate glow gold"', 0, "VERBATIM"),
]
for label, text, want_rc, want in v4:
    outs = run_seeds(text)
    rc, o = next(iter(outs))
    t.ok(len(outs) == 1 and rc == want_rc and want in o, label + f" ({len(SEEDS)} seeds, identical)", "\n---\n".join(x[1] for x in outs))
# --- v4.1: Auditor gate L1-0226 B1 (bare **Maxwell:** label; t-number elsewhere on the row or in the heading)
syn41 = os.path.join(d, "SYN-RULINGS-v41.md")
open(syn41, "w").write('## Z1 bare rows (t921u, Nov 1)\n'
                       '**Maxwell:** "Watch the gate at night and call the council."\n'
                       '**Maxwell:** (t920u, Nov 1, Z1 update) "Send the urgent email right away. Keep everything else the same"\n'
                       '**Maxwell:** (t923u and t924u, merged) "Paint the shed green"\n'
                       '| Z3 | t927u | **Maxwell:** "Keep the dog bowl full" | SETTLED |\n'
                       '## Z2 notes with no t-number\n'
                       '**Maxwell:** "Keep the lamp on tonight"\n'
                       '**Maxwell:** "Do it the way t930u said"\n')
QC4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quote_check.v4.py")
def run41(post, tool="quote_check.py", seeds=("0", "1", "13", "40")):
    outs = set()
    for sd in seeds:
        env = dict(os.environ, PYTHONHASHSEED=sd, PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), tool),
                            "--rulings", syn41, "--ledger", empty, post], capture_output=True, text=True, env=env)
        outs.add((p.returncode, p.stdout + p.stderr))
    return outs
v41 = [
    ("B1 (gate 0226): bare label, t-number after it on the row, correct cite -> VERBATIM",
     '**Maxwell (t920u):** "Keep everything else the same"', 0, "VERBATIM"),
    ("B1: bare label row, whole text with its row t-number -> VERBATIM, says where the t-number came from",
     '**Maxwell (t920u):** "Send the urgent email right away. Keep everything else the same"', 0, "t-number read from the row"),
    ("B1: bare label under a '## ... (t921u)' heading, correct cite -> VERBATIM",
     '**Maxwell (t921u):** "Watch the gate at night and call the council."', 0, "t-number read from the heading"),
    ("B1: bare-label row text cited under a WRONG t-number -> still WRONG-TNUM, names t920u",
     '**Maxwell (t922u):** "Keep everything else the same"', 1, "cite t920u"),
    ("B1: heading row text cited under the other row's t-number -> WRONG-TNUM, names t921u",
     '**Maxwell (t920u):** "Watch the gate at night and call the council."', 1, "WRONG-TNUM"),
    ("B1: two t-numbers on one bare row, cite the first -> VERBATIM",
     '**Maxwell (t923u):** "Paint the shed green"', 0, "VERBATIM"),
    ("B1: two t-numbers on one bare row, cite the second -> VERBATIM",
     '**Maxwell (t924u):** "Paint the shed green"', 0, "VERBATIM"),
    ("B1: two t-numbers on one bare row, cite neither -> WRONG-TNUM naming both",
     '**Maxwell (t925u):** "Paint the shed green"', 1, "cite t923u, t924u"),
    ("B1: bare label in a table, t-number in an unlabelled cell of the same row -> VERBATIM",
     '**Maxwell (t927u):** "Keep the dog bowl full"', 0, "VERBATIM"),
    ("B1: bare label, no t-number on the row or heading, no cite -> VERBATIM + t-number hint, as before",
     '**Maxwell:** "Keep the lamp on tonight"', 0, "VERBATIM"),
]
for label, text, want_rc, want in v41:
    outs = run41(text)
    rc, o = next(iter(outs))
    t.ok(len(outs) == 1 and rc == want_rc and want in o, label + " (4 seeds, identical)", "\n---\n".join(x[1] for x in outs))
# bare label with no t-number anywhere: v4.1 output must equal v4's, byte for byte
same = [
    ("B1 control: bare label, no t-number anywhere, cited t926u -> same output as v4", '**Maxwell (t926u):** "Keep the lamp on tonight"'),
    ("B1 control: bare label, no t-number anywhere, no cite -> same output as v4", '**Maxwell:** "Keep the lamp on tonight"'),
    ("B1 control: a t-number INSIDE the quote is not the row's (heading reset by '## Z2') -> same output as v4", '**Maxwell (t930u):** "Do it the way t930u said"'),
]
for label, text in same:
    a, b = run41(text), run41(text, QC4)
    t.ok(len(a) == 1 and a == b, label, "v4.1:\n" + "\n".join(x[1] for x in a) + "\nv4:\n" + "\n".join(x[1] for x in b))
# live SETTLED-RULINGS A27 rows (default ledger): the false WRONG-TNUM from gate 0226 is gone
for label, text, want in [
    ("B1 live A27 :168: **Maxwell (t561u):** 'Keep everything else the same' -> VERBATIM", '**Maxwell (t561u):** "Keep everything else the same"', "VERBATIM"),
    ("B1 live A27 :166: **Maxwell (t560u):** whole row text -> VERBATIM",
     '**Maxwell (t560u):** "if he finds anything crazy, urgent, or a big deal (breaking news, security threats, major opportunities, anything time-sensitive), he must immediately involve the council (Quartermaster, Chancellor, Instructor, Auditor) and make sure Maxwell gets his attention right away — do not wait for the next scheduled briefing or status line."', "VERBATIM"),
    ("B1 live A27: t561u words cited as t560u -> WRONG-TNUM", '**Maxwell (t560u):** "Keep everything else the same"', "WRONG-TNUM")]:
    rc, o = run("quote_check.py", text)
    t.ok(rc == (0 if want == "VERBATIM" else 1) and want in o, label, o)
here = os.path.dirname(os.path.abspath(__file__))
t.ok(os.path.isdir(os.path.join(here, "runs", "quote_check")), "tool made its own scratch dir qm/runs/quote_check/ (os.makedirs)")
src = open(os.path.join(here, "quote_check.py")).read()
t.ok(not re.search(r"[\"']/tmp", src) and 'os.path.join(HERE, "runs", "quote_check")' in src, "source: scratch under qm/runs/, no /tmp")
t.ok("texts = sorted({" in src and "for t in own:" not in src, "source (v4): row texts sorted; no early-return loop over own texts")
t.ok("def bare_row_tnums(" in src and 'if kind == OWN and not inside.strip():' in src, "source (v4.1): bare-label t-numbers only for OWN rows with an empty label bracket")
print("scratch kept at " + d)
sys.exit(t.done())
