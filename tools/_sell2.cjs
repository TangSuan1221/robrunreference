const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
for(const [k,v] of m){ if(/sell/i.test(k)&&!/_duplicate$/.test(k)) console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,140)) }
