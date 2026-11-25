const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=50)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,210));if(++n>=lim)break}}}
p("A. 租地/地契", /rent|plot_sale|land_plot|plot_title|title_/i, 50)
p("B. 新生活/开局", /new_life|start|begin|first_time|onboarding|welcome/i, 30)
p("C. 破产/没钱提示", /not_enough|no_money|insufficient|need_money|cant_afford/i, 25)
