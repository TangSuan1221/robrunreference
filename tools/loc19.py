import os, re, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
loc = json.load(open(os.path.join(ws,'out','loc_en.json'), encoding='utf-8'))
# keys used by realm entry / settlement enter / plot / unlock
pats = [
 r'^(realm_|region_|switch_realm|schedule_)',
 r'^(settlement_|plot_|rent_|land_|owner_)',
 r'^(tax_|taxes_|laundr)',
 r'^(vendor_|laptop|black_market|market_)',
 r'^(tutorial_(plot|main_building|leave_settlement|clean_cache|become_robber|set_car|take_clean))',
 r'^(world_map|map_)',
 r'^(global_notification_plot|location_chat_plot|deferred_alarm)',
 r'^(hints_)',
 r'^(building_|bunker|gate_|checkpoint)',
 r'^(mission_|quest_|objective_)',
]
rx = re.compile('|'.join('(?:'+p+')' for p in pats), re.I)
sel = {k:v for k,v in loc.items() if rx.match(k)}
print(len(sel))
with open(os.path.join(ws,'out','loc_core.txt'),'w',encoding='utf-8') as f:
    for k in sorted(sel): f.write(f"{k} = {sel[k]}\n")
