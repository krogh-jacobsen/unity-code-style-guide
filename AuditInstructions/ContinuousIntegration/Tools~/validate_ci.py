"""Checks the CI starter files; reads only this folder. Run from anywhere.

Runs the project check script against good and deliberately broken fixture projects, lints the
workflows for safety properties, and, when the .NET SDK is installed, proves the style gates pass on
clean code and fail on bad code with the shipped EditorConfig.
"""
import re
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
ROOT = FOLDER.parents[1]
SCRIPT = FOLDER / "Scripts" / "check_unity_project.py"
errors = []
notes = []
fixture_count = 0


def require(condition, message):
    if not condition:
        errors.append(message)


def write(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def meta(path, guid):
    write(Path(str(path) + ".meta"), f"fileFormatVersion: 2\nguid: {guid}\n")


CLEAN_PLAYER = """using UnityEngine;

namespace Game
{
    public sealed class Player : MonoBehaviour
    {
        private int m_health = 3;
    }
}
"""
TESTS = "using NUnit.Framework;\n\npublic class PlayerTests\n{\n    [Test]\n    public void Works() { }\n\n    [Ignore(\"later\")]\n    [Test]\n    public void Placeholder() { }\n}\n"


def project(root):
    """A minimal valid Unity project: code, a test assembly with tests, and hidden folders."""
    for name, guid in (("Game", "a" * 32),):
        (root / "Assets" / name).mkdir(parents=True)
        meta(root / "Assets" / name, guid)
    write(root / "Assets/Game/Player.cs", CLEAN_PLAYER)
    meta(root / "Assets/Game/Player.cs", "b" * 32)
    (root / "Assets/Game/Tests").mkdir()
    meta(root / "Assets/Game/Tests", "c" * 32)
    write(root / "Assets/Game/Tests/Game.Tests.asmdef", '{ "name": "Game.Tests", "optionalUnityReferences": ["TestAssemblies"] }')
    meta(root / "Assets/Game/Tests/Game.Tests.asmdef", "d" * 32)
    write(root / "Assets/Game/Tests/PlayerTests.cs", TESTS)
    meta(root / "Assets/Game/Tests/PlayerTests.cs", "e" * 32)
    write(root / "Assets/Game/.hidden/x.txt", "ignored by Unity: no meta needed")
    write(root / "Assets/Game/Docs~/y.txt", "ignored by Unity: no meta needed")


def run_check(root):
    global fixture_count
    fixture_count += 1
    return subprocess.run([sys.executable, "-I", str(SCRIPT), "--project", str(root)], capture_output=True, text=True)


def mutate(name, expected, change):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        project(root)
        change(root)
        result = run_check(root)
        require(result.returncode == 1 and expected in result.stderr, f"Fixture '{name}' should fail with '{expected}': {result.stderr or result.stdout}")


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    project(root)
    result = run_check(root)
    require(result.returncode == 0, f"Good fixture failed: {result.stderr}")
    require("1 ignored" in result.stdout or "(1 ignored)" in result.stdout, "Ignored placeholder tests were not counted")

mutate("missing meta", "has no .meta file", lambda r: write(r / "Assets/Game/NoMeta.json", "{}"))
mutate("orphan meta", "orphan .meta", lambda r: meta(r / "Assets/Game/Gone.cs", "f" * 32))
mutate("duplicate guid", "duplicates the GUID", lambda r: (write(r / "Assets/Game/Two.cs", "// x\n"), meta(r / "Assets/Game/Two.cs", "b" * 32)))
mutate("bad guid", "no single valid guid", lambda r: (write(r / "Assets/Game/Three.cs", "// x\n"), write(r / "Assets/Game/Three.cs.meta", "fileFormatVersion: 2\n")))
mutate("test outside a test assembly", "no assembly definition covers it",
       lambda r: (write(r / "Assets/Loose/Loose.cs", TESTS), meta(r / "Assets/Loose/Loose.cs", "1" * 32), meta(r / "Assets/Loose", "2" * 32)))
mutate("test inside a runtime assembly", "is not a test assembly",
       lambda r: (write(r / "Assets/Runtime/Runtime.asmdef", '{ "name": "Runtime" }'), meta(r / "Assets/Runtime/Runtime.asmdef", "3" * 32),
                  write(r / "Assets/Runtime/Bad.cs", TESTS), meta(r / "Assets/Runtime/Bad.cs", "4" * 32), meta(r / "Assets/Runtime", "5" * 32)))
mutate("invalid asmdef", "not valid JSON", lambda r: (write(r / "Assets/Game/Broken.asmdef", "{"), meta(r / "Assets/Game/Broken.asmdef", "6" * 32)))


def extra_test(root, location="Extra", definition=None, reference=None):
    folder = root / "Assets" / location
    folder.mkdir(parents=True, exist_ok=True)
    for parent in (folder, *folder.parents):
        if parent == root / "Assets":
            break
        if not Path(str(parent) + ".meta").exists():
            meta(parent, "8" * 31 + str(len(parent.parts) % 10))
    write(folder / "ExampleTests.cs", TESTS)
    meta(folder / "ExampleTests.cs", "9" * 32)
    if definition is not None:
        write(folder / "Extra.asmdef", json.dumps(definition))
        meta(folder / "Extra.asmdef", "1" * 32)
    if reference is not None:
        write(folder / "Extra.asmref", json.dumps({"reference": reference}))
        meta(folder / "Extra.asmref", "2" * 32)


def check_case(name, change, expected_code=0, expected=""):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        project(root)
        change(root)
        result = run_check(root)
        require(result.returncode == expected_code and expected in result.stdout + result.stderr,
                f"Fixture '{name}' expected exit {expected_code} and '{expected}': {result.stderr or result.stdout}")


check_case("named asmref", lambda r: extra_test(r, reference="Game.Tests"))
check_case("GUID asmref", lambda r: extra_test(r, reference="GUID:" + "d" * 32))
check_case("unresolved package asmref", lambda r: extra_test(r, reference="Missing.Tests"), 0, "Not verified: asmref target cannot be resolved")
check_case("invalid asmref", lambda r: extra_test(r, reference=""), 1, "requires a non-empty reference")
check_case("predefined Editor assembly", lambda r: extra_test(r, "Editor"), 0, "predefined Editor assembly")
check_case("Editor-only asmdef", lambda r: extra_test(r, definition={"name": "Extra", "includePlatforms": ["Editor"]}),
           0, "verify test discovery")
check_case("constraint is not test configuration", lambda r: extra_test(r, definition={"name": "Extra", "defineConstraints": ["UNITY_INCLUDE_TESTS"]}),
           1, "is not a test assembly")
check_case("NUnit alone is not test configuration", lambda r: extra_test(r, definition={"name": "Extra", "precompiledReferences": ["nunit.framework.dll"]}),
           1, "is not a test assembly")
check_case("explicit test references", lambda r: extra_test(r, definition={"name": "Extra", "overrideReferences": True,
           "references": ["UnityEngine.TestRunner"], "precompiledReferences": ["nunit.framework.dll"]}))
check_case("unresolved framework GUID", lambda r: extra_test(r, definition={"name": "Extra", "overrideReferences": True,
           "references": ["GUID:" + "7" * 32], "precompiledReferences": ["nunit.framework.dll"]}),
           0, "Not verified: test-framework GUID references")


def framework_guid(root):
    write(root / "Assets/Framework/Runtime.asmdef", '{"name":"UnityEngine.TestRunner"}')
    meta(root / "Assets/Framework", "5" * 32)
    meta(root / "Assets/Framework/Runtime.asmdef", "6" * 32)
    extra_test(root, definition={"name": "Extra", "overrideReferences": True,
               "references": ["GUID:" + "6" * 32], "precompiledReferences": ["nunit.framework.dll"]})


check_case("resolved framework GUID", framework_guid)
check_case("Editor folder under runtime asmdef", lambda r: (
    write(r / "Assets/Game/Game.asmdef", '{"name":"Game"}'), meta(r / "Assets/Game/Game.asmdef", "3" * 32),
    extra_test(r, "Game/Editor")), 1, "is not a test assembly")


def embedded_reference(root):
    folder = root / "Packages/com.example.tests"
    write(folder / "package.json", '{"name":"com.example.tests","version":"1.0.0"}')
    write(folder / "Tests.asmdef", '{"name":"Embedded.Tests","optionalUnityReferences":["TestAssemblies"]}')
    meta(folder / "Tests.asmdef", "4" * 32)
    extra_test(root, reference="GUID:" + "4" * 32)


check_case("embedded-package asmref", embedded_reference)

# Match the documented repository-root invocation, including spaces and a Unity subfolder.
with tempfile.TemporaryDirectory() as temp:
    repository = Path(temp)
    nested = repository / "Games/My Unity Project"
    project(nested)
    installed = repository / ".github/unity-ci/check_unity_project.py"
    installed.parent.mkdir(parents=True)
    shutil.copy(SCRIPT, installed)
    fixture_count += 1
    result = subprocess.run([sys.executable, str(installed), "--project", str(nested)], cwd=repository, capture_output=True, text=True)
    require(result.returncode == 0, f"Nested-project invocation failed: {result.stderr}")

# Workflow safety properties.
checks = (FOLDER / "Workflows" / "unity-checks.yml").read_text()
selfhosted = (FOLDER / "Workflows" / "unity-tests-self-hosted.yml").read_text()
for name, text in (("unity-checks.yml", checks), ("unity-tests-self-hosted.yml", selfhosted)):
    require("permissions:" in text and "contents: read" in text, f"{name}: least-privilege permissions missing")
    require("pull_request_target" not in text, f"{name}: must not use pull_request_target")
    require(not re.search(r"uses: [^@\s]+@(main|master|latest)\b", text), f"{name}: unpinned action")
require("secrets." not in checks and "UNITY_LICENSE" not in checks and "UNITY_SERVICE_ACCOUNT" not in checks,
        "unity-checks.yml must stay licence-free and secret-free")
require("lfs: false" in checks, "unity-checks.yml should skip LFS objects")
require("head.repo.full_name == github.repository" in selfhosted, "Self-hosted workflow must exclude fork pull requests")
require("runs-on: [self-hosted, unity]" in selfhosted, "Self-hosted workflow label changed")
require("not run" in checks.lower(), "unity-checks.yml must state that Editor tests do not run")
require("UNITY_PROJECT_PATH: ${{ github.workspace }}" in selfhosted, "Self-hosted project path must be configurable")
require("working-directory: ${{ env.UNITY_PROJECT_PATH }}" in selfhosted, "Self-hosted doctor must inspect the selected project")
require(selfhosted.count('unity test "$UNITY_PROJECT_PATH"') == 2, "Both test modes must explicitly target the selected project")
guide = (FOLDER / "SetupCI.md").read_text()
require('unity vcs doctor "$UNITY_PROJECT_PATH"' in guide and 'from the repository\nroot' in guide,
        "Local CI instructions must run from the repository root with an explicit project")
for script in re.findall(r"\.github/unity-ci/([\w.]+)", checks):
    require((FOLDER / "Scripts" / script).exists(), f"unity-checks.yml references a missing script: {script}")
if shutil.which("ruby"):
    for workflow in (FOLDER / "Workflows").glob("*.yml"):
        parsed = subprocess.run(["ruby", "-ryaml", "-e", "YAML.load_file(ARGV[0])", str(workflow)], capture_output=True, text=True)
        require(parsed.returncode == 0, f"{workflow.name} is not valid YAML: {parsed.stderr.strip()[:200]}")
else:
    notes.append("YAML syntax not checked (no ruby)")

# Style gates: clean code passes, bad code fails, using the shipped EditorConfig and lint project.
if shutil.which("dotnet"):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        project(root)
        shutil.copy(ROOT / "AgentsInstructions/CodeStyleGuide/EditorConfig/.editorconfig", root / ".editorconfig")
        lint = root / ".github/unity-ci"
        lint.mkdir(parents=True)
        shutil.copy(FOLDER / "Scripts/Lint.csproj", lint / "Lint.csproj")
        env = {"UNITY_PROJECT_PATH": str(root), "PATH": __import__("os").environ["PATH"], "HOME": __import__("os").environ.get("HOME", ""),
               "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"}

        def dotnet(*arguments):
            return subprocess.run(["dotnet", *arguments], capture_output=True, text=True, env=env, cwd=root, timeout=180)

        restore = dotnet("restore", str(lint / "Lint.csproj"))
        if restore.returncode:
            if os.environ.get("STARTER_REQUIRE_DOTNET") == "1":
                errors.append("Required style gates could not run: dotnet restore failed\n" + restore.stdout + restore.stderr)
            else:
                notes.append("style gates not verified (dotnet restore failed)")
        else:
            gates = {
                "whitespace": ["format", "whitespace", str(lint / "Lint.csproj"), "--no-restore", "--verify-no-changes"],
                "naming": ["format", "style", str(lint / "Lint.csproj"), "--no-restore", "--diagnostics", "IDE1006", "--severity", "info", "--verify-no-changes"],
            }
            for gate, command in gates.items():
                result = dotnet(*command)
                require(result.returncode == 0, f"Style gate '{gate}' failed on clean code:\n{result.stdout}{result.stderr}")
            write(root / "Assets/Game/Bad.cs", "using UnityEngine;\npublic class Bad : MonoBehaviour\n{\n\tprivate int badField;\n    public void Go(){   Debug.Log(\"x\");   }\n}\n")
            meta(root / "Assets/Game/Bad.cs", "7" * 32)
            for gate, command in gates.items():
                result = dotnet(*command)
                require(result.returncode == 2, f"Style gate '{gate}' did not fail on bad code:\n{result.stdout}{result.stderr}")
            write(root / "Assets/ThirdPartyAssets/Vendor/V.cs", "public class v_bad{private int Bad;}\n")
            os_gates = dotnet(*gates["naming"])
            require("ThirdPartyAssets" not in os_gates.stdout + os_gates.stderr, "Lint project must exclude ThirdPartyAssets")
else:
    if os.environ.get("STARTER_REQUIRE_DOTNET") == "1":
        errors.append("Required style gates could not run: no dotnet SDK")
    else:
        notes.append("style gates not verified (no dotnet SDK)")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS continuous integration: {fixture_count} fixture projects, workflow safety rules" + (f" ({'; '.join(notes)})" if notes else ", style gates") + " verified")
