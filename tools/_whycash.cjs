const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=45)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,240));if(++n>=lim)break}}}
p("A. 出城/离开/边界", /leave|exit|border/i, 45)
p("B. 没收/失去/丢失", /confiscat|lose|lost|los(e|ing)_|seiz/i, 45)
p("C. 藏钱/货币/现金保管", /hide.*curr|curr.*hide|hide_|stash|dirty_cash/i, 35)
p("D. 罪犯身份离开城市", /robber.*(leave|exit|city)|criminal.*(leave|exit|city)|mask/i, 30)
