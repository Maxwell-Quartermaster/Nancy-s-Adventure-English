#!/usr/bin/env python3
import os, sys
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
print("scratch kept at " + d)
sys.exit(t.done())
