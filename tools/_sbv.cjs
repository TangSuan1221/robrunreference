const fs=require("fs");
const dir="out/so_dump2/SettlementBuildingViewDescriptions";
for(const f of fs.readdirSync(dir)){
  const j=JSON.parse(fs.readFileSync(dir+"/"+f,"utf8"));
  console.log("\n### "+f);
  console.log("顶层键:", Object.keys(j).join(", "));
  const listKey=Object.keys(j).find(k=>Array.isArray(j[k]));
  if(!listKey){ console.log(JSON.stringify(j).slice(0,900)); continue }
  const list=j[listKey];
  console.log(listKey+" 长度 =", list.length);
  list.forEach((it,i)=>{
    const id=it._id||it.id||"?";
    const keys=Object.keys(it);
    console.log("\n["+i+"] _id="+id+"  键: "+keys.join(","));
    console.log("   "+JSON.stringify(it).slice(0,700));
  });
}
