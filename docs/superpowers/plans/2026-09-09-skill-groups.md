# Skill Groups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the 19 skills into `language` / `product` / `cli` group directories, keep skill names, and make README / AGENTS / evals / checkers agree, including per-group install subpaths.

**Architecture:** Directory membership is the group. `check-catalog.sh` scans `skills/<group>/<name>/SKILL.md`, forbids a shallow `skills/*/SKILL.md`, requires nested README links and `skills/skills/<group>` install lines. Docs follow the tree. Skill `name` and `--skill <name>` do not change. No catalog file.

**Tech Stack:** bash, awk, git mv, Markdown skill files, existing Python unittests.

**Spec:** [`docs/superpowers/specs/2026-09-09-skill-groups-design.md`](../specs/2026-09-09-skill-groups-design.md)

## Global Constraints

- Groups are exactly `language`, `product`, `cli`. Membership is the spec tree. `_shared/` stays at `skills/_shared/`.
- `name`, `--skill <name>`, and `@gerrit` / `@gh` / `@zh-en-gloss` stay unchanged.
- Group install is `npx skills add shfshanyue/skills/skills/<group>`, not `--skill <group>`.
- No group `SKILL.md`, no group README, no generated catalog, no group routers.
- Do not rewrite skill prose to `skills/<group>/…` (install layout stays flat by `name`).
- Bump `metadata.version` only on `english-collocations` and `minimal-pairs` (1.3.0 → 1.4.0). Other skills are `git mv` only.
- Do not rewrite historical specs or plans. Do not change hooks or CI workflow filenames.
- After Task 1, do not run `check-catalog.sh` on this repo until Task 3 finishes (fixtures only until then).

## File map

| File | Responsibility |
|------|----------------|
| `scripts/test-check-catalog.sh` | Nested fixtures + shallow / bad-path / missing-group cases |
| `scripts/check-catalog.sh` | Nested scan, shallow fail, nested README links, group-install set |
| `scripts/check-shared.sh` | Diff canonical `_shared/` against copies under `skills/language/` |
| `skills/language/*`, `skills/product/*`, `skills/cli/*` | Relocated skill directories |
| `README.md` | All / group / per-skill install; three skill tables; grouped tree |
| `AGENTS.md` | Catalog step, runtime pointer, three cluster tables, shared + exemplar paths |
| `evals/trigger-cases.md` | `## Language` / `## Product` / `## CLI`; demote thematic headings; move Chinese gloss |
| `skills/language/english-collocations/SKILL.md` | `mistakes.md` location + version 1.4.0 |
| `skills/language/minimal-pairs/SKILL.md` | `mistakes.md` location + version 1.4.0 |
| `skills/product/producthunt-top/scripts/fetch_top.py` | Sibling error string (lookup unchanged) |

---

### Task 1: Nested catalog checker

**Files:**
- Modify: `scripts/test-check-catalog.sh` (replace)
- Modify: `scripts/check-catalog.sh` (replace)

**Interfaces:**
- Consumes: `CHECK_CATALOG_ROOT` (optional); fixture at `skills/<group>/<name>/SKILL.md`; README `## Quick Install` / `## Skills`; AGENTS `## Reference — skill clusters`; `evals/trigger-cases.md` Expected skill column
- Produces: exit 0 iff nested filesystem names match the four catalog sources, no `skills/*/SKILL.md` exists, README table links resolve to real `skills/<group>/<name>/SKILL.md` with matching basename, and Quick Install group tokens match filesystem groups. Prints `MISSING` / `EXTRA` / `SHALLOW skill:` otherwise.

- [ ] **Step 1: Replace `scripts/test-check-catalog.sh` with nested fixtures**

Overwrite the file with:

