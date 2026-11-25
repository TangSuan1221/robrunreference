import json, glob, os, collections
d = json.load(open('out/l10n_en.json', encoding='utf-8'))
byid, bykey = {}, {}
for t in d['tables']:
    byid.update(t['byId']); bykey.update(t['byKey'])
def L(ls):
    if not isinstance(ls, dict): return str(ls)
    kid = (ls.get('m_TableEntryReference') or {}).get('m_KeyId')
    return byid.get(str(kid), '?%s' % kid)
G = {  # group guid -> title
 'ae8bbb84':'Basic Structures','4c38dbcc':'Additional Structures','ef9d803c':'Equipment',
 '900f7d42':'Grow Tables','8ba59963':'Furniture','2fd96a00':'Containers','7654dad5':'Racks',
 'cdcfea87':'Opening speed boost','8081d4ac':'Additional Slots','e66d7f6a':'Additional collections',
 '36d8aeb6':'Laundering speed boost','fc5d0b8f':'Special Modules','d09f5679':'Defense Improvement',
 '31227508':'Repacking speed boost','0eed02ab':'Additional Slots','b3e3ab8c':'Process speed boost',
 '1331bab4':'Modules'}
def short(g): return G.get(str(g)[:8], str(g)[:8]) if g else None

def walk(o, path=''):
    """yield (path, key, value) leaf-ish for interesting fields"""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '[%d]' % i)
    else:
        yield path, o

for f in sorted(glob.glob('out/so_dump2/*/*.json')):
    j = json.load(open(f, encoding='utf-8')); tree = j['tree']
    print('='*104)
    print('## %s   pid=%s' % (tree.get('m_Name'), j['path_id']))
    for k, v in tree.items():
        if k in ('m_GameObject','m_Enabled','m_Script','references'): continue
        if isinstance(v, list):
            print('  %s : list[%d]' % (k, len(v)))
            for i, e in enumerate(v):
                if not isinstance(e, dict):
                    print('    [%d] %r' % (i, e)); continue
                iid = (e.get('<Identified>k__BackingField') or {}).get('_id') if isinstance(e.get('<Identified>k__BackingField'), dict) else None
                if iid is None: iid = e.get('_id') or e.get('<Id>k__BackingField') or e.get('<IdInternal>k__BackingField')
                nm = e.get('<Name>k__BackingField')
                ln = ['    [%d] id=%-30s' % (i, iid)]
                if nm is not None: ln.append('name=%r' % L(nm))
                # group / guid / sprite / type hints
                for kk, vv in e.items():
                    if not isinstance(vv, dict): continue
                    if '<Group>k__BackingField' in vv:
                        ln.append('group=%s' % short(vv['<Group>k__BackingField'].get('_guid')))
                    if '<MiniTooltipTitle>k__BackingField' in vv:
                        ln.append('tip=%r' % L(vv['<MiniTooltipTitle>k__BackingField']))
                rest = [kk.replace('<','').replace('>k__BackingField','') for kk in e
                        if kk not in ('_id','<Identified>k__BackingField','<Name>k__BackingField')]
                if rest: ln.append('fields=%s' % rest)
                print('  '.join(ln))
        elif isinstance(v, dict):
            if 'm_TableEntryReference' in v: print('  %s : %r' % (k, L(v)))
            elif '_localizedString' in v: print('  %s : %r' % (k, L(v['_localizedString'])))
            elif '_list' in v: print('  %s : %s' % (k, [short(x) for x in v['_list']]))
            elif '_guid' in v: print('  %s : group=%s' % (k, short(v['_guid'])))
            elif '<Group>k__BackingField' in v:
                print('  %s : group=%s tip=%r' % (k, short(v['<Group>k__BackingField'].get('_guid')),
                      L(v.get('<MiniTooltipTitle>k__BackingField') or {})))
            else: print('  %s : %s' % (k, json.dumps(v, ensure_ascii=False)[:160]))
        else:
            print('  %s : %r' % (k, v))
