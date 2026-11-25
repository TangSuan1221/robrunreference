const fs=require("fs");const readline=require("readline");
const rl=readline.createInterface({input:fs.createReadStream("out/mb_all.jsonl")});
const seen=new Map();
rl.on("line",l=>{let o;try{o=JSON.parse(l)}catch(e){return}
 const s=o.script||o.Script||o.className||"";
 if(/StringTable|SharedTableData/i.test(s)){const k=(o.bundle||"?")+" :: "+s+" :: "+(o.name||"");seen.set(k,(seen.get(k)||0)+1)}});
rl.on("close",()=>{for(const [k,v] of seen) console.log(v+"x  "+k)});
