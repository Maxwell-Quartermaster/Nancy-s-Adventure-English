#!/usr/bin/env python3
"""quote_check.py - check Maxwell quotes and quoted spec rules in a council post (patch, not installed).

  quote_check.py --file post.md      or      quote_check.py "<post text>"
Maxwell lines (a line starting **Maxwell..., or "Maxwell said/says '...'") get one verdict:
  VERBATIM   exact match against a MAXWELL OWN row (SETTLED-RULINGS.md / ASKS-LEDGER.md)
  RELAY      the t-number or text is an Ara relay row: label it **Ara (relay, tN, chat):**
  PARAPHRASE the t-number is a paraphrase-only row (NO VERBATIM ON RECORD)
  ALTERED    near match with words changed or cut without a [...cut...] marker (diff shown)
  WRONG-TNUM the text matches a MAXWELL OWN row, but under a different t-number than the one cited
  UNKNOWN    no record
Quoted spec rules (a line naming spec / rule N / PASTE with a quote) are checked word for word
against the PASTE: SPEC-VERBATIM, SPEC-CUT, SPEC-ALTERED, SPEC-NOTFOUND.
A leading list marker ("9. ", "- ", "* ") on a spec quote is ignored. Thai quotes are checked when
they hold 6+ Thai characters (Thai has no spaces between words, so word counts don't work).
Exit 0 = only VERBATIM / SPEC-VERBATIM, 1 = anything flagged, 2 = error.
v2 (2026-11-01): list-marker strip, WRONG-TNUM, Thai by character count, own scratch dir runs/quote_check/.
v3 (2026-11-01): every match is tried, not just the first; a quote is whole if ANY match sits at a value or
sentence edge (gate 0200 T6: "ขนมปัง" first appears inside a longer verse word, later as a whole value).
v4 (2026-11-01): gate L1-0207 A2/A3. Ledger rows: every own text is tried before ALTERED (A2), and each row's
texts are sorted so the verdict never depends on PYTHONHASHSEED (A3).
"""
import argparse, difflib, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "runs", "quote_check")  # this tool's own scratch; never /tmp, never another bot's folder
THAI_RE = re.compile(r"[\u0E00-\u0E7F]")
THAI_RUN_RE = re.compile(r"[\u0E00-\u0E7F][\u0E00-\u0E7F \u201c\u201d\"',.!?]*[\u0E00-\u0E7F]")
LIST_MARK_RE = re.compile(r"^\s*(?:\d+[.)]|[-*\u2022])\s+")
THAI_MIN = 6

V = "/workspace/v608build"
DEF_RULINGS = f"{V}/SETTLED-RULINGS.md"
DEF_LEDGER = f"{V}/ASKS-LEDGER.md"
DEF_PASTE = f"{V}/r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md"
PASTE_MD5 = "317e91ce86f073c961f8169183d2bbd3"

LABEL_RE = re.compile(r"\*\*([A-Z][A-Za-z ]*?)(?: \(([^)]*)\))?(?:,[^*]*)?(?::\*\*|\*\*:?)")
T_RE = re.compile(r"\bt(\d+)u\b")
CUT_RE = re.compile(r"\s*\[(?:…|\.\.\.)[^\]]*?cut(?:…|\.\.\.)?\]\s*", re.I)
QUOTE_RE = re.compile(r"[\"“]([^\"”]+)[\"”]|(?<![A-Za-z])'([^']{6,}?)'(?![A-Za-z])|`([^`]+)`")
OWN, RELAY, PARA, BOT = "MAXWELL OWN", "RELAY", "PARAPHRASE", "BOT"


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("–", "-")
    s = re.sub(r"\*\*|`", "", s)
    return re.sub(r"\s+", " ", s).strip()


def key(s):  # comparison form: lowercase, no outer punctuation
    return norm(s).lower().strip(" .!?,;:'\"")


