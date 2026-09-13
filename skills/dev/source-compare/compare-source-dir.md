# `.compare-source/`

Project-local corpus for `source-compare`. Not a trigger — it maps names to paths after the skill is already running. Tree items fill the **search set** when nothing is named; refs only resolve names until named.

## Project root and file

Project root is `git rev-parse --show-toplevel` when that succeeds for cwd; otherwise cwd. No home-directory fallback.

Corpus file: `<project-root>/.compare-source/corpus.md`. Open it by that path. Other files in `.compare-source/` are ignored.

The invoking project is a tree only when it is named in the question or listed as a tree in `corpus.md`.

## List format

List items only:

```markdown
- name: path
```

- `name` is the token users say
- `path` must be a directory (absolute, or relative to the project root)
- A heading whose text is `refs` (any `#` level, case-insensitive) starts the refs list. List items after it are refs until a later heading that is not `refs`. All other list items are trees
- Other prose and tables are ignored — they are not facts about the trees; the code is
- No intro or identity line per tree

Example (illustrative paths; this pack does not ship a corpus):

```markdown
# compare source

- grok-build: /Users/you/code/source/grok-build
- deepseek-harness: /Users/you/code/source/deepseek-harness

# refs

- vercel-ai-sdk: /Users/you/code/source/ai
- ai: /Users/you/code/source/ai
```

## Save offer

After the answer, one offer covering what applies. Show the proposed lines. Write only on yes.

**Create** when `corpus.md` is missing and this run resolved a tree name→path map: create `.compare-source/` if needed and write those `- name: path` lines. If the same offer includes new refs, write `# refs` and those lines in the same create.

**Append refs** when this run resolved a new ref (the user gave packaged-dependency or reference source that is not already a ref `name`): append the new `- name: path` lines under the existing `# refs` heading, after that section's last item. If the heading is missing, append it at the end of the file, then the lines.

Name for a path-only ref: the token the user said; if they only gave a path, the directory basename.

Never rewrite, reorder, or delete existing lines.
