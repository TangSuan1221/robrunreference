import os, json, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,'scriptableobjects_assets_all.bundle')
env = UnityPy.load(p)
want = {7245226053162067993, -3955775674806922645, 7586590884206883568}
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    if obj.path_id not in want: continue
    t = obj.read_typetree()
    print('=====', t.get('m_Name'))
    print(json.dumps(t, ensure_ascii=False, indent=1)[:4000])
