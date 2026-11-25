const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=40)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,200));if(++n>=lim)break}}}
p("A. 区/等级/tier", /district|tier|_level_|level_\d|region_/i, 45)
p("B. 产业/business/物业", /business|conquest_object|object_name|_business_/i, 30)
p("C. 聚落公共建筑（8种）", /^(crypto_1|farm_1|lab_1|weapon_discount_1|equipment_discount_1|defense_points|block_station|improved_alcohol)/i, 40)
