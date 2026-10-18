import os
import sys
import re

def check_links():
    print("=" * 60)
    print("KrishiAtlas Internal Links & Source Reference Checker")
    print("=" * 60)

    # 1. Load valid source IDs from SOURCE_REGISTRY.md
    source_reg_path = 'content/SOURCE_REGISTRY.md'
    valid_source_ids = set()
    if os.path.exists(source_reg_path):
        with open(source_reg_path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.findall(r'`(SRC-\d{4})`', line)
                valid_source_ids.update(m)
    print(f"Loaded {len(valid_source_ids)} verified source IDs from registry.")

    # 2. Check articles
    articles_dir = 'content/articles'
    files = [os.path.join(articles_dir, f) for f in os.listdir(articles_dir) if f.endswith('.md')] if os.path.exists(articles_dir) else []

    errors = []
    warnings = []

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check source_ids cited in frontmatter
        cited_sources = re.findall(r'source_ids:\s*\[(.*?)\]', content)
        if cited_sources:
            src_list = [s.strip(' "\'').strip() for s in cited_sources[0].split(',') if s.strip()]
            for s in src_list:
                if s and s not in valid_source_ids:
                    warnings.append(f"{fpath}: Cited source '{s}' not found in SOURCE_REGISTRY.md")

        # Check markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in links:
            if url.startswith(('http://', 'https://')):
                # External link syntax check
                if not re.match(r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', url):
                    warnings.append(f"{fpath}: Potentially malformed external URL: {url}")
            elif url.startswith('#'):
                # Anchor link
                pass
            else:
                # Internal link
                target_path = os.path.normpath(os.path.join(os.path.dirname(fpath), url))
                if not os.path.exists(target_path):
                    errors.append(f"{fpath}: Broken internal link to '{url}' (resolved to {target_path})")

    if warnings:
        print(f"\n[!] Link warnings ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  - {w}")

    if errors:
        print(f"\n[FAIL] Found {len(errors)} broken links:")
        for e in errors[:10]:
            print(f"  - {e}")
        return False
    else:
        print("[PASS] Zero broken internal links found.")
        return True

if __name__ == '__main__':
    ok = check_links()
    sys.exit(0 if ok else 1)
