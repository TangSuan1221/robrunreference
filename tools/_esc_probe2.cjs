const fs=require("fs")
const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"))
const m=new Map()
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v)
function show(keys){for(const k of keys){ if(m.has(k)) console.log("\n["+k+"]\n"+String(m.get(k)).replace(/<color=[^>]*>/g,"").replace(/<\/color>/g,"").replace(/\n/g,"\n    ")); else console.log("\n["+k+"] <NOT FOUND>")}}
show(["codex_buff_robber_description","hints_become_robber_description","hints_location_leave_header","hints_location_leave_description","codex_buff_safe_zone_description","tutorial_first_theft","tutorial_first_theft_sub_step_second","close_room_message","left_until_exit","exit_marker_description","location_border_1","location_border_2","car_leave_tip"])
const m2=[]
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) if(/^tsd_u_civil_gas_station/.test(k)) m2.push([k,v])
console.log("\n\n===== 加油站 NPC 对话（开车甩警察）=====")
for(const [k,v] of m2) console.log("\n["+k+"]\n"+String(v).replace(/<color=[^>]*>/g,"").replace(/<\/color>/g,"").replace(/\n/g,"\n    "))
