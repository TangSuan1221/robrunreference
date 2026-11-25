import json
d = json.load(open('out/l10n_en.json', encoding='utf-8'))
byid, bykey, id2key = {}, {}, d['id2key']
for t in d['tables']:
    byid.update(t['byId']); bykey.update(t['byKey'])
ids = {
 233478058996072448:'home_0 Name', 233478081553039360:'home_1 Name', 280141695060103168:'home_2 Name',
 245772851524837376:'BuilderName',
 7376271090200922230:'FirstAidCabinetsSlot tooltip', 7470816146856923267:'StoragesSlot tooltip',
 7296098114520795685:'ShelvesSlot tooltip', 7476280879215071493:'CollectionTableSlot tooltip',
}
for k,v in ids.items():
    print('%-34s %-22s id2key=%r  text=%r' % (v, k, id2key.get(str(k)), byid.get(str(k))))
print()
print('=== entries matching BUILD / WORKBENCH / PLOT / SETTLEMENT keys (byKey) ===')
import re
pat = re.compile(r'(?i)(build|workbench|plot|settle|storage|shelv|outbuild|mainbuild|defen|collect|upgrade|raid|tax)')
hits = [(k, v) for k, v in bykey.items() if k and pat.search(k)]
print('matched keys:', len(hits))
for k, v in hits[:80]:
    print('  %-40s %s' % (k, v[:110].replace('\n',' ')))
