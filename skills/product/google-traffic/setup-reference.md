# Google Traffic — setup index

Three layers; each repo shares **auth** and **host**, and sets its own **scope**.

| Layer | Install | Location | Holds |
|-------|---------|----------|-------|
| **auth** | Once per machine | `~/.config/gcloud/` | ADC, GSC OAuth client JSON, `GOOGLE_PROJECT_ID` |
| **host** | Once per machine (per agent) | See host-wiring | MCP server registration |
| **scope** | Per repo | Project `AGENTS.md` | GA4 `property_id`, GSC `site_url` |

## When to read which reference

| Step 1 signal | Read |
|---------------|------|
| MCP server missing | [`host-wiring-reference.md`](host-wiring-reference.md) |
| `needsAuth` / auth error | [`auth-reference.md`](auth-reference.md) |
| Step 2 — no scope in `AGENTS.md` | [`scope-reference.md`](scope-reference.md) |

After auth or host changes, reload MCP on your **host**, then retry Step 1.
