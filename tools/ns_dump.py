#!/usr/bin/env python
"""Dump class bodies (by namespace/class regex) from dump.cs, optionally fields-only.

Usage:
  python tools/ns_dump.py --ns 'Plot|Settlement' --out out/base_dump.txt
  python tools/ns_dump.py --ns 'SettlementBuilder' --sigs   # fields + method signatures only
Options:
  --ns REGEX      match against "Namespace.Class" (case-insensitive), required
  --out PATH      write to file instead of stdout
  --sigs          drop method bodies `{ }` -> keep as signature only, and drop RVA comments
  --max-lines N   skip classes whose body exceeds N lines (default 400)
  --min-fields N  only classes with at least N field lines (default 0)
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
    ap.add_argument('--ns', required=True)
    ap.add_argument('--out', default=None)
    ap.add_argument('--sigs', action='store_true')
    ap.add_argument('--max-lines', type=int, default=400)
    ap.add_argument('--min-fields', type=int, default=0)
    ap.add_argument('--dump', default=DUMP)
    args = ap.parse_args()
    lines = open(args.dump, 'r', encoding='utf-8', errors='replace').read().split('\n')
    pat = re.compile(args.ns, re.I)
    out = open(args.out, 'w', encoding='utf-8') if args.out else sys.stdout
    n_class = 0
    n_skip = 0
    for ns, s, e in iterate(lines):
        body = lines[s:e + 1]
        decl = body[0].strip()
        nm = re.search(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w`]*)', decl)
        full = '%s.%s' % (ns, nm.group(1) if nm else '?')
        if not pat.search(full):
            continue
        if not pat.search(full) or len(body) > args.max_lines:
            n_skip += 1
            continue
        nf = sum(1 for ln in body if '// 0x' in ln)
        if nf < args.min_fields:
            continue
        out.write('// ==== %s   (line %d, %d fields) ====\n' % (full, s + 1, nf))
        for ln in body:
            if args.sigs:
                if ln.strip().startswith('// RVA:'):
                    continue
                if ln.rstrip().endswith('{ }') or ln.rstrip().endswith('{ }'):
                    ln = ln.rstrip()
                ln = re.sub(r'\s*\{\s*\}\s*$', ';', ln)
            out.write(ln + '\n')
        out.write('\n')
        n_class += 1
    if args.out:
        out.close()
    print('// %d classes written, %d skipped (too long / no match)' % (n_class, n_skip), file=sys.stderr)


if __name__ == '__main__':
    main()
