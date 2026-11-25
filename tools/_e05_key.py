import json, sys, os
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
km = json.load(open(os.path.join(ws, 'out', 'loc_keymap.json'), encoding='utf-8'))
loc = json.load(open(os.path.join(ws, 'out', 'loc_en.json'), encoding='utf-8'))
ids = sys.argv[1:] if len(sys.argv) > 1 else []
if not ids:
    ids = sys.stdin.read().split()
for i in ids:
    k = km.get(str(i))
    if k is None:
        print(i, '-> [NO KEY]')
        continue
    v = loc.get(k)
    print(i, '->', k, '=>', (v if v is not None else '[NO TEXT]'))
