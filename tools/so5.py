import os, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
targets = ['MapViewDescription','MapMarkerViewDescriptions','LocationViewDescriptions','RealmGridViewDescription']
found={}
for f in sorted(os.listdir(aa)):
    if not f.endswith('.bundle'): continue
    p=os.path.join(aa,f)
    try: env=UnityPy.load(p)
    except Exception: continue
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour': continue
        try: t=obj.read_typetree()
        except Exception: continue
        nm=t.get('m_Name')
        if nm in targets and nm not in found:
            found[nm]=(f,obj.path_id,t)
    if all(k in found for k in targets): break
for k,(f,pid,t) in found.items():
    print('=====',k,f,pid)
    def flat(d,pre=''):
        out={}
        for kk,vv in d.items():
            if isinstance(vv,dict): out.update(flat(vv,pre+kk+'.'))
            elif isinstance(vv,list): out[pre+kk]=f'list[{len(vv)}]'
            else: out[pre+kk]=vv
        return out
    fl=flat(t)
    for kk,vv in fl.items():
        if 'm_GameObject' in kk or 'm_Script' in kk or 'AssetGUID' in kk: continue
        if isinstance(vv,(int,float,bool,str)):
            print(' ',kk,'=',vv)
