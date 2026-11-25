"""Per-bundle MonoBehaviour index using a global MonoScript path_id -> class map."""
import argparse
import glob
import json
import os
import re
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"


def iter_serialized(env):
    for path, sf in env.files.items():
        if hasattr(sf, "objects"):
            yield path, sf
        elif hasattr(sf, "files"):
            for _inner_path, inner in sf.files.items():
                if hasattr(inner, "objects"):
                    yield path, inner


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern")
    ap.add_argument("--script-map", default="out/scripts.json")
    ap.add_argument("--match", default=None)
    ap.add_argument("--out-index", default="out/mb_all.jsonl")
    ap.add_argument("--out-dir", default="out/mb_dump")
    ap.add_argument("--limit-bundles", type=int, default=0)
    args = ap.parse_args()

    smap = json.load(open(args.script_map, encoding="utf-8"))
    files = sorted(glob.glob(args.pattern))
    if args.limit_bundles:
        files = files[: args.limit_bundles]
    matcher = re.compile(args.match) if args.match else None
    os.makedirs(os.path.dirname(args.out_index) or ".", exist_ok=True)
    if matcher:
        os.makedirs(args.out_dir, exist_ok=True)

    total = 0
    with open(args.out_index, "a", encoding="utf-8") as idx:
        for bi, path in enumerate(files, 1):
            base = os.path.basename(path)
            try:
                env = UnityPy.load(path)
            except Exception as exc:  # noqa: BLE001
                print(f"[{bi}/{len(files)}] LOADFAIL {base}: {exc}", flush=True)
                continue
            n = 0
            for _p, sf in iter_serialized(env):
                for obj in sf.objects.values():
                    if obj.type.name != "MonoBehaviour":
                        continue
                    try:
                        tree = obj.read_typetree()
                    except Exception:  # noqa: BLE001
                        continue
                    if not isinstance(tree, dict):
                        continue
                    n += 1
                    total += 1
                    pptr = tree.get("m_Script")
                    sname = None
                    if isinstance(pptr, dict):
                        info = smap.get(str(pptr.get("m_PathID")))
                        if info:
                            sname = info.get("class")
                    rec = {
                        "bundle": base,
                        "path_id": obj.path_id,
                        "script": sname,
                        "name": tree.get("m_Name"),
                        "keys": list(tree.keys()),
                    }
                    idx.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    if matcher and (matcher.search(sname or "") or matcher.search(str(tree.get("m_Name") or ""))):
                        d = os.path.join(args.out_dir, (sname or "unknown"))
                        os.makedirs(d, exist_ok=True)
                        with open(os.path.join(d, f"{obj.path_id}.json"), "w", encoding="utf-8") as fh:
                            json.dump({"bundle": base, "path_id": obj.path_id, "tree": tree}, fh, ensure_ascii=False, indent=1, default=str)
            print(f"[{bi}/{len(files)}] {base}: mb={n}", flush=True)
    print("DONE total", total, flush=True)


if __name__ == "__main__":
    main()
