# shanyue-skills

A collection of agent skills and hooks for Amp/Cursor-based workflows.

## Quick Install

Install any skill with one command:

```bash
# Install a single skill
npx skills add shfshanyue/skills --skill launch-kit
npx skills add shfshanyue/skills --skill reddit-promotion
npx skills add shfshanyue/skills --skill resume-project-prep
npx skills add shfshanyue/skills --skill deep-learner
npx skills add shfshanyue/skills --skill english-practice
npx skills add shfshanyue/skills --skill english-tutor
npx skills add shfshanyue/skills --skill english-collocations
npx skills add shfshanyue/skills --skill minimal-pairs
npx skills add shfshanyue/skills --skill producthunt
npx skills add shfshanyue/skills --skill producthunt-top
npx skills add shfshanyue/skills --skill microsaas-opportunity
npx skills add shfshanyue/skills --skill google-traffic
npx skills add shfshanyue/skills --skill idiom-chain
npx skills add shfshanyue/skills --skill word-chain
npx skills add shfshanyue/skills --skill poetry-quiz
npx skills add shfshanyue/skills --skill zh-en-gloss
npx skills add shfshanyue/skills --skill thirty-seconds
npx skills add shfshanyue/skills --skill gerrit
npx skills add shfshanyue/skills --skill gh

# Install all skills
npx skills add shfshanyue/skills
```

## Skills

| Skill | One-line |
|-------|----------|
| [`launch-kit`](skills/launch-kit/SKILL.md) | Multi-platform product launch copy → `launch-kit.md` |
| [`reddit-promotion`](skills/reddit-promotion/SKILL.md) | Reddit subreddit/post discovery and outreach plan (Reddit MCP) |
| [`resume-project-prep`](skills/resume-project-prep/SKILL.md) | Codebase → interview prep and resume project write-up |
| [`deep-learner`](skills/deep-learner/SKILL.md) | Structured topic tutor with roadmap and Socratic nodes |
| [`english-practice`](skills/english-practice/SKILL.md) | Router — pick the right English practice skill |
| [`english-tutor`](skills/english-tutor/SKILL.md) | English dialogue + grammar correction |
| [`english-collocations`](skills/english-collocations/SKILL.md) | Scenario collocation drills with mistake log |
| [`minimal-pairs`](skills/minimal-pairs/SKILL.md) | Phoneme minimal-pair drills with mistake log |
| [`producthunt`](skills/producthunt/SKILL.md) | Query Product Hunt GraphQL API v2 |
| [`producthunt-top`](skills/producthunt-top/SKILL.md) | Fetch and export Product Hunt top posts |
| [`microsaas-opportunity`](skills/microsaas-opportunity/SKILL.md) | Score a PH list or a named product as a MicroSaaS opening |
| [`google-traffic`](skills/google-traffic/SKILL.md) | GA4 + GSC analytics via MCP (cross-project) |
| [`idiom-chain`](skills/idiom-chain/SKILL.md) | Chinese idiom chain game (成语接龙) |
| [`word-chain`](skills/word-chain/SKILL.md) | English last-letter word chain + word cards |
| [`poetry-quiz`](skills/poetry-quiz/SKILL.md) | Classical Chinese poetry fill-in-the-blank quiz |
| [`zh-en-gloss`](skills/zh-en-gloss/SKILL.md) | Inline English glosses in Chinese replies (`@zh-en-gloss`) |
| [`thirty-seconds`](skills/thirty-seconds/SKILL.md) | Offline 30 Seconds (30秒) board game card generator |
| [`gerrit`](skills/gerrit/SKILL.md) | Gerrit SSH query/diff/review via `@gerrit` / `/gerrit` |
| [`gh`](skills/gh/SKILL.md) | GitHub CLI via `@gh` / `/gh` |

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
│   ├── launch-kit/
│   ├── reddit-promotion/
│   ├── resume-project-prep/
│   ├── deep-learner/
│   ├── english-practice/      # English practice router
│   ├── english-tutor/
│   ├── gerrit/
│   ├── gh/
│   ├── english-collocations/
│   ├── minimal-pairs/
│   ├── producthunt/
│   ├── producthunt-top/
│   ├── microsaas-opportunity/
│   ├── google-traffic/
│   ├── idiom-chain/
│   ├── word-chain/
│   ├── poetry-quiz/
│   ├── zh-en-gloss/
│   └── thirty-seconds/
├── docs/superpowers/specs/    # Pre-ship design docs (not runtime pointers)
├── hooks/
│   └── block-git-commit-push.sh
├── hooks.json
└── README.md
```
