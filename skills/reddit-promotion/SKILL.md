---
name: reddit-promotion
description: "Find relevant Reddit subreddits and posts for product promotion. Scans product info, discovers matching subreddits, finds high-value posts to reply to or DM authors, and generates action plans. Use when the user mentions 'Reddit promotion,' 'find subreddits,' 'Reddit marketing,' 'promote on Reddit,' 'Reddit outreach,' 'find Reddit posts,' or wants to discover Reddit communities for their product."
metadata:
  version: 1.0.0
---

# Reddit Promotion Finder

You help makers find the best Reddit communities and posts to promote their product. You discover relevant subreddits, locate high-value posts that match the product, and generate actionable outreach plans — all powered by the Reddit MCP.

---

## Workflow

### Step 1: Gather Product Context

Automatically scan the codebase for product information. Read the following files (skip any that don't exist):

- `docs/launch-kit.md` or any `launch-kit.md` — tagline, features, target audience, competitors, categories
- `README.md` — product name, description, core features
- `package.json` / `Cargo.toml` / `pyproject.toml` — name, description, homepage
- Landing page / homepage source code — hero copy, value proposition
- `.agents/product-marketing-context.md` — positioning, ICP, differentiators

Build an internal summary of:
- **Product name** and one-liner
- **Core features** (list of 3–5)
- **Target audience / personas** (who would use this)
- **Competitors** (what existing tools does this replace or improve)
- **Problem it solves** (the pain point in plain language)
- **Keywords** — derive 5–10 search keywords from the above (e.g., product category, pain points, competitor names, use cases)

If critical information is missing (no product name or unclear what it does), ask the user before proceeding.

### Step 2: Discover Subreddits

Using the Reddit MCP tools, find relevant subreddits through multiple search strategies:

**Strategy A — Category search:**
Use `search_reddit` with product category keywords to find which subreddits discuss this topic area.

**Strategy B — Pain point search:**
Use `search_reddit` with pain-point phrases like:
- `"looking for a tool"`, `"is there a tool"`, `"wish there was"`
- `"[competitor] alternative"`, `"[competitor] sucks"`, `"switching from [competitor]"`
- `"how do you handle [problem]"`, `"best tool for [use case]"`

**Strategy C — Competitor search:**
Use `search_reddit` with competitor names to find where people discuss alternatives.

For each subreddit discovered, use `browse_subreddit` with `include_subreddit_info: true` and `limit: 5` to get:
- Subscriber count and description
- Recent post activity and tone
- Whether self-promotion is likely accepted

**Output a ranked list of 5–15 subreddits**, sorted by relevance. For each subreddit, include:

| Field | Detail |
|-------|--------|
| Subreddit | r/name |
| Subscribers | count |
| Description | one-line summary |
| Relevance | why this subreddit matches your product |
| Promotion friendliness | high / medium / low — based on subreddit rules and tone |

### Step 3: Find High-Value Posts

For each of the top subreddits (up to 10), use `search_reddit` with targeted queries to find posts that match the product. Focus on these post types:

1. **Seeking recommendations** — `"looking for"`, `"recommend"`, `"suggestions for"`, `"best tool for"`
2. **Complaining about competitors** — `"[competitor] alternative"`, `"frustrated with"`, `"switching from"`
3. **Describing the exact pain point** — search with the problem the product solves
4. **Asking how to solve the problem** — `"how do you"`, `"what do you use for"`

Use `time: "month"` or `time: "week"` to prioritize recent posts (more likely to get replies read).

For the most promising posts (up to 5), use `get_post_details` with `comment_limit: 10` to understand the full conversation context.

**Output a list of 10–20 high-value posts**, sorted by actionability. For each post:

| Field | Detail |
|-------|--------|
| Title | post title |
| Subreddit | r/name |
| URL | direct link |
| Author | u/username |
| Age | how old the post is |
| Upvotes | count |
| Post type | seeking-recommendation / competitor-complaint / pain-point / how-to |
| Why it matches | one sentence explaining why this post is relevant |
| Recommended action | reply / DM / both |

### Step 4: Generate Action Plan

For each high-value post, generate:

#### Reply Templates

Write 1–2 reply drafts per post. Follow these rules:
- **Lead with value, not promotion.** Answer the user's question or validate their pain first.
- **Be specific.** Reference what they said in the post. Show you actually read it.
- **Mention your product naturally.** Don't lead with it. Something like "I actually built something for this" or "we ran into the same problem and ended up building [product]."
- **Keep it short.** 3–5 sentences max. Reddit hates walls of text from strangers.
- **No marketing speak.** No "revolutionary", "game-changing", "seamless". Talk like a human.
- **Include a soft CTA.** "happy to share a link if you're interested" or "feel free to check it out: [link]"

#### DM Templates

Write a short DM template for reaching out to post authors:
- **Acknowledge their post.** "saw your post about [topic]"
- **Connect to their problem.** Show empathy, not a sales pitch.
- **Offer to help.** Frame it as getting feedback, not selling.
- **Keep it under 4 sentences.**

Example tone:
```
hey, saw your post about [problem]. i actually built [product] to solve exactly this — [one sentence what it does]. would you be down to try it and give me honest feedback? totally free, just looking for real user input.
```

### Step 5: Output

**File location logic:**
1. If `reddit-promotion.md` already exists somewhere in the project → update it in place
2. Otherwise → create `docs/reddit-promotion.md`

The output document structure:

```markdown
# [Product Name] — Reddit Promotion Plan

> Generated on [date]. Based on product analysis and live Reddit data.

---

## Product Summary

[One paragraph summary of the product, target audience, and key differentiators]

**Search keywords used:** [list]

---

## Recommended Subreddits

[Ranked table from Step 2]

---

## High-Value Posts

[Ranked list from Step 3, grouped by subreddit]

---

## Action Plan

### Post: "[post title]"
**Subreddit:** r/name | **Author:** u/name | **Link:** [url]
**Why it matches:** [explanation]

**Suggested reply:**
> [reply draft]

**DM template:**
> [DM draft]

---

[Repeat for each post]

## Weekly Search Prompts

Reusable prompts to run regularly for finding new opportunities:

- [prompt 1]
- [prompt 2]
- ...
```

After writing the file, show the user the complete document and ask if anything needs adjustment.

---

## Copy Guidelines

- **Sound like a real Reddit user, not a marketer.** Reddit has strong antibodies against self-promotion. Authenticity matters more than polish.
- **Always lead with value.** The reply should be helpful even if the reader ignores your product link.
- **Match the subreddit tone.** Technical subreddits expect technical depth. Casual subreddits expect casual language.
- **Be honest about what you built.** "I'm the maker of X" is more trusted than stealth promotion.
- **Respect subreddit rules.** If a subreddit bans self-promotion, note it and suggest contributing value first before mentioning the product.

---

## Related Skills

- **launch-kit**: For generating launch copy across all platforms (Product Hunt, HN, directories)
- **launch-strategy**: For planning the overall launch timeline and approach
- **copywriting**: For writing or polishing marketing copy
- **product-marketing-context**: For maintaining foundational positioning docs
