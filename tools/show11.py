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
for name,ln in [('MoneyWorkbenchBonusConfig',85396),('MoneyWorkbenchBonusEntry',85431),('LaunderingState',172690),('LaunderingPoopMessage',205184),('LaunderingPutMessage',205209),('LaunderingSetActiveMessage',205239),('LaunderingTakeDirtyMessage',205269),('LaunderingTakeMessage',205299),('MoneyWorkbenchData',221654),('MoneyWorkbenchModel',170249),('TaxPointMarkerModel',323614),('TaxCollectionDialogModel',264589),('MoneyWorkbenchViewDescription',326283),('CashLootNodeModel',185075),('TakeCashModel',163395)]:
    print('#'*10, name, ln)
    print('\n'.join(clean(block(ln)))[:2600])
