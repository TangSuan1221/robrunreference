import os, struct, UnityPy, json, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def looks_text(s):
    if not s: return False
    return all((c=='\t' or c=='\n' or c=='\r' or ord(c)>=32) for c in s)

def scan_strings(raw, start):
    """yield (str_start, string) for every Unity string found scanning byte by byte."""
    n = len(raw); pos = start
    while pos + 4 <= n:
        ln = struct.unpack_from('<i', raw, pos)[0]
        if 0 < ln <= 8192 and pos+4+ln <= n:
            b = raw[pos+4:pos+4+ln]
            try: s = b.decode('utf-8')
            except UnicodeDecodeError: s = None
            if s is not None and looks_text(s):
                yield pos, s
                pos += 4+ln
                pos = (pos+3)&~3
                continue
        pos += 1

def keys_from_shared(raw):
    """SharedTableData: iterate entries: int64 id, string key, metadata(GUID16 + count + items)."""
    out = []
    # locate entry list: after 'm_TableCollectionName' string and guid string.
    # simplest: find the first id whose following string matches a key-like pattern and the 8 bytes after string are zeroed metadata guid start
    pos = 0x60
    n = len(raw)
    while pos + 12 <= n:
        idv = struct.unpack_from('<q', raw, pos)[0]
        ln = struct.unpack_from('<i', raw, pos+8)[0]
        if 0 < ln <= 200 and pos+12+ln <= n:
            try: key = raw[pos+12:pos+12+ln].decode('ascii')
            except UnicodeDecodeError: key = None
            if key and re.match(r'^[A-Za-z0-9_.\-]+$', key):
                out.append((idv, key))
                # advance: skip key string, then metadata
                q = (pos+12+ln+3)&~3
                # metadata: 16-byte guid? then int count; most are empty (guid zeros, count 0) = 20 bytes
                # detect: if next 20 bytes are all zero -> skip 20
                if raw[q:q+20] == b'\x00'*20:
                    pos = q + 20
                else:
                    # try skipping 8 (guid low) + 4 count
                    pos = q + 12
                continue
        pos += 1
    return out

keymap = {}
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data()
    d = obj.read()
    ks = keys_from_shared(raw)
    print(d.m_Name, 'keys', len(ks), ks[:3])
    for idv,k in ks: keymap[idv]=k
print('keymap total', len(keymap))
json.dump({str(k):v for k,v in keymap.items()}, open(os.path.join(ws,'out','loc_keymap.json'),'w',encoding='utf-8'), ensure_ascii=False)
