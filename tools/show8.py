import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
def block(ln, maxh=1200):
    depth=0; started=False; end=ln-1
    for j in range(ln-1, min(ln+maxh, len(lines))):
        depth += lines[j].count('{') - lines[j].count('}')
        if '{' in lines[j]: started=True
        if started and depth==0:
            end=j; break
    return lines[ln-1:end+1]
def clean(bl):
    out=[]
    for l in bl:
        if '[CompilerGenerated]' in l or '[NullableContext' in l or '[Nullable(' in l or 'k__BackingField' in l: continue
        if re.search(r'public .* (get_|set_)', l): continue
        if re.match(r'\s*// RVA:', l): continue
        if re.match(r'\s*public (void|int|long|bool|float|string|IReadOnly|List|Dictionary|ValueTuple|static)[^\n]*\(\) \{ \}', l): continue
        if l.strip()=='': continue
        out.append(l.rstrip())
    return out
for name,ln in [('CargoOpenWorkbenchDescription',116331),('CargoExchangeWorkbenchDescription',117094),('CargoProductionWorkbenchDescription',115741),('CargoChargeWorkbenchDescription',117571),('CryptoWorkbenchDescription',101323),('MoneyWorkbenchDescription',85459),('CollectionTableDescription',104327),('CargoOpenWorkbenchData',0)]:
    print('#'*12, name, ln)
    print('\n'.join(clean(block(ln)))[:3500])
