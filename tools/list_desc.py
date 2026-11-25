#!/usr/bin/env python
"""List the static *Descriptions registries and their entry names.

These are generated reference catalogues: each `FooDescriptions` static class exposes
one static property per authored `FooDescription` entry, so they enumerate the game's
content ids (buildings, cargos, slots, workbenches ...).

Usage:
  python tools/list_desc.py                     # all registries, names only
  python tools/list_desc.py --filter Settlement # only registries matching substring
  python tools/list_desc.py --filter Plot --json out/desc_index.json
"""
import argparse
import json
import re
import sys

DUMP = 'out/il2cpp/dump.cs'


def iterate(lines):
    cur_ns = ''
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith('// Namespace:'):
            cur_ns = line.split(':', 1)[1].strip()
            i += 1
            continue
        s = line.strip()
        if (s.startswith('public ') or s.startswith('internal ') or s.startswith('private ')
                or s.startswith('protected ')) and re.search(r'\b(class|struct|enum|interface)\b', s) \
                and i + 1 < n and lines[i + 1].startswith('{'):
            j = i + 1
            while j < n and lines[j] != '}':
                j += 1
            nm = re.search(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w`]*)', s)
            yield cur_ns, nm.group(1) if nm else '?', i, min(j, n - 1)
            i = j + 1
            continue
        i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--filter', default='')
    ap.add_argument('--json', default=None)
    ap.add_argument('--dump', default=DUMP)
    args = ap.parse_args()
    lines = open(args.dump, 'r', encoding='utf-8', errors='replace').read().split('\n')
    flt = args.filter.lower()
    index = {}
    prop_re = re.compile(r'public static ([A-Za-z_][\w<>,\.\[\] ]*?) ([A-Za-z_][\w]*)(?:<[^>]*>)? \{ get; \}')
    for ns, name, s, e in iterate(lines):
        if not name.endswith('Descriptions'):
            continue
        if flt and flt not in (ns + '.' + name).lower():
            continue
        entries = []
        for ln in lines[s:e + 1]:
            m = prop_re.search(ln)
            if m:
                t, pn = m.group(1).strip(), m.group(2)
                if pn == 'Enum':
                    continue
                entries.append({'name': pn, 'type': t})
        if entries:
            index[ns + '.' + name] = entries
            print('## %s.%s  (%d entries, line %d)' % (ns, name, len(entries), s + 1))
            for en in entries:
                print('   %-40s %s' % (en['name'], en['type']))
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=1)
        print('// wrote %s (%d registries)' % (args.json, len(index)), file=sys.stderr)


if __name__ == '__main__':
    main()
