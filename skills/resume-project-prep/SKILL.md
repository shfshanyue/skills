---
name: resume-project-prep
description: >
  Scan a project codebase to generate interview preparation materials and resume project descriptions.
  Use when the user mentions "resume project," "interview prep," "prepare for interview,"
  "project highlights," "interview questions," "analyze my project for interview,"
  "what to say about this project," "project experience," "walk me through your project,"
  "hardest thing you built," "most complex thing," "technical challenges," or wants to
  extract interview-worthy talking points from their codebase. Also trigger when someone
  wants help explaining a technical project to interviewers, preparing for behavioral
  technical questions, or writing the project section of their resume.
---

# Resume Project Prep

Scan a project codebase and generate a complete interview preparation document — including a polished resume project description and a structured Q&A guide covering complexity, design decisions, and technical highlights.

## Step 1: Determine Preferences

**Language**: Infer the output language from the language the user used in their prompt. If the user wrote in Chinese, output in Chinese. If in English, output in English. If ambiguous, briefly ask. Do not ask if the language is obvious.

**Target level**: Ask the user what seniority level they are targeting:
- Mid-level (2-5 years): Focus on independent problem-solving, decision-making
- Senior: Focus on system-level thinking, architecture trade-offs, scalability
- Both: Cover both perspectives

Wait for the user's answer before proceeding.

## Step 2: Scan the Codebase

Use `finder`, `Read`, `glob`, and `Grep` to systematically analyze the project:

### 2.1 Project Structure & Tech Stack
- Read the root directory listing
- Identify dependency files (package.json, go.mod, pom.xml, requirements.txt, Cargo.toml, etc.)
- Identify the framework, language, and major libraries

### 2.2 Architecture & Module Layout
- Map out the directory structure and module boundaries
- Identify architectural patterns (MVC, layered, microservices, event-driven, etc.)
- Find entry points, routing, middleware, configuration

### 2.3 Hunt for Interview-Worthy Code
This is the core of the skill. Look for code that is **complex, involves trade-offs, or solves real problems**. Specifically:

- **Concurrency / async handling**: goroutines, thread pools, async/await patterns, message queues, race condition prevention
- **Caching strategies**: Redis usage, cache invalidation logic, multi-level caching
- **Database design**: schema design, migrations, query optimization, transactions, sharding
- **Authentication & authorization**: JWT, OAuth, RBAC, middleware chains
- **Error handling & resilience**: retry logic, circuit breakers, graceful degradation
- **Performance optimization**: indexing, pagination, batch processing, connection pooling
- **Third-party integrations**: payment gateways, external APIs, webhook handling
- **Design patterns**: factory, strategy, observer, dependency injection, etc.
- **DevOps / infrastructure**: Dockerfile, CI/CD configs, deployment scripts, monitoring

For each area found, note the specific files and implementation details — these become the basis for interview talking points.

### 2.4 Filtering: What's "Worth Talking About"

Not everything is interview material. Prioritize items that meet at least one criterion:
- Required a non-obvious design decision (why X over Y?)
- Involved meaningful complexity (not just CRUD)
- Solved a real problem (performance, reliability, scalability)
- Demonstrates depth of understanding (not just library usage)

## Step 3: Generate the Output Document

Produce a single Markdown document with this structure:

```
# [Project Name] — Interview Preparation

## 1. Resume Project Description
(2-3 concise paragraphs suitable for direct use in a resume. Use an accomplishment-driven style:
what was built, what problems it solved, key technical choices, and measurable outcomes if possible.)

## 2. Technical Overview
- **Tech Stack**: [languages, frameworks, databases, infrastructure]
- **Architecture**: [pattern name + one-line description]
- **Core Modules**: [list with brief purpose of each]

## 3. Interview Q&A Guide

### Complexity & Challenges
1. **[Challenge Title]**
   - Situation: ...
   - How it was solved: ...
   - Reference answer: ...

### Design Decisions & Trade-offs
1. **[Decision Title]**
   - What was chosen and why
   - What was considered but rejected
   - Reference answer: ...

### Performance & Scalability
1. ...

### "The Hardest / Most Complex Thing You Did"
(Synthesize the single best answer from all findings above — pick the most
impressive point and craft a complete, compelling response.)

## 4. Go Deeper
You can ask me about any of the points above for a more detailed answer.
I'll explain with reference to the actual code and suggest follow-up questions
the interviewer might ask.
```

Adapt section depth to what the codebase actually contains. If the project has no caching logic, don't fabricate a caching section. Be honest and grounded in real code.

## Step 4: Follow-up Q&A Mode

After delivering the document, the user may ask about any specific point. When answering:

1. **Give a detailed answer** grounded in the actual codebase — reference specific files, functions, or patterns found during the scan.
2. **End every answer** with a section like:

> 💡 **Interviewer might follow up with:**
> 1. [Follow-up question 1]
> 2. [Follow-up question 2]
> 3. [Follow-up question 3]

The follow-up questions should be realistic — the kind of thing a real interviewer would dig into after hearing the initial answer. Think about: edge cases, failure scenarios, alternative approaches, production considerations, and "what would you do differently."

## Key Principles

- **Grounded in code**: Every claim must trace back to something real in the codebase. Never fabricate features or capabilities.
- **Interview-oriented**: Frame everything through the lens of "would an interviewer find this interesting?" Mundane CRUD operations are not interesting. Clever solutions to hard problems are.
- **Concise but deep**: The initial output should be scannable. Depth comes through follow-up questions.
- **Honest**: If the project is simple, say so honestly and help the user frame it in the best truthful light. Don't inflate complexity.
