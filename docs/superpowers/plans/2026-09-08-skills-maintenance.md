# Skills Maintenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every skill appear in README, AGENTS, and evals; unify descriptions; extract the reddit-promotion template; reshape english-tutor; drop seo-geo; add a catalog CI check.

**Architecture:** A new `scripts/check-catalog.sh` diffs the filesystem skill set against four parse windows (README install, README table, AGENTS clusters, evals Expected skill). Skill bodies, evals, and indexes are edited in place until that check passes. Shared-file CI stays. No catalog generator, no eval runner.

**Tech Stack:** bash, awk, GitHub Actions, Markdown skill files.

**Spec:** [`docs/superpowers/specs/2026-09-08-skills-maintenance-design.md`](../specs/2026-09-08-skills-maintenance-design.md)

## Global Constraints

- One pack: every `skills/<name>/SKILL.md` except `_shared` is listed in README table, README `--skill` install lines, AGENTS skill clusters, and evals Expected skill.
- Descriptions: leading word + `Use when` + one trigger per branch; user-invoked skills use `Use when the user attaches @name or /name`.
- CI runs only `scripts/check-shared.sh` then `scripts/check-catalog.sh`. No description lint, no Done-when lint, no eval numbering check.
- `check-catalog.sh` derives the skill set from the filesystem; do not hard-code the 19 names.
- Evals stay in `evals/trigger-cases.md`. Behavioral cases are named (`gerrit review`, `zh-en-gloss density`, `microsaas own-product`), not numbered in the trigger sequence.
- Do not add `seo-geo`. Do not name it in `google-traffic`.
- Do not change `gerrit` / `gh` CLI workflows, game rules, or other skills' step structure.
- Bump `metadata.version` on every skill file that changes.
- `docs/superpowers/specs/` are not runtime pointers.

## File map

| File | Responsibility |
|------|----------------|
| `scripts/check-catalog.sh` | Compare filesystem skills to four catalog sources; print missing/extra; exit 1 on mismatch |
| `scripts/test-check-catalog.sh` | Fixture tests for the checker (local TDD; not a CI step) |
| `.github/workflows/check-shared.yml` | Run shared sync then catalog check |
| `skills/gerrit/SKILL.md`, `gh/SKILL.md`, `zh-en-gloss/SKILL.md`, `thirty-seconds/SKILL.md` | Description + version only |
| `skills/google-traffic/SKILL.md` | Drop `seo-geo`; version bump |
| `skills/reddit-promotion/template.md` | Generated plan skeleton |
| `skills/reddit-promotion/SKILL.md` | Point at template; keep copy guidelines |
| `skills/english-tutor/SKILL.md` | Open / host-each-message / Reference |
| `evals/trigger-cases.md` | Renumber; add missing trigger rows; Behavioral section |
| `README.md` | Install + table + tree for `gerrit`/`gh`; Reddit MCP note |
| `AGENTS.md` | Clusters, add-skill catalog step, description `@` rule, CI |

---

### Task 1: Catalog checker

**Files:**
- Create: `scripts/check-catalog.sh`
- Create: `scripts/test-check-catalog.sh`
- Modify: `.github/workflows/check-shared.yml`

**Interfaces:**
- Consumes: repo layout `skills/<name>/SKILL.md`, README `## Quick Install` / `## Skills`, AGENTS `## Reference — skill clusters` (em dash), `evals/trigger-cases.md` tables
- Produces: `CHECK_CATALOG_ROOT` (optional, default repo root); `scripts/check-catalog.sh` exits 0 iff all four sources match the filesystem set; stderr/stdout lists `MISSING <source>: name ...` and `EXTRA <source>: name ...`

- [ ] **Step 1: Write the failing fixture test**

Create `scripts/test-check-catalog.sh`:

