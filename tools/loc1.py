import os, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa, "localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
print(os.path.exists(p), os.path.getsize(p))
env = UnityPy.load(p)
cnt = {}
objs = []
for obj in env.objects:
    cnt[obj.type.name] = cnt.get(obj.type.name,0)+1
    objs.append(obj)
print(cnt)
for obj in objs:
    if obj.type.name in ('MonoBehaviour','TextAsset'):
        try:
            d = obj.read()
        except Exception as e:
            print('read err', obj.type.name, e); continue
        print('---', obj.type.name, 'path_id', obj.path_id, 'name', getattr(d,'m_Name','?'))
        if obj.type.name=='TextAsset':
            data = d.m_Script if isinstance(d.m_Script, bytes) else d.m_Script.encode('utf-8','surrogateescape')
            print('  size', len(data))
