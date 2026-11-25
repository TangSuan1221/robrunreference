const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const c=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)){console.log("["+k+"] "+c(v).replace(/\n/g," ").slice(0,200));if(++n>=lim)break}}}
p("A. homeless / no base", /homeless|no_home|no_base|without_base|haven.t|nowhere|vagrant/i, 30)
p("B. respawn / spawn", /respawn|spawn_point|death_screen/i, 40)
p("C. stash / storage only at base", /only_at|at_your_base|at_home|your_home|your_base|territory/i, 45)
p("D. drop on death / lose", /lose_|lost_|drop_|confiscat|on_death/i, 45)
