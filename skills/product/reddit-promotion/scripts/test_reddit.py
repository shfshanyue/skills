#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import format_datetime
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import reddit  # noqa: E402


def _ok(payload: object) -> mock.MagicMock:
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(payload).encode()
    resp.status = 200
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


def _http_error(code: int, headers: dict[str, str] | None = None, body: bytes = b"{}") -> urllib.error.HTTPError:
    hdrs = EmailMessage()
    for key, value in (headers or {}).items():
        hdrs[key] = value
    return urllib.error.HTTPError(
        reddit.API_ROOT + "/search",
        code,
        "error",
        hdrs=hdrs,
        fp=io.BytesIO(body),
    )


def _token(access: str = "token-1", expires_in: int = 3600) -> dict:
    return {"access_token": access, "token_type": "bearer", "expires_in": expires_in, "scope": "*"}


def _post(**overrides: object) -> dict:
    data = {
        "id": "abc123",
        "name": "t3_abc123",
        "title": "Need a tool",
        "subreddit": "python",
        "author": "alice",
        "score": 12,
        "upvote_ratio": 0.9,
        "num_comments": 3,
        "created_utc": 1700000000.0,
        "url": "https://example.com/tool",
        "permalink": "/r/python/comments/abc123/need_a_tool/",
        "is_self": False,
        "over_18": False,
        "stickied": False,
        "locked": False,
        "link_flair_text": "Help",
        "selftext": "",
        "preview": {"images": [{"source": {"url": "https://preview.example/x"}}]},
        "media": {"oembed": {"html": "<iframe>"}},
        "all_awardings": [{"name": "gold"}],
    }
    data.update(overrides)
    return {"kind": "t3", "data": data}


def _listing(*children: dict) -> dict:
    return {"kind": "Listing", "data": {"children": list(children), "after": "t3_next"}}


def _comment(**overrides: object) -> dict:
    data = {
        "id": "c1",
        "author": "bob",
        "body": "try this",
        "score": 2,
        "created_utc": 1700000001.0,
        "permalink": "/r/python/comments/abc123/need_a_tool/c1/",
        "depth": 0,
        "is_submitter": False,
        "replies": "",
        "all_awardings": [],
    }
    data.update(overrides)
    return {"kind": "t1", "data": data}


ENV = {
    "REDDIT_CLIENT_ID": "client-id",
    "REDDIT_CLIENT_SECRET": "supersecretvalue",
}


class TestCredentials(unittest.TestCase):
    def test_missing_both_names_env_vars_and_script_app(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                reddit.require_credentials()
        message = str(ctx.exception)
        self.assertIn("REDDIT_CLIENT_ID", message)
        self.assertIn("REDDIT_CLIENT_SECRET", message)
        self.assertIn("https://www.reddit.com/prefs/apps", message)
        self.assertIn("script", message)
        self.assertIn("platform:app:version (by /u/name)", message)

    def test_missing_secret_only(self) -> None:
        with mock.patch.dict(os.environ, {"REDDIT_CLIENT_ID": "abc"}, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                reddit.require_credentials()
        message = str(ctx.exception)
        self.assertIn("missing REDDIT_CLIENT_SECRET", message)
        self.assertIn("REDDIT_CLIENT_ID", message)
        self.assertIn("script", message)

    def test_blank_values_count_as_missing(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"REDDIT_CLIENT_ID": "  ", "REDDIT_CLIENT_SECRET": ""},
            clear=True,
        ):
            with self.assertRaises(SystemExit) as ctx:
                reddit.require_credentials()
        self.assertIn("REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET", str(ctx.exception))

    def test_returns_stripped_values(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"REDDIT_CLIENT_ID": " id ", "REDDIT_CLIENT_SECRET": " secret "},
        ):
            self.assertEqual(reddit.require_credentials(), ("id", "secret"))


class TestUserAgent(unittest.TestCase):
    def test_default_matches_contact_format_and_skill_version(self) -> None:
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        self.assertIn(f"version: {reddit.APP_VERSION}", text)
        self.assertRegex(
            reddit.DEFAULT_USER_AGENT,
            r"^[^:\s]+:[^:\s]+:[^:\s]+ \(by /u/[^)]+\)$",
        )
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(reddit.user_agent(), reddit.DEFAULT_USER_AGENT)

    def test_env_overrides_default(self) -> None:
        custom = "ios:demo:1.0 (by /u/maker)"
        with mock.patch.dict(os.environ, {"REDDIT_USER_AGENT": f"  {custom}  "}):
            self.assertEqual(reddit.user_agent(), custom)


