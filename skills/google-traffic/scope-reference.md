# Google Traffic — scope

**scope** is per repo: which GA4 property and GSC site this codebase uses. **auth** is machine-wide — see [`auth-reference.md`](auth-reference.md).

Add to the project **`AGENTS.md`** (copy and fill):

```markdown
## Google Traffic (scope)

- GA4 property_id: `123456789`
- GSC site_url: `sc-domain:example.com`
```

## site_url format

`site_url` must match `list_properties` **exactly** — e.g. `sc-domain:example.com` vs `https://www.example.com/` are different entries. When unsure, call `list_properties` and paste the returned string.

## Multi-repo

Same Google **auth** across repos; each repo's **scope** block points at its own property and site. Switching workspace → read **this repo's** `AGENTS.md` before reporting.
