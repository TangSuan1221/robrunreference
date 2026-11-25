#!/usr/bin/env python
"""Extract class definitions from Il2CppDumper dump.cs by name substring.

Usage:
  python tools/dump_class.py SettlementBuildingDescription PlotBuildingConfig
  python tools/dump_class.py --regex 'Settlement.*Builder' --max 5
  python tools/dump_class.py --list   (list all class names matching nothing = summary counts)
Options:
  --dump PATH (default out/il2cpp/dump.cs)
  --ctx N     extra context lines after class end (default 0)
  --limit N   max classes printed per pattern (default 3)
  --no-fields only print signature lines (class decl + methods)
"""
import re
import sys

DUMP = 'out/il2cpp/dump.cs'

CLASS_RE = re.compile(r'^(?:public|internal|private|protected|sealed|abstract|static|readonly|partial|\[|//|@)*.*?\b(class|struct|enum|interface)\s+([A-Za-z_][\w`<>,\.\[\]]*)')
DECL_RE = re.compile(r'^(// Namespace: (.*))$')


def load(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read().split('\n')


def blocks(lines):
    """Yield (start_idx, end_idx, decl_line, name, namespace, kind)."""
    cur_ns = ''
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = DECL_RE.match(line.strip())
        if m:
            cur_ns = m.group(2).strip()
            i += 1
            continue
        if line.startswith('// Namespace:'):
            cur_ns = line.split(':', 1)[1].strip()
            i += 1
            continue
        stripped = line.strip()
        if stripped.startswith('public ') or stripped.startswith('internal ') or stripped.startswith('private ') or stripped.startswith('protected '):
            if re.search(r'\b(class|struct|enum|interface)\b', stripped) and lines[i + 1].startswith('{'):
                # find matching closing brace at column 0
                j = i + 1
                while j < n and lines[j] != '}':
                    j += 1
                name_m = re.search(r'\b(?:class|struct|enum|interface)\s+([A-Za-z_][\w`]*)', stripped)
                kind_m = re.search(r'\b(class|struct|enum|interface)\b', stripped)
                yield (i, min(j, n - 1), stripped, name_m.group(1) if name_m else '?',
                       cur_ns, kind_m.group(1) if kind_m else '?')
                i = j + 1
                continue
        i += 1


def main():
    args = sys.argv[1:]
    path = DUMP
    limit = 3
    show_all = False
    if '--dump' in args:
        i = args.index('--dump')
        path = args[i + 1]
        del args[i:i + 2]
    if '--limit' in args:
        i = args.index('--limit')
        limit = int(args[i + 1])
        del args[i:i + 2]
    if '--all' in args:
        show_all = True
        args.remove('--all')
    if not args:
        print(__doc__)
        return
    lines = load(path)
    patterns = [p.lower() for p in args]
    printed = {}
    total = 0
    for (s, e, decl, name, ns, kind) in blocks(lines):
        key = (ns, name)
        full = ('%s.%s' % (ns, name)).lower()
        for p in patterns:
            if p in full:
                c = printed.get(p, 0)
                if not show_all and c >= limit:
                    break
                printed[p] = c + 1
                total += 1
                print('// ==== %s  (line %d-%d) ====' % (full, s + 1, e + 1))
                for ln in lines[s:e + 1]:
                    print(ln)
                print()
                break
    print('// printed %d class bodies' % total, file=sys.stderr)


if __name__ == '__main__':
    main()
