#!/usr/bin/env python
"""Decode Unity Localization StringTable + SharedTableData from Addressables bundles.

Usage:
  PYTHONPATH=tools/pylib python tools/dump_stringtable.py \
      --bundle "...\localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle" \
      [--shared-bundle "...\localization-assets-shared_assets_all.bundle"] \
      --out out/l10n_en.json

Layout (Unity 6 / Localization 1.x, IL2CPP build):
  StringTable : m_Name, m_LocaleId, m_SharedData(PPtr), m_TableData[ {m_Id, m_Localized, m_Metadata} ]
  SharedTableData : m_Entries[ {m_Id, m_Key} ]
"""
import argparse
import json
import sys

import UnityPy

UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"


def read_tables(path):
    env = UnityPy.load(path)
    out = []
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        try:
            t = obj.read_typetree()
        except Exception as e:
            print('skip %s: %s' % (obj.path_id, e), file=sys.stderr)
            continue
        if 'm_TableData' in t and isinstance(t.get('m_TableData'), list):
            out.append({'kind': 'StringTable', 'name': t.get('m_Name', ''),
                        'path_id': obj.path_id, 'bundle': path.split('\\')[-1],
                        'rows': t['m_TableData']})
        elif 'm_Entries' in t and isinstance(t.get('m_Entries'), list):
            out.append({'kind': 'SharedTableData', 'name': t.get('m_Name', ''),
                        'path_id': obj.path_id, 'bundle': path.split('\\')[-1],
                        'rows': t['m_Entries']})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle', required=True, action='append')
    ap.add_argument('--shared-bundle', action='append', default=[])
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    tables = []
    for b in list(args.bundle) + list(args.shared_bundle):
        tables += read_tables(b)

    # id -> key name (from SharedTableData)
    id2key = {}
    for tb in tables:
        if tb['kind'] != 'SharedTableData':
            continue
        for r in tb['rows']:
            i = r.get('m_Id')
            k = r.get('m_Key')
            if i:
                id2key[i] = k

    out = {'tables': [], 'id2key': {str(k): v for k, v in id2key.items()}}
    total = 0
    for tb in tables:
        if tb['kind'] != 'StringTable':
            continue
        byid, bykey = {}, {}
        for r in tb['rows']:
            i = str(r.get('m_Id', ''))
            v = r.get('m_Localized', '')
            if not i:
                continue
            byid[i] = v
            k = id2key.get(r.get('m_Id'))
            if k:
                bykey[k] = v
        out['tables'].append({'name': tb['name'], 'path_id': tb['path_id'],
                              'count': len(byid), 'byId': byid, 'byKey': bykey})
        total += len(byid)
        print('  %-40s %6d entries' % (tb['name'], len(byid)), file=sys.stderr)
    print('StringTables: %d, entries: %d, shared keys: %d -> %s'
          % (len(out['tables']), total, len(id2key), args.out), file=sys.stderr)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
