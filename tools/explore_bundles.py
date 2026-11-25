"""Probe Unity bundles: list objects, check typetree availability, dump sample info to JSON."""
import json
import os
import sys
import traceback

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"


def walk_container(env, bundle_path, limit=40):
    info = {"bundle": os.path.basename(bundle_path), "objects": [], "errors": []}
    try:
        env = UnityPy.load(bundle_path)
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"load: {exc}")
        return info
    counts = {}
    samples = []
    for obj in env.objects:
        tname = obj.type.name
        counts[tname] = counts.get(tname, 0) + 1
        if len(samples) < limit and tname in ("MonoBehaviour", "ScriptableObject"):
            try:
                data = obj.read()
                name = getattr(data, "m_Name", None)
                typetree_ok = True
                err = None
                try:
                    tree = obj.read_typetree()
                except Exception as exc:  # noqa: BLE001
                    typetree_ok = False
                    err = str(exc)[:200]
                    tree = None
                samples.append(
                    {
                        "path_id": obj.path_id,
                        "type": tname,
                        "name": name,
                        "script": _script_name(data),
                        "typetree_ok": typetree_ok,
                        "err": err,
                        "keys": list(tree.keys())[:40] if isinstance(tree, dict) else None,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                samples.append({"path_id": obj.path_id, "type": tname, "read_err": str(exc)[:200]})
    info["counts"] = counts
    info["samples"] = samples
    return info


def _script_name(data):
    try:
        mono = data.m_Script
        if mono is None:
            return None
        script = mono.read()
        return getattr(script, "m_ClassName", None) or getattr(script, "m_Name", None)
    except Exception:  # noqa: BLE001
        return None


if __name__ == "__main__":
    out = []
    for path in sys.argv[1:]:
        print("==", path, flush=True)
        res = walk_container(None, path)
        print(json.dumps(res.get("counts", {}), ensure_ascii=False), flush=True)
        for err in res.get("errors", []):
            print("ERR", err, flush=True)
        for s in res.get("samples", [])[:12]:
            print(json.dumps(s, ensure_ascii=False)[:600], flush=True)
        out.append(res)
    with open("out/bundle_probe.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("saved out/bundle_probe.json")
