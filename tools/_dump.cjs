const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,210));if(++n>=lim)break}}}
p("A. 垃圾桶 dumpster", /dumpster|trash|garbage/i, 20)
p("B. 运输 cargo haul", /haul|freight|transport.*cargo|cargo.*job|cargo.*deliver/i, 25)
p("C. 警察名额/满员", /duty.*full|full.*duty|cop.*limit|police.*limit|no.*slot|slots.*full/i, 25)
p("D. 自由职业/杂活", /freelance|odd_job|side_job|work_|earn_|income/i, 30)
