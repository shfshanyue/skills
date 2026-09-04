# Diff reference

Gerrit SSH does **not** return diff text. Fetch the change ref with git, then run `git diff`.

## Step A — Metadata

```bash
ssh -p <port> <user>@<host> gerrit query \
  --format=JSON \
  --current-patch-set \
  --files \
  --commit-message \
  --comments \
  "change:<N>"
```

Extract from the change object:

| Field | Use |
|-------|-----|
| `subject` | Title |
| `currentPatchSet.ref` | Git ref to fetch (e.g. `refs/changes/68/46568/1`) |
| `currentPatchSet.revision` | Commit hash |
| `currentPatchSet.files` | Per-file `+insertions/-deletions` |
| `commitMessage` | Full message (with `--commit-message`) |
| `comments` | Existing review threads (with `--comments`) |

Extract fields with `jq` — do not paste raw JSON into the chat.

```bash
REF=$(ssh -p <port> <user>@<host> gerrit query --format=JSON --current-patch-set \
  "change:<N>" \
  | jq -r 'select(.currentPatchSet?) | .currentPatchSet.ref' | head -1)
```

Other metadata (`subject`, `currentPatchSet.files`, `commitMessage`, `comments`) — same query, `jq` select the field.

## Step B — Fetch change ref

Run from the **local clone** of the Gerrit project:

```bash
git fetch -q origin "$REF"
```

### Ref rule (manual)

`refs/changes/{last-two-digits}/{change-number}/{patchset}`

Example: change `46568`, patch set `1` → `refs/changes/68/46568/1`

```bash
CHANGE=46568
PATCHSET=1
REF="refs/changes/$(printf '%02d' $((CHANGE % 100)))/${CHANGE}/${PATCHSET}"
git fetch -q origin "$REF"
```

Prefer `currentPatchSet.ref` from the query over manual construction when patch set ≠ 1.

## Step C — Diff

```bash
# Full patch
git diff FETCH_HEAD^..FETCH_HEAD

# Stat only
git diff --stat FETCH_HEAD^..FETCH_HEAD

# Single file
git diff FETCH_HEAD^..FETCH_HEAD -- path/to/file.py
```

## Present for code review

Include in order:

1. Change number, subject, Gerrit URL
2. Commit message
3. File stat (`--stat` or from query `--files`)
4. Existing comments (if any)
5. Diff body (full or per-file if large — ask user or truncate with note)

After review, the user may invoke **review** branch to post scores via `gerrit review`.

## Failures

| Error | Action |
|-------|--------|
| `git fetch` fails | Confirm cwd is the correct project clone; check remote URL matches Gerrit project |
| Empty diff | Change may be merge-only or ref wrong — re-check patch set from query |
| File not in clone | Fetch succeeded but path missing — user may need a different repo |
