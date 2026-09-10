# source-compare Skill — Design Doc

Date: 2026-09-10
Status: Approved (brainstorm phase) → ready for implementation plan
Runtime skills live in `skills/<group>/<name>/SKILL.md`. This spec is not a runtime pointer.

Extends the group list in [`2026-09-09-skill-groups-design.md`](2026-09-09-skill-groups-design.md): adds a fourth group `dev`. Grouping rules (directory membership, no generated catalog, identity = `name`) stay unchanged.

---

## 1. Purpose

A **compare** skill: one question, several local source trees, one side-by-side answer with citations.

It is a generic workflow. It does not hard-code product names, repository paths, or file maps. Trees come from the question or from a corpus file the user keeps outside the skill.

The motivating case is reading the same capability (for example web fetch) in `grok-build` and `deepseek-harness` together. Those names are examples, not part of the skill.

### Locked decisions

| Topic | Choice |
|-------|--------|
| Approach | Live-search compare. No tool index, no cached directory layout. |
| Invocation | Model-invoked. Leading word **Compare**. |
| Corpus | Named trees first for the **search set**. Corpus files map names to paths and supply the set when nothing is named. |
| Corpus files | `source-corpus.md` in the current directory, then `~/.source-corpus.md`. Format in a disclosed pointer. Paths never live in this repo. |
| Search | One evidence pack per tree. Dispatch one explore subagent per tree when the harness can; otherwise sequential. |
| Answer | Comparison table + per-tree citations + a same/different close. Output language follows the user. |
| Packaging | `skills/dev/source-compare/` in this pack. New group `dev`. Catalog four-place membership. |
| Version | `1.0.0` |

### Out of scope

- Hard-coded grok / deepseek / harness paths or file maps
- YAML corpus, `~/.config/...` paths, sibling-repo auto-discovery
- Bundled grep/index scripts
- Editing, porting, or committing in the trees unless the user asks
- Interview writeups (`resume-project-prep`)
- User-only invocation (`@source-compare` as the sole trigger)
- Changing `check-catalog.sh` rules (filesystem already derives groups)

---

## 2. Identity and triggers

**Name:** `source-compare`

**Description** (two sentences, one English trigger per branch, sibling in the tail):

Compare local source trees. Use when the user names two or more codebases, asks for a side-by-side / 对照 of the same feature or tool, or asks how something is implemented while `source-corpus.md` is in the current directory. For interview writeups from one repo, use `resume-project-prep`.

Branches:

| Branch | Trigger |
|--------|---------|
| Named trees | Two or more codebase names or paths in the question |
| Compare intent | Side-by-side, 对照, "your/our source", same feature across trees |
| Cwd corpus | `source-corpus.md` present in cwd and the question is how something is implemented |

`~/.source-corpus.md` does **not** trigger the skill. It only resolves names and fills the search set after the skill is already running.

Do not load for a single current-repo "how does this fetch work" with no compare intent and no cwd corpus.

---

## 3. Tree resolution

Search set and path map are different jobs.

**Search set**

1. If the question names one or more trees, the search set is exactly those trees (named-first).
2. Else read `./source-corpus.md` if it exists; the search set is every listed tree.
3. Else read `~/.source-corpus.md` if it exists; same.
4. Else ask the user which directories to search. Do not guess sibling folders or `~/code/source`.

A single named tree is a runtime filter after the skill already loaded (compare intent or cwd corpus), not a trigger by itself. Emit a one-row table and skip a theatrical same/different close.

**Path map**

For each token in the search set:

1. If it is an existing directory (absolute, or relative to cwd), use that path.
2. Else load cwd corpus then home corpus (even when names were given) and match `name` case-insensitively.
3. Else ask for that token's path. Wait. Do not drop the token.

A named filesystem path that exists wins over a corpus name of the same string.

**Done when:** every tree in the search set has an existing directory, or the user has been asked for every missing path and the set is complete.

### Corpus file format

Disclosed in `skills/dev/source-compare/corpus-file.md`. SKILL.md points at it from the resolve step.

- Filename: `source-corpus.md` (cwd) or `~/.source-corpus.md` (home).
- One tree per list item: `- name: /absolute/or/relative/path`
- `name` is the token users say. `path` must be a directory.
- Other prose, headings, and tables in the file are ignored.

Example (illustrative paths only; do not commit a real corpus):

```markdown
# source corpus

- grok-build: /Users/you/code/source/grok-build
- deepseek-harness: /Users/you/code/source/deepseek-harness
```

The skill never writes this file unless the user asks it to.

---

## 4. Live search

Do not cache which file implements which tool. Every run searches the resolved trees as they are now.

