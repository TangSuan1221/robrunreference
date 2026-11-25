import os, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
env = UnityPy.load(p)
n=0
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    try:
        t = obj.read_typetree()
        print(obj.path_id, list(t.keys())[:12])
        print(json.dumps({k:(v if not isinstance(v,(list,dict)) else type(v).__name__) for k,v in t.items()}, ensure_ascii=False)[:400])
        n+=1
        if n>=5: break
    except Exception as e:
        print('ERR', obj.path_id, e)
        n+=1
        if n>=5: break
