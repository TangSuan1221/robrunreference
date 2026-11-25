import os, re, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
loc = json.load(open(os.path.join(ws,'out','loc_en.json'), encoding='utf-8'))
pat = re.compile(r'^(realm|settlement|plot|rent|tax|land|district|sector|building|defen|raid|evict|unlock|enter_|leave_|owned|owner|resident|price|purchase|move_|garage|vehicle|door_|window|alarm|laundr|workbench|storage|shelv|cargo|crypto|money|cash|prison|wanted|police|cop_|crime|arrest|imprison|escape|tattoo|clan_|party_|region|switch_realm|realm_|base_|bunker|checkpoint|lab_|farm_|power_|black_market|trading|shop_|vendor|market|laptop|codex|tutorial|schedule|burning|conquest|flag|silence|decoder|module|durability|breach|lockpick|season|battlepass|grade|tier)', re.I)
sel = {k:v for k,v in loc.items() if pat.match(k)}
print('selected', len(sel))
with open(os.path.join(ws,'out','loc_settlement.txt'),'w',encoding='utf-8') as f:
    for k in sorted(sel):
        f.write(f"{k} = {sel[k]}\n")
# counts by prefix
from collections import Counter
c = Counter(k.split('_')[0] for k in sel)
print(c.most_common(40))
