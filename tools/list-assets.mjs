// List GitHub release assets for a repo/tag (bypasses rate-limited API by scraping HTML)
const targets = [
  ['Perfare/Il2CppDumper', 'v6.7.46'],
  ['AssetRipper/AssetRipper', '2.0.0'],
  ['SamboyCoding/Cpp2IL', null],
]

for (const [repo, tag] of targets) {
  const url = tag
    ? `https://github.com/${repo}/releases/expanded_assets/${tag}`
    : `https://github.com/${repo}/releases`
  try {
    const r = await fetch(url)
    const t = await r.text()
    const names = [...t.matchAll(/href="([^"]*\/releases\/download\/[^"]+)"/g)].map((m) => m[1])
    console.log('==', url, r.status, 'count=' + names.length)
    console.log(names.slice(0, 20).join('\n'))
  } catch (e) {
    console.log(url, 'ERR', e.message)
  }
}
