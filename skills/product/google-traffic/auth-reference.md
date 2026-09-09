# Google Traffic — auth

**auth** is machine-wide: one Google account, one gcloud directory. **scope** (`property_id`, `site_url`) lives in each repo's `AGENTS.md` — see [`scope-reference.md`](scope-reference.md).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (`uvx` runs the MCP packages)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)

## Paths (single source)

| Artifact | Path |
|----------|------|
| ADC (GA4) | `~/.config/gcloud/application_default_credentials.json` |
| GSC OAuth client JSON | `~/.config/gcloud/gsc-oauth-client.json` |
| Env template | [`gcloud.env.example`](gcloud.env.example) |

Copy `gcloud.env.example` values into your shell profile or MCP `env` / `envFile`. Reload MCP on your **host** after changes.

## OAuth client

Shared by GA4 ADC login and GSC MCP.

1. In [Google Cloud Console](https://console.cloud.google.com/), create a **Desktop** OAuth client.
2. Save the downloaded JSON as `~/.config/gcloud/gsc-oauth-client.json` — **never commit**.
3. Set `GSC_OAUTH_CLIENT_SECRETS_FILE` to that path (or another location, e.g. `~/.cursor/google-gsc-oauth-client.json`).

## GA4

1. In your GCP project, enable **Google Analytics Admin API** and **Google Analytics Data API**.
2. Run ADC login with `analytics.readonly` — default ADC omits that scope; reuse the Desktop OAuth client from **OAuth client** above (`--client-id-file` may point at your `GSC_OAUTH_CLIENT_SECRETS_FILE` path instead):

```bash
gcloud auth application-default login \
  --client-id-file=~/.config/gcloud/gsc-oauth-client.json \
  --scopes="https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform,openid,https://www.googleapis.com/auth/userinfo.email"
```

3. Set `GOOGLE_APPLICATION_CREDENTIALS` to the ADC path above (or rely on gcloud default if your MCP reads it).
4. Set `GOOGLE_PROJECT_ID` to that GCP project id — **not** a GA4 `property_id`.

## GSC

1. Set `GSC_OAUTH_CLIENT_SECRETS_FILE` if not done in **OAuth client**.
2. Reload MCP on your **host**. First GSC tool call opens browser OAuth.

## Verify auth

| Server | Tool | Pass |
|--------|------|------|
| `google-analytics` | `get_account_summaries` | Returns account/property list |
| `google-gsc` | `list_properties` | Returns sites for the logged-in Google account |

If tools reject with auth errors, call `mcp_auth` on that server, then retry.

## Scope env (do not set globally)

Keep `GA4_PROPERTY_ID` and `GSC_DEFAULT_SITE` out of global env when you work across multiple repos — use **scope** in each project's `AGENTS.md` instead.

## Credential safety

| Artifact | Commit to git? |
|----------|----------------|
| Skill `mcp.json`, `gcloud.env.example` | Yes |
| ADC, OAuth JSON, filled `.env` | **No** |

Teammates create their own OAuth client or receive secrets through your team's secret manager — not via git.
