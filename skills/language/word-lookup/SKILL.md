---
name: word-lookup
description: "Lookup host. Use when the user wants a dictionary entry for an English word, phrase, or idiom, or 查单词. For collocation drills, use `english-collocations`; for word-chain cards, use `word-chain`."
metadata:
  version: 1.1.0
---

# Word Lookup

Host one **lookup card** per target: a single **lemma** or a multi-word **phrase entry** (phrasal verb, idiom, prepositional phrase). One **sense** per card; headings in the order below. Chinese learner card; IPA on every related English **word** in list sections.

## Steps

### 1. Open

Take the lookup target from the message. If none, ask once for the word or phrase and wait.

Classify the target:

| Kind | When |
|------|------|
| **Phrase entry** | User names or quotes **two or more** English words as one unit (`make up one's mind`, `in spite of`, `look forward to`) |
| **Lemma** | Otherwise — one word (including hyphenated compounds queried as one token: `well-being`) |

Pick **one sense** (phrase or word): context in the message, otherwise the most common. Emit one **lookup card** using the matching rules in **Lookup card**.

**Done when:** a complete lookup card is in the chat, or one question has asked for the missing target.

### 2. Host each user message

Classify, then take exactly one branch:

| Branch | When | Action |
|--------|------|--------|
| New target | A different English word or phrase | Open a new lookup card for that target |
| Other sense | User names a POS/sense from **其他义项** | Open a new lookup card for that sense |
| Expand | User asks to thicken one heading | Add list items under that H2 only; leave the rest |
| Hand-off | Collocation drill, word-chain, phoneme drill, or dialogue | One-line hand-off to the owning skill |
| Else | Treat as New target when it is a word or phrase; otherwise one clarifying question | — |

**Done when:** a new or updated card is in the chat, a hand-off has named the next skill, or one question is waiting.

## Reference

### Lookup card

Renderable markdown — headings render as headings. Output the card directly; code fences only for actual code.

`#` title = the queried **lemma** (lowercase unless a fixed capital form) or the **phrase** as the user gave it (keep `I`, `sb`/`sth` placeholders if present). Then these `##` headings, in this order, every time:

| Heading | Lemma | Phrase entry |
|---------|-------|----------------|
| **词性** | One POS (`noun` / `verb` / `adj` / `adv`) | Unit type: `phrasal verb` / `idiom` / `prepositional phrase` / `noun phrase` / `fixed expression` |
| **音标** | IPA; BrE/AmE differ → `BrE /…/; AmE /…/` | IPA for the **whole phrase** on one line; BrE/AmE differ → same split |
| **释义** | 1–2 sentences Chinese | Same |
| **英英释义** | 1–2 sentences English; learner-friendly | Same |
| **简单例句** | List; 1–2 sentences in this POS | List; 1–2 sentences using the **whole phrase** |
| **常见搭配** | List; 3–5: `phrase — 短中文` (co-occurrence) | List; 3–5 **frames or collocates** that take this phrase (`finally make up one's mind — 终于下定决心`); do not repeat the H1 phrase alone |
| **常见词组** | List; 2–4 frozen chunks | List; 2–4 **related** idioms/phrases (`change one's mind — 改变主意`); not the H1 phrase |
| **派生词** | List; 3–6 affixal lexemes: `word /IPA/ 短中文` | List; affixal forms of the **head word** only (phrasal verb → main verb; `in spite of` → `spite /spaɪt/ 恶意` if useful). Nothing useful → one item `- 无常见派生词` |
| **形近词** | List; 2–4: `word /IPA/ 短中文 — 易混处` | List; 2–4 **confusable phrases or words**; every **English word** token in the line has IPA (`make up /ˈmeɪkʌp/ 化妆 — 名词，非本义`) |
| **词源** | 1–2 sentences | Same; may trace the head word or the idiom's history |
| **同源词** | List; 2–5 English etymon cousins: `word /IPA/ 短中文`; else `- 无常见英文同源词` | List from **head word** etymon when clear; else `- 无常见英文同源词` |
| **其他义项** | Other POS for this spelling (`noun — 行为、法令`). None → `无` | Other senses of the **same surface form** (`make up — 化妆；编造`). None → `无` |

