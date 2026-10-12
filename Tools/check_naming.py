"""Check real Roslyn IDE1006 diagnostics; requires .NET 10 SDK/dotnet format."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"WrongInterface", "wrongLookup", "WrongInstance", "WrongStatic", "WrongConstant", "wrongProperty"}
with tempfile.TemporaryDirectory(prefix="starter-naming-") as temp:
    target = Path(temp)
    shutil.copy(ROOT / "EditorConfig/.editorconfig", target / ".editorconfig")
    # Explicit runner severity; the shipped IDE suggestions do not imply build enforcement.
    with (target / ".editorconfig").open("a") as config:
        config.write("\n[*.cs]\ndotnet_diagnostic.IDE1006.severity = warning\n")
    for fixture in ("Good", "Bad"):
        project = target / fixture
        project.mkdir()
        shutil.copy(ROOT / "Tools/NamingFixture" / (fixture + ".cs"), project / (fixture + ".cs"))
        (project / "Fixture.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>')
        restore = subprocess.run(["dotnet", "restore", str(project)], capture_output=True, text=True)
        if restore.returncode:
            raise SystemExit(restore.stdout + restore.stderr)
        report = project / "report"
        result = subprocess.run(["dotnet", "format", "style", str(project), "--no-restore", "--diagnostics", "IDE1006", "--severity", "info", "--verify-no-changes", "--report", str(report), "--verbosity", "diagnostic"], capture_output=True, text=True)
        reports = list(report.glob("*.json"))
        data = json.loads(reports[0].read_text()) if reports else []
        diagnostics = [change for item in data for change in item.get("FileChanges", []) if change.get("DiagnosticId") == "IDE1006"]
        if fixture == "Good":
            if result.returncode or diagnostics: raise SystemExit("Good naming fixture failed:\n" + result.stdout + result.stderr)
        else:
            if result.returncode != 2 or len(diagnostics) != len(EXPECTED):
                raise SystemExit("Expected six naming diagnostics:\n" + result.stdout + result.stderr + str(data))
            # One diagnostic at each deliberately invalid declaration proves rule intersections.
            lines = {change["LineNumber"] for change in diagnostics}
            if lines != {1, 2, 5, 6, 7, 8}: raise SystemExit("Unexpected diagnostic locations: " + str(lines))
            by_line = {change["LineNumber"]: change["FormatDescription"] for change in diagnostics}
            expected_messages = {1: "Missing prefix: 'I'", 2: "upper case", 5: "Missing prefix: 'm_'",
                                 6: "Missing prefix: 's_'", 7: "Missing prefix: 'k_'", 8: "upper case"}
            if not all(fragment in by_line[line] for line, fragment in expected_messages.items()):
                raise SystemExit("Unexpected naming rule selection: " + str(by_line))
        print(f"{fixture}: {len(diagnostics)} IDE1006 diagnostics (expected)")
print("Naming intersections verified with " + subprocess.check_output(["dotnet", "--version"], text=True).strip())
