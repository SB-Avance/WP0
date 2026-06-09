from pathlib import Path

p = Path("rebuild/scripts/export_messages.py")
for i, l in enumerate(p.read_text().splitlines(), 1):
    if len(l) > 88:
        print(i, len(l), l)
