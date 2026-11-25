import os
import sys
import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"
env = UnityPy.load(sys.argv[1])
for path, sf in list(env.files.items()):
    b = os.path.basename(path)
    if "settlement" in b.lower():
        print(repr(path), "->", repr(getattr(sf, "name", None)), type(sf).__name__)
