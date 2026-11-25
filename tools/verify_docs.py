import os, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference\docs_reverse"
files = []
for root, dirs, fs in os.walk(ws):
    for f in fs:
        if f.endswith('.md'):
            files.append(os.path.join(root,f))
print('files', len(files))
total = 0
for p in sorted(files):
    txt = open(p, encoding='utf-8').read()
    total += len(txt)
    h2 = len(re.findall(r'^## ', txt, re.M))
    h3 = len(re.findall(r'^### ', txt, re.M))
    links = re.findall(r'\]\(([^)]+\.md)\)', txt)
    broken = []
    for l in links:
        if l.startswith('http'): continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), l))
        if not os.path.exists(target):
            broken.append(l)
    rel = os.path.relpath(p, ws)
    if broken:
        print('BROKEN', rel, broken)
    print(f'{len(txt):6d} chars  h2={h2:2d} h3={h3:2d}  {rel}')
print('total chars', total)
