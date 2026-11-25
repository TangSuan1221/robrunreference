import os, UnityPy
from collections import Counter
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
env = UnityPy.load(p)
print(type(env.files))
for k,v in env.files.items():
    print(k, type(v).__name__)
    break
# try iterate container
b = list(env.files.values())[0]
print(dir(b)[:40])
