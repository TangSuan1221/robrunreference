import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
env = UnityPy.load(os.path.join(aa, 'scriptableobjects_assets_all.bundle'))
TARGETS = {
    5244587876244765392: 'SkinCenterShopPacksViewDescriptions',
    3160280219446727305: 'SkinCenterCryptoCoinsViewDescriptions',
    -3649879233042651237: 'CryptoCoinsPackViewDescriptions',
    -3099635110258796736: 'ModalDialogLocalization',
}
km = json.load(open(os.path.join(ws, 'out', 'loc_keymap.json'), encoding='utf-8'))
en = json.load(open(os.path.join(ws, 'out', 'loc_en.json'), encoding='utf-8'))

def walk(node, path, rows):
    if not isinstance(node, dict):
        return
    tr = node.get('m_TableEntryReference') or (node.get('_localizedString') or {}).get('m_TableEntryReference')
    if tr:
        rows.append((path, tr.get('m_KeyId')))
        return
    for k, v in node.items():
        if k.startswith('m_') and k != 'm_Name':
            continue
        walk(v, path + '/' + k, rows)

for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    pid = obj.path_id
    if pid >= (1 << 63):
        pid -= (1 << 64)
    if pid not in TARGETS:
        continue
    t = obj.read_typetree()
    rows = []
    for k, v in t.items():
        if k.startswith('m_') or k == 'references':
            continue
        walk(v, k, rows)
    print('=====', TARGETS[pid], len(rows))
    for path, kid in rows:
        key = km.get(str(kid))
        if not key:
            continue
        if any(w in key for w in ('shop', 'pack', 'price', 'discount', 'purchase', 'offer', 'expired', 'timer', 'buy', 'crypto', 'modal')):
            print('  %-58s %-44s %s' % (path.split('/')[-1], key, (en.get(key) or '')[:90]))
