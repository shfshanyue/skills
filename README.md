# shanyue-skills

`shanyue-skills` is a small skills-and-hooks repository for Cursor-based agent workflows.

It currently contains:
- A reusable skill for generating launch copy assets.
- Shell execution hooks that enforce safe Git behavior in the agent shell.

## Project Structure

- `launch-kit/` — skill definition for launch copy generation.
- `hooks/` — hook scripts used by Cursor before shell execution.

## Skills

### `launch-kit`

File: `launch-kit/SKILL.md`

Purpose:

- Generates a unified `launch-kit.md` with copy for Product Hunt, Hacker News, Indie Hackers, software directories, and similar launch channels.
- Scans project files (like `README.md`, package metadata, and product pages) to infer product context.
- Produces multiple copy variants (taglines, one-liners, short/medium descriptions) plus feature lists, categories, social proof, and platform-ready snippets.
- Writes output to an existing `launch-kit.md` when present, or creates `docs/launch-kit.md`.

## Hooks

### `block-git-commit-push.sh`

File: `hooks/block-git-commit-push.sh`

Purpose:
- A stricter command parser for `beforeShellExecution`.
- Allows most commands, but blocks `git commit` and `git push` 
- Returns structured JSON with `permission: "deny"` and guidance for running commit/push locally.

## Why These Hooks Exist

These hooks help keep risky Git write operations out of the agent shell and force final repository-changing actions to happen in the user's own system terminal.

## Quick Setup

1. Keep this repo available to your Cursor environment.
2. Reference `launch-kit/SKILL.md` when you want launch copy generation behavior.
3. Register hook scripts in your Cursor hooks configuration (`beforeShellExecution`) as needed.

## Notes

- Current skill count: **1**
- Current hook script count: **2**
- This README documents the repository as it exists now; update it if you add more skills or hooks.
