# Review reference

Post scores and comments via SSH:

```bash
ssh -p <port> <user>@<host> gerrit review <CHANGE,PATCHSET> [options]
```

Run `ssh -p <port> <user>@<host> gerrit review --help` on the target server for the current flag list.

---

## Workflow

### Step 1 — Resolve target

The position argument is a **target**: `CHANGE,PATCHSET` (e.g. `46568,1`) or a full commit hash. A bare change number is not a valid target — Gerrit treats it as a commit abbreviation (real case: `46568` matched `scanform-web #10310` commit `46568ec9...`).

1. User gave `CHANGE,PATCHSET` (e.g. `46568,2`) → use it.
2. Otherwise query:

```bash
ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set "change:<N>"
```

Take `currentPatchSet.number` as `<PS>`; target is `<N>,<PS>`.

3. Confirm query `project` matches the project resolved from the current repo ([`query-reference.md`](query-reference.md#env)). On mismatch, stop and report.

**Done when:** target is `<N>,<PS>` and project is verified, or failure is reported.

### Step 2 — Dry-run

Show the full SSH command (target + flags). Omit `--message` unless the user supplied cover text.

- Batch review: one command per change, each with `,<PS>`.
- A score request (`+1`, `加一`) is **not** execute-now; only explicit confirmation (`run it`, `go ahead`, `execute`) skips dry-run.

Example dry-run output (no cover text):

```
Would run:
  ssh -p 29418 user@gerrit.example.com gerrit review 46568,1 \
    --code-review +1
```

**Done when:** command is shown and awaiting confirmation, or user explicitly said execute-now.

### Step 3 — Execute

SSH the command. Report success or stderr. Offer the Gerrit change URL.

**Done when:** success or SSH error is explained.

---

## Common flags

| Flag | Example |
|------|---------|
| `--code-review` | `--code-review +1`, `--code-review +2`, `--code-review -1` |
| `--verified` | `--verified +1`, `--verified -1` |
| `--message` | `--message "LGTM"` (only when user supplied cover text) |
| `--submit` | Submit after approvals (requires permission) |
| `--abandon` | Abandon the change |

Combine flags in one invocation:

```bash
ssh -p <port> <user>@<host> gerrit review 46568,1 \
  --code-review +2 \
  --message "Approved" \
  --submit
```

## Parsing user intent

| User says | Map to |
|-----------|--------|
| `+1`, `CR+1`, `code-review +1`, `加一` | `--code-review +1` (no message) |
| `+2`, `CR+2`, `approve` | `--code-review +2` |
| `verified +1`, `V+1` | `--verified +1` |
| `LGTM` with no score | `--code-review +1` with `--message "LGTM"` |
| `submit` | Add `--submit` only if labels already satisfied; warn if not |

## Guards

- **+2 / submit** — confirm explicitly; these are high impact.
- **-1 / abandon** — confirm and require a message explaining why.
- Do not echo SSH credentials or private keys.

## After execution

Report success or the SSH stderr. Offer the Gerrit change URL for verification in the web UI.
