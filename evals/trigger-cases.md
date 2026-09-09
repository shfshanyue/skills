# Trigger eval cases

Manual trigger tests for skill routing and activation. Run each prompt with the full skill set installed; record pass/fail against the pass criterion.

## Language

### Router

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 1 | 练英语 | `english-practice` | Agent names a target skill and hands off without teaching |
| 2 | 英文单词接龙 | `word-chain` | Agent opens a word-chain game with a word card |
| 3 | 成语接龙 | `idiom-chain` | Agent asks which rule (A/B/C) before playing |
| 4 | 帮我背诗词 | `poetry-quiz` | Agent starts a poetry fill-in-the-blank quiz |
| 5 | I want to practice English conversation | `english-practice` → `english-tutor` | Router hands off to `english-tutor` |
| 6 | Correct my grammar while we chat about my weekend | `english-tutor` | Agent greets in English, sets a grammar focus, and starts dialogue (does not load `english-practice`) |

### English drills

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 7 | 练固定搭配 | `english-collocations` | Agent presents a scenario with target collocations |
| 8 | 最小对立对 | `minimal-pairs` | Agent presents a minimal pair contrast round |
| 9 | Help me fix my Chinglish collocations | `english-collocations` | Agent uses the 6-section grading template on first submission |

### Subject tutoring

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 10 | 我想系统学量子力学 | `deep-learner` | Agent opens with greeting and asks for topic or presents diagnostic questions |

### Games

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 11 | 生成30秒卡片 | `thirty-seconds` | Agent asks 中文词条 vs English terms if unset, or generates describer + answer-key cards |

### Chinese gloss (user-invoked)

`zh-en-gloss` has `disable-model-invocation: true` — load only when the user attaches `@zh-en-gloss` / `/zh-en-gloss` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 35 | `@zh-en-gloss 什么是缓存穿透？` | `zh-en-gloss` | Chinese prose with inline `词 (English)` glosses in each section |
| 36 | (zh-en-gloss installed) 什么是缓存穿透？ (no @) | none | Skill does not load; reply has no inline glosses |
| 37 | (@english-tutor active) Tell me about your weekend | none | Reply is English dialogue with no inline Chinese glosses |

## Product

### Product / launch

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

### Traffic / analytics

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 20 | 看下最近三个月 GSC 流量 | `google-traffic` | Verify MCP → resolve scope → pull GSC data |
| 21 | GA4 各渠道会话占比 | `google-traffic` | Calls `run_report` with channel dimension |
| 22 | 帮我检查这几个 URL 有没有被索引 | `google-traffic` | Uses `batch_url_inspection` with explicit urls |

## CLI

### Gerrit (user-invoked)

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

### GitHub CLI (user-invoked)

`gh` has `disable-model-invocation: true` — load only when the user attaches `@gh` / `/gh` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 31 | `@gh pr list` | `gh` | `command -v gh` → `gh auth status` → `gh pr list --json ... \| jq` → table |
| 32 | `@gh what commands are available?` | `gh` | Runs `gh`, summarizes subcommands; no fabricated static list |
| 33 | `@gh merge PR 42` | `gh` | Dry-runs `gh pr merge`; waits for confirmation |
| 34 | list my open PRs (no `@gh`) | none | Skill does not load unless user also attached `gh` |

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
