import os, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"localization-assets-shared_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data(); d = obj.read()
    nm = d.m_Name.encode()
    i = raw.find(nm)
    print(d.m_Name, 'name at', hex(i), 'prefix', raw[i-12:i].hex(' '))
