#!/usr/bin/env python3
"""Read-only Reddit client using official app-only OAuth.

Usage:
    REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... python reddit.py search --q "looking for a tool"
    python reddit.py subreddit python --sort hot
    python reddit.py post python abc123

POST https://www.reddit.com/api/v1/access_token with grant_type=client_credentials
(HTTP Basic auth is the client id and secret). Data calls go to
https://oauth.reddit.com only. The bearer token is reused until expires_at,
including across processes via a 0600 file under the XDG cache home. HTTP 429
sleeps for Retry-After (capped) and retries. Stdout is trimmed JSON.

No built-in credentials. Does not call unauthenticated .json listings.
Create a script app at https://www.reddit.com/prefs/apps.
"""

from __future__ import annotations

import argparse
import base64
import email.utils
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_ROOT = "https://oauth.reddit.com"
PREFS_URL = "https://www.reddit.com/prefs/apps"
APP_VERSION = "1.2.0"
DEFAULT_USER_AGENT = f"python:reddit-promotion:{APP_VERSION} (by /u/reddit-promotion)"

SEARCH_SORTS = ("relevance", "hot", "top", "new", "comments")
LISTING_SORTS = ("hot", "new", "top", "rising")
COMMENT_SORTS = ("confidence", "top", "new", "controversial", "old", "qa")
TIME_WINDOWS = ("hour", "day", "week", "month", "year", "all")
COMMANDS = ("search", "subreddit", "post")

MAX_ATTEMPTS = 4
MAX_RETRY_WAIT = 120.0
TOKEN_SKEW_SECONDS = 30.0
POST_TEXT_LIMIT = 1500
COMMENT_TEXT_LIMIT = 1000
DESCRIPTION_LIMIT = 2000
SUBMIT_TEXT_LIMIT = 500

_SUBREDDIT_IN_TEXT = re.compile(
    r"(?:^|/)r/([A-Za-z0-9_]{2,21})(?:/|$|\?|#)",
    re.IGNORECASE,
)
_POST_IN_URL = re.compile(r"/comments/([A-Za-z0-9]+)", re.IGNORECASE)


def require_credentials() -> tuple[str, str]:
    client_id = os.environ.get("REDDIT_CLIENT_ID", "").strip()
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "").strip()
    missing = [
        name
        for name, value in (
            ("REDDIT_CLIENT_ID", client_id),
            ("REDDIT_CLIENT_SECRET", client_secret),
        )
        if not value
    ]
    if missing:
        raise SystemExit(
            "ERROR: missing "
            + " and ".join(missing)
            + ".\n"
            "Create a script app at "
            + PREFS_URL
            + " (type: script). Export REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.\n"
            "Optional REDDIT_USER_AGENT: platform:app:version (by /u/name)."
        )
    return client_id, client_secret


def user_agent() -> str:
    custom = os.environ.get("REDDIT_USER_AGENT", "").strip()
    return custom or DEFAULT_USER_AGENT


def default_cache_path() -> Path:
    root = os.environ.get("XDG_CACHE_HOME", "").strip()
    base = Path(root) if root else Path.home() / ".cache"
    return base / "reddit-promotion" / "token.json"


def normalize_subreddit(raw: str) -> str:
    text = raw.strip()
    found = _SUBREDDIT_IN_TEXT.search(text)
    if found and ("/" in text or text.lower().startswith("r/")):
        text = found.group(1)
    else:
        text = text.split("?", 1)[0].split("#", 1)[0].strip("/")
    if not re.fullmatch(r"[A-Za-z0-9_]{2,21}", text):
        raise SystemExit(f"Invalid subreddit name: {raw}")
    return text


def normalize_post_id(raw: str) -> str:
    text = raw.strip()
    found = _POST_IN_URL.search(text)
    if found:
        text = found.group(1)
    elif text.startswith("t3_"):
        text = text[3:]
    else:
        text = text.split("?", 1)[0].split("#", 1)[0].strip("/")
    if not re.fullmatch(r"[A-Za-z0-9]{2,15}", text):
        raise SystemExit(f"Invalid post id: {raw}")
    return text


def _header(headers: object, name: str) -> str | None:
    if headers is None:
        return None
    getter = getattr(headers, "get", None)
    if not callable(getter):
        return None
    value = getter(name)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_retry_after(headers: object, *, now: datetime | None = None) -> float | None:
    """Return Retry-After in seconds, or None when the header is absent or invalid."""
    raw = _header(headers, "Retry-After")
    if raw is None:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    current = now or datetime.now(timezone.utc)
    return max(0.0, (parsed - current).total_seconds())


