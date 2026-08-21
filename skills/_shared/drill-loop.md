# Drill loop (shared core)

Canonical source for scenario drill skills. After editing, sync copies to `english-collocations/drill-loop-core.md` and `minimal-pairs/drill-loop-core.md`.

## Pack sampling

Each round chooses a **pack** (weighted random):

- **60%** → fresh theme pack (weights defined in each skill's SKILL.md)
- **40%** → **review pack** from `mistakes.md` (prefer `wrong attempts >= 2` OR `last seen` older than 7 days)

Packs are ephemeral — generate on the fly; **only mistakes persist** to disk.

## Round workflow (every round)

1. **Read `mistakes.md`** in full if it exists; plan to create on first miss
2. **Choose pack** (60/40 rule above)
3. **Generate candidates** on the fly (count per skill)
4. **Present the round** in English (mode per skill difficulty ladder)
5. **Wait** for the learner's answer
6. **Grade** using the skill's fixed 6-section **grading block**
7. **Update `mistakes.md`** atomically (read whole file → mutate in memory → write whole file back)
8. **Decide next round** (see Divergence below)
9. After **5–8 rounds**, **recap**: list what was practiced, weak spots, 2–3 model lines to reuse

**Done when:** the learner has received a same-target retry prompt (wrong), a grading block ready for the next message (correct), or a 5–8 round recap.

## Grading block (shared rules)

- Output grading as markdown — **never** wrap in a code fence
- Use exactly **6 sections** in the order defined in each skill's SKILL.md
- Each grading message asks for **at most one** user action
- **Recap** after 5–8 rounds

## mistakes.md update rules

- **Location:** same folder as the skill's SKILL.md
- **On wrong attempt** for tracked key `X`:
  - Section exists → increment `wrong attempts`, update `last seen`, append evidence (dedupe)
  - Section missing → append new section
- **On correct attempt** for tracked key `X`:
  - Decrement `wrong attempts`, update `last seen`
  - When `wrong attempts` reaches 0 → delete the `## X` section
- **Atomicity:** read whole file → mutate → write whole file; never partial-append mid-mutation
- **Never reorder or rewrite untouched entries**
- Create file with header + comment block on first miss if missing

## Divergence (skill-specific)

| Dimension | english-collocations | minimal-pairs |
|-----------|---------------------|---------------|
| mistakes key | collocation phrase | phoneme contrast |
| After correct answer | Same message: Part A grading + Part B `## Next round` | Grading in one message; next round prompt in the **next** message |
| Difficulty ladder | L1–L4 | L1–L2 |

Each skill's SKILL.md owns pack weights, grading section text, difficulty ladder, and any "Next round after correct" rules.
