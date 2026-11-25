#!/usr/bin/env python
"""Scan Addressables bundles for TextAsset (and any asset) names + sizes.

Usage:
  PYTHONPATH=tools/pylib python tools/scan_textassets.py [--type TextAsset] [--glob '*.bundle'] [--min-size 0] [--out out/textassets.jsonl]
"""
import argparse
import glob
import json
import os
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"
AA = r"D:\SteamLibrary\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--type', default='TextAsset')
    ap.add_argument('--glob', default='*.bundle')
    ap.add_argument('--min-size', type=int, default=0)
    ap.add_argument('--out', default=None)
    ap.add_argument('----dir', dest='dir', default=AA)
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(args.dir, args.glob)))
    out = open(args.out, 'w', encoding='utf-8') if args.out else sys.stdout
    n = 0
    for f in files:
        try:
            env = UnityPy.load(f)
        except Exception as e:
            print('ERR load %s: %s' % (os.path.basename(f), e), file=sys.stderr)
            continue
        seen = set()
        for obj in env.objects:
            if obj.type.name != args.type:
                continue
            try:
                name = obj.peek_name()
            except Exception:
                name = None
            if name is None:
                try:
                    name = obj.read().m_Name
                except Exception:
                    name = '<noname>'
            try:
                size = obj.byte_size
            except Exception:
                size = -1
            if size < args.min_size:
                continue
            key = (name, size)
            if key in seen:
                continue
            seen.add(key)
            rec = {'bundle': os.path.basename(f), 'name': name, 'size': size,
                   'path_id': obj.path_id}
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
            n += 1
    if args.out:
        out.close()
    print('done, %d rows (type=%s, %d bundles)' % (n, args.type, len(files)), file=sys.stderr)


if __name__ == '__main__':
    main()
