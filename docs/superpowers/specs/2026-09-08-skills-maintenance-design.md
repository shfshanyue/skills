# Skills maintenance — Design Doc

Date: 2026-09-08
Status: Approved (brainstorm phase) → ready for implementation plan
Runtime skills stay in `skills/<name>/SKILL.md`. This spec is not a runtime pointer.

---

## 1. Purpose

Stop catalog drift, make descriptions trigger the same way, and close the eval/CI gaps that let new skills ship without README / AGENTS / evals rows.

This is a maintenance pass on the existing pack. It does not add skills, split the pack, or introduce an eval harness.

### Locked decisions

| Topic | Choice |
|-------|--------|
| Packaging | One installable pack. Every skill is listed in README, AGENTS clusters, and evals. `gerrit` / `gh` stay user-invoked (`@` / `/`); README says so. |
| Descriptions | One profile for all skills, including `disable-model-invocation`: leading word + `Use when` + one trigger per branch. Chinese game skills may add one Chinese trigger. |
| Evals | Complete trigger table + three manual behavioral checklists. No runner, no subagent harness. |
| `reddit-promotion` / `english-tutor` | Extract `reddit-promotion/template.md`; tighten tutor steps to `word-chain` density. No tutor mistake log. |
| `seo-geo` | Delete every pointer. `google-traffic` does not name it. |
| CI | Catalog membership + existing shared-file sync. No description lint, no Done-when lint, no eval numbering check. |
| Approach | Incremental: `check-catalog.sh` + in-place file edits. No generated catalog. Evals stay in one file. |

### Out of scope

- Generating README or AGENTS tables from a catalog file
- Description-quality heuristics in CI
- Splitting `evals/trigger-cases.md`
- Adding `seo-geo` to this repo
- Tutor mistake log / `examples.md`
- New game skills, pack-level router
- Changing `gerrit` / `gh` CLI workflows
- Checking the README directory tree or `@` wording in CI

---

## 2. Catalog checker

### Skill set

A catalog skill is a directory `skills/<name>/` that contains `SKILL.md`, excluding `skills/_shared/`.

Current set (19):

`deep-learner`, `english-collocations`, `english-practice`, `english-tutor`, `gerrit`, `gh`, `google-traffic`, `idiom-chain`, `launch-kit`, `microsaas-opportunity`, `minimal-pairs`, `poetry-quiz`, `producthunt`, `producthunt-top`, `reddit-promotion`, `resume-project-prep`, `thirty-seconds`, `word-chain`, `zh-en-gloss`

The script must derive this set from the filesystem, not from a hard-coded list.

### Four required appearances

Each catalog name must appear in all four places. Names found in those places that are not catalog skills fail (extra). `none` in evals is not a skill name.

| Source | Parse window | What counts as an appearance |
|--------|----------------|------------------------------|
| README skills table | `## Skills` until the next `##` | Markdown link `` [`name`](skills/name/SKILL.md) `` |
| README install commands | `## Quick Install` until the next `##` | `--skill name` on an `npx skills add` line. The all-skills line (`npx skills add shfshanyue/skills` with no `--skill`) is ignored. |
| AGENTS clusters | `## Reference — skill clusters` until the next `##` | First backtick-quoted `name` in the Skill column of each table row |
| evals | `evals/trigger-cases.md` tables, **Expected skill** column | Every backtick-quoted `name` matching `^[a-z0-9-]+$`. A cell `english-practice` → `english-tutor` covers both. Skip the token `none`. |

Do not parse the README project-structure tree, AGENTS exemplar lists, or evals prose outside the Expected skill column.

### Behavior

New script: `scripts/check-catalog.sh`.

- Compare the filesystem set to each of the four extracted sets.
- On mismatch, print skill name, which source, and missing vs extra. Exit non-zero.
- On match, print a one-line success and exit 0.
- Do not check description wording, Done when, eval numbering, or `@` invocation copy.

Keep `scripts/check-shared.sh` unchanged.

### CI

`.github/workflows/check-shared.yml` stays that filename. The job runs both scripts, in order:

1. `bash scripts/check-shared.sh`
2. `bash scripts/check-catalog.sh`

Local: same two commands. AGENTS.md CI section documents both.

---

## 3. Evals

