# Unknown 清单与验证计划

> **用途**：把本系列 16 份技术文档里所有 `[未知]` 项集中成一张"待验证表"，并给出**可执行的验证手段、成本、优先级**。
> **分级**：P0 = 影响玩法闭环必须知道；P1 = 影响平衡调优；P2 = 影响复刻精度。

---

## 0. 为什么有这么多 Unknown

ROB RUN 的**所有数值配置都不在客户端**，而是服务器在开局下发的 `.bytes`（T01 §2.3）。客户端只有：

- 类型 schema（字段名/类型）
- 本地化文案（4,942 条）
- 少量 **本地 ScriptableObject**（视图参数、时间表）

所以本系列能给出的"数值"只有两类：
1. **本地 SO 真值**（已解出，如 `SwitchRealmViewDescription`、`MapMarkerViewDescriptions`、`ConfiscationDescription`）
2. **推断框架**（标明 `[推断]`）

以下所有 `[未知-服务端]` 都需要**运行时手段**才能拿到。

---

## 1. 验证手段（按成本从低到高）

| 手段 | 成本 | 能拿什么 | 限制 |
|---|---|---|---|
| **A. 抓包** | 低 | `references .bytes` → 全部配置数值 | 需 HTTPS 解密（`RemoteReferencesProvider`）+ 反序列化器 |
| **B. 进程内存** | 中 | 已加载的 `StaticReferences` 托管堆 | EAC 拦调试器 |
| **C. 私服/离线** | 高 | 服务端行为（税/突袭/帮战结算） | 需完整协议 |
| **D. 实测统计** | 中 | 概率/时间/收益曲线 | 需要大量样本 |
| **E. 反汇编** | 最高 | 内联常量 | 148MB DLL，慢 |

**推荐顺序**：A（抓包）→ D（实测）→ B（内存）→ C（私服）→ E（反汇编）。

---

## 2. P0：影响玩法闭环的 Unknown（必须拿到）

| # | 未知项 | 所属 | 影响 | 建议手段 |
|---|---|---|---|---|
| P0-01 | `TierParams` 14 个字段的值（5 价格表 + 4 税率 + 洗钱乘区 + 帮战下限 + 聚落数） | S05 | 整个经济无法定价 | A |
| P0-02 | `OwnedSettlementConfig.MaxCount` | S04 | 地主上限 | A |
| P0-03 | `PlotSpotConfig.MaxSpotsCount / MaxPresetsCount` | S04 | 聚落容量 | A |
| P0-04 | `RealmParams.Lifetime / UsersLimit` | S02 | 州寿命/容量 | A |
| P0-05 | 解码器/防御模块/防御块的 `DefensePoints` + `CastDuration` | S09 | PvP 攻防无法平衡 | A |
| P0-06 | `MoneyWorkbenchBonusConfig`（`BonusPerAmount` / `BrokenCablePenaltyPercent` / `RepairBrokenCableDuration`） | S08 | 洗钱曲线 | A |
| P0-07 | `SettlementTaxDescription.TaxCooldown / CashLockDuration` + 税率 | S08 | 税收节奏 | A |
| P0-08 | `MaxDirtyCashAmount`（洗钱台上限） | S08 | 洗钱容量 | A |
| P0-09 | `ExpiringResourceDescription`（建筑/家具改动配额） | S06 | 建造节奏 | A |
| P0-10 | `PlotBuildingConfig.MaxDefensePoints` | S09 | 防御上限 | A |
| P0-11 | 六类工作台的 `SlotsCount` / `Tick` | S07 | 生产节奏 | A |
| P0-12 | `ClanConfig` 10 项 | S14 | 帮派规模/成本 | A |
| P0-13 | `ClanRankDescription` 4 阶 × 11 权限的布尔值 | S14 | 权限矩阵 | A |
| P0-14 | `WantedPointsConfig` 8 项 | S10 | 通缉曲线 | A |
| P0-15 | `PrisonEnterTypeDescription.Years`（州末前/后） | S10 | 服刑时长 | A |
| P0-16 | 聚落/地块/建筑价格的**物品清单** | S04 | 经济门槛 | A |

---

## 3. P1：影响平衡调优的 Unknown

