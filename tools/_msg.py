import re
src = open('out/il2cpp/dump.cs', encoding='utf-8', errors='replace').read().split('\n')
for target in ['FromInventoryToBuilderMessage','SwapBuilderMessage','BuyPlotMessage','MoveBaseMessage']:
    for i,l in enumerate(src):
        if re.match(r'^public (class|sealed class) %s\b' % target, l):
            print('==== %s (line %d)' % (target, i+1))
            depth=0; started=False
            for j in range(i, min(i+60, len(src))):
                lj = src[j]
                if re.search(r'private readonly|public .*\{ get; \}|\.ctor\(', lj):
                    print('   ', lj.strip())
                depth += lj.count('{') - lj.count('}')
                if '{' in lj: started=True
                if started and depth<=0: break
            print()
            break
