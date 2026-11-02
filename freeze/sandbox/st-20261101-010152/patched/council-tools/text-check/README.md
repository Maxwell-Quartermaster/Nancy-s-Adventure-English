# text-check (owner: Instructor; QM split, Nov 1 2026)

This tool checks the **words** on anything in `sheets/` and `showcase/` before it goes to Maxwell. It adds a text pass to send-guard, next to ground-check's pixel pass. It is standalone, and only Chancellor wires it into send-guard, using `send-guard-text-hook.diff`.

```
python3 text_check.py PATH [PATH ...]          # files or folders; uses QM's pointer /workspace/v608build/CURRENT-SNAP.txt
python3 text_check.py --selftest                # planted faults; must print selftest PASS 32/32 (23 original + 9 freeze-copy cases)
```
From Python, `check(path)` returns the list of blocking problems (`[]` means clear), the same shape as `ground_check.check`. `check_full(path)` returns `block`, `warn`, `sources` and `status`.

**Exit codes:** 0 means clear (warnings may still print), 1 means BLOCK or TEXT UNVERIFIED, and 2 means bad input. These match send-guard. The first line is the stamp: `text-check <md5> words <md5> pointer <md5> snap <snap> paste_1b <md5> chrome yes|no`.

## What it checks
| Check | Where | Result |
|---|---|---|
| Retired wording (`text_check_words.json` → `retired`) | Text nodes plus alt/aria-label/title/placeholder/value of every render source an image was built from, and sheet captions | **BLOCK** (`RETIRED`) |
| Fail words, EN and TH (`fail_words`) | Render-source UI text | **BLOCK** (`FAIL-WORD`) |
| Fail words in a sheet caption (council's own words to Maxwell, e.g. "0 FAIL", "wrong tap") | Builder captions | warning (`CAPTION-MENTION`) |
| Thai under 17 px | Every render source that has Thai, loaded in headless Chrome at its render size (`WxH` in the name, tour.py's size, else 390×844). Computed CSS font-size of each visible element with Thai, which is the domcheck_r2 rule (PASTE :35, :63, :388) | **BLOCK** (`THAI<17`) |
| Thai that is 17 px+ in CSS but under 17 after a real CSS transform/zoom scale | Same | warning (`THAI SCALED<17`) |
| Thai that can't be measured (no Chrome, or Thai drawn into a sheet caption by Pillow) | Same | warning (`THAI SIZE UNMEASURED`), never a pass |
| An image whose text can't be traced to a source | Images | **BLOCK** (`TEXT UNVERIFIED`, its own status) |
| `.md` / `.txt` / `.json` council notes in the folders | Each line | warning (`DOC-MENTION`) only. Notes like INDEX.md quote the old wording on purpose to say it's gone |
| Anything else (e.g. `tour.py`) | n/a | `SKIP`, printed |

**What gets scanned:** only text a player could see. Hidden text in a render source counts too, because a screen state can show it. The PASTE spec prose is never scanned. Its rule text ("no lives, no timers", "wrong taps are graced") is exactly what would cause false hits.

**What's allowed (no false positives on real content):** a hit is allowed only when it sits inside a current paste_1b content string. That means the whole text node equals that string, or the string is 12+ characters and covers the hit. Content strings come from `cards`, `verses`, `jesusWords`, `jesusWordsFallback` and `soundDuel`. On paste_1b this covers:
- the sentence cards P1 keeps: bh-24 "Where is the bathroom?" / "ห้องน้ำอยู่ที่ไหนคะ" and bh-10 "ห้องคลอดอยู่ที่ไหนคะ"
- fd-33 "แพ้อาหารอะไรไหม" (allergy)
- the R/L choice "wrong" (cs-04 / cs-22)

UI chrome (`uiText`, `encouragement`, the reward and wrong texts) is never an allow source.

**The list is checked against the live PASTE on every run.** Each retired entry names the uiText path it replaced, and the run warns `STALE-LIST` if that pattern is live again. `not_retired` confirms the live wording:
- `tapPrompt` "Can you find the {word}?" / "หา {word} เจอไหม" (t440u), so "Can you find" is never flagged
- `pantry` "Shop" (t487u)

## How an image is traced (no OCR on the box)
The tracer tries these in order:
1. **Sidecar** `<img>.sources.txt` (md5 + path per line, the format r2h/sheets uses). A listed source whose md5 changed, or that is missing, makes the image TEXT UNVERIFIED.
2. **Showcase tour.** For `showcase-<key>.png`, it reads `tour.py`'s `SHEETS` with the AST and takes each tile's html. When `r2tp` made a sheet copy, it uses that copy: snapshot `showcase/tiles/` first, then `round2/showcase/tiles/`. It also takes the tile captions, the sheet title, and the fixed question/footer of the `sheet()` call. Tile numbers follow tour.py's own numbering, the same as INDEX.md.
3. **Same-name html** (`x.png` → `x.html`, or `png/x.png` → `html/x.html`).
4. **Builder script** in the snapshot. The script is parsed, never run. The builder is the script whose `save()` / `sheet()` writes the image's name. When one script makes several images, only the statements up to its own `save()` are used, plus shared defs and imports.
   - Captions are the script's string constants, minus docstrings, `re.*` arguments and paths. String constants of the local helper modules it uses (round_totals, r2_fit_table) count as "may be drawn".
   - Inputs are the pasted renders it names. Each is traced again (html next to it, or a sidecar, or its own builder, up to depth 2). `r2tp()` inputs map to r2tp's sheet copy when it made one.
   - **An input path built at run time** (a loop such as `V + r + '.html'`) can't be read without running the script, so the image is TEXT UNVERIFIED.

**Freshness guard (is the source still what the render was made from?)** runs at every html→png pair (same-name html, `png/`→`html/`, tour tiles) and for builder scripts vs their image. Order:
1. **Per-PNG render sidecar `<name>.json`** (next to the PNG, written by QM's renderer). If it records a source hash, the current html is hashed and compared. A match is **VERIFIED whatever the mtimes say**. A mismatch is **TEXT UNVERIFIED** (blocks). Keys read, first found wins:
   - flat: `source_md5`, `html_md5`, `src_md5`, `source_sha256`, `html_sha256`, `source_sha1`, `html_sha1`, `source_hash`, `html_hash`
   - nested: `source` / `html` / `src` → `md5`, `sha256`, `sha1`, `sha`, `hash`, `md5sum`
   - The algorithm follows the hex length: 32 = md5, 40 = sha1, 64 = sha256.
   - **Today's real sidecars** (292 under `round2/r2h/png/`, checked Nov 1 00:55 MDT) have only `vw, vh, snap, paste_md5, html, png, el`, so they **have no source hash**. For them the tool prints `sidecar … has no source hash (fields: …); time check used` and falls back to step 2. When their `html` name differs from the traced html, it prints a `SIDECAR-NAME` warning. QM: adding `"html_md5": md5(html)` at render time turns step 1 on, with no tool change needed.
   - An unreadable sidecar gives a `SIDECAR-UNREADABLE` warning, and the time check is used.
2. **mtime.** A source more than 5 s newer than its render is TEXT UNVERIFIED, except in the **copy-burst** case. That is when the snapshot was written in one plain-copy pass: every MANIFEST-listed file, plus `MANIFEST.md5`, has an mtime within 120 s of the others (if the MANIFEST lists nothing, the files on disk are timed). Both the source and render mtimes must also fall inside that pass. Then their order means nothing. The gap is accepted as a copy **only if** the html's md5 equals its `MANIFEST.md5` / `renders-MANIFEST.md5` entry, and the png's too when it's listed. That always prints a `COPY-BURST` warning, so it's never silent. Without a MANIFEST md5, or on a mismatch, it stays TEXT UNVERIFIED and says why.
   - A `cp -p` / `shutil.copy2` snapshot keeps the real times, so it isn't a burst, and a real edit-after-render still blocks. r2h-0021MDT spans about 6450 s, so it's treated as preserved.
   - The brief's "within ~2 s of each other" rule was not used on its own. A pair 2 s apart already passes the 5 s slack, so that rule could never change a result. The whole-snapshot pass window is what catches html/ and png/ being copied seconds or minutes apart.
- A source changed after a showcase **sheet** was made (tour) is still mtime-only, and is skipped for sources inside the snapshot.
- Sources outside the snapshot (e.g. `/workspace/screens-v608/html`) are checked as they are now, and summed up in an `UNFROZEN-SOURCE` warning.
- **Still best: freeze with `cp -p` / `shutil.copy2`** (QM's freeze.py). The copy-burst rule is a backstop. It can't see an edit made *before* a plain-cp freeze, because those times are already lost.

## Limits (so nobody over-reads a PASS)
- A PASS means the **traced sources** are clean. Without OCR, the tool can't prove the PNG pixels came from those sources. It relies on the snapshot's frozen builder, the r2tp copies, and the time guard.
- Text a builder computes at run time from numbers (round totals) is covered only by the helper's string constants, which is a superset.
- Thai drawn by Pillow in sheet captions (DejaVu has no Thai glyphs) is never measured, only warned.
- The fail-word list is in English and Thai, and so is the scan. Add words to `text_check_words.json` (one object per entry, cite the decision).

## Files
- `text_check.py` is the tool, `text_check_words.json` holds the lists (each entry cites its decision), and this README. The copies before the freeze-copy fix are `text_check.4c3666d1.bak` and `README.e2d69f3d.bak`.
- `send-guard-text-hook.diff` is the proposed send-guard wiring, for Chancellor to apply. It adds `TEXT`/`TXTW` lines, `text_check <md5>` in the stamp, and `--no-text`, which exits 3 and prints `TEXT SKIPPED (--no-text): test only, NOT valid for a send to Maxwell`. The diff was tested only on copies in `hook-scratch/` (sg: send_guard 80615576 + text_check 4c3666d1; sg2: the same send_guard + text_check after the freeze-copy fix, 31/31).
- `runs/` holds run outputs, plus selftest scratch dirs that are kept (no-delete rule).
