import os, UnityPy, json
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
print(os.path.getsize(p))
env = UnityPy.load(p)
from collections import Counter
c = Counter()
mons = []
for obj in env.objects:
    c[obj.type.name]+=1
    if obj.type.name=='MonoBehaviour':
        try:
            d = obj.read(check_read=False)
            sn = getattr(d,'m_Script',None)
            cn = sn.m_Name if sn else None
        except Exception as e:
            cn = 'ERR'
        mons.append((cn, obj.path_id))
print(c)
cc = Counter(x[0] for x in mons)
print(len(cc))
for k,v in cc.most_common(60): print(v,k)
