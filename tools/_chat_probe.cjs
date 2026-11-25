const fs=require('fs')
const j=JSON.parse(fs.readFileSync('out/l10n_en.json','utf8'))
// 展平成 [table, key, value]
const rows=[]
for(const t of j.tables||[]) for(const e of t.entries||[]) rows.push([t.name,e.key,e.value])
console.log('total entries', rows.length)
const pats=[/is wanted/i,/escapes/i,/\bdied\b/i,/wanted/i,/chat/i,/motel/i,/looty/i,/escaped/i,/arrest/i]
const seen=new Set()
for(const re of pats){
  console.log('\n===== ' + re)
  let n=0
  for(const [tbl,key,val] of rows){
    if(re.test(val)||re.test(key)){
      const id=key+'|'+val
      if(seen.has(id)) continue
      seen.add(id); n++
      if(n<=25) console.log(`  [${key}] = ${String(val).slice(0,160)}`)
    }
  }
  console.log('  --- matched ' + n)
}
