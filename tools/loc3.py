import os
from UnityPy.streams import EndianBinaryReader
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
p = os.path.join(ws,"out","il2cpp","dump.cs")
lines = open(p, encoding='utf-8', errors='replace').readlines()
# find LocalizationTable and TableEntry base classes
for i,l in enumerate(lines):
    if 'class LocalizationTable' in l or ('class DetailedLocalizationTable' in l) or ('class TableEntry' in l and 'StringTableEntry' not in l) or 'class TableReference' in l:
        print(i+1, l.strip()[:160])
