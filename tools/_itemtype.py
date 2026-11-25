import re
src = open('out/il2cpp/dump.cs', encoding='utf-8', errors='replace').read().split('\n')
def find_block(pat):
    for i,l in enumerate(src):
        if re.match(pat, l):
            start=i; depth=0; started=False
            out=[]
            for j in range(i, min(i+400, len(src))):
                out.append(src[j])
                depth += src[j].count('{') - src[j].count('}')
                if '{' in src[j]: started=True
                if started and depth<=0: break
            return start+1, out
    return None, None
for pat in [r'^public enum ItemType\b', r'^public class InventoryItemDescription\b', r'^public class InventoryItemTypeDescription\b', r'^public (sealed )?class ItemTypeDescription\b']:
    ln, blk = find_block(pat)
    print('#### %s  -> %s' % (pat, ln))
    if blk:
        for l in blk[:90]:
            if l.strip(): print(l)
    print()
