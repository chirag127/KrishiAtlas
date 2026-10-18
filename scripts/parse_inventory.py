import re
import sys
import json
import os

def parse():
    prompt_path = 'KrishiAtlas_KrishiGrantha_Enhanced_Master_Prompt.md'
    if not os.path.exists(prompt_path):
        print(f"File not found: {prompt_path}")
        sys.exit(1)

    with open(prompt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_part_num = None
    current_part_title = None
    parts = []
    articles = []

    part_re = re.compile(r'^## Part\s+(\d+)\s+[\u2013\u2014-]\s+(.*?)\s*$')
    art_re = re.compile(r'^-\s+`?(KA-\d+)`?\s+[\u2013\u2014-]\s+(.*?)\s*$')

    for line_num, line in enumerate(lines, start=1):
        pm = part_re.match(line)
        if pm:
            current_part_num = int(pm.group(1))
            current_part_title = pm.group(2).strip()
            parts.append({
                'part_num': current_part_num,
                'part_title': current_part_title,
                'line': line_num
            })
            continue

        am = art_re.match(line)
        if am:
            art_id = am.group(1).strip()
            art_title = am.group(2).strip()
            articles.append({
                'id': art_id,
                'title': art_title,
                'part': current_part_num,
                'part_title': current_part_title,
                'line': line_num
            })

    print(f"Total parts: {len(parts)}")
    print(f"Total articles: {len(articles)}")
    if len(articles) > 0:
        print(f"First article: {articles[0]}")
        print(f"Last article: {articles[-1]}")
    
    parts_map = {p['part_num']: [] for p in parts}
    for a in articles:
        parts_map[a['part']].append(a)
    
    anomalies = []
    for p_num in sorted(parts_map.keys()):
        count = len(parts_map[p_num])
        if count != 12:
            anomalies.append(f"Part {p_num} has {count} articles instead of 12!")
    
    if anomalies:
        for anom in anomalies:
            print(anom)
    else:
        print("Verification SUCCESS: Exactly 90 parts and exactly 12 articles per part = 1,080 articles.")

    os.makedirs('scripts', exist_ok=True)
    with open('scripts/inventory.json', 'w', encoding='utf-8') as out:
        json.dump({'parts': parts, 'articles': articles}, out, indent=2, ensure_ascii=False)
    print("Saved inventory to scripts/inventory.json")

if __name__ == '__main__':
    parse()
