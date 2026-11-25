import os, sys, json
sys.path.insert(0, r'C:\Users\糖蒜\Desktop\robrun_reference\tools\pylib')
import UnityPy

aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa, 'scriptableobjects_assets_all.bundle')
env = UnityPy.load(p)
want = {5244587876244765392, -3649879233042651237, 2859703315750441957}

def flat(t, prefix=''):
    out = []
    for k, v in t.items():
        if isinstance(v, dict):
            out.extend(flat(v, prefix + k + '.'))
        elif isinstance(v, list):
            out.append((prefix + k, 'list[%d]' % len(v)))
            for i, it in enumerate(v[:6]):
                if isinstance(it, dict):
                    out.extend(flat(it, prefix + k + '[%d].' % i))
                else:
                    out.append((prefix + k + '[%d]' % i, it))
        else:
            out.append((prefix + k, v))
    return out

for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    pid = obj.path_id if obj.path_id in want else (obj.path_id - (1 << 64) if obj.path_id - (1 << 64) in want else None)
    if pid is None:
        continue
    t = obj.read_typetree()
    print('=====', t.get('m_Name'), 'pathid', pid)
    for k, v in flat(t):
        if 'm_GameObject' in k or 'm_Script' in k:
            continue
        if isinstance(v, (int, float, bool, str)):
            print('  %s = %r' % (k, v))
