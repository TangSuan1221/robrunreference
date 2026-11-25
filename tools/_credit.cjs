const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,170));if(++n>=lim)break}}}
p("A. credit 是什么/怎么用", /credit/i, 40)
p("B. 洗钱台/黑市消费", /launder|money_workbench|money_table|black_market/i, 30)
p("C. 轮盘/抽奖", /wheel|roulette|fortune/i, 20)