`````bash
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
  mkdir -p "$dir/skills/g1/alpha" "$dir/skills/g2/beta" "$dir/evals"
  printf '%s\n' '---' 'name: alpha' '---' '# A' > "$dir/skills/g1/alpha/SKILL.md"
  printf '%s\n' '---' 'name: beta' '---' '# B' > "$dir/skills/g2/beta/SKILL.md"
  cat > "$dir/README.md" <<'EOF'
# fixture

## Quick Install

```bash
npx skills add shfshanyue/skills/skills/g1
npx skills add shfshanyue/skills/skills/g2
npx skills add shfshanyue/skills --skill alpha
npx skills add shfshanyue/skills --skill beta
npx skills add shfshanyue/skills
```

## Skills

### Language

| Skill | One-line |
|-------|----------|
| [`alpha`](skills/g1/alpha/SKILL.md) | A |

### Product

| Skill | One-line |
|-------|----------|
| [`beta`](skills/g2/beta/SKILL.md) | B |

## Hooks
EOF
  cat > "$dir/AGENTS.md" <<'EOF'
# AGENTS

## Reference — skill clusters

### Language

| User intent | Skill |
|-------------|-------|
| Alpha work | `alpha` |

### Product

| User intent | Skill |
|-------------|-------|
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
sed -i.bak '/skills\/g2\/beta\/SKILL.md/d' "$FIX/README.md"
assert_exit 1 "missing readme-table" bash "$CHECKER"
assert_grep 'MISSING readme-table:.*beta' "reports missing beta table"
make_fixture "$FIX"

# Extra in evals
printf '%s\n' '| 4 | ghost | `ghost` | no |' >> "$FIX/evals/trigger-cases.md"
assert_exit 1 "extra evals" bash "$CHECKER"
assert_grep 'EXTRA evals:.*ghost' "reports extra ghost"
make_fixture "$FIX"

# Shallow SKILL.md
mkdir -p "$FIX/skills/shadow"
printf '%s\n' '---' 'name: shadow' '---' '# S' > "$FIX/skills/shadow/SKILL.md"
assert_exit 1 "shallow skill" bash "$CHECKER"
assert_grep 'SHALLOW skill:.*skills/shadow/SKILL.md' "reports shallow path"
make_fixture "$FIX"

# Flat / wrong README path
sed -i.bak 's|skills/g1/alpha/SKILL.md|skills/alpha/SKILL.md|' "$FIX/README.md"
assert_exit 1 "flat readme-table path" bash "$CHECKER"
assert_grep 'MISSING readme-table:.*alpha' "flat path does not count"
make_fixture "$FIX"

# Missing group subpath
sed -i.bak '/skills\/skills\/g2/d' "$FIX/README.md"
assert_exit 1 "missing group-install" bash "$CHECKER"
assert_grep 'MISSING group-install:.*g2' "reports missing g2 group"
make_fixture "$FIX"

# none is not a skill
# (already in fixture; complete fixture must still pass — covered above)

if [ "$FAIL" -ne 0 ]; then
  echo "test-check-catalog: FAILED"
  exit 1
fi
echo "test-check-catalog: all passed"
`````

Keep the file executable (`chmod +x` if needed).

- [ ] **Step 2: Run tests against the current checker (expect FAIL)**

Run: `bash scripts/test-check-catalog.sh`

Expected: FAIL. Complete fixture exits non-zero (current checker looks at `skills/*/SKILL.md`, so the nested fixture is empty or mismatched). Do not edit production skills in this step.

- [ ] **Step 3: Replace `scripts/check-catalog.sh`**

Overwrite with:

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

fs_skills() {
  local d name group
  for d in "$ROOT/skills"/*/*/SKILL.md; do
    [ -f "$d" ] || continue
    name="$(basename "$(dirname "$d")")"
    group="$(basename "$(dirname "$(dirname "$d")")")"
    [ "$group" = "_shared" ] && continue
    printf '%s\n' "$name"
  done | sort -u
}

fs_groups() {
  local d group
  for d in "$ROOT/skills"/*/*/SKILL.md; do
    [ -f "$d" ] || continue
    group="$(basename "$(dirname "$(dirname "$d")")")"
    [ "$group" = "_shared" ] && continue
    printf '%s\n' "$group"
  done | sort -u
}

readme_install() {
  section "$ROOT/README.md" "## Quick Install" \
    | { grep -E 'npx skills add' || true; } \
    | { grep -oE -- '--skill[[:space:]]+[a-z0-9-]+' || true; } \
    | awk '{print $2}' \
    | sort -u
}

