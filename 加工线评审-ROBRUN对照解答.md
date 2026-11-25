# 加工线评审 5 问 · 用 ROB RUN 的真实做法回答

> 证据来源：ROB RUN（Steam 4262460，Unity 6000.3.18f1 IL2CPP）逆向产物
> `out\il2cpp\dump.cs`、`out\l10n_en.json`、`out\so_dump*\*`
> 标记：[观] = 二进制/资产直读事实；[推] = 由符号与结构推断；[未] = 未确认

---

## 总判断

| 评审意见 | 性质 | ROB RUN 的态度 |
|---|---|---|
| 主城原料点位临时摆 + 掉落表没对齐建筑编号 | **架构问题** | 从根上消灭：点位是数据坐标，掉落是「组→容器」反向声明 |
| 深加工反而亏钱 | **设计问题** | 不做价格梯度，做**渠道分离** |
| 种植 90 分钟拍脑袋 | **参数问题** | 时长拆成「tick × 槽数」两个正交旋钮 |
| 收藏箱拆不了 | **设计问题** | 原设计就不拆，**产出即货物** |
| 16 种建筑先藏哪些 | **运营问题** | 从不藏建筑，只藏**区**和**坑位** |

---

## 0 顺带：点位不该在场景里摆

`LocationLootNodeDescription` / `LocationContainerDescription` 的位置是纯数据字段：

```csharp
private readonly int <EntityId>;
private readonly Vector3 <Position>;
private readonly Quaternion <Orientation>;
private readonly Vector3 <InteractPoint>;
private readonly HashSet<PhysicsBodyId> <InteractIgnoreStaticBodies>;
private readonly InteractDescription <InteractDescription>;
```

连地皮掉落点也是枚举字段，不是场景物件：
`PlotSchemeDescription.MainBuildingLootPosition` / `CompoundWallLootPosition` /
`OutbuildingLootPositions[Slot]` / `EmptySpotPlotLootPosition` / `OccupiedSpotPlotLootPosition`。

**结论**：「临时摆的」在 ROB RUN 架构里不存在。点位表就是坐标表，策划填数字，美术不进场景。
评审说的根因是「点位做成 GameObject + 掉落表按建筑编号挂」，两个临时方案叠在一起必然对不齐。

---

## 1 掉落表没对齐建筑编号 → 反着声明

**ROB RUN 的事实（[观] dump.cs:189654）**

```csharp
class BuildingGroupLootsModel {
    Dictionary<LocationContainerDescription, List<BuildingGroupLootModel>> _containersGroups;
    Dictionary<LocationLootNodeDescription,   List<BuildingGroupLootModel>> _lootNodesGroups;
    List<BuildingGroupLootModel> _groups;
}
class LocationBuildingGroupLootDescription {          // dump.cs:102898
    int <Index>;
    Lazy<IReadOnlyList<LocationContainerDescription>> <ContainersLazy>;   // 我管哪些容器
    Lazy<IReadOnlyList<LocationLootNodeDescription>>  <LootNodesLazy>;    // 我管哪些战利品点
}
class BuildingGroupLootModel {                         // dump.cs:189677
    const int _limit = 1;                  // 每组只刷一次
    int _groupLootSpawnedAmount;
    LocationBuildingGroupLootDescription <Description>;
}
```

**关键反转**：翻遍 `LocationContainerDescription` 全部字段（EntityId / InventoryEntityId /
ContainerDescriptionFunc / Position / Orientation / InteractPoint / RequirementItemFunc /
SecurityAlarmDescriptionFunc / IsEventContainer / IsCashWithdrawalContainer）——
**里面没有任何「组 ID」或「掉落表 ID」字段**。

映射方向是 **组 → 容器列表**，容器不知道组的存在。所以：

- 新增建筑 → 把它的容器塞进已有组，或新建组把容器列进去
- **建筑表一个字都不用改**，不存在「编号没对齐」
- `_limit = 1` + `_groupLootSpawnedAmount` 自动防重复刷

单点概率也独立，不用整表 roll：

