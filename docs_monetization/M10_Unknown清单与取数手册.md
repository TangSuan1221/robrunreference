# M10 · 商业化 Unknown 清单与取数手册（附回填模板）

> 本文不是"分析"，是**施工图**：把本系列所有"知道字段、不知道数值"的地方集中到一张表，给出**唯一可行的取法**、报文名、反汇编地址、以及可直接填的回填表格。
> **原则**：能抓包解决的不反汇编，能反汇编解决的不猜，猜的必须标 `[推断]` 并给推理链。

---

## 0. 为什么"数值"拿不到：三层服务端权威（先说清原因）

| 层 | 机制 | 证据 | 后果 |
|---|---|---|---|
| **配置层** | 只要带 `BinarySerializable` 的 `*Params` / `*Config`，都由服务端按 `RealmVersion` 下发（`RealmMapVersionComputedConfig`） | dump.cs:79224、80017 的 `BinarySerializable` 标记 | 客户端只有**结构**，没有值 |
| **查询层** | 价格不是本地算的，客户端发 `Tier` 问服务端要"物品→数量"表 | `GetItemAmountsForSettlementPriceMessage(tier)` dump.cs:202054 | **连价格表都不在客户端** |
| **平台层** | B-Coin 价格由 Steam `TransactionDescription` 提供，本地只做字符串格式化 | `CryptoCoinsPackTransactionRules.GetPriceText(transaction, currency)` dump.cs:448281 | 价格随区/币种/促销变，客户端无从得知 |

→ **结论**：本作是"厚服务端"架构。**任何声称"从客户端读到商店价格"的结论都是假的**。要真数值，只有两条路：**抓包** 或 **看商店页/游戏内截图**。

---

## 1. 抓包目标清单（按优先级）

> 传输层：`Kefir.Framework.Network` + `MessagePack` + `ZstdNet`（压缩）。抓到的 payload 需要 **zstd 解压 + MessagePack 解码**，再按 `dump.cs` 里的字段顺序读。
> 每条消息在 `dump.cs` 里都有完整字段表，**字段顺序 = 序列化顺序**，可直接当 schema 用。

### P0：一次会话就能拿全的四张表

| # | 消息 | 方向 | 能拿到什么 | dump.cs |
|---|---|---|---|---|
| 1 | `GetShopPacksMessage` | C→S 请求 / S→C **全量商品包** | 34 个包的 `Contents`、`CryptoCoinsPrice`、`AvailabilityStartTs/EndTs`、`IsPermanent`、`IsHidden`、featured 价 | 202094 |
| 2 | `GetItemAmountsForSettlementPriceMessage` | C→S(Tier) / S→C **物品→数量** | **15 条据点价格表的真实数值**（M02 全表） | 202054 |
| 3 | `CurrencyExchangeGetInfoMessage` | C→S / S→C | 当前汇率、点差、买卖额度余量、下次刷新时间、历史曲线点 | 206646 |
| 4 | Realm 配置响应（`GetRealmsMessage` 之后的下行） | S→C | `TierParams` 16 字段、`SectorParams`（含 `BuyerSectorModifier`）、区→档映射 | 202078 |

### P1：需要触发一次交易/一次进入

| # | 消息 | 触发 | 能拿到什么 | dump.cs |
|---|---|---|---|---|
| 5 | `BuyShopPackMessage` / `BuyFeaturedShopPackMessage` | 买一个包 | 服务端扣费价、赠送内容、补偿额 | 198099 / 198014 |
| 6 | `BuyBattlePassPremiumMessage` / `...WithRewardsMessage` | 点"Buy Premium/Premium+" | 战令售价、Premium+ 的一次性解锁价 | 207940 / 207965 |
| 7 | `ClaimBattlePassFreeRewardMessage` 等 4 条 | 领奖 | 每格奖励内容、页/行索引、点数消耗、可重复次数 | 208015–208100 |
| 8 | `ExchangeRouletteChipsMessage` / `ApplyRouletteBetMessage` | 换筹码/下注 | 筹码↔现金汇率、下注档位、赔率 | 204208 / 204133 |
| 9 | `GetLockedVendorTreeNodesPriceItemsCountMessage` | 打开黑市解锁树 | **解锁价格的计价物与数量**（疑似也是物品计价） | 203120 |
| 10 | `BuyInventoryItemMessage` | 黑市买货 | 单价、折扣、税 | 205324 |
| 11 | `StoreInfoResponse` / `StoreUserInfo` | 打开储值页 | B-Coin 6 档的 `Base/Bonus/Discount` 与本地化价格串 | 1758114 / 1758208 |

