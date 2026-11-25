const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const flat=[]
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) flat.push([k,v])
function dump(t,re,lim){const h=flat.filter(([k,v])=>re.test(k)||re.test(String(v)));console.log("\n##### "+t+"  hits="+h.length);for(const [k,v] of h.slice(0,lim||40))console.log(k.padEnd(48)+" = "+String(v).replace(/\n/g," | ").slice(0,200))}
dump("cash 键", /cash/i, 40)
dump("money/workbench 洗钱", /money|launder|dirty/i, 45)
