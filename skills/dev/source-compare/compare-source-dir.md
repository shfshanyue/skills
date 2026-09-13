# `.compare-source/`

Project-local corpus for `source-compare`. Not a trigger — it maps names to paths and fills the **search set** after the skill is already running.

## Project root and file

Project root is `git rev-parse --show-toplevel` when that succeeds for cwd; otherwise cwd. No home-directory fallback.

Corpus file: `<project-root>/.compare-source/corpus.md`. Open it by that path. Other files in `.compare-source/` are ignored.

The invoking project is a tree only when it is named in the question or listed in `corpus.md`.

## List format

List items only:

```markdown
- name: path
```

- `name` is the token users say
- `path` must be a directory (absolute, or relative to the project root)
- Other prose, headings, and tables are ignored — they are not facts about the trees; the code is
- No intro or identity line per tree

Example (illustrative paths; this pack does not ship a corpus):

```markdown
# compare source

- grok-build: /Users/you/code/source/grok-build
- deepseek-harness: /Users/you/code/source/deepseek-harness
```

## Save offer

Write `corpus.md` only when all of these hold:

1. `corpus.md` is missing
2. This run resolved a name→path map
3. The user accepted the one save offer after the comparison

Then create `.compare-source/` if needed and write only `- name: path` lines. Never overwrite an existing `corpus.md`.
