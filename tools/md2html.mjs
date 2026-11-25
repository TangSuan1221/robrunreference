/**
 * 零依赖 markdown → 单文件 HTML 导出器。
 * 目的：绕过 dsh-better-sidebar 的渲染崩溃，让文档在任何浏览器里直接可读。
 * 支持：标题 / 表格 / 围栏代码 / 无序·有序列表（含缩进嵌套）/ 引用 / 分隔线 /
 *       粗体·斜体·行内代码·链接。
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { basename } from 'node:path'

const ROOT = 'C:/Users/Lenovo/Desktop/robrun'

const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

/** 行内渲染：先抽出 code span，再转义，再处理强调/链接，最后放回 code。 */
function inline(src) {
  const codes = []
  let s = src.replace(/`([^`]+)`/g, (_, c) => {
    codes.push(c)
    return `\u0000${codes.length - 1}\u0000`
  })
  s = esc(s)
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  s = s.replace(/(^|[^\w*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
  s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
  s = s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${esc(codes[Number(i)])}</code>`)
  return s
}

/** 按 | 切表格行，但跳过 code span 内的竖线。 */
function splitRow(line) {
  let s = line.trim()
  if (s.startsWith('|')) s = s.slice(1)
  if (s.endsWith('|')) s = s.slice(0, -1)
  const out = []
  let buf = ''
  let tick = 0
  for (const ch of s) {
    if (ch === '`') { tick ^= 1; buf += ch; continue }
    if (ch === '|' && tick === 0) { out.push(buf); buf = ''; continue }
    buf += ch
  }
  out.push(buf)
  return out.map((c) => c.trim())
}

