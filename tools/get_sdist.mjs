// Download an sdist and extract its top-level python package(s) into tools/pylib
import { mkdirSync, writeFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'

const pkg = process.argv[2]
const r = await fetch(`https://pypi.org/pypi/${pkg}/json`, { signal: AbortSignal.timeout(30000) })
const meta = await r.json()
const sdist = (meta.urls || []).find((u) => u.filename.endsWith('.tar.gz') || u.filename.endsWith('.zip'))
if (!sdist) {
  console.log('no sdist', pkg)
  process.exit(1)
}
mkdirSync('tools/sdist', { recursive: true })
const path = `tools/sdist/${sdist.filename}`
const bin = await fetch(sdist.url, { signal: AbortSignal.timeout(120000) })
writeFileSync(path, Buffer.from(await bin.arrayBuffer()))
console.log('downloaded', path)
