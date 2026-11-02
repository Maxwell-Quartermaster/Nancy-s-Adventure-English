# v6 add-ons

## Conversations category (Watchman research, moved to v6 Oct 30)

Source: /workspace/nancys-adventure-english-v5-14-watchman-research.md. Auditor checks these when v6 opens.

C1 One scenario is one run. Each scenario has at most 10 player turns, and each turn fills one pip, so the run fits the existing 10-pip run and the 5-minute rest. Limits: at most 12 nodes, at most 3 choices per node (2 forward plus 1 grace), and every branch rejoins a gather node within 2 steps (note R3.2, Ink weave).

C2 Use the node schema in note R3.1: {id, speaker, en, th, picture, choices:[{en, th, next | grace}]}. A choice has either next or grace, never both. A node with no choices auto-advances after its audio.

C3 Grace redirect (note R1.4/R3.4): the other speaker says "Oh, did you mean…?" and the node replays with the grace choice dimmed to 40%. After 2 grace picks the right choice glows gold. No red X, no XP loss, no damage.

C4 Every line is a usable chunk of at most 8 words with a chunkId. Reuse chunks across scenarios. Design judgment, not sourced: put one repair chunk in all three scenarios, "Sorry, can you say that slowly?", because it's the phrase she'll use most in real life.

C5 Scenario contents for the launch, with no emergency features (the game rule stands):

   - Grocery checkout: greeting, "Paper or plastic?", card or cash, "Do you need a receipt?", thank you.

   - Clinic check-in: name, "I have an appointment at 2," handing over her insurance card, "Can I have a Thai interpreter, please?" The interpreter line is a request, not an emergency, so it fits the rule. Federal rule 45 CFR 92.201 makes the interpreter free.

   - Asking for help in a store: "Excuse me, where is the…?", "Do you have this in…?", the repair chunk.

   Keep labor and medical content in Baby-and-Hospital so the two don't overlap.

C6 Turn format default (still Maxwell's 50/50 from the note; act-don't-ask default applied): she hears the English line, taps the reply tile (English, with the Thai underneath and a picture), then says it aloud on the honor system. No voice recognition.

C7 Every node picture must pass Maxwell's at-a-glance rule from the 4:22 PM flag. One object per node, nothing abstract.

C8 Resume: save {scenarioId, nodeId, graceCount} to IndexedDB after every node. An interruption resumes on the same node, the same as auto-pause.

C9 Validator: window.__test() prints PASS only if every node is reachable, every path ends within 10 turns, there are no dead ends, no choice has both next and grace, and the node and choice limits hold.

C10 Spacing for launch: chunks she missed come back as a short replay in her next session. The scenario-level due boxes (note R1.2) move to v6, matching Chancellor's deferral of spaced boxes.

Chancellor's v6 calls:

G1 Conversations takes the Scrolls tile, and Scrolls moves into My Stuff. The grid stays at 8 tiles.

G2 Conversations opens at level 6, the same level as Colors, so it lands as a reward and not as homework.

G3 The roughly 36 Thai lines get reviewed in January at the earliest, after the baby comes, and stay out of the Nov 7 review.


## Conversations dialogue drafts (Quartermaster, Oct 30, 4:45 PM MT)

Deferred from v5-20 by Chancellor's 4:31 PM scope call. Drafted to the C1-C10 limits above, so nothing has to be rewritten when v6 opens.

- Data: `/workspace/v520/conversations-draft-v6.json`. It holds 3 branching trees: grocery checkout (6 nodes), clinic check-in (5) and asking for help in a store (5). Each node has the other person's line and 2-3 replies. Each reply has either `next` or `grace`, never both. "Sorry, can you say that slowly?" is the grace repeat in every scenario.
- Validator, run Oct 30: every node is reachable, every path ends within 10 turns, there are no dead ends, and each node has 3 choices or fewer.
- Thai: every line is a NEEDS NANCY draft. Instructor's review copy is `/workspace/v520/conversations-for-instructor.md`. Per G3, the review waits until January.
- Excluded: 911, emergency, interpreter and "show the nurse" content (pending Maxwell for the phrasebook; banned in the game). Also no store names, addresses or personal names. Watchman's C5 interpreter line is held back for the same reason.
- Instructor's label for the tile: บทสนทนา (Conversations).

## Animated Map hero (deferred to v6)

v5-20 has a static hero only: about 96 pt, wearing all her equipped gear, standing above the Map grid. The full animated version moves to v6 because it needs new animation art and is scope creep before the Nov 10 paste. That version adds idle breathing, a wave when she returns, and a gear-change flourish, with reduced motion falling back to a fade.

## Spaced review boxes and Sound Duel voices (deferred to v6, Quartermaster, Oct 30, ~5:20 PM MT)

From Watchman's v5-14 research, accepted for v6 by Chancellor's split. v5-20 ships only the word-ending pairs, the 3-new-word cap and the Never list.
- Spaced review boxes: Leitner-style due boxes per card (and per scenario once Conversations lands, note R1.2). v5-20 keeps the simple "cards missed last session" review.
- Sound Duel voices: recorded voices for the Echo Knight pairs instead of speechSynthesis; v5-20 keeps speechSynthesis.

## INFINITY LOOP ideas (Quartermaster, Oct 30, 7:08 PM MT; L4 design lens, out of v5-20 scope)
- Skip-a-card: one gentle "skip for now" per session that sends the card to the review queue without counting as a miss (C1-L4-02).
- Maxwell-voiced encouragement on misses: short recorded lines in his voice replacing the text encouragement (C1-L4-02; pairs with Sound Duel voices above).
- Weekly "you're doing well" note: a Sunday summary of days played and words met, no numbers compared to anyone (C1-L4-02).
- State migration: v5-20 resets playtest data on a schema mismatch (Chancellor 7:05 PM). Before any version changes `schema` after Nancy has real progress, add an additive migration that never drops progress (C3-L3-01).
- Drawn replacements for the Emoji 13.0 pictures (🫂 🪨 🪙 🛻 👰‍♀️) so pre-iOS 14.2 phones never fall back (C2-L2-02).