List headings: one `-` item per line. **派生词** / **形近词** / **同源词**: every listed **English word** carries IPA in the same style as **音标** (when BrE/AmE both appear on **音标**, related words use the first). A word with two POS readings uses the reading that belongs in that list.

**Lemma:** **派生词** = affixal lexemes of this stem. **同源词** = English cousins from the same etymon (`act` → `agent`). **词源** may name Latin or Old English; **同源词** stays English.

**Phrase entry:** treat the user’s string as one dictionary unit. **Head word** = main verb (`make up one's mind` → `make`) or the fixed pivot (`in spite of` → `spite`). Do not split into separate lookup cards unless the user asks for a single word inside the phrase.

Worked example (output as raw markdown, not in a code fence):

> # act
>
> ## 词性
> verb
>
> ## 音标
> /ækt/
>
> ## 释义
> 行动、做事；采取某种做法。
>
> ## 英英释义
> To do something for a particular purpose, or to behave in a particular way.
>
> ## 简单例句
> - We have to act now before the problem gets worse.
>
> ## 常见搭配
> - act on — 根据…采取行动
> - act as — 充当、起…作用
> - act quickly — 迅速行动
>
> ## 常见词组
> - act out — 用行动表现（情绪或故事）
> - catch sb in the act — 当场抓住
>
> ## 派生词
> - action /ˈækʃn/ 行动
> - active /ˈæktɪv/ 活跃的
> - actor /ˈæktə(r)/ 演员
> - inactive /ɪnˈæktɪv/ 不活跃的
>
> ## 形近词
> - exact /ɪɡˈzækt/ 精确的 — 不是 act 词族
> - fact /fækt/ 事实 — 词源不同
>
> ## 词源
> 来自拉丁 *agere*「做」，经古法语进入英语。
>
> ## 同源词
> - agent /ˈeɪdʒənt/ 代理人
> - agenda /əˈdʒendə/ 议程
> - agile /ˈædʒaɪl/ 敏捷的
>
> ## 其他义项
> noun — 行为；法令

Phrase entry example:

> # make up one's mind
>
> ## 词性
> idiom
>
> ## 音标
> /ˌmeɪk ʌp wʌnz ˈmaɪnd/
>
> ## 释义
> 下定决心；做出决定（尤指犹豫之后）。
>
> ## 英英释义
> To decide what you want to do or choose after thinking about it.
>
> ## 简单例句
> - She finally made up her mind and accepted the offer.
>
> ## 常见搭配
> - finally make up one's mind — 终于下定决心
> - can't make up one's mind — 拿不定主意
> - make up your mind about — 对…作出决定
>
> ## 常见词组
> - change one's mind — 改变主意
> - bear in mind — 记住、考虑到
> - have a mind of one's own — 有主见
>
> ## 派生词
> - maker /ˈmeɪkə(r)/ 制造者
> - makeup /ˈmeɪkʌp/ 化妆品；构成
> - mindful /ˈmaɪndfəl/ 留心的
>
> ## 形近词
> - make up /ˈmeɪkʌp/ 编造；化妆 — 不同义项
> - make up for /ˌmeɪk ˈʌp fə(r)/ 弥补 — 接 for，非「下决心」
>
> ## 词源
> `make up` 本义「拼凑、组成」；`mind` 来自古英语「记忆、心意」。合为「把心意定下来」。
>
> ## 同源词
> - remind /rɪˈmaɪnd/ 提醒
> - mental /ˈmentl/ 心理的
>
> ## 其他义项
> 无（本卡为 idiom「下决心」；`make up` 单独有「化妆、编造」等义，见 **形近词**）

### Scope

Dictionary lookup only. Cross-link: `english-collocations` (collocation drills), `word-chain` (word-chain cards), `minimal-pairs` (phoneme drills), `english-tutor` (dialogue grammar).
