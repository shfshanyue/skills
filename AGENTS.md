# AGENTS.md

Conventions for maintaining this skills repository.

## Steps — adding or editing a skill

1. **Frontmatter:** `name`, `description` (≤2 sentences; one trigger per branch; leading word first), `metadata.version` (bump on change)
2. **Workflow:** ordered steps; each step ends with **Done when** (checkable, exhaustive bound)
3. **Hierarchy:** inline steps + in-file reference; push long reference behind a pointer file in the same folder
4. **Boundaries:** one-line hand-off when another skill owns adjacent work
5. **Environment:** do not cache script flags, directory layout, or `--help` output — point at the source
6. **Catalog:** put the skill in `skills/<group>/<name>/`, then add the README group table row, the `--skill` install line, the matching clusters sub-table row, and an evals Expected skill cell

**Done when:** frontmatter, steps with Done when, boundaries, version bump, and catalog membership are all present.

## Reference — description pointers

- Start with a **leading word** (host, router, drill, planner, …)
- One English trigger per branch; Chinese game skills may add one Chinese trigger
- Route to sibling skills in the description tail, not in a paragraph of synonyms
- User-invoked skills (`disable-model-invocation`) use the same `Use when` profile; `@name` / `/name` is the trigger

## Reference — completion criteria

Use **Done when** on every workflow step. Avoid fuzzy bounds ("understanding reached").

## Reference — shared files

| Canonical | Sync copies to |
|-----------|----------------|
| [`skills/_shared/drill-loop.md`](skills/_shared/drill-loop.md) | `language/english-collocations/drill-loop-core.md`, `language/minimal-pairs/drill-loop-core.md` |
| [`skills/_shared/plain-text-line.md`](skills/_shared/plain-text-line.md) | `language/idiom-chain/plain-text-line.md`, `language/poetry-quiz/plain-text-line.md` |

After editing a canonical file, update all copies in the same commit.

## Reference — design specs

[`docs/superpowers/specs/`](docs/superpowers/specs/) are pre-ship specs. **Do not** point runtime skills at them. Shipped behavior lives in `skills/<group>/<name>/SKILL.md`.

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

### Dev

| User intent | Skill |
|-------------|-------|
| Learn a feature across local source trees | `source-compare` |

## Reference — hooks

[`hooks.json`](hooks.json) + [`hooks/block-git-commit-push.sh`](hooks/block-git-commit-push.sh): `beforeShellExecution` prompts for user approval before `git commit` or `git push` in the agent shell.

## Reference — evals

[`evals/trigger-cases.md`](evals/trigger-cases.md): trigger test cases for routing and activation. Update when adding or changing skill descriptions.

## Reference — CI

[`.github/workflows/check-shared.yml`](.github/workflows/check-shared.yml): runs [`scripts/check-shared.sh`](scripts/check-shared.sh) then [`scripts/check-catalog.sh`](scripts/check-catalog.sh). Run both locally before pushing.

## Reference — exemplar skills

- **Steps + Done when + leading words:** [`skills/language/word-chain/SKILL.md`](skills/language/word-chain/SKILL.md)
- **Disclosed template:** [`skills/product/launch-kit/SKILL.md`](skills/product/launch-kit/SKILL.md) → `template.md`; [`skills/product/reddit-promotion/SKILL.md`](skills/product/reddit-promotion/SKILL.md) → `template.md`; [`skills/product/microsaas-opportunity/SKILL.md`](skills/product/microsaas-opportunity/SKILL.md) → `analysis.md` + `report.md`
- **Script as source of truth:** [`skills/product/producthunt/SKILL.md`](skills/product/producthunt/SKILL.md) → `scripts/query.py`; [`skills/product/producthunt-top/SKILL.md`](skills/product/producthunt-top/SKILL.md) → `scripts/fetch_top.py` (transport via `producthunt`)
