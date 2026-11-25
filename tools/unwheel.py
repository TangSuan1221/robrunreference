import zipfile, os, glob
ws = r"C:\Users\糖蒜\Desktop\robrun_reference"
dst = os.path.join(ws, "tools", "pylib")
os.makedirs(dst, exist_ok=True)
for whl in glob.glob(os.path.join(ws,"tools","wheels","*.whl")):
    with zipfile.ZipFile(whl) as z:
        z.extractall(dst)
    print("ok", os.path.basename(whl))
