"""Extract MonoScript path_id -> m_ClassName map (plus assembly) from the monoscripts bundle."""
import json
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"

bundle = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "out/scripts.json"
env = UnityPy.load(bundle)
m = {}
print("top files:", [(type(v).__name__, k.split('/')[-1]) for k, v in list(env.files.items())[:5]])
files = []
for path, sf in env.files.items():
    if hasattr(sf, "objects"):
        files.append(sf)
    elif hasattr(sf, "files"):
        for inner_path, inner in sf.files.items():
            if hasattr(inner, "objects"):
                files.append(inner)
print("serialized files:", len(files))
for sf in files:
    for obj in sf.objects.values():
        if obj.type.name != "MonoScript":
            continue
        try:
            s = obj.read()
        except Exception:  # noqa: BLE001
            continue
        cn = getattr(s, "m_ClassName", None)
        ns = getattr(s, "m_Namespace", None)
        asm = getattr(s, "m_AssemblyName", None)
        m[str(obj.path_id)] = {"class": cn, "ns": ns, "asm": asm}
json.dump(m, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("scripts:", len(m), "->", out)
sample = list(m.items())[:5]
for k, v in sample:
    print(k, v)
