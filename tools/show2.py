import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
re_type = re.compile(r'^(?:public |internal |private |protected )?(?:sealed |abstract |static |partial |readonly |ref )*(?:class|struct|interface|enum)\s+([A-Za-z0-9_<>`, ]+?)\s*(?::|$)')
# index
idx=[]
for i,l in enumerate(lines):
    s=l.strip()
    if s.startswith('//'): continue
    m=re_type.match(s)
    if m: idx.append((m.group(1).strip(), i))
want = ['OwnedSettlementConfig','PlotSpotConfig','EvictConfig','LandOwnershipDialogModel','SettlementCardView','RentPlotInfoDialogModel','RentSignModel','BuySettlementView','SettlementOwnerPanelView','ClanOwnerPanelView','LandOwnershipSettlementView','RealmEntryView','RealmInfoSourceModel','SwitchRealmDialogModel','SwitchRealmDialogView','RealmScheduleDayRowView','RealmBuildingsMarkerView','RealmSectorCenterView','RealmPopulationView','MapDialogView','MapBuildingDescription','MapBuildingView']
def clean(block):
    out=[]
    for l in block:
        if '[CompilerGenerated]' in l or '[NullableContext' in l or '[Nullable(' in l or 'k__BackingField' in l: continue
        if re.search(r'public .* (get_|set_)', l): continue
        if re.match(r'\s*// RVA:', l): continue
        if re.match(r'\s*public (void|int|long|bool|float|string|IReadOnly|List|Dictionary|ValueTuple)[^\n]*\(\) \{ \}', l): continue
        if l.strip()=='' : continue
        out.append(l.rstrip())
    return out
lines_full = lines
for w in want:
    hits=[ln for nm,ln in idx if nm==w or nm.startswith(w+'<')]
    if not hits:
        print('### MISSING', w); continue
    for ln in hits[:1]:
        # find end
        end=ln
        depth=0; started=False
        for j in range(ln, min(ln+3000, len(lines))):
            depth += lines[j].count('{') - lines[j].count('}')
            if '{' in lines[j]: started=True
            if started and depth==0:
                end=j; break
        print('#'*10, w, 'line', ln+1)
        print('\n'.join(clean(lines[ln:end+1])))
