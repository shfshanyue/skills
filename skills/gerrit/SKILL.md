---
name: gerrit
description: Gerrit SSH operator — query, diff, review, and arbitrary CLI subcommands.
disable-model-invocation: true
metadata:
  version: 1.1.0
---

# Gerrit

Invoke with **`@gerrit`** or **`/gerrit`**, then state what you want — e.g. `inbox`, `diff 46568`, `what CLI commands are available?`, `review 46568 +1`.

Gerrit exposes a **remote CLI over SSH**: `ssh -p <port> <user>@<host> gerrit <subcommand>`. This skill runs those commands from the **current git repo** (must be a Gerrit project). Connection details come from [`.gitreview`](query-reference.md#env) or `git remote`; the live `gerrit` / `gerrit <cmd> --help` output is the source of truth for subcommands and flags.

---

## Workflow

### Step 1 — Resolve environment

Read [`query-reference.md`](query-reference.md#env) and resolve **host**, **port**, **user**, **project** from `.gitreview` or `git remote get-url origin`. Probe with:

```bash
ssh -o ConnectTimeout=10 -o BatchMode=yes -p <port> <user>@<host> gerrit version
```

**Done when:** host, port, user, and project are known, or SSH failure is reported and execution stops.

### Step 2 — Classify branch

Pick exactly one branch from the user's message (after `@gerrit` / `/gerrit`):

| Branch | When |
|--------|------|
| **query** | inbox, dashboard, open changes, pending reviews, or a Gerrit search string |
| **diff** | change number + read or review the patch |
| **review** | score, comment, LGTM, or submit |
| **cli** | explore available subcommands, `--help` for a command, or run any other `gerrit` subcommand |

**Routing defaults:** change number + read code → **diff**; change number + score/submit → **review**; inbox / my changes / pending reviews → **query** (inbox presets); unfamiliar subcommand name → **cli**.

**Done when:** exactly one branch is selected and parameters (change number, query string, labels, subcommand) are known or extracted from the user message.

### Step 3 — Execute branch

- **query** — [`query-reference.md`](query-reference.md): inbox presets (three fixed queries) or custom `gerrit query --format=JSON …`
- **diff** — [`diff-reference.md`](diff-reference.md): metadata query → `git fetch` change ref → `git diff`
- **review** — [`review-reference.md`](review-reference.md): resolve target → dry-run → execute
- **cli** — [`cli-reference.md`](cli-reference.md): **explore** (`gerrit` list + `gerrit <cmd> --help`) or **execute** (help first, then run; mutating commands dry-run)

**Done when:** branch output is complete (table, diff, dry-run proposal, or command output), or failure is explained with the SSH/git error.

### Step 4 — Present

Deliver a concise summary:

- Resolved **host**, **project**, and branch used
- Results (table, diff excerpt, or command output)
- Change URLs: `https://<host>/c/<project>/+/<change-number>`
- For **cli** explore mode: note that naming a subcommand and args will run or dry-run it

**Done when:** results are in the chat.

---

## Boundaries

- Search, inbox, custom `gerrit query` → **query**
- Fetch patch / AI code review on a change → **diff**
- `gerrit review` scores and submit → **review**
- List subcommands, `--help`, `set-reviewers`, `ls-projects`, `stream-events`, admin commands → **cli**
- GitHub PR workflows (`gh pr`) → out of scope
- Gerrit REST API over HTTPS (often needs SSO) → out of scope unless user insists; prefer SSH

---

## Reference — key constraints

- `gerrit query --files` returns file names and line counts only — **not** diff text; use **diff** branch for patches.
- `gerrit query` date filter: `before:` is **exclusive** (day after the inclusive end date).
- Never hardcode host, user, or project — resolve per run from the repo environment.
- **review** branch: resolve **target** (`CHANGE,PATCHSET`) before SSH — see [`review-reference.md`](review-reference.md).
