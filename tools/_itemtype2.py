import re
src = open('out/il2cpp/dump.cs', encoding='utf-8', errors='replace').read().split('\n')
for i,l in enumerate(src):
    if re.match(r'^public enum InventoryItemType\b', l):
        print('line', i+1)
        vals=[]
        for j in range(i, min(i+400, len(src))):
            m = re.match(r'\s*(\w+)\s*=\s*(-?\d+),', src[j])
            if m: vals.append((m.group(1), int(m.group(2))))
            if '}' in src[j] and j>i: break
        print('count', len(vals))
        for k,(n,v) in enumerate(vals):
            print('  %-42s %d' % (n, v))
        break
