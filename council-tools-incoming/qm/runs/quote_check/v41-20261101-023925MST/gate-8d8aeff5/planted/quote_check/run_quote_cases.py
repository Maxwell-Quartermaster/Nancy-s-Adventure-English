#!/usr/bin/env python3
"""Auditor planted cases for QM quote_check v2 e6deb411 (re-adapted from gate 0141 run_quote_cases.py 3471faa3). Runs the COPY in ../../qm-copy with data copies in ../../data. Writes only here."""
import json, os, re, subprocess, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.dirname(os.path.dirname(H))
TOOL = os.path.join(G, "qm", "quote_check.py"); D = os.path.join(G, "data")
BASE = ["--rulings", f"{D}/SETTLED-RULINGS.md", "--ledger", f"{D}/ASKS-LEDGER.c7461aa0.md", "--paste", f"{D}/nancys-adventure-english-v6-08-1B-v32-PASTE.md"]
KIT = "/workspace/audit/fault-kit/cases/quote_check"
# kit kind -> QM verdicts that count as that kind (adapter only; expectations unchanged)
KMAP = {"UNSOURCED": {"UNKNOWN", "ALTERED", "PARAPHRASE", "WRONG-TNUM"}, "TRUNCATED": {"SPEC-CUT", "ALTERED"}, "RELAY": {"RELAY"}}
def run(args):
    p = subprocess.run([sys.executable, TOOL, *BASE, *args], capture_output=True, text=True, cwd=H)
    return p.returncode, (p.stdout + p.stderr).strip()
def verdicts(o):
    return re.findall(r"^FLAG line \d+: ([A-Z-]+):", o, re.M)
res = []
# ---- fault kit cases (v1.1)
kc = json.load(open(f"{KIT}/cases.json"))["cases"]
for c in kc:
    rc, o = run(["--file", f"{KIT}/{c['post']}"]); fl = verdicts(o)
    if c["expect"] == "CLEAN": ok = rc == 0 and not fl
    else:
        k = c["expect"].split(":")[1]; ok = rc == 1 and any(v in KMAP[k] for v in fl)
    res.append(dict(id="KIT-" + c["id"], expect=c["expect"], rc=rc, flags=fl, ok=ok, required=True, out=o))
