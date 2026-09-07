#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fetch_top  # noqa: E402


class TestSiblingTransport(unittest.TestCase):
    def test_producthunt_scripts_points_at_query_py(self) -> None:
        scripts = fetch_top._producthunt_scripts()
        self.assertTrue((scripts / "query.py").is_file())
        self.assertEqual(scripts.name, "scripts")
        self.assertEqual(scripts.parent.name, "producthunt")

    def test_missing_sibling_exits_with_install_hint(self) -> None:
        with mock.patch.object(Path, "is_file", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                fetch_top._producthunt_scripts()
        msg = str(ctx.exception)
        self.assertIn("producthunt skill not found", msg)
        self.assertIn("npx skills add", msg)
        self.assertIn("producthunt", msg)


class TestFetchPosts(unittest.TestCase):
    def test_paginates_until_count(self) -> None:
        calls: list[dict] = []

        def graphql(token: str, query: str, variables: dict | None = None) -> dict:
            calls.append(variables or {})
            page = len(calls)
            nodes = [{"id": f"{page}-1"}, {"id": f"{page}-2"}]
            return {
                "posts": {
                    "edges": [{"node": n} for n in nodes],
                    "pageInfo": {
                        "hasNextPage": page == 1,
                        "endCursor": f"c{page}",
                    },
                }
            }

        posts = fetch_top.fetch_posts(graphql, "tok", "a", "b", "RANKING", 3)
        self.assertEqual([p["id"] for p in posts], ["1-1", "1-2", "2-1"])
        self.assertEqual(calls[0]["first"], 3)
        self.assertIsNone(calls[0]["after"])
        self.assertEqual(calls[1]["first"], 1)
        self.assertEqual(calls[1]["after"], "c1")
        self.assertEqual(calls[0]["postedAfter"], "a")
        self.assertEqual(calls[0]["order"], "RANKING")
        self.assertIn("query TopPosts", fetch_top.QUERY)

    def test_load_transport_returns_real_functions(self) -> None:
        graphql, require_token = fetch_top._load_transport()
        self.assertTrue(callable(graphql))
        self.assertTrue(callable(require_token))
        with mock.patch.dict(os.environ, {"PRODUCT_HUNT_TOKEN": "phc_x"}):
            self.assertEqual(require_token(), "phc_x")


class TestNoLocalHttp(unittest.TestCase):
    def test_fetch_top_has_no_api_url(self) -> None:
        self.assertFalse(hasattr(fetch_top, "API_URL"))


if __name__ == "__main__":
    unittest.main()
