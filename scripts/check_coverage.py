import os
import sys
import json
import re
import yaml

def check_coverage():
    print("=" * 60)
    print("KrishiAtlas Catalog Coverage & Completion Tracker")
    print("=" * 60)

    with open('scripts/inventory.json', 'r', encoding='utf-8') as f:
        inv = json.load(f)

    total_catalog = len(inv['articles'])
    parts = inv['parts']
    articles_by_part = {p['part_num']: [] for p in parts}
    for a in inv['articles']:
        articles_by_part[a['part']].append(a)

    articles_dir = 'content/articles'
    existing_files = [f for f in os.listdir(articles_dir) if f.endswith('.md')] if os.path.exists(articles_dir) else []

    file_by_id = {}
    status_by_id = {}
    words_by_id = {}

    for fname in existing_files:
        fpath = os.path.join(articles_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        art_id = None
        status = 'draft'
        body = content
        if content.startswith('---'):
            parts_split = content.split('---', 2)
            if len(parts_split) >= 3:
                try:
                    fm = yaml.safe_load(parts_split[1]) or {}
                    art_id = fm.get('id')
                    status = fm.get('status', 'draft')
                    body = parts_split[2]
                except Exception:
                    pass

        if not art_id:
            m = re.match(r'^(KA-\d{3,4})', fname)
            if m:
                art_id = m.group(1)

        if art_id:
            file_by_id[art_id] = fname
            status_by_id[art_id] = status
            words_by_id[art_id] = len(re.findall(r'\b\w+\b', body))

    published_count = sum(1 for s in status_by_id.values() if s == 'published')
    researched_count = sum(1 for s in status_by_id.values() if s in ('researched', 'reviewed'))
    draft_count = sum(1 for s in status_by_id.values() if s == 'draft')
    total_written = len(file_by_id)
    total_words = sum(words_by_id.values())

    print(f"Total Base Catalog Articles : {total_catalog}")
    print(f"Articles Written to Disk    : {total_written} ({total_written/total_catalog*100:.1f}%)")
    print(f"  - Fully Published         : {published_count}")
    print(f"  - Researched / Reviewed   : {researched_count}")
    print(f"  - Drafts                  : {draft_count}")
    print(f"Total Word Count Across All : {total_words:,} words")
    print(f"Average Words per Article   : {total_words/max(1, total_written):.0f} words\n")

    # Part by part summary
    print(f"{'Part':<6} {'Title':<45} {'Done':<6} {'Target':<6} {'Status':<12}")
    print("-" * 75)
    for p in parts:
        p_num = p['part_num']
        p_title = p['part_title'][:43]
        p_arts = articles_by_part[p_num]
        done_in_part = sum(1 for a in p_arts if a['id'] in file_by_id and status_by_id.get(a['id']) == 'published')
        p_status = "Complete" if done_in_part == len(p_arts) else f"{done_in_part}/{len(p_arts)}"
        print(f"{p_num:<6} {p_title:<45} {done_in_part:<6} {len(p_arts):<6} {p_status:<12}")

    return total_written, published_count, total_catalog

if __name__ == '__main__':
    check_coverage()