### P2：低频但决定"付费上限"

| # | 消息 | 能拿到什么 | dump.cs |
|---|---|---|---|
| 12 | `OpenBankAccountMessage` | 开户费用/条件 | 202279 |
| 13 | `CheatSetBankAccountMessage` / `CheatCurrencyExchangeFutureRatesMessage` | ⚠️ 仅作弊/调试通道，**说明汇率是服务端预测生成** | 199498 / 206606 |
| 14 | `ClaimMailAttachmentsMessage` | 补发/赠送邮件里的货币量 | 205006 |
| 15 | `PurchaseDeliveredNotificationUpdater` 上行 | 订单状态机（已送达/重复） | 445595 |

---

## 2. 反汇编取数（只用于"客户端硬编码常量"）

> 适用：`*.cctor` 里写死的枚举常量（如显卡 `Power`、槽位数、B-Coin 包 id）。**不适用于** §0 的三层服务端数据。
> 文件：`C:\game\steamapps\common\Rob Run\GameAssembly.dll`；dump.cs 的 `// RVA:` 是 VA，`// Offset:` 是**文件偏移**（可直接 seek）。

| 目标 | 类 | `.cctor` RVA | dump.cs 行 |
|---|---|---|---|
| 显卡 Power / ResourcePoints | `VideoCardDescriptions` | `0x3D9E460` | 44042 |
| 矿机三个槽位数 | `CryptoWorkbenchDescriptions` | `0x3D7B590` | 43888 |
| 矿机产物 / 坏卡 | `CryptoWorkbenchConfigs` | `0x3D7B140` | 43840 |
| 散热 / 加速修正值 | `CryptoWorkbenchEfficiencyUpgradeDescriptions` / `...SpeedupUpgradeDescriptions` | 见该类 `.cctor` 行 | 43936 / 43984 |
| B-Coin 6 档 Base/Bonus/Discount | `CryptoCoinsPackDescriptions` | `0x49A3920` | 22632 |
| 15 条价格条目（客户端白名单） | `InventoryItemsPriceDescriptions` | `0x49A9B60` | 23191 |
| 新号初始 Credits | `CurrencyDescription.get_StartCoinsCount` | `0x4039680` | 63971 |
| 34 个商品包常量 | `ShopPackDescriptions` | 见该类 `.cctor` 行 | 29449+ |

**取数方法（三步，无需 Ghidra）**：
1. 读 `dump.cs` 该类末尾的 `.cctor()` 行，取 `Offset: 0x…`；
2. 用任意 PE 解析（或直接按 `Offset`）从 `GameAssembly.dll` 截 `~0x200` 字节；
3. 扫 `B8+r / B9 / BA / C7 /0` 后的 `imm32`，按**出现顺序**与构造参数顺序对齐；`lea` 的 RIP 相对地址指向字符串字面量，可与 `stringliteral.json` 对上 → 确定"哪个 id 配哪个值"。

> **可选工具**：本机未能安装 `capstone`（pip 写临时目录被沙箱拒绝）。若需要，可在**有管理员权限的普通 shell**里 `pip install capstone` 后，用 `Cs(CS_ARCH_X86, CS_MODE_64)` 反汇编上述字节段；或把 `GameAssembly.dll` 丢进 IDA/Ghidra 按 `RVA` 跳转。

---

## 3. 回填模板（抓到数就直接填）

### 3.1 据点 15 条价格表（M02 §2.2）

