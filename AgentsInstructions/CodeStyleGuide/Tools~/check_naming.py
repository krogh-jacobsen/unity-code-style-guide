"""Check real Roslyn IDE1006 naming diagnostics; requires the .NET 10 SDK (dotnet format).

Default (no arguments): self-test. The kit's .editorconfig must produce no diagnostics on
NamingFixture/Good.cs and exactly six, one per rule intersection, on NamingFixture/Bad.cs.

--target <project> [--editorconfig <file>] [--exclude NAME ...] [--json-out FILE]:
read-only count of naming-rule violations in a Unity project's owned C#, split into runtime,
Editor, and test code. The Unity CLI exposes compile errors (`unity recompile`, console) but not
IDE analyzers, so this copies the owned files under the chosen .editorconfig into a temporary
folder, builds a throwaway SDK project, and runs `dotnet format style --verify-no-changes`.
Unity types do not resolve there; IDE1006 needs only declarations, so naming counts still hold.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]  # CodeStyleGuide folder, for EditorConfig/.editorconfig
FIXTURES = Path(__file__).resolve().parent / "NamingFixture"
KIT_EDITORCONFIG = ROOT / "EditorConfig/.editorconfig"
EXPECTED = {"WrongInterface", "wrongLookup", "WrongInstance", "WrongStatic", "WrongConstant", "wrongProperty"}
# Folder names (any path segment, case-insensitive) treated as vendor, sample, or generated code.
DEFAULT_EXCLUDES = ["ThirdParty", "ThirdPartyAssets", "3rdParty", "3rdPartyAssets", "Vendor", "Plugins",
                    "Samples", "Sample", "TextMesh Pro", "AssetStoreTools", "_Recovery", "AI Toolkit"]
GROUPS = ("runtime", "editor", "tests")
CSPROJ = ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework>'
          '<Nullable>disable</Nullable><ImplicitUsings>disable</ImplicitUsings>{extra}</PropertyGroup></Project>')


def write_editorconfig(source, target):
    shutil.copy(source, target / ".editorconfig")
    # Explicit runner severity; the shipped IDE suggestions do not imply build enforcement.
    with (target / ".editorconfig").open("a") as config:
        config.write("\n[*.cs]\ndotnet_diagnostic.IDE1006.severity = warning\n")


def run_format(project):
    restore = subprocess.run(["dotnet", "restore", str(project)], capture_output=True, text=True)
    if restore.returncode:
        raise SystemExit(restore.stdout + restore.stderr)
    report = project / "report"
    result = subprocess.run(["dotnet", "format", "style", str(project), "--no-restore", "--diagnostics", "IDE1006",
                             "--severity", "info", "--verify-no-changes", "--report", str(report),
                             "--verbosity", "diagnostic"], capture_output=True, text=True)
    reports = list(report.glob("*.json"))
    data = json.loads(reports[0].read_text()) if reports else []
    diagnostics = [dict(change, FilePath=item.get("FilePath", "")) for item in data
                   for change in item.get("FileChanges", []) if change.get("DiagnosticId") == "IDE1006"]
    return result, diagnostics


def self_test():
    with tempfile.TemporaryDirectory(prefix="starter-naming-") as temp:
        target = Path(temp)
        write_editorconfig(KIT_EDITORCONFIG, target)
        for fixture in ("Good", "Bad"):
            project = target / fixture
            project.mkdir()
            shutil.copy(FIXTURES / (fixture + ".cs"), project / (fixture + ".cs"))
            (project / "Fixture.csproj").write_text(CSPROJ.format(extra=""))
            result, diagnostics = run_format(project)
            if fixture == "Good":
                if result.returncode or diagnostics: raise SystemExit("Good naming fixture failed:\n" + result.stdout + result.stderr)
            else:
                if result.returncode != 2 or len(diagnostics) != len(EXPECTED):
                    raise SystemExit("Expected six naming diagnostics:\n" + result.stdout + result.stderr + str(diagnostics))
                # One diagnostic at each deliberately invalid declaration proves rule intersections.
                lines = {change["LineNumber"] for change in diagnostics}
                if lines != {1, 2, 5, 6, 7, 8}: raise SystemExit("Unexpected diagnostic locations: " + str(lines))
                by_line = {change["LineNumber"]: change["FormatDescription"] for change in diagnostics}
                expected_messages = {1: "Missing prefix: 'I'", 2: "upper case", 5: "Missing prefix: 'm_'",
                                     6: "Missing prefix: 's_'", 7: "Missing prefix: 'k_'", 8: "upper case"}
                if not all(fragment in by_line[line] for line, fragment in expected_messages.items()):
                    raise SystemExit("Unexpected naming rule selection: " + str(by_line))
                # The --target classifier must name the rule behind each message.
                rules = naming_rules(KIT_EDITORCONFIG)
                names = {classify(change["FormatDescription"], "", rules) for change in diagnostics}
                if not {"const_fields_should_have_k_prefix", "static_fields_should_have_s_prefix"} <= names:
                    raise SystemExit("Rule classifier failed: " + str(names))
            print(f"{fixture}: {len(diagnostics)} IDE1006 diagnostics (expected)")
    print("Naming intersections verified with " + subprocess.check_output(["dotnet", "--version"], text=True).strip())


# ---------------------------------------------------------------------------------------------
# --target
# ---------------------------------------------------------------------------------------------

def naming_rules(editorconfig):
    """Map each naming rule to its required prefix (or None) from an .editorconfig."""
    text = Path(editorconfig).read_text(encoding="utf-8", errors="replace")
    prefixes = dict(re.findall(r"^\s*dotnet_naming_style\.(\w+)\.required_prefix\s*=\s*(\S*)", text, re.M))
    rules = {}
    for rule, style in re.findall(r"^\s*dotnet_naming_rule\.(\w+)\.style\s*=\s*(\w+)", text, re.M):
        rules[rule] = prefixes.get(style) or None
    return rules


def classify(message, line_text, rules):
    """Name the rule behind one IDE1006 message, using the declaration line for capitalization."""
    match = re.search(r"Missing prefix: '([^']*)'", message)
    if match:
        owners = [rule for rule, prefix in rules.items() if prefix == match.group(1)]
        return owners[0] if len(owners) == 1 else f"missing prefix '{match.group(1)}'"
    if "upper case" in message:
        if re.search(r"\bconst\b", line_text):
            return "public constants: PascalCase"
        return "PascalCase (properties, methods, types; includes Unity interface members)"
    if "lower case" in message:
        return "camelCase after the prefix"
    detail = re.sub(r"^.*?Naming rule violation:\s*", "", message)
    return re.sub(r"'[^']*'", "'…'", detail).split(":")[0].strip() or message


def code_group(rel, text):
    parts = {p.lower() for p in Path(rel).parts[:-1]}
    if parts & {"tests", "test"} or re.search(r"\[\s*(Test|UnityTest)\b", text):
        return "tests"
    if "editor" in parts:
        return "editor"
    head = next((line.strip() for line in text.splitlines()
                 if line.strip() and not line.strip().startswith(("//", "/*", "*", "using"))), "")
    return "editor" if re.match(r"#if\s+UNITY_EDITOR\b", head) else "runtime"


def owned_sources(project, excludes):
    excludes = {e.lower() for e in excludes}
    roots = [project / "Assets"]
    packages = project / "Packages"
    if packages.is_dir():
        roots += [p for p in packages.iterdir() if p.is_dir() and (p / "package.json").is_file()]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and not d.endswith("~")
                           and d.lower() not in excludes]
            for name in filenames:
                if name.endswith(".cs"):
                    yield Path(dirpath, name).relative_to(project)


def area(rel):
    parts = Path(rel).parts
    return "/".join(parts[:2]) if len(parts) > 2 else parts[0]


def target_report(project, editorconfig, excludes):
    project = Path(project).resolve()
    if not (project / "Assets").is_dir():
        raise SystemExit(f"{project} has no Assets folder; not a Unity project")
    rules = naming_rules(editorconfig)
    files = {g: 0 for g in GROUPS}
    counts, areas, groups = {}, {}, {}
    with tempfile.TemporaryDirectory(prefix="starter-naming-target-") as temp:
        work = Path(temp)
        write_editorconfig(editorconfig, work)
        src = work / "src"
        for rel in owned_sources(project, excludes):
            text = (project / rel).read_text(encoding="utf-8", errors="replace")
            groups[rel.as_posix()] = code_group(rel.as_posix(), text)
            files[groups[rel.as_posix()]] += 1
            (src / rel).parent.mkdir(parents=True, exist_ok=True)
            (src / rel).write_text(text, encoding="utf-8")
        if not groups:
            raise SystemExit("No owned C# files found")
        (work / "Target.csproj").write_text(CSPROJ.format(
            extra="<EnableDefaultCompileItems>false</EnableDefaultCompileItems>"
                  "<OutputType>Library</OutputType><NoWarn>CS0246;CS0234;CS0103</NoWarn>").replace(
            "</Project>", '<ItemGroup><Compile Include="src/**/*.cs" /></ItemGroup></Project>'))
        result, diagnostics = run_format(work)
        if result.returncode not in (0, 2):
            raise SystemExit("dotnet format failed:\n" + result.stdout[-4000:] + result.stderr[-4000:])
        lines_cache = {}
        for change in diagnostics:
            rel = Path(change["FilePath"]).resolve().relative_to(src.resolve()).as_posix()
            if rel not in lines_cache:
                lines_cache[rel] = (src / rel).read_text(encoding="utf-8", errors="replace").splitlines()
            lines = lines_cache[rel]
            number = change.get("LineNumber", 0)
            line_text = lines[number - 1] if 0 < number <= len(lines) else ""
            rule = classify(change.get("FormatDescription", ""), line_text, rules)
            row = counts.setdefault(rule, {g: 0 for g in GROUPS})
            row[groups.get(rel, "runtime")] += 1
            areas.setdefault(rule, {}).setdefault(area(rel), 0)
            areas[rule][area(rel)] += 1
    return {"project": project.name, "editorconfig": Path(editorconfig).name, "namingRules": sorted(rules),
            "excludes": sorted(excludes),
            "files": files, "rules": counts,
            "topAreas": {r: sorted(a.items(), key=lambda kv: -kv[1])[:3] for r, a in areas.items()},
            "dotnet": subprocess.check_output(["dotnet", "--version"], text=True).strip()}


def markdown(report):
    f = report["files"]
    out = [f"### Naming check: {report['project']}", "",
           f"- Rules from `{report['editorconfig']}` ({len(report['namingRules'])} naming rules); "
           f"dotnet format {report['dotnet']}; IDE1006 only",
           f"- Owned C# files: {f['runtime']} runtime, {f['editor']} Editor, {f['tests']} tests "
           f"(excluded folders: {', '.join(report['excludes']) or 'none'})", "",
           "| Rule | Runtime | Editor | Tests | Total | Where most are |", "|---|---:|---:|---:|---:|---|"]
    for rule, row in sorted(report["rules"].items(), key=lambda kv: -sum(kv[1].values())):
        where = ", ".join(f"`{a}` {n}" for a, n in report["topAreas"][rule])
        out.append(f"| {rule} | {row['runtime']} | {row['editor']} | {row['tests']} | {sum(row.values())} | {where} |")
    if not report["rules"]:
        out.append("| (no IDE1006 diagnostics) | 0 | 0 | 0 | 0 | |")
    out += ["", "Counts are candidates: a documented project rule that differs from this .editorconfig is a "
                "conflict to record, not drift."]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", help="Unity project to scan (read-only); omit to run the self-test")
    parser.add_argument("--editorconfig", default=str(KIT_EDITORCONFIG),
                        help="naming rules to apply (default: the kit's .editorconfig)")
    parser.add_argument("--exclude", action="append", default=[], help="extra vendor/generated folder name")
    parser.add_argument("--no-default-excludes", action="store_true")
    parser.add_argument("--json-out", help="also write the result as JSON")
    args = parser.parse_args()
    if not args.target:
        self_test()
        return 0
    excludes = ([] if args.no_default_excludes else DEFAULT_EXCLUDES) + args.exclude
    report = target_report(args.target, args.editorconfig, excludes)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2))
    print(markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
