import os, re, json
from collections import Counter
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
out = os.path.join(ws,'out','mb_index.jsonl')
n=0; agg=Counter(); names=Counter(); errs=0
for line in open(out,encoding='utf-8'):
    try: r=json.loads(line)
    except: continue
    n+=1
    if 'error' in r: errs+=1; continue
    for k,v in r.get('types',{}).items(): agg[k]+=v
print('bundles',n,'errors',errs,'types',len(agg))
for k,v in agg.most_common(80): print(v,k)
