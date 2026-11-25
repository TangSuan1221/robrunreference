import os, struct, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa, "localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name != 'MonoBehaviour': continue
    raw = obj.get_raw_data()
    print('===', obj.path_id, 'len', len(raw))
    print(raw[:96].hex(' '))
    # readable ascii in first 200 bytes
    print(repr(raw[:200]))
