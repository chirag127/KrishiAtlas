import os
import sys
import json
import hashlib
import re

def test_book():
    print("=" * 60)
    print("KrishiGrantha Master Book Acceptance Test Suite")
    print("=" * 60)

    master_path = 'exports/KrishiGrantha_Master.md'
    manifest_path = 'exports/KrishiGrantha_Manifest.json'

    if not os.path.exists(master_path):
        print(f"[FAIL] Master book not found at {master_path}")
        return False
    if not os.path.exists(manifest_path):
        print(f"[FAIL] Manifest not found at {manifest_path}")
        return False

    with open(master_path, 'r', encoding='utf-8') as f:
        master_content = f.read()

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    errors = []

    # 1. Verify manifest hash matches master file
    actual_hash = hashlib.sha256(master_content.encode('utf-8')).hexdigest()
    if manifest.get('master_md_sha256') != actual_hash:
        errors.append(f"Manifest sha256 mismatch: recorded {manifest.get('master_md_sha256')} vs actual {actual_hash}")
    else:
        print("[PASS] Master markdown SHA-256 matches manifest.")

    # 2. Check for secrets, credentials, or local environment paths
    suspicious_patterns = [
        r'ghp_[A-Za-z0-9_]{30,}',
        r'sk-[A-Za-z0-9]{32,}',
        r'AKIA[0-9A-Z]{16}',
        r'(?i)password\s*[:=]\s*["\'][^"\']+["\']',
        r'c:\\users\\chira\\',
        r'file:///c:'
    ]
    for pat in suspicious_patterns:
        m = re.search(pat, master_content)
        if m:
            errors.append(f"Potential secret or local path detected in master book matching: {pat}")
    if not any('Potential secret' in e for e in errors):
        print("[PASS] Privacy audit on book output passed (zero credentials or machine-local paths).")

    # 3. Verify owner case study is included
    if "Owner Case Study: Strategic Decision Analysis Between Corporate Employment at TCS and Agricultural Enterprise in Ghaziabad" not in master_content and "Owner Decision Analysis" not in master_content:
        errors.append("Owner authorized case study is missing from master book output!")
    else:
        print("[PASS] Expressly authorized owner case study is included in master book.")

    # 4. Check that every published article in manifest appears exactly once in the book
    published_count = 0
    for art in manifest.get('articles', []):
        if art.get('included_in_book'):
            title = art.get('title')
            # Check appearance
            count = master_content.count(f"### {title}")
            if count == 0:
                errors.append(f"Included article '{title}' ({art['id']}) not found under '### {title}' in book!")
            elif count > 1:
                errors.append(f"Duplicate appearance: article '{title}' ({art['id']}) appears {count} times in book!")
            published_count += 1

    print(f"[INFO] Verified {published_count} included articles across all parts.")

    if errors:
        print(f"\n[FAIL] Test suite failed with {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\n[SUCCESS] All KrishiGrantha master book acceptance tests PASSED.")
        return True

if __name__ == '__main__':
    ok = test_book()
    sys.exit(0 if ok else 1)
