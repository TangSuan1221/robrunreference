import re
p="out/il2cpp/dump.cs"
lines=open(p,encoding="utf-8",errors="replace").read().split("\n")
def block(name, maxf=60):
    idx=[i for i,l in enumerate(lines) if re.match(r"^public (static )?(sealed )?(class|struct) "+re.escape(name)+r"\b", l)]
    if not idx: print("\n### "+name+" NOT FOUND"); return
    i=idx[0]
    print("\n"+"="*18+" "+name+"  (line %d) "%(i+1)+"="*18)
    j=i; n=0
    while j<len(lines) and n<maxf:
        l=lines[j]
        if j>i and re.match(r"^// Namespace:",l): break
        if re.search(r"k__BackingField|^\tpublic .*\{ get|^\tpublic void \.ctor|^\tpublic static .*\(", l):
            print("  "+l.strip()); n+=1
        j+=1
for n in ["LocationPlotSpotsDescription","PlotSchemeDescription","LocationPlotDescription","LocationPlotSpotDescription","DistrictDescription","TierDescription"]:
    block(n,25)
