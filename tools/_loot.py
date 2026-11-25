import re
src = open('out/il2cpp/dump.cs', encoding='utf-8', errors='replace').read().split('\n')
def block(name, maxn=70):
    for i,l in enumerate(src):
        if re.match(r'^(public|internal)( sealed| abstract)? class %s\b' % name, l):
            print('==== %s (dump.cs:%d)' % (name, i+1))
            depth=0; started=False
            for j in range(i, min(i+maxn, len(src))):
                lj = src[j]
                if re.search(r'(private|public|protected|internal|\[).*;|\.ctor\(', lj) and not lj.strip().startswith('//'):
                    print('   ', lj.strip())
                if re.match(r'\s*// (Properties|Methods)', lj): break
                depth += lj.count('{') - lj.count('}')
                if '{' in lj: started=True
                if started and depth<=0: break
            print()
            return
    print('!! not found', name, '\n')
for n in ['BuildingGroupLootModel','BuildingGroupLootsModel','LocationBuildingGroupLootDescription','BuildingLootDescription','BuildingLootViewDescription']:
    block(n)
