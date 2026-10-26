"""Repository-wide static checks, then every topic folder's own validator.

Topic-specific checks live beside their content in <folder>/Tools~/validate_*.py and run on their
own. This runner only adds what spans folders: Markdown links, GUID uniqueness, and the AGENTS contract.
"""
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote
import argparse
import os
import re
import subprocess
import sys
from audit_contract import canonical_contract, contract_errors, published_entry_points

ROOT = Path(__file__).resolve().parents[2]  # repository root; this file is AuditInstructions/Tools/validate_all.py
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--resources-only", action="store_true", help="Skip the Markdown link and anchor scan")
parser.add_argument("--markdown-path", action="append", default=[], help="Limit Markdown checks to a repository-relative file; repeatable")
parser.add_argument("--require-dotnet", action="store_true", help="Fail if topic .NET checks cannot execute")
args = parser.parse_args()
if args.require_dotnet:
    os.environ["STARTER_REQUIRE_DOTNET"] = "1"
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


def exact_case(path):
    """True when every path component matches the on-disk spelling (macOS and Windows ignore case, Linux does not)."""
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True
    current = ROOT
    for part in relative.parts:
        if part not in {entry.name for entry in current.iterdir()}:
            return False
        current = current / part
    return True


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
        require(not destination.exists() or exact_case(destination), f"{path.relative_to(ROOT)}: link differs in letter case from the file on disk: {target}")
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

agents = (ROOT / "AGENTS.md").read_text()
stack = (ROOT / "AgentsInstructions/UnityTechStack/UnityTechStack.md").read_text()
require("6000.7.x" in stack, "Intended version must remain Unity 6.7")
require(not re.search(r"6000\.[0-9]|C# version:", agents), "AGENTS must route version choices to one source")
require("AuditInstructions/ProjectAuditGuides/ProjectReview.md" in agents and "AuditInstructions/SetupInstructions/README.md" in agents,
        "AGENTS routing missing")
require("preset" in (ROOT / "AgentsInstructions/CodeStyleGuide/EditorConfig/.editorconfig").read_text(), "Preset formatter exclusion missing")
require("CLAUDE.md" not in (ROOT / ".gitignore").read_text().splitlines(), "CLAUDE compatibility stub ignored")
for directory in ("AuditInstructions/SetupInstructions", "AuditInstructions/ProjectAuditGuides"):
    for path in (ROOT / directory).rglob("*.md"):
        require(not re.search(r"setup-project\.sh|ConfigurePresets\.cs|unity-project-setup|tbkj-project-audit", path.read_text()),
                f"Missing/private automation dependency: {path.relative_to(ROOT)}")

# Published entry points are discovered independently of their own opening text.
contract = canonical_contract(agents)
agent_documents = published_entry_points(ROOT)
for path in agent_documents:
    require(path.is_file(), f"Missing published entry point: {path.relative_to(ROOT)}")
    if path.is_file():
        for error in contract_errors(path.read_text(), contract):
            require(False, f"{path.relative_to(ROOT)}: {error}")

# Agent documents date their volatile facts ("Last verified: October 2026"); warn when they age.
STALE_DAYS = 183
warnings = []
for path in sorted((ROOT / "AuditInstructions").rglob("*.md")):
    for month in re.findall(r"Last verified:?\*{0,2}:? ?\*{0,2} ?([A-Z][a-z]+ 20[0-9]{2})", path.read_text()):
        try:
            age = (datetime.now() - datetime.strptime(month, "%B %Y")).days
        except ValueError:
            continue
        if age > STALE_DAYS:
            warnings.append(f"WARN stale ({month}, {age} days): {path.relative_to(ROOT)}")

installation = subprocess.run([sys.executable, "-I", str(ROOT / "AuditInstructions/Tools/check_installation.py")], capture_output=True, text=True)
print(installation.stdout.strip() or "FAIL installation staging", flush=True)
if installation.returncode:
    errors.append(installation.stderr.strip())

workflow = ROOT / ".github/workflows/repository-checks.yml"
require(workflow.is_file(), "Repository CI workflow missing")
if workflow.is_file():
    ci = workflow.read_text()
    require("contents: read" in ci and "persist-credentials: false" in ci, "Repository CI permissions/checkout changed")
    require("pull_request_target" not in ci and "secrets." not in ci, "Repository CI must stay secret-free")
    require("validate_all.py --require-dotnet" in ci and "check_naming.py" in ci, "Repository CI must run both validation commands")
    require("pull_request:" in ci and "push:" in ci and "workflow_dispatch:" in ci, "Repository CI triggers missing")
    require("timeout-minutes:" in ci, "Repository CI timeout missing")
    require(not re.search(r"uses: [^@\s]+@(main|master|latest)\b", ci), "Repository CI action must use a version tag or commit")

regression = subprocess.run([sys.executable, str(Path(__file__).with_name("test_audit_contract.py"))], capture_output=True, text=True)
print(regression.stdout.strip() or "FAIL audit workflow regressions")
if regression.returncode:
    errors.append(regression.stderr.strip())

validators = sorted(ROOT.glob("*/Tools~/validate_*.py")) + sorted(ROOT.glob("AuditInstructions/*/Tools~/validate_*.py")) + sorted(ROOT.glob("AuditInstructions/*/*/Tools~/validate_*.py"))
for script in validators:
    result = subprocess.run([sys.executable, "-I", str(script)], capture_output=True, text=True)
    print(result.stdout.strip() or f"FAIL {script.relative_to(ROOT)}", flush=True)
    if result.returncode:
        errors.append(f"{script.relative_to(ROOT)}:\n{result.stderr.strip()}")

print("\n".join(warnings)) if warnings else None
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
scope = "Markdown links not checked" if args.resources_only else f"{len(markdown)} Markdown files, {links} local links/anchors"
print(f"PASS repository: {scope}, {len(guids)} unique GUIDs, {len(validators)} folder validators")
