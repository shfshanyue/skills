---
name: microsaas-opportunity
description: "MicroSaaS curator. Use when the user wants a Product Hunt list or a named product / product website scored as a MicroSaaS opportunity. For raw Product Hunt lists, use producthunt-top; for launch copy of their own product, use launch-kit."
metadata:
  version: 1.1.0
---

# MicroSaaS Opportunity

Score **other people's** products as a **MicroSaaS** opening. Two branches: a Product Hunt **list** as candidates, or one **product** (name or URL). Chinese report.

## Steps

### 1. Route

| Branch | When | Action |
|--------|------|--------|
| Own product | 我的产品 / our product / this repo / launch copy | This skill scores other people's products; for launch copy, `launch-kit` |
| Raw list | list / export / 榜单 with no MicroSaaS ask | One-line to `producthunt-top` |
| List | PH period + MicroSaaS | List gather |
| Product | a product name, homepage, or PH post/product URL | Product gather |

**Done when:** the branch is List or Product, or a one-line hand-off has been made.

### 2. Gather

**List.** Hand off to `producthunt-top` with period from the request (`today` if unset), `count: 8`, `format: json`. Reuse PH JSON already in this session. If `producthunt-top` is missing, stop: `npx skills add shfshanyue/skills --skill producthunt-top`.

**Product.** Subject is the named product or URL in the request.

1. Product Hunt post or product URL → `producthunt` for that slug. Fields: `name`, `tagline`, `description`, `url`, `website`, `votesCount`, `commentsCount`, `topics`, `makers`.
2. Other URL → fetch the page (and a linked pricing page). Take name, one-liner, audience, features, pricing as written.
3. Name only → resolve to one URL (one search), then 1 or 2. If it does not resolve, ask once.

**Done when:** every item in scope has gathered fields (up to 8 posts, or 1 product), or gather has failed and the user has been told or asked once.

### 3. Select and 描述

**List:** pick up to 4 from the gathered posts ([`analysis.md`](analysis.md) **Select**). **Product:** that product is the set.

Then write a **描述** (same file) for each selected product only.

**Done when:** the set is known (up to 4, or the one product) and each selected product has a 描述.

### 4. Deep dive

For each selected product, fill the five parts in [`analysis.md`](analysis.md). **List** also writes **趋势观察**.

**Done when:** every selected product has all five parts, and a list run has a 3–5 sentence 趋势观察 — or the fit set was empty and that is stated.

### 5. Present

Emit Chinese markdown from [`report.md`](report.md). One product block per selected item. Chat. Write a file only if the user asked to save or export.

**Done when:** the report is in the chat in that template, and at most two follow-ups that match the request have been offered.

## Boundaries

- Raw Product Hunt list / export → `producthunt-top`
- Arbitrary Product Hunt GraphQL → `producthunt`
- Launch copy for the user's own product → `launch-kit`
