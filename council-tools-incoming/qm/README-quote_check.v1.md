**Quartermaster:** # quote_check.py: Maxwell quote and spec-quote checker (patch)
**Quartermaster:** Run: `python3 quote_check.py --file post.md` or `python3 quote_check.py "<post text>"`.
**Quartermaster:** Checks every line starting **Maxwell...** and every "Maxwell said/says/wrote/ruled '...'" against labelled rows in SETTLED-RULINGS.md and ASKS-LEDGER.md.
**Quartermaster:** VERBATIM: exact match to a MAXWELL OWN row (whole text, whole sentences, or pieces in order around a […Name cut…] marker). If the row itself is marked UNVERIFIED (t527u, C7), the output says so.
**Quartermaster:** RELAY: the t-number or text is an Ara relay row. Relabel as **Ara (relay, tN, chat):**.
**Quartermaster:** PARAPHRASE: the t-number is paraphrase-only (NO VERBATIM ON RECORD).
**Quartermaster:** ALTERED: near match with words changed, or cut mid-sentence with no […cut…] marker. A word diff is shown (record->post).
**Quartermaster:** UNKNOWN: no record, or the row is a bot's own words (for example Chancellor t76u).
**Quartermaster:** t-numbers are per chat. If the post names the chat (QM chat, Watchman DM, ...), only that chat's rows count. Otherwise RELAY or PARAPHRASE wins when chats disagree (the cautious answer).
**Quartermaster:** Spec quotes: any line naming spec, rule N or PASTE with a quote of 3+ words is checked word for word against r2h-build/nancys-adventure-english-v6-08-1B-v32-PASTE.md (317e91ce; it warns if the md5 differs). With "rule N" it checks section 1 rule N only.
**Quartermaster:** SPEC-VERBATIM is ok. SPEC-CUT (part of a sentence, no marker), SPEC-ALTERED (diff shown) and SPEC-NOTFOUND are flagged.
**Quartermaster:** Exit 0 = nothing flagged, 1 = something flagged, 2 = usage error. Overrides: `--rulings`, `--ledger`, `--paste`.
**Quartermaster:** Limit: it can only judge against what is on the box. The relays for t141u-t143u have no text on the box, so those come back RELAY by t-number alone.
**Quartermaster:** Self-test: `python3 selftest_quote_check.py`.
