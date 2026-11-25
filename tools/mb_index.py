import os, sys, json, time, glob
import UnityPy
from collections import Counter
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
outp = os.path.join(ws,'out','mb_index.jsonl')
done = set()
if os.path.exists(outp):
    for line in open(outp,encoding='utf-8'):
        try: done.add(json.loads(line)['bundle'])
        except: pass
bundles = sorted(glob.glob(os.path.join(aa,'*.bundle')))
print('bundles', len(bundles), 'done', len(done), flush=True)
f = open(outp,'a',encoding='utf-8')
t0=time.time()
for i,p in enumerate(bundles):
    b = os.path.basename(p)
    if b in done: continue
    try:
        env = UnityPy.load(p)
        cnt = Counter()
        names = []
        for obj in env.objects:
            if obj.type.name!='MonoBehaviour': continue
            try:
                t = obj.read_typetree()
                sn = t.get('m_Script') or {}
                nm = sn.get('m_Name') or '?'
                cnt[nm]+=1
                mname = t.get('m_Name')
                if mname: names.append([nm, mname])
            except Exception:
                cnt['<unreadable>']+=1
        rec = {'bundle': b, 'size': os.path.getsize(p), 'types': dict(cnt), 'assets': names[:4000]}
        f.write(json.dumps(rec, ensure_ascii=False)+'\n'); f.flush()
        print(f'{i+1}/{len(bundles)} {b} {dict(cnt.most_common(5))}', flush=True)
    except Exception as e:
        f.write(json.dumps({'bundle':b,'error':str(e)}, ensure_ascii=False)+'\n'); f.flush()
        print('ERR', b, e, flush=True)
print('done in', round(time.time()-t0,1), flush=True)
