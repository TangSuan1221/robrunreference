import os, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    t = obj.read_typetree()
    print(t.get('m_Script'))
    print(t.get('m_GameObject'))
    break
