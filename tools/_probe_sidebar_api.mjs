// 直连 sidebar host API，判断是后端报错还是前端渲染崩溃
const BASE = 'http://127.0.0.1:59285'

async function call(method, payload) {
  const url = `${BASE}/sidebar/api/${method}`
  let r, body
  try {
    r = await fetch(url, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (e) {
    return { method, transport: 'FAILED', error: String(e) }
  }
  try { body = await r.json() } catch { body = await r.text().catch(() => '<unreadable>') }
  return { method, status: r.status, body }
}

const out = []
out.push(await call('session.cwd', {}))
const ws = 'C:\\Users\\Lenovo\\Desktop\\robrun'
const md = ws + '\\营地建造系统-可复刻设计说明.md'
out.push(await call('fs.tree', { path: ws }))
out.push(await call('fs.read', { path: md }))
out.push(await call('fs.read', { path: ws + '\\tools\\ns_dump.py' }))

for (const o of out) {
  console.log('\n=== ' + o.method)
  if (o.transport) { console.log('  ' + o.transport + ': ' + o.error); continue }
  console.log('  HTTP ' + o.status)
  let b = o.body
  if (b && typeof b === 'object') {
    // 只打印骨架，避免刷屏
    const clone = JSON.parse(JSON.stringify(b))
    if (clone.value) {
      if (Array.isArray(clone.value.entries)) {
        clone.value.entries = `[${clone.value.entries.length} entries] first: ` + JSON.stringify(clone.value.entries.slice(0, 3))
      }
      if (typeof clone.value.content === 'string') {
        clone.value.content = `<${clone.value.content.length} chars> ` + JSON.stringify(clone.value.content.slice(0, 80))
      }
    }
    console.log('  ' + JSON.stringify(clone).slice(0, 900))
  } else {
    console.log('  ' + String(b).slice(0, 400))
  }
}
