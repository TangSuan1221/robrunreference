import json, os
ws = r'C:\Users\糖蒜\Desktop\robrun_reference'
en = json.load(open(os.path.join(ws, 'out', 'loc_en.json'), encoding='utf-8'))
keys = []
for k in en:
    if k.startswith(('skin_center', 'payment_', 'buy_offer_pack', 'shop_pack', 'mail_crypto', 'not_enough', 'modal_buy_pack', 'minus_percent', 'steam_overlay')):
        keys.append(k)
for k in sorted(keys):
    print(k + '\t' + (en[k] or '').replace('\n', '\\n'))
print('---PACKS---')
for n in ['drift', 'streetkid', 'vengeance', 'kingpin', 'desert', 'apex', 'hooligan', 'agent', 'red_hill', 'hustle', 'cozy_pink', 'line', 'gasoline', 'wooden']:
    for suf in ('_header', '_description'):
        k = n + '_pack' + suf
        print(k + '\t' + (en.get(k) or '').replace('\n', '\\n'))
