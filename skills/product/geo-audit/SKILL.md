---
name: geo-audit
description: "Audit website GEO and AI discoverability from a URL. Use when reviewing public-site signals, creating an explicitly requested prompt baseline, or testing actual AI answers about a brand."
metadata:
  version: 1.1.0
---

# GEO Audit

Review public website evidence separately from interpretation, recommendations, and any sampled AI answers. This is a diagnostic, not a promise of indexing, ranking, or citation.

## Steps

### 1. Fix the scope

Use the URL supplied by the user; do not infer a site from a brand name. Classify the request as a public-site audit, a prompt baseline, an actual AI-answer test, or an explicitly requested combination. A website-only audit does not generate prompts or query AI systems. Generate a prompt baseline only when requested; run actual-answer tests only when explicitly requested. For a broad request such as “run a GEO audit” that does not distinguish them, ask once whether the user wants only public website signals or also actual AI answers, then wait. If the URL is missing, ask once; combine the URL and scope questions when both are missing. Use the user's language and record any stated audience or page priorities.

**Done when:** the URL, requested scope, language, and stated priorities are recorded, or one consolidated clarification has been asked and the workflow is paused.

### 2. Collect bounded public evidence

Start with the supplied URL and record redirects and the final URL. Attempt the homepage, `/robots.txt`, and a sitemap linked by the site or at a conventional sitemap endpoint; record each outcome, including inaccessible or missing resources. Treat robots directives as declared policy only, not proof that a crawler follows them or that a page is indexed. Respect disallowed paths and access controls.

For an audit or actual-answer test, inspect no more than six representative public pages total, including the homepage when accessible. Prefer user-prioritized URLs and pages linked from primary navigation, such as about, product/service, pricing, documentation, or a relevant explainer. For an actual-answer test, collect enough evidence to ground neutral prompts. Do not exhaustively crawl. When a page is client-rendered, use an available browser when useful and label rendered evidence separately from direct fetches.

For each inspected URL, keep the access outcome, inspection method, and relevant evidence: access/canonical/robots signals; titles, headings, topics, audience, product or service facts and material claims; and inspectable structured data or self-contained, attributable passages. Record a short quote or concrete observation. Report unavailable, dynamic, or ambiguous evidence as unknown.

**Done when:** the homepage, robots file, and sitemap have each been attempted and recorded, and each sampled page has an exact URL, method, and observation or explicit unknown/access note; otherwise state the blocker and stop expanding the sample.

### 3. Assess website evidence when an audit is in scope

Organize findings under **Crawlability and site signals**, **Page topics and factual clarity**, and **Structured and quotable content**. Keep these layers distinct for each material finding:

- **Observed:** directly retrieved evidence, linked to its exact URL with a short quote or concrete value.
- **Inference:** what the evidence may mean for discoverability or answer extraction; label uncertainty and confidence.
- **Recommendation:** a specific, proportionate change tied to the finding.

Prioritize access blockers and ambiguity in core facts before editorial refinements. If useful, use High / Medium / Low with a brief impact rationale, not an opaque GEO score. State sampling, rendering, access, and content limits. Treat structured-data presence or syntax as an observation; do not claim eligibility or inclusion in search or AI results without direct evidence.

**Done when:** every material conclusion has linked observed evidence or is labeled as inference, every recommendation is tied to a finding, and material unknowns and sampling limits are stated.

### 4. Run optional actual AI-answer tests only when explicitly requested

Build three neutral prompts from inspected site evidence: **brand understanding** (what the brand does and whom it serves), **knowledge explanation** (a site-supported topic for a stated audience), and **product comparison** (the brand versus a user-named alternative or a clearly defined category for a use case). Keep wording factual and open-ended; never imply that the target brand should be recommended. Use the exact same prompt for each compared model or engine. Ask once only if a missing alternative or use case materially prevents a grounded comparison.

Prefer an available multi-model harness with selectable models. Probe the current environment and live help for model selection, web access, and tool-call controls before use; Cursor Agent CLI and Factory Droid are examples only, not assumed dependencies or cached command interfaces. If no harness is available, use independent subagents only when each model identity and independent access can be verified. If identity or independent access cannot be verified, state that a fair model comparison cannot be made; do not present an ordinary response as a query to ChatGPT Search, Perplexity, or another real product. A harness comparison is not equivalent to testing those products' interfaces. Claim a product-interface test only when that interface was directly tested, and identify its product and mode.

Default to the three prompt categories against one or two available, identifiable engines/models, with at least one recorded attempt per prompt and engine/model. Keep model and web-tool settings fixed across comparable attempts when possible; otherwise record each attempt's settings and tool calls. Repeat only when answers vary materially or the user asks. Use read-only queries: do not submit forms to or modify the target site.

For every attempt, retain the exact prompt and complete answer; provider/model/version as exposed; harness, subagent, or directly tested product and entry point; date and time with timezone; language and region; web/browsing status and tools called; repeat number; brand and competitor mentions; accuracy against evidence; and cited URLs in displayed order. Separate direct answer content from your accuracy assessment. Do not imply the sample represents all users or predicts stable rankings.

**Done when:** all three default categories have a grounded prompt and each requested engine/model attempt has the required record, or the report explicitly states which tests could not be run and why, without claiming an unperformed product test or fair comparison.

### 5. Build a monitoring-prompt baseline only when requested

Derive prompts from inspected topics and facts; do not invent offerings, audiences, competitors, or claims. Unless the user narrows scope, provide one neutral prompt in each of the three categories in Step 4, plus a compact note on what a later evaluator should record. A baseline is a set of test inputs, not test results; do not run it against AI systems. If the user requested actual tests but not a reusable baseline, report the test prompts with the results rather than silently creating a separate baseline deliverable.

**Done when:** each requested category has a grounded prompt and evaluation note, or a material missing detail has been identified and the user has been asked once; when no baseline was requested, none is produced.

### 6. Present the report

Use [`report.md`](report.md) as a compact structure and adapt or translate its headings to the user's language. Include scope and date, summary, evidence-linked findings, limitations, and next steps. Keep website **Observed / Inference / Recommendation** separate from the optional **AI Answer Test Results** section; include a prompt baseline only when requested. Write a file only when the user asks to save or export.

**Done when:** every requested deliverable is presented in the user's language, website observations/inferences/recommendations and AI test results are visibly distinct, evidence URLs and material limits are present, and no claim promises indexing, ranking, or citation.

## Boundaries

- GSC or GA4 performance and URL-inspection data → `google-traffic`.
- Ongoing alerts or scheduled monitoring → `automation-and-scheduling`, only when explicitly requested; a prompt baseline is not authorization to create a task.
- Website inspection covers public evidence; actual-answer results cover only the recorded model, harness, or directly tested product and mode. Neither establishes universal crawling, visibility, or ranking.
