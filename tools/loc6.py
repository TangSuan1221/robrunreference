import os, struct, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def read_obj_header(raw):
    off = 12
    ln = struct.unpack_from('<i', raw, off)[0]; name = raw[off+4:off+4+ln].decode('utf-8','replace'); off += 4+ln
    off = (off+3)&~3
    off += 8
    return off, name

def scan_pairs(raw, start):
    """Scan for sequences of int64 id followed by Unity string."""
    pairs = []
    n = len(raw)
    pos = start
    while pos + 12 <= n:
        idv = struct.unpack_from('<q', raw, pos)[0]
        ln = struct.unpack_from('<i', raw, pos+8)[0]
        if 0 < ln < 4096 and pos+12+ln <= n:
            s = raw[pos+12:pos+12+ln]
            try:
                txt = s.decode('utf-8')
                if all(c=='\t' or c=='\n' or c=='\r' or ord(c)>=32 for c in txt) and idv != 0:
                    pairs.append((idv, txt, pos))
                    pos = (pos+12+ln+3)&~3
                    continue
            except UnicodeDecodeError:
                pass
        pos += 1
    return pairs

out = {}
for name in ["localization-assets-shared_assets_all.bundle"]:
    pass
# shared table data: id -> key
keymap = {}
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data()
    off, nm = read_obj_header(raw)
    # SharedTableData fields: m_TableCollectionName string, m_TableCollectionNameGuidString string, m_Entries list
    # parse strings sequentially
    def rd_str(o):
        ln = struct.unpack_from('<i', raw, o)[0]; s = raw[o+4:o+4+ln].decode('utf-8','replace'); return s, (o+4+ln+3)&~3
    cur = off + 8  # skip script? no, off already after script
    tname, cur = rd_str(cur)
    guid, cur = rd_str(cur)
    cnt = struct.unpack_from('<i', raw, cur)[0]; cur += 4
    entries = []
    for i in range(cnt):
        eid = struct.unpack_from('<q', raw, cur)[0]; cur += 8
        k, cur = rd_str(cur)
        # metadata: guid string + count
        g, cur = rd_str(cur)
        mc = struct.unpack_from('<i', raw, cur)[0]; cur += 4
        # skip metadata entries (assume empty)
        entries.append((eid,k))
    print(nm, tname, cnt, entries[:3])
    for eid,k in entries: keymap[eid]=k
print('keymap size', len(keymap))
json.dump({str(k):v for k,v in keymap.items()}, open(os.path.join(ws,'out','loc_keymap.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=0)
