---
name: workstream-digest
description: "Brief host. Use when the user invokes `@workstream-digest` for a weekly work-goal review or 工作目标周报. Use when the user invokes it with `period=now` to decide what to push next."
argument-hint: "period=week|now tone=direct|soft [since=7d]"
disable-model-invocation: true
metadata:
  version: 1.1.0
---

# Work goal brief

Produce a **brief** that contrasts (1) what the user treats as most important with (2) where time and activity actually went, then outputs fixed sections from [`report-skeleton.md`](report-skeleton.md).

A **work goal** is one outcome that can move forward on its own (a product, learning track, side project). The same goal across chats or repos is **one row** — never split by chat window or tool UI.

In user-facing text, say **work goal** and **brief**; avoid jargon (*line*, *digest*, *focus*) in headings and prose.

## Steps

### 1. Set scope

Read arguments or the user’s first message.

| Input | Default |
|-------|---------|
| `period` | `week` — last 7 days |
| `period=now` | last 48 hours unless `since` is set |
| `since` | user value overrides the defaults above |
| `tone` | `direct` — name mismatches plainly; `soft` — same facts, gentler wording, still name goals |
| Language | match the user’s message (if unclear, ask once) |

**Done when:** time window, tone, and output language are fixed with no further clarifying questions pending.

### 2. Gather evidence

Borrow only the **locate and verify** discipline from superpowers `diagnosing-superpowers` ([`session-discovery.md`](https://github.com/obra/superpowers/blob/main/skills/diagnosing-superpowers/references/session-discovery.md), [`context-safety.md`](https://github.com/obra/superpowers/blob/main/skills/diagnosing-superpowers/references/context-safety.md)). Do **not** run its intake, case directories, analyst subagents, or “what went wrong” flow.

Rules for this step (internal — **not** pasted into the brief):

1. **Verify before you claim.** Every fact in the brief must come from transcripts, session exports, memory files, or commands you just ran in this turn. Numbers come only from those sources, not memory.
2. **Discover in this environment.** Use exposed session tools, configured storage, docs, or bounded file inspection. Hints about where to look are fine; verify against real history. If the user supplied a usable path, do not search again.
3. **Confirm identity.** Use session id, working directory, timestamps, and message content. Recency alone is not enough. Separate parent sessions, child sessions, and unrelated candidates. If ambiguous, ask for one distinguishing fact and stop.
4. **Read records on their own terms.** Separate the human’s words from injected reminders, tool results, and parent-agent dispatches. Match tool calls to results. Missing fields are not zero. Do not assume another harness’s format.
5. **Read-only and size-aware.** Never modify, move, or delete session files. Measure before reading; do not dump whole files. Narrow any single record past ~500 characters to the fields you need.
6. **Gaps are explicit in the brief.** When you cannot verify something, say **未见近期证据** (or equivalent in the output language) and name what is missing (e.g. no sessions for that repo, no stated priority in memory).
7. **Git is optional.** Use commit history only when the workspace has git. Workspaces without git (e.g. some bot harnesses) — infer progress from conversation and file activity only; do not report “zero commits” as a substitute for what was done.

**Brief output rules:** Do **not** include `path:line`, file paths, session ids, shell commands, or raw command output in any section. Describe outcomes in plain language.

**Done when:** every fact you plan to write is verified or marked as a gap; the brief draft obeys the output rules above.

### 3. Group work goals

Merge activity into goals, not into sessions or UIs. Same product or repo theme in the window → one goal. Do not invent goals without evidence.

Keep features and tests under the product goal (e.g. repeat-table E2E under Form Builder), not as separate top-level goals. Preferences and editor settings are not work goals.

**Done when:** each goal with evidence has a name and 2–5 outcome bullets for `period=week`, or at most 3 bullets per goal for `period=now` (see section 3 of [`report-skeleton.md`](report-skeleton.md)).

### 4. Stated importance vs actual time

- **Stated:** what the user said or wrote as top priority (including memory or profile files). If none: **未见你说过的重点** / state that no stated priority was found, with gap detail.
- **Actual:** where sessions and concrete work landed, in plain language (not commit counts unless they clarify a outcome).
- **Mismatch (one sentence):** `direct` — name which important goal was crowded out and what absorbed time. `soft` — same facts, e.g. “Time mostly went to …; you said the top priority was …”.
- **Adjustments:** 1–3 concrete moves (reclaim time, park something, or one either-or for the user). If aligned: say the window matched, then one step to protect the current top priority.

**Done when:** stated and actual each have at least one sentence; mismatch + adjustments follow the branches above; no paths or commands in prose.

### 5. Write the brief

Follow [`report-skeleton.md`](report-skeleton.md) in order. Section 3 uses a **list per goal** (what happened), not evidence paragraphs. Default to short paragraphs elsewhere; use a table only if the user asked.

**Done when:** all five sections are present; **下一步** / **Next** has 1–4 verb-led bullets doable in the window; no unverified guesses; no `path:line`, paths, ids, or commands in user-facing text.
