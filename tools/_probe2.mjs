const BASE='http://127.0.0.1:59285'
const SID='session-6e427a56-bb37-4d42-85dd-81f05572a323'
const ws='C:\\\\Users\\\\Lenovo\\\\Desktop\\\\robrun'
async function call(method,payload){
  const r=await fetch(BASE+'/sidebar/api/'+method,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({sessionId:SID,cwd:ws,...payload})})
  let b; try{b=await r.json()}catch{b=null}
  return {method,status:r.status,body:b}
}
const md=ws+'\\\\营地建造系统-可复刻设计说明.md'
for(const [m,p] of [['session.cwd',{}],['fs.tree',{path:ws}],['fs.read',{path:md}],['fs.read',{path:ws+'\\\\tools\\\\ns_dump.py'}]]){
  const o=await call(m,p)
  console.log('\n=== '+m+'  HTTP '+o.status)
  const v=o.body?.value
  if(o.body?.error) console.log('  ERROR '+JSON.stringify(o.body.error))
  if(v){ if(Array.isArray(v.entries)) console.log('  entries='+v.entries.length+' first='+JSON.stringify(v.entries.slice(0,2)))
         if(typeof v.content==='string') console.log('  kind='+v.kind+' len='+v.content.length+' head='+JSON.stringify(v.content.slice(0,60)))
         if(v.root) console.log('  root='+v.root) }
}
