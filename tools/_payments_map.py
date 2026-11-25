import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
env = UnityPy.load(os.path.join(aa, 'scriptableobjects_assets_all.bundle'))
TARGET = 2859703315750441957
km = json.load(open(os.path.join(ws,'out','loc_keymap.json'), encoding='utf-8'))
en = json.load(open(os.path.join(ws,'out','loc_en.json'), encoding='utf-8'))
def walk(n, p, rows):
    if not isinstance(n, dict): return
    tr = n.get('m_TableEntryReference') or (n.get('_localizedString') or {}).get('m_TableEntryReference')
    if tr:
        rows.append((p, tr.get('m_KeyId'))); return
    for k, v in n.items():
        if k.startswith('m_') and k != 'm_Name': continue
        walk(v, p + '/' + k, rows)
for obj in env.objects:
    if obj.type.name != 'MonoBehaviour': continue
    pid = obj.path_id
    if pid >= (1 << 63): pid -= (1 << 64)
    if pid != TARGET: continue
    t = obj.read_typetree(); rows = []
    for k, v in t.items():
        if k.startswith('m_') or k == 'references': continue
        walk(v, k, rows)
    for p, kid in rows:
        key = km.get(str(kid))
        print('%-40s %-40s %s' % (p, key, (en.get(key) or '')[:60]))
