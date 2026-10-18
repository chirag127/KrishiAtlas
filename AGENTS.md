# AGENTS.md — Durable Operating Rules for Agents and Subagents

Welcome to the **KrishiAtlas** and **KrishiGrantha** codebase. All automated or human agents working in this repository must strictly adhere to the rules below.

---

## 1. Role and Editorial Charter

- Maintain the highest standard of agricultural scholarship, economic realism, and scientific caution.
- Synthesize real agronomic, legal, and financial data from primary sources (ICAR, State Agricultural Universities, Ministry of Agriculture & Farmers Welfare, NABARD, APEDA, Income Tax Act, etc.).
- Never invent yields, pesticide recipes, drug doses, subsidy percentages, land prices, or profit claims. When local data is uncertain, state the exact requirements to obtain it.

---

## 2. File Ownership and Concurrency Rules

- **Canonical Articles:** Located strictly in `content/articles/` with the naming format `KA-[ID]-[slug].md`.
- **Concurrency:** When multiple agents run, each agent is assigned a disjoint range of article IDs (e.g. Agent 1: Part 1–10; Agent 2: Part 11–20). No two agents may modify the same article file, catalog file, or export file simultaneously.
- **Master Outputs:** The compiled book `exports/KrishiGrantha_Master.md` and manifest `exports/KrishiGrantha_Manifest.json` are generated exclusively via `scripts/build_book.py`. Never edit the master book manually.

---

## 3. Article Metadata and Content Standards

Each article markdown file MUST begin with valid YAML frontmatter:

```yaml
---
id: KA-001
title: "Exact approved title"
part: 1
part_title: "Exact part title"
slug: "what-agriculture-includes-and-where-its-boundaries-lie"
status: "published" # draft | researched | reviewed | published | needs-update
primary_topics: ["Agricultural Systems", "Farming Typology"]
region_scope: ["India", "Global"]
crops_or_enterprises: ["General"]
source_ids: ["SRC-0001", "SRC-0002"]
first_researched: "2026-10-18"
last_verified: "2026-10-18"
review_due: "2027-10-18"
evidence_grade: "high" # high | moderate | limited | mixed | not-yet-established
related_article_ids: ["KA-002", "KA-003"]
canonical_concepts: ["agriculture-scope", "farming-system-definition"]
book_include: true
---
```

### TTS & Read-Aloud Optimization

- Plain markdown paragraphs and descriptive headings.
- Avoid raw HTML, dense data tables, ASCII art, or decorative emojis inside article bodies.
- Spell out abbreviations upon first use (e.g., "Krishi Vigyan Kendra (KVK)").
- Frame mathematical calculations in clear narrative sentences.

---

## 4. Privacy, Credentials and Case Study Ethics

- Strictly exclude API keys, tokens, session cookies, database passwords, and `.env` files.
- The owner case study (`content/case-studies/owner-agriculture-vs-tcs.md` and Part 90) is **expressly authorized for public release**.
- Clearly mark owner-reported figures (e.g. 9-10 bighas / ~5 acres in Ghaziabad, ₹3.6 LPA TCS package) as unverified owner-reported context. Do not invent cadastral survey numbers or private personal names.

---

## 5. Continuous Validation and Checkpointing

After every batch of articles or code modifications:

1. Run `python scripts/validate_content.py` to ensure schema adherence.
2. Run `python scripts/check_duplicates.py` to prevent redundant prose or overlapping concepts.
3. Run `python scripts/build_book.py` to recompile `exports/KrishiGrantha_Master.md`.
4. Update `progress/STATUS.md`, `progress/TASKS.json`, and `PROJECT_STATE.md`.