For each tree, collect an **evidence pack**:

- Entry path (the function or file that starts the capability)
- Key symbols (functions, types, tool names)
- Short notes (transport, retries, parsing, errors — only what the code shows)
- Quote-worthy spans (path and line range)
- Or **not found**: queries tried, no invention

Dispatch: if the harness can run subagents, one explore subagent per tree with the same question and that tree's root; the parent synthesizes. Otherwise search sequentially in the current session. Stay inside that root. Default `rg` / gitignore is enough; do not add a bundled indexer.

**Done when:** every tree has an evidence pack or an explicit not-found with the queries tried.

---

## 5. Answer shape

Follow the user's language.

Emit in this order:

1. **Table** — one row per tree: name, entry path, key symbols, one-line note (or `not found`).
2. **Citations** — per tree, short quoted spans with path and lines. Enough to show the mechanism, not whole files.
3. **Close** — what is the same, what is different. Omit this close when the search set has one tree.

Every positive claim has a path. A missing capability is a row, not a guessed implementation.

**Done when:** the table has one row per tree, every positive claim cites a path (and lines when quoting), not-found rows are marked, and the close matches the search-set size.

---

## 6. Runtime files

```
skills/dev/source-compare/
  SKILL.md          # frontmatter + three steps with Done when + one-line boundary
  corpus-file.md    # filename, lookup order, list format, example
```

SKILL.md structure (mirror `word-chain` density):

1. Resolve trees — pointer to `corpus-file.md`
2. Search each tree
3. Emit the comparison

In-file reference stays short: search-set vs path-map, named-path-wins, read-only. Push corpus syntax to `corpus-file.md`.

Boundary line: interview writeups from one codebase → `resume-project-prep`. Read-only on the trees unless the user asks to change them.

`metadata.version`: `1.0.0`

---

## 7. Catalog

New group `dev`. `scripts/check-catalog.sh` already derives groups from `skills/<group>/<name>/SKILL.md`; no checker change.

| Place | Addition |
|-------|----------|
| Filesystem | `skills/dev/source-compare/SKILL.md` |
| README Quick Install | Group line `npx skills add shfshanyue/skills/skills/dev`; `--skill source-compare` under a `# dev` comment |
| README Skills | New `### Dev` table with one row |
| AGENTS clusters | New `### Dev` sub-table: user intent "Same feature across local source trees" → `source-compare` |
| evals | New Dev section; Expected skill cell `source-compare` |

AGENTS.md group list in the clusters header currently names Language / Product / CLI. Add Dev there. The add-a-skill steps already say `skills/<group>/<name>/`; no new convention beyond the extra group.

README project-structure tree is not checked by CI. Update it if it still lists only three groups, so humans see `dev`.

---

## 8. Evals

Manual trigger rows. Number from the next free id in `evals/trigger-cases.md` (currently 37). Behavioral checklist is the only home for the answer-shape rules; trigger rows cite it by name.

### Trigger

| Prompt | Expected skill | Pass criterion |
|--------|----------------|----------------|
| `grok-build 和 deepseek-harness 里 web fetch 是怎么实现的？` | `source-compare` | Resolves two named trees; meets Behavioral — source-compare answer |
| `对照两边的 tool calling` (cwd has `source-corpus.md`) | `source-compare` | Uses cwd corpus; meets Behavioral — source-compare answer |
| `你在你们的源码中，Web fetch 是如何实现的？` (no names, no cwd corpus) | `source-compare` | Compare-intent branch loads; home corpus fills the set if present, otherwise the agent asks; meets Behavioral — source-compare answer |
| `这段代码的 fetch 怎么写的` (no names, no cwd corpus) | none | Does not load `source-compare` |
| `Turn this repo into interview prep` | `resume-project-prep` | Existing interview row still wins; `source-compare` does not load |

### Behavioral — source-compare answer

- [ ] Search set is named trees when names are present, otherwise the corpus list
- [ ] Each tree is an existing directory or the agent asked for the missing path
- [ ] Table has one row per tree
- [ ] Every positive claim cites a path inside that tree
- [ ] Not-found is explicit; no invented files
- [ ] Same/different close present when two or more trees were searched
- [ ] No writes in the trees

---

## 9. Error and edge cases

| Case | Behavior |
|------|----------|
| Named tree, no corpus, path missing | Ask for that path; do not skip the tree |
| Corpus path missing on disk | Ask; do not search a stale path |
| Capability missing in one tree | `not found` row; still compare the rest |
| One named tree | One-row table; no same/different close |
| User asks to change code after the comparison | Leave this skill's read-only default; implement only if they ask |
| Subagents unavailable | Sequential search; same evidence pack and answer shape |
