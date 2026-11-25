import re
from collections import Counter
rows = []
with open(r"C:\Users\糖蒜\Desktop\robrun_reference\out\class_index.tsv", encoding='utf-8') as f:
    for line in f:
        ns,name,ln = line.rstrip("\n").split("\t")
        rows.append((ns,name,int(ln)))
print("=== all namespaces (by count desc) ===")
c = Counter(ns for ns,_,_ in rows)
for k,v in c.most_common():
    print(f"{v:5d}  {k}")
