const urls = [
  'https://github.com/lxraa/Il2CppDumper/releases/expanded_assets/v6.7.46-lxraa.1',
  'https://github.com/lxraa/Il2CppDumper/releases/tag/v6.7.46-lxraa.1',
]
for (const u of urls) {
  try {
    const r = await fetch(u, { signal: AbortSignal.timeout(20000) })
    const t = await r.text()
    const names = [...t.matchAll(/\/releases\/download\/[^"'\s<>]+/g)].map((m) => m[0])
    console.log('==', u, r.status, 'hits=' + names.length)
    console.log([...new Set(names)].join('\n'))
  } catch (e) {
    console.log('==', u, 'ERR', e.message)
  }
}
