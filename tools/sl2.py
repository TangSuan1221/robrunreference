import json, re, os
WS = r"C:\Users\糖蒜\Desktop\robrun_reference"
data = json.load(open(os.path.join(WS,"out","il2cpp","stringliteral.json"), encoding='utf-8'))
vals = [d['value'] for d in data]
pat = re.compile(r'^(realm|settlement|plot|base|rent|tax|land|district|sector|clan|building|defen|raid|evict|unlock|enter|leave|location|map|prison|laptop|vendor|black|market|cargo|laundr|money|workbench|storage|surviv|health|stamina|hunger|food|water|buff|reputation|tutorial|codex|battlepass|region|switch|population|owned|owner|resident|price|cost|purchase|claim|title|tier|grade|upgrade|move|garage|vehicle|car_|helicopter|door|window|alarm|wanted|police|cop|crime|arrest|imprison|escape|tattoo|party|chat|notification|dialog|hud|inventory)', re.I)
hits = [v for v in vals if pat.match(v)]
print("hits", len(hits))
out = os.path.join(WS,"out","strings_game.txt")
with open(out,'w',encoding='utf-8') as o:
    for v in sorted(set(hits)):
        o.write(v+"\n")
print(out)
# also keys containing 'description' or with dots
keys = [v for v in vals if re.match(r'^[a-z0-9_]+(\.[a-z0-9_]+)+$', v, re.I) and len(v)<80]
print("dotted keys", len(keys))
with open(os.path.join(WS,"out","strings_keys.txt"),'w',encoding='utf-8') as o:
    for v in sorted(set(keys)): o.write(v+"\n")
