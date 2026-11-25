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
for name,ln in [('TaxCollectionSettlementModel',264440),('TaxCollectionDialogModel',0),('TaxCollectionDialogView',0),('TaxPointModel',0),('MoneyWorkbenchData',0),('MoneyWorkbenchBonusConfig',0),('MoneyWorkbenchBonusEntry',0),('LaunderingState',0),('LaunderingMessage',0),('LaunderingPutMessage',0),('LaunderingTakeMessage',0),('LaunderingTakeDirtyMessage',0),('LaunderingSetActiveMessage',0),('LaunderingPoopMessage',0),('MoneyLaunderingDialogModel',0),('SettlementCashDatabaseData',220731),('SettlementCashPublicData',220750),('SettlementCashEntityModel',0),('TaxCollectionClanModelUpdater',0),('SettlementTaxDescription',67066)]:
    print('#'*10, name, ln)
    if ln==0: continue
    print('\n'.join(clean(block(ln)))[:2600])
