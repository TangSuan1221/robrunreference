const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const m=new Map()
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v)
const clean=s=>String(s).replace(/<color=[^>]*>/g,"").replace(/<\/color>/g,"")
function dump(t,re,lim){console.log("\n########## "+t);let n=0;for(const [k,v] of m){ if(re.test(k)&&!/_duplicate$/.test(k)){ console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,230)); if(++n>=(lim||50)) break } }}
dump("A. settlement 相关", /^settlement|settlement_/i, 45)
dump("B. plot 相关（地皮/地块）", /^plot|_(plot|plots)_/i, 45)
