---
name: english-practice
description: "English practice router. Use when the user wants to practice English but has not picked dialogue, collocations, pronunciation, or a general study topic."
metadata:
  version: 1.1.1
---

# English Practice Router

Dispatch only — **do not teach**. Identify what the user wants, name the matching skill, and hand off.

If the user already @mentions a specific skill, skip routing and follow that skill directly.

## Dispatch

| Intent | Hand off to |
|--------|-------------|
| Conversation, grammar correction, spoken English chat | `english-tutor` |
| Collocations, fixed pairings, Chinglish wording | `english-collocations` |
| Pronunciation, phoneme contrasts, 最小对立对 | `minimal-pairs` |
| Structured learning on a general topic (not English-specific) | `deep-learner` |
| Inline English glosses while reading Chinese answers | Tell user to `@zh-en-gloss` (user-invoked; router does not auto-load) |
| Word chain game / 英文单词接龙 | `word-chain` |
| Chinese idiom chain / 成语接龙 | `idiom-chain` |
| Classical poetry quiz / 诗词填空 | `poetry-quiz` |

Ask one clarifying question only when intent is genuinely ambiguous after the user's first message.

**Done when:** the user knows which skill to use and you have handed off (or they already named a skill and you skipped routing).
