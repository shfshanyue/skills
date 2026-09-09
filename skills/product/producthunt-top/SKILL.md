---
name: producthunt-top
description: "Product Hunt top-list fetcher. Use when the user wants to list, compare, monitor, or export Product Hunt launches for today, a date, week, or month. For MicroSaaS opportunity analysis, use microsaas-opportunity; for arbitrary Product Hunt GraphQL, use producthunt."
metadata:
  version: 1.4.0
---

# Product Hunt Top List

Ranked Product Hunt posts for a time period. Auth and GraphQL transport are owned by `producthunt`; this skill owns period, count, order, and presentation.

## Workflow

### Step 1 — Confirm parameters

Defaults if the user is brief:

- **Time period** — `today` (default), `yesterday`, `this_week`, `this_month`, or `YYYY-MM-DD`
- **Count** — default `10`
- **Output format** — `table` (default), `markdown`, `json`, or `csv`
- **Save to file** — optional. If the user says "save" or "export," default to `producthunt-<period>-<date>.md` in the current directory

"Show me today's top products" → skip questions, use defaults.

**Done when:** period, count, format, and optional output path are known, from defaults or the request.

### Step 2 — Auth and transport

Hand off to `producthunt` for `PRODUCT_HUNT_TOKEN` and GraphQL. If that skill is not installed (sibling `producthunt` missing), stop and tell the user to install it: `npx skills add shfshanyue/skills --skill producthunt`.

**Done when:** `producthunt` is available and its token step is done, or the user has been asked for the token exactly once.

### Step 3 — Fetch

Run the bundled ranking script. Current flags and defaults: `python scripts/fetch_top.py --help`.

The script is the source of truth for the TopPosts query, Pacific Time day boundaries, pagination, and output formatting.

**Done when:** the script has printed or written the requested output, or exited with a missing-skill / token / API error.

### Step 4 — Present

Terminal: compact table with rank, name, tagline, votes, comments, topics, URL. Markdown: makers plus a short summary block at the top.

**Example markdown:**

```markdown
# Product Hunt — Top 10 (2026-04-30)

| # | Product | Tagline | Votes | Comments |
|---|---------|---------|-------|----------|
| 1 | [ProductName](https://www.producthunt.com/posts/...) | One-line tagline | 1,234 | 89 |

## 1. ProductName
> One-line tagline

- Votes: 1,234 · Comments: 89
- Topics: AI, Developer Tools
- Makers: @alice, @bob
- Link: https://www.producthunt.com/posts/...
```

After listing, offer at most two follow-ups that match the request (today vs yesterday, topic filter, export, or MicroSaaS analysis via `microsaas-opportunity`).

**Done when:** results are in the chat and at most two follow-ups have been offered.

## Boundaries

- Arbitrary Product Hunt GraphQL → `producthunt`
- MicroSaaS opportunity analysis → `microsaas-opportunity`
- Product Hunt launch copy → `launch-kit`

## Reference

- **Empty list for `today`** — very early UTC; try `--period yesterday`
- **Date filter off-by-one** — Product Hunt resets at midnight Pacific Time; the script converts the period to PT
