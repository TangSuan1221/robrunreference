const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] = "+clean(v).replace(/\n/g," | ").slice(0,120));if(++n>=lim)break}}}
p("split/move/drop 动作", /^(item_|inventory_|context_)?(action_)?(split|move|drop|put|place|lower|unload|discard)/i, 40)
p("含 Drop 的 key", /drop/i, 40)
p("现金藏匿 / cash stash", /stash|cash_hide|hide_cash/i, 20)
