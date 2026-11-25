import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
env = UnityPy.load(os.path.join(aa, 'scriptableobjects_assets_all.bundle'))
TARGET = 1168351570948069171
for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    pid = obj.path_id
    if pid >= (1 << 63):
        pid -= (1 << 64)
    if pid != TARGET:
        continue
    t = obj.read_typetree()
    print(json.dumps(t, ensure_ascii=False)[:3000])
