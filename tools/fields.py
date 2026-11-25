#!/usr/bin/env python
"""Compact field-only extractor: for class names given on the command line, print the
class declaration and its field lines (dropping properties/methods/RVA noise).

Usage:
  python tools/fields.py PlotConstructionSlotDescription StorageSlotDescription
  python tools/fields.py --ns 'Models.ReferencesProject.Descriptions.(Plot|MainBuilding)' --limit 40
"""
import argparse
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
            yield cur_ns, i, min(j, n - 1)
            i = j + 1
            continue
        i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('names', nargs='*')
    ap.add_argument('--ns', default=None)
    ap.add_argument('--limit', type=int, default=60)
    ap.add_argument('--with-methods', action='store_true')
    ap.add_argument('--dump', default=DUMP)
    args = ap.parse_args()
    lines = open(args.dump, 'r', encoding='utf-8', errors='replace').read().split('\n')
    ns_pat = re.compile(args.ns, re.I) if args.ns else None
    want = [w.lower() for w in args.names]
    shown = 0
    for ns, s, e in iterate(lines):
        body = lines[s:e + 1]
        decl = body[0]
        nm = re.search(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w`]*)', decl)
        cname = nm.group(1) if nm else '?'
        full = ns + '.' + cname
        hit = (ns_pat and ns_pat.search(full)) or any(w in full.lower() for w in want)
        if not hit:
            continue
        shown += 1
        if shown > args.limit:
            break
        print('## %s  (line %d)  %s' % (full, s + 1, decl.strip()[:120]))
        in_fields = True
        for ln in body[1:]:
            t = ln.strip()
            if t.startswith('// Properties') or t.startswith('// Methods'):
                in_fields = False
            if not in_fields and not args.with_methods:
                continue
            if t.startswith('//'):
                continue
            if re.match(r'^(public|private|internal|protected|static|readonly|\[)', t) and 'get; }' not in t:
                print('    ' + t)
        print()


if __name__ == '__main__':
    main()
