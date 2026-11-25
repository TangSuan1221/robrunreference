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
keys = ['RealmLoadScreen','MainMenuLoadScreen','StartGameLoadScreen','GlobalScreenContent','GlobalScreenFactory','RealmScreenFactory','BattleLoadScreen','Loading','LoadingStep','GameLoadingStepsViewDescription','ReadyCheck','EnterMainMenuCommand','SwitchRealmCommand','SwitchRegionCommand','FindRealmByIdMessage','RealmInfoSource','RealmInfoSourceModel','SearchRealmsInSelectedRegionUpdater','RegionEntryView','RegionSwitchListModel','RegionSwitchListUpdater','RegionSwitchListView','RegionSwitchConfirmButtonCooldownUpdater','SwitchRealmDialogInputUpdater','SwitchRealmSearchResetUpdater','SwitchRealmButtonInteractableUpdater','SwitchRealmConfirmationButtonRequestingStatusUpdater','SwitchRealmViewDescription','SwitchRealmFriendsView','SwitchRealmFriendsUpdater','SwitchRealmFriendsTooltipUpdater','SwitchRealmLocalization','RealmScheduleTooltipUpdater','RealmScheduleTooltipView','RealmScheduleTimeView','RealmScheduleDayRowView','RealmEntry','RealmEntryView','RealmId','RealmNamesConfig','RealmOccupancy','RealmRecommendation','RealmEntrySelection','LineOccupancy','RealmAgeViewUpdater','SwitchRealmRefreshButtonRequestingStatusUpdater','RealmInfoSourceData','LastCreatedRealmData','RealmChatMessagesData','SubscribeRealmInfoUpdater','SubscribeRealmInfoMessage','RealmInfoMessage','BattleScreenContentDirectory','ScreenContent','GlobalScreen','RealmEntryMessage','EnterRealmMessage','RealmLoadedMessage','RealmLeaveMessage','ServerShutdown','ServerShutdownNotifications','ServerShutdownNotificationModel','Reconnect','Disconnect','NetworkIssuesView','NetworkIssuesViewUpdater','RegionSwitchConfirmButtonCooldownUpdater']
for k in keys:
    print(f"{k}\t{d.get(k,'-')}")
