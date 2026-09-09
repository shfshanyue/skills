# Skill groups — Design Doc

Date: 2026-09-09
Status: Approved (brainstorm phase) → ready for implementation plan
Runtime skills live in `skills/<group>/<name>/SKILL.md`. This spec is not a runtime pointer.

Supersedes the catalog layout in [`2026-09-08-skills-maintenance-design.md`](2026-09-08-skills-maintenance-design.md) (`skills/<name>/SKILL.md`). Do not rewrite that spec. Membership, descriptions, evals, and “no generated catalog” still stand.

---

## 1. Purpose

Make the 19-skill pack scannable and installable by audience, without changing skill identity.

Today README is one table, AGENTS clusters is a flat routing table, and `skills/` is a flat directory. Users cannot install “just the language skills” except by listing every `--skill` name.

### Locked decisions

| Topic | Choice |
|-------|--------|
| Groups | Three directories: `language`, `product`, `cli` |
| Membership | Directory membership is grouping. No catalog file, no group `SKILL.md`, no group README |
| Identity | `name`, `--skill <name>`, and `@gerrit` / `@gh` / `@zh-en-gloss` stay unchanged |
| Group install | Source subpath: `npx skills add shfshanyue/skills/skills/<group>`. Not `--skill <group>` (CLI matches skill `name` only) |
| Approach | `git mv` + update README / AGENTS / evals / checkers. No generated catalog |
| Runtime install layout | Still flat by `name` (agent skills dir). Grouping exists only in this repo and in the group-install subpath |

### Out of scope

- Renaming skills or changing `@` / `/` invocation
- Group-level routers, group `SKILL.md`, group README, generated catalog
- Splitting the pack, changing hooks, moving `_shared` into a group
- Rewriting historical specs or plans
- Description lint, Done-when lint, eval numbering checks
- Checking README project-structure tree or `@` wording in CI

---

## 2. Layout and identity

A catalog skill is a directory `skills/<group>/<name>/` that contains `SKILL.md`.

- `<group>` is `language`, `product`, or `cli`
- `<name>` matches frontmatter `name` (unchanged)
- Exclude any path whose first component under `skills/` is `_shared`
- Do not treat `skills/<group>/SKILL.md` as a skill. A `SKILL.md` at that depth is an error (CLI would shadow nested skills)

`skills/_shared/` stays at the top of `skills/`. It is not a group.

### Membership

```
skills/
  _shared/
  language/
    english-practice/
    english-tutor/
    english-collocations/
    minimal-pairs/
    zh-en-gloss/
    word-chain/
    idiom-chain/
    poetry-quiz/
    thirty-seconds/
    deep-learner/
  product/
    launch-kit/
    reddit-promotion/
    producthunt/
    producthunt-top/
    microsaas-opportunity/
    google-traffic/
    resume-project-prep/
  cli/
    gerrit/
    gh/
```

Move with `git mv` so history follows the directories. Skill-internal relative links (`template.md`, `drill-loop-core.md`, `scripts/`) move with the folder and do not change.

Names stay globally unique. Install and evals key off `name`, not path.

### Install

```bash
# All
npx skills add shfshanyue/skills

# One group (subpath)
npx skills add shfshanyue/skills/skills/language
npx skills add shfshanyue/skills/skills/product
npx skills add shfshanyue/skills/skills/cli

# One skill (name unchanged)
npx skills add shfshanyue/skills --skill english-tutor
```

README Quick Install uses that order: all → group subpaths → per-skill `--skill` lines (grouped with comments). Order is a README convention, not a checker rule.

---

## 3. Catalog surfaces

Four required appearances per skill **name** remain. Paths and headings gain the group.

### README

**Quick Install** (`## Quick Install` until the next `##`):

- One all-skills line: `npx skills add shfshanyue/skills` (no `--skill`, ignored for name membership)
- One group line per group directory: `npx skills add shfshanyue/skills/skills/<group>`
- One `--skill <name>` line per catalog skill

**Skills** (`## Skills` until the next `##`, including `###` subsections):

Three subsections: `### Language`, `### Product`, `### CLI`. Each is a table. A skill row is a markdown link of the form:

`` [`name`](skills/<group>/<name>/SKILL.md) ``

The file must exist. The last path component must equal `name`.

**Project Structure** tree lists `_shared/` plus the three groups. CI does not parse this tree.

### AGENTS.md

**Adding or editing a skill — Catalog step:** put the skill in `skills/<group>/<name>/`, then add the README group table row, the `--skill` line, the matching clusters sub-table row, and an evals Expected skill cell.

**Runtime pointer:** shipped behavior lives in `skills/<group>/<name>/SKILL.md`.

**Reference — skill clusters** stays one `##` section until the next `##`. Split into three sub-tables (`### Language` / `### Product` / `### CLI`). Columns stay `User intent | Skill`. The checker still takes the first backtick-quoted `name` in the Skill column of each table row.

**Shared files table:** copy paths become `language/english-collocations/drill-loop-core.md`, `language/minimal-pairs/drill-loop-core.md`, `language/idiom-chain/plain-text-line.md`, `language/poetry-quiz/plain-text-line.md`. Canonical paths stay `skills/_shared/…`.

