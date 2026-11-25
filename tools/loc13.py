import os, struct, UnityPy, json, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"

def iter_unity_strings(raw, start=0):
    n=len(raw); pos=start
    while pos+4<=n:
        ln = struct.unpack_from('<i', raw, pos)[0]
        if 0 < ln <= 8192 and pos+4+ln <= n:
            b = raw[pos+4:pos+4+ln]
            try: s = b.decode('utf-8')
            except UnicodeDecodeError: s=None
            if s is not None and all(c in '\t\n\r' or ord(c)>=32 for c in s):
                yield pos, s
                pos = (pos+4+ln+3)&~3
                continue
        pos+=1

keymap={}
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data(); d = obj.read()
    ents=[]
    for spos, s in iter_unity_strings(raw, 0x40):
        if re.match(r'^[a-z][a-z0-9_.\-]{1,80}$', s) or re.match(r'^[a-z][a-z0-9_]*_[a-z0-9_]*$', s):
            # candidate id at spos-8
            if spos>=8:
                idv = struct.unpack_from('<q', raw, spos-8)[0]
                if idv != 0:
                    ents.append((idv, s))
    print(d.m_Name, 'candidates', len(ents), ents[:3])
    for idv,k in ents: keymap[idv]=k
print('total keys', len(keymap))
json.dump({str(k):v for k,v in keymap.items()}, open(os.path.join(ws,'out','loc_keymap.json'),'w',encoding='utf-8'), ensure_ascii=False)
