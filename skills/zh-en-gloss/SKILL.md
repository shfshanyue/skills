---
name: zh-en-gloss
description: "Adds inline English glosses in parentheses after important Chinese terms in replies, e.g. 有氧运动 (aerobic exercise), 均衡饮食 (balanced diet). Use whenever this skill is installed — default on for Chinese prose answers so the user can learn vocabulary while reading. Apply glosses unless the user opts out (不用标注、纯中文、stop glossing) or a conflicting skill takes over (english-tutor, translation-practice-zh-en). Not for translation drills or mostly-English dialogue."
metadata:
  version: 1.2.0
---

# Chinese Reply with English Glosses (zh-en-gloss)

Answer the user's question normally in **Chinese**, but embed **English glosses** after important or complex terms so they can pick up vocabulary while reading.

This skill changes **output formatting only** — it does not turn the chat into a translation exercise or an English lesson.

## Activation (default on)

**When this skill is installed, apply gloss formatting by default** on Chinese prose in your replies.

**Opt out** for the rest of the conversation when the user says: 不用标注了、关闭英文、纯中文、不要括号英文、stop glossing, or similar.

**Do not gloss** when:

- The user asks for a **mostly-English** reply or is clearly practicing English dialogue (`english-tutor` active or @mentioned)
- The user is doing a **translation drill** (`translation-practice-zh-en` active or @mentioned)
- The reply is **already mostly English** (e.g. code review in English, pasted English text)
- The user explicitly wants **no inline annotations** for this message

If the user @mentions `zh-en-gloss` after opting out, **re-enable** glossing for the rest of that conversation unless they opt out again.

When another skill conflicts, follow the **latest explicit instruction**. Default with this skill installed: **Chinese prose + inline English glosses**.

## Format rules

1. **Pattern:** `中文词或短语 (English)` — one natural English phrase or term in parentheses.
2. **Phrase-level glosses**, not word-by-word chopping:
   - Good: `饭后散步 (a walk after meals)`
   - Bad: `饭后 (after meal) 散步 (walk)`
3. **Capitalization:** common phrases lowercase; proper nouns and established terms Title Case (`Redis`, `mindfulness meditation`).
4. **Density — allocate per paragraph/section, not per whole reply:**
   - **Unit of counting:** each plain-text **paragraph** or each block under a **`###` heading** gets its own gloss budget. Never treat the entire message as one shared pool.
   - **Short reply** (<3 sentences, single block): **4–8** glosses for that block
   - **Each substantive paragraph or section:** **3–6** glosses in that block alone
   - **Long reply** (4+ paragraphs or 2+ headings): **every** Chinese prose paragraph/section must meet the **3–6** quota — including the **last** paragraphs; do not taper off toward the end
   - **Do not front-load:** finishing early sections does not reduce later sections' quota
   - **Numbered/bulleted lists:** gloss **key learnable items** per list (at least one gloss on the head term of each numbered item when the list is teaching content); skip glossing every item in a run of very common parallels (e.g. 晨间拉伸、多喝水、优质蛋白) only when that would add noise
5. **Repeats:** within the **same paragraph/section**, gloss the **first** occurrence; in a **new** paragraph or section, you may gloss the same term again if it is central there.
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

### Wellness / healthy habits (general topic)

If you want to build a sustainable daily routine, a solid foundation usually looks like:

1. 规律作息 (a regular sleep schedule)
2. 有氧运动 (aerobic exercise)
3. 饭后散步 (a walk after meals)
4. 均衡饮食 (a balanced diet)
5. 正念冥想 (mindfulness meditation)

Good energy often comes from 晨间拉伸、多喝水、优质蛋白、户外活动 — gloss selectively here; do not force a gloss on every item.

**长期坚持 (long-term consistency)** and **适度恢复 (adequate recovery)** matter more than occasional all-out pushes for building **精力 (energy)** and **专注力 (focus)**.

### Long reply — even density across sections

**Section 1 — 作息 (sleep schedule):** 固定起床时间 (a fixed wake-up time) 比偶尔早睡更重要；**睡眠质量 (sleep quality)** 影响第二天的 **专注力 (focus)**。

**Section 2 — 运动 (exercise):** 每周三次 **有氧运动 (aerobic exercise)** 就够；**过度训练 (overtraining)** 反而拖慢 **恢复 (recovery)**。

**Section 3 — 总结 (summary):** **可持续 (sustainable)** 的小习惯，比短期 **拼命 (all-out effort)** 更值得 **坚持 (stick with)**。

Wrong pattern: 8 glosses in section 1, 0 in sections 2–3. Each section above carries its own **3–6** glosses.

### Technical topic (Redis cache penetration)

**缓存穿透 (cache penetration)** happens when requests hit keys that were never cached. Typical mitigations:

1. **布隆过滤器 (Bloom filter)** — block obviously invalid keys upstream
2. **空值缓存 (null-value caching)** — cache negative results with a short TTL
3. **参数校验 (parameter validation)** — reject bad queries before they reach the cache layer

Keep `Redis`, function names, and code snippets unglossed inside code blocks; gloss the surrounding Chinese explanation as above.
