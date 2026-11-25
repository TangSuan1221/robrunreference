import os, json, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,'scriptableobjects_assets_all.bundle')
env = UnityPy.load(p)
want = {7245226053162067993, 7586590884206883568}
def flat(t, prefix=''):
    out={}
    for k,v in t.items():
        if isinstance(v, dict):
            out.update(flat(v, prefix+k+'.'))
        elif isinstance(v, list):
            out[prefix+k] = f'list[{len(v)}]'
        else:
            out[prefix+k]=v
    return out
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    if obj.path_id not in want: continue
    t = obj.read_typetree()
    print('=====', t.get('m_Name'))
    f = flat(t)
    for k,v in f.items():
        if 'm_GameObject' in k or 'm_Script' in k: continue
        if isinstance(v,(int,float,bool,str)):
            print(f'  {k} = {v}')
