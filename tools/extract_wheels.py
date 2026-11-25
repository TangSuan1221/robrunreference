import sys, zipfile, pathlib

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for whl in sys.argv[2:]:
    p = pathlib.Path(whl)
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            target = out / name
            if name.endswith('/'):
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(name) as src, open(target, 'wb') as dst:
                dst.write(src.read())
    print('extracted', p.name)
