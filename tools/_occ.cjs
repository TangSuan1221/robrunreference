const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=60)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," ").slice(0,220));if(++n>=lim)break}}}
p("A. busy/occupied/in_use", /busy|occup|in_use|inuse|already_used|someone|another_player|other_player/i, 60)
p("B. wait/free ready", /_wait|wait_|_free|not_available|unavailable|cooldown/i, 50)
p("C. interact/hold/long", /interact|hold_|prolong|long_press|taking|progress/i, 55)
p("D. hide object 占用", /hide_?object|hideobject|cupboard|has_person/i, 30)
p("E. seat/driver/vehicle", /seat|driver|passenger|board|enter_car|occup/i, 30)
