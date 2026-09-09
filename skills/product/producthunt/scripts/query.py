#!/usr/bin/env python3
"""POST a GraphQL query to Product Hunt API v2.

Usage:
    PRODUCT_HUNT_TOKEN=phc_xxx python query.py --query 'query { __typename }' --variables '{}'

Reads the developer token from PRODUCT_HUNT_TOKEN.
Docs: https://api.producthunt.com/v2/docs
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.producthunt.com/v2/api/graphql"
USER_AGENT = "producthunt-skill/1.0"


def require_token() -> str:
    token = os.environ.get("PRODUCT_HUNT_TOKEN")
    if not token:
        raise SystemExit(
            "ERROR: PRODUCT_HUNT_TOKEN env var is not set.\n"
            "Get one at https://www.producthunt.com/v2/oauth/applications"
        )
    return token


def graphql(token: str, query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
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


def main() -> int:
    parser = argparse.ArgumentParser(description="POST a GraphQL query to Product Hunt API v2.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--query", help="GraphQL query string")
    src.add_argument("--file", help="Path to a .graphql file")
    parser.add_argument("--variables", default="{}", help="JSON object of GraphQL variables")
    args = parser.parse_args()

    gql = args.query if args.query is not None else Path(args.file).read_text(encoding="utf-8")
    try:
        variables = json.loads(args.variables)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid --variables JSON: {e}")
    if not isinstance(variables, dict):
        raise SystemExit("--variables must be a JSON object")

    data = graphql(require_token(), gql, variables)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