def retry_delay(headers: object, attempt: int, *, now: datetime | None = None) -> float:
    """Seconds to sleep before another try. Exits when Retry-After is above the cap."""
    seconds = parse_retry_after(headers, now=now)
    if seconds is None:
        seconds = min(2.0**attempt, 30.0)
    if seconds > MAX_RETRY_WAIT:
        raise SystemExit(
            f"HTTP 429 from Reddit. Retry-After is {seconds:.0f}s, "
            f"above the {MAX_RETRY_WAIT:.0f}s cap. Try again later."
        )
    return seconds


def redact(text: str, secret: str | None = None) -> str:
    if secret and len(secret) >= 8:
        text = text.replace(secret, "***")
    text = re.sub(
        r'("access_token"\s*:\s*")[^"]*"',
        r'\1***"',
        text,
    )
    if len(text) > 400:
        text = text[:400] + "..."
    return text


def _error_body(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read()
    except Exception:
        return ""
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="replace")
    return str(raw or "")


class RedditHTTPError(Exception):
    def __init__(self, code: int, body: str):
        super().__init__(body)
        self.code = code
        self.body = body


def request_json(
    url: str,
    *,
    method: str,
    headers: dict[str, str],
    data: bytes | None = None,
    sleeper=time.sleep,
    secret: str | None = None,
    attempts: int = MAX_ATTEMPTS,
) -> object:
    last_body = ""
    for attempt in range(attempts):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                status = getattr(resp, "status", 200)
        except urllib.error.HTTPError as exc:
            body = _error_body(exc)
            last_body = body
            if exc.code == 429 and attempt + 1 < attempts:
                sleeper(retry_delay(exc.headers, attempt))
                continue
            if exc.code == 429:
                raise SystemExit(
                    "HTTP 429 from Reddit: still rate limited after retries. "
                    + redact(body, secret)
                )
            raise RedditHTTPError(exc.code, body)
        except urllib.error.URLError as exc:
            raise SystemExit(f"Network error reaching Reddit: {exc.reason}")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            raise SystemExit(
                f"Reddit returned non-JSON (HTTP {status}): {redact(raw, secret)}"
            )
        return payload
    raise SystemExit(
        "HTTP 429 from Reddit: still rate limited after retries. "
        + redact(last_body, secret)
    )


def oauth_url(path: str, params: dict[str, str | int]) -> str:
    query = urllib.parse.urlencode(params)
    if not path.startswith("/"):
        path = "/" + path
    return f"{API_ROOT}{path}?{query}" if query else f"{API_ROOT}{path}"


def fetch_token(
    client_id: str,
    client_secret: str,
    ua: str,
    *,
    sleeper=time.sleep,
) -> tuple[str, float]:
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    try:
        payload = request_json(
            TOKEN_URL,
            method="POST",
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "User-Agent": ua,
            },
            data=data,
            sleeper=sleeper,
            secret=client_secret,
        )
    except RedditHTTPError as exc:
        raise SystemExit(
            f"HTTP {exc.code} from Reddit token endpoint: {redact(exc.body, client_secret)}. "
            "Check REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET from a script app at "
            f"{PREFS_URL}."
        )
    if not isinstance(payload, dict):
        raise SystemExit("Reddit token response was not a JSON object.")
    if payload.get("error"):
        raise SystemExit(
            "Reddit token request failed: "
            + str(payload.get("error"))
            + ". Check REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET "
            f"from a script app at {PREFS_URL}."
        )
    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise SystemExit("Reddit token response did not include access_token.")
    try:
        expires_in = float(payload["expires_in"])
    except (KeyError, TypeError, ValueError):
        raise SystemExit("Reddit token response did not include expires_in.")
    if expires_in <= 0:
        raise SystemExit("Reddit token response did not include expires_in.")
    return token, expires_in


