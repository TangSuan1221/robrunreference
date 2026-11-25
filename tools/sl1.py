import json, re, os
WS = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = os.path.join(WS,"out","il2cpp","stringliteral.json")
data = json.load(open(p, encoding='utf-8'))
print(type(data), len(data))
print(json.dumps(data[:5], ensure_ascii=False, indent=1)[:800])