# ---------------------------------------------------------------- records
def load_records(paths):
    """Each labelled cell segment becomes a record: kind, tnums, chat, texts, src."""
    recs = []
    for path in paths:
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            for cell in line.split(" | "):
                labs = list(LABEL_RE.finditer(cell))
                for i, m in enumerate(labs):
                    name, inside = m.group(1).strip(), (m.group(2) or "")
                    if name == "Quartermaster" and not inside:
                        continue  # plain QM note line
                    seg = cell[m.end(): labs[i + 1].start() if i + 1 < len(labs) else len(cell)]
                    il = inside.lower()
                    if "paraphrase" in il:
                        kind = PARA
                    elif "relay" in il or name == "Ara":
                        kind = RELAY
                    elif name == "Maxwell":
                        kind = OWN
                    else:
                        kind = BOT
                    tn = set(T_RE.findall(inside))
                    if kind == PARA:
                        tn |= set(T_RE.findall(seg.split("NO VERBATIM")[0]))
                    if kind == RELAY and not tn:
                        continue
                    chat = ""
                    parts = [p.strip() for p in inside.split(",")]
                    if len(parts) > 1:
                        chat = parts[-1]
                    texts = []
                    if kind in (OWN, RELAY):
                        q = [x for x in re.findall(r'"([^"]{8,})"', seg)]
                        if '"' in seg:
                            a, b = seg.find('"'), seg.rfind('"')
                            if b > a:
                                q.append(seg[a + 1:b])
                        texts = sorted({norm(x) for x in q} - {""})  # v4: sorted, so order never depends on PYTHONHASHSEED
                    recs.append(dict(kind=kind, tnums=tn, chat=chat, texts=texts, who=name,
                                     unverified="UNVERIFIED" in line,
                                     src=f"{path.rsplit('/', 1)[-1]}:{ln}"))
    return recs


# ---------------------------------------------------------------- matching
def pieces(quote):
    return [p for p in (key(x) for x in CUT_RE.split(quote)) if p]


def contains_in_order(text, ps):
    k, pos = key(text), 0
    for p in ps:
        j = k.find(p, pos)
        if j < 0:
            return False
        pos = j + len(p)
    return True


def occurrences(k, piece):
    """Every start index of piece in k (overlapping too), not just the first."""
    out, j = [], k.find(piece)
    while j >= 0 and piece:
        out.append(j)
        j = k.find(piece, j + 1)
    return out


def at_sentence_edges(text, piece):
    """True if ANY occurrence of piece in text sits at a whole value / sentence edge (v3: was first match only)."""
    k = key(text)
    for j in occurrences(k, piece):
        before = k[:j].rstrip()
        after = k[j + len(piece):].lstrip()
        ok_b = before == "" or before[-1] in ".!?:;\"'"
        ok_a = after == "" or after[0] in ".!?;\"'" or after[:1] in "/"
        if ok_b and ok_a:
            return True
    return False


def worddiff(a, b):
    aw, bw = norm(a).split(), norm(b).split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if op == "equal":
            continue
        if i2 > i1: out.append("-[" + " ".join(aw[i1:i2]) + "]")
        if j2 > j1: out.append("+[" + " ".join(bw[j1:j2]) + "]")
    return " ".join(out)


def best_near(quote, texts):
    best = (0.0, None)
    q = key(CUT_RE.sub(" ", quote))
    for t in texts:
        kt = key(t)
        # compare against the best same-length window too, so a short quote of a long row still scores
        r = difflib.SequenceMatcher(None, q, kt).ratio()
        qw, tw = q.split(), kt.split()
        if len(tw) > len(qw) > 2:
            for i in range(0, len(tw) - len(qw) + 1):
                w = " ".join(tw[i:i + len(qw) + 2])
                r = max(r, difflib.SequenceMatcher(None, q, w).ratio())
        if r > best[0]:
            best = (r, t)
    return best


def own_text_match(quote, recs):
    """The MAXWELL OWN record whose text holds this quote verbatim (whole sentences or marked cuts), else None."""
    ps = pieces(quote)
    if not ps:
        return None
    for r in recs:
        if r["kind"] != OWN:
            continue
        for t in r["texts"]:
            if contains_in_order(t, ps) and (len(ps) > 1 or at_sentence_edges(t, ps[0])):
                return r
    return None


