import re, os, json
from collections import Counter, defaultdict

WS = r"C:\Users\糖蒜\Desktop\robrun_reference"
dump = os.path.join(WS, "out", "il2cpp", "dump.cs")

# regex to find type declarations with line numbers
re_type = re.compile(r'^(?:public |internal |private |protected )?(?:sealed |abstract |static |partial |readonly |ref )*(?:class|struct|interface|enum)\s+([A-Za-z0-9_]+)')

cur_ns = "(global)"
types = []  # (ns, name, line)
with open(dump, encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f, 1):
        s = line.rstrip()
        if s.startswith('// Namespace:'):
            cur_ns = s.split(':',1)[1].strip() or "(global)"
        st = s.strip()
        m = re_type.match(st)
        if m and not st.startswith('//'):
            types.append((cur_ns, m.group(1), i))

by_ns = defaultdict(list)
for ns, name, ln in types:
    by_ns[ns].append((name, ln))

want = [
 'Game.Global', 'Game.Global.LandOwnership', 'Game.Global.LandOwnership.Settlement',
 'Game.Global.Sectors', 'Game.Global.RegionSwitch', 'Game.Global.UI.Map', 'Game.Global.Ui.Map',
 'Game.Global.ScheduleTooltip', 'Game.Global.ServerShutdownNotifications',
 'Models.Data.Realm', 'Models.Data.RealmInfo', 'Models.Data.RealmInfo.ClanConquestObjects',
 'Models.Data.RealmInfo.ClanConquestSectors', 'Models.Data.RealmInfo.OwnedSettlements',
 'Models.Data.RealmInfo.Realm', 'Models.Data.RealmInfo.RealmPopulation',
 'Models.References.Realm', 'Models.References.Location', 'Models.References.Location.LocationPlotSpotsPresets',
 'Models.References.Location.LocationTraders', 'Models.References.Location.LocationVehiclesSpawnPoints',
 'Models.Models.Realm', 'Game.Realm.Sectors', 'Game.Realm.SettlementBuilding',
 'Game.Battle.Map', 'Game.Battle.Map.MapDistrictName', 'Game.Battle.Map.MapObjectInfoPanelViews',
 'Game.Battle.ClanBattle', 'Game.Battle.ClanBattle.Conquest', 'Game.Battle.ClanBattle.ClanProtectingInfo',
 'Models.Messages.FindRealmById', 'Models.Messages.Settlement', 'Models.Messages.Builder',
 'Models.Data.Settlement', 'Models.Data.Settlement.Builder',
 'Models.References.SettlementBuilding', 'Models.References.Plot',
 'Models.Utils.Settlement', 'Game.Battle.Taxes.Settlement', 'Game.Battle.Taxes.Dialog',
 'Game.Battle.Taxes.Dialog.Tabs', 'Game.Battle.Taxes.Dialog.Elements', 'Game.Battle.Taxes.Clan',
 'Game.Battle.Entities.TaxPoint', 'Game.Battle.EntityModel.TaxPoint', 'Game.Battle.EntityModel.SettlementCash',
 'Game.Battle.Entities.Plot', 'Game.Battle.Entities.Plot.Dialog', 'Game.Battle.Entities.Plot.Dialog.Input',
 'Game.Battle.Entities.Plot.LocationPlot.Unlock', 'Game.Battle.Entities.Plot.VehicleBench',
 'Game.Battle.Entities.Plot.PlotContainers.Views', 'Game.Battle.EntityModel.Plot',
 'Game.Battle.EntityModel.Plot.RentDialog', 'Game.Battle.EntityModel.Plot.PlanningBoard',
 'Game.Battle.Builder', 'Game.Battle.SettlementBuilder', 'Game.Battle.Entities.DefenseBlock',
 'Models.References.DefenseBlock', 'Models.Data.DefenseBlock', 'Models.Messages.PlotBuildingDefenseSlot',
 'Game.Global.PlotAlarm', 'Game.Battle.Laptop', 'Game.Battle.Laptop.ShopBuy', 'Game.Battle.Laptop.ShopSell',
 'Game.Battle.VendorTree', 'Game.Battle.CargoExchanger', 'Game.Battle.Entities.CargoExchanger.Updaters',
 'Game.Battle.EntityModel.CargoExchanger', 'Game.Battle.CurrencyExchange', 'Models.Messages.Laundering',
 'Models.References.MoneyWorkbench', 'Models.Data.Settlement.MoneyWorkbench',
 'Game.Battle.Entities.HubTrader', 'Game.Battle.Entities.BuyerEntity', 'Game.Battle.Buyer',
 'Game.Battle.Entities.Trader', 'Game.Battle.Entities.Trader.Dialog',
 'Game.Battle.Prison', 'Game.Battle.Prison.Escape', 'Game.Global.Prison', 'Models.References.Prison',
 'Game.Global.ImprisonmentYears', 'Game.Battle.Ui.HUD', 'Game.Battle.Ui', 'Game.Battle.DeathDialog',
 'Game.Battle.Ui.Stamina', 'Game.Battle.Buffs', 'Game.Battle.Tutorial', 'Game.Battle.Tutorial.Steps',
 'Game.Global.Tutorial', 'Game.Global.Reputation', 'Game.Global.BattlePass', 'Game.Global.Codex',
 'Game.Global.Mail', 'Game.Global.Party', 'Game.Global.Clan', 'Models.Data.Clan',
 'Game.Battle.Entities.Player.Talks', 'Game.Battle.Laptop', 'Game.Locations', 'Game.Locations.BuildingDifficulty',
 'Game.Battle.Entities.LocationLootables', 'Game.Battle.Entities.LocationDefenseBlock',
 'Game.Battle.LocationEvents', 'Game.Battle.LocationEffects',
 'Models.Systems', 'Game.Shared', 'Game.Common',
]
print("want namespaces found:", sum(1 for w in want if w in by_ns), "/", len(want))
missing = [w for w in want if w not in by_ns]
print("missing:", missing)
tot = sum(len(by_ns[w]) for w in want if w in by_ns)
print("total classes:", tot)
for w in want:
    if w in by_ns:
        print(f"{len(by_ns[w]):4d}  {w}")
