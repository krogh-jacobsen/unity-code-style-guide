"""Licence-free Unity project checks for CI: meta pairing, duplicate GUIDs, and test isolation.

Needs only Python 3 and a checkout: no Unity Editor, licence, or network. Run from anywhere:
    python3 check_unity_project.py [--project PATH]
Exits 1 on any error. Under GitHub Actions it emits annotations and a job summary.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--project", default=os.environ.get("UNITY_PROJECT_PATH", "."), help="Unity project root (contains Assets/)")
args = parser.parse_args()
PROJECT = Path(args.project).resolve()
ASSETS = PROJECT / "Assets"
if not ASSETS.is_dir():
    raise SystemExit(f"No Assets folder under {PROJECT}")

errors, notices = [], []
on_actions = os.environ.get("GITHUB_ACTIONS") == "true"


def report(kind, path, message):
    relative = path.relative_to(PROJECT).as_posix() if path else ""
    (errors if kind == "error" else notices).append(f"{relative}: {message}" if relative else message)
    if on_actions:
        location = f" file={relative}" if relative else ""
        print(f"::{kind}{location}::{message}")


def unity_ignores(path):
    """Unity skips dot-prefixed and tilde-suffixed names, 'cvs', and .tmp files when importing."""
    name = path.name
    return name.startswith(".") or name.endswith("~") or name.lower() == "cvs" or name.lower().endswith(".tmp")


def walk(root):
    for entry in sorted(root.iterdir()):
        if unity_ignores(entry):
            continue
        yield entry
        if entry.is_dir():
            yield from walk(entry)


assets, metas = [], []
for entry in walk(ASSETS):
    (metas if entry.suffix == ".meta" else assets).append(entry)

# Every asset needs a .meta beside it, and every .meta needs its asset.
asset_names = {p.as_posix() for p in assets}
for asset in assets:
    if not Path(asset.as_posix() + ".meta").exists():
        report("error", asset, "has no .meta file; commit the .meta Unity generated, or references to it will break")
for meta in metas:
    if meta.with_suffix("").as_posix() not in asset_names:
        report("error", meta, "is an orphan .meta file: its asset is missing (deleted without its .meta, or ignored by .gitignore)")

# GUIDs must be unique across the project.
guids = {}
for meta in metas:
    found = re.findall(r"^guid: ([0-9a-f]{32})\s*$", meta.read_text(errors="replace"), re.M)
    if len(found) != 1:
        report("error", meta, "has no single valid guid line")
        continue
    if found[0] in guids:
        report("error", meta, f"duplicates the GUID of {guids[found[0]]}")
    guids[found[0]] = meta.relative_to(PROJECT).as_posix()

# Resolve effective assemblies before judging test isolation. An asmref names an asmdef;
# it does not carry that definition's configuration. Embedded packages can own definitions too.
definitions, by_name, by_guid, boundaries = {}, {}, {}, {}
assembly_files = [p for p in assets if p.suffix in (".asmdef", ".asmref")]
packages = PROJECT / "Packages"
if packages.is_dir():
    for package in sorted(packages.iterdir()):
        if package.is_dir() and (package / "package.json").is_file():
            assembly_files.extend(p for p in walk(package) if p.suffix in (".asmdef", ".asmref"))

for path in assembly_files:
    try:
        definition = json.loads(path.read_text(errors="replace"))
        if not isinstance(definition, dict):
            raise ValueError("expected an object")
    except (ValueError, OSError):
        report("error", path, "is not valid JSON assembly configuration")
        definition = {}
    if path.parent in boundaries:
        report("error", path, "shares a folder with another assembly definition/reference")
    boundaries[path.parent] = (path, definition)
    if path.suffix == ".asmdef":
        definitions[path] = definition
        name = definition.get("name")
        if name:
            if name in by_name:
                report("error", path, f"duplicates assembly name {name}")
            by_name[name] = path
        metadata = Path(str(path) + ".meta")
        if metadata.is_file():
            match = re.search(r"^guid: ([0-9a-f]{32})\s*$", metadata.read_text(), re.M)
            if match:
                by_guid[match[1]] = path


def resolve_reference(reference):
    if not isinstance(reference, str):
        return None
    return by_guid.get(reference[5:]) if reference.startswith("GUID:") else by_name.get(reference)


for folder, (path, definition) in list(boundaries.items()):
    if path.suffix == ".asmref":
        reference = definition.get("reference")
        target = resolve_reference(reference)
        if target is None:
            if not isinstance(reference, str) or not reference:
                report("error", path, "asmref requires a non-empty reference string")
            else:
                report("notice", path, "Not verified: asmref target cannot be resolved from Assets or embedded Packages; inspect resolved registry/git packages in Unity")
            boundaries[folder] = (path, {"unresolvedAsmref": True})
        else:
            boundaries[folder] = (target, definitions[target])


def is_test_assembly(definition):
    if "TestAssemblies" in definition.get("optionalUnityReferences", []):
        return True
    references = set()
    for reference in definition.get("references", []):
        target = resolve_reference(reference)
        references.add(definitions[target].get("name") if target else reference)
    # A define constraint only gates compilation; it does not add test-framework references.
    nunit_configured = ("nunit.framework.dll" in definition.get("precompiledReferences", [])
                        and definition.get("overrideReferences") is True)
    if nunit_configured and "UnityEngine.TestRunner" in references:
        return True
    if nunit_configured and any(isinstance(r, str) and r.startswith("GUID:") and resolve_reference(r) is None
                                for r in definition.get("references", [])):
        return None  # Framework assembly identities may live in unresolved registry/git packages.
    return False


def owning_definition(path):
    for folder in [path.parent, *path.parent.parents]:
        if folder in boundaries:
            return boundaries[folder]
        if folder == ASSETS:
            break
    return None, None


test_files = tests = ignored = 0
for path in assets:
    if path.suffix != ".cs":
        continue
    text = path.read_text(errors="replace")
    count = len(re.findall(r"^\s*\[(?:Test|UnityTest|TestCase)\b", text, re.M))
    if not count and "using NUnit.Framework" not in text:
        continue
    test_files += 1
    tests += count
    ignored += len(re.findall(r"^\s*\[Ignore\b", text, re.M))
    assembly_path, definition = owning_definition(path)
    if definition and definition.get("unresolvedAsmref"):
        # Resolved registry/git packages are not necessarily present in a plain CI checkout.
        # Do not turn unavailable dependency evidence into a false configuration defect.
        continue
    elif definition is None:
        if "Editor" in path.relative_to(ASSETS).parts[:-1]:
            report("notice", path, "uses a predefined Editor assembly; verify discovery with the installed Test Framework")
        else:
            report("error", path, "contains test code but no assembly definition covers it; inspect player isolation in Unity")
    elif is_test_assembly(definition) is None:
        report("notice", path, "Not verified: test-framework GUID references need resolved package metadata and Unity discovery")
    elif not is_test_assembly(definition):
        if definition.get("includePlatforms") == ["Editor"]:
            report("notice", path, "is Editor-only but lacks recognized test configuration; verify test discovery in Unity")
        else:
            report("error", path, f"contains test code, but {assembly_path.relative_to(PROJECT).as_posix()} is not a test assembly")
if ignored:
    report("notice", None, f"{ignored} [Ignore] attributes found; inspect reasons and report skipped tests separately from passes")

summary = [
    "## Unity project checks (no Unity licence)",
    "",
    f"- {len(assets)} assets and {len(metas)} meta files checked; {len(guids)} unique GUIDs",
    f"- {tests} tests in {test_files} test files; {ignored} are `[Ignore]`d",
    f"- **{len(errors)} errors**",
    "",
    "> **Editor tests were not run here.** This job needs no Unity licence, so EditMode and PlayMode tests",
    "> are not executed. A green check means these static checks passed; discovery and normal-player isolation still need Unity.",
    "> Run `unity test` locally before merging.",
]
summary += ["", *[f"- ERROR {line}" for line in errors]] if errors else []
summary += ["", *[f"- NOTICE {line}" for line in notices]] if notices else []
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as handle:
        handle.write("\n".join(summary) + "\n")

if errors:
    print("\n".join(f"ERROR {line}" for line in errors), file=sys.stderr)
    raise SystemExit(1)
for notice in notices:
    print(f"NOTICE {notice}")
print(f"PASS unity project: {len(assets)} assets, {len(metas)} metas, {tests} tests in {test_files} files ({ignored} ignored)")