```bash
#!/usr/bin/env bash
# Fixture tests for check-catalog.sh. Not run by CI.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHECKER="$ROOT/scripts/check-catalog.sh"
FAIL=0

assert_exit() {
  local want="$1" label="$2"
  shift 2
  local rc=0
  "$@" > /tmp/check-catalog-out.txt 2>&1 || rc=$?
  if [ "$rc" -ne "$want" ]; then
    echo "FAIL $label: exit $rc want $want"
    cat /tmp/check-catalog-out.txt
    FAIL=1
  else
    echo "PASS $label (exit $want)"
  fi
}

assert_grep() {
  local pattern="$1" label="$2"
  if grep -E "$pattern" /tmp/check-catalog-out.txt >/dev/null; then
    echo "PASS $label"
  else
    echo "FAIL $label: no match /$pattern/"
    cat /tmp/check-catalog-out.txt
    FAIL=1
  fi
}

make_fixture() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir/skills/alpha" "$dir/skills/beta" "$dir/evals"
  printf '%s\n' '---' 'name: alpha' '---' '# A' > "$dir/skills/alpha/SKILL.md"
  printf '%s\n' '---' 'name: beta' '---' '# B' > "$dir/skills/beta/SKILL.md"
  cat > "$dir/README.md" <<'EOF'
# fixture

## Quick Install

```bash
npx skills add org/skills --skill alpha
npx skills add org/skills --skill beta
npx skills add org/skills
```

## Skills

| Skill | One-line |
|-------|----------|
| [`alpha`](skills/alpha/SKILL.md) | A |
| [`beta`](skills/beta/SKILL.md) | B |

## Hooks
EOF
  cat > "$dir/AGENTS.md" <<'EOF'
# AGENTS

## Reference — skill clusters

| User intent | Skill |
|-------------|-------|
| Alpha work | `alpha` |
| Beta work | `beta` (helper) |

## Reference — hooks
EOF
  cat > "$dir/evals/trigger-cases.md" <<'EOF'
# Trigger eval cases

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 1 | do alpha | `alpha` | loads |
| 2 | do both | `alpha` → `beta` | hand-off |
| 3 | unrelated | none | no load |
EOF
}

FIX=$(mktemp -d)
trap 'rm -rf "$FIX"' EXIT
make_fixture "$FIX"

export CHECK_CATALOG_ROOT="$FIX"
assert_exit 0 "complete fixture" bash "$CHECKER"

# Missing from README table
sed -i.bak '/skills\/beta\/SKILL.md/d' "$FIX/README.md"
assert_exit 1 "missing readme-table" bash "$CHECKER"
assert_grep 'MISSING readme-table:.*beta' "reports missing beta table"
make_fixture "$FIX"

# Extra in evals
printf '%s\n' '| 4 | ghost | `ghost` | no |' >> "$FIX/evals/trigger-cases.md"
assert_exit 1 "extra evals" bash "$CHECKER"
assert_grep 'EXTRA evals:.*ghost' "reports extra ghost"
make_fixture "$FIX"

# none is not a skill
# (already in fixture; complete fixture must still pass — covered above)

if [ "$FAIL" -ne 0 ]; then
  echo "test-check-catalog: FAILED"
  exit 1
fi
echo "test-check-catalog: all passed"
```

- [ ] **Step 2: Run the test and confirm it fails**

Run: `bash scripts/test-check-catalog.sh`

Expected: FAIL because `scripts/check-catalog.sh` does not exist (`No such file or directory`) or the checker is missing.

- [ ] **Step 3: Write `scripts/check-catalog.sh`**

```bash
#!/usr/bin/env bash
# Compare skills/ directories to README, AGENTS clusters, and evals.
set -euo pipefail

ROOT="${CHECK_CATALOG_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

section() {
  local file="$1" heading="$2"
  awk -v h="$heading" '
    $0 == h {p=1; next}
    p && /^## / {exit}
    p {print}
  ' "$file"
}

# Newline-separated sorted unique names.
fs_skills() {
  local d name
  for d in "$ROOT/skills"/*/SKILL.md; do
    [ -f "$d" ] || continue
    name="$(basename "$(dirname "$d")")"
    [ "$name" = "_shared" ] && continue
    printf '%s\n' "$name"
  done | sort -u
}

readme_install() {
  section "$ROOT/README.md" "## Quick Install" \
    | grep -E 'npx skills add' \
    | grep -oE -- '--skill[[:space:]]+[a-z0-9-]+' \
    | awk '{print $2}' \
    | sort -u
}

readme_table() {
  section "$ROOT/README.md" "## Skills" \
    | grep -oE '\[`[a-z0-9-]+`\]\(skills/[a-z0-9-]+/SKILL\.md\)' \
    | sed -E 's/\[`([a-z0-9-]+)`\]\(skills\/\1\/SKILL\.md\)/\1/' \
    | sort -u
}

agents_clusters() {
  section "$ROOT/AGENTS.md" "## Reference — skill clusters" \
    | awk -F'|' '
      NR<=2 {next}
      NF<3 {next}
      {
        col=$3
        if (match(col, /`[a-z0-9-]+`/)) {
          s=substr(col, RSTART+1, RLENGTH-2)
          print s
        }
      }
    ' | sort -u
}

evals_expected() {
  awk -F'|' '
    /^\|/ && $2 !~ /^[[:space:]]*#/ && $2 !~ /---/ && NF>=4 {
      col=$4
      while (match(col, /`[a-z0-9-]+`/)) {
        s=substr(col, RSTART+1, RLENGTH-2)
        if (s != "none") print s
        col=substr(col, RSTART+RLENGTH)
      }
    }
  ' "$ROOT/evals/trigger-cases.md" | sort -u
}

diff_set() {
  local label="$1" got="$2" want="$3"
  local missing extra
  missing="$(comm -23 "$want" "$got" | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  extra="$(comm -13 "$want" "$got" | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  if [ -n "$missing" ]; then
    echo "MISSING $label: $missing"
    RC=1
  fi
  if [ -n "$extra" ]; then
    echo "EXTRA $label: $extra"
    RC=1
  fi
}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

fs_skills > "$TMP/fs"
readme_install > "$TMP/readme-install"
readme_table > "$TMP/readme-table"
agents_clusters > "$TMP/agents-clusters"
evals_expected > "$TMP/evals"

RC=0
diff_set "readme-install" "$TMP/readme-install" "$TMP/fs"
diff_set "readme-table" "$TMP/readme-table" "$TMP/fs"
diff_set "agents-clusters" "$TMP/agents-clusters" "$TMP/fs"
diff_set "evals" "$TMP/evals" "$TMP/fs"

if [ "$RC" -ne 0 ]; then
  exit 1
fi
echo "All catalog sources match skills/."
```

