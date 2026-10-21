"""Dependency-free static checks for the starter checkout; does not import Unity assets."""
from pathlib import Path
from urllib.parse import unquote
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--resources-only", action="store_true", help="Check resource safety and inventories without scanning Markdown links")
parser.add_argument("--markdown-path", action="append", default=[], help="Limit Markdown checks to a repository-relative file; repeatable")
args = parser.parse_args()
errors = []
links = 0

def require(condition, message):
    if not condition:
        errors.append(message)

def headings(path):
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    counts = {}
    result = set()
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
        base = re.sub(r"[^\w\-\s]", "", title.lower()).replace(" ", "-")
        number = counts.get(base, 0)
        counts[base] = number + 1
        result.add(base if number == 0 else base + "-" + str(number))
    return result

markdown = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
if args.markdown_path:
    markdown = [ROOT / name for name in args.markdown_path]
for path in ([] if args.resources_only else markdown):
    content = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    for raw in re.findall(r"\[[^]]*\]\(([^)]+)\)", content):
        target = raw.strip().strip("<>")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        filename, _, anchor = unquote(target).partition("#")
        destination = (path.parent / filename).resolve() if filename else path
        links += 1
        require(destination.exists(), f"{path.relative_to(ROOT)}: missing link {target}")
        if anchor and destination.is_file() and destination.suffix == ".md":
            require(anchor in headings(destination), f"{path.relative_to(ROOT)}: missing anchor {target}")

guids = {}
for path in ROOT.rglob("*.meta"):
    if ".git" in path.parts:
        continue
    matches = re.findall(r"^guid: ([0-9a-f]{32})$", path.read_text(), re.M)
    require(len(matches) == 1, f"Invalid GUID: {path.relative_to(ROOT)}")
    require(path.with_suffix("").exists(), f"Orphan metadata: {path.relative_to(ROOT)}")
    if len(matches) == 1:
        guid = matches[0]
        require(guid not in guids, f"Duplicate GUID: {path.relative_to(ROOT)} and {guids.get(guid)}")
        guids[guid] = str(path.relative_to(ROOT))

presets = list((ROOT / "LLMInstructions/SetupInstructions/Presets").rglob("*.preset"))
require(len(presets) == 13, "Expected thirteen presets")
inventory = (ROOT / "LLMInstructions/SetupInstructions/Presets/readme.md").read_text()
for path in presets:
    require(path.name in inventory, f"Undocumented preset: {path.name}")
    require(Path(str(path) + ".meta").exists(), f"Missing preset metadata: {path.name}")
    content = path.read_text()
    properties = re.findall(r"propertyPath: (.+)", content)
    exclusions = content.partition("m_ExcludedProperties:")[2]
    excluded = set(re.findall(r"^  - (.+)$", exclusions, re.M))
    included = [p for p in properties if not any(p == e or p.startswith(e + ".") for e in excluded)]
    require(bool(excluded) and bool(included), f"Preset must be deliberately partial: {path.name}")
    for prop in included:
        require(not re.search(r"SpriteSheet|SpritePivot|SpriteBorder|ExternalObjects|PlatformSetting|UserData|AssetBundle", prop), f"Unsafe included preset property: {path.name}: {prop}")

defaults = list((ROOT / "LLMInstructions/SetupInstructions/ScriptTemplates").glob("*.cs.txt"))
optional = list((ROOT / "LLMInstructions/SetupInstructions/ScriptTemplates/OptionalScriptTemplates").glob("*.cs.txt"))
retired = list((ROOT / "LLMInstructions/SetupInstructions/ScriptTemplates/OptionalScriptTemplates/ReferenceOnly").glob("*.cs.txt"))
require((len(defaults), len(optional), len(retired)) == (5, 11, 1), "Template selection inventory must be 5 default, 11 optional, 1 retired")
for path in defaults + optional + retired:
    require(Path(str(path) + ".meta").exists(), f"Missing template metadata: {path.name}")
    content = path.read_text()
    tokens = set(re.findall(r"#[A-Z][A-Z0-9_]*#", content))
    require(tokens <= {"#SCRIPTNAME#", "#ROOTNAMESPACEBEGIN#", "#ROOTNAMESPACEEND#", "#NOTRIM#"}, f"Unknown template tokens: {path.name}")
    require(content.count("#ROOTNAMESPACEBEGIN#") == content.count("#ROOTNAMESPACEEND#") == 1, f"Namespace tokens: {path.name}")
    require("#SCRIPTNAME#" in content, f"Missing script token: {path.name}")
    require(not re.search(r"#region|Assert\.Pass|UITKBaseClass|: IState|\[(Server|Client)Rpc\]", content), f"Stale scaffold: {path.name}")
    require(not re.search(r"\b[msk]_[A-Z]", re.sub(r'"[^"\n]*"', "", content)), f"Wrong prefix casing: {path.name}")

agents = (ROOT / "AGENTS.md").read_text()
stack = (ROOT / "LLMInstructions/SetupInstructions/UnityTechStack.md").read_text()
require("6000.7.x" in stack, "Intended version must remain Unity 6.7")
require(not re.search(r"6000\.[0-9]|C# version:", agents), "AGENTS must route version choices to one source")
require("LLMInstructions/AuditGuides/ProjectReview.md" in agents and "LLMInstructions/SetupInstructions/README.md" in agents, "AGENTS routing missing")
require("preset" in (ROOT / "EditorConfig/.editorconfig").read_text(), "Preset formatter exclusion missing")
require("CLAUDE.md" not in (ROOT / ".gitignore").read_text().splitlines(), "CLAUDE compatibility stub ignored")
for directory in ("LLMInstructions/SetupInstructions", "LLMInstructions/AuditGuides"):
    for path in (ROOT / directory).rglob("*.md"):
        require(not re.search(r"setup-project\.sh|ConfigurePresets\.cs|unity-project-setup|tbkj-project-audit", path.read_text()), f"Missing/private automation dependency: {path.relative_to(ROOT)}")

resource_inventory = ROOT / "Tools/resource-inventory.json"
require(resource_inventory.exists(), "Resource identity inventory missing")
if resource_inventory.exists():
    for relative, expected in json.loads(resource_inventory.read_text()).items():
        path = ROOT / relative
        require(path.exists(), f"Inventory resource missing: {relative}")
        require(guids.get(expected) == relative + ".meta", f"Resource GUID drift: {relative}")

scene_root = ROOT / "LLMInstructions/SetupInstructions/SceneTemplates"
scene_templates = list(scene_root.rglob("*.scenetemplate"))
require(len(scene_templates) == 3, "Expected three initial scene templates")
for name in ("StrategySandbox", "UIPreview", "AssetLookDev"):
    for filename in (name + ".unity", name + ".scenetemplate", "Preview.png"):
        path = scene_root / name / filename
        require(path.exists(), f"Scene template resource missing: {name}/{filename}")
for path in scene_root.rglob("*"):
    if path.suffix == ".meta":
        continue
    require(Path(str(path) + ".meta").exists(), f"Scene template metadata missing: {path.relative_to(ROOT)}")
    if path.suffix == ".cs":
        require(not re.search(r"RailroadTycoon|StrategyCore|UnityEditor|NUnit", path.read_text()),
                f"Unexpected game/editor/test dependency: {path.relative_to(ROOT)}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
scope = "resource checks; Markdown links not checked" if args.resources_only else f"{len(markdown)} Markdown files, {links} local links/anchors"
print(f"PASS: {scope}, {len(guids)} unique GUIDs, {len(presets)} partial presets, {len(defaults) + len(optional) + len(retired)} script template sources, {len(scene_templates)} scene templates")
