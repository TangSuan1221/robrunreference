import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
def block(ln, maxh=900):
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
for name,ln in [('SettlementPriceRules',741),('SettlementTaxExtensions',8658),('EvictConfig',77318),('OwnedSettlementConfig',77350),('PlotSpotConfig',77371),('SettlementNameConfig',77413),('LandOwnershipDialogModel',459026),('LandOwnershipDialogUpdater',459072),('RentPlotDialogModel',361464),('RentPlotDialogUpdater',361513),('BuySettlementMessage',198064),('GetItemAmountsForSettlementPriceMessage',202054),('ReportSettlementNameMessage',202509),('RentSignModel',160520),('PlotRentSignExtensions',8032),('SettlementBuildingViewDescription',401789),('BuildingBonus',459344),('SpecialBuildingInfo',464127),('OwnerState',265117),('LandOwnershipTabs',459185)]:
    print('#'*12, name, ln)
    print('\n'.join(clean(block(ln)))[:3000])
