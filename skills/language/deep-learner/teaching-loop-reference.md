# Teaching loop reference

Use this file for Phase 3 (per-node teaching) and Phase 4 (scoring).

## Deliberate practice

| Principle                 | How It Shows Up                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| **Target weaknesses**     | Diagnose blind spots early; after scoring, drill specifically on weak areas              |
| **Immediate feedback**    | After every answer: confirm correctness, explain why, and connect to the bigger picture  |
| **Push beyond comfort**   | When the learner answers correctly, escalate difficulty — don't linger on easy territory |
| **Purposeful repetition** | Low-scoring topics get revisited from new angles until mastered                          |

## Session tone

- **Language matching**: respond in the same language the learner uses throughout the session
- **Tone**: concise, encouraging, curious — celebrate progress but keep momentum
- After correct answers, the brief explanation is mandatory — it makes this feel like learning rather than testing

## Socratic pattern (every question)

1. **Set the stage** (3–6 sentences): context, scenario, thought experiment, or analogy
2. **Ask a guiding question** that emerges from the context
3. **Offer answer options** when applicable (open-ended for transfer questions)

## Question ladder (Q1–Q6 per node)

```
Q1: Concept recognition — relatable scenario, ask what's happening
Q2: Principle application — which principle applies and why
Q3: Scenario-based reasoning — two contrasting scenarios, reason through them
Q4: Identify the error — common misconception as a believable statement
Q5: Transfer & analogy — new context, apply what they've learned (open-ended)
Q6: Teach-back — explain the concept to a complete beginner
```

## Per-question rules

1. **One question per message** — never batch questions
2. Every question starts with context/narrative before the question itself
3. **On correct answer:** acknowledge reasoning, give 2–4 sentence depth explanation, set up the next question with new context
4. **On wrong answer:** use a follow-up scenario to expose the contradiction, log as "node weakness", re-approach from a fresh angle
5. **Hint ("I'd like a hint"):** clue embedded in a mini-scenario or analogy, then re-ask
6. Ground abstract concepts in analogies and real-world examples
7. **Teach-back (Q6):** evaluate for accuracy, simplicity, no jargon; if gaps remain, point out where a beginner would be confused and ask them to retry

## Question display format

> 💡 **Node: [Name]** | Progress: [X/Y] | Difficulty: ⭐⭐⭐
>
> [Context / scenario / thought experiment — 3–6 sentences]
>
> [Question that emerges from the context]
>
> A. [option]
> B. [option]
> C. [option]
> D. I'd like a hint

## Phase 4 — Scoring dimensions

- **Conceptual accuracy** (40%)
- **Ability to give examples** (30%)
- **Transfer & application** (30%)

After scoring, execute **in order**:

1. **Weakness Analysis Report:**

```
🔍 Weakness Analysis for [Node Name]:
  - Error 1: [what went wrong] → Root cause: [why]
  - Error 2: [what went wrong] → Root cause: [why]
📌 Recommended practice focus: [specific suggestion]
```

2. Re-render the Mermaid roadmap (see [`roadmap-reference.md`](roadmap-reference.md))
3. Update the text progress tracker
4. Handle the score:

| Score     | Action |
| --------- | ------ |
| **≥ 80**  | Mark node green ✅; before unlocking next node, issue **Summary Challenge** (summarize node in 3–5 sentences as if teaching a beginner); provide feedback, then unlock with 2–3 sentence key takeaways |
| **60–79** | Mark node orange 🟠; generate 2–3 targeted practice questions on weak spots, then re-score |
| **< 60**  | Mark node red 🔴; re-teach from weakest point with fresh questions until score ≥ 80 |
