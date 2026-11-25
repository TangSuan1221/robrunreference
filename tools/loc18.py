import os, re, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
loc = json.load(open(os.path.join(ws,'out','loc_en.json'), encoding='utf-8'))
groups = {
 'realm': r'^(realm|region|switch_realm|realm_names|schedule)',
 'settlement': r'^(settlement|plot|rent|land|district|sector|owned|owner|resident|evict|move_)',
 'tax': r'^(tax|laundr|money_|cash_)',
 'defense': r'^(defen|raid|alarm|breach|lockpick|decoder|module|durability|bunker|building_protection)',
 'base_ui': r'^(building_|base|laptop|vendor|shop_|codex)',
}
for g,pat in groups.items():
    rx = re.compile(pat, re.I)
    sel = {k:v for k,v in loc.items() if rx.match(k)}
    p = os.path.join(ws,'out',f'loc_{g}.txt')
    with open(p,'w',encoding='utf-8') as f:
        for k in sorted(sel): f.write(f"{k} = {sel[k]}\n")
    print(g, len(sel), p)
