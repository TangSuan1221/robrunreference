import os, struct, UnityPy, json, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def unity_str(raw, o):
    ln = struct.unpack_from('<i', raw, o)[0]
    if ln < 0 or ln > 65536 or o+4+ln > len(raw): return None, o
    b = raw[o+4:o+4+ln]
    try: s = b.decode('utf-8')
    except UnicodeDecodeError: return None, o
    return s, (o+4+ln+3)&~3

def looks_text(s):
    if not s: return False
    return all((c=='\t' or c=='\n' or c=='\r' or ord(c)>=32) for c in s)

def scan_pairs(raw, start):
    """Scan for int64 id followed by a text string."""
    res = []
    n = len(raw)
    pos = start
    while pos + 12 <= n:
        ln = struct.unpack_from('<i', raw, pos+8)[0]
        if 0 < ln <= 8192 and pos+12+ln <= n:
            b = raw[pos+12:pos+12+ln]
            ok = True
            try:
                s = b.decode('utf-8')
            except UnicodeDecodeError:
                ok = False; s = None
            if ok and looks_text(s):
                idv = struct.unpack_from('<q', raw, pos)[0]
                res.append((pos, idv, s))
                pos = (pos+12+ln+3)&~3
                continue
        pos += 1
    return res

# 1) key map from SharedTableData: find id+key string pairs
keymap = {}
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data()
    d = obj.read()
    pairs = scan_pairs(raw, 0x40)
    print('shared', d.m_Name, 'pairs', len(pairs), pairs[:2])
    for _, idv, s in pairs:
        if re.match(r'^[A-Za-z0-9_.\-]+$', s) and len(s) < 80:
            keymap[idv] = s
print('keymap', len(keymap))
json.dump({str(k):v for k,v in keymap.items()}, open(os.path.join(ws,'out','loc_keymap.json'),'w',encoding='utf-8'), ensure_ascii=False)
