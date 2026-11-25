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
keys=['MapDialogModel','MapDialogView','MapView','MapViewDescription','MapZoomInputUpdater','MapZoomSliderInputUpdater','MapMultiTouchInputUpdater','MapCollectionViewUpdater','MapCollectionsViewUpdater','MapCollectionContentView','MapCollectionItemView','MapBuildingPanelInfoViewUpdater','MapBuildingProtectorBlockUpdater','MapObjectInfoPanelView','MapObjectInfoOwnerView','MapObjectInfoCargoView','MapObjectInfoRewardItemView','MapObjectInfoCargoExchangerView','MapDialogPopulationCounterUpdater','MapCounterPopulationView','MapObjectivesPanelView','MapObjectivesVisibilityUpdater','MapObjectivesPlayerPrefsUpdater','MapEventPanelView','MapEventPanelUpdater','MapMarkerBehavior','MapMarkerView','MapMarkerViewDescription','MapMarkerViewDescriptions','MapMarkerModel','StaticMapMarkerModel','BuildingMapMarkerModel','BuildingClanMapMarkerModel','BuildingPartyMapMarkerModel','VehicleMapMarkerModel','PlotSpotMapMarkerModel','MapInfoMarkerModel','MapInfoMarker','MovableMapMarkerModel','MinimapView','MapDistrictNameView','MapDistrictNameUpdater','DistrictNameView','MapSettlementNameReportInteractableUpdater','MapLockCollectionTableHintUpdater','MapPoint','MapBuildingPoint','MapMarkerPoint','MapTerrainPoint','MapPosition','RealmGridView','RealmGridViewDescription','RealmLocationView','RealmSectorCenterView','RealmSectorSettlementsUpdater','RealmSectorUpdater','RealmSectorsUpdater','RealmSelectionCellView','RealmSelectionCellUpdater','RealmCellView','RealmCellsView','RealmBurningCellsView','RealmBuildingsMarkerView','RealmPopulationView','RealmPopulationDetailAnimationUpdater','RealmSectorRoadView','RealmDottedLineView','RealmNearestCameraSectorModelUpdater','LocationViewDescription','LocationNameViewDescriptions','LocationScreenView','GlobalScreenContent','MapFakeBuildingView','MapBuildingView','MapBuildingViewUpdater','MapMeshView','MapBuildingDescription']
for k in keys:
    print(f"{k}\t{d.get(k,'-')}")
