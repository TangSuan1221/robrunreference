import json, glob, os
d = json.load(open('out/l10n_en.json', encoding='utf-8'))
byid, bykey = {}, {}
for t in d['tables']:
    byid.update(t['byId']); bykey.update(t['byKey'])
def L(ls):
    """LocalizedString dict -> english text"""
    if not isinstance(ls, dict): return str(ls)
    kid = (ls.get('m_TableEntryReference') or {}).get('m_KeyId')
    return byid.get(str(kid), '?%s' % kid)
for f in sorted(glob.glob('out/so_dump/*/*.json')):
    j = json.load(open(f, encoding='utf-8'))
    tree = j['tree']; name = tree.get('m_Name')
    print('='*100)
    print('%s  (%s)' % (name, os.path.basename(f)))
    for k, v in tree.items():
        if k in ('m_GameObject','m_Enabled','m_Script','references'): continue
        if isinstance(v, list):
            print('  %s : list[%d]' % (k, len(v)))
            for i, e in enumerate(v):
                if not isinstance(e, dict): print('    [%d] %r' % (i, e)); continue
                ident = (e.get('<Identified>k__BackingField') or e.get('_id') or {})
                idv = ident.get('_id') if isinstance(ident, dict) else ident
                nm = e.get('<Name>k__BackingField')
                grp = None
                for kk, vv in e.items():
                    if isinstance(vv, dict) and '<Group>k__BackingField' in vv:
                        grp = vv['<Group>k__BackingField'].get('_guid')
                extra = ''
                if nm is not None: extra += ' name=%r' % L(nm)
                if grp: extra += ' group=%s' % grp[:8]
                keys = [kk for kk in e if not kk.startswith('_')][:6]
                if len(e) > 1 or extra:
                    print('    [%d] id=%-28s%s  fields=%s' % (i, idv, extra, [kk.replace('<','').replace('>k__BackingField','') for kk in e]))
                else:
                    print('    [%d] id=%s' % (i, idv))
        elif isinstance(v, dict):
            if 'm_TableEntryReference' in v:
                print('  %s : %r' % (k, L(v)))
            elif '_guid' in v or '_list' in v:
                print('  %s : %s' % (k, v))
            elif '_view' in v or '<Group>' in str(v):
                print('  %s : %s' % (k, {kk: (vv if not isinstance(vv,dict) else list(vv.keys())) for kk,vv in v.items()}))
            else:
                print('  %s : %s' % (k, json.dumps(v, ensure_ascii=False)[:200]))
        else:
            print('  %s : %r' % (k, v))
