---
name: gh
description: GitHub CLI operator — run `gh` subcommands via `@gh` / `/gh`.
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# GitHub CLI

Invoke with **`@gh`** or **`/gh`**, then state what you want — e.g. `pr list`, `issue view 42`, `what commands are available?`, `merge PR 42`.

All GitHub operations go through **`gh`**. The live `gh` / `gh <cmd> --help` output is the source of truth for subcommands and flags.

---

## Workflow

### Step 1 — Probe environment

Probe in order; **stop on the first failure**:

**1a. `gh` on PATH**

```bash
command -v gh
```

- Missing → stop; say `gh` is not installed; point to https://cli.github.com/
- Present → continue

**1b. Auth**

```bash
gh auth status
```

- Not logged in → stop; suggest `gh auth login` or `GITHUB_TOKEN` / `GH_TOKEN`
- Logged in → continue

**1c. `jq` (only when this turn uses `--json`)**

```bash
command -v jq
```

- Missing → stop; say `jq` is required to trim JSON output safely; point to https://jqlang.org/
- Plain-text output (no `--json`) or explore (`gh --help`) → skip 1c

**1d. Repo context (optional)**

- When the command targets the current repo → `gh repo view --json nameWithOwner,url | jq`
- Pure explore → skip 1d

**Done when:** `gh` is available and authenticated; `jq` is available when `--json` is needed; `owner/repo` is resolved when needed or skip reason is stated.

### Step 2 — Classify intent

| Branch | When | Action |
|--------|------|--------|
| **explore** | what commands exist, how a subcommand works | `gh` or `gh <cmd> --help` |
| **execute** | default; user gave subcommand + args | run `--help` first if unsure, then assemble |

**Done when:** the command to run (or explore target) is determined.

### Step 3 — Execute

- **Read-only** (`list`, `view`, `diff`, `gh api` GET, etc.) → run directly
- **Mutating** (`create`, `merge`, `close`, `delete`, `gh api` POST/PUT/PATCH, etc.) → show the full command and **wait for confirmation** unless the user already said to execute (e.g. "run it", "go ahead")
- **`--json` output** → pipe through `jq`:

```bash
gh pr list --json number,title,url,state | jq '[.[] | {number, title, url, state}]'
gh pr view 42 --json title,url,body | jq '{title, url, body: (.body | .[0:500])}'
```

- Plain-text output (no `--json`) → no `jq`
- Run commands in the shell; never fabricate output

**Done when:** the command has run, a mutating command is dry-run and awaiting confirmation, or a clear error is reported.

### Step 4 — Present

Deliver a concise summary:

- `owner/repo` when applicable
- Key results (table, links, or summary)
- PR/Issue URLs from `jq`-filtered fields; if missing, `gh ... view --json url | jq -r .url`

**Done when:** results are readable in the chat.

---

## Reference

- **Prerequisites** — `command -v gh` before anything else; missing → stop, https://cli.github.com/
- **Auth** — `gh auth status`; never log tokens
- **jq** — before `--json`, `command -v jq`; missing → stop, https://jqlang.org/; do not paste raw JSON blobs into the chat
- **Repo** — default to the current git repo; cross-repo with `-R owner/repo`
- **Explore** — `gh` lists top-level commands; `gh <cmd> --help` for flags; no static command tables in this skill
- **Mutating dry-run** — show the command first; "run it" / "go ahead" counts as confirmation
- **jq hygiene** — lists: `.[] | {fields}`; truncate long text: `.body | .[0:N]`; scalars: `jq -r .field`