| id | 物品1 | 数量1 | 物品2 | 数量2 | 物品3 | 数量3 | 折合 Credits（可选） |
|---|---|---|---|---|---|---|---|
| `tier_1_plot_price` | | | | | | | |
| `tier_2_plot_price` | | | | | | | |
| `tier_3_plot_price` | | | | | | | |
| `tier_1_settlement_price` | | | | | | | |
| `tier_2_settlement_price` | | | | | | | |
| `tier_3_settlement_price` | | | | | | | |
| `tier_1_settlement_building_price` | | | | | | | |
| `tier_2_settlement_building_price` | | | | | | | |
| `tier_3_settlement_building_price` | | | | | | | |
| `tier_1_settlement_building_plot_price` | | | | | | | |
| `tier_2_settlement_building_plot_price` | | | | | | | |
| `tier_3_settlement_building_plot_price` | | | | | | | |
| `tier_1_local_move_plot_price` | | | | | | | |
| `tier_2_local_move_plot_price` | | | | | | | |
| `tier_3_local_move_plot_price` | | | | | | | |

### 3.2 B-Coin 6 档（id 已实证，数值待填）

| 包 | id（=价格点） | Base | Bonus | 合计 | Discount | 本地化价格串 | 首充？ |
|---|---|---|---|---|---|---|---|
| Pack0 | `tier_499`（推断） | | | | | | |
| Pack1 | `tier_999`（推断） | | | | | | |
| Pack2 | `tier_1499`（推断） | | | | | | |
| Pack3 | `tier_1999`（推断） | | | | | | |
| Pack4 | `tier_2999`（推断） | | | | | | |
| Pack5 | `tier_4999`（推断） | | | | | | |
| ? | `tier_1`（异常项，待确认是测试包还是首充包） | | | | | | |

### 3.3 34 个商品包（M03 用）

| 包 | 类别 | Contents（9 类外观中的哪几件） | CryptoCoinsPrice | Featured 价 | 起止时间 | 永久 | 隐藏 | 独立计时器 |
|---|---|---|---|---|---|---|---|---|
| DriftPack | 主题合集 | | | | | | | |
| StreetkidPack | 主题合集 | | | | | | | |
| VengeancePack | 主题合集 | | | | | | | |
| KingpinPack | 主题合集 | | | | | | | |
| DesertPack | 主题合集 | | | | | | | |
| ApexPack | 主题合集 | | | | | | | |
| HooliganPack | 主题合集 | | | | | | | |
| AgentPack | 主题合集 | | | | | | | |
| RedHillPack | 主题合集 | | | | | | | |
| HustlePack | 主题合集 | | | | | | | |
| CozyPinkPack | 主题合集 | | | | | | | |
| LinePack | 主题合集 | | | | | | | |
| GasolinePack | 主题合集 | | | | | | | |
| WoodenPack | 主题合集 | | | | | | | |
| Mask16/17/18/21/13/9/6/12/15/36/33Pack | 单件面具 | | | | | | | |
| Bag26Pack | 单件背包 | | | | | | | |
| Cb45S1 / Dp9S2 / ApScalarS1 / Pdw90S5 / Pdw90S7 / Drm14S4 / Rc556S2 / Rc556S1 | 单件武器皮 | | | | | | | |

### 3.4 战令（M04 用）

| 项 | 待填 |
|---|---|
| 赛季数 / 每季页数 / 每页行数 | |
| Free 轨每页格数 | |
| Premium 轨每页格数 | |
| Main Reward 解锁条件 | |
| Repeatable 池内容与单次点数 | |
| Premium 售价（B-Coin） | |
| Premium+ 售价（B-Coin） | |
| 点数获取速率（哪些行为给多少） | |
| 点数上限 | |

### 3.5 兑换市场（M06 用）

| 参数 | 字段 | 待填 |
|---|---|---|
| 卖出延迟 | `SellCryptoDelay` | |
| 卖点差延迟 | `SpreadSellCryptoDelay` | |
| 买入延迟 | `BuyCryptoDelay` | |
| 买点差延迟 | `SpreadBuyCryptoDelay` | |
| 卖出额度 | `SellCryptoLimit`（`BeginTs/PeriodDuration/Count/Cooldown`） | |
| 买入额度 | `BuyCryptoLimit` | |
| 单笔上限 | `CryptoCoinsPerTransactionLimit` | |
| 点差 | `ExchangeRateGap` | |
| 汇率周期 | `RatePeriod` | |

