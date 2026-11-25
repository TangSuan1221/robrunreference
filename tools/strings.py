"""Extract printable ASCII strings from a binary and grep them.

Usage: python tools/strings.py <file> [--min 6] [--grep REGEX] [--out FILE]
"""
import argparse
import re
import sys


def strings(path, minimum=6):
    data = open(path, "rb").read()
    cur = bytearray()
    for b in data:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= minimum:
                yield cur.decode("ascii", "replace")
            cur = bytearray()
    if len(cur) >= minimum:
        yield cur.decode("ascii", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--min", type=int, default=6)
    ap.add_argument("--grep", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    pat = re.compile(args.grep, re.I) if args.grep else None
    n = 0
    fh = open(args.out, "w", encoding="utf-8") if args.out else None
    for s in strings(args.path, args.min):
        if pat and not pat.search(s):
            continue
        n += 1
        if fh:
            fh.write(s + "\n")
        elif args.limit == 0 or n <= args.limit:
            print(s)
        if args.limit and n >= args.limit:
            break
    if fh:
        fh.close()
        print("wrote", args.out)
    print("matched", n)


if __name__ == "__main__":
    main()
