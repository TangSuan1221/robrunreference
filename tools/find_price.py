#!/usr/bin/env python
"""Find classes whose fields look like price/resource containers.

Usage: python tools/find_price.py [--pat REGEX]
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
    ap.add_argument('--pat', default=r'Price|Cost|ItemAmounts|Resources|Payment|Pay')
    ap.add_argument('--limit', type=int, default=40)
    ap.add_argument('--dump', default=DUMP)
    args = ap.parse_args()
    lines = open(args.dump, 'r', encoding='utf-8', errors='replace').read().split('\n')
    pat = re.compile(args.pat, re.I)
    name_re = re.compile(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w]*)')
    res = []
    for ns, s, e in iterate(lines):
        m = name_re.search(lines[s])
        full = ns + '.' + (m.group(1) if m else '?')
        hits = []
        for ln in lines[s:e + 1]:
            if 'k__BackingField' in ln and pat.search(ln):
                hits.append(ln.strip()[:200])
            elif pat.search(ln) and ('(' in ln and ')' in ln) and 'RVA' not in ln and 'public' in ln and '{ }' in ln:
                hits.append('M ' + ln.strip()[:200])
        if hits:
            res.append((full, hits, s + 1))
    for full, hits, line in res[:args.limit]:
        print('## %s (line %d)' % (full, line))
        for h in hits[:8]:
            print('   ' + h)
    print('// %d classes matched' % len(res), file=sys.stderr)


if __name__ == '__main__':
    main()