---

## 4. Unknown 总表（按系统归并，含状态）

| # | 系统 | Unknown | 状态 | 取法 |
|---|---|---|---|---|
| 1 | 据点 | 15 条价格表数值 | ❌ 未知 | `GetItemAmountsForSettlementPriceMessage` |
| 2 | 据点 | 区→档映射 | ❌ 未知 | Realm 配置下行 |
| 3 | 据点 | `BuyerSectorModifier` 每区值 | ❌ 未知 | 同上 |
| 4 | 据点 | 4 个税率值 | ❌ 未知 | 同上 |
| 5 | 据点 | 8 种聚落建筑 bonus 值 | ❌ 未知 | 同上 |
| 6 | 据点 | 矿机三槽位数 | ⚠️ 可反汇编 | `CryptoWorkbenchDescriptions..cctor` |
| 7 | 据点 | 显卡 Power/ResourcePoints | ⚠️ 可反汇编 | `VideoCardDescriptions..cctor` |
| 8 | 商店 | 34 包价格/内容 | ❌ 未知 | `GetShopPacksMessage` |
| 9 | 商店 | featured 价来源与折扣规则 | ⚠️ 部分 | 抓包对比（同包不同账号/时间） |
| 10 | 商店 | 补偿公式 `CalculateCompensation` | ⚠️ 可反汇编 | `ShopPackRules.CalculateCompensation` |
| 11 | 战令 | Premium/Premium+ 售价 | ❌ 未知 | `BuyBattlePassPremium*` |
| 12 | 战令 | 页/行/奖励内容 | ❌ 未知 | `ClaimBattlePass*` + `BattlePassViewDescriptions` SO |
| 13 | 战令 | 点数获取速率 | ❌ 未知 | 行为埋点/抓包 |
| 14 | 货币 | `StartCoinsCount` | ⚠️ 可反汇编 | `CurrencyDescription.get_StartCoinsCount` |
| 15 | 货币 | 汇率生成算法 | ❌ 未知 | 长期抓 `CurrencyExchangeGetInfo` |
| 16 | 储值 | 6 档 Base/Bonus/Discount | ⚠️ 可反汇编 / 抓 `StoreInfoResponse` | |
| 17 | 储值 | 各币种 `AmountStep` | ❌ 未知 | Steamworks |
| 18 | 赌场 | 赔率与抽水 | ⚠️ 可反汇编 | `RouletteBetOddsConfig`（`RouletteConfigs..cctor`） |
| 19 | 抽奖 | 奖池/保底/限购 | ❌ 未知 | 抓 `InfiniteReward` 相关消息 |
| 20 | 黑市 | 解锁树的计价物 | ⚠️ 疑似物品 | `GetLockedVendorTreeNodesPriceItemsCountMessage` |

---

## 5. 工作量与顺序建议

| 阶段 | 内容 | 预估 | 产出 |
|---|---|---|---|
| **第 1 步** | 装抓包（mitmproxy + zstd + msgpack 解码脚本），进一次游戏到主城 | 0.5 天 | 能解 MessagePack 的管道 |
| **第 2 步** | 拉 `GetShopPacksMessage` + `GetItemAmountsForSettlementPriceMessage` | 0.5 天 | M02/M03 数值表回填 80% |
| **第 3 步** | 打开储值页 + 战令页 | 0.5 天 | M04/M05 售价回填 |
| **第 4 步** | 反汇编 §2 的 5 个 `.cctor` | 0.5 天 | 矿机/显卡/储值档数值 |
| **第 5 步** | 连续 7 天抓 `CurrencyExchangeGetInfo` | 自动 | 汇率模型拟合 |

> **注意**：抓包会触碰 EAC（EasyAntiCheat）。本机 `C:\game\steamapps\common\Rob Run\EasyAntiCheat` 存在，`fix_eac.bat` 亦在目录中。**仅在离线/私人环境、且自担风险的前提下进行**；本系列文档的所有 `[未知-服务端]` 标记即为"未抓包"的诚实边界。
