# CLI reference

Catch-all for Gerrit SSH subcommands not covered by **query**, **diff**, or **review**.

The **authoritative command list** is what your account sees at runtime — do not rely on a static list in this file.

## Explore mode

When the user asks what Gerrit can do, which commands exist, or how a subcommand works (without executing a mutating action):

### List subcommands

```bash
ssh -p <port> <user>@<host> gerrit
```

Parse the output for available command names (varies by Gerrit version and account permissions).

### Help for one command

```bash
ssh -p <port> <user>@<host> gerrit <subcommand> --help
```

Present flags and a minimal usage example. Group the subcommand list by purpose when summarizing (developer / admin / meta) — grouping is for readability only.

**Done when:** subcommand list is shown, and any subcommand the user named has a `--help` summary.

## Execute mode

When the user wants to **run** a subcommand (e.g. `set-reviewers`, `ls-projects`, `stream-events`):

1. Run `gerrit <subcommand> --help` first.
2. Assemble the full SSH command from `--help` and user args.
3. Apply mutating rules below.
4. Run and return output (or structured summary for long JSON streams).

## Mutating vs read-only

| Class | Examples | Behavior |
|-------|----------|----------|
| **Read-only** | `version`, `query`, `ls-projects`, `ls-groups`, `show-queue` | Execute directly |
| **Mutating** | `review`, `set-reviewers`, `create-*`, `set-*`, `submit`, `delete-*`, `gc`, `flush-caches` | **Dry-run first** — show command, wait for user confirmation |

`review` has its own branch and rules in [`review-reference.md`](review-reference.md); still use dry-run there.

## Example subcommands (non-exhaustive)

Verified in conversation; your `gerrit` output may differ.

| Subcommand | Typical use |
|------------|-------------|
| `query` | Prefer **query** branch for structured search |
| `review` | Prefer **review** branch for scoring |
| `set-reviewers` | `--add user <change>` / `--remove user <change>` |
| `ls-projects` | List visible projects |
| `ls-groups` | List groups |
| `ls-members` | Members of a group |
| `stream-events` | Long-running JSON event stream (needs `streamEvents` permission) |
| `version` | Server version (also used in env probe) |

### set-reviewers example

```bash
ssh -p <port> <user>@<host> gerrit set-reviewers --add alice 46568
ssh -p <port> <user>@<host> gerrit set-reviewers --remove bob 46568
```

Dry-run before executing.

### stream-events

```bash
ssh -p <port> <user>@<host> gerrit stream-events
```

Runs until interrupted. Warn the user; do not start unless they intend a long-running watch. For a quick capability check, use `--help` only.

## Admin commands

Accounts with admin rights may see `create-project`, `flush-caches`, `gc`, `show-connections`, etc. Same rules: `--help` first, dry-run for mutating ops, confirm destructive actions.

## REST API

Gerrit also exposes HTTPS REST endpoints (`/changes/.../patch`, `/files/.../diff`). Many instances require SSO; **prefer SSH + git fetch** for diffs unless the user has HTTP credentials configured.
