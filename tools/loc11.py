import os, struct, UnityPy, json, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def unity_str(raw, o):
    ln = struct.unpack_from('<i', raw, o)[0]
    if ln < 0 or ln > 65536 or o+4+ln > len(raw): return None, o
    try: s = raw[o+4:o+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None, o
    return s, (o+4+ln+3)&~3

def parse_shared(raw):
    """Returns (table_name, guid_str, [(id,key)]) walking the SharedTableData layout."""
    o = 0x10  # after object header (12) + name pointer? we start content at 0x10 to be safe
    # find table name: first string after 0x40
    o = 0x3C
    tname, o = unity_str(raw, o)
    guid, o = unity_str(raw, o)
    # metadata collection: GUID 16? detect: try int count first
    # heuristics: if 4 bytes are small (0..5) treat as count
    cnt = struct.unpack_from('<i', raw, o)[0]
    if 0 <= cnt < 64:
        o += 4 + cnt*20
    else:
        o += 16
        cnt2 = struct.unpack_from('<i', raw, o)[0]
        if 0 <= cnt2 < 64: o += 4 + cnt2*20
    entries = []
    # now o should be at the int32 count of m_Entries
    ecnt = struct.unpack_from('<i', raw, o)[0]
    o += 4
    for i in range(ecnt):
        idv = struct.unpack_from('<q', raw, o)[0]; o += 8
        k, o = unity_str(raw, o)
        if k is None: break
        # metadata: detect zeros
        if raw[o:o+20] == b'\x00'*20:
            o += 20
        else:
            o += 4 + 0  # count only? 
        entries.append((idv,k))
    return tname, guid, entries

keymap={}
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data(); d = obj.read()
    tname, guid, ents = parse_shared(raw)
    print(d.m_Name, '| table', tname, '| guid', guid, '| entries', len(ents), ents[:3])
    for idv,k in ents: keymap[idv]=k
print('total keys', len(keymap))
json.dump({str(k):v for k,v in keymap.items()}, open(os.path.join(ws,'out','loc_keymap.json'),'w',encoding='utf-8'), ensure_ascii=False)
