import re, json, collections
src = open('out/il2cpp/dump.cs', encoding='utf-8', errors='replace').read().split('\n')
# find class blocks: lines starting with "public class X" / "public sealed class X"
blocks = {}
i = 0
while i < len(src):
    m = re.match(r'^(?:public|internal)(?: sealed| abstract)? class (\w+)', src[i])
    if m:
        name = m.group(1); start = i; depth = 0; started = False
        j = i
        while j < len(src) and j < i + 400:
            depth += src[j].count('{') - src[j].count('}')
            if '{' in src[j]: started = True
            if started and depth <= 0: break
            j += 1
        blocks.setdefault(name, (start, j))
        i = j
    i += 1
targets = [n for n in blocks if re.search(r'(SlotDescription|SlotTypeDescription)$', n)]
rows = []
for n in sorted(targets):
    s, e = blocks[n]
    body = src[s:e+1]
    members = [re.match(r'\s*private static readonly \S+ <(\w+)>k__BackingField', l) for l in body]
    members = [m.group(1) for m in members if m]
    if members:
        rows.append((n, len(members), members))
for n, c, mem in rows:
    print('%-52s %3d  %s' % (n, c, ','.join(mem)))
json.dump({n: mem for n, c, mem in rows}, open('out/enum_slots.json','w'), indent=1)
