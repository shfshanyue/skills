# english-collocations Skill — Design Doc

Date: 2026-05-24
Status: Approved (brainstorm phase) → ready for implementation plan
Related skill (sibling, do not merge): `skills/english-tutor`

---

## 1. Purpose & Positioning

A narrow drill-style skill for mastering English **collocations** (fixed word pairings) through scenario-based sentence construction with heavy teaching feedback and persistent mistake tracking across sessions.

- **Scope (collocation types covered)**:
  - verb + noun (`make a decision`, `take a shower`, `do homework`)
  - adj + noun (`heavy rain`, `strong coffee`, `deep sleep`)
  - verb + preposition / phrasal verbs (`depend on`, `look forward to`, `come up with`)
  - adv + adj / adv + verb (`highly recommended`, `strongly agree`)
  - business / academic fixed expressions (`in conclusion`, `with regard to`, `take into account`)
  - **CS / product / engineering domain** (`ship a feature`, `roll out a release`, `spin up a server`, `deprecate an API`, `address technical debt`, `align on requirements`, `unblock the team`, `cut a release`, `merge a PR`, `triage bugs`, `cherry-pick a commit`, etc.)

- **What this skill is NOT**:
  - Not dialogue / role-play (that is `english-tutor`'s job).
  - Not grammar tutoring (only touches grammar when a collocation error involves preposition or tense choice).
  - Not bulk vocabulary drilling — every collocation is practiced inside a scenario.

- **Boundary with `english-tutor`**:
  - `english-tutor` = conversational grammar focus through dialogue.
  - `english-collocations` = drill-driven word-pairing mastery through scenario sentences.
  - The two skills cross-reference each other in their description fields.

---

## 2. Triggers (description field hints)

Skill description should match natural phrasings such as:

- "练习固定搭配 / collocations / 地道搭配 / 词组搭配"
- "中式英语 / Chinglish 修正"
- "ship a feature / roll out / spin up 之类技术表达练习"
- "写邮件搭配不地道"
- "verb + noun collocations / prepositional collocations"
- English business / academic fixed expressions

---

## 3. Session Workflow

```
Round Start
  1. AI reads mistakes.md (if it exists).
  2. AI picks the round's pack source:
       - 60% new theme pack (dev / product / daily / meeting / writing / academic)
       - 40% review pack (sampled from mistakes.md)
  3. AI generates 5–8 candidate collocations for the chosen pack on the fly
     (NOT persisted; packs are ephemeral).
  4. AI presents an English scenario + 1–2 target collocations to use.
  5. User constructs a sentence.
  6. AI grades using the fixed 6-section feedback template (see §4).
  7. If wrong → AI gives a new scenario forcing the SAME collocation again.
     If right → next round at next difficulty level.
  8. AI updates mistakes.md (append new mistake, decrement / remove on correct retry).
  9. Repeat for 5–8 rounds, then recap.
```

### 3.1 Difficulty ladder

| Level | What the user must produce                                        |
| ----- | ----------------------------------------------------------------- |
| L1    | One sentence using **one** target collocation                     |
| L2    | One sentence using **two** target collocations in the same line   |
| L3    | One sentence using one collocation **+ extra constraint** (tense, voice, modal) |
| L4    | A short paragraph (3–5 sentences) containing **three** target collocations |

### 3.2 Adaptive control

- 2 consecutive correct answers → level + 1.
- Any wrong answer → level − 1 (floor at L1).
- Same collocation may not appear at a level the user has already cleared, unless surfaced via the review pack.

### 3.3 Session length & recap

- Default 5–8 rounds per session.
- Recap at end: list practiced collocations, which ones were wrong, 2–3 model sentences to reuse.

### 3.4 Scenario language

- Scenarios are written in **English** (extra reading-comprehension exposure).
- AI may insert a one-line Chinese gloss only if the user explicitly asks.

---

## 4. Feedback Template (fixed format per grade)

Every grading reply MUST use this 6-section template and MUST NOT introduce a new scenario in the same message (single-focus, mirrors `english-tutor`'s correction-only rule):

```
**Score**: x / 5
**Natural version**: <best version, 1–2 variants>
**Why your collocation is off**:
  - <Chinglish? wrong register? wrong preposition? wrong domain?>
**Synonym contrast**:
  - <target collocation> vs <near-synonym 1> vs <near-synonym 2> — where each fits
**Counter-examples**:
  - 1 scenario where the target collocation does NOT fit, with a brief why
**Now try again** (only if original was wrong):
  - A NEW scenario forcing the same collocation
```

- If the original answer was correct, the `Now try again` slot is replaced by a short praise line and the next round begins in a separate message at level + 1.
- The grading message asks for AT MOST one user action.

---

## 5. Persistence: `mistakes.md`

### 5.1 Location & visibility

- Path: `skills/english-collocations/mistakes.md`
- Human-readable and AI-greppable.
- Git tracking is the user's choice (skill itself does not enforce); skill should mention this in a comment near the top of `mistakes.md`.

### 5.2 Format

```markdown
# Collocation Mistakes Log

<!-- Optional: add this file to .gitignore if you don't want to track your mistakes. -->

## ship a feature
- pack: dev / product
- wrong attempts: 2
- last seen: 2026-05-24
- your worst version: "publish a feature this week"
- natural: "ship a feature this week"
- note: `publish` 多用于内容/文章/论文，软件功能用 `ship` / `release` / `roll out`

## turn on the computer
- pack: daily
- wrong attempts: 1
- last seen: 2026-05-20
- your worst version: "open the computer"
- natural: "turn on the computer" / "boot up the computer"
- note: `open` 不与电源/设备搭配
```

### 5.3 Read / write rules

- **Read** at session start (whole file).
- **Review-pack sampling**: prioritize entries with `wrong attempts >= 2` OR `last seen` older than 7 days from today.
- **On wrong attempt** for a collocation:
  - If section exists → increment `wrong attempts`, update `last seen`, append worst version if worse than current.
  - If not → append a new section.
- **On correct attempt** for a tracked collocation:
  - Decrement `wrong attempts`, update `last seen`.
  - When `wrong attempts` reaches 0 → delete the section entirely.
- **Atomicity**: read whole file → mutate in memory → write whole file back. No partial appends mid-mutation.

---

## 6. Boundaries / Anti-patterns

- No role-play dialogue — defer to `english-tutor` for that.
- No general grammar lessons unless directly tied to the offending collocation.
- Never dump > 8 collocations in a single message; always scenario-first.
- Never combine a grading message with a new round's scenario.
- Never silently rewrite or reorder existing `mistakes.md` entries; only touch the entry being graded.

---

## 7. File Inventory

| File                                              | Purpose                                  | Created by      |
| ------------------------------------------------- | ---------------------------------------- | --------------- |
| `skills/english-collocations/SKILL.md`            | The skill definition + workflow prose    | Implementation  |
| `skills/english-collocations/mistakes.md`         | Persistent mistake log (lazy-created on first wrong answer) | Skill at runtime |

No additional pack files, no JSON, no scripts. Packs are generated by the AI per round and discarded.

---

## 8. Open Items (for the implementation plan)

- Exact wording of the `description` field (must pack the trigger phrases from §2 without becoming bloated).
- A worked-example loop in SKILL.md (one full round of: scenario → user sentence → graded feedback → mistakes.md diff) so the AI sees the pattern.
- Decide whether to ship an empty `mistakes.md` stub or let the skill create it on first miss (recommend: create on first miss; keep repo clean).
