import re,sys
p="out/il2cpp/dump.cs"
lines=open(p,encoding="utf-8",errors="replace").read().split("\n")
def block(name, maxf=999):
    idx=[i for i,l in enumerate(lines) if re.match(r"^public (static )?(sealed )?(class|struct) "+re.escape(name)+r"\b", l)]
    if not idx: print("\n### "+name+" NOT FOUND"); return
    for i in idx[:1]:
        print("\n"+"="*20+" "+name+"  (line %d) "%(i+1)+"="*20)
        j=i
        n=0
        while j<len(lines) and n<maxf:
            l=lines[j]
            if j>i and re.match(r"^// Namespace:",l): break
            if "k__BackingField" in l or re.match(r"^\tpublic .*\{ get",l) or re.match(r"^\tpublic void \.ctor",l) or re.match(r"^\tprivate static void \.cctor",l):
                print("  "+l.strip())
                n+=1
            j+=1
for n in ["SettlementLocationsPlotSpotsPreset","OwnedSettlementConfig","LocationSettlementCashDescription","SettlementBuildingDescription"]:
    block(n, 40)
