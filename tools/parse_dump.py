"""Parse Il2CppDumper dump.cs into class/method indices.

Outputs out/dump_classes.tsv and out/dump_methods.tsv plus a JSON index
out/dump_index.json  { classes: {name: {ns, kind, line, base, fields[], methods[]}} }
"""
import json
import os
import re
import sys

DUMP = sys.argv[1] if len(sys.argv) > 1 else "out/il2cpp/dump.cs"

re_ns = re.compile(r"^// Namespace: (.*)$")
re_type = re.compile(r"^(?:\[[^\]]*\]\s*)*(public|internal|private|protected)?\s*(?:static |sealed |abstract |partial )*(class|struct|enum|interface)\s+([\w`<>,\.\[\]]+)\s*(?::\s*([^{]+))?")
re_field = re.compile(r"^\s*(?:public|private|protected|internal)\s+(?:static |readonly |const )*([\w\.<>,\[\]`?&]+)\s+(\w+);\s*(?://\s*(0x[0-9A-Fa-f]+))?")
re_meth = re.compile(r"^\s*(?:public|private|protected|internal)\s+(?:static |virtual |abstract |override |sealed |new |extern |unsafe )*([\w\.<>,\[\]`?&]+)\s+(\w+)\s*\(([^)]*)\)")
re_rva = re.compile(r"^\s*// RVA: (0x[0-9A-Fa-f]+) Offset: (0x[0-9A-Fa-f]+) VA: (0x[0-9A-Fa-f]+)")

classes = {}
order = []
cur = None
cur_ns = ""
pending_rva = None
with open(DUMP, encoding="utf-8", errors="replace") as fh:
    for lineno, line in enumerate(fh, 1):
        line = line.rstrip("\n")
        m = re_ns.match(line)
        if m:
            cur_ns = m.group(1).strip()
            continue
        m = re_type.match(line)
        if m and "{" not in line[: line.find("(") if "(" in line else len(line)]:
            name = m.group(3)
            base = (m.group(4) or "").strip()
            cur = {
                "name": name,
                "ns": cur_ns,
                "kind": m.group(2),
                "line": lineno,
                "base": base,
                "fields": [],
                "methods": [],
            }
            classes[name] = cur
            order.append(name)
            continue
        m = re_rva.match(line)
        if m:
            pending_rva = m.group(1)
            continue
        if cur is None:
            continue
        m = re_meth.match(line)
        if m:
            cur["methods"].append({"ret": m.group(1), "name": m.group(2), "args": m.group(3).strip(), "rva": pending_rva, "line": lineno})
            pending_rva = None
            continue
        m = re_field.match(line)
        if m:
            cur["fields"].append({"type": m.group(1), "name": m.group(2), "offset": m.group(3), "line": lineno})
            pending_rva = None

os.makedirs("out", exist_ok=True)
with open("out/dump_classes.tsv", "w", encoding="utf-8") as fh:
    for name in order:
        c = classes[name]
        fh.write(f"{c['line']}\t{c['kind']}\t{c['ns']}\t{name}\t{c['base']}\t{len(c['fields'])}\t{len(c['methods'])}\n")
with open("out/dump_methods.tsv", "w", encoding="utf-8") as fh:
    for name in order:
        c = classes[name]
        for m in c["methods"]:
            fh.write(f"{m['line']}\t{c['name']}\t{m['ret']}\t{m['name']}\t{m['args']}\t{m['rva']}\n")
json.dump({"classes": classes, "order": order}, open("out/dump_index.json", "w", encoding="utf-8"), ensure_ascii=False)
print("classes:", len(classes), "methods:", sum(len(c["methods"]) for c in classes.values()))
print("wrote out/dump_classes.tsv out/dump_methods.tsv out/dump_index.json")