# ---- Auditor planted cases: (id, post, expect 'FLAG'/'OK', required, why)
TH_ORIG = "แล้วดาวิดก็พูดกับคนฟีลิสเตียคนนั้นว่า “ท่านมาหาข้าด้วยดาบ ด้วยหอกและด้วยหอกซัด แต่ข้ามาหาท่านในพระนามแห่งพระยาห์เวห์จอมทัพ พระเจ้าแห่งกองทัพอิสราเอล ผู้ซึ่งท่านได้ท้าทาย"  # PASTE :427 1 Sam 17:45 th, whole string
TH_FRAG = "[…Auditor cut…] ท่านมาหาข้าด้วยดาบ ด้วยหอกและด้วยหอกซัด แต่ข้ามาหาท่านในพระนามแห่งพระยาห์เวห์จอมทัพ […Auditor cut…]"
TH_ALT = TH_ORIG.replace("ดาบ", "ดาป")
GEN_ORIG = "ในปฐมกาล พระเจ้าทรงเนรมิตสร้างฟ้าและแผ่นดิน"; GEN_ALT = GEN_ORIG.replace("ฟ้า", "ฝ้า")
P = [
 ("Q01-one-word-change", '**Maxwell (t405u, QM chat):** "Title screen should be clean and beautiful"', "FLAG", True, "one word changed (pretty->beautiful)"),
 ("Q02-dropped-word", '**Maxwell (t405u, QM chat):** "Title screen should be clean pretty"', "FLAG", True, "'and' dropped"),
 ("Q02b-dropped-word-t421u", '**Maxwell (t421u, QM chat):** "Only send photos of final updates not news."', "FLAG", True, "'old' dropped"),
 ("Q03-curly-quotes-control", '**Maxwell (t402u, QM chat):** “You don’t have to say tap it! She’ll get it”', "OK", True, "curly vs straight is typography only; must stay VERBATIM"),
 ("Q03b-curly-apostrophe-only", '**Maxwell (t402u, QM chat):** "You don’t have to say tap it! She’ll get it"', "OK", True, "curly apostrophes inside straight quotes"),
 ("Q04-wrong-tnum-correct-text", '**Maxwell (t403u, QM chat):** "You don\'t have to say tap it! She\'ll get it"', "FLAG", True, "text is t402u, cited as t403u"),
 ("Q04b-wrong-tnum-other-own-row", '**Maxwell (t405u, QM chat):** "You don\'t have to say tap it! She\'ll get it"', "FLAG", True, "text is t402u, cited as t405u (an existing own row)"),
 ("Q05-paraphrase-as-Maxwell", '**Maxwell (t405u, QM chat):** The title page needs to look tidy and nice.', "FLAG", True, "paraphrase under a Maxwell label"),
 ("Q05b-paraphrase-no-tnum", '**Maxwell:** Keep the title tidy and nice.', "FLAG", True, "paraphrase, no t-number"),
 ("Q05c-paraphrase-said-unquoted", '**Auditor:** Maxwell said the title screen should be tidy and nice.', "FLAG", False, "ADVISORY: unquoted 'Maxwell said' paraphrase"),
 ("Q06-thai-1char-long", f'**Instructor:** the PASTE verse text is "{TH_ALT}"', "FLAG", True, "Thai David verse, one char ดาบ->ดาป"),
 ("Q06-control-thai-exact", f'**Instructor:** the PASTE verse text is "{TH_ORIG}"', "OK", True, "control: exact Thai"),
 ("Q06c-thai-fragment-edge-cut-markers", f'**Instructor:** the PASTE verse text is "{TH_FRAG}"', "OK", False, "ADVISORY: fragment marked with […cut…] at both edges"),
 ("Q06b-thai-1char-short", f'**Instructor:** the PASTE Genesis 1:1 Thai is "{GEN_ALT}"', "FLAG", True, "Thai Gen 1:1 (2 space-separated words), one char ฟ้า->ฝ้า"),
 ("Q07-relay-as-own-text", '**Maxwell:** "Tile 25: looks fine, looks good, he likes it."', "FLAG", True, "t487u relay text under **Maxwell:**"),
 ("Q07b-relay-via-said", '**Chancellor:** Maxwell said "Maxwell wants you to ask him questions directly from now on, instead of routing them through Ara."', "FLAG", True, "t490u relay quoted as Maxwell said"),
 ("Q07c-relay-tnum-own-chat-label", '**Maxwell (t487u, QM DM):** "Flow would be: choose your character, then gear, then shop"', "FLAG", True, "t487u relay cited as own words"),
 ("T5-thai-5char-exact", '**Instructor:** the PASTE says "สีแดง"', "OK", True, "5 Thai chars (PASTE th 'red'): under THAI_MIN 6, must stay exit 0"),
 ("T5b-thai-5char-1letter", '**Instructor:** the PASTE says "สีแดว"', "OK", False, "ADVISORY/RECORD: 5 Thai chars with one letter changed; below threshold so not checked by design"),
 ("T6-thai-6char-exact", '**Instructor:** the PASTE says "ขนมปัง"', "OK", True, "6 Thai chars exact (bread): SPEC-VERBATIM"),
 ("T6b-thai-6char-1letter", '**Instructor:** the PASTE says "ขนมปัน"', "FLAG", True, "6 Thai chars, ง->น: must flag"),
 ("TM1-mixed-exact", '**Instructor:** the PASTE ask is "หา {word} เจอไหม"', "OK", True, "short Thai+English template exact"),
 ("TM2-mixed-1letter", '**Instructor:** the PASTE ask is "หา {word} เจอไหน"', "FLAG", True, "short Thai+English template, ม->น"),
 ("TM3-mixed-boss-1letter", '**Instructor:** the PASTE says "ได้รับเมื่อชนะบอส {n} ครั่ง"', "FLAG", True, "Thai+{n} template, ้->่ tone mark"),
 ("TM4-mixed-short-thai", '**Instructor:** the PASTE label is "แลกด้วย {n}"', "OK", True, "2-word Thai(7)+{n} exact"),
 ("E1-relay-no-text-t141u", '**Maxwell (t141u):** anything at all here', "FLAG", True, "KNOWN EDGE: relay with no text on box resolves by t-number alone (RELAY)"),
 ("E2-t527u-unverified", '**Maxwell (t527u, QM chat):** "Remove the circles entirely."', "OK", True, "KNOWN EDGE: VERBATIM but must say UNVERIFIED"),
]
for i, post, exp, req, why in P:
    rc, o = run([post]); fl = verdicts(o)
    ok = (rc == 1 and bool(fl)) if exp == "FLAG" else (rc == 0 and not fl)
    if i == "E2-t527u-unverified": ok = ok and "UNVERIFIED" in o
    if i in ("Q04-wrong-tnum-correct-text", "Q04b-wrong-tnum-other-own-row"): ok = ok and "WRONG-TNUM" in fl
    if i == "Q06b-thai-1char-short": ok = ok and any(v.startswith("SPEC-") for v in fl)
    res.append(dict(id=i, expect=exp, rc=rc, flags=fl, ok=ok, required=req, why=why, out=o))
