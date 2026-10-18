# KrishiAtlas & KrishiGrantha

**KrishiAtlas** is an open-access, evidence-based encyclopedia of Indian and global agriculture, rural economics, farm taxation, land policy, public subsidies, and agribusiness strategy.

**KrishiGrantha** is the comprehensive, concatenated reference compendium automatically compiled from the canonical Markdown article corpus into `exports/KrishiGrantha_Master.md` for text-to-speech (TTS) accessibility and high-quality Markdown-to-PDF generation.

---

## Project Structure & Architecture

```
KrishiAtlas/
├── content/
│   ├── articles/                    # Canonical individual article files (KA-001 through KA-1080)
│   ├── case-studies/                # Authorized public decision case studies
│   │   └── owner-agriculture-vs-tcs.md
│   ├── ARTICLE_CATALOG.md           # Master 90-part, 1,080-article authoritative catalog
│   ├── SOURCE_REGISTRY.md           # Authoritative primary institutions and legal statutes
│   ├── SUBSIDY_AND_BENEFIT_REGISTER.md  # Central and State agricultural subsidy dossier
│   ├── TAX_LAW_REGISTER.md          # Direct (Sec 10(1)) and indirect (GST) farm tax rules
│   ├── LEARNING_OPPORTUNITY_REGISTER.md # Free government courses, KVK training, MOOCs
│   ├── LAND_MARKET_RESEARCH.md      # Farmland purchase restrictions, circle rates, due diligence
│   ├── PROFITABILITY_EVIDENCE_REGISTER.md # CACP cost frameworks (A1, A2, C2), enterprise ROCE
│   ├── STATE_AND_DISTRICT_COVERAGE.md  # All 28 Indian States & 8 Union Territories matrix
│   ├── GLOSSARY.md                  # Plain-language, TTS-ready definitions
│   ├── METHODS_AND_LIMITATIONS.md   # Research standards, evidence grading, financial caveats
│   ├── ERRATA.md                    # Dated factual correction register
│   ├── FACT_CHECK_QUEUE.md          # Live fact-checking pipeline
│   └── DUPLICATION_INDEX.json       # Concept mapping to prevent semantic overlap
├── exports/
│   ├── KrishiGrantha_Master.md      # Deterministic compiled master book
│   ├── KrishiGrantha_Master.txt     # Clean plain-text book export
│   └── KrishiGrantha_Manifest.json  # Checksums, word counts, and build metadata
├── progress/
│   ├── STATUS.md                    # Chronological execution and session log
│   └── TASKS.json                   # Machine-readable task and milestone tracker
├── scripts/
│   ├── validate_content.py          # Frontmatter and schema validator
│   ├── check_duplicates.py          # Paragraph and concept redundancy detector
│   ├── check_coverage.py            # Inventory progress and completion reporter
│   ├── check_links.py               # Internal link and source registry verifier
│   ├── build_book.py                # Deterministic concatenator for KrishiGrantha
│   ├── test_book.py                 # Acceptance test suite for master book
│   └── privacy_audit.py             # Security, credential, and secret audit
├── AGENTS.md                        # Durable multi-agent operating rules
├── DECISIONS.md                     # Architectural, UX, and technical decision records
└── PROJECT_STATE.md                 # Live authoritative project state
```

---

## Core Features & Content Principles

1. **Deterministic Master Catalog:** 90 parts, exactly 12 named articles per part = **1,080 base articles** (`KA-001` through `KA-1080`).
2. **Scientific & Legal Caution:** Recommendations for pesticides, fertilizer rates, seed treatments, and veterinary care are strictly restricted to official label claims (CIBRC, ICAR, SAUs).
3. **Rigorous Economic Realism:** Full separation of gross revenue from true economic profit (CACP Cost C2). All crop models account for land opportunity cost, family labour, working capital interest, price volatility, and post-harvest losses.
4. **Authorized Public Case Study:** Includes the prominently published decision analysis (`content/case-studies/owner-agriculture-vs-tcs.md` and Part 90) evaluating corporate IT employment at TCS Bhubaneswar (₹3.6 LPA package) versus family land enterprise in Ghaziabad, UP, with unverified personal and land data explicitly marked.
5. **Zero-Cost Deployment:** Static-first web architecture hostable on GitHub Pages with zero paid APIs, zero tracking cookies, and client-side deterministic search.

---

## Development & Build Commands

### 1. Validate Article Frontmatter & Content
```bash
python scripts/validate_content.py
```

### 2. Detect Redundant or Duplicate Paragraphs
```bash
python scripts/check_duplicates.py
```

### 3. Check Inventory Coverage
```bash
python scripts/check_coverage.py
```

### 4. Build KrishiGrantha Master Book & Manifest
```bash
python scripts/build_book.py
```

### 5. Run Book Acceptance Tests
```bash
python scripts/test_book.py
```

### 6. Run Privacy & Secret Audit
```bash
python scripts/privacy_audit.py
```

---

## Ethical Boundaries & Privacy Standard
- KrishiAtlas strictly excludes all API keys, private passwords, tokens, `.env` files, and local machine usernames from public exports and repositories.
- The owner case study is published with informed authorization. No unprovided exact village survey numbers, property coordinates, or private personal names are invented.
