#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import os
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import query  # noqa: E402


def _http_response(body: bytes, status: int = 200) -> mock.MagicMock:
    resp = mock.MagicMock()
    resp.read.return_value = body
    resp.status = status
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


class TestRequireToken(unittest.TestCase):
    def test_missing_token_exits(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                query.require_token()
        self.assertIn("PRODUCT_HUNT_TOKEN", str(ctx.exception))
        self.assertIn("v2/oauth/applications", str(ctx.exception))

    def test_returns_env_value(self) -> None:
        with mock.patch.dict(os.environ, {"PRODUCT_HUNT_TOKEN": "phc_test"}):
            self.assertEqual(query.require_token(), "phc_test")


class TestGraphql(unittest.TestCase):
    @mock.patch("urllib.request.urlopen")
    def test_returns_data_object(self, urlopen: mock.Mock) -> None:
        payload = {"data": {"posts": {"edges": []}}}
        urlopen.return_value = _http_response(json.dumps(payload).encode())
        result = query.graphql("phc_test", "query { posts { edges { node { id } } } }")
        self.assertEqual(result, {"posts": {"edges": []}})
        req = urlopen.call_args[0][0]
        self.assertEqual(req.full_url, query.API_URL)
        self.assertEqual(req.get_header("Authorization"), "Bearer phc_test")
        self.assertEqual(req.get_header("Content-type"), "application/json")

    @mock.patch("urllib.request.urlopen")
    def test_http_error_exits(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = urllib.error.HTTPError(
            query.API_URL, 401, "Unauthorized", hdrs=None, fp=io.BytesIO(b'{"error":"bad"}')
        )
        with self.assertRaises(SystemExit) as ctx:
            query.graphql("bad", "query { __typename }")
        self.assertIn("401", str(ctx.exception))

    @mock.patch("urllib.request.urlopen")
    def test_graphql_errors_exit(self, urlopen: mock.Mock) -> None:
        payload = {"errors": [{"message": "nope"}]}
        urlopen.return_value = _http_response(json.dumps(payload).encode())
        with self.assertRaises(SystemExit) as ctx:
            query.graphql("phc_test", "query { nope }")
        self.assertIn("GraphQL errors", str(ctx.exception))
        self.assertIn("nope", str(ctx.exception))

    @mock.patch("urllib.request.urlopen")
    def test_none_variables_sent_as_empty_object(self, urlopen: mock.Mock) -> None:
        urlopen.return_value = _http_response(b'{"data": {}}')
        query.graphql("phc_test", "query { __typename }", None)
        sent = json.loads(urlopen.call_args[0][0].data.decode())
        self.assertEqual(sent["variables"], {})


class TestMain(unittest.TestCase):
    @mock.patch("query.graphql", return_value={"ok": True})
    @mock.patch("query.require_token", return_value="phc_test")
    def test_prints_json(self, _token: mock.Mock, _gql: mock.Mock) -> None:
        buf = io.StringIO()
        with mock.patch("sys.argv", ["query.py", "--query", "query { __typename }"]):
            with mock.patch("sys.stdout", buf):
                rc = query.main()
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue()), {"ok": True})

    def test_rejects_non_object_variables(self) -> None:
        with mock.patch("sys.argv", ["query.py", "--query", "query { x }", "--variables", "[1]"]):
            with self.assertRaises(SystemExit) as ctx:
                query.main()
        self.assertIn("JSON object", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
