#!/usr/bin/env python
"""Generate the base-building content catalogue annex from out/base/desc_all.json.

Writes out/base/base_catalog.md : every base-building related *Descriptions registry
with its full entry list.
"""
import json
import re

SRC = 'out/base/desc_all.json'
OUT = 'out/base/base_catalog.md'

PAT = re.compile(r'(?i)(Building|Plot|Storage|Shelving|Workbench|Defense|Collection|Compound|Door'
                 r'|Furniture|Cabinet|WindowBlind|PlotContainer|Cargo|WaterZone|Slot)')

# Grouping for readability: (heading, registry-substring regex)
GROUPS = [
    ('A. 建筑主体 (MainBuilding / Outbuilding / CompoundWall)', r'MainBuilding|Outbuilding|CompoundWall'),
    ('B. 建造槽位 (Slot 定义)', r'Descriptions\.Slots\.|PlotCarSlot|CollectionTableSlot'),
    ('C. 室内设施 (Storage / Shelving / CollectionTable / FirstAid / Door / WindowBlinds / PlotContainer)',
     r'Storage\.|Shelving\.|CollectionTable\.|FirstAidCabinet|Door\.|WindowBlind|PlotContainer'),
    ('D. 工作台 (Cargo* / Crypto* / Money*)', r'Workbench|VideoCard'),
    ('E. 防守 (DefenseBlock / PlotBuildingDefenseSettings / Decoder)', r'Defense|Decoder'),
    ('F. 聚落层建筑与配置 (Settlement*)', r'Settlement'),
    ('G. 价格与地块 (Price / Plot / Spot)', r'Price|Plot\.|PlotSpot|SettlementBuilding'),
    ('H. 货物与收集品 (Cargo / Collection)', r'Cargo|Collection'),
]


def main():
    d = json.load(open(SRC, encoding='utf-8'))
    sel = {k: v for k, v in d.items() if PAT.search(k)}
    lines = ['# ROB RUN 基地建造 —— 内容注册表全表 (OBSERVATION)',
             '',
             '由 `out/il2cpp/dump.cs` 的静态注册表类反推得出：每个 `XxxDescriptions` 静态类的每个静态属性',
             '＝ 一条被序列化的 `XxxDescription` 条目（即游戏内的一个内容 id）。',
             '',
             '总计 **%d** 个与基地建造相关的注册表、**%d** 条条目。' % (len(sel), sum(len(v) for v in sel.values())),
             '']
    used = set()
    for title, rx in GROUPS:
        sub = {k: v for k, v in sel.items() if re.search(rx, k)}
        sub = {k: v for k, v in sub.items() if k not in used}
        if not sub:
            continue
        used |= set(sub)
        lines.append('## ' + title)
        lines.append('')
        for k in sorted(sub):
            entries = sub[k]
            short = k.replace('Models.ReferencesProject.', '')
            lines.append('- **%s** (%d): %s' % (short, len(entries),
                                                ', '.join(e['name'] for e in entries)))
        lines.append('')
    rest = {k: v for k, v in sel.items() if k not in used}
    if rest:
        lines.append('## 其他')
        lines.append('')
        for k in sorted(rest):
            lines.append('- **%s** (%d): %s' % (k.replace('Models.ReferencesProject.', ''), len(rest[k]),
                                                ', '.join(e['name'] for e in rest[k])))
        lines.append('')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('wrote %s (%d registries, %d entries)' % (OUT, len(sel), sum(len(v) for v in sel.values())))


if __name__ == '__main__':
    main()
