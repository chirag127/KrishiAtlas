import os
import sys
import re
import yaml
import json

VALID_STATUSES = {'draft', 'researched', 'reviewed', 'published', 'needs-update'}
VALID_EVIDENCE_GRADES = {'high', 'moderate', 'limited', 'mixed', 'not-yet-established'}

def parse_frontmatter(content):
    if not content.startswith('---'):
        return None, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content
    try:
        data = yaml.safe_load(parts[1])
        body = parts[2]
        return data, body
    except Exception as e:
        return {'_yaml_error': str(e)}, content

def validate_article(filepath, seen_ids, seen_slugs, catalog_map):
    errors = []
    warnings = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data, body = parse_frontmatter(content)
    if not data:
        return [f"Missing frontmatter in {filepath}"], []
    if '_yaml_error' in data:
        return [f"Invalid YAML frontmatter in {filepath}: {data['_yaml_error']}"], []

    # Required fields
    required_fields = ['id', 'title', 'part', 'part_title', 'slug', 'status', 'evidence_grade', 'book_include']
    for rf in required_fields:
        if rf not in data:
            errors.append(f"Missing required frontmatter field '{rf}' in {filepath}")

    art_id = data.get('id', '')
    if not re.match(r'^KA-\d{3,4}$', art_id):
        errors.append(f"Invalid ID format '{art_id}' in {filepath}")
    elif art_id in seen_ids:
        errors.append(f"Duplicate ID '{art_id}' found in {filepath} (previously seen in {seen_ids[art_id]})")
    else:
        seen_ids[art_id] = filepath

    slug = data.get('slug', '')
    if not slug:
        errors.append(f"Empty slug in {filepath}")
    elif slug in seen_slugs:
        errors.append(f"Duplicate slug '{slug}' in {filepath} (previously seen in {seen_slugs[slug]})")
    else:
        seen_slugs[slug] = filepath

    status = data.get('status', '')
    if status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}' in {filepath}. Must be one of {VALID_STATUSES}")

    evidence_grade = data.get('evidence_grade', '')
    if evidence_grade not in VALID_EVIDENCE_GRADES:
        errors.append(f"Invalid evidence_grade '{evidence_grade}' in {filepath}. Must be one of {VALID_EVIDENCE_GRADES}")

    title = data.get('title', '')
    if title.startswith('KA-'):
        warnings.append(f"Title has internal ID prefix: '{title}' in {filepath}")

    # Check against catalog if mapped
    if art_id in catalog_map:
        cat_info = catalog_map[art_id]
        if title != cat_info['title']:
            warnings.append(f"Article title '{title}' differs from catalog title '{cat_info['title']}'")

    # Word count and content depth
    words = len(re.findall(r'\b\w+\b', body))
    if status == 'published':
        if words < 600:
            errors.append(f"Published article {art_id} has only {words} words. Minimum substantive threshold is 600+ words.")
        if not data.get('source_ids'):
            errors.append(f"Published article {art_id} must have non-empty source_ids.")
        if not data.get('last_verified'):
            errors.append(f"Published article {art_id} must have a valid last_verified date.")

    # Strict TTS Paragraph-Only Enforcement: no raw HTML, no tables, no bullet lists, no numbered lists
    if status == 'published':
        if '<table' in body.lower() or '<div' in body.lower():
            errors.append(f"Published article {art_id} contains raw HTML tags, which breaks TTS flow.")
        if re.search(r'^\s*\|.*\|', body, re.MULTILINE):
            errors.append(f"Published article {art_id} contains markdown tables. Use pure narrative paragraphs for TTS.")
        if re.search(r'^\s*[-*]\s+', body, re.MULTILINE):
            errors.append(f"Published article {art_id} contains bullet lists. Use pure narrative paragraphs for TTS.")
        if re.search(r'^\s*\d+\.\s+', body, re.MULTILINE):
            errors.append(f"Published article {art_id} contains numbered lists. Use pure narrative paragraphs for TTS.")

    return errors, warnings

def run_validation():
    print("=" * 60)
    print("KrishiAtlas Content & Schema Validator")
    print("=" * 60)

    # Load catalog map
    catalog_map = {}
    if os.path.exists('scripts/inventory.json'):
        with open('scripts/inventory.json', 'r', encoding='utf-8') as f:
            inv = json.load(f)
            for a in inv.get('articles', []):
                catalog_map[a['id']] = a

    articles_dir = 'content/articles'
    if not os.path.exists(articles_dir):
        os.makedirs(articles_dir, exist_ok=True)

    files = [os.path.join(articles_dir, f) for f in os.listdir(articles_dir) if f.endswith('.md')]
    print(f"Discovered {len(files)} article files in {articles_dir}")

    seen_ids = {}
    seen_slugs = {}
    all_errors = []
    all_warnings = []
    status_counts = {s: 0 for s in VALID_STATUSES}

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        data, _ = parse_frontmatter(content)
        if data and 'status' in data:
            status_counts[data['status']] = status_counts.get(data['status'], 0) + 1

        errs, warns = validate_article(filepath, seen_ids, seen_slugs, catalog_map)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    print("\n--- Article Status Breakdown ---")
    for s, c in status_counts.items():
        print(f"  {s:<15}: {c}")

    if all_warnings:
        print(f"\n[!] Warnings ({len(all_warnings)}):")
        for w in all_warnings[:20]:
            print(f"  - {w}")
        if len(all_warnings) > 20:
            print(f"  ... and {len(all_warnings)-20} more warnings")

    if all_errors:
        print(f"\n[X] Errors ({len(all_errors)}):")
        for e in all_errors[:20]:
            print(f"  - {e}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors)-20} more errors")
        print("\nValidation FAILED.")
        return False
    else:
        print("\n[OK] All articles passed schema and integrity validation.")
        return True

if __name__ == '__main__':
    success = run_validation()
    sys.exit(0 if success else 1)
