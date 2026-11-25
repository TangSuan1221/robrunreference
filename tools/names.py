import os, re
WS = r"C:\Users\糖蒜\Desktop\robrun_reference"
for g in ['realm_sector','ownership_land','plot_entity','map_ui','builder','defense','economy','survival','meta']:
    p = os.path.join(WS,'out','slices', g+'.txt')
    names=[]
    for line in open(p,encoding='utf-8'):
        m = re.match(r'^(public|internal|private|protected)[^\n]*\b(class|struct|interface|enum)\s+([A-Za-z0-9_<>`, ]+?)\s*(?::|$)', line.strip())
        if m:
            nm = m.group(3).strip()
            names.append(nm)
    print(f"=== {g} ({len(names)}) ===")
    print(", ".join(names))
