import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('KrishiAtlas_KrishiGrantha_Enhanced_Master_Prompt.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1785, len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
