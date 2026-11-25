import os,UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION="6000.3.18f1"
b=r"D:\SteamLibrary\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64\localization-locales_assets_all.bundle"
env=UnityPy.load(b)
for o in env.objects:
    print("OBJ", o.type.name, getattr(o,"path_id",""))
    if o.type.name in ("MonoBehaviour","ScriptableObject"):
        try:
            t=o.read_typetree()
            for k,v in t.items():
                if k.startswith("m_"): continue
                print("   ",k,"=",(str(v)[:200]))
        except Exception as e:
            print("    read fail",e)