```csharp
LocationLootNodeDescription:            // dump.cs:87051
    float <SpawnProbability>;                  // 独立概率
    bool  <IsSpawnGuaranteed>;                 // 必出
    Lazy<HashSet<PlayerRoleDescription>> <AvailableForUseRolesLazy>;  // 按角色限制
```

**改法**：`rules.json` 从 `{buildingId: lootTable}` 改成

```json
{ "groups": [
    { "index": 0, "containers": ["..."], "lootNodes": ["..."] },
    { "index": 1, "containers": ["..."], "lootNodes": ["..."] }
]}
```

加一个 CI 校验：**每个容器的 entityId 必须被至少一个组覆盖**，没覆盖就 build 失败。
「没对齐」该由机器抓，不该靠人肉对编号。

---

## 2 深加工亏钱 → 不是调价，是换渠道

**ROB RUN 的事实（[观] dump.cs:118184）** —— `CargoDescription` 有三套独立的钱，一件货可同时挂多套：

```csharp
int  <ArrestCoinsReward>;        // 渠道 A：上交/逮捕
int  <ExchangeCoinsReward>;      // 渠道 B：走私商直接卖
int  <ExchangeCumulativePoints>; // 渠道 B'：走私商累积点数
long <ExchangeTime>;             // 该渠道的耗时
Func<CargoDescription> <ExchangeCargoFunc>;          // 换出什么
Func<CargoDescription> <ImprovedExchangeCargoFunc>;  // 升级后换出更好的
Func<CumulativeCargoDescription> <CumulativeCargoFunc>;
long <TakeTime>;  long <OpenTime>;                   // 每个动作独立时长
```

硬晶体自己的描述就写明了这套逻辑（`out\l10n_base_keys.txt`）：

> `cargo_hard_crystal_1_description` = "**Valuable as is**, but can also be packaged at a
> Lab Bench **for retail sale**."

打包的目的**不是变贵，是换渠道**：原料走批发（快、单价低），成品走零售（慢、单价高）。
深加工真正的回报是 `ImprovedExchangeCargoFunc`——**能换到市面上买不到的东西**。

**33000~82500 vs 27500~66000 的根因**：不是数值填小，是**产出数量不确定**
（"1 块晶体磨几袋粉没定死"）。期望值算不出来，必然有一档被支配。

三选一（按改动量）：

- **A（最小，推荐）**：粉末袋不给钱，给 `ExchangeCumulativePoints`。攒点数换独占货物。
  价格比较自动失效，报表都不用重调。
- **B**：转化率写死成表字段（`1 晶体 = N 袋粉`），硬约束
  `袋单价 × N > 晶体单价 × (1 + 加工时间折损)`，写进 CI。
- **C**：稀缺性错位——硬晶体随便卖，粉末袋是**唯一能进某条兑换链**的东西。

**原则**：同一件东西不要有两个可比的售价；不同售价必须挂不同的渠道、耗时或独占性。

---

## 3 种植 90 分钟 → 拆成 tick × 槽数

**ROB RUN 的事实**

```csharp
CargoChargeWorkbenchDescription:
    int  <CargoInventorySlotsCount>;              // 并行货槽数
    long <TickPeriod>;                            // 每跳时长
    bool <CanCollectChargedCargoReward>;
    long <CollectChargedCargoRewardTime>;         // 领奖也要时间

CargoProductionWorkbenchDescription:
    long <ResultTickDuration>;                    // 每跳时长
    int  <ResultTickCount>;                       // 跳数
```

产出不是固定值，是两段独立随机（[观] dump.cs:118470）：

```csharp
ChargedCargoCollectRewardDescription:
    Func<InventoryItemDescription> <RewardItemFunc>;
    int <MinRewardItemsCount>;  int <MaxRewardItemsCount>;   // 主产出区间
    int <BonusRewardMinCount>;  int <BonusRewardMaxCount>;   // 额外奖励区间再 roll
```

**为什么这么设计**：加速升级缩 `TickPeriod`，加槽升级加 `CargoInventorySlotsCount`，两条**正交**。

**改法**：90 分钟不是「待定」，现在就能定死——

> 基准 tick = 15 分钟，槽数 = 6 → 单台 24 分钟/轮
> 90 分钟 = 「6 槽 × 15 分钟」这条产线的整体产出周期