def chat_key(c):
    c = c.lower()
    for k in ("qm", "quartermaster", "watchman", "instructor", "chancellor", "auditor", "council"):
        if k in c:
            return "qm" if k == "quartermaster" else k
    return ""


def classify(quote, tnums, recs, chat=""):
    """Return (verdict, detail). t-numbers are per chat, so a chat named in the post narrows the rows."""
    byt = [r for r in recs if r["tnums"] & tnums] if tnums else []
    ck = chat_key(chat)
    if ck and any(chat_key(r["chat"]) == ck for r in byt):
        byt = [r for r in byt if chat_key(r["chat"]) == ck]
    elif len({chat_key(r["chat"]) for r in byt}) > 1:
        pass  # several chats share this t-number; RELAY/PARAPHRASE wins below (the cautious answer)
    tl = ", ".join(f"t{t}u" for t in sorted(tnums, key=int)) or "no t-number"
    if byt:
        kinds = {r["kind"] for r in byt}
        srcs = ", ".join(sorted({r["src"] for r in byt}))
        if RELAY in kinds:
            r = next(r for r in byt if r["kind"] == RELAY)
            chat = f", {r['chat']}" if r["chat"] else ""
            return "RELAY", f"{tl} is an Ara relay row ({srcs}); label it **Ara (relay, {tl}{chat}):**, not **Maxwell:**"
        if OWN in kinds:
            own = [t for r in byt if r["kind"] == OWN for t in r["texts"]]
            if quote:
                ps = pieces(quote)
                # v4 (gate L1-0207 A2/A3): try EVERY own text first; VERBATIM if any one is a whole match.
                # ALTERED-cut only after all were tried, naming the shortest holding text (ties by text), so
                # the result never depends on row or set order.
                held = [t for t in own if ps and contains_in_order(t, ps)]
                if any(len(ps) > 1 or at_sentence_edges(t, ps[0]) for t in held):
                    unv = " (record itself marked UNVERIFIED on the box)" if any(r["unverified"] for r in byt) else ""
                    return "VERBATIM", f"{tl} matches a MAXWELL OWN row ({srcs}){unv}"
                if held:
                    t = min(held, key=lambda x: (len(x), x))
                    return "ALTERED", f"{tl}: quote is cut mid-sentence without a […cut…] marker. Record: \"{t}\""
                w = own_text_match(quote, recs)
                if w and not (w["tnums"] & tnums):
                    rt = ", ".join(f"t{x}u" for x in sorted(w["tnums"], key=int))
                    return "WRONG-TNUM", f"text matches MAXWELL OWN {rt} ({w['src']}), but the post cites {tl}; cite {rt}"
                r, t = best_near(quote, own)
                if t:
                    return "ALTERED", f"{tl} ({srcs}) near match {r:.2f}. Diff record->post: {worddiff(t, CUT_RE.sub(' ', quote))}"
                return "UNKNOWN", f"{tl} is a MAXWELL OWN row ({srcs}) but no verbatim text is on the box to compare"
            return "VERBATIM", f"{tl} is a MAXWELL OWN row ({srcs}); no quote text in the post to compare"
        if PARA in kinds:
            return "PARAPHRASE", f"{tl} is paraphrase-only ({srcs}, NO VERBATIM ON RECORD); label it **<Bot> (paraphrase):**"
        return "UNKNOWN", f"{tl} is a bot's own row ({srcs}), not Maxwell's words"
    # no t-number match: search by text
    if quote:
        ps = pieces(quote)
        for kind in (OWN, RELAY):
            for r in recs:
                if r["kind"] != kind:
                    continue
                for t in r["texts"]:
                    if ps and contains_in_order(t, ps) and (len(ps) > 1 or at_sentence_edges(t, ps[0])):
                        rt = ", ".join(f"t{x}u" for x in sorted(r["tnums"], key=int))
                        if kind == RELAY:
                            return "RELAY", f"text matches Ara relay {rt} ({r['src']}); label it **Ara (relay, {rt}):**"
                        if tnums and not (r["tnums"] & tnums):
                            return "WRONG-TNUM", f"text matches MAXWELL OWN {rt} ({r['src']}), but the post cites {tl}; cite {rt}"
                        return "VERBATIM", f"text matches MAXWELL OWN {rt} ({r['src']}); add the t-number {rt}"
        own = [(t, r) for r in recs if r["kind"] == OWN for t in r["texts"]]
        rr, t = best_near(quote, [x for x, _ in own])
        if t and rr >= 0.75:
            r = next(r for x, r in own if x == t)
            rt = ", ".join(f"t{x}u" for x in sorted(r["tnums"], key=int))
            return "ALTERED", f"near match {rr:.2f} to MAXWELL OWN {rt} ({r['src']}). Diff record->post: {worddiff(t, CUT_RE.sub(' ', quote))}"
    return "UNKNOWN", f"{tl}: no record in SETTLED-RULINGS.md or ASKS-LEDGER.md"


