const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
for(const [k,v] of m){ if(/^(crypto_1|farm_1|lab_1|weapon_discount_1|equipment_discount_1|defense_points|block_station|improved_alcohol|car_garage_0|workshop_1|crypto_farm_1|meth_lab_1|narco_farm_1|storage_1)/i.test(k)&&/_name$|_description$/.test(k)) console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,160)) }
