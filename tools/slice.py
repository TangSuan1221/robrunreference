import re, os
from collections import defaultdict
WS = r"C:\Users\糖蒜\Desktop\robrun_reference"
dump = os.path.join(WS, "out", "il2cpp", "dump.cs")
re_type = re.compile(r'^(?:public |internal |private |protected )?(?:sealed |abstract |static |partial |readonly |ref )*(?:class|struct|interface|enum)\s+([A-Za-z0-9_]+)\s*([:{]?)')
cur_ns = "(global)"
types = []
with open(dump, encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f, 1):
        s = line.rstrip()
        if s.startswith('// Namespace:'):
            cur_ns = s.split(':',1)[1].strip() or "(global)"
        st = s.strip()
        if st.startswith('//'): continue
        m = re_type.match(st)
        if m:
            types.append((cur_ns, m.group(1), i))
by_ns = defaultdict(list)
for ns,name,ln in types: by_ns[ns].append((name,ln))
os.makedirs(os.path.join(WS,'out','slices'), exist_ok=True)
groups = {
 'realm_sector': ['Models.Data.Realm','Models.Data.RealmInfo','Models.Data.RealmInfo.ClanConquestObjects','Models.Data.RealmInfo.ClanConquestSectors','Models.Data.RealmInfo.OwnedSettlements','Models.Data.RealmInfo.Realm','Models.Data.RealmInfo.RealmPopulation','Models.References.Realm','Models.Models.Realm','Game.Realm.Sectors','Game.Realm.SettlementBuilding','Game.Battle.ClanBattle','Game.Battle.ClanBattle.Conquest','Game.Battle.ClanBattle.ClanProtectingInfo','Models.Messages.FindRealmById','Game.Global.Sectors','Game.Global.RegionSwitch','Game.Global.ScheduleTooltip'],
 'ownership_land': ['Game.Global.LandOwnership','Game.Global.LandOwnership.Settlement','Models.Messages.Settlement','Models.Utils.Settlement','Game.Battle.Taxes.Settlement','Game.Battle.Taxes.Dialog','Game.Battle.Taxes.Dialog.Tabs','Game.Battle.Taxes.Dialog.Elements','Game.Battle.Taxes.Clan','Game.Battle.Entities.TaxPoint','Game.Battle.EntityModel.TaxPoint','Game.Battle.EntityModel.SettlementCash','Game.Battle.Entities.Plot.LocationPlot.Unlock','Game.Battle.EntityModel.Plot.RentDialog','Game.Battle.Entities.Plot.Dialog','Game.Battle.Entities.Plot.Dialog.Input'],
 'plot_entity': ['Game.Battle.Entities.Plot','Game.Battle.EntityModel.Plot','Models.References.Plot','Game.Battle.Entities.Plot.VehicleBench','Game.Battle.Entities.Plot.PlotContainers.Views','Game.Battle.EntityModel.Plot.PlanningBoard','Models.Data.Settlement','Models.Data.Settlement.Builder','Models.References.SettlementBuilding'],
 'map_ui': ['Game.Battle.Map','Game.Battle.Map.MapDistrictName','Game.Battle.Map.MapObjectInfoPanelViews','Game.Global.UI.Map','Game.Global.Ui.Map'],
 'builder': ['Game.Battle.Builder','Game.Battle.SettlementBuilder','Models.Messages.Builder','Models.References.Builder','Models.Data.Settlement.CargoOpenWorkbench','Models.Data.Settlement.CargoExchangeWorkbench','Models.Data.Settlement.CargoProductionWorkbench','Models.Data.Settlement.CargoChargeWorkbench','Models.Data.Settlement.CryptoWorkbench','Models.Data.Settlement.Storage','Models.Data.Settlement.Shelving','Models.Data.Settlement.Doors','Models.Data.Settlement.Loot','Models.Data.Settlement.Vehicle','Models.Data.Settlement.PlotContainer','Game.Battle.Entities.Plot.Builder','Game.Battle.EntityModel.Plot.Builder','Game.Battle.EntityModel.Plot.Builder.MainBuilding','Game.Battle.EntityModel.Plot.Builder.Outbuilding'],
 'defense': ['Game.Battle.Entities.DefenseBlock','Models.References.DefenseBlock','Models.Data.DefenseBlock','Models.Messages.PlotBuildingDefenseSlot','Game.Global.PlotAlarm','Game.Battle.Entities.LocationDefenseBlock','Game.Global.PoliceReinforcementInvitePopup'],
 'economy': ['Game.Battle.Laptop','Game.Battle.Laptop.ShopBuy','Game.Battle.Laptop.ShopSell','Game.Battle.VendorTree','Game.Battle.CargoExchanger','Game.Battle.Entities.CargoExchanger.Updaters','Game.Battle.EntityModel.CargoExchanger','Game.Battle.CurrencyExchange','Models.Messages.Laundering','Models.References.MoneyWorkbench','Models.Data.Settlement.MoneyWorkbench','Game.Battle.Entities.HubTrader','Game.Battle.Entities.BuyerEntity','Game.Battle.Buyer','Game.Battle.Entities.Trader','Game.Battle.Entities.Trader.Dialog','Game.Battle.Entities.ShopSplit','Game.Battle.Inventory.ShopSplit'],
 'survival': ['Game.Battle.Ui.HUD','Game.Battle.Ui','Game.Battle.DeathDialog','Game.Battle.Ui.Stamina','Game.Battle.Buffs','Game.Global.Reputation','Game.Battle.Prison','Game.Battle.Prison.Escape','Game.Global.Prison','Models.References.Prison','Game.Global.ImprisonmentYears','Game.Battle.EntityModel.BattleCharacter.Stats.Updaters','Game.Battle.Entities.BattleCharacter.Stats.Updaters'],
 'meta': ['Game.Battle.Tutorial','Game.Battle.Tutorial.Steps','Game.Global.Tutorial','Game.Global.BattlePass','Game.Global.Codex','Game.Global.Mail','Game.Global.Party','Game.Global.Clan','Models.Data.Clan','Game.Global','Game.Battle.Entities.Player.Talks','Game.Locations','Game.Locations.BuildingDifficulty','Game.Battle.Entities.LocationLootables','Models.Systems','Game.Shared','Game.Common','Game.Global.Settings'],
}
name2ln = {}
for ns,name,ln in types: name2ln[(ns,name)] = ln
alllns = sorted(set(ln for _,_,ln in types))
import bisect
for g, nss in groups.items():
    targets = []
    for ns in nss:
        for (name,ln) in by_ns.get(ns, []):
            targets.append(ln)
    if not targets: continue
    targets.sort()
    out = os.path.join(WS,'out','slices', g + '.txt')
    with open(out,'w',encoding='utf-8') as o:
        # read ranges: from ln to next type line (any type) exclusive
        with open(dump, encoding='utf-8', errors='replace') as f:
            lines = f.readlines()  # 82MB fine
        for ln in targets:
            start = ln-1
            idx = bisect.bisect_right(alllns, ln)
            end = alllns[idx]-1 if idx < len(alllns) else len(lines)
            o.writelines(lines[start:end])
            o.write("\n")
    print(g, os.path.getsize(out), "bytes")
