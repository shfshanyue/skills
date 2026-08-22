---
name: producthunt-top
description: "Product Hunt top-list fetcher. Use when the user wants to list, compare, monitor, summarize, analyze, or export Product Hunt launches for today, a date, week, or month."
metadata:
  version: 1.1.0
---

# Product Hunt Top List

Fetch the top posts (products) from Product Hunt via the official GraphQL API v2 and present them in a clean, ranked format.

The user has a Product Hunt **Developer Token** (a personal API access token), which the script reads from the `PRODUCT_HUNT_TOKEN` environment variable. If it's missing, ask the user once and offer to export it for the session.

---

## Workflow

### Step 1: Confirm intent and parameters

Before running, confirm these inputs (use sensible defaults if the user is brief):

- **Time period** — `today` (default), `yesterday`, `this_week`, `this_month`, or a specific date `YYYY-MM-DD`.
- **Count** — how many posts to return (default `10`, max `20` per page; the script paginates if more is requested).
- **Output format** — `table` (default, printed to terminal), `markdown`, `json`, or `csv`.
- **Save to file** — optional path. If the user says "save" or "export," default to `producthunt-<period>-<date>.md` in the current directory.

If the user just says "show me today's top products," skip the questions and use defaults.

**Done when:** period, count, format, and optional output path are known, either from defaults or the user's request.

### Step 2: Verify token

Check `PRODUCT_HUNT_TOKEN` is set:

```bash
if [ -z "$PRODUCT_HUNT_TOKEN" ]; then
  echo "PRODUCT_HUNT_TOKEN is not set"
fi
```

If missing, ask the user for it once. Do **not** print or log the token. Suggest they add it to their shell profile (`~/.zshrc` or `~/.bashrc`) as:

```bash
export PRODUCT_HUNT_TOKEN="phc_xxx..."
```

**Done when:** `PRODUCT_HUNT_TOKEN` is available to the fetch script or the user has been asked for it exactly once.

### Step 3: Run the fetch script

Use the bundled script to query the API. It handles pagination, ranking, and formatting:

```bash
python scripts/fetch_top.py \
  --period today \
  --count 10 \
  --format markdown
```

Run `python scripts/fetch_top.py --help` for the current flag list and defaults.

The script is the single source of truth for GraphQL fields, pagination, date boundaries, and output formatting internals.

**Done when:** the script exits successfully and has printed or written the requested output.

### Step 4: Present the results

For terminal output, render a compact table with: rank, name, tagline, votes, comments, topics, URL. For markdown, include the thumbnail/image, maker names, and a short summary block at the top.

**Example markdown output:**

```markdown
# Product Hunt — Top 10 (2026-04-30)

| # | Product | Tagline | Votes | Comments |
|---|---------|---------|-------|----------|
| 1 | [ProductName](https://www.producthunt.com/posts/...) | One-line tagline | 1,234 | 89 |
| 2 | ... | ... | ... | ... |

## 1. ProductName
> One-line tagline

- Votes: 1,234 · Comments: 89
- Topics: AI, Developer Tools
- Makers: @alice, @bob
- Link: https://www.producthunt.com/posts/...
```

### Step 5: (Optional) Follow-up actions

After listing, offer 2–3 useful next steps based on the user's apparent goal:

- "Want me to summarize trends across these top 10 (categories, themes)?"
- "Want to compare today vs yesterday?"
- "Want to filter by topic (e.g., AI, Developer Tools)?"
- "Want to export this to `producthunt-top.md` for your records?"

Pick at most one or two — don't spam.

**Done when:** results have been presented and at most two relevant follow-up actions have been offered.

---

## Troubleshooting

- **401 / Unauthorized** → token missing, expired, or malformed. Ask user to regenerate from https://www.producthunt.com/v2/oauth/applications.
- **429 / Rate limit** → API allows ~6,250 complexity points per 15 min. The script already requests minimal fields; if hit, wait or reduce `--count`.
- **Empty list for `today`** → very early UTC; try `--period yesterday`.
- **Date filter off-by-one** → Product Hunt resets at midnight Pacific Time. The script converts the requested period to PT before querying.

---

## Notes

- Never echo the token into logs, file output, or shell history. The script masks it.
- Keep the SKILL.md lean; deeper API behavior lives in `scripts/fetch_top.py` comments.
