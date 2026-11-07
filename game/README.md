# Playable game

Static browser game for Nancy's Adventure English. Open `index.html` from this folder. Paths are relative, so a GitHub Pages project subpath can host the folder later without a backend.

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/`. The service worker and IndexedDB need that http origin; a `file://` open will not save.

## Checks

```bash
node --test game/tests/regression.test.mjs
node game/tests/layout-check.mjs
```

Run the second command from the repository root. It serves this folder and drives headless Chrome at 390×844 and 320×568.

## Release gate

Checked before these files were added: GitHub repository `Maxwell-Quartermaster/Nancy-s-Adventure-English` is **private**. The approved cards, daily verses, and title drawing are in this private branch for that reason. This work does not change repository visibility, add a project license, merge, deploy, or change GitHub Pages. Scripture wording is copied, not rewritten. Do not publish this branch.

## Still partial

Gear bonuses, the weapon rows, guardian kneel, the backup review list, and Sound Duel rounds are in this build and covered by tests. Still open: every trophy drawing at full note detail, count/letter/size scenes beyond one step, a full Character shelf, and a physical iPhone pass. Bench tap boxes sit on the seat; a tall emoji can still show a little font padding above the wood.

## Recorded ambiguities

- `ms-04`, `ms-05`, and `ms-06` are marked `fill` and also have real English. They play as written cards. The Example label appears only when `tag` is `Example`.
- A region tap starts one zone. The next tap uses a different open zone in that region, so the end guardian is not locked behind the bonus guardian.
- A locked region names the guardian who opens it.
- Miss feedback uses moonstone. The guardian meter is a dark berry bar on boss screens only.
- The card file does not tag a set of six word-ending pairs. Pairs that share a three-letter ending are eight, including light/right, and those eight are scheduled with the six picture pairs.
