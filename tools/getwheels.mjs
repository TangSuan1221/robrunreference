// Resolve and download pure/cp311 win_amd64 wheels from PyPI (avoids pip's hang)
import { mkdirSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'

const out = 'tools/wheels'
mkdirSync(out, { recursive: true })

const PY = 'cp311'
const ABIS = ['cp311-cp311', 'cp311-abi3', 'cp311-none']
const PLATS = ['win_amd64', 'any']

function score(name) {
  if (!name.endsWith('.whl') && !name.endsWith('.tar.gz')) return -1
  if (name.endsWith('.tar.gz')) return 1
  const m = name.match(/-(cp\d+|py\d+|py3)-([^-]+)-([^-]+)\.whl$/)
  if (!m) return 1
  const [, py, abi, plat] = m
  const pyOk = py === PY || py === 'py3'
  if (!pyOk) return -1
  const abiOk = abi === 'abi3' || abi === 'none' || abi === PY
  if (!abiOk) return -1
  const platOk = PLATS.includes(plat)
  if (!platOk) return -1
  let s = 10
  if (plat === 'win_amd64') s += 5
  if (py === PY) s += 3
  if (abi === 'abi3') s += 1
  return s
}

async function pypi(name) {
  const r = await fetch(`https://pypi.org/pypi/${name}/json`, { signal: AbortSignal.timeout(30000) })
  if (!r.ok) throw new Error(`${name}: HTTP ${r.status}`)
  return r.json()
}

const seen = new Set()
const queue = process.argv.slice(2)
const picked = []

while (queue.length) {
  const name = queue.shift()
  const key = name.toLowerCase()
  if (seen.has(key)) continue
  seen.add(key)
  const meta = await pypi(name)
  const urls = meta.urls || []
  const cands = urls
    .map((u) => ({ u, s: score(u.filename) }))
    .filter((c) => c.s >= 0)
    .sort((a, b) => b.s - a.s)
  if (!cands.length) {
    console.log('NO WHEEL for', name, urls.map((u) => u.filename).join(','))
    continue
  }
  const best = cands[0].u
  const path = join(out, best.filename)
  const r = await fetch(best.url, { signal: AbortSignal.timeout(120000) })
  const buf = Buffer.from(await r.arrayBuffer())
  writeFileSync(path, buf)
  picked.push(best.filename)
  console.log('GOT', best.filename, buf.length)
  // parse metadata for Requires-Dist from the JSON info
  const reqs = (meta.info.requires_dist || []).filter((d) => !d.includes('extra =='))
  for (const d of reqs) {
    const depName = d.split(/[ ;<>=!~[]/)[0].trim()
    if (depName && !seen.has(depName.toLowerCase())) queue.push(depName)
  }
  console.log('  deps:', reqs.join(' | '))
}
console.log('DONE', picked.length, 'wheels')
