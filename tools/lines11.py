import re
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
for n in ['VehicleDescription','CarDescription','HelicopterDescription','CarUpgradeDescription','CarTrunkDescription','GarageDescription','PlotGarageSlotDescription','PlotCarSlotDescription','PlotHelicopterSlotDescription','VehicleBenchModel','IVehicleBenchSlotModel','VehicleBenchItemActionModel','VehicleInventoryItemModel','VehicleBenchItemView','GarageAddCarMessage','GarageRemoveCarMessage','GarageSwapCarsMessage','GarageSwapPlotCarWithInventoryMessage','GarageUnsetCarMessage','GarageVehicleInventoryMessage','CarTrunkInventoryUpgradeSlotsModel','CarUpgradesHolderModel','VehicleKeyHolderModel','VehicleSpawnerModel','VehicleLootModel','VehicleModules','CarStatsDescription','CarTrunkPositionModel','PlotVehicleModel','PlotCarModel','PlotHelicopterModel','VehicleTransformModel','VehicleSlotsModel','VehicleSeatDescription']:
    print(f"{n}\t{d.get(n,'-')}")
