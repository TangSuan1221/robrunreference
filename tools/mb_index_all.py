"""Build a global index: every MonoBehaviour in the Addressables folder with its script class.

Writes out/mb_all.jsonl  {bundle, cab, path_id, script, name, keys}
Optionally dumps full typetree JSON for scripts/names matching --match into out/mb_dump/<script>/
"""
import argparse
import json
import os
import re
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("aa_dir")
    ap.add_argument("--match", default=None)
    ap.add_argument("--out-index", default="out/mb_all.jsonl")
    ap.add_argument("--out-dir", default="out/mb_dump")
    ap.add_argument("--only-bundle", default=None, help="substring filter on bundle filename")
    args = ap.parse_args()

    env = UnityPy.load(args.aa_dir)
    cab2bundle = {}
    for path, sf in env.files.items():
        try:
            cab2bundle[sf.name] = os.path.basename(path)
        except Exception:  # noqa: BLE001
            pass
    print("files:", len(env.files), "cabs:", len(cab2bundle), flush=True)

    matcher = re.compile(args.match) if args.match else None
    os.makedirs(os.path.dirname(args.out_index) or ".", exist_ok=True)
    if matcher:
        os.makedirs(args.out_dir, exist_ok=True)

    total = 0
    resolved = 0
    with open(args.out_index, "w", encoding="utf-8") as idx:
        for obj in env.objects:
            if obj.type.name != "MonoBehaviour":
                continue
            cab = getattr(obj.assets_file, "name", None)
            bundle = cab2bundle.get(cab, "")
            if args.only_bundle and args.only_bundle not in bundle:
                continue
            total += 1
            try:
                tree = obj.read_typetree()
            except Exception:  # noqa: BLE001
                continue
            sname = None
            pptr = tree.get("m_Script") if isinstance(tree, dict) else None
            if isinstance(pptr, dict):
                try:
                    s = pptr.read()
                    sname = getattr(s, "m_ClassName", None)
                except Exception:  # noqa: BLE001
                    sname = None
            if sname:
                resolved += 1
            name = tree.get("m_Name") if isinstance(tree, dict) else None
            rec = {
                "bundle": bundle,
                "path_id": obj.path_id,
                "script": sname,
                "name": name,
                "keys": list(tree.keys()) if isinstance(tree, dict) else [],
            }
            idx.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if matcher and (matcher.search(sname or "") or matcher.search(name or "")):
                d = os.path.join(args.out_dir, (sname or "unknown"))
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, f"{obj.path_id}.json"), "w", encoding="utf-8") as fh:
                    json.dump({"bundle": bundle, "path_id": obj.path_id, "tree": tree}, fh, ensure_ascii=False, indent=1, default=str)
            if total % 2000 == 0:
                print("scanned", total, "resolved", resolved, flush=True)
    print("DONE total", total, "resolved", resolved, flush=True)


if __name__ == "__main__":
    main()
