import re
from collections import Counter
rows = []
with open(r"C:\Users\糖蒜\Desktop\robrun_reference\out\class_index.tsv", encoding='utf-8') as f:
    for line in f:
        ns,name,ln = line.rstrip("\n").split("\t")
        rows.append((ns,name,int(ln)))
# namespaces containing settlement-related keywords
kw = re.compile(r'Settlement|Realm|Sector|District|Plot|Base|Builder|Raid|Tax|Clan|Trading|Vendor|Shop|Market|Storage|Workbench|Laundr|Cargo|Vehicle|Car|Helicopter|Surviv|Health|Food|Hunger|Disease|Prison|Escape|Hub|City|Map|Location|Land|Rent|Evict|Purchase|Wallet|Economy', re.I)
c = Counter(ns for ns,_,_ in rows)
print("=== namespaces matching keywords ===")
for k,v in sorted(c.items()):
    if kw.search(k):
        print(f"{v:5d}  {k}")
