# Start here: Nancy's Adventure English

**Quartermaster:** Welcome! This page is the quick tour for any outside AI collaborator. Please read it, then [CONTRIBUTING.md](CONTRIBUTING.md), before you suggest a change.

## What the game is

**Quartermaster:** Nancy's Adventure English is an English-learning adventure RPG made for Nancy, a Thai-speaking adult beginner, to play on her iPhone. It is a gentle game: rest is a gift, nothing ever breaks or fails, and a wrong tap is never called wrong. Each screen should tell her she is seen, loved and capable.

**Quartermaster:** The game is built from one long build prompt (the "PASTE"). Its card data is a JSON block at the end, and Grok Build turns it into the app.

## Which files are current

**Quartermaster:** The live app is **v5-37**. CURRENT stays v5-37: `nancys-adventure-english-v5-37-PASTE.md`, md5 `acc534a51a922102ee37844e04d17955` (in this repo at `root-notes/nancys-adventure-english-v5-37-PASTE.md`).

**Quartermaster:** The working build is **v6-08 1B v32**: `r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md` (md5 `317e91ce86f073c961f8169183d2bbd3`, 188,116 chars). It is not live yet.

**Quartermaster:** The latest frozen snapshot is **`snap-r2h-0021MDT/`**. The pointer file `CURRENT-SNAP.txt` names it, along with its manifest md5s. Only the freeze tool moves the pointer, so please never edit that file by hand.

**Quartermaster:** There is a PASTE size ceiling of 188,200 characters, and the current bank is 84 characters. Every change has to fit inside it.

**Quartermaster:** Schedule: content freeze Fri Nov 6, 11:59 PM PT; Nancy's Thai pass Nov 7; paste Nov 10.

## Folder map

| Path | What is in it |
|---|---|
| `README.md` | Repo title, plus links to this page and CONTRIBUTING.md |
| `CURRENT-SNAP.txt` | Pointer to the latest frozen snapshot and the working PASTE |
| `COUNCIL-HANDBOOK.md` | One-page handbook: bot roles, rules, gates, schedule |
| `SETTLED-RULINGS.md` | Every past ruling, labelled |
| `ASKS-LEDGER.md` | Open and closed questions for Maxwell, with his answers |
| `STATUS.md` | One status row per bot |
| `README-build.md` | v6-08 build log and character ledger |
| `root-notes/` | Earlier FINAL and PASTE versions, including the live v5-37 files |
| `r2h-build/` | The working v6-08 1B PASTE files |
| `snap-r2h-0021MDT/` | Latest frozen snapshot: PASTE, cards, verses, title, code, renders, showcase |
| `snap-*/` | Older frozen snapshots, kept for history |
| `round2/`, `r2h-rerun-stage/`, `r2i-stage/`, `scene-fill-20261101/`, `staged/` | Staged work rounds (not frozen) |
| `r2h-rerun-stage-excluded/` | Items parked out of a stage |
| `scenes/`, `screens/`, `eyes/`, `title/`, `verse-popup/`, `polish-r1/`, `b1/` | Render scripts, screenshots and before/after sheets |
| `decisions/` | Side-by-side choice sheets shown to Maxwell |
| `patches/` | Build patches |
| `freeze/` | The freeze tool, its README and test sandboxes |
| `phone-test/` | Phone test guide |
| `council-tools-incoming/` | Council tools and their test-run outputs (`qm/runs/`) |
| `*.py` at the root | Build, fix and check scripts for v6-08 |

## Hard rules (never break these)

**Quartermaster:** The Bible verses stay byte-identical to the PASTE. Verses are free gifts: never purchasable, and no new verse moments.

**Quartermaster:** Thai text is 17 px or larger, at line-height 1.7.

**Quartermaster:** The game must work in Safari 14 at a 320 pt width.

**Quartermaster:** No surnames.

**Quartermaster:** No personal contact info: no phone numbers, email addresses or street addresses anywhere in the game or this repo.

**Quartermaster:** Page 30 is HELD. Do not change it.

**Quartermaster:** Also from the handbook: no 911, no "Call Max" and no "Show the Nurse"; no timers, energy or fail words; older emoji only (Emoji 13.0 or earlier). Do not write new Thai; every Thai string is a NEEDS NANCY draft that Nancy checks herself.

## Where decisions live

**Quartermaster:** `SETTLED-RULINGS.md` holds every ruling made so far. `ASKS-LEDGER.md` holds every question asked of Maxwell and his answers. Please check both before you propose something, because the answer may already be there.

**Quartermaster:** Labels: **Maxwell (tN, chat):** is used only for Maxwell's own typed words. Anything a bot writes starts with that bot's bold name, like **Quartermaster:**. A summary is marked as a paraphrase.

## How to help

**Quartermaster:** See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: open a pull request, never push to main, and Maxwell approves every change.
