const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const c=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)||c(v).toLowerCase().includes(t.toLowerCase())){if(re.test(k)){console.log("["+k+"] "+c(v).replace(/\n/g," ").slice(0,220));if(++n>=lim)break}}}}
p("A. trailer 文本", /trailer/i, 30)
const p2=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)){console.log("["+k+"] "+c(v).replace(/\n/g," ").slice(0,200));if(++n>=lim)break}}}
p2("B. 建造/结构/初始", /builder_|structure|construction|initial|start_main|empty_plot|free_house/i, 55)
p2("C. rent 相关", /^rent_|rent_land|hint_rent|plot_plan/i, 35)
