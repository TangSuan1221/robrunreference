import re, sys
p = r"C:\Users\糖蒜\Desktop\robrun_reference\out\il2cpp\dump.cs"
ns = "?"
rows = []
cur = None
re_ns = re.compile(r'^namespace\s+(.+?)\s*$')
re_type = re.compile(r'^(?:public |internal |private |protected )?(?:sealed |abstract |static |partial |readonly |ref )*(?:class|struct|interface|enum)\s+([A-Za-z0-9_<>,.`\[\] ]+?)\s*(?::.*)?$')
re_comment = re.compile(r'^// Namespace:\s*(.*)$')
with open(p, encoding='utf-8', errors='replace') as f:
    ln = 0
    for line in f:
        ln += 1
        s = line.strip()
        if s.startswith('// Namespace:'):
            ns = s.split(':',1)[1].strip() or "(global)"
            continue
        if s.startswith('// Image'):
            continue
        m = re_type.match(s)
        if m:
            name = m.group(1).strip()
            rows.append((ns, name, ln))
print("classes", len(rows))
# namespace summary
from collections import Counter
c = Counter(n for n,_,_ in rows)
print("namespaces", len(c))
for k,v in c.most_common(40):
    print(f"{v:5d}  {k}")
with open(r"C:\Users\糖蒜\Desktop\robrun_reference\out\class_index.tsv","w",encoding='utf-8') as o:
    for ns,name,ln in rows:
        o.write(f"{ns}\t{name}\t{ln}\n")
