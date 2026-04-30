---
name: producthunt-top
description: "Fetch the top/trending product list from Product Hunt using the official Product Hunt GraphQL API v2. Use whenever the user mentions 'Product Hunt,' 'PH top products,' 'today's top products,' 'trending products,' 'Product Hunt leaderboard,' 'Product Hunt daily,' 'Product Hunt weekly,' 'Product Hunt monthly,' or wants to retrieve, rank, summarize, or analyze Product Hunt posts. Also trigger when the user asks to compare, monitor, or list launches on Product Hunt, or to export PH posts to JSON/Markdown/CSV."
metadata:
  version: 1.0.0
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

### Step 3: Run the fetch script

Use the bundled script to query the API. It handles pagination, ranking, and formatting:

```bash
python scripts/fetch_top.py \
  --period today \
  --count 10 \
  --format markdown
```

Available flags:

| Flag | Description | Default |
|---|---|---|
| `--period` | `today`, `yesterday`, `this_week`, `this_month`, or a date `YYYY-MM-DD` | `today` |
| `--count` | Number of posts to return | `10` |
| `--format` | `table`, `markdown`, `json`, `csv` | `table` |
| `--output` | Path to save output (otherwise prints to stdout) | — |
| `--order` | `RANKING` (top of the day) or `VOTES` | `RANKING` |

The script reads the token from `PRODUCT_HUNT_TOKEN` and queries the `posts` field on `https://api.producthunt.com/v2/api/graphql`.

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

---

## API Reference (cheat sheet)

- **Endpoint:** `POST https://api.producthunt.com/v2/api/graphql`
- **Auth:** `Authorization: Bearer $PRODUCT_HUNT_TOKEN`
- **Docs:** https://api.producthunt.com/v2/docs

Minimal query the script uses:

```graphql
query TopPosts($postedAfter: DateTime, $postedBefore: DateTime, $order: PostsOrder, $first: Int, $after: String) {
  posts(postedAfter: $postedAfter, postedBefore: $postedBefore, order: $order, first: $first, after: $after) {
    edges {
      node {
        id
        name
        tagline
        description
        slug
        url
        website
        votesCount
        commentsCount
        createdAt
        featuredAt
        thumbnail { url }
        topics(first: 5) { edges { node { name } } }
        makers { name username }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
```

`order: RANKING` returns the daily leaderboard order (rank #1 first). `VOTES` returns by raw vote count.

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
