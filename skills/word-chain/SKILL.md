---
name: word-chain
description: "Word chain host — English last-letter word game with a light gloss after every valid play (POS, meaning, pronunciation, example, 1–2 collocations). Use when the user wants word chain, English last-letter chain, or 英文单词接龙. For Chinese idiom chain, use `chengyu-jielong`. For deeper collocation drills, use `english-collocations`."
metadata:
  version: 1.0.0
---

# Word Chain

Host a classic English **word chain**: each play is one **content word**; the next word starts with the previous word's **link letter**. After every valid play, emit a fixed **word card** (light gloss). Host entirely in English. Repeats are allowed.
## Steps

### 1. Open

On trigger, play first — emit one **word card**, then prompt with that word's **link letter**.

**Done when:** exactly one word card is on the board and the user has been asked to continue from its link letter.

### 2. Host each user message

Classify the message, then take exactly one branch:

| Branch | When | Action |
|--------|------|--------|
| End | `stop` / `quit` / `end game` / `I'm done` (or similar) | Stop immediately. Report total words N, AI X, user Y. Thank them; invite another round. |
| Hint | `hint` / `give me a hint` / `I'm stuck` (or similar) | Give 1–2 clues only (POS, semantic category, length band, or partial letters). Wait. |
| Play | Anything else treated as a word | Run **Validate**, then **Resolve**. |

**Done when:** End has reported the score, or Hint/Play has replied and is waiting for the next user message (chain still open unless End).

#### Validate (Play only)

Apply in order; stop at the first failure:

1. **Content word?** Common noun / verb / adjective / adverb. Fail proper nouns, abbreviations, single-letter tokens, pure interjections, non-words.  
   Fail reply: `"X" isn't a valid content word for this game. Please try again with a word starting with "Y".`
2. **Link letter?** First alphabetic letter of the play equals the current link letter (case-insensitive; strip accidental punctuation).  
   Fail reply: `"X" is a word, but it must start with "Y". Please try again.`

On either fail: wait for retry — leave the board unchanged.

#### Resolve (both checks pass)

Emit, in order:

1. Short affirmation (e.g. `Nice one!`)
2. User's **word card**
3. Blank line + `I'll take the "X":` (X = user's link letter)
4. Blank line + your **word card** (must obey the link letter; if you miss, admit it and replace with a valid card immediately)
5. `Your turn — start with "Y".` (Y = your new link letter)

**Done when:** both word cards are complete, the transition line uses the user's link letter, and the prompt uses your new link letter.

## Reference

### Link letter

The last **alphabetic** character of a word (ignore trailing punctuation). Case-insensitive. That letter is the required start of the next play.

### Content word

Playable unit = one English word: noun, verb, adjective, or adverb. Multi-word phrases are gloss material only — they live under `[Collocations]`, never as a play.

### Word card (plain text, fixed order)

Emit each field on its own line as ordinary text (no code fences, no `<pre>`):

```
[Word] elephant
[POS] noun
[Meaning] A very large mammal with a trunk, native to Africa and Asia.
[Pronunciation] /ˈelɪfənt/ — stress on the first syllable; /f/ not /v/.
[Example] The elephant used its trunk to pick up the fruit.
[Collocations] 1) elephant in the room — an obvious problem nobody wants to talk about
2) herd of elephants — the usual group noun for elephants
```

| Field | Rule |
|-------|------|
| `[Word]` | The play; lowercase unless a fixed capital form is standard |
| `[POS]` | One primary POS for this play: noun / verb / adjective / adverb |
| `[Meaning]` | 1–2 short sentences; dictionary sense for that POS |
| `[Pronunciation]` | IPA (or clear stress) + one short pitfall tip |
| `[Example]` | One natural sentence in the stated POS |
| `[Collocations]` | 1–2 items; each = phrase + very short gloss |

Every AI play and every accepted user play gets a full word card.

### Scope

This skill hosts word chain only. Point users to `english-collocations` for collocation drills, `chengyu-jielong` for 成语接龙, `minimal-pairs` for phoneme drills, `english-tutor` for dialogue grammar.
