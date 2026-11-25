// Simple downloader: node tools/dl.mjs <url> <outfile>
import { createWriteStream } from 'node:fs'
import { Readable } from 'node:stream'
import { pipeline } from 'node:stream/promises'

const [url, out] = process.argv.slice(2)
if (!url || !out) {
  console.error('usage: node dl.mjs <url> <outfile>')
  process.exit(1)
}
const r = await fetch(url, { redirect: 'follow' })
if (!r.ok) {
  console.error('HTTP', r.status, url)
  process.exit(1)
}
await pipeline(Readable.fromWeb(r.body), createWriteStream(out))
console.log('OK', out, (await import('node:fs')).statSync(out).size)
