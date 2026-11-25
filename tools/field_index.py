#!/usr/bin/env python
"""Index which classes carry numeric config-ish fields (Price/Cost/Time/Duration/Points/Capacity...).

Usage:
  python tools/field_index.py --pat 'Price|Cost|Duration|Time' --limit 80
  python tools/field_index.py --pat 'Capacity|Slots|Amount' --ns 'Settlement|Plot'
Prints: ClassFullName  -> field list
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


FIELD_RE = re.compile(r'(?:private|public|internal|protected)\s+(?:readonly\s+|static\s+)*([^;]+?)\s+<([A-Za-z_]\w*)>k__BackingField;')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pat', default='Price|Cost|Duration|Time')
    ap.add_argument('--ns', default=None)
    ap.add_argument('--limit', type=int, default=80)
    ap.add_argument('--dump', default=DUMP)
    args = ap.parse_args()
    lines = open(args.dump, 'r', encoding='utf-8', errors='replace').read().split('\n')
    fpat = re.compile(args.pat, re.I)
    npat = re.compile(args.ns, re.I) if args.ns else None
    out = []
    for ns, s, e in iterate(lines):
        decl = lines[s]
        nm = re.search(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w`]*)', decl)
        full = ns + '.' + (nm.group(1) if nm else '?')
        if npat and not npat.search(full):
            continue
        hits = []
        for ln in lines[s:e + 1]:
            m = FIELD_RE.search(ln)
            if m and fpat.search(m.group(2)):
                hits.append('%s %s' % (m.group(1).strip(), m.group(2)))
        if hits:
            out.append((full, hits, s + 1))
    out.sort(key=lambda x: (-len(x[1]), x[0]))
    for full, hits, line in out[:args.limit]:
        print('## %s (line %d)' % (full, line))
        print('   ' + '; '.join(hits))
    print('// %d classes matched' % len(out), file=sys.stderr)


if __name__ == '__main__':
    main()
