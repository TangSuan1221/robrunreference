import os, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = os.path.join(ws,'out','il2cpp','dump.cs')
types=0; methods=0; fields=0
re_rva = re.compile(r'^\s*// RVA:')
for line in open(p, encoding='utf-8', errors='replace'):
    s=line.strip()
    if s.startswith('public ') or s.startswith('internal ') or s.startswith('private ') or s.startswith('protected '):
        if re.search(r'\b(class|struct|interface|enum)\s+\w', s) and s.endswith('TypeDefIndex') or 'TypeDefIndex:' in s:
            types+=1
    if re_rva.match(line): methods+=1
print('types', types, 'methods', methods)
