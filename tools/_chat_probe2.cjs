const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const t=j.tables[0]
console.log("byId keys:", Object.keys(t.byId).length, "byKey keys:", Object.keys(t.byKey).length)
const bk=Object.keys(t.byKey).slice(0,5)
for(const k of bk) console.log("  byKey", k, "=>", JSON.stringify(t.byKey[k]).slice(0,120))
// build a flat search space: key -> value
const flat=[]
for(const tb of j.tables){
  for(const [k,v] of Object.entries(tb.byKey||{})) flat.push([tb.name,k,v])
}
console.log("flat total", flat.length)
global.FLAT=flat
const pats=[/wanted/i,/\bescape/i,/\bdied\b/i,/\bchat\b/i,/motel/i,/looty/i,/arrest/i,/\bkilled\b/i,/\bdies\b/i]
for(const re of pats){
  const hits=flat.filter(([tb,k,v])=>re.test(String(v))||re.test(k))
  console.log("\n===== "+re+"  hits="+hits.length)
  for(const [tb,k,v] of hits.slice(0,20)) console.log("   ["+k+"] = "+String(v).slice(0,150))
}
