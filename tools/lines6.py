import re, os
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = ws + r"\out\il2cpp\dump.cs"
lines = open(p, encoding='utf-8', errors='replace').readlines()
re_decl = re.compile(r'^(?:public |internal |private |protected )[^\n]*?\b(class|struct|interface|enum)\s+([A-Za-z0-9_<>`,\. ]+)')
idx=[]
for i,l in enumerate(lines):
    s=l.strip()
    if s.startswith('//'): continue
    m=re_decl.match(s)
    if m: idx.append((m.group(2).strip(), i+1))
d={}
for n,ln in idx: d.setdefault(n,ln)
for n in ['MoneyWorkbenchBonusConfig','MoneyWorkbenchBonusEntry','LaunderingState','LaunderingPutMessage','LaunderingTakeMessage','LaunderingTakeDirtyMessage','LaunderingSetActiveMessage','LaunderingPoopMessage','TaxPointModel','TaxPointMarkerModel','TaxCollectionDialogModel','TaxCollectionDialogView','MoneyWorkbenchData','MoneyWorkbenchModel','SettlementCashEntityModel','MoneyLaunderingTooltipsUpdater','TaxCollectionSettlementModelUpdater','PlayerTaxPointViewUpdater','TaxPointView','TaxCashView','TaxCashPileTargetProvider','TaxCashPileStateUpdater','TaxCashLockProgressMarkerUpdater','CloseTaxDialogOnCashLockUpdater','MoneyWorkbenchView','MoneyWorkbenchViewDescription','MoneyWorkbenchViewStateUpdater','PoopPileNodeView','MoneyWorkbenchPoopPileViewUpdater','CashLootNodeModel','TakeCashModel','CashLootNodeView','SettlementCashAvailableTriggerUpdater']:
    print(f"{n}\t{d.get(n,'-')}")
