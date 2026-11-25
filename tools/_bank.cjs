const fs=require("fs");const j=JSON.parse(fs.readFileSync("out/l10n_en.json","utf8"));const m=new Map();
for(const tb of j.tables) for(const [k,v] of Object.entries(tb.byKey||{})) m.set(k,v);
const clean=s=>String(s).replace(/<[^>]*>/g,"");
const p=(t,re,lim=45)=>{console.log("\n##### "+t);let n=0;for(const [k,v] of m){if(re.test(k)&&!/_duplicate$/.test(k)){console.log("["+k+"] "+clean(v).replace(/\n/g," | ").slice(0,180));if(++n>=lim)break}}}
p("A. 银行账户", /bank_account|open_bank|bank_/i, 40)
p("B. 提现 / ATM / 存钱", /atm|withdraw|deposit/i, 30)
p("C. 赚钱途径（job/salary/reward）", /^global_map_job|job_|salary|_reward\b/i, 35)
