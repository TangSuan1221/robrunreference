const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,200));if(++n>=lim)break}}}
p("A. 角色可用性 AvailableFor*", /availablefor|available_for|unavailable_for|required_role|only_criminal|only_robber|criminal_only/i, 40)
p("B. 变罪犯 / 面具", /robber|mask/i, 40)
p("C. 笔记本卖货 / tutorial", /laptop|tutorial_sell|sell_loot/i, 30)
