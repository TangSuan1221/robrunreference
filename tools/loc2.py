import os, re
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
dump = open(os.path.join(ws,"out","il2cpp","dump.cs"), encoding='utf-8', errors='replace')
# find Unity.Localization string table classes
targets = ['StringTable','LocalizedString','LocalizationTable','StringTableEntry','TableReference','SharedTableData']
lines = dump.readlines()
for i,line in enumerate(lines):
    s=line.strip()
    if any(t in s for t in ['class StringTable','class SharedTableData','class LocalizedString ','class TableEntryData','class StringTableEntry']):
        print(i+1, s[:200])
