# word-chain Skill — Design Doc

Date: 2026-07-13
Status: Approved (brainstorm phase) → ready for implementation plan
Related skills (siblings, do not merge):
- `skills/chengyu-jielong` — Chinese idiom chain twin (process template)
- `skills/english-collocations` — deeper collocation drilling (cross-link only)

---

## 1. Purpose & Positioning

A narrow **game-host + light teaching** skill for classic English **word chain**: the next word must start with the last letter of the previous word.

- **Game unit**: single English **words** only. Phrases and fixed expressions are **never** playable chain units.
- **Teaching focus**: after a valid play, output a fixed light-teaching block (POS, meaning, pronunciation, example, 1–2 collocations). Collocations exist only as teaching supplements for the played word.
- **Host language**: **English throughout** (rules, corrections, transitions, scoring).
- **Approach**: mirror `chengyu-jielong` session flow (Approach 1 from brainstorm) — AI opens, validate each user play, fixed output template, hints, end-on-request scoring — adapted for English last-letter rules and the English teaching block.

### What this skill is NOT

- Not a difficulty ladder, theme pack, or persistent mistake log.
- Not phrase/collocation-as-move gameplay.
- Not grammar tutoring or bulk vocabulary quizzes.
- Not a merge of `english-collocations` or `chengyu-jielong`.

### Boundary with siblings

| Skill | Role vs word-chain |
|-------|--------------------|
| `chengyu-jielong` | Same host pattern for Chinese idioms; cross-link when user wants 成语接龙 |
| `english-collocations` | Deeper collocation drill; cross-link when user wants to practice pairings beyond the light block |
| `english-tutor` | Conversational grammar; out of scope here |
| `minimal-pairs` | Pronunciation minimal-pair drills; out of scope (word-chain only gives a short pronunciation tip per word) |

---

## 2. Triggers (`description` field)

Model-invoked. Description should match natural phrasings such as:

- "word chain" / "play word chain" / "English word chain"
- "last letter word game" / "words starting with the last letter"
- English 末字母接龙 / 想练英文单词接龙

Include cross-reach clauses for `english-collocations` (deeper collocations) and `chengyu-jielong` (Chinese idiom chain).

---

## 3. Session Workflow

```
Trigger
  → AI plays first word (full teaching block) + prompt for next letter
  → User plays a word
      → invalid → correct and wait (do not continue the chain)
      → valid → affirm + user teaching block → transition → AI teaching block → prompt
  → Repeat until user says stop / quit / end game / I'm done (or similar)
  → Brief score summary + invite another round
```

Rules locked at design time (no opening rule menu):

| Decision | Choice |
|----------|--------|
| Chain rule | Last **alphabetic** letter of previous word = first letter of next word (case-insensitive; ignore trailing punctuation) |
| Who opens | AI always opens |
| Difficulty / theme | None — any valid content word allowed |
| Repeats | Allowed — do not track used words this round |
| End | Only on explicit user request; never end proactively |

Hints: on `hint` / `give me a hint` / `I'm stuck` (or similar), give 1–2 clues (POS, semantic category, length band, or partial letters). **Never** reveal the full target word.

---

## 4. Output Format & Teaching Block

Every field on its own line as **plain text**. Do **not** wrap any output in Markdown code fences, triple backticks, `<pre>`, or other code formatting — some chat UIs render the whole block as a `plaintext` code box.

### Teaching block fields (fixed order)

Used for both a correct user play and every AI play:

```
[Word] elephant
[POS] noun
[Meaning] A very large mammal with a trunk, native to Africa and Asia.
[Pronunciation] /ˈelɪfənt/ — stress on the first syllable; /f/ not /v/.
[Example] The elephant used its trunk to pick up the fruit.
[Collocations] 1) elephant in the room — an obvious problem nobody wants to talk about
2) herd of elephants — the usual group noun for elephants
```

Field requirements:

| Field | Requirement |
|-------|-------------|
| `[Word]` | The played word, lowercase unless a fixed capital form is standard (content words here are normally lowercase) |
| `[POS]` | One primary part of speech for this play: noun / verb / adjective / adverb |
| `[Meaning]` | 1–2 short sentences; accurate dictionary sense for the intended POS |
| `[Pronunciation]` | IPA (or clear stress marking) + one short pitfall tip — not a phonetics lesson |
| `[Example]` | One natural sentence using the word in the stated POS |
| `[Collocations]` | **1–2** items; each = phrase + very short gloss (usage note optional, keep short) |

### Turn order after a correct user play

1. Short affirmation (e.g. `Nice one!`)
2. User word teaching block
3. Blank line + transition: `I'll take the "X":` (X = last letter of the user's word)
4. Blank line + AI word teaching block
5. Prompt: `Your turn — start with "Y".` (Y = last letter of the AI word)

### AI open / AI continue

Emit the teaching block, then the prompt line. No transition line on the opening move.

---

## 5. Validation, Hints, Scoring

### Validation order (every user reply that is a play)

1. **Valid content word?**  
   Common noun / verb / adjective / adverb.  
   Reject: proper nouns, abbreviations, single-letter words, pure interjections, obvious non-words.  
   On fail: `"X" isn't a valid content word for this game. Please try again with a word starting with "Y".` — wait for retry; do not advance.

2. **First letter matches?**  
   Case-insensitive; ignore accidental punctuation around the word.  
   On fail: `"X" is a word, but it must start with "Y". Please try again.` — wait for retry.

3. Both pass → §4 correct-user-play flow.

If the AI accidentally plays a word that breaks the letter rule, admit the mistake and immediately play a valid replacement (full teaching block).

Repeats are allowed; no used-word list.

### End & score

On stop / quit / end game / I'm done (or similar):

1. Stop the chain immediately
2. Report: total words N; AI X; user Y
3. Thank the user and invite another round

---

## 6. Skill File Layout

```
skills/word-chain/
└── SKILL.md
```

README install/symlink entries are implementation follow-ups (same pattern as other skills in this repo).

No scripts, no `mistakes.md`, no external word list file in v1.

---

## 7. Implementation Writing Constraint

When authoring or editing `skills/word-chain/SKILL.md`, **must** read and follow **`writing-great-skills`** (`~/.agents/skills/writing-great-skills/SKILL.md`) before writing:

- Optimize for **predictability** of process
- Prune the model-invoked `description` (front-load, one trigger per branch, no body duplication)
- Use clear **steps** with checkable completion criteria vs **reference** where appropriate
- Prefer the information hierarchy and glossary terms from that skill

Do **not** only copy-paste `chengyu-jielong` wording. Use `chengyu-jielong` as the **behavioral twin** for game flow; use `writing-great-skills` as the **authoring standard** for how the skill text is structured.

The implementation plan (next phase) must list "apply writing-great-skills while drafting SKILL.md" as an explicit step.

---

## 8. Success Criteria

- Trigger phrases reliably select this skill for English word-chain requests
- Every valid turn emits the full teaching block in the fixed field order, as plain text
- Invalid plays are rejected without advancing; hints never give the full word
- Collocations appear only in `[Collocations]`, never as chain moves
- Session ends only on user request, with a correct AI/user word count
- `SKILL.md` authored under `writing-great-skills` constraints

---

## 9. Out of Scope for v1

- Difficulty levels, themes, timed rounds
- Ban-list / no-repeat mode (may be a later optional toggle)
- Persistent cross-session logs
- Bilingual host mode
- Playable multi-word phrases
- Separate reference files or scripts
