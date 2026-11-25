const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const flat=[]
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) flat.push([k,v])
function dump(t,re,lim){const h=flat.filter(([k,v])=>re.test(k)||re.test(String(v)));console.log("\n##### "+t+"  hits="+h.length);for(const [k,v] of h.slice(0,lim||45))console.log(k.padEnd(50)+" = "+String(v).replace(/\n/g," | ").slice(0,210))}
dump("A. 逃离 / 出城 / exit", /(escape|exit|leave|flee|evac|extract)/i, 50)
dump("B. cash zone / 边界 / 关卡", /(cash.?zone|checkpoint|border|tunnel|perimeter|zone)/i, 35)
