---
name: reddit-promotion
description: "Reddit promotion planner. Use when the user wants to find subreddits, high-value posts, or outreach drafts for product promotion on Reddit."
metadata:
  version: 1.2.0
---

# Reddit Promotion Finder

Find subreddits and posts for a product, then draft a value-led outreach plan. Live Reddit data comes only from this skill's read-only script, `scripts/reddit.py`. Do not call a Reddit MCP, an RSS feed, or an unauthenticated `reddit.com` `.json` URL.

The script is the source of truth for OAuth, endpoints, flags, trimming, token reuse, and HTTP 429 handling. From this skill's directory, current flags are `python scripts/reddit.py --help`.

## Workflow

### Step 1: Gather product context

Read these files and skip any that are missing:

- `docs/launch-kit.md` or any `launch-kit.md`
- `README.md`
- `package.json`, `Cargo.toml`, or `pyproject.toml`
- Landing-page or homepage source
- `.agents/product-marketing-context.md`

Record the product name and one-liner, 3–5 core features, target audience, competitors, the problem solved, and 5–10 search keywords (category, pain, competitor names, use cases).

If the product name is missing, or what the product does is unclear, ask once and wait.

**Done when:** product name, one-liner, target audience, problem, and 5–10 search keywords are recorded, or the user has been asked once for the missing critical context and the workflow is waiting.

### Step 2: Credentials

Run the script only when `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` are set. Optional `REDDIT_USER_AGENT` overrides the contact string (`platform:app:version (by /u/name)`).

If either required variable is unset, run any read subcommand once and show the script's stderr. Stop. Do not invent credentials and do not browse Reddit another way.

The script's error names both variables and https://www.reddit.com/prefs/apps (app type: script). Never print the secret or the bearer token.

**Done when:** both required variables are set, or the script's missing-credential error has been shown once and the workflow has stopped.

### Step 3: Discover subreddits

Run `search` in three passes: category keywords, pain phrases, and competitor names. Pain phrases include "looking for a tool", "is there a tool", "wish there was", "[competitor] alternative", "switching from [competitor]", and "how do you handle [problem]".

From the posts returned, pick the distinct relevant subreddits (at most 15). For each, run `subreddit` and judge promotion friendliness from `public_description`, `description`, and `submit_text`. Use only names, counts, and text the script returned. Do not invent subscriber counts.

Rank 5–15 subreddits. If fewer than 5 distinct relevant subreddits came back, rank those and stop. For each row record:

| Field | Detail |
|-------|--------|
| Subreddit | r/name |
| Subscribers | `subscribers` |
| Description | one line from `public_description` or `title` |
| Relevance | why it matches the product |
| Promotion friendliness | high / medium / low, with the rule or tone evidence |

**Done when:** that ranked list is complete from script JSON, or the script exited and its error was reported and the workflow stopped.

### Step 4: Find high-value posts

For the top subreddits (at most 10), run `search` scoped to that subreddit. Cover four post types: seeking a recommendation, complaining about a competitor, describing this product's pain, and asking how to solve that pain. Prefer a recent time window (week or month) when the script help lists that window.

For the strongest posts (at most 5, unless the user asked for more), run `post` and read the trimmed comments before drafting.

Rank 10–20 posts by how actionable they are. If the searches return fewer relevant posts, rank those and stop. Do not invent titles, authors, scores, or URLs. For each post record:

| Field | Detail |
|-------|--------|
| Title | `title` |
| Subreddit | r/name |
| URL | `permalink` |
| Author | `author` |
| Age | from `created_utc` |
| Upvotes | `score` |
| Post type | seeking-recommendation / competitor-complaint / pain-point / how-to |
| Why it matches | one sentence |
| Recommended action | reply / DM / both |

**Done when:** 10–20 posts are ranked, or every relevant post from those searches is ranked when fewer than 10 match, or the script exited and its error was reported and the workflow stopped.

### Step 5: Draft the action plan

For each high-value post, write:

- 1–2 replies. Answer the question or name the pain first. Cite a detail from the post or its comments. Mention the product after that, in one plain sentence, as its maker. Keep it to 3–5 sentences. No "revolutionary", "game-changing", or "seamless". Soft CTA only ("happy to share a link", or the link once).
- One DM under 4 sentences: their post, their problem, a request for feedback.

Example tone:

```
hey, saw your post about [problem]. i actually built [product] to solve exactly this — [one sentence what it does]. would you be down to try it and give me honest feedback? totally free, just looking for real user input.
```

**Done when:** every ranked post has at least one specific reply and one short DM.

### Step 6: Write the plan

1. If `reddit-promotion.md` already exists in the project, update that file.
2. Otherwise create `docs/reddit-promotion.md`.

Follow [`template.md`](template.md). Show the full document and ask what to change.

**Done when:** `reddit-promotion.md` is written at that path, the full plan is in the chat, and the user has been asked what to adjust.

## Copy guidelines

- Sound like a participant in that subreddit, not a marketer.
- The reply must still help if the reader ignores the product.
- Match a technical subreddit with technical detail and a casual one with casual language.
- Say that you built it. "I'm the maker of X" is more trusted than a disguised pitch.
- If the about text forbids promotion, set friendliness to low and tell the user to contribute before mentioning the product.

## Boundaries

Launch copy, launch sequencing, and positioning are a different task. Hand off only when a matching installed skill exists or the user asks for that work.

## Reference

- Missing `REDDIT_CLIENT_ID` or `REDDIT_CLIENT_SECRET` — show the script error and stop. Do not substitute RSS or `.json`.
- HTTP 401 — the script app id or secret was rejected. Point at https://www.reddit.com/prefs/apps.
- HTTP 429 — the script sleeps for `Retry-After` and retries. If it still exits, report that and stop.
- The script reuses the OAuth token until expiry. Do not print the token or copy the cache file into the project.
