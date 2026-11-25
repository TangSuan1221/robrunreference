const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=45)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] = "+clean(v).replace(/\n/g," | ").slice(0,175));if(++n>=lim)break}}}
p("卖不了 / 不能卖 的限制", /cannot_sell|cant_sell|not_sell|sell_forbidden|sell_.*_blocked|no_sell|sell_price_modifier/i, 30)
p("wine / bottle / 酒", /wine|bottle|alcohol|champagne|whisk|vodka/i, 35)
p("Fence / 收赃", /fence|loot_sell|sell_loot|marker_/i, 35)
p("stash 相关", /stash/i, 25)