# ---------------------------------------------------------------- spec
def load_paste(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    rules, in_rules = {}, False
    for l in lines:
        if l.startswith("## "):
            in_rules = l.startswith("## 1. Rules")
        m = re.match(r"(\d+)\. (.*)", l)
        if in_rules and m:
            rules[m.group(1)] = norm(m.group(2))
    return [norm(l) for l in lines], rules


def sentences(line):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", norm(re.sub(r"^\s*(?:\d+\.|-)\s+", "", line))) if s.strip()]


def strip_mark(q):
    return LIST_MARK_RE.sub("", q, count=1)


def thai_count(s):
    return len(THAI_RE.findall(s))


def thai_near(quote, paste_lines):
    """Best character-level near match for a Thai quote: compare with every Thai run in the PASTE,
    using same-length character windows so a short quote of a long run still scores."""
    q = key(CUT_RE.sub(" ", quote))
    best = (0.0, None)
    n = len(q)
    for line in paste_lines:
        for run in THAI_RUN_RE.findall(line):
            k = key(run)
            cands = [k] if len(k) <= n else [k[i:i + n] for i in range(0, len(k) - n + 1)]
            for c in cands:
                sm = difflib.SequenceMatcher(None, q, c, autojunk=False)
                if sm.real_quick_ratio() <= best[0] or sm.quick_ratio() <= best[0]:
                    continue
                r = sm.ratio()
                if r > best[0]:
                    best = (r, c)
    return best


def chardiff(a, b):
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        if i2 > i1: out.append("-[" + a[i1:i2] + "]")
        if j2 > j1: out.append("+[" + b[j1:j2] + "]")
    return " ".join(out)


def check_spec(quote, rule_no, paste_lines, rules):
    quote = strip_mark(quote)
    ps = pieces(quote)
    if not ps:
        return None
    scope = [rules[rule_no]] if rule_no and rule_no in rules else paste_lines
    where = f"rule {rule_no}" if rule_no and rule_no in rules else "PASTE"
    # v3: try EVERY line and every match; SPEC-CUT only if no match anywhere is a whole value or sentence
    cut = None
    for line in scope:
        if not contains_in_order(line, ps):
            continue
        in_one = False
        for s in sentences(line):
            if contains_in_order(s, ps):
                in_one = True
                if len(ps) > 1 or key(s) == ps[0] or at_sentence_edges(line, ps[0]):
                    return "SPEC-VERBATIM", f"matches {where} word for word"
                if cut is None:
                    cut = ("SPEC-CUT", f"{where} says \"{s}\"; the quote drops: {worddiff(s, CUT_RE.sub(' ', quote))} (mark cuts as […cut…])")
        if not in_one:
            return "SPEC-VERBATIM", f"matches {where} word for word"
    if cut:
        return cut
    if thai_count(quote) >= THAI_MIN and len(quote.split()) < 3:
        r, t = thai_near(quote, scope)
        if t and r >= 0.8:
            return "SPEC-ALTERED", f"Thai near match {r:.2f} to {where}: \"{t[:160]}\". Char diff PASTE->post: {chardiff(t, key(CUT_RE.sub(' ', quote)))[:300]}"
        return "SPEC-NOTFOUND", f"not in {where} (PASTE {PASTE_MD5[:8]})"
    r, t = best_near(quote, scope)
    if t and r >= 0.6:
        return "SPEC-ALTERED", f"near match {r:.2f} to {where}: \"{t[:160]}\". Diff PASTE->post: {worddiff(t, CUT_RE.sub(' ', quote))[:300]}"
    return "SPEC-NOTFOUND", f"not in {where} (PASTE {PASTE_MD5[:8]})"


# ---------------------------------------------------------------- post scan
MAX_LINE = re.compile(r"^\s*(?:[-*>]\s*)?\*\*Maxwell\b([^*]*)\*\*\s*(.*)")
SAID = re.compile(r"Maxwell\s*(?:\([^)]*\)\s*)?(?:said|says|wrote|ruled)[,:]?\s*", re.I)
SPEC_HINT = re.compile(r"\b(?:spec(?:\s+rule)?|rule)\s*#?\s*(\d+)\b|\bspec\b|\bPASTE\b", re.I)


def quotes_in(s):
    return [norm(next(g for g in m.groups() if g)) for m in QUOTE_RE.finditer(s)]


def scan(post, recs, paste_lines, rules):
    results = []
    for n, line in enumerate(post.splitlines(), 1):
        done = False
        m = MAX_LINE.match(line)
        if m:
            label, rest = m.group(1), m.group(2)
            tn = set(T_RE.findall(label)) or set(T_RE.findall(rest))
            qs = quotes_in(rest) or ([norm(T_RE.sub("", rest)).strip(" ()")] if rest.strip() else [])
            for q in qs or [""]:
                v, d = classify(q, tn, recs, label)
                results.append((n, v, q, d))
            done = True
        if not done and SAID.search(line):
            after = line[SAID.search(line).end():]
            qs = quotes_in(after)[:1]
            tn = set(T_RE.findall(line))
            for q in qs:
                v, d = classify(q, tn, recs, line)
                results.append((n, v, q, d))
        sh = SPEC_HINT.search(line)
        if sh:
            rule_no = None
            mm = re.search(r"\b(?:spec\s+)?rule\s*#?\s*(\d+)\b", line, re.I)
            if mm:
                rule_no = mm.group(1)
            for q in quotes_in(line):
                if len(strip_mark(q).split()) < 3 and thai_count(q) < THAI_MIN:
                    continue  # too short to judge; Thai is measured by characters, not spaces
                r = check_spec(q, rule_no, paste_lines, rules)
                if r:
                    results.append((n, r[0], q, r[1]))
    return results


def make_scratch():
    os.makedirs(SCRATCH, exist_ok=True)
    return SCRATCH


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--rulings", default=DEF_RULINGS)
    ap.add_argument("--ledger", default=DEF_LEDGER)
    ap.add_argument("--paste", default=DEF_PASTE)
    a = ap.parse_args(argv)
    post = open(a.file, encoding="utf-8").read() if a.file else a.text
    if post is None:
        ap.error("give post text or --file")
    make_scratch()
    pm = hashlib.md5(open(a.paste, "rb").read()).hexdigest()
    if pm != PASTE_MD5:
        print(f"NOTE: PASTE md5 {pm[:8]} is not the expected {PASTE_MD5[:8]}; spec checks are against {a.paste}")
    recs = load_records([a.rulings, a.ledger])
    pl, rules = load_paste(a.paste)
    res = scan(post, recs, pl, rules)
    if not res:
        print("NONE: no Maxwell quotes or quoted spec rules found")
        return 0
    flagged = 0
    for n, v, q, d in res:
        ok = v in ("VERBATIM", "SPEC-VERBATIM")
        flagged += not ok
        print(f"{'ok  ' if ok else 'FLAG'} line {n}: {v}: \"{q[:120]}\" - {d}")
    print(f"{len(res)} checked, {flagged} flagged (records: {len(recs)}, PASTE {pm[:8]})")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
