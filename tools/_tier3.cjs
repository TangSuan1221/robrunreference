const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const c=s=>String(s).replace(/<[^>]*>/g,"");
const p2=(t,re,lim=50)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)){console.log("["+k+"] "+c(v).replace(/\n/g," ").slice(0,190));if(++n>=lim)break}}}
p2("A. 免费/起始/赠予", /free|given|starter|default_house|initial_building|gift|no_charge/i, 45)
p2("B. 建造/放置/购买结构", /^build_|place_|buy_|purchase_|install_|cant_|cannot_/i, 55)
p2("C. plot 相关全部", /^plot_|plot_title|land_plot|vacant/i, 45)
