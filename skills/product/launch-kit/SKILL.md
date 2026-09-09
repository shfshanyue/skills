---
name: launch-kit
description: "Launch kit generator. Use when the user wants ready-to-paste product launch copy, directory submission copy, Product Hunt/HN/Indie Hackers materials, or a multi-platform `launch-kit.md`."
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

**Done when:** every existing source above has been checked, an internal product summary exists, and unknown fields are explicitly marked as gaps.

### Step 2: Generate Draft

Using the scanned information, generate the full launch-kit.md following the template structure below. For each section, produce the best copy you can from available information.

Write all copy in English. Be direct, benefit-oriented, and concise. Avoid marketing fluff. Match the brand voice found in the codebase.

**For multi-candidate sections** (Tagline, One-liner, Short Description, Medium Description):
- Generate distinct variants with different angles — the AI should freely choose the best variant directions based on the product's characteristics (e.g., founder story, feature-led, problem-led, outcome-led, differentiation-led)
- Label each variant (A, B, C, etc.) for easy reference

**Done when:** the draft follows [`template.md`](template.md), each required section is present, and placeholders are limited to fields that could not be inferred.

### Step 3: Identify Gaps and Ask

After generating the draft, list any fields that could not be reliably inferred from the codebase. Common gaps include:

- Testimonials / social proof quotes
- Founder story / personal motivation
- Competitor list (if not mentioned anywhere in the codebase)
- Aggregate rating or user count
- Logo URL
- Store listing URLs

Present the draft first, then ask about missing fields one section at a time. Do not block the draft on missing information — generate placeholder markers like `[TODO: add testimonials]` and let the user fill them in.

**Done when:** the user has seen the draft and the first missing-field question targets one section only.

### Step 4: Output

**File location logic:**
1. If `launch-kit.md` already exists somewhere in the project → update it in place
2. Otherwise → create `docs/launch-kit.md`

After writing the file, show the user the complete document and ask if anything needs adjustment.

**Done when:** `launch-kit.md` has been created or updated at the selected path, the full document has been shown, and the user has a clear adjustment prompt.

---

## Template Structure

Use [`template.md`](template.md) as the single source of truth for the generated `launch-kit.md` structure.

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

## Skill Boundaries

This skill generates the launch copy kit. For broader launch strategy, copy polishing, or positioning work, hand off only when a matching installed skill is available or the user asks for that separate work.
