import json, glob, os
d = json.load(open('out/l10n_en.json', encoding='utf-8'))
byid, bykey = {}, {}
for t in d['tables']:
    byid.update(t['byId']); bykey.update(t['byKey'])
def L(ls):
    if not isinstance(ls, dict): return str(ls)
    kid = (ls.get('m_TableEntryReference') or {}).get('m_KeyId')
    return byid.get(str(kid), '?%s' % kid)
for f in glob.glob('out/so_dump/BuilderGroupEnumViewDescriptions/*.json'):
    j = json.load(open(f, encoding='utf-8')); tree = j['tree']
    print('SO:', tree.get('m_Name'), ' pid=', j['path_id'])
    lst = tree.get('<List>k__BackingField') or []
    print('groups:', len(lst))
    for e in lst:
        print('  id=%-34s guid=%s  title=%r' % (
            (e.get('<Id>k__BackingField') or ''),
            (e.get('<Guid>k__BackingField') or '')[:36],
            L(e.get('<Title>k__BackingField'))))