| # | 未知项 | 所属 | 建议手段 |
|---|---|---|---|
| P1-01 | `SectorSettlementsCount` 每档值 | S05 | A |
| P1-02 | `CanBuySettlement` 哪些 Tier 为 true | S05 | A |
| P1-03 | `SettlementOwnerTaxBonusFrom/To` 语义 | S05 | A |
| P1-04 | `RealmScheduleConfig.TimesSinceWeekStart[]` | S02 | A |
| P1-05 | `RealmVersion` 是否只有 V0（当前代码只有 V0，但 V1 类存在） | S05 | A |
| P1-06 | 后坐力/破门 `CastDuration` 与 `DefensePoints` 的对应公式 | S09 | A/D |
| P1-07 | `PlotAlarmNotification.Priory` 取值规则 | S09 | A |
| P1-08 | 警报"延迟生效"的倒计时长度 | S09 | A |
| P1-09 | `DeathScreenModel` 4 个时间戳的时长 | S10 | A |
| P1-10 | `BattleStaminaViewDescription` 4 个值 | S10 | A |
| P1-11 | `InitialDirtyLevel`（车库） | S12 | A |
| P1-12 | 载具 `CryptoCoinsPrice` / `ImprisonmentYearsRequired` | S12 | A |
| P1-13 | `TraderInventoryDescription.BuyPriceModifier` | S13 | A |
| P1-14 | `CargoExchangerConfig` 3 个上限 | S13 | A |
| P1-15 | `BarterRecipeDescription` 配方表 | S13 | A |
| P1-16 | `BarterDialogModel.CooldownEndTs` | S13 | A |
| P1-17 | 战令赛季周期与奖励表 | S16 | A |
| P1-18 | `CodexViewDescription.IsMandatory` 的强制规则 | S16 | A |
| P1-19 | `ClanBattleTierDescription` / `ClanBattlePeriodDescription` | S14 | A |
| P1-20 | 帮战胜负判定（占点时长/杀人数） | S14 | C/D |

---

## 4. P2：影响复刻精度的 Unknown

| # | 未知项 | 所属 | 备注 |
|---|---|---|---|
| P2-01 | `PlotGradeDescription` 的等级数（当前只见 StartGrade / Grade3） | S06 | 框架支持多蓝图 |
| P2-02 | 是否存在第二张地块蓝图 | S06 | 当前只见 `SettlementPlotScheme3` |
| P2-03 | `BuilderSlotViewDescription` 完整字段 | S06 | UI 外观 |
| P2-04 | 建造面板 17 个分组名（SO 值） | S06 | 既有文档给了枚举 |
| P2-05 | `PlotSchemeDescription.DiagonalSizeXZ` | S06 | 地块尺寸 |
| P2-06 | `CarInteractionPointsDescription` 交互点 | S12 | 引擎盖/后备箱/车门 |
| P2-07 | `VehicleTrunkInventorySettingsDescription` | S12 | 后备箱设置 |
| P2-08 | `PoliceCarTrunkDescription` | S12 | 警车特殊规则 |
| P2-09 | `BillOfSale` 用途 | S13 | 地契？ |
| P2-10 | `IsCategoryTrader` 语义 | S13 | 分类商人 |
| P2-11 | `VendorTreeNodeDescription` 完整节点列表 | S13 | 树规模 |
| P2-12 | `LocationActivity` 枚举 | S03 | 地图活动 |
| P2-13 | `MapViewDescription` 4 个值 | S03 | SO 不在已扫描包内 |
| P2-14 | `Marker` 枚举中未出现在 `_markers` 的编号 | S03 | gap |
| P2-15 | `RealmGridViewDescription._realmVersion` 与地图预制的对应 | S03 | 是否每版本一张图 |
| P2-16 | `Settlement.bytes` / `Settlement2.bytes` 二进制格式 | S01 | 关卡几何 |
| P2-17 | `SettlementConnectionExpiringResourceDescription` 用途 | S01 | 聚落连接 |
| P2-18 | 27 种 Buff 各自效果 | S10 | Buff 表 |
| P2-19 | `UnavailableTargetActionsKeys` 完整 key 表 | S11 | 不可用原因 |
| P2-20 | 32 种互斥进程的长按时长 | S11 | — |
| P2-21 | `DeathScreenModel.DeathType` 枚举值 | S10 | 死亡类型 |
| P2-22 | `ModalDialogData` 字段 | S16 | 弹窗内容 |
| P2-23 | `NicknameValidationDescription` 规则 | S16 | 改名校验 |
| P2-24 | `MaintenanceScreenModel` 维护时间来源 | S16 | — |
| P2-25 | `AchievementDescription` 成就清单 | S16 | — |
| P2-26 | `MailViewDescription` 邮件类型 | S16 | — |
| P2-27 | `ReportReasonDescription` 举报理由 | S16 | — |

