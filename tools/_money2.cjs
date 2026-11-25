const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=45)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,230));if(++n>=lim)break}}}
p("A. 卖/收款/拿钱", /take_cash|withdraw|sell_|_sell|payout|receive/i, 40)
p("B. Hub / motel", /motel|hub|lenny/i, 30)
p("C. 背包丢失/寄存", /inventor.*(lost|lose|keep|store|transfer)|stor.*inventor|safe.*inventor/i, 30)
p("D. 脏钱机制", /dirty/i, 30)
