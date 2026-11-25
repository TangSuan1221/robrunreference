import os, struct, UnityPy
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
aa = r"C:\game\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64"
for name in ["localization-assets-shared_assets_all.bundle","localization-locales_assets_all.bundle"]:
    p = os.path.join(aa,name)
    print('=====', name, os.path.getsize(p))
    env = UnityPy.load(p)
    for obj in env.objects:
        if obj.type.name in ('MonoBehaviour','ScriptableObject'):
            d = obj.read()
            print(' ', obj.type.name, obj.path_id, getattr(d,'m_Name','?'))

p = os.path.join(aa, "localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
env = UnityPy.load(p)
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw = obj.get_raw_data()
    d = obj.read()
    name = d.m_Name
    print('=== table', name)
    # parse: header 12 bytes + name string + script pptr 8 bytes
    off = 12
    ln = struct.unpack_from('<i', raw, off)[0]; off += 4 + ln
    off = (off + 3) & ~3
    off += 8  # script
    # LocaleIdentifier: string then int64
    ln = struct.unpack_from('<i', raw, off)[0]; off += 4 + ln
    off = (off+3)&~3
    # locale id long
    lid = struct.unpack_from('<q', raw, off)[0]; off += 8
    # shared data pptr
    sh = struct.unpack_from('<iq', raw, off); off += 8
    # metadata collection: count + entries (probably 1 int for count?)
    # dump next 32 bytes
    print(' localeId', lid, 'shared', sh, 'next', raw[off:off+32].hex(' '))
    # try: metadata as int count=0 then list count
    cnt = struct.unpack_from('<i', raw, off)[0]; off += 4
    print(' metaCount?', cnt)
