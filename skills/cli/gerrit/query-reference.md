# Query reference

## env

Resolve connection variables from the **current git repository** (run from repo root).

### From `.gitreview`

If `.gitreview` exists:

```ini
[gerrit]
host=gerrit.example.com
port=29418
project=my-project
```

Use `host`, `port`, and `project` from the `[gerrit]` section.

### From `git remote`

SSH user from `origin`:

```bash
git remote get-url origin
# ssh://USER@HOST:PORT/PROJECT
```

Parse with:

```bash
REMOTE=$(git remote get-url origin)
USER=$(echo "$REMOTE" | sed -n 's#ssh://\([^@]*\)@.*#\1#p')
HOST=$(echo "$REMOTE" | sed -n 's#ssh://[^@]*@\([^:]*\):.*#\1#p')
PORT=$(echo "$REMOTE" | sed -n 's#ssh://[^@]*@[^:]*:\([0-9]*\)/.*#\1#p')
PROJECT=$(echo "$REMOTE" | sed -n 's#ssh://[^@]*@[^:]*:[0-9]*/\(.*\)#\1#p')
```

Prefer `project` from `.gitreview` when present; use remote parsing as fallback. If `port` is missing, default to `29418`.

### SSH wrapper

All Gerrit SSH commands use this shape:

```bash
ssh -o ConnectTimeout=10 -p <port> <user>@<host> gerrit <subcommand> [args...]
```

### Change URL

```
https://<host>/c/<project>/+/<change-number>
```

---

## inbox presets

When the user asks for inbox, dashboard, open changes, or pending reviews, run **all three** queries and present three sections. All three are scoped to the current repo (`project:<project>`). For cross-project search, use a **custom query** without the `project:` filter (see [custom query](#custom-query) below).

Replace `<project>` with the resolved project name.

```bash
# My open changes
ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set \
  "owner:self status:open project:<project>"

# Awaiting my review
ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set \
  "reviewer:self status:open is:open project:<project>"

# Recently merged to main (last 5)
ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set \
  "project:<project> status:merged branch:main limit:5"
```

### Parse JSON lines

Prefer `jq` over inline Python — one pipe, no script file.

Each result line is one JSON object; the last line is `{"type":"stats","rowCount":N,...}` — skip it.

Suggested columns: `#`, `subject` (truncate), `owner.name`, Code-Review / Verified from `currentPatchSet.approvals`, WIP flag.

```bash
ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set \
  "owner:self status:open project:<project>" \
| jq -r '
  select(.type == "stats") | "--- \(.rowCount) rows ---",
  select(.type != "stats") |
  (
    (.currentPatchSet.approvals // [] | map(select(.type == "Code-Review")) | first | .value) // "-"
  ) as $cr |
  (if .workInProgress then " WIP" else "" end) as $wip |
  "#\(.number)\($wip) [\($cr)] \(.owner.name // "?"): \(.subject | .[0:70])"
'
```

---

## custom query

For arbitrary searches:

```bash
ssh -p <port> <user>@<host> gerrit query \
  --format=JSON \
  --current-patch-set \
  "<query>"
```

Add flags as needed:

| Flag | Use |
|------|-----|
| `--files` | File list + insertion/deletion counts (no diff body) |
| `--commit-message` | Include commit message |
| `--comments` | Include review comments |

Default to `limit:20` in the query string when the user does not specify a limit and the result set may be large.

### Search syntax (common)

| Intent | Example query |
|--------|----------------|
| My open changes | `owner:self status:open` |
| Awaiting my review | `reviewer:self status:open is:open` |
| Merged in date range | `status:merged after:2026-09-01 before:2026-09-08` |
| By topic | `topic:my-feature status:open` |
| By file path | `file:path/to/file.py status:merged` |
| CI failed | `status:open label:Verified=-1` |
| Ready to submit | `status:open label:Code-Review=+2 label:Verified=+1 -is:wip` |
| Single change | `change:46568` |

### Date bounds

- `after:YYYY-MM-DD` — inclusive start
- `before:YYYY-MM-DD` — **exclusive** end (use the day **after** the last inclusive day)

Example: merges Mon Apr 7 – Sun Apr 13 → `after:2026-04-07 before:2026-04-14`.

### Merge time

Prefer `currentPatchSet.approvals` where `type == "SUBM"` → `grantedOn` for merge timestamp. Fall back to `lastUpdated`.
