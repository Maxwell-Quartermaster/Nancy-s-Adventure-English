# Contributing to Nancy's Adventure English

**Quartermaster:** Thanks for helping! New here? Start with [START-HERE.md](START-HERE.md).

## The basics

**Quartermaster:** Use pull requests only. Never push to `main`, and never force-push.

**Quartermaster:** Maxwell approves every change. Nothing merges without his yes.

**Quartermaster:** Keep each change small and labelled. Every pull request should say:
- which file or files it touches (full path),
- which version it is based on (for example `v6-08 1B v32`, PASTE md5 `317e91ce`, or snapshot `snap-r2h-0021MDT`),
- what it changes and why, in plain words,
- its PASTE character cost, if it touches the PASTE (ceiling 188,200; bank 84 right now).

**Quartermaster:** One idea per pull request. If you have two options, describe them side by side as 1A and 1B so Maxwell can pick one.

## Please do not

**Quartermaster:** Do not edit older versions in `root-notes/` or the frozen `snap-*` folders. Propose changes against the latest build, v6-08 1B v32, in `r2h-build/`.

**Quartermaster:** Do not edit `CURRENT-SNAP.txt` by hand. Only the freeze tool moves it.

**Quartermaster:** Do not change any Bible verse, even by one byte.

**Quartermaster:** Do not write or rewrite Thai. Nancy checks every Thai string herself.

**Quartermaster:** Do not add personal contact info (phone numbers, emails, addresses), surnames, passwords, tokens or keys.

**Quartermaster:** Do not change page 30. It is HELD.

## Rule check before you open a pull request

- [ ] Verses byte-identical
- [ ] Thai 17 px or larger, line-height 1.7
- [ ] Works in Safari 14 at 320 pt
- [ ] No surnames, no personal contact info
- [ ] Page 30 untouched
- [ ] Checked `SETTLED-RULINGS.md` and `ASKS-LEDGER.md` first

## Writing style

**Quartermaster:** Lines a bot writes start with its bold name, like **Quartermaster:**. Use **Maxwell (tN, chat):** only to quote Maxwell's own words exactly. Mark a summary as a paraphrase.

## Council workflow (branches)

**Quartermaster:** `main` holds only checked, Maxwell-approved work. No bot pushes to `main` directly.
**Quartermaster:** Each bot works on its own branch, and each branch owns one lane, so changes never clash:

| Branch | Owner | Lane |
|---|---|---|
| `quartermaster/integration` | Quartermaster | Build lead: merges, freezes, the PASTE file |
| `instructor/thai` | Instructor | Thai text and Nancy's sign-off sheets |
| `watchman/placeholders` | Watchman | Placeholder cards and research-backed fixes |
| `chancellor/scope` | Chancellor | Scope, budget fit tables, boss options |
| `auditor/gates` | Auditor | Gate reports, fault kits, check results |

**Quartermaster:** Flow: bot commits to its branch, then Auditor gates it, then Quartermaster merges into `quartermaster/integration` one change at a time, then Maxwell says yes, then it merges into `main` and gets a version tag.
**Quartermaster:** Every saved build gets a tag like `v6-08-1B-v32` so any version can be restored.
**Quartermaster:** Outside collaborators open pull requests from their own branch, using the same rules.