readme_groups() {
  section "$ROOT/README.md" "## Quick Install" \
    | { grep -oE 'skills/skills/[a-z0-9-]+' || true; } \
    | sed 's|skills/skills/||' \
    | sort -u
}

readme_table() {
  local link name group last
  section "$ROOT/README.md" "## Skills" \
    | { grep -oE '\[`[a-z0-9-]+`\]\(skills/[a-z0-9-]+/[a-z0-9-]+/SKILL\.md\)' || true; } \
    | while IFS= read -r link; do
        [ -n "$link" ] || continue
        name="$(printf '%s\n' "$link" | sed -E 's/\[`([a-z0-9-]+)`\].*/\1/')"
        group="$(printf '%s\n' "$link" | sed -E 's/.*\(skills\/([a-z0-9-]+)\/.*/\1/')"
        last="$(printf '%s\n' "$link" | sed -E 's/.*\/([a-z0-9-]+)\/SKILL\.md\)/\1/')"
        [ "$name" = "$last" ] || continue
        [ -f "$ROOT/skills/$group/$name/SKILL.md" ] || continue
        printf '%s\n' "$name"
      done \
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

RC=0

for d in "$ROOT/skills"/*/SKILL.md; do
  [ -f "$d" ] || continue
  echo "SHALLOW skill: ${d#"$ROOT"/}"
  RC=1
done

fs_skills > "$TMP/fs"
fs_groups > "$TMP/fs-groups"
readme_install > "$TMP/readme-install"
readme_groups > "$TMP/readme-groups"
readme_table > "$TMP/readme-table"
agents_clusters > "$TMP/agents-clusters"
evals_expected > "$TMP/evals"

diff_set "readme-install" "$TMP/readme-install" "$TMP/fs"
diff_set "readme-table" "$TMP/readme-table" "$TMP/fs"
diff_set "agents-clusters" "$TMP/agents-clusters" "$TMP/fs"
diff_set "evals" "$TMP/evals" "$TMP/fs"
diff_set "group-install" "$TMP/readme-groups" "$TMP/fs-groups"

if [ "$RC" -ne 0 ]; then
  exit 1
fi
echo "All catalog sources match skills/."
```

Keep executable.

- [ ] **Step 4: Run fixture tests (expect PASS)**

Run: `bash scripts/test-check-catalog.sh`

Expected: `test-check-catalog: all passed` and every case prints PASS.

Do not run `bash scripts/check-catalog.sh` on this repo yet.

- [ ] **Step 5: Commit**

```bash
git add scripts/test-check-catalog.sh scripts/check-catalog.sh
git commit -m "Scan nested skill groups in the catalog checker."
```

---

### Task 2: Move skill directories

**Files:**
- Move: every `skills/<name>/` except `_shared` into `skills/language/`, `skills/product/`, or `skills/cli/`
- Modify: `scripts/check-shared.sh`

**Interfaces:**
- Consumes: spec membership tree; `git mv`
- Produces: `skills/<group>/<name>/SKILL.md` for all 19 skills; `check-shared.sh` diffs copies under `skills/language/`

- [ ] **Step 1: Create group directories and `git mv`**

```bash
mkdir -p skills/language skills/product skills/cli

git mv skills/english-practice skills/english-tutor skills/english-collocations \
  skills/minimal-pairs skills/zh-en-gloss skills/word-chain skills/idiom-chain \
  skills/poetry-quiz skills/thirty-seconds skills/deep-learner \
  skills/language/

git mv skills/launch-kit skills/reddit-promotion skills/producthunt \
  skills/producthunt-top skills/microsaas-opportunity skills/google-traffic \
  skills/resume-project-prep \
  skills/product/

git mv skills/gerrit skills/gh skills/cli/
```

Leave `skills/_shared/` where it is. Do not add `SKILL.md` or README under the group directories.

- [ ] **Step 2: Confirm the tree**

Run: `find skills -name SKILL.md | sort`

Expected: exactly 19 paths, all `skills/{language,product,cli}/<name>/SKILL.md`. No `skills/*/SKILL.md`. `_shared` has no `SKILL.md`.

- [ ] **Step 3: Point `check-shared.sh` at the new copy paths**

Replace the four `diff` lines with:

```bash
diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/language/english-collocations/drill-loop-core.md"
diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/language/minimal-pairs/drill-loop-core.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/language/idiom-chain/plain-text-line.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/language/poetry-quiz/plain-text-line.md"
```

Leave the shebang, comment, `ROOT=`, and success echo unchanged.

- [ ] **Step 4: Run shared sync and Product Hunt tests**

Run:

```bash
bash scripts/check-shared.sh
python3 skills/product/producthunt/scripts/test_query.py
python3 skills/product/producthunt-top/scripts/test_fetch_top.py
```

Expected: `All shared file copies are in sync.` and both Python files exit 0 (`OK` / `Ran … tests`).

`fetch_top.py` still uses `parents[2] / "producthunt" / "scripts"` — do not change the lookup in this task.

- [ ] **Step 5: Commit**

```bash
git add -A skills scripts/check-shared.sh
git commit -m "Move skills into language, product, and cli groups."
```

---

### Task 3: Catalog surfaces

**Files:**
- Modify: `README.md` (`## Quick Install`, `## Skills`, `## Project Structure`)
- Modify: `AGENTS.md` (catalog step, runtime pointer, shared table, clusters, exemplars)
- Modify: `evals/trigger-cases.md` (group headings; move Chinese gloss under Language)

**Interfaces:**
- Consumes: nested paths from Task 2; checker from Task 1
- Produces: real-repo `bash scripts/check-catalog.sh` exit 0

- [ ] **Step 1: Replace README Quick Install, Skills, and Project Structure**

Replace from `## Quick Install` through the closing fence of Project Structure with:

`````markdown
## Quick Install

Install any skill with one command:

```bash
# Install all skills
npx skills add shfshanyue/skills

# Install one group
npx skills add shfshanyue/skills/skills/language
npx skills add shfshanyue/skills/skills/product
npx skills add shfshanyue/skills/skills/cli

# Install a single skill
# language
npx skills add shfshanyue/skills --skill english-practice
npx skills add shfshanyue/skills --skill english-tutor
npx skills add shfshanyue/skills --skill english-collocations
npx skills add shfshanyue/skills --skill minimal-pairs
npx skills add shfshanyue/skills --skill zh-en-gloss
npx skills add shfshanyue/skills --skill word-chain
npx skills add shfshanyue/skills --skill idiom-chain
npx skills add shfshanyue/skills --skill poetry-quiz
npx skills add shfshanyue/skills --skill thirty-seconds
npx skills add shfshanyue/skills --skill deep-learner
# product
npx skills add shfshanyue/skills --skill launch-kit
npx skills add shfshanyue/skills --skill reddit-promotion
npx skills add shfshanyue/skills --skill producthunt
npx skills add shfshanyue/skills --skill producthunt-top
npx skills add shfshanyue/skills --skill microsaas-opportunity
npx skills add shfshanyue/skills --skill google-traffic
npx skills add shfshanyue/skills --skill resume-project-prep
# cli
npx skills add shfshanyue/skills --skill gerrit
npx skills add shfshanyue/skills --skill gh
```

## Skills

### Language

| Skill | One-line |
|-------|----------|
| [`english-practice`](skills/language/english-practice/SKILL.md) | Router — pick the right English practice skill |
| [`english-tutor`](skills/language/english-tutor/SKILL.md) | English dialogue + grammar correction |
| [`english-collocations`](skills/language/english-collocations/SKILL.md) | Scenario collocation drills with mistake log |
| [`minimal-pairs`](skills/language/minimal-pairs/SKILL.md) | Phoneme minimal-pair drills with mistake log |
| [`zh-en-gloss`](skills/language/zh-en-gloss/SKILL.md) | Inline English glosses in Chinese replies (`@zh-en-gloss`) |
| [`word-chain`](skills/language/word-chain/SKILL.md) | English last-letter word chain + word cards |
| [`idiom-chain`](skills/language/idiom-chain/SKILL.md) | Chinese idiom chain game (成语接龙) |
| [`poetry-quiz`](skills/language/poetry-quiz/SKILL.md) | Classical Chinese poetry fill-in-the-blank quiz |
| [`thirty-seconds`](skills/language/thirty-seconds/SKILL.md) | Offline 30 Seconds (30秒) board game card generator |
| [`deep-learner`](skills/language/deep-learner/SKILL.md) | Structured topic tutor with roadmap and Socratic nodes |

### Product

| Skill | One-line |
|-------|----------|
| [`launch-kit`](skills/product/launch-kit/SKILL.md) | Multi-platform product launch copy → `launch-kit.md` |
| [`reddit-promotion`](skills/product/reddit-promotion/SKILL.md) | Reddit subreddit/post discovery and outreach plan (Reddit MCP) |
| [`resume-project-prep`](skills/product/resume-project-prep/SKILL.md) | Codebase → interview prep and resume project write-up |
| [`producthunt`](skills/product/producthunt/SKILL.md) | Query Product Hunt GraphQL API v2 |
| [`producthunt-top`](skills/product/producthunt-top/SKILL.md) | Fetch and export Product Hunt top posts |
| [`microsaas-opportunity`](skills/product/microsaas-opportunity/SKILL.md) | Score a PH list or a named product as a MicroSaaS opening |
| [`google-traffic`](skills/product/google-traffic/SKILL.md) | GA4 + GSC analytics via MCP (cross-project) |

### CLI

| Skill | One-line |
|-------|----------|
| [`gerrit`](skills/cli/gerrit/SKILL.md) | Gerrit SSH query/diff/review via `@gerrit` / `/gerrit` |
| [`gh`](skills/cli/gh/SKILL.md) | GitHub CLI via `@gh` / `/gh` |

See each skill's `SKILL.md` for full workflow. Maintainers: see [`AGENTS.md`](AGENTS.md).

## Hooks

### [`block-git-commit-push.sh`](hooks/block-git-commit-push.sh)

A command parser for `beforeShellExecution` that prompts for user approval before `git commit` or `git push` in the agent shell (`permission: ask`).

## Project Structure

```
├── AGENTS.md                  # Conventions for maintaining this repo
├── skills/
│   ├── _shared/               # Canonical shared reference (sync to skill copies)
│   │   ├── drill-loop.md
│   │   └── plain-text-line.md
│   ├── language/
│   ├── product/
│   └── cli/
├── docs/superpowers/specs/    # Pre-ship design docs (not runtime pointers)
├── hooks/
│   └── block-git-commit-push.sh
├── hooks.json
└── README.md
```
`````

Keep the `# shanyue-skills` title and intro paragraph above Quick Install. Do not change Hooks body text except that it stays between Skills and Project Structure as shown.

- [ ] **Step 2: Update AGENTS.md catalog, pointer, shared copies, clusters, exemplars**

Catalog step 6 becomes:

```markdown
6. **Catalog:** put the skill in `skills/<group>/<name>/`, then add the README group table row, the `--skill` install line, the matching clusters sub-table row, and an evals Expected skill cell
```

Runtime pointer (design specs section) becomes:

```markdown
[`docs/superpowers/specs/`](docs/superpowers/specs/) are pre-ship specs. **Do not** point runtime skills at them. Shipped behavior lives in `skills/<group>/<name>/SKILL.md`.
```

Shared files table:

```markdown
| Canonical | Sync copies to |
|-----------|----------------|
| [`skills/_shared/drill-loop.md`](skills/_shared/drill-loop.md) | `language/english-collocations/drill-loop-core.md`, `language/minimal-pairs/drill-loop-core.md` |
| [`skills/_shared/plain-text-line.md`](skills/_shared/plain-text-line.md) | `language/idiom-chain/plain-text-line.md`, `language/poetry-quiz/plain-text-line.md` |
```

Replace the single clusters table with:

```markdown
## Reference — skill clusters

### Language

| User intent | Skill |
|-------------|-------|
| Vague "practice English" / 练英语 | `english-practice` (router — hand off, do not teach) |
| English dialogue / grammar chat | `english-tutor` |
| Collocations / Chinglish pairings | `english-collocations` |
| Pronunciation / minimal pairs | `minimal-pairs` |
| Structured topic learning (any subject) | `deep-learner` |
| Inline English glosses in Chinese replies (`@zh-en-gloss`) | `zh-en-gloss` |
| English word chain / 英文单词接龙 | `word-chain` |
| Chinese idiom chain / 成语接龙 | `idiom-chain` |
| Classical poetry quiz / 诗词填空 | `poetry-quiz` |
| Offline 30 Seconds / 30秒卡片 | `thirty-seconds` |

### Product

| User intent | Skill |
|-------------|-------|
| Product launch copy | `launch-kit` |
| Reddit outreach plan | `reddit-promotion` |
| Resume / interview prep from codebase | `resume-project-prep` |
| Product Hunt GraphQL query | `producthunt` |
| Product Hunt top list fetch/export | `producthunt-top` |
| MicroSaaS opportunity (PH list or a named product) | `microsaas-opportunity` |
| Search traffic / GSC / GA4 reports | `google-traffic` |

### CLI

| User intent | Skill |
|-------------|-------|
| Gerrit SSH (`@gerrit` / `/gerrit`) | `gerrit` |
| GitHub CLI (`@gh` / `/gh`) | `gh` |
```

Exemplars:

```markdown
- **Steps + Done when + leading words:** [`skills/language/word-chain/SKILL.md`](skills/language/word-chain/SKILL.md)
- **Disclosed template:** [`skills/product/launch-kit/SKILL.md`](skills/product/launch-kit/SKILL.md) → `template.md`; [`skills/product/reddit-promotion/SKILL.md`](skills/product/reddit-promotion/SKILL.md) → `template.md`; [`skills/product/microsaas-opportunity/SKILL.md`](skills/product/microsaas-opportunity/SKILL.md) → `analysis.md` + `report.md`
- **Script as source of truth:** [`skills/product/producthunt/SKILL.md`](skills/product/producthunt/SKILL.md) → `scripts/query.py`; [`skills/product/producthunt-top/SKILL.md`](skills/product/producthunt-top/SKILL.md) → `scripts/fetch_top.py` (transport via `producthunt`)
```

Do not change description-pointer rules, hooks, evals, or CI sections except as above.

- [ ] **Step 3: Regroup evals headings**

In `evals/trigger-cases.md`, do not merge tables, renumber, or edit pass criteria. Apply these heading edits and one move:

1. Insert `## Language` immediately before the current `## Router`.
2. Rename `## Router` → `### Router`, `## English drills` → `### English drills`, `## Subject tutoring` → `### Subject tutoring`, `## Games` → `### Games`.
3. Cut the whole `## Chinese gloss (user-invoked)` block (the `disable-model-invocation` sentence plus its table, currently after GitHub CLI) and paste it after the Games table. Rename that heading to `### Chinese gloss (user-invoked)`.
4. Insert `## Product` immediately before `## Product / launch`, then rename `## Product / launch` → `### Product / launch` and `## Traffic / analytics` → `### Traffic / analytics`.
5. Insert `## CLI` immediately before `## Gerrit (user-invoked)`, then rename `## Gerrit (user-invoked)` → `### Gerrit (user-invoked)` and `## GitHub CLI (user-invoked)` → `### GitHub CLI (user-invoked)`.
6. Leave `## Behavioral` and `## Updating` as top-level headings.

- [ ] **Step 4: Run the catalog checker on this repo**

Run: `bash scripts/check-catalog.sh`

Expected: `All catalog sources match skills/.` exit 0.

If it prints MISSING/EXTRA, fix the named source; do not weaken the checker.

- [ ] **Step 5: Commit**

```bash
git add README.md AGENTS.md evals/trigger-cases.md
git commit -m "Group README, AGENTS, and evals by language, product, and cli."
```

---

### Task 4: Skill-body paths and verification

**Files:**
- Modify: `skills/language/english-collocations/SKILL.md`
- Modify: `skills/language/minimal-pairs/SKILL.md`
- Modify: `skills/product/producthunt-top/scripts/fetch_top.py`

**Interfaces:**
- Consumes: `skills/_shared/drill-loop.md` location rule (same folder as `SKILL.md`); existing `parents[2]` sibling lookup
- Produces: no `skills/<name>/mistakes.md` strings in those two SKILL.md files; sibling error text without `skills/producthunt`; all spec verification commands exit 0

- [ ] **Step 1: Point collocations `mistakes.md` at the skill folder**

In `skills/language/english-collocations/SKILL.md`:

- `metadata.version: 1.3.0` → `1.4.0`
- Opening paragraph: `persist mistakes to \`skills/english-collocations/mistakes.md\`` → `persist mistakes to \`mistakes.md\` in the same folder as this \`SKILL.md\``
- Drill round: `**mistakes.md path:** \`skills/english-collocations/mistakes.md\`` → `**mistakes.md path:** \`mistakes.md\` next to \`SKILL.md\` (tracked key = collocation phrase)`
- Format section: `Location: \`skills/english-collocations/mistakes.md\`.` → `Location: \`mistakes.md\` in the same folder as this \`SKILL.md\`.`

Do not change `drill-loop-core.md` (already says same folder as SKILL.md).

- [ ] **Step 2: Point minimal-pairs `mistakes.md` at the skill folder**

In `skills/language/minimal-pairs/SKILL.md`:

- `metadata.version: 1.3.0` → `1.4.0`
- Opening paragraph: `persist mistakes to \`skills/minimal-pairs/mistakes.md\`` → `persist mistakes to \`mistakes.md\` in the same folder as this \`SKILL.md\``
- Drill round: `**mistakes.md path:** \`skills/minimal-pairs/mistakes.md\`` → `**mistakes.md path:** \`mistakes.md\` next to \`SKILL.md\` (tracked key = **phoneme contrast**, e.g. \`/l/ vs /r/\`)`
- Format section: `Location: \`skills/minimal-pairs/mistakes.md\`.` → `Location: \`mistakes.md\` in the same folder as this \`SKILL.md\`.`

- [ ] **Step 3: Soften the producthunt-top sibling error**

In `skills/product/producthunt-top/scripts/fetch_top.py`, keep `_producthunt_scripts` lookup. Change only the `SystemExit` text:

```python
        raise SystemExit(
            "producthunt skill not found (expected sibling producthunt skill).\n"
            "Install: npx skills add shfshanyue/skills --skill producthunt"
        )
```

Do not bump `producthunt-top` version.

- [ ] **Step 4: Full verification**

Run:

```bash
bash scripts/check-shared.sh
bash scripts/check-catalog.sh
bash scripts/test-check-catalog.sh
python3 skills/product/producthunt/scripts/test_query.py
python3 skills/product/producthunt-top/scripts/test_fetch_top.py
```

Expected: all exit 0.

Also run:

```bash
rg -n 'skills/(english-collocations|minimal-pairs)/mistakes.md' skills/language
rg -n 'expected sibling skills/producthunt' skills/product/producthunt-top
find skills -name SKILL.md | grep -vE '^skills/(language|product|cli)/[^/]+/SKILL.md$'
```

Expected: no matches from either `rg`; `find | grep` prints nothing.

- [ ] **Step 5: Commit**

```bash
git add skills/language/english-collocations/SKILL.md \
  skills/language/minimal-pairs/SKILL.md \
  skills/product/producthunt-top/scripts/fetch_top.py
git commit -m "Fix mistakes.md and producthunt sibling paths after grouping."
```

---

## Self-review (spec coverage)

| Spec section | Task |
|--------------|------|
| Layout / membership / git mv / no group SKILL.md | Task 2 |
| Install all / group subpath / `--skill` name | Task 3 README |
| README tables + nested links + tree | Task 3 |
| AGENTS catalog step, pointer, clusters, shared, exemplars | Task 3 |
| evals group headings; Chinese gloss under Language; Behavioral top-level | Task 3 |
| check-catalog nested scan, shallow, nested links, group-install | Task 1 |
| check-shared paths | Task 2 |
| test-check-catalog nested + three new cases | Task 1 |
| mistakes.md same-folder; version 1.4.0 | Task 4 |
| producthunt sibling lookup kept, error string | Task 4 |
| Historical specs untouched | (no task — do not edit them) |
| Verification commands | Task 4 Step 4 |
