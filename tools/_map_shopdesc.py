import json, os
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
km = json.load(open(os.path.join(ws, 'out', 'loc_keymap.json'), encoding='utf-8'))
en = json.load(open(os.path.join(ws, 'out', 'loc_en.json'), encoding='utf-8'))
d = json.load(open(os.path.join(ws, 'out', 'shop_viewdesc.json'), encoding='utf-8'))
for e in d['entries']:
    hk = e.get('<Header>k__BackingField')
    dk = e.get('<Description>k__BackingField')
    k1 = km.get(str(hk))
    k2 = km.get(str(dk))
    print('%-34s header=%-28s | %s' % (e['id'], k1, (en.get(k1) or '')[:60]))
    print('%-34s desc  =%-28s | %s' % ('', k2, (en.get(k2) or '')[:80]))
