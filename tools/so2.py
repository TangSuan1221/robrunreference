import os, json, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
out = os.path.join(ws,'out','so_index.tsv')
names = {}
for f in sorted(os.listdir(aa)):
    if not f.endswith('.bundle'): continue
    if not any(k in f for k in ['space-mainmenu_assets_all','space-realm_assets_all','scriptableobjects_assets_all','space-global_assets_all','inbuild_assets_all']): continue
    p = os.path.join(aa,f)
    try: env = UnityPy.load(p)
    except Exception as e: continue
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour': continue
        try: t = obj.read_typetree()
        except Exception: continue
        nm = t.get('m_Name')
        if nm:
            names.setdefault(str(nm), (f, obj.path_id))
print('names', len(names))
with open(out,'w',encoding='utf-8') as o:
    for k,(f,pid) in sorted(names.items()):
        o.write(f"{k}\t{f}\t{pid}\n")
for k in sorted(names):
    if any(q in k.lower() for q in ['switchrealm','confisc','realmconfig','tierdesc','realmversion','switch']):
        print(k, names[k])
