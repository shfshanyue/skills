---
name: producthunt
description: "Product Hunt GraphQL API. Use when the user wants to query Product Hunt via GraphQL. For ranked top-list fetch/export, use producthunt-top; for MicroSaaS opportunity analysis, use microsaas-opportunity; for Product Hunt launch copy, use launch-kit."
metadata:
  version: 1.2.0
---

# Product Hunt GraphQL

POST a GraphQL query to Product Hunt API v2. The bundled script is the source of truth for URL, headers, and error handling.

## Workflow

### Step 1 — Token

Check `PRODUCT_HUNT_TOKEN`. If missing, ask once. Never print the token. Suggest they add it to their shell profile:

```bash
export PRODUCT_HUNT_TOKEN="phc_xxx..."
```

Create a token at https://www.producthunt.com/v2/oauth/applications

**Done when:** `PRODUCT_HUNT_TOKEN` is set for this session, or the user has been asked for it exactly once.

### Step 2 — Assemble query

Take the GraphQL query and variables from the user, or from a calling skill (`producthunt-top` supplies its TopPosts query; `microsaas-opportunity` a single-post slug). Schema: https://api.producthunt.com/v2/docs

**Done when:** the query string and variables object are known.

### Step 3 — Execute

Run the bundled script. Current flags and defaults: `python scripts/query.py --help`.

**Done when:** the script printed JSON to stdout, or exited with an HTTP/GraphQL error on stderr.

### Step 4 — Present

Show the JSON, or a compact table when the payload is a short list. Surface the script's error text when it exits non-zero.

**Done when:** results or the script's error are in the chat.

## Boundaries

- Ranked top-list fetch/export → `producthunt-top`
- MicroSaaS opportunity analysis → `microsaas-opportunity`
- Product Hunt launch copy → `launch-kit`

## Reference

- **401** — token missing, expired, or malformed. Regenerate at https://www.producthunt.com/v2/oauth/applications
- **429** — ~6,250 complexity points per 15 min; shrink the query or wait
- Never echo the token into logs, files, or shell history
