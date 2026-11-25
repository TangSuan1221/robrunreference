const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,190));if(++n>=lim)break}}}
p("A. 市民/角色切换", /citizen|civil/i, 25)
p("B. 安全区", /safe_zone|motel/i, 20)
p("C. 交易商/销赃点", /trader|fence|sell_point|smuggler/i, 30)
p("D. 现金不能用的提示", /unavailable_by_cash|unavailable_by_money|not_enough_cash|need_cash/i, 20)
