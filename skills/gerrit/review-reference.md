# Review reference

Post scores and comments via SSH:

```bash
ssh -p <port> <user>@<host> gerrit review <change-number> [options]
```

Run `ssh -p <port> <user>@<host> gerrit review --help` on the target server for the current flag list.

## Dry-run (default)

**Always dry-run first** unless the user explicitly says to execute now (e.g. "run it", "go ahead", "execute").

Show the exact command that would run, including `--message` text, and wait for confirmation before SSH.

Example dry-run output:

```
Would run:
  ssh -p 29418 user@gerrit.example.com gerrit review 46568 \
    --code-review +1 \
    --message "LGTM, spec looks comprehensive"
```

## Common flags

| Flag | Example |
|------|---------|
| `--code-review` | `--code-review +1`, `--code-review +2`, `--code-review -1` |
| `--verified` | `--verified +1`, `--verified -1` |
| `--message` | `--message "LGTM"` |
| `--submit` | Submit after approvals (requires permission) |
| `--abandon` | Abandon the change |

Combine flags in one invocation:

```bash
ssh -p <port> <user>@<host> gerrit review 46568 \
  --code-review +2 \
  --message "Approved" \
  --submit
```

## Parsing user intent

| User says | Map to |
|-----------|--------|
| `+1`, `CR+1`, `code-review +1` | `--code-review +1` |
| `+2`, `CR+2`, `approve` | `--code-review +2` |
| `verified +1`, `V+1` | `--verified +1` |
| `LGTM` with no score | Ask score or default `--code-review +1` with message |
| `submit` | Add `--submit` only if labels already satisfied; warn if not |

## Guards

- **+2 / submit** — confirm explicitly; these are high impact.
- **-1 / abandon** — confirm and require a message explaining why.
- Do not echo SSH credentials or private keys.

## After execution

Report success or the SSH stderr. Offer the Gerrit change URL for verification in the web UI.
