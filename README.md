# shanyue-skills

A collection of agent skills and hooks for Amp/Cursor-based workflows.

## Quick Install

Install any skill with one command:

```bash
# Install a single skill
npx skills add shfshanyue/skills/launch-kit
npx skills add shfshanyue/skills/reddit-promotion
npx skills add shfshanyue/skills/resume-project-prep
npx skills add shfshanyue/skills/deep-learner
npx skills add shfshanyue/skills/english-tutor
npx skills add shfshanyue/skills/producthunt-top
npx skills add shfshanyue/skills/chengyu-jielong
npx skills add shfshanyue/skills/poetry-quiz

# Install all skills
npx skills add shfshanyue/skills
```

## Local Development

All skills are maintained in this repo and symlinked to `~/.agents/skills/` for local testing. Changes take effect immediately without any sync step.

```bash
# Set up symlinks for local development (run once)
ln -sf $(pwd)/skills/launch-kit ~/.agents/skills/launch-kit
ln -sf $(pwd)/skills/reddit-promotion ~/.agents/skills/reddit-promotion
ln -sf $(pwd)/skills/resume-project-prep ~/.agents/skills/resume-project-prep
ln -sf $(pwd)/skills/deep-learner ~/.agents/skills/deep-learner
ln -sf $(pwd)/skills/english-tutor ~/.agents/skills/english-tutor
ln -sf $(pwd)/skills/producthunt-top ~/.agents/skills/producthunt-top
ln -sf $(pwd)/skills/chengyu-jielong ~/.agents/skills/chengyu-jielong
ln -sf $(pwd)/skills/poetry-quiz ~/.agents/skills/poetry-quiz
```

## Skills

### `launch-kit`

> `skills/launch-kit/SKILL.md`

Generates a unified `launch-kit.md` with copy for Product Hunt, Hacker News, Indie Hackers, software directories, and similar launch channels.

- Scans project files (README, package metadata, product pages) to infer product context
- Produces multiple copy variants (taglines, one-liners, short/medium descriptions)
- Generates feature lists, categories, social proof, and platform-ready snippets
- Writes output to an existing `launch-kit.md` or creates `docs/launch-kit.md`

### `reddit-promotion`

> `skills/reddit-promotion/SKILL.md`

Finds relevant Reddit subreddits and posts for product promotion. Powered by [reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy).

- Discovers matching subreddits based on product keywords, pain points, and competitors
- Locates high-value posts (recommendation requests, competitor complaints, pain point discussions)
- Generates reply and DM templates that sound human, not like marketing
- Outputs a complete action plan to `docs/reddit-promotion.md`

### `resume-project-prep`

> `skills/resume-project-prep/SKILL.md`

Scans a project codebase to generate interview preparation materials and resume project descriptions.

- Analyzes tech stack, architecture, and module layout
- Hunts for interview-worthy code (concurrency, caching, design patterns, etc.)
- Generates a polished resume project description and structured Q&A guide
- Supports follow-up Q&A mode with realistic interviewer follow-up questions

### `deep-learner`

> `skills/deep-learner/SKILL.md`

Interactive 1-on-1 tutor: guided questioning, deliberate practice, and roadmap-style progress (Mermaid) for mastering any topic.

- Diagnostic assessment and topic focusing before the learning path
- Per-node Socratic teaching with scoring, weakness analysis, and targeted practice
- Language mirroring (e.g. Chinese/English) and one question per message

### `english-tutor`

> `skills/english-tutor/SKILL.md`

Mixed-mode English practice: one grammar focus per round, short dialogue, immediate correction, adaptive difficulty. Narrower than `deep-learner`—conversation-first English, not general-topic tutoring.

- Mostly-English tutoring with brief Chinese only when needed for clarification
- Correction turns are single-focus (correct version + short why + retry); no extra follow-up question in the same message as a fix
- Recap after a stretch of practice: what you drilled, repeated fixes, and 2–3 reusable model sentences

### `producthunt-top`

> `skills/producthunt-top/SKILL.md`

Fetches top/trending Product Hunt posts via the official GraphQL API v2, and returns ranked results in table/markdown/json/csv formats.

- Supports flexible periods (`today`, `yesterday`, `this_week`, `this_month`, or a specific date)
- Reads `PRODUCT_HUNT_TOKEN` from environment securely (without leaking secrets)
- Supports terminal display and export to Markdown/JSON/CSV files
- Includes practical follow-ups such as trend summaries and period-over-period comparison

### `chengyu-jielong`

> `skills/chengyu-jielong/SKILL.md`

Hosts the classic Chinese idiom chain game (成语接龙) with the user — picks the rule, plays the first idiom, and validates every reply.

- User chooses the chain rule at start (strict same character, same pinyin, or same pinyin + tone)
- AI plays first, every idiom comes with source (出处), meaning (含义), and an example sentence (例句)
- Validates user input: rejects non-idioms and idioms that break the rule, asks for a retry
- Provides on-demand hints (1–2 clues, never the full answer); allows repeated idioms
- Ends and tallies the score (AI vs. user count) only when the user says `结束`

### `poetry-quiz`

> `skills/poetry-quiz/SKILL.md`

Hosts a Chinese classical poetry fill-in-the-blank quiz (诗词上下句填空) — AI always asks, user always answers, with one line of a classical poem as the prompt and the user supplying the matching 上句 / 下句.

- User picks a difficulty at start (简单 / 中等 / 困难); pool covers 唐诗、宋词、元曲、诗经楚辞
- Direction is randomized per question (请接下句 or 请接上句); every prompt shows 题面 / 方向 / 出处
- Friendly correction: real-but-wrong classical lines are acknowledged with their source before asking for a retry
- Ladder hints (主题 → 首字 → 前两字), auto-advanced on wrong answers; never reveals the full answer
- Weighted scoring (2 / 1 / 0 points), couplets deduplicated across directions, never fabricates lines
- Ends with score, per-category accuracy, and study suggestions only when the user says `结束`

## Hooks

### `block-git-commit-push.sh`

> `hooks/block-git-commit-push.sh`

A command parser for `beforeShellExecution` that blocks `git commit` and `git push` in the agent shell, forcing these operations to happen in the user's own terminal.

## Project Structure

```
├── skills/
│   ├── launch-kit/            # Launch copy generation skill
│   │   └── SKILL.md
│   ├── reddit-promotion/      # Reddit promotion finder skill
│   │   ├── SKILL.md
│   │   └── mcp.json
│   ├── resume-project-prep/   # Interview prep skill
│       └── SKILL.md
│   ├── deep-learner/          # Interactive tutor (guided learning) skill
│   │   └── SKILL.md
│   ├── english-tutor/         # English conversation + grammar practice skill
│   │   └── SKILL.md
│   ├── producthunt-top/       # Product Hunt top/trending posts fetcher
│   │   └── SKILL.md
│   ├── chengyu-jielong/       # Chinese idiom chain game (成语接龙) host
│   │   └── SKILL.md
│   └── poetry-quiz/           # Chinese classical poetry fill-in-the-blank quiz host
│       └── SKILL.md
├── hooks/
│   └── block-git-commit-push.sh
├── hooks.json
└── README.md
```