class RedditClient:
    """App-only client. Reuses one bearer token until expires_at."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        ua: str,
        *,
        sleeper=time.sleep,
        clock=time.time,
        cache_path: Path | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.ua = ua
        self.sleeper = sleeper
        self.clock = clock
        self.cache_path = cache_path
        self._token: str | None = None
        self._expires_at = 0.0

    def access_token(self) -> str:
        now = self.clock()
        if self._token is not None and now < self._expires_at:
            return self._token
        self._read_cache()
        now = self.clock()
        if self._token is not None and now < self._expires_at:
            return self._token
        token, expires_in = fetch_token(
            self.client_id,
            self.client_secret,
            self.ua,
            sleeper=self.sleeper,
        )
        skew = min(TOKEN_SKEW_SECONDS, expires_in / 2)
        self._token = token
        self._expires_at = now + (expires_in - skew)
        self._write_cache()
        return self._token

    def invalidate(self) -> None:
        self._token = None
        self._expires_at = 0.0
        path = self.cache_path
        if path is None:
            return
        try:
            path.unlink(missing_ok=True)
        except OSError:
            return

    def _read_cache(self) -> None:
        path = self.cache_path
        if path is None:
            return
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeError):
            return
        if not isinstance(payload, dict) or payload.get("client_id") != self.client_id:
            return
        token = payload.get("access_token")
        try:
            expires_at = float(payload["expires_at"])
        except (KeyError, TypeError, ValueError):
            return
        if not isinstance(token, str) or not token or self.clock() >= expires_at:
            return
        self._token = token
        self._expires_at = expires_at

    def _write_cache(self) -> None:
        path = self.cache_path
        if path is None or self._token is None:
            return
        blob = json.dumps(
            {
                "client_id": self.client_id,
                "access_token": self._token,
                "expires_at": self._expires_at,
            }
        ).encode()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            try:
                os.write(fd, blob)
            finally:
                os.close(fd)
            os.chmod(path, 0o600)
        except OSError:
            return

    def get(self, path: str, params: dict[str, str | int] | None = None) -> object:
        return self._get(path, params or {}, allow_refresh=True)

    def _get(self, path: str, params: dict[str, str | int], *, allow_refresh: bool) -> object:
        query = {"raw_json": "1", **params}
        url = oauth_url(path, query)
        token = self.access_token()
        try:
            return request_json(
                url,
                method="GET",
                headers={
                    "Authorization": f"bearer {token}",
                    "Accept": "application/json",
                    "User-Agent": self.ua,
                },
                sleeper=self.sleeper,
                secret=self.client_secret,
            )
        except RedditHTTPError as exc:
            if exc.code == 401 and allow_refresh:
                self.invalidate()
                return self._get(path, params, allow_refresh=False)
            hint = ""
            if exc.code == 401:
                hint = (
                    " Check REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET "
                    f"from a script app at {PREFS_URL}."
                )
            elif exc.code == 403:
                hint = (
                    " Reddit may be rejecting the User-Agent. "
                    "Set REDDIT_USER_AGENT to platform:app:version (by /u/name)."
                )
            raise SystemExit(
                f"HTTP {exc.code} from Reddit: {redact(exc.body, self.client_secret)}.{hint}"
            )


def build_client() -> RedditClient:
    client_id, client_secret = require_credentials()
    return RedditClient(
        client_id,
        client_secret,
        user_agent(),
        cache_path=default_cache_path(),
    )


def truncate(text: str, limit: int) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def absolute_reddit_url(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    if value.startswith("https://") or value.startswith("http://"):
        return value
    if not value.startswith("/"):
        value = "/" + value
    return "https://www.reddit.com" + value


def _number(value: object) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def trim_post(data: dict) -> dict:
    selftext, truncated = truncate(str(data.get("selftext") or ""), POST_TEXT_LIMIT)
    return {
        "id": data.get("id"),
        "title": data.get("title"),
        "subreddit": data.get("subreddit"),
        "author": data.get("author"),
        "score": _number(data.get("score")),
        "upvote_ratio": _number(data.get("upvote_ratio")),
        "num_comments": _number(data.get("num_comments")),
        "created_utc": _number(data.get("created_utc")),
        "url": data.get("url"),
        "permalink": absolute_reddit_url(data.get("permalink")),
        "is_self": bool(data.get("is_self")),
        "over_18": bool(data.get("over_18")),
        "stickied": bool(data.get("stickied")),
        "locked": bool(data.get("locked")),
        "link_flair_text": data.get("link_flair_text"),
        "selftext": selftext,
        "selftext_truncated": truncated,
    }


def trim_subreddit(data: dict) -> dict:
    description, description_truncated = truncate(
        str(data.get("description") or ""),
        DESCRIPTION_LIMIT,
    )
    submit_text, submit_truncated = truncate(
        str(data.get("submit_text") or ""),
        SUBMIT_TEXT_LIMIT,
    )
    active = data.get("active_user_count")
    if active is None:
        active = data.get("accounts_active")
    name = data.get("display_name")
    url = absolute_reddit_url(data.get("url"))
    if url is None and isinstance(name, str) and name:
        url = f"https://www.reddit.com/r/{name}/"
    over_18 = data.get("over18")
    if over_18 is None:
        over_18 = data.get("over_18")
    return {
        "name": name,
        "title": data.get("title"),
        "public_description": data.get("public_description") or "",
        "description": description,
        "description_truncated": description_truncated,
        "subscribers": _number(data.get("subscribers")),
        "active_users": _number(active),
        "created_utc": _number(data.get("created_utc")),
        "over_18": bool(over_18),
        "subreddit_type": data.get("subreddit_type"),
        "url": url,
        "submission_type": data.get("submission_type"),
        "submit_text": submit_text,
        "submit_text_truncated": submit_truncated,
    }


def _trim_child(child: object) -> dict | None:
    if not isinstance(child, dict):
        return None
    kind = child.get("kind")
    data = child.get("data")
    if not isinstance(data, dict):
        return None
    if kind == "t1":
        return trim_comment(data)
    if kind == "more":
        return {
            "kind": "more",
            "id": data.get("id"),
            "count": _number(data.get("count")),
        }
    return None


def _reply_children(replies: object) -> list[dict]:
    if not isinstance(replies, dict):
        return []
    data = replies.get("data")
    if not isinstance(data, dict):
        return []
    children = data.get("children")
    if not isinstance(children, list):
        return []
    trimmed = [_trim_child(child) for child in children]
    return [item for item in trimmed if item is not None]


def trim_comment(data: dict) -> dict:
    body, truncated = truncate(str(data.get("body") or ""), COMMENT_TEXT_LIMIT)
    return {
        "kind": "comment",
        "id": data.get("id"),
        "author": data.get("author"),
        "body": body,
        "body_truncated": truncated,
        "score": _number(data.get("score")),
        "created_utc": _number(data.get("created_utc")),
        "permalink": absolute_reddit_url(data.get("permalink")),
        "depth": _number(data.get("depth")),
        "is_submitter": bool(data.get("is_submitter")),
        "replies": _reply_children(data.get("replies")),
    }


def _listing_children(payload: object, label: str) -> list:
    if not isinstance(payload, dict):
        raise SystemExit(f"Unexpected Reddit {label} payload.")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise SystemExit(f"Unexpected Reddit {label} payload.")
    children = data.get("children")
    if not isinstance(children, list):
        raise SystemExit(f"Unexpected Reddit {label} payload.")
    return children


def listing_posts(payload: object) -> list[dict]:
    posts: list[dict] = []
    for child in _listing_children(payload, "listing"):
        if not isinstance(child, dict) or child.get("kind") != "t3":
            continue
        data = child.get("data")
        if isinstance(data, dict):
            posts.append(trim_post(data))
    return posts


def listing_comments(payload: object) -> list[dict]:
    comments: list[dict] = []
    for child in _listing_children(payload, "comments"):
        trimmed = _trim_child(child)
        if trimmed is not None:
            comments.append(trimmed)
    return comments


def about_data(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise SystemExit("Unexpected Reddit about payload.")
    data = payload.get("data")
    if not isinstance(data, dict) or not data.get("display_name"):
        raise SystemExit("Unexpected Reddit about payload.")
    return data


def split_comments_payload(payload: object) -> tuple[dict, list[dict]]:
    if not isinstance(payload, list) or len(payload) < 2:
        raise SystemExit("Unexpected Reddit comments payload.")
    posts = listing_posts(payload[0])
    if not posts:
        raise SystemExit("Reddit comments response did not include the post.")
    return posts[0], listing_comments(payload[1])


def _quote_path(segment: str) -> str:
    return urllib.parse.quote(segment, safe="")


def cmd_search(
    client: RedditClient,
    *,
    q: str,
    sort: str,
    t: str,
    limit: int,
    subreddit: str | None,
    restrict_sr: bool,
) -> dict:
    if subreddit:
        path = f"/r/{_quote_path(subreddit)}/search"
    else:
        path = "/search"
    # type=link keeps discovery on posts. Subreddit metadata comes from `subreddit`.
    payload = client.get(
        path,
        {
            "q": q,
            "sort": sort,
            "t": t,
            "limit": limit,
            "restrict_sr": "true" if restrict_sr else "false",
            "type": "link",
        },
    )
    return {
        "q": q,
        "subreddit": subreddit,
        "sort": sort,
        "t": t,
        "restrict_sr": restrict_sr,
        "posts": listing_posts(payload),
    }


def cmd_subreddit(
    client: RedditClient,
    *,
    name: str,
    sort: str,
    t: str | None,
    limit: int,
) -> dict:
    quoted = _quote_path(name)
    about = client.get(f"/r/{quoted}/about", {})
    params: dict[str, str | int] = {"limit": limit}
    if t is not None:
        params["t"] = t
    listing = client.get(f"/r/{quoted}/{sort}", params)
    return {
        "sort": sort,
        "t": t,
        "subreddit": trim_subreddit(about_data(about)),
        "posts": listing_posts(listing),
    }


def cmd_post(
    client: RedditClient,
    *,
    subreddit: str,
    post_id: str,
    limit: int,
    sort: str,
    depth: int,
) -> dict:
    payload = client.get(
        f"/r/{_quote_path(subreddit)}/comments/{_quote_path(post_id)}",
        {"limit": limit, "sort": sort, "depth": depth},
    )
    post, comments = split_comments_payload(payload)
    return {
        "subreddit": subreddit,
        "id": post_id,
        "sort": sort,
        "limit": limit,
        "depth": depth,
        "post": post,
        "comments": comments,
    }


def _limit_arg(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("limit must be an integer") from exc
    if number < 1 or number > 100:
        raise argparse.ArgumentTypeError("limit must be from 1 to 100")
    return number


def _depth_arg(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("depth must be an integer") from exc
    if number < 0 or number > 10:
        raise argparse.ArgumentTypeError("depth must be from 0 to 10")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Reddit client. App-only OAuth (client_credentials), "
            "then https://oauth.reddit.com. Prints trimmed JSON."
        ),
        epilog=(
            "Env: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET from a script app\n"
            f"at {PREFS_URL}.\n"
            "Optional REDDIT_USER_AGENT: platform:app:version (by /u/name).\n"
            f"Default User-Agent: {DEFAULT_USER_AGENT}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser(
        "search",
        help="Search posts globally (/search) or in one subreddit (/r/{sub}/search)",
    )
    search.add_argument("--q", required=True, help="Search query (q)")
    search.add_argument("--sort", choices=SEARCH_SORTS, default="relevance")
    search.add_argument("--t", choices=TIME_WINDOWS, default="all", help="Time window (t)")
    search.add_argument("--limit", type=_limit_arg, default=25)
    search.add_argument(
        "--subreddit",
        help="Subreddit for /r/{sub}/search. Bare name or r/name.",
    )
    search.add_argument(
        "--restrict-sr",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="restrict_sr. Default: on when --subreddit is set, otherwise off.",
    )

    community = subparsers.add_parser(
        "subreddit",
        help="Subreddit about plus a hot/new/top/rising listing",
    )
    community.add_argument("name", help="Subreddit name, r/name, or subreddit URL")
    community.add_argument("--sort", choices=LISTING_SORTS, default="hot")
    community.add_argument(
        "--t",
        choices=TIME_WINDOWS,
        default=None,
        help="Time window (t). Default for top: all. Omitted for other sorts unless set.",
    )
    community.add_argument("--limit", type=_limit_arg, default=25)

    post = subparsers.add_parser("post", help="One post and its comments")
    post.add_argument("subreddit", help="Subreddit name, r/name, or subreddit URL")
    post.add_argument("id", help="Base36 id, t3_ id, or a comments URL")
    post.add_argument("--limit", type=_limit_arg, default=25)
    post.add_argument("--sort", choices=COMMENT_SORTS, default="confidence")
    post.add_argument("--depth", type=_depth_arg, default=4)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "search":
        subreddit = normalize_subreddit(args.subreddit) if args.subreddit else None
        restrict_sr = args.restrict_sr if args.restrict_sr is not None else subreddit is not None
        result = cmd_search(
            build_client(),
            q=args.q,
            sort=args.sort,
            t=args.t,
            limit=args.limit,
            subreddit=subreddit,
            restrict_sr=restrict_sr,
        )
    elif args.command == "subreddit":
        name = normalize_subreddit(args.name)
        window = args.t
        if args.sort == "top" and window is None:
            window = "all"
        result = cmd_subreddit(
            build_client(),
            name=name,
            sort=args.sort,
            t=window,
            limit=args.limit,
        )
    elif args.command == "post":
        result = cmd_post(
            build_client(),
            subreddit=normalize_subreddit(args.subreddit),
            post_id=normalize_post_id(args.id),
            limit=args.limit,
            sort=args.sort,
            depth=args.depth,
        )
    else:
        raise SystemExit(f"Unknown command: {args.command}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
