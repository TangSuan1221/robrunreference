import json, UnityPy
UnityPy.config.FALLBACK_UNITY_VERSION = "6000.3.18f1"
env = UnityPy.load(r"D:\SteamLibrary\steamapps\common\Rob Run\ROB RUN_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle")
for obj in env.objects:
    if obj.type.name != 'MonoBehaviour': continue
    t = obj.read_typetree()
    print('===', obj.path_id, t.get('m_Name'))
    for k,v in t.items():
        if isinstance(v,(list,dict)):
            print('  ',k, type(v).__name__, len(v))
        else:
            print('  ',k,'=',repr(v)[:120])
    # drill into m_TableData
    td = t.get('m_TableData')
    if isinstance(td, list) and td:
        print('  m_TableData[0] keys:', list(td[0].keys()) if isinstance(td[0],dict) else type(td[0]))
        print('  m_TableData[0] sample:', json.dumps(td[0], ensure_ascii=False)[:600])
    ent = t.get('m_Entries')
    if isinstance(ent, list) and ent:
        print('  m_Entries[0]:', json.dumps(ent[0], ensure_ascii=False)[:600])
