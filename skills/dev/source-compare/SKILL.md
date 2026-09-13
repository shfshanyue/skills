---
name: source-compare
description: "Compare local source trees. Use when the user names two or more codebases, or asks for a side-by-side / 对照 of the same feature or tool; for interview writeups from one repo, use `resume-project-prep`; for Product Hunt launch lists, use `producthunt-top`."
metadata:
  version: 1.0.0
---

# Source Compare

**Learn-by-compare:** read the same capability in several local source trees and teach how each implements it. Trees come from the question or from `.compare-source/corpus.md`. Live search each run — no cached file map.

Leave the trees unchanged. The only write this skill may make is the save offer in [`compare-source-dir.md`](compare-source-dir.md).

## Steps

### 1. Resolve trees and axis

Project root, corpus path, list format: [`compare-source-dir.md`](compare-source-dir.md). Open `corpus.md` by that path (dotdirs are often hidden from listings).

**Search set** (which trees):

1. Question names one or more trees → exactly those tokens (corpus extras stay out)
2. Else `corpus.md` exists → every `name` in it
3. Else ask which directories and wait

A corpus-filled set larger than 4, or more than 4 named trees: ask which to keep and wait. One named tree is a filter after this skill already loaded — teach from that tree.

**Path map** (token → directory), per token:

1. Existing directory (absolute, or relative to cwd) wins over a corpus `name` of the same string
2. Else match a corpus `name` case-insensitively; relative paths are relative to the project root; the path must be an existing directory. Two case-insensitive hits: use exact case if one matches; otherwise ask
3. Else ask for that token's path and wait — keep the token

**Comparison axis:** the capability, feature, or tool. If the question omits it, ask once and wait. Search starts only with an axis.

**Done when:** every search-set token maps to an existing directory, the set has at most 4 trees (or the user confirmed a subset), and the comparison axis is known.

### 2. Search each tree

Every run searches the trees as they are now. Collect one **evidence pack** per tree:

| Field | Found | Not found |
|-------|-------|-----------|
| name | Tree token | Tree token |
| entry | Function or file that starts the capability (path) | `not found` |
| symbols | Functions, types, tool names | empty |
| note | One line from the code (transport, retries, parsing, errors — only what the code shows) | queries tried |
| spans | Quote-worthy path + line range + short quote | empty |

If the harness can run subagents: one explore subagent per tree, same question and axis, `cwd` = that tree's root, isolation none (trees may sit outside this workspace). Stay inside that root even when one tree is nested in another. Otherwise search sequentially in this session. Default `rg` / gitignore is enough.

**Done when:** every tree has an evidence pack (found, or not-found with the queries tried).

### 3. Teach from the packs

Teach the implementations in the user's language, in the agent's usual way of explaining source.

Grounding:

- Every tree in the search set is accounted for
- Every positive claim points at a path from that tree's pack (and lines when quoting)
- A missing capability is said as not found

If `corpus.md` was missing and this run resolved a name→path map, ask once whether to write it (rules in [`compare-source-dir.md`](compare-source-dir.md)). Then this skill ends. A later request to change code is ordinary implementation.

**Done when:** the answer accounts for every tree, every positive claim cites a path in that tree, not-found is explicit, and the save offer is written or declined when it applied.

## Boundaries

Interview writeups from one codebase → `resume-project-prep`. Product Hunt launch lists → `producthunt-top`.

## Reference

| Term | Rule |
|------|------|
| Search set | Named trees when present; else every corpus `name`; else ask |
| Path map | Existing directory (cwd-relative or absolute) wins; else corpus `name`; else ask |
| Fan-out | At most 4 trees; larger sets wait for a subset |
| Grounding | Every tree accounted; positive claims cite a pack path; missing = not found |
| Save | Offer once after the answer iff `corpus.md` was missing and paths were resolved |
