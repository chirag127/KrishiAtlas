import os
import sys
import json
import re

def build_search_index():
    print("=" * 60)
    print("KrishiAtlas Search Index Generator")
    print("=" * 60)

    index_items = []

    # 1. Index Articles from scripts/inventory.json
    inv_path = 'scripts/inventory.json'
    if os.path.exists(inv_path):
        with open(inv_path, 'r', encoding='utf-8') as f:
            inv = json.load(f)

        for a in inv.get('articles', []):
            index_items.append({
                'id': a['id'],
                'type': 'article',
                'title': a['title'],
                'part': a['part'],
                'part_title': a['part_title'],
                'url': f"article.html?id={a['id']}",
                'keywords': f"{a['title']} Part {a['part']} {a['part_title']} agriculture farming India crop".lower()
            })

    # 2. Index Glossary Terms
    glossary_path = 'content/GLOSSARY.md'
    if os.path.exists(glossary_path):
        with open(glossary_path, 'r', encoding='utf-8') as f:
            content = f.read()

        terms = re.findall(r'###\s+([^\n]+)\n+([^\n#]+)', content)
        for term, defn in terms:
            index_items.append({
                'id': f"GLOSS-{len(index_items)}",
                'type': 'glossary',
                'title': term.strip(),
                'part': 0,
                'part_title': 'Glossary',
                'url': "glossary.html",
                'snippet': defn.strip()[:160] + "...",
                'keywords': f"{term} {defn}".lower()
            })

    # 3. Index Owner Case Study
    index_items.append({
        'id': 'CS-001',
        'type': 'case_study',
        'title': 'Owner Case Study: Ghaziabad Land vs. TCS Employment Decision Analysis',
        'part': 90,
        'part_title': 'Owner Case Study',
        'url': 'case-study.html',
        'snippet': 'Rigorous financial and legal evaluation of corporate IT employment at TCS Bhubaneswar vs family agriculture in Western UP.',
        'keywords': 'tcs ghaziabad owner case study employment salary land revenue sugarcane theka bigha acre'.lower()
    })

    # 4. Index Key Hubs (Subsidies, Taxes, Land, Courses)
    hubs = [
        ('HUB-SUB', 'subsidy', 'Central & State Agricultural Subsidy Register', 'subsidies.html', 'pm-kisan aif midh smam pmksy drip irrigation subsidies tractor farm grants'),
        ('HUB-TAX', 'tax', 'Agricultural Tax Law & Section 10(1) Partial Integration Hub', 'taxation.html', 'income tax section 10(1) partial integration gst capital gains section 54b rule 7 rule 8'),
        ('HUB-LAND', 'land', 'Agricultural Land Affordability & Cadastral Due Diligence Hub', 'land.html', 'land purchase circle rate guideline value up revenue code khatauni khasra non-farmer restrictions'),
        ('HUB-LEARN', 'education', 'Free Agricultural Courses, KVK Training & Fellowship Catalog', 'courses.html', 'free courses degrees diplomas kvk training manage ac&abc icar swayam agmoocs')
    ]
    for hid, htype, htitle, hurl, hkeys in hubs:
        index_items.append({
            'id': hid,
            'type': htype,
            'title': htitle,
            'part': 0,
            'part_title': 'Reference Register',
            'url': hurl,
            'snippet': htitle,
            'keywords': f"{htitle} {hkeys}".lower()
        })

    os.makedirs('site', exist_ok=True)
    out_path = 'site/search_index.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(index_items, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated search index with {len(index_items)} searchable items saved to {out_path}.")

if __name__ == '__main__':
    build_search_index()
