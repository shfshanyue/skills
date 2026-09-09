# Google Traffic — host wiring

**host** registers MCP servers with your agent. **auth** paths are the same on every host — see [`auth-reference.md`](auth-reference.md). Canonical server defs: skill [`mcp.json`](mcp.json) (command, args, `includeTools`, package pins).

## Host config locations

| Host | Global | Project | Format |
|------|--------|---------|--------|
| Cursor | `~/.cursor/mcp.json` | `.cursor/mcp.json` | JSON → `mcpServers` |
| Claude Code | `~/.claude.json` | `.mcp.json` | JSON → `mcpServers` |
| Codex | `~/.codex/config.toml` | `.codex/config.toml` | TOML → `[mcp_servers.name]` |
| Grok Build | `~/.grok/config.toml` | `.grok/config.toml` | TOML → `[mcp_servers.name]` |
| Gemini CLI | `~/.gemini/settings.json` | `.gemini/settings.json` | JSON → `mcpServers` |

Official references: [Cursor MCP](https://cursor.com/docs/context/mcp), [Claude Code MCP](https://code.claude.com/docs/en/mcp-servers), [Codex config](https://developers.openai.com/codex/config-reference), [Grok settings](https://docs.x.ai/build/settings).

Grok may also load Claude/Cursor project configs (compat). Cursor registers skill-bundled `mcp.json` on install; other hosts need manual wiring below.

## Wrapper — JSON (Cursor, Claude)

Wrap blocks from [`mcp.json`](mcp.json) under `mcpServers`. Point `env` at gcloud **auth** paths (or `${env:…}` from shell):

```json
{
  "mcpServers": {
    "google-analytics": {
      "command": "uvx",
      "args": ["analytics-mcp==0.7.0"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${userHome}/.config/gcloud/application_default_credentials.json",
        "GOOGLE_PROJECT_ID": "${env:GOOGLE_PROJECT_ID}"
      }
    },
    "google-gsc": {
      "command": "uvx",
      "args": ["mcp-search-console==0.3.3"],
      "env": {
        "GSC_OAUTH_CLIENT_SECRETS_FILE": "${userHome}/.config/gcloud/gsc-oauth-client.json"
      }
    }
  }
}
```

Use `command` / `args` / `includeTools` from [`mcp.json`](mcp.json) — do not hardcode versions elsewhere.

## Wrapper — TOML (Codex, Grok)

```toml
[mcp_servers.google-analytics]
command = "uvx"
args = ["analytics-mcp==0.7.0"]
[mcp_servers.google-analytics.env]
GOOGLE_APPLICATION_CREDENTIALS = "/Users/YOU/.config/gcloud/application_default_credentials.json"
GOOGLE_PROJECT_ID = "your-gcp-project-id"

[mcp_servers.google-gsc]
command = "uvx"
args = ["mcp-search-console==0.3.3"]
[mcp_servers.google-gsc.env]
GSC_OAUTH_CLIENT_SECRETS_FILE = "/Users/YOU/.config/gcloud/gsc-oauth-client.json"
```

Codex can forward shell vars with `env_vars = ["GOOGLE_PROJECT_ID"]` instead of inline values.

## CLI shortcuts

| Host | Add servers |
|------|-------------|
| Claude Code | `claude mcp add --scope user …` |
| Codex | `codex mcp add …` |
| Grok | `grok mcp add …` |
| Gemini CLI | `gemini mcp add -s user …` |

After editing, reload MCP on that **host** and run auth verify in [`auth-reference.md`](auth-reference.md).