Single file: `evals/trigger-cases.md`. Still manual. Header still says to run each prompt with the full skill set installed.

### Trigger table

- Every catalog skill has at least one row whose Expected skill column contains `` `name` ``.
- Add rows that are missing today:
  - `thirty-seconds` — e.g. `生成30秒卡片` / `30 Seconds cards` → opens card generation (asks language if unset, or generates).
  - `reddit-promotion` — e.g. find Reddit posts to promote this product → scans product context or asks; uses Reddit MCP or reports it missing. Does not draft launch-kit copy as the main deliverable.
  - Direct `english-tutor` — a conversation/grammar-practice prompt that is already specific (not vague `练英语`). Expected skill is `english-tutor` only (not via the router). Keep existing case `练英语` → `english-practice` and `I want to practice English conversation` → `english-practice` → `english-tutor`.
- Renumber the whole file to unique sequential integers starting at 1. No `13b` suffixes. No reused numbers across Gerrit and GitHub sections. Group headings stay.
- Keep negative rows (no `@gerrit` / `@gh` / `@zh-en-gloss` → skill does not load). Those rows use `none` and do not satisfy catalog membership for any skill.
- Gerrit trigger rows that currently inline the review-pass rules instead say “Meets Behavioral — gerrit review”. They do not restate the checklist. Behavioral cases are named, not numbered in the trigger sequence.

### Behavioral section (end of the same file)

Three cases. Each has a prompt and a checkbox list. Human records pass/fail against every box.

**1. `gerrit` review** — this is the only home for the current “Review pass” rules.

- Resolve target to `refs/changes/{last-two}/{N}/{PS}` via query `.currentPatchSet.ref`, construction, or user input.
- Dry-run before SSH.
- Dry-run command contains `--project <project>` before that change ref.
- Omit `--message` unless the user supplied cover text.

Existing review prompts (today 22, 24–26) remain trigger rows and point here.

**2. `zh-en-gloss` density**

- Prompt: `@zh-en-gloss 分别解释缓存穿透、缓存击穿和缓存雪崩，分三节说明`
- Each paragraph or `###` section has 3–6 `词 (English)` glosses.
- The last sections meet the same quota (no taper).
- No glosses inside code blocks.
- Existing negative rows (no `@`, or English-tutor dialogue) stay in the trigger table; they are not this behavioral case.

**3. `microsaas-opportunity` does not score the user’s own product**

- Prompt: 帮我分析我自己的产品做 MicroSaaS (today 13e).
- Agent states this skill scores other people’s products.
- Does not score the local repo as a competitor.
- May point at `launch-kit` for copy.

Today’s 13e pass criterion moves here; the trigger row only says “Meets Behavioral — microsaas own-product”.

No eval runner. CI does not execute these cases or check numbering.

---

## 4. Skill bodies

Bump `metadata.version` on every skill whose files change.

### Descriptions — fix only those that fail the shared rules

Rules (also add to AGENTS.md): leading word first; `Use when`; one English trigger per branch; Chinese games may add one Chinese trigger; do not summarize workflow; user-invoked skills use `Use when the user attaches @name or /name …`.

Target wording (edit for house style, keep this meaning):

| Skill | Target description |
|-------|-------------------|
| `gerrit` | Gerrit SSH operator. Use when the user attaches `@gerrit` or `/gerrit` to query, diff, review, or run Gerrit CLI subcommands. |
| `gh` | GitHub CLI operator. Use when the user attaches `@gh` or `/gh` to run `gh` subcommands. |
| `zh-en-gloss` | Gloss formatter. Use when the user attaches `@zh-en-gloss` or `/zh-en-gloss` for inline 词 (English) glosses in Chinese replies. |
| `thirty-seconds` | Thirty Seconds card generator. Use when the user wants 30 Seconds cards or 30秒卡片. |
| `english-tutor` | English dialogue tutor. Use when the user wants English conversation practice with grammar correction. For collocations-only drills, use `english-collocations`. |
| `google-traffic` | Drop the `seo-geo` sentence. Keep the traffic-reporter leading word and the existing GA4/GSC/page/index triggers. |

Leave descriptions that already match the rules. Keep `disable-model-invocation: true` on `gerrit`, `gh`, and `zh-en-gloss`.

