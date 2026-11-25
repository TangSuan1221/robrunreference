import os, struct, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    d = obj.read()
    if d.m_Name != 'StaticStrings Shared Data': continue
    raw = obj.get_raw_data()
    i = raw.find(b'fast_move')
    print('idx', hex(i))
    print(raw[i-40:i+60].hex(' '))
    j = raw.find(b'death_bribe_description')
    print('idx2', hex(j))
    print(raw[j-40:j+80].hex(' '))
