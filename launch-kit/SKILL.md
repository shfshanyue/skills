---
name: launch-kit
description: "Generate a unified launch copy kit (launch-kit.md) for any product. Auto-scans the codebase for product info, then asks about missing fields. Use when the user mentions 'launch kit,' 'launch copy,' 'launch materials,' 'submission copy,' 'directory listing copy,' 'Product Hunt copy,' 'prepare launch assets,' or wants ready-to-paste copy for launching on multiple platforms."
metadata:
  version: 1.0.0
---

# Launch Kit Generator

You generate a unified launch copy kit — a single markdown document containing all the copy a maker needs to launch on Product Hunt, Hacker News, Indie Hackers, BetaList, AlternativeTo, G2, and other platforms and software directories. The output is designed for copy-paste submission.

---

## Workflow

### Step 1: Scan the Codebase

Automatically read the following files (skip any that don't exist):

**Product identity:**
- `README.md` — product name, description, features
- `package.json` / `Cargo.toml` / `pyproject.toml` — name, version, description, homepage
- `AGENTS.md` — project overview, architecture, core features, tech stack

**Marketing copy:**
- Landing page / homepage source code — hero copy, tagline, feature descriptions, social proof
- Pricing page source code — tiers, prices, feature breakdown
- About page source code — founder story, mission

**Product metadata:**
- `CHANGELOG.md` or changelog page — latest version, recent features
- Chrome Web Store / App Store listing files — existing store descriptions
- `manifest.json` (for extensions) — name, description, version

**Existing launch kit:**
- Search for any existing `launch-kit.md` in the project — if found, use it as the base for updates rather than generating from scratch

After scanning, build an internal summary of: product name, full name, website, store links, logo URL, pricing, version, core features, target audience, competitors, differentiators, testimonials, and founder context.

### Step 2: Generate Draft

Using the scanned information, generate the full launch-kit.md following the template structure below. For each section, produce the best copy you can from available information.

Write all copy in English. Be direct, benefit-oriented, and concise. Avoid marketing fluff. Match the brand voice found in the codebase.

**For multi-candidate sections** (Tagline, One-liner, Short Description, Medium Description):
- Generate distinct variants with different angles — the AI should freely choose the best variant directions based on the product's characteristics (e.g., founder story, feature-led, problem-led, outcome-led, differentiation-led)
- Label each variant (A, B, C, etc.) for easy reference

### Step 3: Identify Gaps and Ask

After generating the draft, list any fields that could not be reliably inferred from the codebase. Common gaps include:

- Testimonials / social proof quotes
- Founder story / personal motivation
- Competitor list (if not mentioned anywhere in the codebase)
- Aggregate rating or user count
- Logo URL
- Store listing URLs

Present the draft first, then ask about missing fields one section at a time. Do not block the draft on missing information — generate placeholder markers like `[TODO: add testimonials]` and let the user fill them in.

### Step 4: Output

**File location logic:**
1. If `launch-kit.md` already exists somewhere in the project → update it in place
2. Otherwise → create `docs/launch-kit.md`

After writing the file, show the user the complete document and ask if anything needs adjustment.

---

## Template Structure

The generated `launch-kit.md` must follow this structure:

```markdown
# [Product Name] Launch Kit

> Unified copy kit for all launch platforms and directory submissions.
> Copy-paste ready. Pick the best variant for each platform.

---

## Basic Info

| Field | Value |
|-------|-------|
| Product Name | |
| Full Name | |
| Website | |
| Store Link | |
| Logo | |
| Pricing | |
| Version | |

---

## Tagline (≤60 characters)

> Pick the best fit for each platform.

- **A:** [variant]
- **B:** [variant]
- **C:** [variant]

---

## One-liner (~140 characters)

- **A:** [variant]
- **B:** [variant]
- **C:** [variant]

---

## Short Description (~300 characters)

Suitable for: BetaList, Fazier, Uneed, SideProjectors, etc.

### Version A

> [copy]

### Version B

> [copy]

---

## Medium Description (~450 characters)

Suitable for: Product Hunt, Microlaunch, Peerlist, SaaSHub, etc.

### Version A

> [copy]

### Version B

> [copy]

---

## Features List

For platforms that ask for key features:

- **[Feature name]** — [one-sentence description]
- ...

---

## Categories / Tags

**Primary:** [tags]

**Secondary:** [tags]

**Long-tail (for directories):** [tags]

---

## Alternative To

For platforms like AlternativeTo, OpenAlternative, SaaSHub:

**[Product Name] is an alternative to:**
- [Competitor 1]
- [Competitor 2]
- ...

**What makes [Product Name] different:**
- [differentiator]
- ...

---

## Target Audience / Use Cases

For platforms that ask "Who is this for?":

- **[Persona]** — [use case description]
- ...

---

## Pricing Description

> **Free** — [what's included]
>
> **[Paid tier]** — [price] — [what's included]
>
> ...

---

## Proof Points / Social Proof

- [metric or fact]
- ...

**Testimonials (pick 1–2 per platform):**

> "[quote]" — [Name], [Title/Role]

---

## Product Hunt First Comment

### Version A

```text
[first comment copy]
```

**When to use:** [guidance]

### Version B

```text
[first comment copy]
```

**When to use:** [guidance]

---

## Hacker News / Indie Hackers Post Title

- **Show HN:** [title]
- **Show HN:** [title]
- **IH:** [title]

---

## Maker Story

For platforms that ask "Why did you build this?":

> [1-paragraph founder story]

---

## Quick Copy Reference

| Platform Type | Use These Sections |
|---|---|
| **BetaList, Fazier, Uneed, Microlaunch** | Tagline + Short Description + Features List + Categories |
| **Product Hunt** | Tagline + Medium Description + Features List + Maker Story + Proof Points + First Comment |
| **Hacker News, Indie Hackers** | HN Post Title + Maker Story + Medium Description |
| **Peerlist, SideProjectors** | Tagline + Medium Description + Features List + Target Audience |
| **SaaSHub, SaaS Genius** | One-liner + Medium Description + Categories + Alternative To + Pricing |
| **G2, Capterra** | Medium Description + Features List + Pricing + Proof Points |
| **AlternativeTo, OpenAlternative** | Short Description + Alternative To + Categories |
| **SourceForge, Softonic** | Medium Description + Features List + Categories + Pricing |
```

---

## Copy Guidelines

When writing copy for the launch kit, follow these principles:

- **Be specific, not generic.** "Tracks browsing time per URL path" beats "helps you be more productive."
- **Benefits over features.** Lead with what it does for the user, then explain how.
- **Respect character limits.** Each section specifies a target length — stay within ±10%.
- **No marketing fluff.** Avoid words like "revolutionary," "game-changing," "cutting-edge," "seamless," "powerful." Use plain language.
- **Show, don't tell.** Use concrete examples (e.g., "YouTube tutorials vs. YouTube Shorts") instead of abstract claims.
- **Vary the angles.** Each variant in a multi-candidate section should take a genuinely different approach — not just rephrase the same idea.
- **Match brand voice.** If the codebase has an established tone (casual, technical, friendly), match it.

---

## Related Skills

- **launch-strategy**: For planning the launch itself (phased approach, Product Hunt strategy, post-launch)
- **copywriting**: For writing or rewriting individual page copy in more depth
- **copy-editing**: For polishing existing copy
- **product-marketing-context**: For maintaining foundational positioning docs (separate from this kit)
