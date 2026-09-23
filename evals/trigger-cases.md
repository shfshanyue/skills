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

### Dictionary

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 45 | 查一下 act 这个词 | `word-lookup` | Agent emits an H1 `act` lookup card with H2 headings 词性 through 其他义项; related-word lists are one item per line with IPA |
| 46 | 查单词 | `word-lookup` | Agent asks for the lemma once; does not open word-chain or a collocation drill |
| 47 | 查一下 make up one's mind 这个短语 | `word-lookup` | H1 is the full phrase; 词性 is a phrase-level label (e.g. idiom); 简单例句 uses the whole phrase; does not split into a card for `make` only |

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
| 18 | Turn this repo into interview prep | `resume-project-prep` | Agent asks target level, then scans codebase; `source-compare` does not load |
| 19 | 帮我找 Reddit 上能推广这个产品的帖子 | `reddit-promotion` | Agent scans product context or asks; uses Reddit MCP or reports it missing; does not draft `launch-kit` copy as the main deliverable |

### Traffic / analytics

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 20 | 看下最近三个月 GSC 流量 | `google-traffic` | Verify MCP → resolve scope → pull GSC data |
| 21 | GA4 各渠道会话占比 | `google-traffic` | Calls `run_report` with channel dimension |
| 22 | 帮我检查这几个 URL 有没有被索引 | `google-traffic` | Uses `batch_url_inspection` with explicit urls |

## Productivity

### Work goal brief (user-invoked)

`workstream-digest` has `disable-model-invocation: true` — load only when the user attaches `@workstream-digest` / `/workstream-digest` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 48 | `@workstream-digest period=week` | `workstream-digest` | Brief has five sections per `report-skeleton.md`; P0/P1/P2/搁置 buckets; claims cite `path:line` or state 未见近期证据 with gap |
| 49 | `@workstream-digest period=now tone=soft` | `workstream-digest` | Shorter window; **今天** next steps; mismatch wording gentler but still names goals |
| 50 | 帮我写个工作周报 (no `@workstream-digest`) | none | Skill does not load unless user attached or named `workstream-digest` |

## CLI

### Gerrit (user-invoked)

`gerrit` has `disable-model-invocation: true` — load only when the user attaches `@gerrit` / `/gerrit` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 23 | `@gerrit inbox` | `gerrit` | Resolves env from repo, runs inbox preset queries, table output |
| 24 | `@gerrit diff 46568` | `gerrit` | Fetches change ref, shows diff |
| 25 | `@gerrit what CLI commands are available?` | `gerrit` | Runs `gerrit`, summarizes subcommands |
| 26 | `/gerrit review 46568 +1` | `gerrit` | Meets Behavioral — gerrit review; dry-run shows `gerrit review --project <project> 46568,<PS> --code-review +1` |
| 27 | show my open gerrit changes (no `@gerrit`) | none | Skill does not load unless user also attached `gerrit` |
| 28 | `@gerrit 把待我 review 的都加一` | `gerrit` | Meets Behavioral — gerrit review; inbox query first; one dry-run line per pending change |
| 29 | `@gerrit review 46568 +1 LGTM` | `gerrit` | Meets Behavioral — gerrit review; dry-run includes `--message "LGTM"` |
| 30 | `@gerrit review 46568,2 +2 --submit` | `gerrit` | Meets Behavioral — gerrit review; target is `46568,2`; +2/submit confirmed |

### GitHub CLI (user-invoked)

`gh` has `disable-model-invocation: true` — load only when the user attaches `@gh` / `/gh` or names the skill explicitly.

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 31 | `@gh pr list` | `gh` | `command -v gh` → `gh auth status` → `gh pr list --json ... \| jq` → table |
| 32 | `@gh what commands are available?` | `gh` | Runs `gh`, summarizes subcommands; no fabricated static list |
| 33 | `@gh merge PR 42` | `gh` | Dry-runs `gh pr merge`; waits for confirmation |
| 34 | list my open PRs (no `@gh`) | none | Skill does not load unless user also attached `gh` |

## Dev

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 38 | grok-build 和 deepseek-harness 里 web fetch 是怎么实现的？ | `source-compare` | Resolves two named trees; meets Behavioral — source-compare answer |
| 39 | 对照两边的 tool calling (project root has `.compare-source/corpus.md`) | `source-compare` | Uses corpus tree names as the search set; meets Behavioral — source-compare answer |
| 40 | 对照两边的 tool calling (no `.compare-source/`) | `source-compare` | Compare-intent branch loads; agent asks which directories; meets Behavioral — source-compare answer |
| 41 | 这段代码的 fetch 怎么写的 (no names, no compare intent) | none | Does not load `source-compare` |
| 42 | grok-build 和 vercel-ai-sdk 里 Agent loop 怎么实现的？ (corpus trees: grok-build, deepseek-harness; ref: vercel-ai-sdk) | `source-compare` | Search set is grok-build + vercel-ai-sdk; deepseek-harness stays out; meets Behavioral — source-compare answer |
| 43 | 对照两边的 tool calling (corpus has two trees + `# refs`) | `source-compare` | Search set is the two trees only; unnamed refs stay out; meets Behavioral — source-compare answer |
| 44 | 这个依赖的源码在 /Users/you/code/source/ai，去看它的 Agent loop | `source-compare` | Treats that path as the search set; offers to append `# refs`; meets Behavioral — source-compare answer |

## Behavioral

Manual. Check every box. Trigger rows cite these by name; they do not restate the lists.

### Behavioral — gerrit review

Only home for review-pass rules. Used by trigger rows 26, 28, 29, 30.

- [ ] Target resolves to `N,PS` via user `N,PS` or query `"\(.number),\(.currentPatchSet.number)"`
- [ ] Dry-run before SSH
- [ ] Dry-run command contains `--project <project>` before that `N,PS` target
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

### Behavioral — source-compare answer

Only home for grounding and resolve rules. Used by trigger rows 38, 39, 40, 42, 43, 44. Do not score answer formatting.

- [ ] Comparison axis is known before search (from the question, or the agent asked)
- [ ] Search set is named trees or refs when names are present, otherwise corpus tree names (not `# refs`), or the agent asked which directories
- [ ] Unnamed refs stay out of the search set (including package names found in code)
- [ ] If `corpus.md` was missing and tree paths were resolved, the agent asked once whether to write it; wrote only on yes
- [ ] If this run resolved a new ref, the agent asked once whether to append `# refs`; appended only on yes; did not rewrite existing lines
- [ ] Corpus-filled sets larger than 4 were narrowed by asking
- [ ] Each tree is an existing directory, or the agent asked for the missing path and waited
- [ ] Every tree in the search set is accounted for in the answer
- [ ] Every positive claim cites a path inside that tree
- [ ] Not-found is explicit; no invented files
- [ ] No writes in the trees or in `.compare-source/` (unless the user accepted the save offer)

## Updating

Add a row when introducing a new skill or changing a description pointer. Remove or revise rows when behavior changes. New catalog skills must appear in the Expected skill column so `scripts/check-catalog.sh` passes.
