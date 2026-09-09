---
name: google-traffic
description: >-
  Traffic reporter for GA4 and Search Console MCP reports. Use when the user
  wants search traffic review, GSC or GA4 data, monthly traffic ritual, page
  traffic deep-dive, or URL indexing status.
metadata:
  version: 1.1.2
---

# Google Traffic

Pull **GA4** and **Google Search Console** data through bundled MCP servers. Report trends, page-level search performance, and indexing health. On-page title, meta, schema, and JSON-LD are out of scope. Project SEO scripts live in the repo's `AGENTS.md`.

**auth** (machine-wide gcloud login) and **scope** (this repo's `property_id` + `site_url`) are separate — see [`setup-reference.md`](setup-reference.md).

---

## Workflow

### Step 1: Verify MCP

Use `GetMcpTools` to find servers matching `google-analytics` and `google-gsc` (names may be prefixed by the host).

If missing or `needsAuth` / error:

1. Missing server → read [`host-wiring-reference.md`](host-wiring-reference.md) for **host** registration.
2. Auth failure → read [`auth-reference.md`](auth-reference.md) for **auth** under `~/.config/gcloud/`.
3. Reload MCP on your **host** after auth or host changes.
4. Call `mcp_auth` on the failing server if tools still reject.

**Done when:** both target servers are `ready`, or the user explicitly skips and knows reports will be incomplete; if setup ran, **auth** paths live under `~/.config/gcloud/` and `list_properties` returns sites for the logged-in Google account.

### Step 2: Resolve scope

Resolve **GA4 `property_id`** and **GSC `site_url`** in order:

1. This repo's `AGENTS.md` — `property_id` and `site_url` (template: [`scope-reference.md`](scope-reference.md))
2. `README.md`, `package.json` `homepage`, or `.agents/product-marketing-context.md` — domain hints
3. MCP discovery — `list_properties` (GSC) and `get_account_summaries` (GA4); ask user to pick if ambiguous

Record the chosen ids in the report header.

**Done when:** `property_id` and `site_url` come from **this repo's** `AGENTS.md` first; if absent, from MCP discovery with user pick — not from global `GA4_PROPERTY_ID` / `GSC_DEFAULT_SITE`.

### Step 3: Classify branch

Pick exactly one branch from the user request:

| Branch | When |
|--------|------|
| **monthly** | Monthly review, traffic ritual, overall search trend |
| **page** | Specific path, URL, or "this landing page" |
| **index** | Indexing, indexed status, sitemap health |

Default to **monthly** when the user asks generally for "traffic" or "GSC data" without a URL.

**Done when:** one branch is chosen and any user time window is noted (default 28d; 90d when user says 三个月 / 90 days).

### Step 4: Execute branch

Follow [`workflows-reference.md`](workflows-reference.md) for tool combinations.

- **monthly** — GSC overview, period compare, top queries/pages; GA4 channel + pagePath; fill report template fields.
- **page** — GSC queries + country/device for the URL; GA4 `pagePath` slice; at least one actionable recommendation.
- **index** — `get_sitemaps` plus `batch_url_inspection` with explicit `urls` (one per line).

**Done when:** every row in the branch's workflow table has data, a documented MCP failure, or user skip.

### Step 5: Report

Deliver a concise summary:

- Time window, `site_url`, `property_id`
- Headline metrics (GSC clicks/impressions/CTR; GA4 sessions/channels as relevant)
- Findings (bullets)
- Recommended actions

**Done when:** summary is in the chat (table or bullets).

---

## Boundaries

- Mahjong hand analysis, codebase architecture, or product logic → not this skill.
- Title, meta, schema, JSON-LD, and keyword research for copy → out of scope.
- **auth** / **host** setup → [`auth-reference.md`](auth-reference.md), [`host-wiring-reference.md`](host-wiring-reference.md).
- Project SEO automation (e.g. `check:hreflang`, `check:meta`) → read project `AGENTS.md`; do not cache script commands here.

---

## Reference — MCP gotchas

- GSC `get_search_analytics`: `dimensions` is a **string** (e.g. `"query"`), not an array.
- `batch_url_inspection` / `check_indexing_issues`: **`urls` required** (newline-separated).
- Server names: resolve via `GetMcpTools`; never hardcode `project-0-*` ids.
