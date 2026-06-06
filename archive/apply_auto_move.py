import os
import shutil
import time

root = r"C:\VS\BIN"
proposal = os.path.join(root, "archive", "AUTO_MOVE_LIST.md")
if not os.path.exists(proposal):
    print("No AUTO_MOVE_LIST.md found")
    raise SystemExit(2)
lines = []
with open(proposal, "r", encoding="utf-8") as f:
    for l in f:
        l = l.strip("\n")
        if l.strip().startswith("- "):
            lines.append(l.strip()[2:].strip())
if not lines:
    print("No items found")
    raise SystemExit(0)
timestamp = time.strftime("%Y%m%d_%H%M%S")
destRoot = os.path.join(root, "archive", timestamp)
moved = []
for it in lines:
    src = os.path.join(root, it)
    if os.path.exists(src):
        dest = os.path.join(destRoot, it)
        destdir = os.path.dirname(dest)
        os.makedirs(destdir, exist_ok=True)
        shutil.move(src, dest)
        print("Moved:", src, "->", dest)
        moved.append((src, dest))
    else:
        print("Not found:", src)
print("Done. Destination:", destRoot)
if not moved:
    raise SystemExit(1)
else:
    raise SystemExit(0)
