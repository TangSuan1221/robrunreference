const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=50)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,240));if(++n>=lim)break}}}
p("A. 帮派 clan_", /^clan_/i, 55)
p("B. 掠夺锁/警报", /raid_lock|alarm|breach|defense_block/i, 45)
p("C. 税收 tax", /tax/i, 45)
p("D. 队伍 party", /party/i, 30)
