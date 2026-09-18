# shanyue-skills

A collection of agent skills and hooks for Amp/Cursor-based workflows.

## Quick Install

Install any skill with one command:

```bash
# Install all skills
npx skills add shfshanyue/skills

# Install one group
npx skills add shfshanyue/skills/skills/language
npx skills add shfshanyue/skills/skills/product
npx skills add shfshanyue/skills/skills/cli
npx skills add shfshanyue/skills/skills/dev

# Install a single skill
# language
npx skills add shfshanyue/skills --skill english-practice
npx skills add shfshanyue/skills --skill english-tutor
npx skills add shfshanyue/skills --skill english-collocations
npx skills add shfshanyue/skills --skill minimal-pairs
npx skills add shfshanyue/skills --skill zh-en-gloss
npx skills add shfshanyue/skills --skill word-lookup
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
# dev
npx skills add shfshanyue/skills --skill source-compare
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
| [`word-lookup`](skills/language/word-lookup/SKILL.md) | English dictionary lookup card / 查单词 |
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

### Dev

| Skill | One-line |
|-------|----------|
| [`source-compare`](skills/dev/source-compare/SKILL.md) | Learn a feature by comparing implementations across local source trees |

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
│   ├── cli/
│   └── dev/
├── docs/superpowers/specs/    # Pre-ship design docs (not runtime pointers)
├── hooks/
│   └── block-git-commit-push.sh
├── hooks.json
└── README.md
```
