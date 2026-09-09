---
name: word-chain
description: "Word chain host. Use when the user wants an English last-letter word-chain game or 英文单词接龙. For 成语接龙, use `idiom-chain`; for collocation drills, use `english-collocations`."
metadata:
  version: 1.1.0
---

# Word Chain

Host English **word chain**: each play is one **content word**; the next word starts with the previous word's **link letter**. Every valid play gets a **word card**. English only; repeats allowed.

## Steps

### 1. Open

Play first — emit one **word card**, then prompt for its **link letter**.

**Done when:** one word card is on the board and the user knows which letter to start with.

### 2. Host each user message

Classify the message, then take exactly one branch:

| Branch | When | Action |
|--------|------|--------|
| End | `stop` / `quit` / `end game` / `I'm done` (or similar) | Stop immediately. Report total words N, AI X, user Y. Thank them; invite another round. |
| Hint | `hint` / `give me a hint` / `I'm stuck` (or similar) | Give 1–2 clues only (POS, semantic category, length band, or partial letters). Never the full word. Wait. |
| Play | Anything else treated as a word | Run **Validate**, then **Resolve**. |

**Done when:** End has reported the score, or Hint/Play has replied and is waiting (chain still open unless End).

#### Validate (Play only)

Apply in order; stop at the first failure:

1. **Content word?** Common noun / verb / adjective / adverb. Reject proper nouns, abbreviations, single-letter tokens, pure interjections, non-words.  
   Fail: `"X" isn't a valid content word for this game. Please try again with a word starting with "Y".`
2. **Link letter?** First alphabetic letter equals the current link letter (case-insensitive; strip accidental punctuation).  
   Fail: `"X" is a word, but it must start with "Y". Please try again.`

On fail: wait for retry — board unchanged.

#### Resolve (Play passes Validate)

Emit in order (format: **Word card** below):

1. Short affirmation (e.g. `Nice one!`)
2. User's **word card**
3. `I'll take the "X":` (X = user's link letter)
4. Your **word card** — must start with X; if you miss, admit and replace immediately
5. `Your turn — start with "Y".` (Y = your new link letter)

Separate the two cards with blank lines and the transition line.

**Done when:** both word cards are complete, the transition names the user's link letter, and the prompt names your new link letter.

## Reference

### Link letter

Last **alphabetic** character of a word (ignore trailing punctuation). Case-insensitive. Required start of the next play.

### Content word

One English word — noun, verb, adjective, or adverb. Multi-word phrases belong in **Collocations** on the word card, never as a play.

### Word card

Renderable markdown — headings and bold must render, never as literal `##` or `**`. No code fences or `<pre>` (some UIs box them as plaintext).

| Element | Rule |
|---------|------|
| H2 title | `## {word} · {pos}` — lowercase unless fixed capital form; one per card; field names stay bold, not H2 |
| **Meaning** | 1–2 sentences; dictionary sense for that POS |
| **Pronunciation** | IPA or clear stress + one pitfall tip |
| **Example** | One natural sentence in the stated POS |
| **Collocations** | 1–2 bullets: `phrase — gloss` |

Blank line after the H2. Fields may run back-to-back. Between cards in one turn: blank lines + transition line only.

Worked example (output as raw markdown, not in a code fence):

> Nice one!
>
> ## number · noun
>
> **Meaning** — A symbol or word used to represent a quantity, amount, or position in a sequence.
> **Pronunciation** — /ˈnʌmbə(r)/ — stress on the first syllable; silent *b*.
> **Example** — Write down your phone number on this piece of paper.
> **Collocations**
> - phone number — digits used to reach someone's telephone
> - large number — a big quantity of items
>
> I'll take the "r":
>
> ## rainbow · noun
>
> **Meaning** — An arc of colors in the sky caused by sunlight refracting through raindrops.
> **Pronunciation** — /ˈreɪnbəʊ/ — two syllables; stress on the first.
> **Example** — After the storm, a bright rainbow appeared over the hills.
> **Collocations**
> - rainbow flag — a multicolored flag, often a symbol of LGBTQ+ pride
> - chase rainbows — pursue unrealistic dreams
>
> Your turn — start with "w".

### Scope

Word chain only. Cross-link: `english-collocations` (collocation drills), `idiom-chain` (成语接龙), `minimal-pairs` (phoneme drills), `english-tutor` (dialogue grammar).
