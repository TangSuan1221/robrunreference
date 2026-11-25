import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
re_td = re.compile(r'// TypeDefIndex: (\d+)')
re_ns = re.compile(r'^// Namespace: (.*)$')
re_decl = re.compile(r'^(?:public |internal |private |protected )')
tds=set(); nss=set(); decls=0; rvas=0; fields=0
for line in open(p, encoding='utf-8', errors='replace'):
    s=line.rstrip()
    m=re_td.search(s)
    if m: tds.add(m.group(1))
    m=re_ns.match(s)
    if m: nss.add(m.group(1).strip())
    if re_decl.match(s.strip()) and ('class ' in s or 'struct ' in s or 'interface ' in s or 'enum ' in s):
        decls+=1
    if s.strip().startswith('// RVA:'): rvas+=1
print('unique TypeDefIndex', len(tds))
print('namespaces', len(nss))
print('decls', decls, 'rvas', rvas)
