import os
import sys
import re
import hashlib
import json

def get_paragraphs(text):
    # split into non-empty paragraphs
    paras = text.split('\n\n')
    cleaned = []
    for p in paras:
        p_clean = re.sub(r'#+\s*', '', p).strip()
        # ignore short paragraphs / headings / frontmatter
        if len(p_clean) > 80:
            cleaned.append(p_clean)
    return cleaned

def check_duplicates():
    print("=" * 60)
    print("KrishiAtlas Duplicate & Semantic Redundancy Checker")
    print("=" * 60)

    articles_dir = 'content/articles'
    if not os.path.exists(articles_dir):
        print("No articles directory found.")
        return True

    files = [os.path.join(articles_dir, f) for f in os.listdir(articles_dir) if f.endswith('.md')]
    print(f"Auditing {len(files)} files for duplicate content...")

    seen_hashes = {}
    duplicates_found = []

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # strip frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]

        paras = get_paragraphs(content)
        for idx, p in enumerate(paras):
            # Normalize whitespace and lower
            norm = re.sub(r'\s+', ' ', p.lower()).strip()
            # Hash paragraph
            p_hash = hashlib.sha256(norm.encode('utf-8')).hexdigest()
            if p_hash in seen_hashes:
                orig_file, orig_idx = seen_hashes[p_hash]
                duplicates_found.append({
                    'original': f"{orig_file} (p.{orig_idx})",
                    'duplicate': f"{filepath} (p.{idx})",
                    'snippet': p[:100] + '...'
                })
            else:
                seen_hashes[p_hash] = (filepath, idx)

    if duplicates_found:
        print(f"\n[!] Detected {len(duplicates_found)} duplicate paragraphs:")
        for d in duplicates_found[:10]:
            print(f"  Duplicate between {d['original']} and {d['duplicate']}")
            print(f"    Snippet: \"{d['snippet']}\"")
        return False
    else:
        print("[OK] Zero exact duplicate paragraphs found across all articles.")
        return True

if __name__ == '__main__':
    ok = check_duplicates()
    sys.exit(0 if ok else 1)
