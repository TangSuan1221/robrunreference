import os, struct, UnityPy, json, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def iter_unity_strings(raw, start=0):
    n=len(raw); pos=start
    while pos+4<=n:
        ln = struct.unpack_from('<i', raw, pos)[0]
        if 0 < ln <= 65536 and pos+4+ln <= n:
            b = raw[pos+4:pos+4+ln]
            try: s = b.decode('utf-8')
            except UnicodeDecodeError: s=None
            if s is not None and all(c in '\t\n\r' or ord(c)>=32 for c in s):
                yield pos, s
                pos = (pos+4+ln+3)&~3
                continue
        pos+=1

keymap = json.load(open(os.path.join(ws,'out','loc_keymap.json'), encoding='utf-8'))
print('keys', len(keymap), list(keymap.items())[:3])
p = os.path.join(aa,"localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data(); d = obj.read()
    tabs = {}
    for spos, s in iter_unity_strings(raw, 0x40):
        if spos >= 8:
            idv = struct.unpack_from('<q', raw, spos-8)[0]
            if idv != 0:
                tabs[idv] = s
    print(d.m_Name, 'entries', len(tabs))
    hit = [k for k in list(tabs)[:5]]
    print(' sample', [(k, tabs[k][:40]) for k in hit])
    # match to keymap
    matched = sum(1 for k in tabs if str(k) in keymap)
    print(' matched ids', matched)
