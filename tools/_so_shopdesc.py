import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy

ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa, 'scriptableobjects_assets_all.bundle')
env = UnityPy.load(p)
TARGET = 5244587876244765392

out = {}
for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    pid = obj.path_id
    if pid >= (1 << 63):
        pid -= (1 << 64)
    if pid != TARGET:
        continue
    t = obj.read_typetree()
    out['name'] = t.get('m_Name')
    for k, v in t.items():
        if k.startswith('m_') or k == 'references':
            continue
        if isinstance(v, (int, float, bool, str)):
            out[k] = v
    lst = t.get('<List>k__BackingField') or []
    entries = []
    for e in lst:
        d = {'id': e['<Identified>k__BackingField']['_id']}
        for fld in ('<Header>k__BackingField', '<Description>k__BackingField'):
            ref = e.get(fld)
            if ref:
                d[fld] = ref.get('m_TableEntryReference', {}).get('m_KeyId')
        g = e.get('<Gradient>k__BackingField')
        if g:
            d['grad'] = (round(g['<LeftColor>k__BackingField']['r'], 3), round(g['<LeftColor>k__BackingField']['g'], 3), round(g['<LeftColor>k__BackingField']['b'], 3))
        d['bg'] = e.get('_backgroundSprite', {}).get('m_SubObjectName')
        d['item'] = e.get('_itemSprite', {}).get('m_SubObjectName')
        entries.append(d)
    out['entries'] = entries

json.dump(out, open(os.path.join(ws, 'out', 'shop_viewdesc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'entries'}, ensure_ascii=False, indent=1))
print('entries:', len(out.get('entries', [])))
for e in out.get('entries', []):
    print(e['id'], e.get('<Header>k__BackingField'), e.get('<Description>k__BackingField'), e.get('bg'), e.get('item'))
