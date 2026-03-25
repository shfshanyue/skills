# shanyue-skills

A collection of agent skills and hooks for Amp/Cursor-based workflows.

## Quick Install

Install any skill with one command:

```bash
# Install a single skill
npx skills add shfshanyue/skills/launch-kit
npx skills add shfshanyue/skills/reddit-promotion

# Install all skills
npx skills add shfshanyue/skills
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

## Hooks

### `block-git-commit-push.sh`

> `hooks/block-git-commit-push.sh`

A command parser for `beforeShellExecution` that blocks `git commit` and `git push` in the agent shell, forcing these operations to happen in the user's own terminal.

## Project Structure

```
├── skills/
│   ├── launch-kit/          # Launch copy generation skill
│   │   └── SKILL.md
│   └── reddit-promotion/    # Reddit promotion finder skill
│       ├── SKILL.md
│       └── mcp.json
├── hooks/
│   └── block-git-commit-push.sh
├── hooks.json
└── README.md
```
