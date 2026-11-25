import json, re, collections
d = json.load(open('out/l10n_en.json', encoding='utf-8'))
byid, bykey = {}, {}
for t in d['tables']:
    byid.update(t['byId']); bykey.update(t['byKey'])
keys = sorted(k for k in bykey if k)
groups = collections.Counter()
for k in keys:
    groups[k.split('_')[0]] += 1
print('top key prefixes:', groups.most_common(30))
print()
prefixes = ['builder','main_building','outbuilding','storage','shelv','collection_table','cargo',
            'defense','defence','plot','workbench','crypto','money_workbench','first_aid','raid',
            'compound','wall','car_bench','vehicle','settlement','location','building','upgrade','tax','rent']
sel = [k for k in keys if any(k==p or k.startswith(p+'_') for p in prefixes)]
print('selected keys:', len(sel))
out=[]
for k in sel:
    out.append('%-52s | %s' % (k, bykey[k].replace('\n','\\n')))
open('out/l10n_base_keys.txt','w',encoding='utf-8').write('\n'.join(out))
print('written out/l10n_base_keys.txt')
