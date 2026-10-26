"""Static identity checks for the CLI script example; reads only this folder. Run from anywhere."""
import json
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
errors = []


def meta_guids(asset):
    meta = asset.parent / (asset.name + ".meta")
    return re.findall(r"^guid: ([0-9a-f]{32})$", meta.read_text(), re.M) if meta.exists() else []


inventory = json.loads((Path(__file__).parent / "inventory.json").read_text())
for relative, expected in inventory.items():
    path = FOLDER if relative == "." else FOLDER / relative
    if not path.exists():
        errors.append(f"Inventory resource missing: {relative}")
    if expected not in meta_guids(path):
        errors.append(f"Resource GUID drift: {relative}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS CLI example: {len(inventory)} resource identities verified")
