import os, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
env = UnityPy.load(p)
b = list(env.files.values())[0]
print('inner files:', list(b.files.keys())[:10])
for name, sf in b.files.items():
    print(' SF', name, type(sf).__name__, 'externals', getattr(sf,'externals',None))
    print(' types', [t.__name__ if hasattr(t,'__name__') else t for t in getattr(sf,'types',[])[:5]])
    objs = getattr(sf,'objects',{})
    print(' objs', len(objs))
    break
