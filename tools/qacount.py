import re, os
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = os.path.join(ws,'docs_reverse','qa','全系统边界用例矩阵.md')
txt = open(p, encoding='utf-8').read()
ids = re.findall(r'^\| (S\d\d-\d\d) \|', txt, re.M)
print('case rows', len(ids), 'unique', len(set(ids)))
# per system
from collections import Counter
c = Counter(i.split('-')[0] for i in ids)
print(dict(sorted(c.items())))
