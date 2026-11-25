import sys, json, io
import UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"
aa = r"D:\SteamLibrary\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
target = int(sys.argv[1])
env = UnityPy.load(aa + r"\scriptableobjects_assets_all.bundle")
for o in env.objects:
    if o.path_id != target: continue
    print("type:", o.type.name, "path_id:", o.path_id)
    try:
        tt = o.read_typetree()
        print(json.dumps(tt, ensure_ascii=False, indent=2)[:8000])
    except Exception as e:
        print("ERR", e)
