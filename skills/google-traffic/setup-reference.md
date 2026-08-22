# Google Traffic MCP — one-time setup

Install once on your machine. Every project using the `google-traffic` skill shares these credentials.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (`uvx` runs the MCP packages)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) (GA4 auth)

## 1. Export environment variables

Copy [`analytics-mcp.env.example`](analytics-mcp.env.example) and [`gsc-mcp.env.example`](gsc-mcp.env.example). Fill real paths, then add to `~/.zshrc` (or `~/.cursor/analytics-mcp.env` + `~/.cursor/gsc-mcp.env` if your MCP config uses `envFile`):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
export GOOGLE_PROJECT_ID="your-gcp-project-id"
export GSC_OAUTH_CLIENT_SECRETS_FILE="$HOME/.cursor/google-gsc-oauth-client.json"
```

Restart Cursor after changing env so MCP servers pick up values.

## 2. Google Analytics (GA4)

1. In your GCP project, enable **Google Analytics Admin API** and **Google Analytics Data API**.
2. Run `gcloud auth application-default login`.
3. Confirm `GOOGLE_APPLICATION_CREDENTIALS` points to the ADC JSON path.

## 3. Google Search Console (GSC)

1. In [Google Cloud Console](https://console.cloud.google.com/), create a **Desktop** OAuth client.
2. Download JSON to e.g. `~/.cursor/google-gsc-oauth-client.json` — **never commit**.
3. Set `GSC_OAUTH_CLIENT_SECRETS_FILE` to that absolute path.
4. Reload MCP in Cursor. First GSC tool call opens browser OAuth.

## 4. Verify

After reload MCP servers:

| Server | Tool | Pass |
|--------|------|------|
| `google-analytics` | `get_account_summaries` | Returns account/property list |
| `google-gsc` | `list_properties` | Returns sites you own |

If tools fail with auth errors, call `mcp_auth` on that server, then retry.

## 5. Per-project defaults (not global)

Put GA4 `property_id` and GSC `site_url` in the **project** `AGENTS.md` (one line). The skill reads them before calling `list_properties` / `get_account_summaries`. Do not hardcode site-specific IDs in global env unless you only ever work on one product.

## Fallback: merge MCP into `~/.cursor/mcp.json`

If the skill-bundled [`mcp.json`](mcp.json) does not register after installing the skill, merge the same two server blocks into `~/.cursor/mcp.json` manually (still one-time, not per-repo). Use the `env` block from `mcp.json` or point `envFile` at your `~/.cursor/*.env` files.

## Credential safety

| Artifact | Commit to git? |
|----------|----------------|
| `mcp.json`, `*.env.example` in this skill | Yes |
| `*.env`, OAuth JSON, ADC files | **No** |

Each teammate creates their own OAuth client or receives secrets through your team's secret manager — not via git.
