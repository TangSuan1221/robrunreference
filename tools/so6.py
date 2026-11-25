import os, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p=os.path.join(aa,'scriptableobjects_assets_all.bundle')
env=UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    if obj.path_id!=5791299520934949914: continue
    t=obj.read_typetree()
    ms=t.get('_markers') or []
    print('count', len(ms))
    for m in ms[:90]:
        if isinstance(m,dict):
            print(m.get('id'), '|', {k:v for k,v in m.items() if k!='id' and not isinstance(v,(dict,list))})