AGENTS heading uses a Unicode em dash: `## Reference — skill clusters`. Copy it from `AGENTS.md`; a hyphen-minus will parse an empty section.

- [ ] **Step 4: Run fixture tests**

Run: `bash scripts/test-check-catalog.sh`

Expected: `test-check-catalog: all passed`

If `readme_table` sed fails to keep `alpha`/`beta`, fix the regex until the complete fixture exits 0.

- [ ] **Step 5: Confirm the real repo fails**

Run: `bash scripts/check-catalog.sh ; echo EXIT:$?`

Expected: exit 1, and the output includes at least:

```
MISSING readme-install: gerrit gh
MISSING readme-table: gerrit gh
MISSING agents-clusters: thirty-seconds
MISSING evals: reddit-promotion thirty-seconds
```

(order of names on a line may follow `sort`.) Do not fix README/AGENTS/evals in this task.

- [ ] **Step 6: Wire CI**

Replace `.github/workflows/check-shared.yml` with:

```yaml
name: check-shared

on:
  push:
  pull_request:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/check-shared.sh
      - run: bash scripts/check-catalog.sh
```

Keep the filename `check-shared.yml`.

- [ ] **Step 7: Commit**

```bash
git add scripts/check-catalog.sh scripts/test-check-catalog.sh .github/workflows/check-shared.yml
git commit -m "Add catalog membership check."
```

---

### Task 2: Description-only skill edits

**Files:**
- Modify: `skills/gerrit/SKILL.md` (frontmatter only)
- Modify: `skills/gh/SKILL.md` (frontmatter only)
- Modify: `skills/zh-en-gloss/SKILL.md` (frontmatter only)
- Modify: `skills/thirty-seconds/SKILL.md` (frontmatter only)

**Interfaces:**
- Consumes: spec §4 target wording
- Produces: four descriptions that start with a leading word and contain `Use when`; `disable-model-invocation: true` unchanged on gerrit/gh/zh-en-gloss

- [ ] **Step 1: Write a failing assertion**

```bash
python3 - <<'PY'
import pathlib, re, sys
root = pathlib.Path("skills")
want = {
  "gerrit": r"Use when the user attaches `@gerrit` or `/gerrit`",
  "gh": r"Use when the user attaches `@gh` or `/gh`",
  "zh-en-gloss": r"Use when the user attaches `@zh-en-gloss` or `/zh-en-gloss`",
  "thirty-seconds": r"Use when the user wants 30 Seconds cards or 30秒卡片",
}
failed = False
for name, pat in want.items():
    text = (root / name / "SKILL.md").read_text()
    fm = text.split("---", 2)[1]
    desc = re.search(r'^description:\s*(.*)$', fm, re.M).group(1)
    if "Use when" not in text.split("---", 2)[1] or not re.search(pat, text):
        print(f"FAIL {name}: description does not match {pat}")
        failed = True
    else:
        print(f"PASS {name}")
sys.exit(1 if failed else 0)
PY
```

Expected before edits: FAIL on all four.

- [ ] **Step 2: Replace frontmatter**

`skills/gerrit/SKILL.md` lines 1–7:

```yaml
---
name: gerrit
description: Gerrit SSH operator. Use when the user attaches `@gerrit` or `/gerrit` to query, diff, review, or run Gerrit CLI subcommands.
disable-model-invocation: true
metadata:
  version: 1.3.1
---
```

`skills/gh/SKILL.md` lines 1–7:

```yaml
---
name: gh
description: GitHub CLI operator. Use when the user attaches `@gh` or `/gh` to run `gh` subcommands.
disable-model-invocation: true
metadata:
  version: 1.0.1
---
```

`skills/zh-en-gloss/SKILL.md` lines 1–7:

```yaml
---
name: zh-en-gloss
description: Gloss formatter. Use when the user attaches `@zh-en-gloss` or `/zh-en-gloss` for inline 词 (English) glosses in Chinese replies.
disable-model-invocation: true
metadata:
  version: 1.3.3
---
```

`skills/thirty-seconds/SKILL.md` lines 1–6:

```yaml
---
name: thirty-seconds
description: "Thirty Seconds card generator. Use when the user wants 30 Seconds cards or 30秒卡片."
metadata:
  version: 1.0.1
---
```

Do not edit bodies below the closing `---`.

- [ ] **Step 3: Re-run the assertion**

Run the same `python3` block from Step 1.

Expected: `PASS` four times, exit 0.

- [ ] **Step 4: Commit**

```bash
git add skills/gerrit/SKILL.md skills/gh/SKILL.md skills/zh-en-gloss/SKILL.md skills/thirty-seconds/SKILL.md
git commit -m "Unify user-invoked and thirty-seconds descriptions."
```

---

### Task 3: Remove seo-geo from google-traffic

**Files:**
- Modify: `skills/google-traffic/SKILL.md`

**Interfaces:**
- Consumes: spec §4 google-traffic
- Produces: file contains no `seo-geo` string; on-page SEO stated as out of scope without naming another skill

