const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,230));if(++n>=lim)break}}}
p("A. lifetime / 寿命", /lifetime/i, 30)
p("B. restart / maintenance / shutdown", /restart|shutdown|maintenance/i, 30)
p("C. day/week/season/wipe", /week|\bday\b|season|wipe|expire|reset/i, 45)
p("D. realm_ 全部", /^realm_/i, 60)
