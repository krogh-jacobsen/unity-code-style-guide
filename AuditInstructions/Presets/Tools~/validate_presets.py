"""Static checks for the import presets; reads only this folder. Run from anywhere."""
import json
import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def meta_guids(asset):
    meta = asset.parent / (asset.name + ".meta")
    return re.findall(r"^guid: ([0-9a-f]{32})$", meta.read_text(), re.M) if meta.exists() else []


presets = sorted(FOLDER.rglob("*.preset"))
require(len(presets) == 13, "Expected thirteen presets")

# SetupPresets.md carries a GUID table so a URL-only agent can verify downloads; it must match the metadata.
guide = (FOLDER / "SetupPresets.md").read_text()
documented = dict(re.findall(r"^\| `([A-Za-z]+/[A-Za-z]+)` \|.*\| `([0-9a-f]{32})` \|$", guide, re.M))
require(len(documented) == len(presets), f"SetupPresets.md GUID table lists {len(documented)} presets, expected {len(presets)}")

for path in presets:
    relative = path.relative_to(FOLDER).with_suffix("").as_posix()
    require(relative in documented, f"Undocumented preset: {path.name}")
    require(documented.get(relative) in meta_guids(path), f"SetupPresets.md GUID differs from metadata: {relative}")
    require(bool(meta_guids(path)), f"Missing preset metadata: {path.name}")
    content = path.read_text()
    properties = re.findall(r"propertyPath: (.+)", content)
    excluded = set(re.findall(r"^  - (.+)$", content.partition("m_ExcludedProperties:")[2], re.M))
    included = [p for p in properties if not any(p == e or p.startswith(e + ".") for e in excluded)]
    require(bool(excluded) and bool(included), f"Preset must be deliberately partial: {path.name}")
    for prop in included:
        require(not re.search(r"SpriteSheet|SpritePivot|SpriteBorder|ExternalObjects|PlatformSetting|UserData|AssetBundle", prop),
                f"Unsafe included preset property: {path.name}: {prop}")

for relative, expected in json.loads((Path(__file__).parent / "inventory.json").read_text()).items():
    path = FOLDER if relative == "." else FOLDER / relative
    require(path.exists(), f"Inventory resource missing: {relative}")
    require(expected in meta_guids(path), f"Resource GUID drift: {relative}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS presets: {len(presets)} partial presets, GUID table matches metadata and inventory")