- [ ] **Step 1: Write the failing assertion**

```bash
if grep -n 'seo-geo' skills/google-traffic/SKILL.md; then
  echo FAIL: seo-geo still present
  exit 1
else
  echo PASS: no seo-geo
fi
```

Expected: FAIL (matches on description, intro, Step 5, Boundaries).

- [ ] **Step 2: Edit the four sites**

Frontmatter `description` (drop the last sentence, keep folded style):

```yaml
description: >-
  Traffic reporter for GA4 and Search Console MCP reports. Use when the user
  wants search traffic review, GSC or GA4 data, monthly traffic ritual, page
  traffic deep-dive, or URL indexing status.
metadata:
  version: 1.1.2
```

Intro paragraph (line 14) replace:

```markdown
Pull **GA4** and **Google Search Console** data through bundled MCP servers. Report trends, page-level search performance, and indexing health. On-page title, meta, schema, and JSON-LD are out of scope. Project SEO scripts live in the repo's `AGENTS.md`.
```

Step 5 bullet list: **delete** the line `- If changes need title/meta/schema/JSON-LD → hand off to \`seo-geo\``.

Step 5 Done when, replace with:

```markdown
**Done when:** summary is in the chat (table or bullets).
```

Boundaries, replace the `seo-geo` row with:

```markdown
- Title, meta, schema, JSON-LD, and keyword research for copy → out of scope.
```

- [ ] **Step 3: Re-run the assertion**

```bash
if grep -n 'seo-geo' skills/google-traffic/SKILL.md; then
  echo FAIL: seo-geo still present
  exit 1
else
  echo PASS: no seo-geo
fi
```

Expected: PASS. Also `grep -n 'seo-geo' skills/google-traffic/` on the whole folder exits 1 (no matches).

- [ ] **Step 4: Commit**

```bash
git add skills/google-traffic/SKILL.md
git commit -m "Drop seo-geo pointer from google-traffic."
```

---

### Task 4: Extract reddit-promotion template

**Files:**
- Create: `skills/reddit-promotion/template.md`
- Modify: `skills/reddit-promotion/SKILL.md`

