import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
env = UnityPy.load(os.path.join(aa, 'scriptableobjects_assets_all.bundle'))
TARGET = 275343534651159011
km = json.load(open(os.path.join(ws, 'out', 'loc_keymap.json'), encoding='utf-8'))
en = json.load(open(os.path.join(ws, 'out', 'loc_en.json'), encoding='utf-8'))
rows = []

def walk(node, path):
    if not isinstance(node, dict):
        return
    tr = node.get('m_TableEntryReference') or (node.get('_localizedString') or {}).get('m_TableEntryReference')
    if tr:
        rows.append((path, tr.get('m_KeyId')))
        return
    for k, v in node.items():
        if k.startswith('m_') and k != 'm_Name':
            continue
        walk(v, path + '/' + k)

for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    pid = obj.path_id
    if pid >= (1 << 63):
        pid -= (1 << 64)
    if pid != TARGET:
        continue
    t = obj.read_typetree()
    for k, v in t.items():
        if k.startswith('m_') or k == 'references':
            continue
        walk(v, k)

out = []
for path, kid in rows:
    key = km.get(str(kid))
    out.append({'field': path, 'keyId': kid, 'key': key, 'text': en.get(key) if key else None})
json.dump(out, open(os.path.join(ws, 'out', 'loc_skincenter.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('total', len(out))
for r in out:
    k = r['key'] or ''
    if any(w in k for w in ('shop', 'pack', 'price', 'discount', 'purchase', 'offer', 'expired', 'timer', 'buy', 'crypto')):
        print('%-64s %-44s %s' % (r['field'].split('/')[-1], k, (r['text'] or '')[:80]))
