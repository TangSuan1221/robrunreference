"""Load the whole Addressables folder as one environment and resolve external script refs."""
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"

aa = sys.argv[1]
env = UnityPy.load(aa)
print("files:", len(env.files))
names = list(env.files.keys())[:5]
print("first files:", names)

target_bundle = sys.argv[2] if len(sys.argv) > 2 else None
count = 0
ok = 0
for obj in env.objects:
    if obj.type.name != "MonoBehaviour":
        continue
    if target_bundle and target_bundle not in (obj.assets_file.name or ""):
        continue
    count += 1
    try:
        data = obj.read()
        sc = data.m_Script
        if sc is not None:
            s = sc.read()
            cn = getattr(s, "m_ClassName", None)
            if cn:
                ok += 1
                if ok <= 15:
                    print("OK", cn, obj.path_id)
    except Exception as exc:  # noqa: BLE001
        if count <= 3:
            print("FAIL", type(exc).__name__, exc)
    if count >= 400:
        break
print("checked", count, "resolved", ok)
