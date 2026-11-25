import sys
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"
aa = sys.argv[1]
env = UnityPy.load(aa)
print("files:", len(env.files))
seen = {}
for obj in env.objects:
    af = obj.assets_file
    key = (getattr(af, "name", None), getattr(af, "path", None))
    if key not in seen:
        seen[key] = 0
    seen[key] += 1
for k, v in list(seen.items())[:12]:
    print(v, k)
print("distinct files:", len(seen))