class TestRetryAfter(unittest.TestCase):
    def test_numeric_header(self) -> None:
        headers = EmailMessage()
        headers["Retry-After"] = "2.5"
        self.assertEqual(reddit.retry_delay(headers, 0), 2.5)

    def test_http_date_header(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        headers = EmailMessage()
        headers["Retry-After"] = format_datetime(now + timedelta(seconds=7), usegmt=True)
        self.assertAlmostEqual(reddit.retry_delay(headers, 0, now=now), 7.0, places=3)

    def test_past_http_date_retries_immediately(self) -> None:
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        headers = EmailMessage()
        headers["Retry-After"] = format_datetime(now - timedelta(seconds=5), usegmt=True)
        self.assertEqual(reddit.retry_delay(headers, 3, now=now), 0.0)

    def test_missing_header_uses_backoff(self) -> None:
        self.assertEqual(reddit.retry_delay(EmailMessage(), 0), 1.0)
        self.assertEqual(reddit.retry_delay(EmailMessage(), 1), 2.0)
        self.assertEqual(reddit.retry_delay(None, 2), 4.0)

    def test_garbage_header_uses_backoff(self) -> None:
        headers = EmailMessage()
        headers["Retry-After"] = "soon"
        self.assertEqual(reddit.retry_delay(headers, 1), 2.0)

    def test_over_cap_exits_without_sleeping_forever(self) -> None:
        headers = EmailMessage()
        headers["Retry-After"] = "500"
        with self.assertRaises(SystemExit) as ctx:
            reddit.retry_delay(headers, 0)
        message = str(ctx.exception)
        self.assertIn("429", message)
        self.assertIn("500", message)
        self.assertIn("120", message)


class TestNormalize(unittest.TestCase):
    def test_subreddit_forms(self) -> None:
        samples = {
            "python": "python",
            "r/python": "python",
            "R/Python": "Python",
            "/r/python/": "python",
            "https://www.reddit.com/r/python/": "python",
            "https://old.reddit.com/r/python/hot": "python",
            "https://reddit.com/r/MachineLearning?sort=hot": "MachineLearning",
        }
        for raw, expected in samples.items():
            self.assertEqual(reddit.normalize_subreddit(raw), expected, raw)

    def test_subreddit_rejects_junk(self) -> None:
        for raw in ("", "a", "has space", "r/", "../etc", "bad/name"):
            with self.assertRaises(SystemExit):
                reddit.normalize_subreddit(raw)

    def test_post_id_forms(self) -> None:
        url = "https://www.reddit.com/r/python/comments/abc123/need_a_tool/"
        self.assertEqual(reddit.normalize_post_id("abc123"), "abc123")
        self.assertEqual(reddit.normalize_post_id("t3_abc123"), "abc123")
        self.assertEqual(reddit.normalize_post_id(url), "abc123")
        old = "https://old.reddit.com/r/python/comments/abc123/"
        self.assertEqual(reddit.normalize_post_id(old), "abc123")

    def test_post_id_rejects_junk(self) -> None:
        with self.assertRaises(SystemExit):
            reddit.normalize_post_id("not an id")


class TestTrim(unittest.TestCase):
    def test_post_drops_media_and_marks_long_selftext(self) -> None:
        long_text = "x" * (reddit.POST_TEXT_LIMIT + 5)
        trimmed = reddit.trim_post(_post(selftext=long_text, is_self=True)["data"])
        self.assertNotIn("preview", trimmed)
        self.assertNotIn("media", trimmed)
        self.assertNotIn("all_awardings", trimmed)
        self.assertEqual(trimmed["permalink"], "https://www.reddit.com/r/python/comments/abc123/need_a_tool/")
        self.assertEqual(len(trimmed["selftext"]), reddit.POST_TEXT_LIMIT)
        self.assertTrue(trimmed["selftext_truncated"])
        self.assertEqual(trimmed["title"], "Need a tool")

    def test_subreddit_prefers_active_user_count(self) -> None:
        trimmed = reddit.trim_subreddit(
            {
                "display_name": "python",
                "title": "Python",
                "public_description": "news",
                "description": "rules " * 10,
                "subscribers": 1000,
                "active_user_count": 12,
                "accounts_active": 99,
                "created_utc": 10,
                "over18": False,
                "subreddit_type": "public",
                "url": "/r/python/",
                "submission_type": "any",
                "submit_text": "be kind",
                "community_icon": "https://styles.example/icon.png",
            }
        )
        self.assertEqual(trimmed["active_users"], 12)
        self.assertEqual(trimmed["url"], "https://www.reddit.com/r/python/")
        self.assertNotIn("community_icon", trimmed)
        self.assertFalse(trimmed["description_truncated"])

    def test_comment_tree_keeps_more_placeholder(self) -> None:
        nested = _comment(
            replies={
                "kind": "Listing",
                "data": {
                    "children": [
                        _comment(id="c2", body="y", depth=1, replies=""),
                        {"kind": "more", "data": {"id": "m1", "count": 4, "children": ["a", "b"]}},
                    ]
                },
            }
        )
        trimmed = reddit.trim_comment(nested["data"])
        self.assertEqual(trimmed["kind"], "comment")
        self.assertEqual(trimmed["replies"][0]["id"], "c2")
        self.assertEqual(trimmed["replies"][0]["replies"], [])
        self.assertEqual(trimmed["replies"][1], {"kind": "more", "id": "m1", "count": 4})
        self.assertNotIn("all_awardings", trimmed)


class TestClient(unittest.TestCase):
    def _client(self, **kwargs: object) -> reddit.RedditClient:
        return reddit.RedditClient(
            "client-id",
            "supersecretvalue",
            kwargs.pop("ua", reddit.DEFAULT_USER_AGENT),
            sleeper=kwargs.pop("sleeper", lambda _seconds: None),
            clock=kwargs.pop("clock", lambda: 1_000.0),
        )

    def _request(self, urlopen: mock.Mock, index: int) -> urllib.request.Request:
        return urlopen.call_args_list[index].args[0]

    @mock.patch("urllib.request.urlopen")
    def test_token_request_is_client_credentials_basic_auth(self, urlopen: mock.Mock) -> None:
        urlopen.return_value = _ok(_token())
        client = self._client()
        self.assertEqual(client.access_token(), "token-1")
        req = self._request(urlopen, 0)
        self.assertEqual(req.full_url, reddit.TOKEN_URL)
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.data.decode(), "grant_type=client_credentials")
        self.assertNotIn("supersecretvalue", req.data.decode())
        encoded = req.get_header("Authorization").split(" ", 1)[1]
        self.assertEqual(base64.b64decode(encoded).decode(), "client-id:supersecretvalue")
        self.assertEqual(req.get_header("User-agent"), reddit.DEFAULT_USER_AGENT)

    @mock.patch("urllib.request.urlopen")
    def test_reuses_token_until_expiry_then_refreshes(self, urlopen: mock.Mock) -> None:
        now = {"t": 1_000.0}
        urlopen.side_effect = [
            _ok(_token("first")),
            _ok(_listing(_post())),
            _ok(_listing(_post())),
            _ok(_token("second")),
            _ok(_listing(_post())),
        ]
        client = self._client(clock=lambda: now["t"])
        client.get("/search", {"q": "a"})
        now["t"] = 1_000.0 + 3600 - reddit.TOKEN_SKEW_SECONDS - 1
        client.get("/search", {"q": "b"})
        now["t"] = 1_000.0 + 3600 - reddit.TOKEN_SKEW_SECONDS
        client.get("/search", {"q": "c"})
        token_posts = [
            call.args[0].full_url
            for call in urlopen.call_args_list
            if call.args[0].full_url == reddit.TOKEN_URL
        ]
        self.assertEqual(len(token_posts), 2)
        self.assertEqual(self._request(urlopen, 1).get_header("Authorization"), "bearer first")
        self.assertEqual(self._request(urlopen, 2).get_header("Authorization"), "bearer first")
        self.assertEqual(self._request(urlopen, 4).get_header("Authorization"), "bearer second")

    @mock.patch("urllib.request.urlopen")
    def test_429_honors_retry_after_then_succeeds(self, urlopen: mock.Mock) -> None:
        sleeps: list[float] = []
        urlopen.side_effect = [
            _ok(_token()),
            _http_error(429, {"Retry-After": "2"}),
            _ok(_listing()),
        ]
        client = self._client(sleeper=sleeps.append)
        payload = client.get("/search", {"q": "tool"})
        self.assertEqual(payload["kind"], "Listing")
        self.assertEqual(sleeps, [2.0])
        self.assertEqual(urlopen.call_count, 3)

    @mock.patch("urllib.request.urlopen")
    def test_429_without_header_backs_off_then_stops(self, urlopen: mock.Mock) -> None:
        sleeps: list[float] = []
        urlopen.side_effect = [_http_error(429) for _ in range(reddit.MAX_ATTEMPTS)]
        with self.assertRaises(SystemExit) as ctx:
            reddit.request_json(
                reddit.API_ROOT + "/search",
                method="GET",
                headers={"User-Agent": "ua"},
                sleeper=sleeps.append,
            )
        self.assertEqual(sleeps, [1.0, 2.0, 4.0])
        self.assertIn("still rate limited", str(ctx.exception))
        self.assertEqual(urlopen.call_count, reddit.MAX_ATTEMPTS)

    @mock.patch("urllib.request.urlopen")
    def test_429_over_cap_does_not_sleep(self, urlopen: mock.Mock) -> None:
        sleeps: list[float] = []
        urlopen.side_effect = [
            _ok(_token()),
            _http_error(429, {"Retry-After": "500"}, b'{"message":"slow down"}'),
        ]
        client = self._client(sleeper=sleeps.append)
        with self.assertRaises(SystemExit) as ctx:
            client.get("/search", {"q": "tool"})
        self.assertEqual(sleeps, [])
        self.assertIn("500", str(ctx.exception))

    @mock.patch("urllib.request.urlopen")
    def test_401_refreshes_token_once(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token("stale")),
            _http_error(401, body=b'{"message":"unauthorized"}'),
            _ok(_token("fresh")),
            _ok(_listing(_post())),
        ]
        client = self._client()
        payload = client.get("/r/python/about", {})
        self.assertEqual(payload["kind"], "Listing")
        self.assertEqual(self._request(urlopen, 3).get_header("Authorization"), "bearer fresh")

    @mock.patch("urllib.request.urlopen")
    def test_second_401_stops(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token("stale")),
            _http_error(401),
            _ok(_token("fresh")),
            _http_error(401, body=b'{"message":"nope"}'),
        ]
        client = self._client()
        with self.assertRaises(SystemExit) as ctx:
            client.get("/search", {"q": "x"})
        message = str(ctx.exception)
        self.assertIn("401", message)
        self.assertIn(reddit.PREFS_URL, message)

    @mock.patch("urllib.request.urlopen")
    def test_error_redacts_secret_and_access_token(self, urlopen: mock.Mock) -> None:
        body = b'{"error":"bad","echo":"supersecretvalue","access_token":"leaked-token"}'
        urlopen.side_effect = _http_error(401, body=body)
        with self.assertRaises(SystemExit) as ctx:
            reddit.fetch_token("client-id", "supersecretvalue", reddit.DEFAULT_USER_AGENT)
        message = str(ctx.exception)
        self.assertNotIn("supersecretvalue", message)
        self.assertNotIn("leaked-token", message)
        self.assertIn("***", message)

    @mock.patch("urllib.request.urlopen")
    def test_token_error_field_on_200(self, urlopen: mock.Mock) -> None:
        urlopen.return_value = _ok({"error": "unauthorized_client"})
        with self.assertRaises(SystemExit) as ctx:
            reddit.fetch_token("client-id", "supersecretvalue", reddit.DEFAULT_USER_AGENT)
        self.assertIn("unauthorized_client", str(ctx.exception))
        self.assertIn("script app", str(ctx.exception))

    @mock.patch("urllib.request.urlopen")
    def test_custom_user_agent_on_token_and_get(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [_ok(_token()), _ok(_listing())]
        custom = "web:outreach:2 (by /u/maker)"
        client = self._client(ua=custom)
        client.get("/search", {"q": "x"})
        self.assertEqual(self._request(urlopen, 0).get_header("User-agent"), custom)
        self.assertEqual(self._request(urlopen, 1).get_header("User-agent"), custom)

    @mock.patch("urllib.request.urlopen")
    def test_disk_cache_reused_across_clients(self, urlopen: mock.Mock) -> None:
        now = {"t": 1_000.0}
        urlopen.side_effect = [
            _ok(_token("cached-token")),
            _ok(_listing(_post())),
            _ok(_listing(_post())),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "token.json"
            first = reddit.RedditClient(
                "client-id",
                "supersecretvalue",
                "ua",
                clock=lambda: now["t"],
                cache_path=path,
            )
            first.get("/search", {"q": "a"})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            stored = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(stored), {"client_id", "access_token", "expires_at"})
            self.assertNotIn("supersecretvalue", path.read_text(encoding="utf-8"))
            second = reddit.RedditClient(
                "client-id",
                "supersecretvalue",
                "ua",
                clock=lambda: now["t"],
                cache_path=path,
            )
            second.get("/search", {"q": "b"})
        token_calls = [
            call.args[0]
            for call in urlopen.call_args_list
            if call.args[0].full_url == reddit.TOKEN_URL
        ]
        self.assertEqual(len(token_calls), 1)
        self.assertEqual(
            urlopen.call_args_list[2].args[0].get_header("Authorization"),
            "bearer cached-token",
        )

    @mock.patch("urllib.request.urlopen")
    def test_disk_cache_ignores_other_client_and_expiry(self, urlopen: mock.Mock) -> None:
        now = {"t": 1_000.0}
        urlopen.side_effect = [
            _ok(_token("one")),
            _ok(_listing()),
            _ok(_token("two")),
            _ok(_listing()),
            _ok(_token("three")),
            _ok(_listing()),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "token.json"
            reddit.RedditClient(
                "client-id",
                "supersecretvalue",
                "ua",
                clock=lambda: now["t"],
                cache_path=path,
            ).get("/search", {"q": "a"})
            reddit.RedditClient(
                "other-client",
                "supersecretvalue",
                "ua",
                clock=lambda: now["t"],
                cache_path=path,
            ).get("/search", {"q": "b"})
            now["t"] = 1_000.0 + 3600
            reddit.RedditClient(
                "other-client",
                "supersecretvalue",
                "ua",
                clock=lambda: now["t"],
                cache_path=path,
            ).get("/search", {"q": "c"})
        self.assertEqual(
            sum(call.args[0].full_url == reddit.TOKEN_URL for call in urlopen.call_args_list),
            3,
        )

    @mock.patch("urllib.request.urlopen")
    def test_401_drops_disk_cache(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token("stale")),
            _ok(_listing()),
            _http_error(401),
            _ok(_token("fresh")),
            _ok(_listing()),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "token.json"
            client = reddit.RedditClient(
                "client-id",
                "supersecretvalue",
                "ua",
                cache_path=path,
            )
            client.get("/search", {"q": "a"})
            self.assertTrue(path.is_file())
            client.get("/search", {"q": "b"})
            stored = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(stored["access_token"], "fresh")


class TestCommands(unittest.TestCase):
    def _urls(self, urlopen: mock.Mock) -> list[str]:
        return [call.args[0].full_url for call in urlopen.call_args_list]

    def _query(self, url: str) -> dict[str, list[str]]:
        return urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)

    @mock.patch("urllib.request.urlopen")
    def test_global_search_path_and_params(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [_ok(_token()), _ok(_listing(_post()))]
        result = reddit.cmd_search(
            reddit.RedditClient("client-id", "supersecretvalue", "ua"),
            q='looking for a "tool"',
            sort="new",
            t="week",
            limit=5,
            subreddit=None,
            restrict_sr=False,
        )
        urls = self._urls(urlopen)
        self.assertTrue(all(".json" not in url for url in urls))
        data_url = urls[1]
        self.assertTrue(data_url.startswith("https://oauth.reddit.com/search?"))
        query = self._query(data_url)
        self.assertEqual(query["q"], ['looking for a "tool"'])
        self.assertEqual(query["sort"], ["new"])
        self.assertEqual(query["t"], ["week"])
        self.assertEqual(query["limit"], ["5"])
        self.assertEqual(query["restrict_sr"], ["false"])
        self.assertEqual(query["type"], ["link"])
        self.assertEqual(query["raw_json"], ["1"])
        self.assertEqual(result["posts"][0]["id"], "abc123")
        self.assertNotIn("preview", json.dumps(result))

    @mock.patch("urllib.request.urlopen")
    def test_subreddit_search_sets_restrict_sr(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [_ok(_token()), _ok(_listing())]
        reddit.cmd_search(
            reddit.RedditClient("client-id", "supersecretvalue", "ua"),
            q="alternative",
            sort="relevance",
            t="month",
            limit=10,
            subreddit="python",
            restrict_sr=True,
        )
        data_url = self._urls(urlopen)[1]
        self.assertTrue(data_url.startswith("https://oauth.reddit.com/r/python/search?"))
        self.assertEqual(self._query(data_url)["restrict_sr"], ["true"])

    @mock.patch("urllib.request.urlopen")
    def test_subreddit_fetches_about_and_listing_with_one_token(self, urlopen: mock.Mock) -> None:
        about = {
            "kind": "t5",
            "data": {
                "display_name": "python",
                "title": "Python",
                "public_description": "news about the language",
                "description": "No spam.",
                "subscribers": 50,
                "accounts_active": 3,
                "created_utc": 10,
                "over18": False,
                "subreddit_type": "public",
                "url": "/r/python/",
                "submission_type": "any",
                "submit_text": "",
            },
        }
        urlopen.side_effect = [_ok(_token()), _ok(about), _ok(_listing(_post()))]
        result = reddit.cmd_subreddit(
            reddit.RedditClient("client-id", "supersecretvalue", "ua"),
            name="python",
            sort="hot",
            t=None,
            limit=5,
        )
        urls = self._urls(urlopen)
        self.assertEqual(sum(url == reddit.TOKEN_URL for url in urls), 1)
        self.assertTrue(urls[1].startswith("https://oauth.reddit.com/r/python/about?"))
        self.assertTrue(urls[2].startswith("https://oauth.reddit.com/r/python/hot?"))
        self.assertEqual(self._query(urls[2])["limit"], ["5"])
        self.assertNotIn("t", self._query(urls[2]))
        self.assertEqual(result["subreddit"]["subscribers"], 50)
        self.assertEqual(result["subreddit"]["active_users"], 3)
        self.assertEqual(result["posts"][0]["subreddit"], "python")

    @mock.patch("urllib.request.urlopen")
    def test_top_listing_sends_t(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token()),
            _ok({"kind": "t5", "data": {"display_name": "python"}}),
            _ok(_listing()),
        ]
        reddit.cmd_subreddit(
            reddit.RedditClient("client-id", "supersecretvalue", "ua"),
            name="python",
            sort="top",
            t="year",
            limit=3,
        )
        listing_url = self._urls(urlopen)[2]
        self.assertTrue(listing_url.startswith("https://oauth.reddit.com/r/python/top?"))
        self.assertEqual(self._query(listing_url)["t"], ["year"])

    @mock.patch("urllib.request.urlopen")
    def test_post_comments_params_and_trim(self, urlopen: mock.Mock) -> None:
        payload = [
            _listing(_post(selftext="body")),
            _listing(_comment(), {"kind": "more", "data": {"count": 2, "id": "more1"}}),
        ]
        urlopen.side_effect = [_ok(_token()), _ok(payload)]
        result = reddit.cmd_post(
            reddit.RedditClient("client-id", "supersecretvalue", "ua"),
            subreddit="python",
            post_id="abc123",
            limit=10,
            sort="confidence",
            depth=2,
        )
        data_url = self._urls(urlopen)[1]
        self.assertTrue(data_url.startswith("https://oauth.reddit.com/r/python/comments/abc123?"))
        query = self._query(data_url)
        self.assertEqual(query["limit"], ["10"])
        self.assertEqual(query["sort"], ["confidence"])
        self.assertEqual(query["depth"], ["2"])
        self.assertEqual(query["raw_json"], ["1"])
        self.assertEqual(result["post"]["selftext"], "body")
        self.assertEqual(result["comments"][0]["author"], "bob")
        self.assertEqual(result["comments"][1]["kind"], "more")
        self.assertNotIn("access_token", json.dumps(result))


class TestMain(unittest.TestCase):
    @mock.patch("urllib.request.urlopen")
    def test_prints_trimmed_json(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [_ok(_token()), _ok(_listing(_post(title="中文标题")))]
        buf = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            env = {**ENV, "XDG_CACHE_HOME": tmp}
            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch("sys.argv", ["reddit.py", "search", "--q", "tool", "--t", "month"]):
                    with mock.patch("sys.stdout", buf):
                        code = reddit.main()
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["q"], "tool")
        self.assertEqual(payload["t"], "month")
        self.assertEqual(payload["posts"][0]["title"], "中文标题")
        self.assertNotIn("supersecretvalue", buf.getvalue())
        self.assertNotIn("token-1", buf.getvalue())

    @mock.patch("urllib.request.urlopen")
    def test_subreddit_top_defaults_time_window(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token()),
            _ok({"kind": "t5", "data": {"display_name": "python", "subscribers": 1}}),
            _ok(_listing()),
        ]
        buf = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            env = {**ENV, "XDG_CACHE_HOME": tmp}
            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch("sys.argv", ["reddit.py", "subreddit", "r/python", "--sort", "top"]):
                    with mock.patch("sys.stdout", buf):
                        reddit.main()
        listing = urlopen.call_args_list[2].args[0].full_url
        self.assertIn("/r/python/top?", listing)
        self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(listing).query)["t"], ["all"])
        self.assertEqual(json.loads(buf.getvalue())["subreddit"]["name"], "python")

    @mock.patch("urllib.request.urlopen")
    def test_post_accepts_comment_url(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [
            _ok(_token()),
            _ok([_listing(_post()), _listing(_comment())]),
        ]
        buf = io.StringIO()
        link = "https://old.reddit.com/r/Python/comments/abc123/title/"
        with tempfile.TemporaryDirectory() as tmp:
            env = {**ENV, "XDG_CACHE_HOME": tmp}
            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch("sys.argv", ["reddit.py", "post", "r/Python", link, "--limit", "8"]):
                    with mock.patch("sys.stdout", buf):
                        reddit.main()
        data_url = urlopen.call_args_list[1].args[0].full_url
        self.assertTrue(data_url.startswith("https://oauth.reddit.com/r/Python/comments/abc123?"))
        self.assertEqual(json.loads(buf.getvalue())["id"], "abc123")

    def test_missing_creds_from_main(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch("sys.argv", ["reddit.py", "search", "--q", "tool"]):
                with self.assertRaises(SystemExit) as ctx:
                    reddit.main()
        message = str(ctx.exception)
        self.assertIn("REDDIT_CLIENT_ID", message)
        self.assertIn("REDDIT_CLIENT_SECRET", message)
        self.assertIn("prefs/apps", message)
        self.assertIn("script", message)

    def test_help_does_not_need_credentials(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch("sys.argv", ["reddit.py", "--help"]):
                with mock.patch("sys.stdout", io.StringIO()):
                    with self.assertRaises(SystemExit) as ctx:
                        reddit.main()
        self.assertEqual(ctx.exception.code, 0)

    @mock.patch("urllib.request.urlopen")
    def test_search_subreddit_defaults_restrict_sr(self, urlopen: mock.Mock) -> None:
        urlopen.side_effect = [_ok(_token()), _ok(_listing())]
        buf = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            env = {**ENV, "XDG_CACHE_HOME": tmp}
            argv = ["reddit.py", "search", "--q", "tool", "--subreddit", "r/python"]
            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch("sys.argv", argv):
                    with mock.patch("sys.stdout", buf):
                        reddit.main()
        data_url = urlopen.call_args_list[1].args[0].full_url
        self.assertTrue(data_url.startswith("https://oauth.reddit.com/r/python/search?"))
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(data_url).query)
        self.assertEqual(query["restrict_sr"], ["true"])
        self.assertEqual(json.loads(buf.getvalue())["subreddit"], "python")

    def test_commands_are_read_only_set(self) -> None:
        parser = reddit.build_parser()
        choices = set(parser._subparsers._group_actions[0].choices)
        self.assertEqual(choices, set(reddit.COMMANDS))

    def test_source_has_no_builtin_creds_or_json_listing(self) -> None:
        text = Path(reddit.__file__).read_text(encoding="utf-8")
        self.assertNotIn("reddit-mcp", text)
        self.assertNotRegex(text, r"reddit\.com/\S+\.json")
        for banned in ("/api/submit", "/api/comment", "/api/vote", "/api/compose", "/api/del"):
            self.assertNotIn(banned, text)
        self.assertEqual(reddit.TOKEN_URL, "https://www.reddit.com/api/v1/access_token")
        self.assertEqual(reddit.API_ROOT, "https://oauth.reddit.com")


if __name__ == "__main__":
    unittest.main()
