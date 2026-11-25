const BASE='http://127.0.0.1:59285'
for (const p of ['/sidebar/bundle/editor.js','/sidebar/bundle/terminal.js','/sidebar/bundle/mermaid.js','/sidebar/bundle/client-editor.js']) {
  try {
    const r = await fetch(BASE+p, { method:'GET' })
    const len = (await r.arrayBuffer()).byteLength
    console.log(`${p}  HTTP ${r.status}  bytes=${len}  ct=${r.headers.get('content-type')}  etag=${r.headers.get('etag')}`)
  } catch (e) { console.log(`${p}  FAILED ${e}`) }
}
