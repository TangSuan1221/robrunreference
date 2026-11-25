# -*- coding: utf-8 -*-
import json,io,os,re
l10n=json.load(io.open("out/l10n_en.json",encoding="utf-8"))
id2key={int(k):v for k,v in l10n["id2key"].items()}
byKey={}
for tb in l10n["tables"]:
    for k,v in tb.get("byKey",{}).items(): byKey[k]=v
def clean(s): return re.sub(r"<[^>]*>","",str(s))
def loc(o):
    if not o: return ""
    r=o.get("m_TableEntryReference") or {}
    kid=r.get("m_KeyId")
    key=id2key.get(int(kid)) if kid is not None else None
    key=key or r.get("m_Key") or ""
    val=byKey.get(key)
    return (key+" = "+clean(val)) if val is not None else ("?? keyId=%s key=%s"%(kid,key))
d="out/so_dump2/SettlementBuildingViewDescriptions"
f=os.path.join(d,os.listdir(d)[0])
j=json.load(io.open(f,encoding="utf-8"))
lst=j["tree"]["<List>k__BackingField"]
print("共 %d 条\n"%len(lst))
out=[]
for it in lst:
    bid=it["<Identified>k__BackingField"]["_id"]
    row={"id":bid,
         "name":loc(it["<Name>k__BackingField"]),
         "settler":loc(it["<SettlerBonus>k__BackingField"]),
         "owner":loc(it["<OwnerBonus>k__BackingField"]),
         "sprite":(it.get("_sprite") or {}).get("m_AssetGUID","")}
    out.append(row)
    print("=== %s ==="%bid)
    print("  Name        : "+row["name"])
    print("  SettlerBonus: "+row["settler"])
    print("  OwnerBonus  : "+row["owner"])
    print()
io.open("out/settlement_buildings.txt","w",encoding="utf-8").write(
  "\n".join("%s | %s | %s | %s"%(r["id"],r["name"],r["settler"],r["owner"]) for r in out))