**Exemplar links** update to the nested paths.

### evals

Keep `evals/trigger-cases.md` as one file. Do not merge tables, renumber, or change pass criteria.

Add `## Language`, `## Product`, and `## CLI`. Demote the current thematic `##` headings to `###` under those groups. Do not merge tables.

| New `##` | Current headings (become `###`) |
|----------|----------------------------------|
| Language | Router, English drills, Subject tutoring, Games, Chinese gloss (user-invoked) |
| Product | Product / launch, Traffic / analytics |
| CLI | Gerrit (user-invoked), GitHub CLI (user-invoked) |

`## Behavioral` stays a top-level heading at the end of the file. The checker still reads only the Expected skill column.

---

## 4. Checkers

### `check-catalog.sh`

Filesystem set: `skills/*/*/SKILL.md`, skip `_shared`. Derive names from the directory that contains `SKILL.md`, not from a hard-coded list.

**Shallow skill:** if any `skills/*/SKILL.md` exists, fail (print the path). This is in addition to the name diffs.

**Name membership** (same four diffs as today: missing vs extra):

| Source | Parse window | What counts |
|--------|----------------|-------------|
| README skills table | `## Skills` until the next `##` | Link `` [`name`](skills/<group>/<name>/SKILL.md) `` whose target file exists and whose last path component equals `name` |
| README install | `## Quick Install` until the next `##` | `--skill name` on an `npx skills add` line. The all-skills line is ignored |
| AGENTS clusters | `## Reference — skill clusters` until the next `##` | First backtick-quoted `name` in the Skill column of each table row |
| evals | `evals/trigger-cases.md` tables, Expected skill column | Every backtick-quoted `name` matching `^[a-z0-9-]+$`. Skip `none` |

A README table link that uses a stale flat path (`skills/name/SKILL.md`) or a wrong group does not count as an appearance (missing) and is not silently accepted.

**Group install:** derive groups as the unique first path component of catalog skills. Quick Install must contain, for each group, a line matching `shfshanyue/skills/skills/<group>` (extract `skills/skills/<token>` and take `<token>`). Extra or missing group tokens fail. Do not treat `npx skills add shfshanyue/skills` as a group.

On mismatch, print skill or group name, which source, and missing vs extra (or the shallow path). Exit non-zero. On full match, one-line success, exit 0.

Do not check description wording, Done when, eval numbering, H3 titles, Quick Install line order, or the project-structure tree.

### `check-shared.sh`

Same four `diff` pairs; destinations move under `skills/language/…`.

### `test-check-catalog.sh`

Fixture layout becomes two levels (`skills/g1/alpha`, `skills/g2/beta`) with matching README links, group subpaths, AGENTS sub-tables, and evals.

Keep today’s cases (complete fixture, missing table row, extra evals name, `none` is not a skill). Add:

- A `skills/shadow/SKILL.md` (shallow) fails
- A table link `skills/alpha/SKILL.md` (flat / wrong path) fails
- A missing `skills/skills/<group>` subpath fails

CI workflow `.github/workflows/check-shared.yml` is unchanged: `check-shared.sh` then `check-catalog.sh`. The fixture script stays local-only.

---

## 5. Skill bodies and scripts

Installed skills remain flat by `name`. Do not rewrite skill prose to `skills/<group>/…` paths; those paths exist only in this repo.

### `mistakes.md`

`skills/_shared/drill-loop.md` already says the log lives in the same folder as `SKILL.md`. In `english-collocations/SKILL.md` and `minimal-pairs/SKILL.md`, replace every hard-coded `skills/<name>/mistakes.md` path with that rule. Sync copies of the shared file are unchanged except for their filesystem path after `git mv`.

Bump `metadata.version` on those two skills. Other skills are `git mv` only — no version bump.

Existing user logs under the installed flat directory keep working because the install layout does not change.

### `producthunt-top` transport

`fetch_top.py` resolves `parents[2] / "producthunt" / "scripts"`:

- In this repo after the move, `parents[2]` is `skills/product/`
- After CLI install, `parents[2]` is the agent skills root (flat)

Leave the lookup. Change the error string from `expected sibling skills/producthunt` to sibling `producthunt` skill, and keep the `--skill producthunt` install hint.

Run `python3 skills/product/producthunt/scripts/test_query.py` and `python3 skills/product/producthunt-top/scripts/test_fetch_top.py` after the move.

### Historical specs

Leave `docs/superpowers/specs/` and `docs/superpowers/plans/` on old paths. They are not runtime pointers.

---

## 6. Verification

After implementation, all of these must pass:

```bash
bash scripts/check-shared.sh
bash scripts/check-catalog.sh
bash scripts/test-check-catalog.sh
python3 skills/product/producthunt/scripts/test_query.py
python3 skills/product/producthunt-top/scripts/test_fetch_top.py
```

Done when: every catalog skill lives at `skills/<group>/<name>/SKILL.md`, README / AGENTS / evals / checkers agree, group subpath install lines exist, no shallow `SKILL.md`, and the commands above exit 0.
