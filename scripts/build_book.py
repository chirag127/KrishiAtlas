import os
import sys
import re
import json
import hashlib
import yaml
from datetime import datetime, timezone

def parse_frontmatter(content):
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    try:
        data = yaml.safe_load(parts[1]) or {}
        body = parts[2]
        return data, body
    except Exception:
        return {}, content

def build_book():
    print("=" * 60)
    print("KrishiGrantha Master Book Compiler")
    print("=" * 60)

    os.makedirs('exports', exist_ok=True)
    inventory_path = 'scripts/inventory.json'
    if not os.path.exists(inventory_path):
        print("Inventory not found at scripts/inventory.json")
        sys.exit(1)

    with open(inventory_path, 'r', encoding='utf-8') as f:
        inv = json.load(f)

    parts = inv['parts']
    articles = inv['articles']
    articles_by_id = {a['id']: a for a in articles}

    # Map files in content/articles
    articles_dir = 'content/articles'
    os.makedirs(articles_dir, exist_ok=True)
    file_map = {}
    for fname in os.listdir(articles_dir):
        if fname.endswith('.md'):
            fpath = os.path.join(articles_dir, fname)
            m = re.match(r'^(KA-\d{3,4})', fname)
            if m:
                file_map[m.group(1)] = fpath
            else:
                with open(fpath, 'r', encoding='utf-8') as f:
                    fm, _ = parse_frontmatter(f.read())
                    if 'id' in fm:
                        file_map[fm['id']] = fpath

    print(f"Found {len(file_map)} source article files mapped to catalog.")

    book_lines = [
        "# KrishiGrantha",
        "",
        "## The Complete Agriculture Knowledge Compendium",
        "### Evidence-Based Agriculture, Farm Economics and Rural Enterprise in India and the World",
        "",
        f"> **Edition & Build Timestamp:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        "> **Canonical Source:** KrishiAtlas Agricultural Knowledge Base  ",
        "> **Editorial Scope:** Comprehensive multi-disciplinary compendium across 90 parts, 1,080 topics, Indian agronomy, farm economics, legal frameworks, public schemes, and empirical decision models.",
        "",
        "---",
        "",
        "## Editorial Note & Scientific Limitations",
        "",
        "KrishiGrantha is compiled as a unified, text-to-speech optimized, evidence-based agricultural reference work. All agronomic packages of practices, fertilizer doses, chemical crop protections, tax statutes, and government subsidy norms are grounded in verified official sources, including the Indian Council of Agricultural Research (ICAR), State Agricultural Universities (SAUs), the Ministry of Agriculture & Farmers Welfare, the Commission for Agricultural Costs & Prices (CACP), NABARD, and the Income-tax Act, 1961.",
        "",
        "Agricultural outcomes are inherently dependent upon local soil biology, weather variations, aquifer depth, local labour markets, and price volatility. No crop model or enterprise profile in this compendium represents a guaranteed financial return. Chemical crop protection prescriptions must adhere strictly to label claims registered by the Central Insecticides Board & Registration Committee (CIBRC); readers should consult their local Krishi Vigyan Kendra (KVK) for on-ground diagnostics.",
        "",
        "The owner decision analysis case study in Part 90 is published with informed authorization to evaluate corporate technology employment against agricultural enterprise under verified Western Uttar Pradesh conditions, with unverified personal and property estimates explicitly marked.",
        "",
        "---",
        "",
        "## Table of Contents",
        ""
    ]

    # Build TOC outline
    parts_map = {p['part_num']: {'title': p['part_title'], 'articles': []} for p in parts}
    for a in articles:
        parts_map[a['part']]['articles'].append(a)

    for p_num in sorted(parts_map.keys()):
        p_info = parts_map[p_num]
        book_lines.append(f"- **Part {p_num:02d} — {p_info['title']}**")
        for a in p_info['articles']:
            has_file = a['id'] in file_map
            status_tag = "" if has_file else " *(In Progress)*"
            book_lines.append(f"  - {a['title']}{status_tag}")
    book_lines.append("")
    book_lines.append("---")
    book_lines.append("")

    # Compile articles
    manifest_articles = []
    total_words = 0
    included_count = 0

    for p_num in sorted(parts_map.keys()):
        p_info = parts_map[p_num]
        book_lines.append(f"## Part {p_num:02d} — {p_info['title']}")
        book_lines.append("")

        for a in p_info['articles']:
            art_id = a['id']
            if art_id in file_map:
                fpath = file_map[art_id]
                with open(fpath, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                fm, body = parse_frontmatter(raw_content)
                f_hash = hashlib.sha256(raw_content.encode('utf-8')).hexdigest()
                words = len(re.findall(r'\b\w+\b', body))
                total_words += words
                included_count += 1

                # Clean heading levels in body: change H1 to H3, H2 to H4, etc.
                cleaned_body_lines = []
                for line in body.splitlines():
                    if line.startswith('# '):
                        # Skip top-level article H1 if it repeats title
                        continue
                    elif line.startswith('## '):
                        cleaned_body_lines.append('#### ' + line[3:])
                    elif line.startswith('### '):
                        cleaned_body_lines.append('##### ' + line[4:])
                    else:
                        cleaned_body_lines.append(line)

                cleaned_body = '\n'.join(cleaned_body_lines).strip()

                book_lines.append(f"### {a['title']}")
                book_lines.append("")
                book_lines.append(f"*Catalog ID: {art_id} | Evidence Grade: {fm.get('evidence_grade', 'unverified')}*")
                book_lines.append("")
                book_lines.append(cleaned_body)
                book_lines.append("")
                book_lines.append("---")
                book_lines.append("")

                manifest_articles.append({
                    'id': art_id,
                    'title': a['title'],
                    'part': p_num,
                    'part_title': p_info['title'],
                    'file': fpath.replace('\\', '/'),
                    'sha256': f_hash,
                    'word_count': words,
                    'status': fm.get('status', 'draft'),
                    'included_in_book': True
                })
            else:
                manifest_articles.append({
                    'id': art_id,
                    'title': a['title'],
                    'part': p_num,
                    'part_title': p_info['title'],
                    'file': None,
                    'sha256': None,
                    'word_count': 0,
                    'status': 'pending',
                    'included_in_book': False
                })

    # Case study special append if present and not yet in Part 90 articles
    case_study_path = 'content/case-studies/owner-agriculture-vs-tcs.md'
    if os.path.exists(case_study_path):
        with open(case_study_path, 'r', encoding='utf-8') as f:
            cs_content = f.read()
        cs_fm, cs_body = parse_frontmatter(cs_content)
        cs_words = len(re.findall(r'\b\w+\b', cs_body))
        total_words += cs_words
        book_lines.append("## Special Authorized Appendix — Owner Case Study")
        book_lines.append("")
        book_lines.append("### Owner Decision Analysis: Corporate IT Employment vs. Ghaziabad Agricultural Enterprise")
        book_lines.append("")
        book_lines.append(cs_body.strip())
        book_lines.append("")
        book_lines.append("---")
        book_lines.append("")

    master_md_content = '\n'.join(book_lines)
    master_path = 'exports/KrishiGrantha_Master.md'
    with open(master_path, 'w', encoding='utf-8') as f:
        f.write(master_md_content)

    # Plain text export
    txt_path = 'exports/KrishiGrantha_Master.txt'
    # Strip markdown symbols for clean text
    plain_text = re.sub(r'#+\s*', '', master_md_content)
    plain_text = re.sub(r'\*\*(.*?)\*\*', r'\1', plain_text)
    plain_text = re.sub(r'\*(.*?)\*', r'\1', plain_text)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(plain_text)

    # Manifest
    manifest = {
        'book_title': "KrishiGrantha — The Complete Agriculture Knowledge Compendium",
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_catalog_articles': len(articles),
        'included_articles_count': included_count,
        'total_words': total_words,
        'master_md_file': master_path,
        'master_md_sha256': hashlib.sha256(master_md_content.encode('utf-8')).hexdigest(),
        'articles': manifest_articles
    }

    manifest_path = 'exports/KrishiGrantha_Manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated {master_path} ({len(master_md_content.encode('utf-8')):,} bytes, {total_words:,} words)")
    print(f"[OK] Generated {txt_path}")
    print(f"[OK] Generated {manifest_path} with {included_count}/{len(articles)} articles included.")

if __name__ == '__main__':
    build_book()