---

## 5. 抓包执行方案（P0 主路径）

### 5.1 目标

拿到 `StaticReferences.Build(environment)` 加载的 `.bytes`，反序列化成 `*Description` 对象。

### 5.2 步骤

```text
1. 确认 `RemoteReferencesProvider` 的 URL
   - 字符串证据：references-provider / references_hash / /config.json
   - 用 `strings` 或 dump.cs 的 `Kefir.Framework.Http` 相关类找 URL 模板
2. 配置系统代理 + 安装根证书（mitmproxy / Fiddler）
3. 启动游戏，记录所有 HTTPS 请求
4. 找到 `.bytes` 响应（可能是压缩的）
5. 用 `references_hash` 校验
6. 用 `*BinarySerializer` 的字段顺序写解析器
   - 字段名/顺序来自 dump.cs 的 `XxxBinarySerializer` 类
   - 基础类型：IBinaryReadStream / ReadOnlyEnum<T> / Lazy<T>
7. 输出 JSON → 与本系列文档的 schema 对照
```

### 5.3 关键类（`[实证]`）

- `Models.ReferencesProject.StaticReferences.Build(string environment)`
- `RemoteReferencesProvider`
- 各 `XxxBinarySerializer`（如 `SettlementBuildingDescriptionBinarySerializer`）

### 5.4 风险

- **EAC（EasyAntiCheat）** 可能检测代理/证书
- 证书固定（certificate pinning）
- `.bytes` 可能加密（不只是压缩）

---

## 6. 实测统计方案（P1 补充）

对无法抓包的"行为数值"，用**样本统计**：

| 目标 | 方法 | 样本量 |
|---|---|---|
| 洗钱速度 | 固定脏钱量，记录 1 小时净钱增量 | 10 次 |
| 税生效延迟 | 居民洗一笔，记录税点变可用时间 | 20 次 |
| 破门时间 | 固定解码器 vs 固定防御，记录撬开耗时 | 30 次 |
| 州寿命 | 记录开服到联邦没收 | 1 次（7 天） |
| 帮战排期 | 记录一周的开战时刻 | 1 周 |

---

## 7. 验证优先级建议

```
第 1 周：P0-01/02/03/04（经济底座）
第 2 周：P0-05/06/07/08（PvP + 洗钱）
第 3 周：P0-09/10/11（建造 + 生产）
第 4 周：P0-12/13/14/15/16（帮派 + 生存 + 产权）
第 5 周起：P1 → P2
```

---

## 8. 本系列已"消除"的 Unknown（本地 SO 解出）

| 项 | 值 | 来源 |
|---|---|---|
| 老州阈值 | 24 小时 | `SwitchRealmViewDescription` |
| 低占用阈值 | 20% | 同上 |
| 中占用阈值 | 82.5% | 同上 |
| 推荐州数 | 3 | 同上 |
| 假人口 | 开，15000 | 同上 |
| 好友 tooltip 上限 | 10 | 同上 |
| marker 数量 | 79 | `MapMarkerViewDescriptions` |
| marker 可见半径 | 100 | 同上 |
| 缩放级别 | 0.33 / 0.66 | 同上 |
| 州末弹窗临界 | 12 小时 | `ConfiscationDescription` |
| 最终倒计时 | 10 秒 | 同上 |
| 终局提示提前 | 1 秒 | 同上 |
| 本地化条目 | 4,942 | `loc_en.json` |
| 物品类型 | 41 种 | `InventoryItemType` |
| 互斥进程 | 32 种 | `MutuallyExclusiveProcessesDescription` |
| 教程步数 | 15 步 | `TutorialStepDescription` |

---

## 9. 如何更新本文件

每验证一项，在本文件对应行标注：

```
P0-01 ✅ 已验证（2026-12-01，抓包）
  值：Tier1 PlotPrice = [{item:"LandPlotTitle1", amount:1}], ...
```

并把数值回填到对应 `Txx` 文档的表格中。
