# source-compare Skill — Design Doc

Date: 2026-09-10
Revised: 2026-09-13
Status: Approved (brainstorm phase) → ready for implementation plan
Runtime skills live in `skills/<group>/<name>/SKILL.md`. This spec is not a runtime pointer.

Extends the group list in [`2026-09-09-skill-groups-design.md`](2026-09-09-skill-groups-design.md): adds a fourth group `dev`. Grouping rules (directory membership, no generated catalog, identity = `name`) stay unchanged.

---

## 1. Purpose

A **learn-by-compare** skill: read the same capability in several local source trees and explain how each implements it.

It is for learning source, not for porting, reviewing, or producing a fixed report. Trees come from the question or from `<project-root>/.compare-source/corpus.md`. It does not hard-code product names, repository paths, or file maps.

The motivating case is learning web fetch (for example) by reading `grok-build` and `deepseek-harness` together. Those names are examples, not part of the skill.

### Locked decisions

| Topic | Choice |
|-------|--------|
| Approach | Live-search compare. No tool index, no cached directory layout. |
| Invocation | Model-invoked. Leading phrase **Compare local source trees** (not bare "Compare" — `producthunt-top` already uses compare for PH lists). |
| Chinese trigger | 对照 is allowed on the compare-intent branch. Locked exception to the game-skill-only rule. |
| Corpus | Named trees first for the **search set**. `<project-root>/.compare-source/corpus.md` maps names to paths and supplies the set when nothing is named. Other `*.md` in that dir are ignored. |
| Corpus fields | List items only: `- name: path`. No tree intros, entry hints, or directory maps in the file. Other prose is ignored and is not a source of facts. |
| First-run save | If `corpus.md` is missing and this run resolved a name→path map, ask once whether to write that file. Write only on yes, and write only `- name: path` lines. Do not overwrite an existing `corpus.md`. |
| Project root | `git rev-parse --show-toplevel` when cwd is in a git work tree; otherwise cwd. No home-directory fallback. |
| Search | One evidence pack per tree. One explore subagent per tree (`cwd` = that tree's root, isolation none) when the harness can; otherwise sequential. Corpus-filled sets larger than 4 → ask which trees. |
| Answer | No fixed template. The agent answers as it normally would when teaching source, from the evidence packs. Claims stay grounded in those packs. Then the save offer if `corpus.md` was missing. |
| Packaging | `skills/dev/source-compare/` in this pack. New group `dev`. Catalog four-place membership. |
| Version | `1.0.0` |

### Out of scope

- Hard-coded grok / deepseek / harness paths or file maps
- Home-directory corpus (`~/.source-corpus.md`, `~/.compare-source` as a global fallback), cwd `source-corpus.md`, YAML corpus, `~/.config/...` paths, sibling-repo auto-discovery
- Treating the invoking project as a tree unless it is named or listed in `corpus.md`
- Symlink or directory children of `.compare-source/` as the corpus; any markdown other than `corpus.md` as the corpus
- Tree intros, “start here” directories, or other study-guide fields in `corpus.md`
- A prescribed answer template (table + citations + close, or any other fixed report shape)
- Bundled grep/index scripts
- Editing, porting, or committing in the trees as part of this skill
- Interview writeups (`resume-project-prep`)
- User-only invocation (`@source-compare` as the sole trigger)
- Changing `check-catalog.sh` rules (filesystem already derives groups)
- Shipping a `.compare-source/` inside this pack

---

## 2. Identity and triggers

**Name:** `source-compare`

**Description** (two sentences, one English trigger per branch, sibling in the tail):

Compare local source trees. Use when the user names two or more codebases, or asks for a side-by-side / 对照 of the same feature or tool; for interview writeups from one repo, use `resume-project-prep`; for Product Hunt launch lists, use `producthunt-top`.

Branches:

| Branch | Trigger |
|--------|---------|
| Named trees | Two or more codebase names or paths in the question |
| Compare intent | Side-by-side / 对照 of the same feature or tool |

`.compare-source/corpus.md` does **not** trigger the skill. It only resolves names and fills the search set after the skill is already running.

Do not load for a single current-repo "how does this fetch work" with no compare intent.

---

## 3. Tree resolution

Search set, path map, and comparison axis are different jobs. Layout of `.compare-source/` lives in `compare-source-dir.md`; this section owns the resolve process.

**Project root and corpus file**

1. Project root is the output of `git rev-parse --show-toplevel` when that succeeds for cwd; otherwise cwd.
2. Corpus file is `<project-root>/.compare-source/corpus.md`. Look up `.compare-source/` and `corpus.md` by name. Directory listings often hide dotdirs — do not depend on `ls` / `list_dir` to discover the dir.
3. Other files in `.compare-source/` are ignored.

**Search set**

1. If the question names one or more trees, the search set is exactly those trees (named-first). Extra names in `corpus.md` are not added.
2. Else if `corpus.md` exists, the search set is every `name` listed in it.
3. Else ask which directories to search. Do not guess sibling folders or paths under `$HOME`.

A single named tree is a runtime filter after the skill already loaded (compare intent), not a trigger by itself. Teach from that one tree.

If a corpus-filled search set has more than 4 trees, ask which to search and wait. Named trees are used as given; if the user named more than 4, ask which to keep.

**Path map**

For each token in the search set:

1. If it is an existing directory (absolute, or relative to cwd), use that path. A named filesystem path that exists wins over a `corpus.md` `name` of the same string.
2. Else if `corpus.md` exists, match `name` case-insensitively (even when names were given). Relative paths are relative to the project root. The path must be an existing directory.
3. Else ask for that token's path. Wait. Do not drop the token.

**Comparison axis**

The capability, feature, or tool to compare. If the question does not name one, ask once and wait. Search does not start without it.

**Done when:** every token in the search set maps to an existing directory, the set has at most 4 trees (or the user confirmed a subset), and the comparison axis is known.

### `.compare-source/` layout

Disclosed in `skills/dev/source-compare/compare-source-dir.md`. SKILL.md points at it from the resolve step.

- Directory: `.compare-source/` at the project root defined above.
- Filename: `corpus.md` only. List items: `- name: path`. `name` is the token users say. `path` must be a directory. No intro or identity line per tree.
- Other prose, headings, and tables are ignored. They are not facts about the trees; the code is.
- The invoking project is not a tree unless it is named or listed in `corpus.md`.
- Create/write: only when `corpus.md` is missing, this run resolved a name→path map, and the user accepted the one save offer. Write only `- name: path` lines. Never overwrite an existing `corpus.md`.

Example (illustrative paths only; do not commit a real corpus in this pack):

```markdown
# compare source

- grok-build: /Users/you/code/source/grok-build
- deepseek-harness: /Users/you/code/source/deepseek-harness
```

---

## 4. Live search

Do not cache which file implements which tool. Every run searches the resolved trees as they are now.

The **evidence pack** is the subagent return contract — what search must collect so the answer can teach from the code. It is not a user-facing template. One schema:

| Field | Found | Not found |
|-------|-------|-----------|
| name | Tree token | Tree token |
| entry | Function or file that starts the capability (path) | `not found` |
| symbols | Functions, types, tool names | empty |
| note | One line from the code (transport, retries, parsing, errors — only what the code shows) | queries tried |
| spans | Quote-worthy path + line range + short quote | empty |

Dispatch: if the harness can run subagents, one explore subagent per tree. Same question, same axis, `cwd` set to that tree's root, isolation none (trees may sit outside the current workspace). The parent synthesizes from the packs. Otherwise search sequentially in the current session. Stay inside that root even when one tree is nested in another. Default `rg` / gitignore is enough; do not add a bundled indexer.

**Done when:** every tree has an evidence pack (found or not-found with the queries tried).

---

## 5. Answer

Teach the implementations from the evidence packs. Follow the user's language. Use the agent's usual way of explaining source — no required table, heading set, or same/different close.

Grounding (the only answer contract):

- Every tree in the search set is accounted for.
- Every positive claim points at a path from that tree's pack (and lines when quoting).
- A missing capability is said as not found, not invented.

If `corpus.md` was missing and this run resolved a name→path map, ask once whether to write `.compare-source/corpus.md`. Write only on yes (create the dir if needed). Then this skill ends. A later request to change code is ordinary implementation, not a further step of this skill.

**Done when:** the answer accounts for every tree, every positive claim cites a path in that tree, not-found is explicit, and the save offer is written or declined when it applied.

---

## 6. Runtime files

```
skills/dev/source-compare/
  SKILL.md                 # frontmatter + three steps with Done when + one-line boundary
  compare-source-dir.md    # project root, corpus.md path, list format, example, save offer
```

SKILL.md structure (mirror `word-chain` density):

1. Resolve trees and axis — pointer to `compare-source-dir.md`
2. Search each tree
3. Teach from the packs (agent's usual style)

In-file reference stays short: search-set vs path-map, named-path-wins, fan-out cap 4, grounding, save offer when `corpus.md` is missing. Push `corpus.md` syntax to `compare-source-dir.md`.

Boundary line: interview writeups from one codebase → `resume-project-prep`. Product Hunt launch lists → `producthunt-top`.

`metadata.version`: `1.0.0`

---

## 7. Catalog

New group `dev`. `scripts/check-catalog.sh` already derives groups from `skills/<group>/<name>/SKILL.md`; no checker change. `dev` is the first group in this pack that is not an audience split; no extra convention beyond the extra group.

| Place | Addition |
|-------|----------|
| Filesystem | `skills/dev/source-compare/SKILL.md` |
| README Quick Install | Group line `npx skills add shfshanyue/skills/skills/dev`; `--skill source-compare` under a `# dev` comment |
| README Skills | New `### Dev` table, one row, one-line: `Learn a feature by comparing implementations across local source trees` |
| AGENTS clusters | New `### Dev` sub-table: user intent "Learn a feature across local source trees" → `source-compare` |
| evals | New Dev section; Expected skill cell `source-compare` |

AGENTS.md group list in the clusters header currently names Language / Product / CLI. Add Dev there. The add-a-skill steps already say `skills/<group>/<name>/`.

README project-structure tree is not checked by CI. Update it if it still lists only three groups, so humans see `dev`.

---

## 8. Evals

Manual trigger rows. Number from the next free id in `evals/trigger-cases.md` (currently **38**; 37 is the last zh-en-gloss row). Behavioral checklist is the only home for grounding and resolve rules; trigger rows cite it by name. Do not score answer formatting.

Do not add a second copy of `Turn this repo into interview prep`. Amend existing row 18's pass criterion: `source-compare` does not load.

### Trigger

| Prompt | Expected skill | Pass criterion |
|--------|----------------|----------------|
| `grok-build 和 deepseek-harness 里 web fetch 是怎么实现的？` | `source-compare` | Resolves two named trees; meets Behavioral — source-compare answer |
| `对照两边的 tool calling` (project root has `.compare-source/corpus.md`) | `source-compare` | Uses `corpus.md` as the search set; meets Behavioral — source-compare answer |
| `对照两边的 tool calling` (no `.compare-source/`) | `source-compare` | Compare-intent branch loads; agent asks which directories; meets Behavioral — source-compare answer |
| `这段代码的 fetch 怎么写的` (no names, no compare intent) | none | Does not load `source-compare` |

### Behavioral — source-compare answer

- [ ] Comparison axis is known before search (from the question, or the agent asked)
- [ ] Search set is named trees when names are present, otherwise the names in `corpus.md` (or the agent asked which directories)
- [ ] If `corpus.md` was missing and paths were resolved, the agent asked once whether to write it; wrote only on yes
- [ ] Corpus-filled sets larger than 4 were narrowed by asking
- [ ] Each tree is an existing directory, or the agent asked for the missing path and waited
- [ ] Every tree in the search set is accounted for in the answer
- [ ] Every positive claim cites a path inside that tree
- [ ] Not-found is explicit; no invented files
- [ ] No writes in the trees or in `.compare-source/` (unless the user asked to create the corpus)

---

## 9. Error and edge cases

| Case | Behavior |
|------|----------|
| Named tree, no matching `corpus.md` `name`, path missing | Ask for that path; do not skip the tree |
| `corpus.md` path missing on disk or not a directory | Ask; do not search a stale path |
| Other `*.md` next to `corpus.md` | Ignore |
| Two list items match a token case-insensitively | Exact case if one; otherwise ask |
| `corpus.md` missing; user supplied paths | Compare; then ask once whether to write `corpus.md` |
| Capability missing in one tree | Say not found for that tree; still teach the rest |
| One named tree | Teach from that one tree |
| Trees named, no axis | Ask for the axis; do not start search |
| Corpus has more than 4 trees, nothing named | Ask which to search |
| One tree nested inside another | Search each at its own root; do not walk out |
| User asks to change code after the comparison | This skill is already finished; treat as ordinary implementation |
| Subagents unavailable | Sequential search; same evidence pack; answer still unconstrained |
