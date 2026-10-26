"""Behavioral checks for Unity.gitignore and Unity.gitattributes; reads only this folder.

Builds a throwaway Git repository, installs both files, and asks Git itself what is ignored,
what stays tracked, and which files route to LFS. Run from anywhere; needs `git` on PATH.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]
errors = []

IGNORED = [
    "Library/x", "Temp/x", "Obj/x", "Logs/x", "UserSettings/Layouts/default.dwlt", "Assets/a.log",
    "MemoryCaptures/a.snap", "Recordings/take.mp4", "Builds/Win/Game.exe",
    "Builds/Win/Game_BurstDebugInformation_DoNotShip/x", "Builds/Win/Game_BackUpThisFolder_ButDontShipItWithYourGame/x",
    "ProfilerCaptures/capture.data", "Assets/ProfilerCaptures/capture.data", "Assets/ProfilerCaptures.meta",
    "Notes/run.pdata", "Notes/run.snap", "Notes/frame.rdc", "Notes/run.diagsession", "Notes/run.etl",
    "Assets/ThirdPartyAssets/Vendor/Tool.cs", "Assets/ThirdPartyAssets/Vendor/Tool.cs.meta", "Assets/ThirdPartyAssets.meta",
    "Game.sln", "Game.csproj", "Game.slnx", "mono_crash.1.json", "sysinfo.txt", "Assets/InitTestScene123.unity",
    "Assets/StreamingAssets/aa/catalog.json", ".vs/x", ".idea/workspace.xml", ".vscode/settings.json",
    ".DS_Store", "Thumbs.db", "Game.apk", "Game.aab", "Game.ipa", "Assets/Plugins/Editor/JetBrains/x.dll",
]
TRACKED = [
    "Assets/Game/Scripts/Player.cs", "Assets/Game/Scripts/Player.cs.meta", "Assets/Game.meta",
    "Assets/Scenes/Main.unity", "Assets/Settings/Build Profiles/Windows.asset", "Assets/Plugins/Native.dll",
    "Assets/StreamingAssets/settings.json", "ProjectSettings/ProjectSettings.asset", "ProjectSettings/ProjectVersion.txt",
    "Packages/manifest.json", "Packages/packages-lock.json", "ArtSource/hero.psd", ".vscode/extensions.json",
    "Assets/ThirdPartyAssetsExtra/Own.cs", "Assets/Game/ThirdPartyAssets/Own.cs", "Assets/Game/ProfilerNotes.md",
    ".editorconfig",
]
LFS = ["Assets/Game/Art/a.png", "Assets/Game/Art/a.tga", "Assets/Game/Art/model.fbx", "Assets/Game/Audio/a.wav",
       "Assets/Game/Video/a.mp4", "ArtSource/hero.psd", "ArtSource/rig.blend"]
EOL_LF = ["Assets/Game/Scripts/Player.cs", "Assets/Scenes/Main.unity", "Assets/Game/UI/Hud.uxml", "Assets/Game/Player.prefab.meta"]
NOT_LFS = ["Assets/Game/Scripts/Player.cs", "Assets/Scenes/Main.unity", "Assets/Game/Data/Config.asset", "Packages/manifest.json"]


def require(condition, message):
    if not condition:
        errors.append(message)


def git(repo, *args, check=False):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


def attribute(repo, name, path):
    return git(repo, "check-attr", name, "--", path).stdout.rsplit(": ", 1)[-1].strip()


ignore = (FOLDER / "Unity.gitignore").read_text()
attributes = (FOLDER / "Unity.gitattributes").read_text()

for label, text, name in (("ignore", ignore, "Unity ignore rules"), ("attributes", attributes, "Unity attributes")):
    require(text.count(f"# BEGIN unity-code-style-guide: {name}") == 1 and text.count(f"# END unity-code-style-guide: {name}") == 1,
            f"Unity.git{label} must contain exactly one managed block")
require(ignore.count("# BEGIN ThirdPartyAssets") == 1 and ignore.count("# END ThirdPartyAssets") == 1,
        "ThirdPartyAssets section markers missing or duplicated")
require(attributes.count("# BEGIN LFS") == 1 and attributes.count("# END LFS") == 1, "LFS section markers missing or duplicated")
require(not re.search(r"merge=unityyamlmerge", attributes), "Merge drivers belong to `unity vcs merge-setup`, not this file")
require(not re.search(r"^\*\.meta\s*$|^\*\*/\*\.meta\s*$", ignore, re.M), "A blanket rule ignores every .meta file")

with tempfile.TemporaryDirectory() as temp:
    repo = Path(temp)
    git(repo, "init", "-q", check=True)
    (repo / ".gitignore").write_text(ignore)
    (repo / ".gitattributes").write_text(attributes)
    for relative in IGNORED + TRACKED + LFS + EOL_LF + NOT_LFS:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x")
    for relative in IGNORED:
        require(git(repo, "check-ignore", "-q", "--", relative).returncode == 0, f"Expected ignored: {relative}")
    for relative in TRACKED + LFS + EOL_LF + NOT_LFS:
        require(git(repo, "check-ignore", "-q", "--", relative).returncode == 1, f"Expected tracked, but ignored: {relative}")
    for relative in LFS:
        require(attribute(repo, "filter", relative) == "lfs", f"Expected LFS: {relative}")
    for relative in NOT_LFS:
        require(attribute(repo, "filter", relative) == "unspecified", f"Must not route to LFS: {relative}")
    for relative in EOL_LF:
        require(attribute(repo, "eol", relative) == "lf", f"Expected eol=lf: {relative}")
    git(repo, "add", "-A")
    staged = set(git(repo, "ls-files").stdout.splitlines())
    require(not any(p.startswith(("Library/", "Temp/", "Builds/", "ProfilerCaptures/", "Assets/ThirdPartyAssets/")) for p in staged),
            "git add -A staged generated or excluded content")


def without(text, begin, end):
    return re.sub(rf"^{re.escape(begin)}.*?^{re.escape(end)}[^\n]*\n", "", text, flags=re.S | re.M)


# Declining an optional section must leave a working file that no longer applies that policy.
with tempfile.TemporaryDirectory() as temp:
    repo = Path(temp)
    git(repo, "init", "-q", check=True)
    trimmed_ignore = without(ignore, "# BEGIN ThirdPartyAssets", "# END ThirdPartyAssets")
    trimmed_attributes = without(attributes, "# BEGIN LFS", "# END LFS")
    (repo / ".gitignore").write_text(trimmed_ignore)
    (repo / ".gitattributes").write_text(trimmed_attributes)
    require("ThirdPartyAssets" not in trimmed_ignore and "lfs" not in trimmed_attributes, "Optional sections were not fully removable")
    require(git(repo, "check-ignore", "-q", "--", "Assets/ThirdPartyAssets/Vendor/Tool.cs").returncode == 1,
            "ThirdPartyAssets must be tracked once its section is removed")
    require(git(repo, "check-ignore", "-q", "--", "Library/x").returncode == 0, "Removing a section dropped other ignore rules")
    require(attribute(repo, "filter", "Assets/a.png") == "unspecified", "LFS still applies after its section is removed")
    require(attribute(repo, "eol", "Assets/a.cs") == "lf", "Removing LFS dropped the text rules")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS version control: {len(IGNORED)} ignored, {len(TRACKED)} tracked, {len(LFS)} LFS paths verified with git")
