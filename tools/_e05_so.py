import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pylib'))
import UnityPy

ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
bundle = sys.argv[1] if len(sys.argv) > 1 else 'scriptableobjects_assets_all.bundle'
want = set(int(x) for x in sys.argv[2].split(',')) if len(sys.argv) > 2 else set()
p = os.path.join(aa, bundle)
env = UnityPy.load(p)

def flat(t, prefix=''):
    out = {}
    for k, v in t.items():
        if isinstance(v, dict):
            out.update(flat(v, prefix + k + '.'))
        elif isinstance(v, list):
            out[prefix + k] = 'list[%d]' % len(v)
        else:
            out[prefix + k] = v
    return out

for obj in env.objects:
    if obj.type.name != 'MonoBehaviour':
        continue
    if want and obj.path_id not in want:
        continue
    try:
        t = obj.read_typetree()
    except Exception as ex:
        print('ERR', obj.path_id, ex)
        continue
    print('===== pathid', obj.path_id, 'name', t.get('m_Name'))
    f = flat(t)
    for k, v in f.items():
        if 'm_GameObject' in k or 'm_Script' in k:
            continue
        if isinstance(v, (int, float, bool)):
            print('  %s = %s' % (k, v))
        elif isinstance(v, str):
            s = v.replace('\n', '\\n')
            print('  %s = "%s"' % (k, s[:200]))
