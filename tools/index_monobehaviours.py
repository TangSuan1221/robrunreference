"""Index every MonoBehaviour inside Addressables bundles: script class, name, field keys.

Outputs:
  out/mb_index.jsonl   one JSON per MonoBehaviour (bundle, path_id, script, name, nkeys)
  out/mb_dump/<script>/<path_id>.json  full typetree for objects matching --match regex

Usage:
  python tools/index_monobehaviours.py <aa_dir_glob> [--match REGEX] [--limit-bundles N]
"""
import argparse
import glob
import json
import os
import re
import sys
import traceback

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"


def build_script_map(env):
    """path_id -> MonoScript class name, built from the environment itself."""
    out = {}
    for o in env.objects:
        if o.type.name != "MonoScript":
            continue
        try:
            s = o.read()
            out[o.path_id] = getattr(s, "m_ClassName", None)
        except Exception:  # noqa: BLE001
            continue
    return out


def script_name(tree, smap):
    pptr = tree.get("m_Script") if isinstance(tree, dict) else None
    if not isinstance(pptr, dict):
        return None
    pid = pptr.get("m_PathID")
    fid = pptr.get("m_FileID", 0)
    if fid not in (0, None):
        return None
    return smap.get(pid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern")
    ap.add_argument("--match", default=None)
    ap.add_argument("--limit-bundles", type=int, default=0)
    ap.add_argument("--out-index", default="out/mb_index.jsonl")
    ap.add_argument("--out-dir", default="out/mb_dump")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if args.limit_bundles:
        files = files[: args.limit_bundles]
    matcher = re.compile(args.match) if args.match else None
    os.makedirs(os.path.dirname(args.out_index), exist_ok=True)
    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.out_index, "a", encoding="utf-8") as idx:
        for bi, path in enumerate(files, 1):
            base = os.path.basename(path)
            try:
                env = UnityPy.load(path)
            except Exception as exc:  # noqa: BLE001
                print(f"[{bi}/{len(files)}] LOAD-FAIL {base}: {exc}", flush=True)
                continue
            n_mb = 0
            n_named = 0
            smap = build_script_map(env)
            for obj in env.objects:
                if obj.type.name != "MonoBehaviour":
                    continue
                n_mb += 1
                try:
                    tree = obj.read_typetree()
                except Exception:  # noqa: BLE001
                    continue
                sname = script_name(tree, smap)
                name = ""
                if isinstance(tree, dict):
                    name = tree.get("m_Name") or ""
                if sname:
                    n_named += 1
                rec = {
                    "bundle": base,
                    "path_id": obj.path_id,
                    "script": sname,
                    "name": name,
                    "nkeys": len(tree) if isinstance(tree, dict) else 0,
                    "keys": list(tree.keys())[:25] if isinstance(tree, dict) else [],
                }
                idx.write(json.dumps(rec, ensure_ascii=False) + "\n")
                if matcher and (matcher.search(sname or "") or matcher.search(name or "")):
                    d = os.path.join(args.out_dir, (sname or "unknown"))
                    os.makedirs(d, exist_ok=True)
                    with open(os.path.join(d, f"{obj.path_id}.json"), "w", encoding="utf-8") as fh:
                        json.dump({"bundle": base, "path_id": obj.path_id, "tree": tree}, fh, ensure_ascii=False, indent=1, default=str)
            print(f"[{bi}/{len(files)}] {base}: mb={n_mb} named={n_named}", flush=True)


if __name__ == "__main__":
    main()
