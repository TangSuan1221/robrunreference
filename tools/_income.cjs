const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=45)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,230));if(++n>=lim)break}}}
p("A. 区中心 Hangar 可卖货", /sector_center|hangar/i, 30)
p("B. 教学/提示里的赚钱方法", /loading_tip.*(cash|money|earn|sell|profit|pay)|how_to_make|make_money|earn/i, 30)
p("C. 轮盘规则", /roulette_dialog|fortune_wheel|wheel_/i, 25)
p("D. 工作/委托/悬赏", /_job_|contract|bounty|order_|delivery|quest_/i, 30)