**Interfaces:**
- Consumes: current SKILL.md output skeleton (today's Step 5 fenced markdown) and `launch-kit` pointer pattern
- Produces: `template.md` is the only copy of the generated-doc skeleton; SKILL.md Step 5 points at it; copy guidelines stay in SKILL.md; version `1.1.0`

- [ ] **Step 1: Write the failing assertion**

```bash
python3 - <<'PY'
from pathlib import Path
skill = Path("skills/reddit-promotion/SKILL.md").read_text()
tmpl = Path("skills/reddit-promotion/template.md")
failed = False
if not tmpl.exists():
    print("FAIL: template.md missing")
    failed = True
if "# [Product Name] — Reddit Promotion Plan" in skill:
    print("FAIL: skeleton still inlined in SKILL.md")
    failed = True
if "template.md" not in skill:
    print("FAIL: SKILL.md does not point at template.md")
    failed = True
if "Sound like a real Reddit user" not in skill:
    print("FAIL: copy guidelines missing from SKILL.md")
    failed = True
if failed:
    raise SystemExit(1)
print("PASS")
PY
```

Expected: FAIL (`template.md missing` and skeleton still inlined).

- [ ] **Step 2: Create `skills/reddit-promotion/template.md`**

```markdown
# Reddit Promotion Plan Template

Use this exact section order when generating `reddit-promotion.md`.

```markdown
# [Product Name] — Reddit Promotion Plan

> Generated on [date]. Based on product analysis and live Reddit data.

---

## Product Summary

[One paragraph summary of the product, target audience, and key differentiators]

**Search keywords used:** [list]

---

## Recommended Subreddits

[Ranked table from Step 2]

---

## High-Value Posts

[Ranked list from Step 3, grouped by subreddit]

---

## Action Plan

### Post: "[post title]"
**Subreddit:** r/name | **Author:** u/name | **Link:** [url]
**Why it matches:** [explanation]

**Suggested reply:**
> [reply draft]

**DM template:**
> [DM draft]

---

[Repeat for each post]

## Weekly Search Prompts

Reusable prompts to run regularly for finding new opportunities:

- [prompt 1]
- [prompt 2]
- ...
```
```

Match `launch-kit/template.md`: an outer instruction line, then one fenced `markdown` block with the skeleton. Nested fences: the outer file uses a wrapping fence longer than the inner one if needed; if the tool rejects nested fences, use a 4-backtick outer fence around the inner 3-backtick skeleton (same as launch-kit).

- [ ] **Step 3: Edit `SKILL.md`**

1. Frontmatter version `1.0.1` → `1.1.0`.
2. In Step 5, **delete** the paragraph `The output document structure:` and the following fenced markdown skeleton (through the closing fence before `After writing the file`).
3. Keep file-location logic and the "After writing the file…" sentence and Done when.
4. Insert immediately after the Step 5 `---` that precedes Copy Guidelines (or before Copy Guidelines):

```markdown
## Template Structure

Use [`template.md`](template.md) as the single source of truth for the generated `reddit-promotion.md` structure.
```

5. Leave Copy Guidelines and Skill Boundaries unchanged.
6. In Step 5, after file-location logic, add one sentence: `Write the document following [`template.md`](template.md).`

Step 5 should read:

```markdown
### Step 5: Output

**File location logic:**
1. If `reddit-promotion.md` already exists somewhere in the project → update it in place
2. Otherwise → create `docs/reddit-promotion.md`

Write the document following [`template.md`](template.md).

After writing the file, show the user the complete document and ask if anything needs adjustment.

**Done when:** `reddit-promotion.md` has been created or updated at the selected path, the full plan has been shown, and the user has a clear adjustment prompt.

---

## Template Structure

Use [`template.md`](template.md) as the single source of truth for the generated `reddit-promotion.md` structure.

---

## Copy Guidelines
```

(Copy Guidelines body unchanged.)

- [ ] **Step 4: Re-run the assertion**

Run the same `python3` block from Step 1.

Expected: `PASS`.

- [ ] **Step 5: Commit**

```bash
git add skills/reddit-promotion/template.md skills/reddit-promotion/SKILL.md
git commit -m "Extract reddit-promotion output skeleton to template.md."
```

---

### Task 5: Reshape english-tutor

**Files:**
- Modify: `skills/english-tutor/SKILL.md` (replace file)

**Interfaces:**
- Consumes: spec §4 english-tutor; correction/difficulty/lesson-pattern content from the current file
- Produces: Open / host-each-message / Reference; no `## Quick start`; no `## Session workflow`; no mistake log; version `1.1.0`; description is the spec target wording

- [ ] **Step 1: Write the failing assertion**

```bash
python3 - <<'PY'
from pathlib import Path
t = Path("skills/english-tutor/SKILL.md").read_text()
failed = False
def need(cond, msg):
    global failed
    if not cond:
        print("FAIL:", msg)
        failed = True
need("## Quick start" not in t, "Quick start still present")
need("## Session workflow" not in t, "Session workflow still present")
need("### 1. Open" in t, "missing Open")
need("### 2. Host each user message" in t, "missing host-each-message")
need("| Correction |" in t and "| Clean |" in t and "| Recap |" in t, "missing branch table")
need("conversation practice with grammar correction" in t, "description not tightened")
need("mistake log" not in t.lower(), "mistake log appeared")
if failed:
    raise SystemExit(1)
print("PASS")
PY
```

Expected: FAIL (`Quick start still present`, `missing Open`, description not tightened).

- [ ] **Step 2: Replace `skills/english-tutor/SKILL.md` with this file**

```markdown
---
name: english-tutor
description: "English dialogue tutor. Use when the user wants English conversation practice with grammar correction. For collocations-only drills, use `english-collocations`."
metadata:
  version: 1.1.0
---

# English Tutor

Host English **dialogue** with **one grammar focus** per round. Default: speak mostly in English. Chinese only for brief clarification when the learner is stuck or asks.

Narrow: spoken/written English through dialogue, not a full curriculum or exam prep.

## Steps

### 1. Open

Greet in English. Ask one short level question (comfort speaking, A–D, or a sentence about their week). Set sentence length and vocabulary. Pick **exactly one** grammar focus, or take the learner's. Micro-explain the rule in at most 4 sentences. Start a role (friend, colleague) with one prompt that forces the focus.

**Done when:** level, one focus, and the first dialogue prompt are in the chat.

### 2. Host each user message

Classify the message, then take exactly one branch:

| Branch | When | Action |
|--------|------|--------|
| Recap | 6–10 exchanges done, or the focus sounds natural, or the learner asks to wrap up | Bullet: focus practiced, 1–2 repeated fixes, 2–3 correct model lines. Invite a new round if they want another topic. |
| Correction | The last line has an error (grammar, word choice, unnatural phrase, wrong collocation) | **Correct version:** one or two tight options → **Why (short):** … → one retry instruction ("Say that again" / "Type the full corrected sentence"). No second task in that message. |
| Clean | No error | One reaction or follow-up question that keeps the focus. |

If Recap and Correction both seem to apply, Correction wins when the last line is still wrong; Recap after that line is clean.

**Done when:** Recap has closed the round, or Correction/Clean has replied and is waiting.

## Reference

### Correction format

The correction reply contains only: **Correct version** → **Why (short)** → one retry instruction. After a clean retry, the next turn may ask one natural dialogue question.

### Difficulty

- **Struggling:** shorter prompts; offer a choice of two completions once, then a full sentence alone next turn.
- **Comfortable:** longer turns; mix two related points only after the first is stable.
- Keep the focus until they produce it without copying a model sentence in the same message.

### Lesson patterns (likes/dislikes + really / quite)

**Pattern A — Like/dislike + noun or -ing**
- "I'm **into** jazz." / "I **enjoy** **going** to museums."
- "I'm **not interested in** politics." / "I **don't like** **waiting** in long lines."

**Pattern B — `really`**
- Stronger like: "I **really love** chocolate."
- Softer dislike: "I'm **not really into** opera."

**Pattern C — `quite` (positive only; not with love/hate)**
- OK: "I **quite like** watching documentaries."
- Prefer **really** or a rephrase for negatives at this level.

**Sample loop**
You: "Are you into podcasts?"
Them: [errors] → you: **Correct version** + **Why** + "Say that again."
Them: [clean retry] → you: "What kind? Do you listen while you commute?"

## Boundaries

- No walls of grammar tables. No 20-item quizzes unless the learner asks.
- One primary grammar focus per round.
- New topic → new round with a new focus and a fresh recap at the end.
- Collocations-only drills → `english-collocations`.
- Structured study of a non-English subject → `deep-learner`.
```

- [ ] **Step 3: Re-run the assertion**

Run the same `python3` block from Step 1.

Expected: `PASS`.

- [ ] **Step 4: Commit**

```bash
git add skills/english-tutor/SKILL.md
git commit -m "Reshape english-tutor to Open, host-each-message, Reference."
```

---

### Task 6: Rewrite evals

**Files:**
- Modify: `evals/trigger-cases.md` (replace file)

**Interfaces:**
- Consumes: spec §3; current prompts; Behavioral names `gerrit review`, `zh-en-gloss density`, `microsaas own-product`
- Produces: unique sequential trigger numbers starting at 1; rows for `thirty-seconds`, `reddit-promotion`, direct `english-tutor`; Gerrit review rows cite Behavioral — gerrit review; 13e becomes the own-product trigger citing Behavioral; named Behavioral section at the end

- [ ] **Step 1: Write the failing assertion**

```bash
python3 - <<'PY'
from pathlib import Path
import re
t = Path("evals/trigger-cases.md").read_text()
failed = False
def need(cond, msg):
    global failed
    if not cond:
        print("FAIL:", msg)
        failed = True
need("`thirty-seconds`" in t, "missing thirty-seconds")
need("`reddit-promotion`" in t, "missing reddit-promotion")
need("Correct my grammar while we chat about my weekend" in t, "missing direct english-tutor prompt")
need("## Behavioral" in t, "missing Behavioral section")
need("Behavioral — gerrit review" in t, "missing gerrit review name")
need("Behavioral — zh-en-gloss density" in t, "missing gloss density name")
need("Behavioral — microsaas own-product" in t, "missing microsaas name")
need("13b" not in t, "letter suffixes remain")
nums = [int(m) for m in re.findall(r'^\| (\d+) \|', t, re.M)]
need(nums == list(range(1, len(nums)+1)), f"numbering {nums}")
need("Review pass (cases" not in t, "old Review pass heading remains")
if failed:
    raise SystemExit(1)
print("PASS", "rows", len(nums))
PY
```

Expected: FAIL (missing thirty-seconds, reddit-promotion, Behavioral, and numbering has 12 after 8 plus 13b).

- [ ] **Step 2: Replace `evals/trigger-cases.md` with this file**

```markdown
# Trigger eval cases

Manual trigger tests for skill routing and activation. Run each prompt with the full skill set installed; record pass/fail against the pass criterion.

## Router

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 1 | 练英语 | `english-practice` | Agent names a target skill and hands off without teaching |
| 2 | 英文单词接龙 | `word-chain` | Agent opens a word-chain game with a word card |
| 3 | 成语接龙 | `idiom-chain` | Agent asks which rule (A/B/C) before playing |
| 4 | 帮我背诗词 | `poetry-quiz` | Agent starts a poetry fill-in-the-blank quiz |
| 5 | I want to practice English conversation | `english-practice` → `english-tutor` | Router hands off to `english-tutor` |
| 6 | Correct my grammar while we chat about my weekend | `english-tutor` | Agent greets in English, sets a grammar focus, and starts dialogue (does not load `english-practice`) |

## English drills

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 7 | 练固定搭配 | `english-collocations` | Agent presents a scenario with target collocations |
| 8 | 最小对立对 | `minimal-pairs` | Agent presents a minimal pair contrast round |
| 9 | Help me fix my Chinglish collocations | `english-collocations` | Agent uses the 6-section grading template on first submission |

## Subject tutoring

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 10 | 我想系统学量子力学 | `deep-learner` | Agent opens with greeting and asks for topic or presents diagnostic questions |

## Games

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 11 | 生成30秒卡片 | `thirty-seconds` | Agent asks 中文词条 vs English terms if unset, or generates describer + answer-key cards |

## Product / launch

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 12 | 导出今天 PH top | `producthunt-top` | Agent hands off auth/transport to `producthunt` and runs or offers to run `fetch_top.py` |
| 13 | 用 GraphQL 查这个 PH 产品的 makers | `producthunt` | Agent checks `PRODUCT_HUNT_TOKEN` and runs or offers to run `query.py` with a custom query |
| 14 | 今天 PH 有哪些 MicroSaaS 机会 | `microsaas-opportunity` | Agent gathers via `producthunt-top` JSON (count 8), selects up to 4, and emits opportunity blocks — not a second 8-item leaderboard |
| 15 | 分析这个产品做 MicroSaaS https://linear.app | `microsaas-opportunity` | Agent fetches the named site (not the local repo) and fills the five-part report |
| 16 | 帮我分析我自己的产品做 MicroSaaS | `microsaas-opportunity` | Meets Behavioral — microsaas own-product |
| 17 | 写 Product Hunt 文案 | `launch-kit` | Agent scans codebase or asks for product info before drafting; does not load `producthunt` |
| 18 | Turn this repo into interview prep | `resume-project-prep` | Agent asks target level, then scans codebase |
| 19 | 帮我找 Reddit 上能推广这个产品的帖子 | `reddit-promotion` | Agent scans product context or asks; uses Reddit MCP or reports it missing; does not draft `launch-kit` copy as the main deliverable |

## Traffic / analytics

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 20 | 看下最近三个月 GSC 流量 | `google-traffic` | Verify MCP → resolve scope → pull GSC data |
| 21 | GA4 各渠道会话占比 | `google-traffic` | Calls `run_report` with channel dimension |
| 22 | 帮我检查这几个 URL 有没有被索引 | `google-traffic` | Uses `batch_url_inspection` with explicit urls |

## Gerrit (user-invoked)

`gerrit` has `disable-model-invocation: true` — load only when the user attaches `@gerrit` / `/gerrit` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 23 | `@gerrit inbox` | `gerrit` | Resolves env from repo, runs inbox preset queries, table output |
| 24 | `@gerrit diff 46568` | `gerrit` | Fetches change ref, shows diff |
| 25 | `@gerrit what CLI commands are available?` | `gerrit` | Runs `gerrit`, summarizes subcommands |
| 26 | `/gerrit review 46568 +1` | `gerrit` | Meets Behavioral — gerrit review; dry-run shows `gerrit review --project <project> refs/changes/68/46568/<PS> --code-review +1` |
| 27 | show my open gerrit changes (no `@gerrit`) | none | Skill does not load unless user also attached `gerrit` |
| 28 | `@gerrit 把待我 review 的都加一` | `gerrit` | Meets Behavioral — gerrit review; inbox query first; one dry-run line per pending change |
| 29 | `@gerrit review 46568 +1 LGTM` | `gerrit` | Meets Behavioral — gerrit review; dry-run includes `--message "LGTM"` |
| 30 | `@gerrit review 46568,2 +2 --submit` | `gerrit` | Meets Behavioral — gerrit review; target is `refs/changes/68/46568/2`; +2/submit confirmed |

## GitHub CLI (user-invoked)

`gh` has `disable-model-invocation: true` — load only when the user attaches `@gh` / `/gh` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 31 | `@gh pr list` | `gh` | `command -v gh` → `gh auth status` → `gh pr list --json ... \| jq` → table |
| 32 | `@gh what commands are available?` | `gh` | Runs `gh`, summarizes subcommands; no fabricated static list |
| 33 | `@gh merge PR 42` | `gh` | Dry-runs `gh pr merge`; waits for confirmation |
| 34 | list my open PRs (no `@gh`) | none | Skill does not load unless user also attached `gh` |

## Chinese gloss (user-invoked)

`zh-en-gloss` has `disable-model-invocation: true` — load only when the user attaches `@zh-en-gloss` / `/zh-en-gloss` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 35 | `@zh-en-gloss 什么是缓存穿透？` | `zh-en-gloss` | Chinese prose with inline `词 (English)` glosses in each section |
| 36 | (zh-en-gloss installed) 什么是缓存穿透？ (no @) | none | Skill does not load; reply has no inline glosses |
| 37 | (@english-tutor active) Tell me about your weekend | none | Reply is English dialogue with no inline Chinese glosses |

## Behavioral

Manual. Check every box. Trigger rows cite these by name; they do not restate the lists.

### Behavioral — gerrit review

Only home for review-pass rules. Used by trigger rows 26, 28, 29, 30.

- [ ] Target resolves to `refs/changes/{last-two}/{N}/{PS}` via query `.currentPatchSet.ref`, construction, or user input
- [ ] Dry-run before SSH
- [ ] Dry-run command contains `--project <project>` before that change ref
- [ ] `--message` omitted unless the user supplied cover text

### Behavioral — zh-en-gloss density

Prompt: `@zh-en-gloss 分别解释缓存穿透、缓存击穿和缓存雪崩，分三节说明`

- [ ] Each paragraph or `###` section has 3–6 `词 (English)` glosses
- [ ] The last sections meet the same quota (no taper)
- [ ] No glosses inside code blocks

Trigger rows 36–37 stay negative cases; they are not this checklist.

### Behavioral — microsaas own-product

Prompt: `帮我分析我自己的产品做 MicroSaaS` (trigger row 16)

- [ ] Agent states this skill scores other people's products
- [ ] Does not score the local repo as a competitor
- [ ] May point at `launch-kit` for copy

## Updating

Add a row when introducing a new skill or changing a description pointer. Remove or revise rows when behavior changes. New catalog skills must appear in the Expected skill column so `scripts/check-catalog.sh` passes.
```

Note: row 37 Expected skill is `none` (backticked), not the old unquoted `No gloss`, so the catalog parser ignores it.

- [ ] **Step 3: Re-run the assertion**

Run the same `python3` block from Step 1.

Expected: `PASS` and `rows 37`.

- [ ] **Step 4: Commit**

```bash
git add evals/trigger-cases.md
git commit -m "Renumber evals and add behavioral checklists."
```

---

### Task 7: README, AGENTS, catalog green

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `scripts/check-catalog.sh` from Task 1; evals from Task 6 (already lists `thirty-seconds` and `reddit-promotion`)
- Produces: catalog check exit 0; shared check exit 0

- [ ] **Step 1: Run catalog check (still red on README/AGENTS)**

Run: `bash scripts/check-catalog.sh ; echo EXIT:$?`

Expected: exit 1 with `MISSING readme-install: gerrit gh`, `MISSING readme-table: gerrit gh`, `MISSING agents-clusters: thirty-seconds`. Evals should no longer be missing if Task 6 landed.

- [ ] **Step 2: Update README install list**

In `## Quick Install`, after the `thirty-seconds` line, add:

```bash
npx skills add shfshanyue/skills --skill gerrit
npx skills add shfshanyue/skills --skill gh
```

- [ ] **Step 3: Update README skills table**

After the `thirty-seconds` row, add:

```markdown
| [`gerrit`](skills/gerrit/SKILL.md) | Gerrit SSH query/diff/review via `@gerrit` / `/gerrit` |
| [`gh`](skills/gh/SKILL.md) | GitHub CLI via `@gh` / `/gh` |
```

Change the `reddit-promotion` one-liner to:

```markdown
| [`reddit-promotion`](skills/reddit-promotion/SKILL.md) | Reddit subreddit/post discovery and outreach plan (Reddit MCP) |
```

- [ ] **Step 4: Update README project structure tree**

Inside the `skills/` tree, add `gerrit/` and `gh/` (alongside the other skill dirs). Keep `_shared/` first. Example insertion after `english-tutor/`:

```
│   ├── gerrit/
│   ├── gh/
```

Do not add evals or scripts as user install steps.

- [ ] **Step 5: Update AGENTS.md**

**Steps — adding or editing a skill** — insert as new item 6 (after Environment):

```markdown
6. **Catalog:** README skills table + `--skill` install line, AGENTS skill clusters row, and an evals Expected skill cell
```

Done when line becomes:

```markdown
**Done when:** frontmatter, steps with Done when, boundaries, version bump, and catalog membership are all present.
```

**Reference — description pointers** — add:

```markdown
- User-invoked skills (`disable-model-invocation`) use the same `Use when` profile; `@name` / `/name` is the trigger
```

**Reference — skill clusters** — add a row (with the other games):

```markdown
| Offline 30 Seconds / 30秒卡片 | `thirty-seconds` |
```

**Reference — exemplar skills** — extend the disclosed-template bullet:

```markdown
- **Disclosed template:** [`skills/launch-kit/SKILL.md`](skills/launch-kit/SKILL.md) → `template.md`; [`skills/reddit-promotion/SKILL.md`](skills/reddit-promotion/SKILL.md) → `template.md`; [`skills/microsaas-opportunity/SKILL.md`](skills/microsaas-opportunity/SKILL.md) → `analysis.md` + `report.md`
```

**Reference — CI** — replace the paragraph with:

```markdown
[`.github/workflows/check-shared.yml`](.github/workflows/check-shared.yml): runs [`scripts/check-shared.sh`](scripts/check-shared.sh) then [`scripts/check-catalog.sh`](scripts/check-catalog.sh). Run both locally before pushing.
```

**Reference — evals** — keep the existing sentence; the new evals file already tells maintainers to add a catalog row.

- [ ] **Step 6: Run both checks**

```bash
bash scripts/check-shared.sh
bash scripts/check-catalog.sh
bash scripts/test-check-catalog.sh
```

Expected:

- `All shared file copies are in sync.`
- `All catalog sources match skills/.`
- `test-check-catalog: all passed`

If catalog still reports EXTRA/MISSING, fix the parse window (wrong heading, table link format) or the missing row — do not hard-code skill names in the checker.

Also:

```bash
grep -R 'seo-geo' skills/google-traffic && echo FAIL || echo PASS no seo-geo
```

Expected: `PASS no seo-geo`.

- [ ] **Step 7: Commit**

```bash
git add README.md AGENTS.md
git commit -m "List every skill in README and AGENTS catalog sources."
```

---

## Self-review (author)

**Spec coverage**

| Spec section | Task |
|--------------|------|
| §2 checker + four parse windows + no description lint | Task 1 |
| §2 CI both scripts, filename kept | Task 1 |
| §3 trigger completeness, renumber, negative rows | Task 6 |
| §3 three named Behavioral checklists | Task 6 |
| §4 descriptions gerrit/gh/zh-en-gloss/thirty-seconds/english-tutor | Tasks 2, 5 |
| §4 google-traffic drop seo-geo | Task 3 |
| §4 reddit-promotion template | Task 4 |
| §4 english-tutor reshape, no mistake log | Task 5 |
| §5 README gerrit/gh, Reddit MCP, tree | Task 7 |
| §5 AGENTS clusters, catalog step, Use when for @, CI | Task 7 |
| §6 order: checker first (red), bodies, evals, indexes, green | Tasks 1→7 |
| §7 done when | Task 7 Step 6 |

**Not in this plan (spec out of scope):** catalog generator, description CI lint, splitting evals, adding seo-geo, tutor examples.md, gerrit/gh workflow changes.
