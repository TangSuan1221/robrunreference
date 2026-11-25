const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,240));if(++n>=lim)break}}}
p("A. federal / feds", /federal|\bfed\b|feds/i, 40)
p("B. raid (非 battle raid)", /raid/i, 40)
p("C. 时间格式 estadh / 时长", /estadh|:time:/i, 25)
p("D. server 相关", /^server|_server|servers_/i, 40)
