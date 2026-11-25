const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,180));if(++n>=lim)break}}}
p("global_map_*", /^global_map/i, 45)
p("map_* / marker / legend", /^map_|marker|legend|_pin_/i, 25)
p("motel / safe zone", /motel|safe_zone|safe_place/i, 15)
p("battle_conqest 全部", /battle_conqest/i, 30)
