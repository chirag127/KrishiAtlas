import json
import os
import re

def slugify(title):
    s = title.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def build_catalog():
    os.makedirs('content', exist_ok=True)
    with open('scripts/inventory.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    parts = data['parts']
    articles = data['articles']

    parts_map = {p['part_num']: {'title': p['part_title'], 'articles': []} for p in parts}
    for a in articles:
        parts_map[a['part']]['articles'].append(a)

    lines = [
        "# KrishiAtlas & KrishiGrantha — Master Article Catalog",
        "",
        "This is the authoritative inventory of all required articles across all 90 parts of the KrishiAtlas and KrishiGrantha agricultural compendium.",
        "",
        f"- **Total Parts:** {len(parts)}",
        f"- **Total Base Articles:** {len(articles)} (KA-001 through KA-1080)",
        "- **Target Editorial Standard:** 1,800–3,200 words for standard articles; 3,000–5,000 words for major technical, legal, state, and enterprise economics articles.",
        "- **Status Legend:** `draft` | `researched` | `reviewed` | `published` | `needs-update`",
        "",
        "---",
        ""
    ]

    for p_num in sorted(parts_map.keys()):
        p_info = parts_map[p_num]
        lines.append(f"## Part {p_num:02d} — {p_info['title']}")
        lines.append("")
        lines.append("| ID | Title | Slug | Target Scope | Initial Status |")
        lines.append("|---|---|---|---|---|")
        for a in p_info['articles']:
            slug = slugify(a['title'])
            lines.append(f"| `{a['id']}` | **{a['title']}** | `{slug}` | Pan-India / Global / Comparative | `draft` |")
        lines.append("")

    with open('content/ARTICLE_CATALOG.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Successfully generated content/ARTICLE_CATALOG.md with {len(articles)} articles across {len(parts)} parts.")

if __name__ == '__main__':
    build_catalog()
