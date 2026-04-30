#!/usr/bin/env python3
"""
Fetch the top posts from Product Hunt via the GraphQL API v2.

Usage:
    PRODUCT_HUNT_TOKEN=phc_xxx python fetch_top.py --period today --count 10 --format markdown

Reads the developer token from the PRODUCT_HUNT_TOKEN env var.
Docs: https://api.producthunt.com/v2/docs
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API_URL = "https://api.producthunt.com/v2/api/graphql"

# Product Hunt's "day" is Pacific Time (UTC-8 standard, UTC-7 DST).
# Using a fixed -08:00 is close enough for filtering purposes; the API
# itself returns ranking based on PT, so small DST drift only affects edges.
PT_OFFSET = timezone(timedelta(hours=-8))

QUERY = """
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
""".strip()


def resolve_period(period: str) -> tuple[str, str, str]:
    """Return (postedAfter, postedBefore, label) ISO-8601 strings in PT."""
    now_pt = datetime.now(PT_OFFSET)
    today_pt = now_pt.replace(hour=0, minute=0, second=0, microsecond=0)

    if period == "today":
        start, end = today_pt, today_pt + timedelta(days=1)
        label = today_pt.strftime("%Y-%m-%d")
    elif period == "yesterday":
        start = today_pt - timedelta(days=1)
        end = today_pt
        label = start.strftime("%Y-%m-%d")
    elif period == "this_week":
        # ISO week: Monday is start
        start = today_pt - timedelta(days=today_pt.weekday())
        end = start + timedelta(days=7)
        label = f"{start.strftime('%Y-%m-%d')}..{(end - timedelta(days=1)).strftime('%Y-%m-%d')}"
    elif period == "this_month":
        start = today_pt.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        label = start.strftime("%Y-%m")
    else:
        # Specific date YYYY-MM-DD
        try:
            d = datetime.strptime(period, "%Y-%m-%d").replace(tzinfo=PT_OFFSET)
        except ValueError:
            raise SystemExit(f"Invalid --period: {period}")
        start, end = d, d + timedelta(days=1)
        label = period

    return start.isoformat(), end.isoformat(), label


def graphql(token: str, variables: dict) -> dict:
    payload = json.dumps({"query": QUERY, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "producthunt-top-skill/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} from Product Hunt API: {body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error reaching Product Hunt API: {e}")

    if "errors" in data:
        raise SystemExit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]


def fetch_posts(token: str, posted_after: str, posted_before: str, order: str, count: int) -> list[dict]:
    posts: list[dict] = []
    cursor: str | None = None
    while len(posts) < count:
        page_size = min(20, count - len(posts))
        data = graphql(token, {
            "postedAfter": posted_after,
            "postedBefore": posted_before,
            "order": order,
            "first": page_size,
            "after": cursor,
        })
        edges = data["posts"]["edges"]
        for e in edges:
            posts.append(e["node"])
        info = data["posts"]["pageInfo"]
        if not info["hasNextPage"] or not edges:
            break
        cursor = info["endCursor"]
    return posts[:count]


def fmt_table(posts: list[dict]) -> str:
    rows = [("#", "Name", "Tagline", "Votes", "Comments")]
    for i, p in enumerate(posts, 1):
        rows.append((
            str(i),
            p["name"][:30],
            (p["tagline"] or "")[:50],
            str(p["votesCount"]),
            str(p["commentsCount"]),
        ))
    widths = [max(len(r[c]) for r in rows) for c in range(len(rows[0]))]
    out = []
    for idx, r in enumerate(rows):
        out.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(r)))
        if idx == 0:
            out.append("  ".join("-" * w for w in widths))
    return "\n".join(out)


def fmt_markdown(posts: list[dict], label: str) -> str:
    lines = [f"# Product Hunt — Top {len(posts)} ({label})", ""]
    lines.append("| # | Product | Tagline | Votes | Comments |")
    lines.append("|---|---------|---------|-------|----------|")
    for i, p in enumerate(posts, 1):
        name = f"[{p['name']}]({p['url']})"
        tagline = (p["tagline"] or "").replace("|", "\\|")
        lines.append(f"| {i} | {name} | {tagline} | {p['votesCount']} | {p['commentsCount']} |")
    lines.append("")
    for i, p in enumerate(posts, 1):
        topics = ", ".join(t["node"]["name"] for t in p["topics"]["edges"]) or "—"
        makers = ", ".join(f"@{m['username']}" for m in p["makers"]) or "—"
        lines.append(f"## {i}. {p['name']}")
        lines.append(f"> {p['tagline']}")
        lines.append("")
        if p.get("description"):
            lines.append(p["description"])
            lines.append("")
        lines.append(f"- Votes: **{p['votesCount']}** · Comments: {p['commentsCount']}")
        lines.append(f"- Topics: {topics}")
        lines.append(f"- Makers: {makers}")
        if p.get("website"):
            lines.append(f"- Website: {p['website']}")
        lines.append(f"- Link: {p['url']}")
        lines.append("")
    return "\n".join(lines)


def fmt_json(posts: list[dict]) -> str:
    return json.dumps(posts, indent=2, ensure_ascii=False)


def fmt_csv(posts: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["rank", "name", "tagline", "description", "votes", "comments", "topics", "makers", "url"])
    for i, p in enumerate(posts, 1):
        topics = "|".join(t["node"]["name"] for t in p["topics"]["edges"])
        makers = "|".join(m["username"] for m in p["makers"])
        w.writerow([i, p["name"], p["tagline"], p.get("description", ""), p["votesCount"], p["commentsCount"], topics, makers, p["url"]])
    return buf.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch top Product Hunt posts.")
    parser.add_argument("--period", default="today",
                        help="today | yesterday | this_week | this_month | YYYY-MM-DD")
    parser.add_argument("--count", type=int, default=10, help="Number of posts (default 10)")
    parser.add_argument("--order", default="RANKING", choices=["RANKING", "VOTES", "NEWEST", "FEATURED_AT"],
                        help="Sort order (default RANKING)")
    parser.add_argument("--format", default="table", choices=["table", "markdown", "json", "csv"])
    parser.add_argument("--output", help="Write output to this file path instead of stdout")
    args = parser.parse_args()

    token = os.environ.get("PRODUCT_HUNT_TOKEN")
    if not token:
        print("ERROR: PRODUCT_HUNT_TOKEN env var is not set.", file=sys.stderr)
        print("Get one at https://www.producthunt.com/v2/oauth/applications", file=sys.stderr)
        return 1

    posted_after, posted_before, label = resolve_period(args.period)
    posts = fetch_posts(token, posted_after, posted_before, args.order, args.count)

    if args.format == "table":
        out = fmt_table(posts)
    elif args.format == "markdown":
        out = fmt_markdown(posts, label)
    elif args.format == "json":
        out = fmt_json(posts)
    else:
        out = fmt_csv(posts)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote {len(posts)} posts to {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
