import re, os, sys
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
sl = os.path.join(ws,'out','slices')
def load(name):
    out=[]
    for g in os.listdir(sl):
        p=os.path.join(sl,g)
        txt=open(p,encoding='utf-8',errors='replace').read()
        # find class block
        m=re.search(r'^(?:public|internal|private|protected)[^\n]*\b(?:class|struct|interface|enum)\s+'+re.escape(name)+r'\b[^\n]*\n\{', txt, re.M)
        if m:
            start=m.start()
            # find matching end brace at column 0
            i=txt.find('\n}', m.end())
            out.append(txt[start:i+2])
    return out
for nm in sys.argv[1:]:
    blocks=load(nm)
    print('#'*20, nm, 'found', len(blocks))
    for b in blocks:
        # strip generated noise
        lines=b.split('\n')
        keep=[]
        skip=False
        for l in lines:
            if '// Fields' in l or '// Properties' in l or '// Methods' in l:
                keep.append(l); continue
            if '[CompilerGenerated]' in l or '[NullableContext' in l or '[Nullable(' in l:
                continue
            if 'k__BackingField' in l: continue
            if re.search(r'public .* (get_|set_)', l): continue
            if re.match(r'\s*// RVA:', l): continue
            if re.match(r'\s*public (void|int|long|bool|float|string|IReadOnly|List|Dictionary|ValueTuple).*\(\) \{ \}', l): continue
            keep.append(l)
        print('\n'.join(keep))
