const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const flat=[]
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) flat.push([k,v])
console.log("=== ALL battle_chat_event_* / chat_battle_event_* ===")
for(const [k,v] of flat.filter(([k])=>/^(battle_chat|chat_battle_event|chat_)/i.test(k)).sort((a,b)=>a[0].localeCompare(b[0])))
  console.log(k.padEnd(52)+" = "+String(v).replace(/\n/g,"\\n").slice(0,170))
