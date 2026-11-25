const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const flat=[]
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) flat.push([k,v])
function dump(title,re,limit){
  const hits=flat.filter(([k,v])=>re.test(k)||re.test(String(v)))
  console.log("\n########## "+title+"   hits="+hits.length)
  for(const [k,v] of hits.slice(0,limit||40)) console.log(k.padEnd(46)+" = "+String(v).replace(/\n/g," | ").slice(0,190))
}
dump("A. death / dead", /^(death|dead)_/i, 45)
dump("B. confiscat", /confiscat/i, 25)
dump("C. lose/lost", /\b(lose|lost|losing)\b/i, 30)
