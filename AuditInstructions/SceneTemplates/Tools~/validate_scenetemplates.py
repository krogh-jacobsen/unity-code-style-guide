"""Static checks for the scene templates; reads only this folder. Run from anywhere.

Skips this Tools~ folder: Unity ignores it, and it legitimately uses Editor and test APIs.
"""
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


scene_templates = [p for p in FOLDER.rglob("*.scenetemplate") if "Tools~" not in p.parts]
require(len(scene_templates) == 3, "Expected three initial scene templates")
for name in ("StrategySandbox", "UIPreview", "AssetLookDev"):
    for filename in (name + ".unity", name + ".scenetemplate", "Preview.png"):
        require((FOLDER / name / filename).exists(), f"Scene template resource missing: {name}/{filename}")

for path in FOLDER.rglob("*"):
    if "Tools~" in path.parts or path.suffix in (".meta", ".md"):  # Markdown guides are not imported
        continue
    require(bool(meta_guids(path)), f"Scene template metadata missing: {path.relative_to(FOLDER)}")
    if path.suffix == ".cs":
        require(not re.search(r"RailroadTycoon|StrategyCore|UnityEditor|NUnit", path.read_text()),
                f"Unexpected game/editor/test dependency: {path.relative_to(FOLDER)}")

# SetupSceneTemplates.md carries a GUID table so a URL-only agent can verify downloads; it must match the metadata.
guide = (FOLDER / "SetupSceneTemplates.md").read_text()
documented = dict(re.findall(r"^\| [^|]+ \| `([^`]+)` \| `([0-9a-f]{32})` \|$", guide, re.M))
shipped = {p.relative_to(FOLDER).as_posix() for p in FOLDER.rglob("*")
           if "Tools~" not in p.parts and p.suffix not in (".meta", ".md")}
require(set(documented) == shipped, f"GUID table paths differ from shipped files: {sorted(set(documented) ^ shipped)}")
for relative, guid in documented.items():
    if (FOLDER / relative).exists():
        require(guid in meta_guids(FOLDER / relative), f"SetupSceneTemplates.md GUID differs from metadata: {relative}")

for relative, expected in json.loads((Path(__file__).parent / "inventory.json").read_text()).items():
    path = FOLDER if relative == "." else FOLDER / relative
    require(path.exists(), f"Inventory resource missing: {relative}")
    require(expected in meta_guids(path), f"Resource GUID drift: {relative}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS scene templates: {len(scene_templates)} templates, metadata and GUIDs verified")
