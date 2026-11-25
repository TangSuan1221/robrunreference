import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
def block(ln, maxh=600):
    depth=0; started=False; end=ln-1
    for j in range(ln-1, min(ln+maxh, len(lines))):
        depth += lines[j].count('{') - lines[j].count('}')
        if '{' in lines[j]: started=True
        if started and depth==0:
            end=j; break
    return lines[ln-1:end+1]
def clean(block):
    out=[]
    for l in block:
        if '[CompilerGenerated]' in l or '[NullableContext' in l or '[Nullable(' in l or 'k__BackingField' in l: continue
        if re.search(r'public .* (get_|set_)', l): continue
        if re.match(r'\s*// RVA:', l): continue
        if re.match(r'\s*public (void|int|long|bool|float|string|IReadOnly|List|Dictionary|ValueTuple|static)[^\n]*\(\) \{ \}', l): continue
        if l.strip()=='': continue
        out.append(l.rstrip())
    return out
for name,ln in [('RealmLoadScreen',409250),('SwitchRealmCommand',408797),('SwitchRegionCommand',408876),('FindRealmByIdMessage',206339),('RealmInfoSource',161348),('RealmOccupancy',416341),('RealmRecommendation',416361),('RealmEntrySelection',416352),('LineOccupancy',416332),('SwitchRealmViewDescription',417902),('RegionEntryView',441779),('RegionSwitchListModel',441898)]:
    print('#'*12, name, ln)
    print('\n'.join(clean(block(ln))))