const HEADING = /^(#{1,6})\s+(.*)$/
const FENCE = /^\s{0,3}(`{3,}|~{3,})(.*)$/
const HR = /^\s{0,3}(-{3,}|\*{3,}|_{3,})\s*$/
const UL = /^(\s*)[-*+]\s+(.*)$/
const OL = /^(\s*)\d+[.)]\s+(.*)$/
const QUOTE = /^\s{0,3}>\s?(.*)$/
const TABLE_SEP = /^\s*\|?[\s:|-]+\|[\s:|-]*$/

function renderMd(md, slugPrefix) {
  const lines = md.replace(/\r\n/g, '\n').split('\n')
  const out = []
  const toc = []
  let i = 0
  let h2 = 0

  while (i < lines.length) {
    const line = lines[i]

    // 围栏代码
    const fm = FENCE.exec(line)
    if (fm) {
      const fence = fm[1]
      const lang = fm[2].trim()
      const body = []
      i += 1
      while (i < lines.length) {
        const cm = FENCE.exec(lines[i])
        if (cm && cm[1][0] === fence[0] && cm[1].length >= fence.length) { i += 1; break }
        body.push(lines[i])
        i += 1
      }
      out.push(
        `<div class="codeblock">${lang ? `<span class="lang">${esc(lang)}</span>` : ''}<pre><code>${esc(body.join('\n'))}</code></pre></div>`,
      )
      continue
    }

    // 表格
    if (line.includes('|') && i + 1 < lines.length && TABLE_SEP.test(lines[i + 1])) {
      const head = splitRow(line)
      i += 2
      const rows = []
      while (i < lines.length && lines[i].includes('|') && lines[i].trim() !== '') {
        rows.push(splitRow(lines[i]))
        i += 1
      }
      out.push(
        '<div class="tablewrap"><table><thead><tr>' +
          head.map((c) => `<th>${inline(c)}</th>`).join('') +
          '</tr></thead><tbody>' +
          rows.map((r) => '<tr>' + r.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>').join('') +
          '</tbody></table></div>',
      )
      continue
    }

    // 标题
    const hm = HEADING.exec(line)
    if (hm) {
      const level = hm[1].length
      const text = hm[2].trim()
      const id = `${slugPrefix}-h${level}-${(h2 += 1)}`
      out.push(`<h${level} id="${id}">${inline(text)}</h${level}>`)
      if (level === 2 || level === 3) toc.push({ level, id, text })
      i += 1
      continue
    }

    // 分隔线
    if (HR.test(line)) { out.push('<hr>'); i += 1; continue }

    // 引用
    if (QUOTE.test(line)) {
      const buf = []
      while (i < lines.length && QUOTE.test(lines[i])) { buf.push(QUOTE.exec(lines[i])[1]); i += 1 }
      out.push(`<blockquote>${buf.map((b) => inline(b)).join('<br>')}</blockquote>`)
      continue
    }

    // 列表
    if (UL.test(line) || OL.test(line)) {
      const ordered = OL.test(line)
      const re = ordered ? OL : UL
      const items = []
      while (i < lines.length) {
        const m = re.exec(lines[i])
        if (!m) {
          // 缩进续行归入上一项
          if (items.length > 0 && /^\s{2,}\S/.test(lines[i])) {
            items[items.length - 1].text += '<br>' + inline(lines[i].trim())
            i += 1
            continue
          }
          break
        }
        const indent = Math.floor(m[1].length / 2)
        items.push({ indent, text: inline(m[2]) })
        i += 1
      }
      let html = ''
      let depth = 0
      const tag = ordered ? 'ol' : 'ul'
      for (const it of items) {
        while (depth < it.indent) { html += `<${tag}>`; depth += 1 }
        while (depth > it.indent) { html += `</${tag}>`; depth -= 1 }
        html += `<li>${it.text}</li>`
      }
      while (depth > 0) { html += `</${tag}>`; depth -= 1 }
      out.push(`<${tag} class="mdlist">${html}</${tag}>`)
      continue
    }

    // 空行
    if (line.trim() === '') { i += 1; continue }

    // 段落
    const buf = []
    while (
      i < lines.length &&
      lines[i].trim() !== '' &&
      !HEADING.test(lines[i]) &&
      !FENCE.test(lines[i]) &&
      !HR.test(lines[i]) &&
      !QUOTE.test(lines[i]) &&
      !UL.test(lines[i]) &&
      !OL.test(lines[i])
    ) {
      buf.push(lines[i])
      i += 1
    }
    if (buf.length > 0) out.push(`<p>${buf.map((b) => inline(b)).join('<br>')}</p>`)
  }

  return { html: out.join('\n'), toc }
}

const FILES = [
  '多人联机据点-详细策划案.md',
  '多人交互物占用-实现规格.md',
  '加工线评审-ROBRUN对照解答.md',
  '营地建造系统-可复刻设计说明.md',
  '基地建造-逆向分析.md',
  'base_catalog.md',
].filter((f) => existsSync(`${ROOT}/${f}`))

const docs = FILES.map((f, idx) => {
  const md = readFileSync(`${ROOT}/${f}`, 'utf8')
  const { html, toc } = renderMd(md, `d${idx}`)
  return { file: f, slug: `d${idx}`, html, toc, chars: md.length }
})

const nav = docs
  .map(
    (d) =>
      `<li class="doc"><a href="#${d.slug}">${esc(basename(d.file, '.md'))}</a><ul>` +
      d.toc
        .filter((t) => t.level === 2)
        .map((t) => `<li><a href="#${t.id}">${esc(t.text.replace(/[*`]/g, ''))}</a></li>`)
        .join('') +
      `</ul></li>`,
  )
  .join('')

const body = docs
  .map((d) => `<section id="${d.slug}">${d.html}</section>`)
  .join('\n<hr class="docsep">\n')

const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ROB RUN 逆向文档</title>
<style>
:root{--bg:#0f1115;--panel:#161a21;--fg:#e6e9ef;--dim:#9aa4b2;--line:#262c36;--acc:#6ea8fe;--code:#1b2029}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.75 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
#wrap{display:grid;grid-template-columns:290px minmax(0,1fr);min-height:100vh}
nav{position:sticky;top:0;height:100vh;overflow:auto;background:var(--panel);border-right:1px solid var(--line);padding:16px 12px;font-size:13px}
nav ul{list-style:none;margin:0;padding-left:12px}
nav>ul{padding-left:0}
nav li.doc{margin:10px 0 4px}
nav li.doc>a{font-weight:600;color:var(--fg);text-decoration:none;font-size:13.5px}
nav a{color:var(--dim);text-decoration:none;display:block;padding:2px 4px;border-radius:4px}
nav a:hover{color:var(--acc);background:#1d2430}
main{padding:28px 40px 120px;max-width:1080px}
section{scroll-margin-top:20px}
h1{font-size:26px;border-bottom:2px solid var(--line);padding-bottom:10px;margin-top:8px}
h2{font-size:20px;margin-top:36px;border-left:4px solid var(--acc);padding-left:10px}
h3{font-size:16.5px;margin-top:26px;color:#cdd6e4}
h4{font-size:15px;color:#cdd6e4}
p{margin:10px 0}
a{color:var(--acc)}
code{background:var(--code);padding:1.5px 5px;border-radius:4px;font:13px/1.5 ui-monospace,Consolas,monospace;color:#ffd68a}
.codeblock{position:relative;margin:14px 0;background:var(--code);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.codeblock .lang{position:absolute;right:8px;top:6px;font-size:11px;color:var(--dim);background:#232a35;padding:1px 6px;border-radius:4px}
pre{margin:0;padding:14px 16px;overflow:auto}
pre code{background:none;padding:0;color:#d6e2f0;font-size:12.5px;line-height:1.65}
.tablewrap{overflow:auto;margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#1c2230;font-weight:600;white-space:nowrap}
tr:nth-child(even) td{background:#141922}
blockquote{margin:14px 0;padding:10px 14px;border-left:3px solid #3d4a5e;background:var(--panel);color:#c3cbd8}
blockquote code{color:#ffd68a}
hr{border:0;border-top:1px solid var(--line);margin:32px 0}
hr.docsep{border-top:3px double #2f3947;margin:60px 0}
.mdlist{margin:10px 0;padding-left:24px}
.mdlist li{margin:4px 0}
ul.mdlist ul,ol.mdlist ol{margin:4px 0}
@media(max-width:900px){#wrap{grid-template-columns:1fr}nav{position:static;height:auto}}
</style></head>
<body><div id="wrap">
<nav><div style="color:var(--dim);font-size:11px;letter-spacing:.08em;margin-bottom:6px">ROB RUN · REA 逆向</div><ul>${nav}</ul></nav>
<main>${body}</main>
</div></body></html>`

writeFileSync(`${ROOT}/docs.html`, html, 'utf8')
console.log('docs.html written')
for (const d of docs) {
  const t = (d.html.match(/<table>/g) || []).length
  const p = (d.html.match(/<pre>/g) || []).length
  const h = (d.html.match(/<h2 /g) || []).length
  console.log(`  ${d.file}: ${d.chars} chars → tables=${t} codeblocks=${p} h2=${h} toc=${d.toc.length}`)
}
console.log('total html bytes =', Buffer.byteLength(html, 'utf8'))
