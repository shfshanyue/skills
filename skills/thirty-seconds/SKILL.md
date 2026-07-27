---
name: thirty-seconds
description: "Generates 30 Seconds (30秒) board game cards for offline play, with rich answer-key glosses after each card. Use when the user wants 30秒卡片、30 Seconds cards、生成猜词卡片、party word-game card sets, or printable cards for the 30 Seconds describing-and-guessing game."
metadata:
  version: 1.0.0
---

# Thirty Seconds (30秒) — Card Generator

Generate **cards** for offline **30 Seconds** play: each card holds five terms for a live describer; after play, the **answer key** supplies rich glosses (meaning + background). Not a live host — no in-chat describing, guessing, or scoring.

Cross-link: `word-chain` (English word chain), `idiom-chain` (成语接龙), `poetry-quiz` (诗词填空).

## Steps

### 1. Open

On trigger (e.g. `生成30秒卡片`, `30 Seconds cards`, `来几张30秒`):

1. If language not stated, ask once: **中文词条** or **English terms**.
2. If count not stated, default **3 cards**; accept any reasonable count (1–10).
3. Confirm language + count in one line, then generate — do not ask further menus (no difficulty, no theme packs).

**Done when:** language and card count are fixed (explicit or defaulted) and generation begins.

### 2. Generate each card

For every card:

1. Pick **five terms** — mixed categories (people, places, film/TV, music, sports, history, science/tech, food, brands, idioms/catchphrases where natural). No difficulty tiers; avoid obscure trivia that only specialists would know.
2. Assign a **face color** — `蓝面` or `黄面`, alternating across cards in a batch when possible.
3. Emit the **Describer block** (five terms only — identifiers must not read this section during play).
4. Emit the **Answer key** (rich gloss per term — see Reference).

Between cards in one batch: blank line + `---` + blank line.

**Done when:** every requested card has both blocks, five distinct terms per card, and no term repeats within the batch.

### 3. Follow-up messages

| Branch | When | Action |
|--------|------|--------|
| More | `再来 N 张`, `more cards`, `再生成` | Same language unless user switches; new batch, new terms (no repeats from this session). |
| Rules | `规则`, `怎么玩`, `how to play` | Short offline rules (see Reference → Offline rules); no new cards unless asked. |
| Switch | `换成英文` / `switch to Chinese` | Confirm, then generate with new language. |

**Done when:** the branch action is complete and the agent is waiting or has delivered the requested cards.

## Reference

### Describer block format

Plain text lines — **not** inside code fences, triple backticks, or `<pre>` (some chat UIs box them as plaintext).

One card:

```
=== 卡片 {n} · {蓝面|黄面} ===
1. {term}
2. {term}
3. {term}
4. {term}
5. {term}
```

Game language matches the chosen mode (Chinese terms in 中文 mode; English in English mode).

### Answer key format

Immediately after each Describer block, same card number:

```
=== 卡片 {n} 详解（猜完后再看）===
【词条】{term}
【释义】{2–3 sentences — dictionary sense or who/what this is}
【背景】{celebrity role, plot hook, place context, event summary, etc.}
【趣味】{one fun fact, quote, or memorable detail — optional if thin}

(repeat for all five terms)
```

Fields run as plain text lines like `idiom-chain`. **【趣味】** skip only when nothing verifiable fits.

### Offline rules (on request only)

- Teams of 2+; one **describer** per turn, rest **guess**.
- ~30 seconds per turn (phone timer or hourglass).
- Describe any order; synonyms, associations, mime OK.
- **Forbidden:** the term itself, derived forms, first letter, rhyme/sounds-like, translation of the term, pointing at objects.
- Board edition: roll die (0/0/1/1/2/2) as handicap; move = correct guesses minus handicap (optional — mention only if user asks about the board).

### Accuracy

- Every term must be real and glosses factually accurate.
- If author/source/year is uncertain, say so — do not invent film plots, dates, or biographies.
- Prefer widely recognizable entries over niche ones.

### Session dedup

Track every term issued in the current conversation; never repeat within the session across batches.
