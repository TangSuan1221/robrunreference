const fs=require("fs");
const l10n=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));
const id2key=l10n.id2key||{}; const byKey=new Map();
for(const tb of l10n.tables) for(const [k,v] of Object.entries(tb.byKey||{})) byKey.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
function loc(o){ if(!o) return "";
  const r=o.m_TableEntryReference||{}; const kid=r.m_KeyId; const key=id2key[String(kid)]||r.m_Key||"";
  const val=key?byKey.get(key):undefined;
  return val!==undefined? key+" = "+clean(val) : ("keyId:"+kid+" key:"+(key||"?"));
}
const dir="out/so_dump2/SettlementBuildingViewDescriptions";
const j=JSON.parse(fs.readFileSync(dir+"/"+fs.readdirSync(dir)[0],"utf8"));
const t=j.tree;
const list=t["<List>k__BackingField"];
console.log("共 "+list.length+" 条\n");
for(const it of list){
  const id=it["<Identified>k__BackingField"]?._id;
  console.log("========== _id = "+id+" ==========");
  console.log("  其余键: "+Object.keys(it).join(", "));
  console.log("  Name        : "+loc(it["<Name>k__BackingField"]));
  console.log("  SettlerBonus: "+loc(it["<SettlerBonus>k__BackingField"]));
  console.log("  OwnerBonus  : "+loc(it["<OwnerBonus>k__BackingField"]));
  const rest={};
  for(const k of Object.keys(it)) if(!/^<(Identified|Name|SettlerBonus|OwnerBonus)>/.test(k)) rest[k]=it[k];
  console.log("  其它字段: "+JSON.stringify(rest).slice(0,420));
  console.log();
}
