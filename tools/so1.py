import os, json, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
# find bundles with SwitchRealmViewDescription in name or look in space-mainmenu / ui bundles
cands = [f for f in os.listdir(aa) if f.endswith('.bundle') and any(k in f.lower() for k in ['switchrealm','mainmenu','realm'])]
print(cands[:20])
targets = ['SwitchRealmViewDescription','ConfiscationDescription','PlotBuildingConfigs','RealmConfigs','TierDescriptions','RealmVersions','SwitchRealmLocalization']
res = []
for f in cands:
    p = os.path.join(aa,f)
    try:
        env = UnityPy.load(p)
    except Exception as e:
        continue
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour': continue
        try:
            t = obj.read_typetree()
        except Exception:
            continue
        nm = t.get('m_Name')
        if not nm: continue
        sc = (t.get('m_Script') or {}).get('m_PathID')
        # heuristic: object name in targets?
        if any(k.lower() in str(nm).lower() for k in ['switchrealm','confiscat','plotbuilding','realmversion','tierdesc','realmconfig']):
            print('---', f, obj.path_id, nm)
            print(json.dumps(t, ensure_ascii=False)[:1500])