玩家感知的「种植时长」是 `槽数 / tick`，不是单株成熟时间。
另外：「待定」这个词本身是问题，文档里要写「当前值 = 90，依据 = X，负责人 = Y」。

---

## 4 收藏箱拆不了 → 原设计就不拆

**这是最干净的一条：ROB RUN 里根本没有「拆箱」这个动作（[观]）。**

```
collection_table_description = "When you pack a collection, you receive
                                cargo that can be sold to the Smuggler."   ← 产出是 cargo
collection_table_collect     = "Pack"                                      ← 动作名是"打包"
collection_reward_cargo_1..4_name = Collection Crate / Collection Crate
                                  / Rare Collection Crate / Unique Collection Crate
描述 = "A complete collection is worth more than individual items. Can be sold..."
CumulativeCargoDescription { int MaxPointsAmount; Func<CargoDescription> CargoForConversionFunc; }
```

收藏箱是 `Cargo` + `CumulativeCargo`，**终点是卖给走私商**；
四档 Basic/Uncommon/Special/Unique 靠 `collection_table_upgrade_0..3_tab` 解锁。

**「放拆货台直接报错拒收」的本质**：箱子引用了**还不存在的产出表**。
缺的不是「拆出来的东西」，是「箱子能被卖掉」这个终点。

- **最小修法**：摘掉拆货台，收藏箱定为可售货物。今天就能做，零新内容。
- **学 ROB RUN**：箱子分四档，**档位间价值差 > 拆散后的价值差**。
  玩家自然永远选整箱卖，「拆」这个动作被设计掉，也永远不用填那张空表。

---

## 5 16 种建筑先藏哪些 → 藏区、藏坑位，不藏建筑

**ROB RUN 从来没「藏」过一个建筑**，它用三层正交限制：

| 层 | 机制 | 玩家感受 |
|---|---|---|
| **坑位硬限制** | `OutbuildingSlotDescription` 只有 `Slot0`/`Slot1` → 2 坑 × 9 种建筑 | 「我要选哪两个」而不是「这个被锁了」 |
| **区等级** | `plot_sale_1/2/3` = Land Plot Title → "LEVEL 1/2/3 DISTRICT"；`settlement_tier_N_desc` = "To access this level, move to a higher-level district." | 「我要搬到高级区」 |
| **页签组顺序** | 17 组 `BuilderGroupEnumViewDescriptions` + 每面板 `GroupsOrder` | 新内容天然排在末尾 |
| **换建筑配额** | `ExpiringResourceDescription changeBuildingExpiringResource` | 「换房要消耗配额」 |

`TierDescription` / `TierParams` / `RealmTiersConfig` 都是独立配置类 → 区等级是**数据开关**，不是代码 if。

**周五试玩改法**：

1. **按功能组藏，不按建筑藏**。16 种归成 5 组（骨架 / 储物 / 生产 / 进阶 / 防御），
   试玩只把前 2 组放进 `GroupsOrder`——**一个字段的事，不用删资产**。
2. **优先藏「输出不稳定」的**：合成台、蓄能台（依赖配方表 + 产出权重）。
   保留输入→输出确定的：主屋、围墙、储物、车库。
3. **必须全开的 5 样**（营地玩法骨架，缺一个玩家就不懂自己在干什么）：
   主屋 ×1、围墙 ×1、储物 ×1、附属坑 ×2、安保系统 ×1 → 正好 6 个建造动作。

---

## 周五前最小动作清单

| 优先级 | 动作 | 工时 |
|---|---|---|
| P0 | 点位从场景 GameObject 改成数据坐标表 | 半天 |
| P0 | `rules.json` 改「组→容器」反向声明 + 覆盖校验 | 半天 |
| P0 | 收藏箱定为可售货物，摘掉拆货台 | 1 小时 |
| P1 | 建筑按功能组归类，`GroupsOrder` 只留 2 组 | 2 小时 |
| P1 | 种植时长改成 `tick × 槽数` 两字段 | 2 小时 |
| P2 | 深加工改渠道分离（粉末袋走累计点数） | 1 天 |

P0 三条加起来一天内能完，且全是「删代码/改配置」而不是「加功能」。
