import os, struct, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data(); d = obj.read()
    i = raw.find(b'Failed to load game data')
    print(d.m_Name, 'text at', hex(i), 'before:', raw[i-16:i].hex(' '))
    j = raw.find(b'Imprison')
    print('  imprison at', hex(j), 'before:', raw[j-16:j].hex(' '))