### `reddit-promotion`

Mirror `launch-kit`:

- New `skills/reddit-promotion/template.md` is the source of truth for the generated `reddit-promotion.md` skeleton: title, Product Summary, Recommended Subreddits, High-Value Posts, Action Plan (per-post reply + DM), Weekly Search Prompts.
- `SKILL.md` workflow steps stay; Step 5 points at `template.md` instead of inlining the skeleton. Add a one-line “Template Structure” pointer like launch-kit.
- Copy guidelines (lead with value, short, sound like a Reddit user) stay in-file in `SKILL.md`.
- README skills-table row notes that Reddit MCP is required.

### `english-tutor`

Reshape to `word-chain` step density. Do not add a mistake log or `examples.md`.

1. **Open** — greet in English; set level (today’s Step 0); pick exactly one grammar focus; micro-explain in ≤4 sentences; start dialogue. Done when: level, one focus, and the first dialogue prompt are in the chat.
2. **Host each user message** — exactly one branch: **Correction** (error in the last line → correct-version + why + one retry instruction, no follow-up question); **Clean** (no error → one dialogue follow-up); **Recap** (after 6–10 exchanges or when the pattern is stable → recap + 2–3 model lines). Done when: the chosen branch has replied and is waiting, or Recap has closed the round.
3. **Reference** — correction format, difficulty adaptation, likes/dislikes + really/quite examples (today’s lesson patterns). Merge today’s Quick start into Open; delete the duplicate Session workflow list.

Boundaries stay: not a full curriculum; collocations → `english-collocations`; structured non-English topics → `deep-learner`.

### `google-traffic`

Remove `seo-geo` from description, intro, report hand-off, and Boundaries. On-page title/meta/schema/JSON-LD is out of scope, stated without naming another skill. Project SEO scripts still belong to the consuming repo’s `AGENTS.md`.

Do not change `gerrit` / `gh` command workflows, game rules, or other skills’ step structure.

---

## 5. README and AGENTS.md

### README

- Quick Install: add `--skill gerrit` and `--skill gh` (and any other catalog skill missing from that list).
- Skills table: add `gerrit` and `gh` with one-liners that include `@gerrit` / `@gh`. `zh-en-gloss` already notes `@zh-en-gloss`.
- `reddit-promotion` one-liner: mention Reddit MCP.
- Project structure tree: add `gerrit/` and `gh/` (manual; not CI).
- Do not document evals or check scripts as user install steps.

### AGENTS.md

- Skill clusters: add `thirty-seconds` (offline 30 Seconds / 30秒卡片).
- Adding-or-editing steps: new skill must appear in README table + install command, AGENTS cluster, and evals (the human-readable form of the catalog check).
- Description pointers: user-invoked skills use the same `Use when` profile; `@name` / `/name` is the trigger.
- CI: run `scripts/check-shared.sh` and `scripts/check-catalog.sh`.

---

## 6. Implementation order

1. Add `scripts/check-catalog.sh` and wire it into `.github/workflows/check-shared.yml`. Confirm it fails on current `main` (README missing `gerrit`/`gh`; AGENTS/evals missing `thirty-seconds`; evals missing `reddit-promotion`).
2. Edit skill bodies (descriptions, `reddit-promotion` template, `english-tutor`, `google-traffic`).
3. Rewrite `evals/trigger-cases.md` (renumber, new trigger rows, Behavioral section).
4. Update README and AGENTS.md.
5. Re-run both check scripts until they pass.

Behavioral evals are written in step 3; they are not automated in step 5.

---

## 7. Testing / done when

- `bash scripts/check-shared.sh` exits 0.
- `bash scripts/check-catalog.sh` exits 0 on the finished tree; fails if any of the 19 names is removed from any of the four sources.
- Every catalog skill is listed in README install + table, AGENTS clusters, and evals Expected skill.
- The six descriptions in §4 match the shared rules; `google-traffic` does not contain `seo-geo`.
- `reddit-promotion/template.md` exists and `SKILL.md` does not duplicate the output skeleton.
- `english-tutor` has Open / host-each-message / Reference, not two overlapping workflows.
- `evals/trigger-cases.md` has unique sequential numbering, the three new trigger rows, and a Behavioral section with the three checklists.
