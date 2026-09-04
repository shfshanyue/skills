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

## English drills

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 6 | 练固定搭配 | `english-collocations` | Agent presents a scenario with target collocations |
| 7 | 最小对立对 | `minimal-pairs` | Agent presents a minimal pair contrast round |
| 8 | Help me fix my Chinglish collocations | `english-collocations` | Agent uses the 6-section grading template on first submission |

## Cross-skill activation

| # | Prompt | Expected behavior | Pass criterion |
|---|--------|-------------------|----------------|
| 9 | (zh-en-gloss installed) 什么是缓存穿透？ | `zh-en-gloss` format | Chinese prose with inline `词 (English)` glosses in each section |
| 10 | (@english-tutor active) Tell me about your weekend | No gloss | Reply is English dialogue with no inline Chinese glosses |
| 11 | 纯中文，不要括号英文 | `zh-en-gloss` opt-out | Subsequent replies have no inline English glosses |

## Subject tutoring

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 12 | 我想系统学量子力学 | `deep-learner` | Agent opens with greeting and asks for topic or presents diagnostic questions |

## Product / launch

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 13 | 导出今天 PH top | `producthunt-top` | Agent checks token and runs or offers to run `fetch_top.py` |
| 14 | 写 Product Hunt 文案 | `launch-kit` | Agent scans codebase or asks for product info before drafting |
| 15 | Turn this repo into interview prep | `resume-project-prep` | Agent asks target level, then scans codebase |

## Traffic / analytics

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 16 | 看下最近三个月 GSC 流量 | `google-traffic` | Verify MCP → resolve scope → pull GSC data |
| 17 | GA4 各渠道会话占比 | `google-traffic` | Calls `run_report` with channel dimension |
| 18 | 帮我检查这几个 URL 有没有被索引 | `google-traffic` | Uses `batch_url_inspection` with explicit urls |

## Gerrit (user-invoked)

`gerrit` has `disable-model-invocation: true` — load only when the user attaches `@gerrit` / `/gerrit` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 19 | `@gerrit inbox` | `gerrit` | Resolves env from repo, runs inbox preset queries, table output |
| 20 | `@gerrit diff 46568` | `gerrit` | Fetches change ref, shows diff |
| 21 | `@gerrit what CLI commands are available?` | `gerrit` | Runs `gerrit`, summarizes subcommands |
| 22 | `/gerrit review 46568 +1` | `gerrit` | Dry-runs `gerrit review` before executing |
| 23 | show my open gerrit changes (no `@gerrit`) | none | Skill does not load unless user also attached `gerrit` |

## GitHub CLI (user-invoked)

`gh` has `disable-model-invocation: true` — load only when the user attaches `@gh` / `/gh` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 24 | `@gh pr list` | `gh` | `command -v gh` → `gh auth status` → `gh pr list --json ... \| jq` → table |
| 25 | `@gh what commands are available?` | `gh` | Runs `gh`, summarizes subcommands; no fabricated static list |
| 26 | `@gh merge PR 42` | `gh` | Dry-runs `gh pr merge`; waits for confirmation |
| 27 | list my open PRs (no `@gh`) | none | Skill does not load unless user also attached `gh` |

## Updating

Add a row when introducing a new skill or changing a description pointer. Remove or revise rows when behavior changes.
