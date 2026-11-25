import re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
re_decl = re.compile(r'^(?:public |internal |private |protected )[^\n]*?\b(class|struct|interface|enum)\s+([A-Za-z0-9_<>`,\. ]+)')
for i,l in enumerate(lines):
    s=l.strip()
    if s.startswith('//'): continue
    m=re_decl.match(s)
    if m and m.group(2).strip() in ('TraderInventoryDescription','VendorTreeNodeDescription','UnlockedVendorTreeNodesModel','VendorTreeSettingsViewDescription','LocationNpcDescription'):
        print(m.group(2).strip(), i+1)
