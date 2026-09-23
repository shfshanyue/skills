# Report skeleton

Emit exactly five sections in this order. Do not add or remove sections.

Section titles: use the **Chinese** heading when the user writes in Chinese; use the **English** heading when the user writes in English. Do not use *focus*, *workstream*, or *digest* as headings.

Do **not** put `path:line`, file paths, session ids, or shell/git commands in any section.

## 1. 现在在做什么 / What you are doing now

One sentence naming the work goal(s) that actually moved forward in the time window.

**Done when:** one sentence is present and names at least one goal by name.

## 2. 优先级建议 / Suggested priority

Use **P0 / P1 / P2 / 搁置** as subheadings (English: **P0 / P1 / P2 / Parked**). Under each level, name work goals. Write **无** / **none** when a level has no goals.

| Level | Meaning |
|-------|---------|
| **P0** | Do first — matches stated top priority or urgent unblock |
| **P1** | Next after P0 |
| **P2** | Worth doing when bandwidth allows |
| **搁置** / **Parked** | Explicitly not pushing this window |

**Done when:** all four levels appear; every named goal sits under exactly one level.

## 3. 各工作目标 / Each goal

List only work goals with verified activity in the time window. For each goal:

- **Heading:** goal name (bold).
- **Bullets:** what happened — requests, decisions, shipped or attempted outcomes. Newest first. Use outcome numbers inside a sentence when helpful (e.g. “117/117 tests passed”); do not lead with commit or session counts as evidence.

| `period` | Bullets per goal |
|----------|------------------|
| `week` (default) | 2–5 |
| `now` | at most 3 |

Example shape (Chinese brief):

- **ScanForm Form Builder**
  - 把 repeat-table 的等待改成 `expect.poll`，当时 117/117 通过
  - 从 9/21 起并行做 layout optimizer 和按页宽自适应
  - 今天在查 `keepNonCanceled`；Grok 按上一版规格在实现
- **new-blog**
  - 本周在改博客并做过一次 Astro 7 升级

**Done when:** every listed goal has a heading and bullets as above, or the section states **无** / **none** if no goals had verified activity.

## 4. 停住了 / 对不上 / 要你选 / Stuck, mismatched, or needs a choice

Call out: goals with no recent progress; important goals crowded out by lower-priority work; at most **one** either-or the user must choose. Write **无** / **none** when nothing applies.

Include the **对不上的地方** sentence from step 4 of the workflow here when priorities and time use disagree.

**Done when:** section is present; either concrete items in plain language or **无** / **none**.

## 5. 下一步 / Next

1–4 bullets. Each bullet starts with a verb and is doable inside the time window.

| `period` | Lead-in |
|----------|---------|
| `week` (default) | **本周** / **This week** |
| `now` | **今天** / **Today** |

**Done when:** count is 1–4; each bullet is actionable and verb-led.
