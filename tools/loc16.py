import os, struct, UnityPy, json
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
p = os.path.join(aa,"localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
env = UnityPy.load(p)
loc = {}
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data()
    for spos, s in iter_unity_strings(raw, 0x40):
        if spos >= 8:
            idv = struct.unpack_from('<q', raw, spos-8)[0]
            k = keymap.get(str(idv))
            if k: loc[k] = s
print('localized keys', len(loc))
json.dump(loc, open(os.path.join(ws,'out','loc_en.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=0)
# dump sorted text file for grepping
with open(os.path.join(ws,'out','loc_en.txt'),'w',encoding='utf-8') as f:
    for k in sorted(loc):
        v = loc[k].replace('\n','\\n')
        f.write(f"{k}\t{v}\n")
print('sorted written')
