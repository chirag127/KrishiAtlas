import os
import sys
import json
import re
import yaml

def markdown_to_html(md_text):
    # lightweight converter for paragraphs, headings, blockquotes, lists, bold, italics
    # Handle blockquotes
    lines = md_text.splitlines()
    html_lines = []
    in_list = False
    in_quote = False

    for line in lines:
        line_str = line.strip()

        # Headings
        if line_str.startswith('#### '):
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            html_lines.append(f"<h4>{line_str[5:]}</h4>")
        elif line_str.startswith('### '):
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            html_lines.append(f"<h3>{line_str[4:]}</h3>")
        elif line_str.startswith('## '):
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            html_lines.append(f"<h2>{line_str[3:]}</h2>")
        elif line_str.startswith('# '):
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            html_lines.append(f"<h2>{line_str[2:]}</h2>")
        elif line_str.startswith('> '):
            if in_list: html_lines.append('</ul>'); in_list = False
            if not in_quote:
                html_lines.append('<blockquote>')
                in_quote = True
            html_lines.append(f"<p>{line_str[2:]}</p>")
        elif line_str.startswith('- ') or line_str.startswith('* '):
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item_text = line_str[2:]
            # formatting
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code>\1</code>', item_text)
            html_lines.append(f"<li>{item_text}</li>")
        elif line_str == '':
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
        else:
            if in_list: html_lines.append('</ul>'); in_list = False
            if in_quote: html_lines.append('</blockquote>'); in_quote = False
            p_text = line_str
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
            p_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_text)
            p_text = re.sub(r'`(.*?)`', r'<code>\1</code>', p_text)
            p_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', p_text)
            html_lines.append(f"<p>{p_text}</p>")

    if in_list: html_lines.append('</ul>')
    if in_quote: html_lines.append('</blockquote>')

    return '\n'.join(html_lines)

def build_site():
    print("=" * 60)
    print("KrishiAtlas Static Site Builder")
    print("=" * 60)

    articles_dir = 'content/articles'
    os.makedirs('site', exist_ok=True)
    articles_db = {}

    if os.path.exists(articles_dir):
        files = [f for f in os.listdir(articles_dir) if f.endswith('.md')]
        print(f"Compiling {len(files)} articles into site database...")
        for fname in files:
            fpath = os.path.join(articles_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            fm = {}
            body = content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        fm = yaml.safe_load(parts[1]) or {}
                        body = parts[2]
                    except Exception:
                        pass

            art_id = fm.get('id')
            if not art_id:
                m = re.match(r'^(KA-\d{3,4})', fname)
                if m: art_id = m.group(1)

            if art_id:
                articles_db[art_id] = {
                    'id': art_id,
                    'title': fm.get('title', 'Untitled'),
                    'part': fm.get('part', 0),
                    'part_title': fm.get('part_title', ''),
                    'slug': fm.get('slug', ''),
                    'status': fm.get('status', 'draft'),
                    'evidence_grade': fm.get('evidence_grade', 'high'),
                    'last_verified': fm.get('last_verified', '2026-10-18'),
                    'source_ids': fm.get('source_ids', []),
                    'html_body': markdown_to_html(body.strip())
                }

    db_path = 'site/articles_data.json'
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(articles_db, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated {db_path} containing {len(articles_db)} compiled articles.")

if __name__ == '__main__':
    build_site()
