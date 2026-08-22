# Google Traffic — workflow reference

Read when executing Step 4 of [`SKILL.md`](SKILL.md). Tool parameter details live in MCP tool schemas (use `GetMcpTools`); this file only lists **which tools** and **project-agnostic defaults**.

## Defaults

| Input | Default |
|-------|---------|
| GSC date window | 28 days (monthly); 90 days when user says "三个月" / "90 days" |
| GA4 date window | Match GSC window |
| GSC `site_url` | From project `AGENTS.md`, else `list_properties` + user pick |
| GA4 `property_id` | From project `AGENTS.md`, else `get_account_summaries` + user pick |

## Branch: monthly

| Goal | GSC | GA4 |
|------|-----|-----|
| Headline trend | `get_performance_overview` | `run_report` — `sessionDefaultChannelGroup`, metrics `sessions`, `activeUsers` |
| Query movement | `compare_search_periods` — recent 30d vs prior 30d, `dimensions`: `"query"` | — |
| Top queries | `get_search_analytics` — `dimensions`: `"query"`, sort by clicks | — |
| Top pages | `get_search_analytics` — `dimensions`: `"page"` | `run_report` — `pagePath`, metrics `sessions`, `screenPageViews` |
| Sitemap health | `get_sitemaps` | — |

**Report template fields:**

```markdown
## YYYY-MM traffic review

- Window: {start} – {end}
- GSC site: {site_url} · GA4 property: {property_id}
- GSC: clicks ___ / impressions ___ / CTR ___% / position ___
- GA4 organic sessions: ___ / total sessions: ___
- Top gains (queries/pages):
- Top losses (queries/pages):
- Indexing issues:
- Actions:
- Next month:
```

## Branch: page

Target: user-supplied path (e.g. `/analysis`) or full URL.

| Goal | GSC | GA4 |
|------|-----|-----|
| Queries for page | `get_search_by_page_query` — `page_url` full URL | — |
| Country / device | `get_advanced_search_analytics` — filter `page` contains path, `dimensions` `country` or `device` | — |
| On-site behavior | — | `run_report` — `pagePath` contains filter, dimensions `deviceCategory` or `sessionDefaultChannelGroup` |

**Done when:** query + at least one breakdown (country or device) + one GA4 slice + one actionable recommendation (CTR gap, locale mismatch, bounce, etc.).

## Branch: index

| Goal | Tool | Notes |
|------|------|-------|
| Sitemap status | `get_sitemaps` | Confirm submitted URLs and status |
| URL inspection | `batch_url_inspection` | **`urls` required** — one URL per line |

Derive URL list from user input, project sitemap URL in README/AGENTS.md, or `curl` sitemap.xml — do not guess URLs.

## Gotchas (variance)

- `get_search_analytics`: `dimensions` is a **string** (`"query"`), not an array.
- `batch_url_inspection`: must pass `urls` (newline-separated); omitting fails.
- `site_url` must match `list_properties` exactly (e.g. `sc-domain:example.com` vs `https://www.example.com/`).
- Discover MCP server ids with `GetMcpTools` — do not assume `project-0-*` prefixes.

## GA4 `run_report` sketch

Use MCP tool hints for `dimension_filter` / `date_ranges`. Typical monthly page report:

```text
property_id: {from scope}
dimensions: [pagePath] or [sessionDefaultChannelGroup]
metrics: [sessions, activeUsers] or [sessions, screenPageViews, bounceRate]
date_ranges: [{ start_date: "90daysAgo", end_date: "yesterday", name: "90d" }]
```

For path filters, use `dimension_filter` on `pagePath` — see `run_report` tool description for `match_type` values.
