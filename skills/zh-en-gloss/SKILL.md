---
name: zh-en-gloss
description: "Adds inline English glosses in parentheses after important Chinese terms in replies, e.g. 睡眠 (sleep), 焦虑症 (anxiety disorder). Use only when the user @mentions zh-en-gloss or explicitly asks for 附英文, 标注英文, 学单词, or inline English annotations while reading Chinese answers. Not for translation drills (use translation-practice-zh-en) or English conversation practice (use english-tutor)."
metadata:
  version: 1.0.0
---

# Chinese Reply with English Glosses (zh-en-gloss)

Answer the user's question normally in **Chinese**, but embed **English glosses** after important or complex terms so they can pick up vocabulary while reading.

This skill changes **output formatting only** — it does not turn the chat into a translation exercise or an English lesson.

## Activation (strict)

Apply gloss formatting **only when**:

- The user **@mentions `zh-en-gloss`**, or
- The user explicitly asks: 附英文、标注英文、学单词、括号里标英文、像截图那样标注, etc.

**Do not** apply glosses when the skill is merely installed but not @mentioned and not explicitly requested.

Once activated, keep glossing **for the rest of that conversation** until the user says 不用标注了、关闭英文、stop glossing, or similar.

If the user also @mentions a conflicting skill (e.g. `english-tutor` for mostly-English dialogue), follow the **latest explicit instruction**. Default when this skill is @mentioned: **Chinese prose + inline English glosses**.

## Format rules

1. **Pattern:** `中文词或短语 (English)` — one natural English phrase or term in parentheses.
2. **Phrase-level glosses**, not word-by-word chopping:
   - Good: `饭后散步 (a walk after meals)`
   - Bad: `饭后 (after meal) 散步 (walk)`
3. **Capitalization:** common phrases lowercase; proper nouns and established terms Title Case (`Redis`, `anxiety disorder`).
4. **Density (medium):**
   - Short reply (<3 sentences): **2–4** glosses
   - Substantive paragraph: **5–10** glosses
   - Numbered/bulleted lists: gloss **key learnable items** (like a priority list); skip glossing every item in a run of very common parallels (e.g. 睡眠不足、长期疲劳) if that would add noise
5. **Repeats:** gloss the **first** occurrence in the same message; later repeats may stay unglossed.
6. **Never gloss:** particles and ultra-common words (的、是、可以、因为), tokens already in English, code identifiers, URLs.
7. **Code blocks:** leave code unchanged; gloss Chinese prose **outside** code blocks only.
8. **No separate vocabulary appendix** unless the user asks — glosses stay inline for readable flow.
9. **Code citations** (` ```startLine:endLine:path `): do not insert glosses inside citation fences.

## What to gloss

**Prioritize:**

- Domain terms (medical, psychological, technical, business, etc.)
- Abstract concepts and multi-character compounds
- Collocations and phrases with a natural English equivalent

**Skip:**

- Elementary vocabulary obvious from context
- Personal and place names (unless the English form is pedagogically useful for the topic)

## Examples

### Health / stress (general topic)

If you are healthy but occasionally under high pressure, priorities are usually:

1. 睡眠 (sleep)
2. 运动 (exercise)
3. 饭后散步 (a walk after meals)
4. 咖啡因控制 (caffeine reduction)
5. 放松训练 (relaxation techniques)

Many “high pressure” feelings may come from 睡眠不足、长期疲劳、血糖波动、工作负荷过高 — gloss selectively here; do not force a gloss on every item.

Medication fits better for **焦虑症 (anxiety disorder)** and **惊恐障碍 (panic disorder)**.

### Technical topic (Redis cache penetration)

**缓存穿透 (cache penetration)** happens when requests hit keys that were never cached. Typical mitigations:

1. **布隆过滤器 (Bloom filter)** — block obviously invalid keys upstream
2. **空值缓存 (null-value caching)** — cache negative results with a short TTL
3. **参数校验 (parameter validation)** — reject bad queries before they reach the cache layer

Keep `Redis`, function names, and code snippets unglossed inside code blocks; gloss the surrounding Chinese explanation as above.