# ---- E3 repeated t-number across chats: synthetic ledger copy (in this folder)
syn = os.path.join(H, "SYN-RULINGS.md")
open(syn, "w").write(
 '| X1 | a | **Maxwell (t900u, QM chat):** "Make the map brighter please" | SETTLED |\n'
 '| X2 | b | **Ara (relay, t900u, Watchman DM):** "Maxwell wants the map brighter" | SETTLED |\n'
 '| X3 | c | **Maxwell (t901u, QM chat):** "Keep the sword small" | SETTLED |\n'
 '| X4 | d | **Watchman (paraphrase, Watchman DM):** t901u sword stays small. NO VERBATIM ON RECORD | SETTLED |\n'
 '| X5 | e | **Watchman (paraphrase, Watchman DM):** t902u shield round. NO VERBATIM ON RECORD | SETTLED |\n')
E3 = [("E3a-t900u-no-chat-own+relay", '**Maxwell (t900u):** "Make the map brighter please"', "FLAG", True, "KNOWN EDGE: own(QM)+relay(Watchman) same t-number, no chat named -> cautious RELAY"),
      ("E3b-t900u-QM-chat", '**Maxwell (t900u, QM chat):** "Make the map brighter please"', "OK", True, "chat named narrows to the QM own row"),
      ("E3e-t902u-paraphrase-only", '**Maxwell (t902u):** "Keep the shield round"', "FLAG", True, "paraphrase-only t-number -> PARAPHRASE"),
      ("E3c-t901u-no-chat-own+paraphrase", '**Maxwell (t901u):** "Keep the sword small"', "OK", True, "v2 README: own-words win over paraphrase for one t-number -> VERBATIM"),
      ("E3d-t901u-unknown-chat", '**Maxwell (t901u, Instructor DM):** "Keep the sword small"', "OK", True, "v2 README: named chat has no row -> all chats used -> VERBATIM")]
for i, post, exp, req, why in E3:
    p = subprocess.run([sys.executable, TOOL, "--rulings", syn, "--ledger", f"{D}/ASKS-LEDGER.c7461aa0.md", "--paste", f"{D}/nancys-adventure-english-v6-08-1B-v32-PASTE.md", post], capture_output=True, text=True, cwd=H)
    o = (p.stdout + p.stderr).strip(); fl = verdicts(o)
    ok = (p.returncode == 1 and bool(fl)) if exp == "FLAG" else (p.returncode == 0 and not fl)
    res.append(dict(id=i, expect=exp, rc=p.returncode, flags=fl, ok=ok, required=req, why=why, out=o))
for r in res:
    tag = "PASS" if r["ok"] else ("FAIL" if r["required"] else "ADVISORY-MISS")
    print(f"{tag} {r['id']}: expect {r['expect']} got exit {r['rc']} {r['flags'] or ''}")
    if not r["ok"] or r["id"].startswith("E"): print("     " + r["out"].replace("\n", "\n     ")[:700])
req = [r for r in res if r["required"]]
print(f"TOTAL required {sum(r['ok'] for r in req)}/{len(req)}; advisory {sum(r['ok'] for r in res if not r['required'])}/{sum(not r['required'] for r in res)}")
json.dump(res, open(os.path.join(H, "results.json"), "w"), ensure_ascii=False, indent=1)
