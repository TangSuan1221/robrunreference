const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const c=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)){console.log("["+k+"] "+c(v).replace(/\n/g," ").slice(0,200));if(++n>=lim)break}}}
p("A. trailer/home/main_building", /trailer|home_[0-9]|main_building/i, 45)
p("B. tier / district level", /^tier|district_name|settlement_tier|settlement_by_tier|_tier_[0-9]/i, 40)
p("C. plot_sale / settlement_sale", /plot_sale|settlement_sale|land_plot_title/i, 30)
