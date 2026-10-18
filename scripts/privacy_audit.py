import os
import sys
import re

SUSPICIOUS_PATTERNS = [
    (r'(?i)ghp_[A-Za-z0-9_]{30,}', 'GitHub Personal Access Token'),
    (r'(?i)sk-[A-Za-z0-9]{32,}', 'OpenAI / Generic Secret Key'),
    (r'(?i)AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'(?i)BEGIN\s+(RSA|OPENSSH|DSA|EC)\s+PRIVATE\s+KEY', 'Private SSH Key'),
    (r'(?i)password\s*[:=]\s*["\'][^"\']{4,}["\']', 'Hardcoded Password'),
    (r'(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*', 'Authorization Bearer Token'),
    (r'c:[\\/]users[\\/][a-zA-Z0-9_-]+[\\/]', 'Machine-local Windows User Directory Path')
]

# Excluded paths from audit (e.g. git internal, binary files)
EXCLUDE_DIRS = {'.git', 'node_modules', '.astro', 'dist', '__pycache__'}

def run_privacy_audit():
    print("=" * 60)
    print("KrishiAtlas Privacy, Credentials & Security Auditor")
    print("=" * 60)

    found_violations = []

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            # Audit text and code files
            if f.endswith(('.md', '.json', '.js', '.ts', '.astro', '.html', '.css', '.py', '.txt')):
                fpath = os.path.join(root, f)
                # Skip the audit script itself
                if os.path.abspath(fpath) == os.path.abspath(__file__):
                    continue

                with open(fpath, 'r', encoding='utf-8', errors='ignore') as handle:
                    content = handle.read()

                for pat, label in SUSPICIOUS_PATTERNS:
                    matches = re.finditer(pat, content)
                    for m in matches:
                        line_num = content[:m.start()].count('\n') + 1
                        found_violations.append({
                            'file': fpath,
                            'line': line_num,
                            'type': label,
                            'snippet': m.group(0)[:40]
                        })

    # Verify that the authorized owner case study is present
    case_study_file = os.path.join('content', 'case-studies', 'owner-agriculture-vs-tcs.md')
    if not os.path.exists(case_study_file):
        found_violations.append({
            'file': case_study_file,
            'line': 0,
            'type': 'Missing Authorized Case Study',
            'snippet': 'The owner expressly authorized the case study; it must be preserved.'
        })
    else:
        print("[PASS] Authorized owner case study file confirmed present.")

    if found_violations:
        print(f"\n[FAIL] Found {len(found_violations)} potential privacy/secret violations:")
        for v in found_violations:
            print(f"  - [{v['type']}] in {v['file']}:{v['line']} -> {v['snippet']}")
        return False
    else:
        print("[PASS] Zero credentials, secrets, or machine-local user paths detected across repository.")
        return True

if __name__ == '__main__':
    ok = run_privacy_audit()
    sys.exit(0 if ok else 1)
