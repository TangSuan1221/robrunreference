import os, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
p = os.path.join(aa,"scriptableobjects_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoScript': continue
    try:
        d = obj.read()
        print(obj.path_id, repr(getattr(d,'m_ClassName',None)), repr(getattr(d,'m_Namespace',None)), repr(getattr(d,'m_AssemblyName',None)))
    except Exception as e:
        print('ERR', obj.path_id, e)
