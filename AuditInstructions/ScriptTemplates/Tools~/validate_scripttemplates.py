"""Static checks for the script templates; reads only this folder. Run from anywhere."""
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


optional_root = FOLDER / "OptionalScriptTemplates"
defaults = list(FOLDER.glob("*.cs.txt"))
optional = list(optional_root.glob("*.cs.txt"))
retired = list((optional_root / "ReferenceOnly").glob("*.cs.txt"))
require((len(defaults), len(optional), len(retired)) == (5, 12, 1),
        "Template selection inventory must be 5 default, 12 optional, 1 retired")

for path in defaults + optional + retired:
    require(bool(meta_guids(path)), f"Missing template metadata: {path.name}")
    content = path.read_text()
    tokens = set(re.findall(r"#[A-Z][A-Z0-9_]*#", content))
    require(tokens <= {"#SCRIPTNAME#", "#ROOTNAMESPACEBEGIN#", "#ROOTNAMESPACEEND#", "#NOTRIM#"},
            f"Unknown template tokens: {path.name}")
    require(content.count("#ROOTNAMESPACEBEGIN#") == content.count("#ROOTNAMESPACEEND#") == 1,
            f"Namespace tokens: {path.name}")
    require("#SCRIPTNAME#" in content, f"Missing script token: {path.name}")
    require(not re.search(r"#region|Assert\.Pass|UITKBaseClass|: IState|\[(Server|Client)Rpc\]", content),
            f"Stale scaffold: {path.name}")
    require(not re.search(r"\b[msk]_[A-Z]", re.sub(r'"[^"\n]*"', "", content)), f"Wrong prefix casing: {path.name}")

# SetupScriptTemplates.md carries a GUID table so a URL-only agent can verify downloads; it must match the metadata.
guide = (FOLDER / "SetupScriptTemplates.md").read_text()
documented = dict(re.findall(r"^\| \d+ \| [^|]+ \| `([^`]+)` \|.*\| `([0-9a-f]{32})` \|$", guide, re.M))
selectable = defaults + optional
require(len(documented) == len(selectable), f"SetupScriptTemplates.md GUID table lists {len(documented)} templates, expected {len(selectable)}")
for path in selectable:
    relative = path.relative_to(FOLDER).as_posix().removesuffix(".cs.txt")
    require(relative in documented, f"Undocumented template: {relative}")
    require(documented.get(relative) in meta_guids(path), f"SetupScriptTemplates.md GUID differs from metadata: {relative}")

# Unity 6.6+ warns (UAL0010/UAL0013) about static state without a lifecycle attribute when domain reload is off.
for path in selectable:
    content = path.read_text()
    has_static_state = re.search(r"\bstatic\s+event\b|\bstatic\s+(?!readonly\b|class\b|partial\b|void\b)[\w<>\[\],.? ]+?\s+\w+\s*(=|;)", content)
    if has_static_state:
        require("AutoStaticsCleanup" in content, f"Static state needs [AutoStaticsCleanup] or [NoAutoStaticsCleanup]: {path.name}")

for relative, expected in json.loads((Path(__file__).parent / "inventory.json").read_text()).items():
    path = FOLDER if relative == "." else FOLDER / relative
    require(path.exists(), f"Inventory resource missing: {relative}")
    require(expected in meta_guids(path), f"Resource GUID drift: {relative}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS script templates: {len(defaults) + len(optional) + len(retired)} sources, tokens and GUIDs verified")
