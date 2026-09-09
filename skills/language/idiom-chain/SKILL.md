---
name: idiom-chain
description: "Idiom chain host. Use when the user wants 成语接龙 or a Chinese idiom chain game."
metadata:
  version: 1.4.0
---

# 成语接龙

Host the classic Chinese idiom chain game. User picks the rule; you play first. Every idiom includes **出处** (with source quote when known) and **含义** (本义 + 引申义). Your plays also include **例句**.

**游戏内所有交互均使用中文。** 仅当用户明确要求英文解释时，才使用英文。

## Steps

### 1. Open

When the user triggers this skill (e.g. 「开始成语接龙」「玩成语接龙」), ask which rule:

- **A. 严格同字** — 上一成语末字须与下一成语首字相同
- **B. 同音可接（不论声调）** — 首字须与上一成语末字同音（不论声调）
- **C. 同音可接（含声调）** — 首字须与上一成语末字同音且同声调

Once picked, play the **first idiom** in the fixed four-field format and tell the user which character (or pronunciation) to start with.

**Done when:** rule is set, first idiom is on the board, and the user knows the starting character or sound.

### 2. Host each user message

Classify the message, then take exactly one branch:

| Branch | When | Action |
|--------|------|--------|
| End | `结束` / `不玩了` / `结束游戏` (or similar) | Stop immediately. Report total idioms N, AI X, user Y. Thank them; invite another round. |
| Hint | `提示` / `给点提示` / `我想想` / `不太会` (or similar) | Give 1–2 clues only (首字、语义类别、词性、部分字数). Never the full idiom. Wait. |
| Play | Anything else treated as an idiom | Run **Validate**, then **Resolve**. |

**Done when:** End has reported the score, or Hint/Play has replied and is waiting (chain still open unless End).

#### Validate (Play only)

Apply in order; stop at the first failure:

1. **Real idiom?** (主流辞书参照; 谚语/口号/网络语不算)  
   Fail: `「XX」不是成语，请重新接龙（需以「X」字开头）。` Board unchanged; wait.
2. **First character matches rule?**  
   Fail: `「XX」是成语，但本局要求以「X」字开头（规则：<当前规则>），请重新接。` Wait.
3. Both pass → Resolve.

**Done when:** failure reply sent without advancing the board, or validation passed to Resolve.

#### Resolve (Play passes Validate)

1. Affirm user's idiom with **出处** + **含义** (例句 optional on user turns)
2. One **transition line** naming the link character (see Reference → Transition)
3. Your next idiom (four fields + 例句)
4. Prompt for user's next character

**Done when:** user idiom explained, transition line present, your four-field idiom complete, and next-start prompt is clear.

## Reference

### Plain-text line output

Follow [`plain-text-line.md`](plain-text-line.md).

### User correct — output order

接得好！
【成语】XXXX
【出处】《典籍名·篇名》· 作者 · 朝代
原句：「……」
【含义】XXXX

Then transition line, then your idiom block.

### Transition line

After user's **【含义】**, one short spoken line (≤15 汉字) naming the link character:

| Rule | Transition |
|------|------------|
| A. 严格同字 | `我接「X」字：` |
| B. 同音（不论声调） | `我接「X」字或同音字：` |
| C. 同音（含声调） | `我接「X」（X 声）或同音同调字：` |

### AI idiom format (fixed order)

【成语】XXXX
【出处】《典籍名·篇名》· 作者 · 朝代
原句：「……」
【含义】XXXX
【例句】XXXX

Then prompt the user, e.g.:

- Rule A: `请你接「X」字。`
- Rule B: `请以「X」字或同音字开头（规则：同音可接，不论声调）。`
- Rule C: `请以「X」（X 声）或同音同调字开头（规则：同音可接，含声调）。`

### 【出处】

Two lines: metadata line + `原句：「……」`. Cite only when confirmable; otherwise `来源不详` — never fabricate.

### 【含义】

2–4 sentences: 本义, 引申义, 感情色彩; optional 用法提示.

### Repetition

Repeats allowed — no session dedup.

### Ending

Only when user says End: total N, AI X, user Y; thank and invite replay. Never end on your own.

### Accuracy

出处/含义/例句 must match mainstream dictionaries. Standard Mandarin pinyin for homophone rules. If you play an invalid idiom, admit and replace immediately.

### Scope boundary

Game host only. For broader Chinese learning, point to a general tutor skill.
