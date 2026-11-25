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
for name,ln in [('WantedPointsConfig',70671),('DeathScreenModel',383737),('PrisonViewDescription',442622),('PrisonEnterTypeDescription',81591),('LocationPrisonEscapeDescription',81468),('PrisonAccusationDialogModel',271439),('TermImprisonmentView',442816),('UserImprisonmentYearsModel',460311),('BattleStaminaViewDescription',259686),('ConfiscationModel',413352),('ConfiscationRule',413394),('ConfiscationDescription',413319),('ImprisonmentYearsByDataModel',460293),('ReviveCommand',407533),('RespawnCommand',407592),('SpawnByMainBuildingCommand',407802),('SpawnByOutBuildingCommand',407886)]:
    print('#'*10, name, ln)
    print('\n'.join(clean(block(ln)))[:2400])
