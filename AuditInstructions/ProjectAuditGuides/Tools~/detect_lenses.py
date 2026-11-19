#!/usr/bin/env python3
"""Detect which project-review lenses apply to a Unity project. Read-only.

Implements the detection half of ProjectReview.md steps 1 and 2: for every lens it counts signals
in all of the project (raw) and in first-party content only (vendor, sample, and generated folders
excluded), then labels the lens Recommended, Optional, or Not detected.

Evidence comes from the highest available rung, and the report names each rung it dropped:
  1. `unity projects info --json`    engine version, render pipeline, packages
  2. `unity projects verify --json`  integrity summary for the integrity pass
  3. `unity command find_assets`     asset types, only when an Editor has this project open
  4. file listing, YAML class IDs in scenes/prefabs, and C# text search, for signals no command exposes

Usage:
  python3 detect_lenses.py <project> [--format markdown|json] [--json-out FILE]
                           [--exclude NAME ...] [--no-default-excludes]
                           [--optional LENS=REASON ...] [--policy-doc FILE ...] [--no-cli]
  python3 detect_lenses.py --self-test

The labels are a starting point for the menu, not a verdict: the agent still reads the evidence,
honours documented project decisions, and may move a lens with a stated reason.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass, field
from pathlib import Path

RECOMMENDED, OPTIONAL, NOT_DETECTED, INCLUDED = 'Recommended', 'Optional', 'Not detected', 'Included'

# Folder names (any path segment, case-insensitive) that hold vendor, sample, or generated content.
DEFAULT_EXCLUDES = [
    'ThirdParty', 'ThirdPartyAssets', '3rdParty', '3rdPartyAssets', 'Vendor', 'Plugins',
    'Samples', 'Sample', 'TextMesh Pro', 'AssetStoreTools', '_Recovery', 'AI Toolkit',
]

TEXT_EXTS = {'.cs', '.unity', '.prefab', '.asset', '.uxml', '.uss', '.controller', '.overrideController',
             '.mixer', '.inputactions', '.playable', '.asmdef', '.asmref', '.shader', '.hlsl',
             '.shadergraph', '.shadersubgraph', '.vfx'}
ASSET_EXTS = {'.png', '.jpg', '.jpeg', '.tga', '.psd', '.exr', '.tif', '.tiff', '.hdr', '.fbx', '.obj',
              '.blend', '.glb', '.gltf', '.wav', '.mp3', '.ogg', '.aif', '.aiff'}
YAML_EXTS = {'.unity', '.prefab'}

# --------------------------------------------------------------------------------------------
# Signals. kind: ext (file extensions), yaml (class IDs in scenes/prefabs), main (main object
# class ID of a .asset file), code (regex over C#, counted per file, in the given code scopes),
# package (manifest key prefix; package presence is always weak).
# `editor_type` is the fully-qualified type for `unity command find_assets` on the Editor rung.
# --------------------------------------------------------------------------------------------


@dataclass
class Signal:
    name: str
    kind: str
    match: object
    strong: bool = True
    scopes: tuple = ('runtime',)
    editor_type: str | None = None
    raw: int = 0
    first_party: int = 0
    paths: list = field(default_factory=list)
    source: str = 'files'


RUNTIME, EDITOR, TEST = 'runtime', 'editor', 'test'
TOOLING = (EDITOR, TEST)


def S(name, kind, match, strong=True, scopes=(RUNTIME,), editor_type=None):
    return Signal(name, kind, match, strong, scopes, editor_type)


def lens_signals():
    """Fresh signal objects per lens; order matches the ProjectReview.md lens table."""
    phys_query = r'\bPhysics\.(Raycast|RaycastAll|RaycastNonAlloc|Linecast|SphereCast\w*|BoxCast\w*|CapsuleCast\w*|Overlap\w*|ComputePenetration|ClosestPoint)\b'
    return {
        'Performance': [S('runtime C# files', 'code', r'\b(class|struct|interface|enum)\b')],
        'Rendering': [
            S('renderers/lights/LOD/particles (23, 137, 108, 205, 198)', 'yaml', {23, 137, 108, 205, 198}),
            S('shaders, Shader Graphs, VFX', 'ext', {'.shader', '.hlsl', '.shadergraph', '.shadersubgraph', '.vfx'},
              editor_type='UnityEngine.Shader'),
            S('renderer features/passes', 'code', r'\b(ScriptableRendererFeature|ScriptableRenderPass|RenderGraph)\b'),
            S('render pipeline package', 'package', ('com.unity.render-pipelines.',), strong=False),
        ],
        'Assets': [
            S('imported textures/models/audio', 'ext', ASSET_EXTS),
            S('Addressables package', 'package', ('com.unity.addressables',), strong=False),
        ],
        'Scenes': [
            S('scenes', 'ext', {'.unity'}, editor_type='UnityEditor.SceneAsset'),
            S('MonoBehaviours', 'code', r':\s*(MonoBehaviour|NetworkBehaviour)\b'),
            S('async code (Awaitable, Task, StartCoroutine)', 'code', r'\b(Awaitable|StartCoroutine)\b|\bTask(<|\.Run|\.Delay|\s)'),
        ],
        'Design': [
            S('commands, services, registries, shared events', 'code',
              r'\b(class|interface)\s+I?\w*(Command|Service|Registry|EventBus|Bus)\b|\bstatic\s+event\b'),
        ],
        'Persistence': [
            S('persistentDataPath / PlayerPrefs', 'code', r'\bApplication\.persistentDataPath\b|\bPlayerPrefs\.'),
            S('JSON/file I/O only', 'code', r'\bJsonUtility\.|\bFile\.(Write|Read|Open|Create)\w*\(|\bBinary(Writer|Reader)\b', strong=False),
        ],
        'UI Toolkit': [
            S('UXML/USS files', 'ext', {'.uxml', '.uss'}, editor_type='UnityEngine.UIElements.VisualTreeAsset'),
            S('UIElements in runtime code', 'code', r'\bUnityEngine\.UIElements\b|\bUIDocument\b|\bPanelSettings\b'),
            S('UIElements in Editor/test code only', 'code', r'\bUnityEngine\.UIElements\b', strong=False, scopes=TOOLING),
        ],
        'uGUI': [
            S('Canvas (223)', 'yaml', {223}),
            S('UnityEngine.UI in runtime code', 'code', r'\bUnityEngine\.UI\b'),
            S('UnityEngine.UI in Editor/test code only', 'code', r'\bUnityEngine\.UI\b', strong=False, scopes=TOOLING),
        ],
        'Input': [
            S('.inputactions assets', 'ext', {'.inputactions'}, editor_type='UnityEngine.InputSystem.InputActionAsset'),
            S('Input System or legacy Input in runtime code', 'code',
              r'\bUnityEngine\.InputSystem\b|\bInput\.(GetKey\w*|GetAxis\w*|GetButton\w*|GetMouseButton\w*|mousePosition)\b'),
            S('Input System package', 'package', ('com.unity.inputsystem',), strong=False),
        ],
        'Physics': [
            S('CharacterController (143)', 'yaml', {143}),
            S('contact callbacks', 'code', r'\bvoid\s+On(Collision|Trigger)(Enter|Stay|Exit)\s*\('),
            S('force-driven bodies', 'code',
              r'\.(AddForce|AddRelativeForce|AddTorque|AddExplosionForce|MovePosition|MoveRotation)\s*\(|\blinearVelocity\s*='),
            S('non-pointer physics queries', 'code', phys_query),  # downgraded per file when pointer picking
            S('Rigidbody (54) in content', 'yaml', {54}, strong=False),
            S('colliders only (65, 64, 135, 136)', 'yaml', {65, 64, 135, 136}, strong=False),
            S('pointer-picking raycasts', 'code', phys_query, strong=False),
        ],
        'Animation': [
            S('Animator Controllers', 'ext', {'.controller', '.overrideController'},
              editor_type='UnityEditor.Animations.AnimatorController'),
            S('Animator API in runtime code', 'code', r'\bAnimator\b|\bRuntimeAnimatorController\b'),
            S('Animator (95) components only', 'yaml', {95}, strong=False),
        ],
        'Audio': [
            S('mixers', 'ext', {'.mixer'}, editor_type='UnityEngine.Audio.AudioMixer'),
            S('AudioSource (82)', 'yaml', {82}),
            S('AudioSource/AudioMixer in runtime code', 'code', r'\b(AudioSource|AudioMixer|AudioMixerGroup)\b'),
        ],
        'Assemblies': [S('first-party .asmdef/.asmref', 'ext', {'.asmdef', '.asmref'})],
        'Testing': [
            S('[Test]/[UnityTest] code', 'code', r'\[\s*(Test|UnityTest|TestCase|TestCaseSource)\b', scopes=(RUNTIME, EDITOR, TEST)),
            S('Test Framework package', 'package', ('com.unity.test-framework',), strong=False),
        ],
        'Editor tooling': [
            S('menu items, editors, drawers, importers', 'code',
              r'\[\s*(MenuItem|InitializeOnLoad\w*|CustomEditor|CustomPropertyDrawer|ScriptedImporter)\b'
              r'|:\s*(EditorWindow|Editor|PropertyDrawer|AssetPostprocessor|ScriptedImporter|ScriptableWizard)\b',
              scopes=(EDITOR,)),
        ],
        'Navigation': [
            S('NavMesh API or components in code', 'code', r'\bNavMesh(Agent|Surface|Link|Obstacle|Modifier)?\b'),
            S('custom pathfinding', 'code', r'\b(class|struct)\s+\w*(Pathfind\w*|PathFinder|AStar|Dijkstra)\w*\b'),
            S('AI Navigation package', 'package', ('com.unity.ai.navigation',), strong=False),
        ],
        'Physics2D': [
            S('2D bodies/colliders (50, 58, 60, 61, 66, 68, 70)', 'yaml', {50, 58, 60, 61, 66, 68, 70}),
            S('Physics2D API or 2D callbacks', 'code', r'\bPhysics2D\.|\bRigidbody2D\b|\bCollider2D\b|\bOn(Collision|Trigger)(Enter|Stay|Exit)2D\b'),
        ],
        'Localization': [
            S('Localization API in code', 'code', r'\bUnityEngine\.Localization\b|\bLocalizedString\b|\bLocalizationSettings\b'),
            S('Localization package', 'package', ('com.unity.localization',), strong=False),
        ],
        'Networking': [
            S('network objects, RPCs, replication', 'code',
              r'\bNetworkBehaviour\b|\bNetworkObject\b|\[\s*(ServerRpc|ClientRpc|Rpc|SyncVar|Command)\b|\bNetworkVariable<'),
            S('networking package', 'package', ('com.unity.netcode', 'com.unity.transport', 'com.unity.services.multiplayer'), strong=False),
        ],
        'Entities': [
            S('ECS systems, jobs, bakers, SubScenes', 'code',
              r':\s*(ISystem|SystemBase|IJobEntity|IComponentData)\b|\bBaker<|\bEntityCommandBuffer\b|\bSubScene\b'),
            S('Entities package', 'package', ('com.unity.entities',), strong=False),
        ],
        'Terrain': [
            S('Terrain/TerrainCollider (218, 154)', 'yaml', {218, 154}),
            S('TerrainData assets (156)', 'main', {156}, editor_type='UnityEngine.TerrainData'),
            S('terrain API in code', 'code', r'\bTerrainData\b|\bSetHeights\w*\(|\bTerrain\.activeTerrain\b'),
        ],
        'Cameras': [
            S('camera rigs, Cinemachine, Timeline in code', 'code',
              r'\bCinemachine\w*\b|\bPlayableDirector\b|\b(class|struct)\s+\w*Camera\w*\b'),
            S('Timeline assets / PlayableDirector (320)', 'ext', {'.playable'}, editor_type='UnityEngine.Timeline.TimelineAsset'),
            S('PlayableDirector (320)', 'yaml', {320}),
            S('plain Camera (20) only', 'yaml', {20}, strong=False),
        ],
    }


LENS_FILES = {
    'Performance': 'UnityPerformanceOptimizationInstructions.md', 'Rendering': 'UnityRenderingInstructions.md',
    'Assets': 'UnityAssetsAndMemoryInstructions.md', 'Scenes': 'UnityScenesAndLifecycleInstructions.md',
    'Design': 'UnityDesignPatternsInstructions.md', 'Persistence': 'UnityPersistenceInstructions.md',
    'UI Toolkit': 'UnityUIToolkitInstructions.md', 'uGUI': 'UnityUGUIInstructions.md',
    'Input': 'UnityInputSystemInstructions.md', 'Physics': 'UnityPhysicsInstructions.md',
    'Animation': 'UnityAnimationInstructions.md', 'Audio': 'UnityAudioInstructions.md',
    'Assemblies': 'UnityAssemblyDefinitionsInstructions.md', 'Testing': 'UnityTestingInstructions.md',
    'Editor tooling': 'UnityEditorToolingInstructions.md', 'Navigation': 'UnityNavigationInstructions.md',
    'Physics2D': 'UnityPhysics2DInstructions.md', 'Localization': 'UnityLocalizationAccessibilityInstructions.md',
    'Networking': 'UnityNetworkingInstructions.md', 'Entities': 'UnityEntitiesInstructions.md',
    'Terrain': 'UnityTerrainInstructions.md', 'Cameras': 'UnityCamerasCinematicsInstructions.md',
}

ASMDEF_POLICY = re.compile(
    r'(without|\bno\b|not use|avoid\w*|do(es)? not (use|add))[^.\n]{0,40}\basmdefs?\b'
    r'|\bpredefined\b[^.\n]{0,40}\bassembl', re.I)
POINTER_PICK = re.compile(r'\b(ScreenPointToRay|ViewportPointToRay)\b')
EDITOR_GUARD = re.compile(r'#if\s+UNITY_EDITOR\b')


# --------------------------------------------------------------------------------------------
# Unity CLI rungs
# --------------------------------------------------------------------------------------------

def run_unity(args, timeout=120):
    """Run the Unity CLI and return parsed JSON, or (None, reason)."""
    exe = shutil.which('unity')
    if not exe:
        return None, 'unity CLI not on PATH'
    try:
        done = subprocess.run([exe, '--no-banner', '--no-pager', '--non-interactive', *args],
                              capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, f'{" ".join(args[:2])} failed: {error}'
    try:
        return json.loads(done.stdout), None
    except json.JSONDecodeError:
        return None, f'{" ".join(args[:2])} returned no JSON (exit {done.returncode})'


def cli_project_facts(project, rungs):
    data, error = run_unity(['projects', 'info', str(project), '--json'])
    if data and data.get('success'):
        d = data['data']
        rungs.append('`unity projects info`: used')
        return {'engine': d.get('version'), 'renderPipeline': d.get('renderPipeline'),
                'packages': d.get('packages') or {}}
    rungs.append(f'`unity projects info`: dropped ({error or "unsuccessful"}); read Packages/manifest.json')
    return None


def cli_verify(project, rungs):
    data, error = run_unity(['projects', 'verify', str(project), '--json'], timeout=600)
    if data and 'data' in data:
        d = data['data']
        rungs.append('`unity projects verify`: used')
        return {'ok': d.get('ok'), 'checks': d.get('checks'), 'summary': d.get('summary'),
                'findings': [f.get('code', f) if isinstance(f, dict) else f for f in d.get('findings', [])][:20]}
    rungs.append(f'`unity projects verify`: dropped ({error or "no data"}); integrity pass needs its own evidence')
    return None


def cli_editor_port(project, rungs):
    """Return the port of a ready Editor that has this project open, else None."""
    data, error = run_unity(['status', '--json'], timeout=30)
    if not data or not data.get('success'):
        rungs.append(f'Editor rung: dropped ({error or "status unavailable"})')
        return None
    target = os.path.realpath(project)
    for inst in (data.get('data') or {}).get('instances', []):
        path = inst.get('projectPath') or inst.get('project') or ''
        if path and os.path.realpath(path) == target and inst.get('state') == 'ready':
            root, _ = run_unity(['command', '--port', str(inst['port']), 'get_authoring_root', '--result-only'], 30)
            if not root or root.get('root') != 'Assets':
                rungs.append('Editor rung: dropped (authoring root is not `Assets`; not changed by this read-only tool)')
                return None
            rungs.append(f'Editor rung: used (`unity command find_assets`, port {inst["port"]})')
            return inst['port']
    rungs.append('Editor rung: dropped (no connected Editor has this project open)')
    return None


def editor_find_assets(port, type_name):
    data, _ = run_unity(['command', '--port', str(port), 'find_assets', '--type', type_name,
                         '--limit', '100000', '--result-only'], timeout=120)
    if not data or 'assets' not in data:
        return None
    return [a.get('assetPath') for a in data['assets'] if a.get('assetPath')]


# --------------------------------------------------------------------------------------------
# File rung
# --------------------------------------------------------------------------------------------

class Scope:
    def __init__(self, project, excludes):
        self.project = Path(project)
        self.excludes = {e.lower() for e in excludes}

    def excluded(self, rel):
        return any(part.lower() in self.excludes or part.endswith('~') for part in Path(rel).parts[:-1])


def project_files(project):
    """Yield project-relative paths under Assets and embedded packages."""
    roots = [project / 'Assets']
    packages = project / 'Packages'
    if packages.is_dir():
        roots += [p for p in packages.iterdir() if p.is_dir() and (p / 'package.json').is_file()]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            for name in filenames:
                if not name.endswith('.meta'):
                    yield Path(dirpath, name).relative_to(project).as_posix()


def code_scope(rel, text):
    parts = {p.lower() for p in Path(rel).parts[:-1]}
    if parts & {'tests', 'test'} or re.search(r'\[\s*(Test|UnityTest)\b', text):
        return TEST
    if 'editor' in parts:
        return EDITOR
    head = next((line.strip() for line in text.splitlines()
                 if line.strip() and not line.strip().startswith(('//', 'using', '/*', '*'))), '')
    return EDITOR if EDITOR_GUARD.match(head) else RUNTIME


def yaml_classes(path):
    counts = {}
    try:
        with open(path, 'rb') as handle:
            for line in handle:
                if line.startswith(b'--- !u!'):
                    m = re.match(rb'--- !u!(\d+) ', line)
                    if m:
                        cid = int(m.group(1))
                        counts[cid] = counts.get(cid, 0) + 1
    except OSError:
        pass
    return counts


def main_class(path):
    try:
        with open(path, 'rb') as handle:
            head = handle.read(4096)
    except OSError:
        return None
    m = re.search(rb'--- !u!(\d+) ', head)
    return int(m.group(1)) if m else None


def add(signal, rel, first_party, amount=1, keep=3):
    signal.raw += amount
    if first_party:
        signal.first_party += amount
        if len(signal.paths) < keep and rel not in signal.paths:
            signal.paths.append(rel)


def scan(project, scope, lenses, packages, editor_port=None):
    all_signals = [s for sigs in lenses.values() for s in sigs]
    editor_done = set()
    if editor_port:
        for s in all_signals:
            if s.editor_type:
                found = editor_find_assets(editor_port, s.editor_type)
                if found is not None:
                    s.source = f'find_assets {s.editor_type}'
                    editor_done.add(id(s))
                    for rel in found:
                        add(s, rel, not scope.excluded(rel))
    pointer_files = set()
    for rel in project_files(project):
        ext = Path(rel).suffix
        first_party = not scope.excluded(rel)
        path = project / rel
        for s in all_signals:
            if s.kind == 'ext' and ext in s.match and not (id(s) in editor_done and rel.startswith('Assets/')):
                add(s, rel, first_party)
        if ext in YAML_EXTS:
            classes = yaml_classes(path)
            for s in all_signals:
                if s.kind == 'yaml':
                    n = sum(classes.get(c, 0) for c in s.match)
                    if n:
                        add(s, rel, first_party, n)
        elif ext == '.asset':
            cid = main_class(path)
            for s in all_signals:
                if s.kind == 'main' and cid in s.match and id(s) not in editor_done:
                    add(s, rel, first_party)
        elif ext == '.cs':
            try:
                text = path.read_text(encoding='utf-8', errors='replace')
            except OSError:
                continue
            kind = code_scope(rel, text)
            pointer = bool(POINTER_PICK.search(text))
            for lens, sigs in lenses.items():
                for s in sigs:
                    if s.kind != 'code' or kind not in s.scopes or not re.search(s.match, text):
                        continue
                    if lens == 'Physics' and s.match.startswith(r'\bPhysics\.'):
                        # A query file that also builds a pointer ray is pointer picking (weak).
                        if s.strong == pointer:
                            continue
                        if pointer:
                            pointer_files.add(rel)
                    add(s, rel, first_party)
    for s in all_signals:
        if s.kind == 'package':
            hits = [p for p in packages if p.startswith(s.match)]
            s.raw = s.first_party = len(hits)
            s.paths = hits[:3]
            s.source = 'manifest'
    return pointer_files


# --------------------------------------------------------------------------------------------
# Labels
# --------------------------------------------------------------------------------------------

def policy_notes(project, extra_docs):
    notes = {}
    docs = [project / n for n in ('AGENTS.md', 'CLAUDE.md', 'README.md')] + [Path(d) for d in extra_docs]
    for doc in docs:
        if not doc.is_file():
            continue
        for number, line in enumerate(doc.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            if ASMDEF_POLICY.search(line):
                try:
                    where = doc.relative_to(project).as_posix()
                except ValueError:
                    where = doc.name
                notes.setdefault('Assemblies', f'documented policy ({where}:{number}) relies on predefined assemblies')
    return notes


def label_lens(lens, sigs, policy):
    strong = [s for s in sigs if s.strong and s.first_party]
    weak = [s for s in sigs if not s.strong and s.first_party]
    if lens == 'Audio':
        hits = strong + weak
        label = RECOMMENDED if len(hits) >= 2 else OPTIONAL if hits else NOT_DETECTED
        reason = f'{len(hits)} distinct audio signal(s); two or more are Recommended'
    elif lens == 'Testing':
        code = next(s for s in sigs if s.kind == 'code')
        package = any(s.first_party for s in sigs if s.kind == 'package')
        label = RECOMMENDED if code.first_party and package else OPTIONAL if code.first_party else NOT_DETECTED
        reason = 'test attributes plus Test Framework package' if label == RECOMMENDED else \
            'test attributes without the Test Framework package' if label == OPTIONAL else 'no test code ("no tests" is a scope fact)'
    elif strong:
        label, reason = RECOMMENDED, 'strong first-party signal'
    elif weak:
        label, reason = OPTIONAL, 'weak or partial signal only'
    else:
        label, reason = NOT_DETECTED, 'nothing detected'
    if lens == 'Assemblies' and not strong:
        reason = 'no first-party asmdef (absence is not a signal)'
    # A documented decision limits a detected lens; only the no-asmdef policy applies without a signal.
    if lens in policy and (label != NOT_DETECTED or lens == 'Assemblies'):
        label, reason = OPTIONAL, policy[lens]
    return label, reason


def integrity_text(verify):
    if not verify:
        return 'projects verify: not run'
    s = verify.get('summary') or {}
    return (f'projects verify: {"ok" if verify.get("ok") else "findings"} ({s.get("errors", "?")} errors, '
            f'{s.get("warnings", "?")} warnings, {s.get("filesScanned", "?")} files)')


def detect(project, excludes=DEFAULT_EXCLUDES, optional=None, policy_docs=(), use_cli=True):
    project = Path(project).resolve()
    rungs, facts, verify, port = [], None, None, None
    if use_cli:
        facts = cli_project_facts(project, rungs)
        verify = cli_verify(project, rungs)
        port = cli_editor_port(project, rungs)
    else:
        rungs.append('Unity CLI rungs: skipped (--no-cli)')
    if facts is None:
        manifest = project / 'Packages' / 'manifest.json'
        packages = json.loads(manifest.read_text()).get('dependencies', {}) if manifest.is_file() else {}
        version_file = project / 'ProjectSettings' / 'ProjectVersion.txt'
        engine = None
        if version_file.is_file():
            m = re.search(r'm_EditorVersion:\s*(\S+)', version_file.read_text())
            engine = m.group(1) if m else None
        facts = {'engine': engine, 'renderPipeline': None, 'packages': packages}
    rungs.append('File rung: file listing, YAML class IDs, C# text search for signals no command exposes')
    scope = Scope(project, excludes)
    lenses = lens_signals()
    pointer_files = scan(project, scope, lenses, facts['packages'], port)
    policy = policy_notes(project, policy_docs)
    for item in optional or []:
        lens, _, reason = item.partition('=')
        policy[lens.strip()] = f'documented decision: {reason.strip() or "stated by the user"}'
    rows = [{'lens': 'Integrity pass', 'file': 'UnityEditorToolingInstructions.md', 'label': INCLUDED,
             'reason': 'always on for a whole-project review', 'raw': None, 'firstParty': None,
             'evidence': [integrity_text(verify)], 'paths': []}]
    for lens, sigs in lenses.items():
        label, reason = label_lens(lens, sigs, policy)
        if lens == 'Physics' and pointer_files and label == OPTIONAL:
            reason += '; physics queries are pointer picking'
        evidence = [f'{s.name}: {s.first_party}/{s.raw}{"" if s.strong else " (weak)"}'
                    for s in sigs if s.raw]
        paths = [p for s in sigs if s.first_party and s.kind != 'package' for p in s.paths]
        rows.append({'lens': lens, 'file': LENS_FILES[lens], 'label': label, 'reason': reason,
                     'raw': sum(s.raw for s in sigs), 'firstParty': sum(s.first_party for s in sigs),
                     'evidence': evidence, 'paths': list(dict.fromkeys(paths))[:3],
                     'sources': sorted({s.source for s in sigs if s.raw})})
    return {'project': project.name, 'engine': facts['engine'], 'renderPipeline': facts['renderPipeline'],
            'excludes': sorted(excludes), 'rungs': rungs, 'integrity': verify, 'lenses': rows}


def markdown(result):
    out = [f'### Lens detection: {result["project"]}', '',
           f'- Engine: {result["engine"] or "unknown"}; render pipeline: {result["renderPipeline"] or "not reported"}',
           f'- Excluded folders (raw counts include them): {", ".join(result["excludes"]) or "none"}']
    out += [f'- {rung}' for rung in result['rungs']]
    out += ['', '| Lens | Raw | First-party | Label | Why | Evidence (first-party/raw) | Representative paths |',
            '|---|---:|---:|---|---|---|---|']
    for row in result['lenses']:
        cell = lambda items: '<br>'.join(f'`{i}`' if '/' in i else i for i in items) or '—'
        out.append(f'| {row["lens"]} | {"" if row["raw"] is None else row["raw"]} | '
                   f'{"" if row["firstParty"] is None else row["firstParty"]} | **{row["label"]}** | {row["reason"]} | '
                   f'{"<br>".join(row["evidence"]) or "—"} | {cell(row["paths"])} |')
    return '\n'.join(out)


# --------------------------------------------------------------------------------------------
# Self-test: a synthetic project, no Unity CLI
# --------------------------------------------------------------------------------------------

class DetectorSelfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        files = {
            'AGENTS.md': '- Gameplay uses the predefined runtime and Editor assemblies, without asmdefs.\n',
            'Packages/manifest.json': json.dumps({'dependencies': {
                'com.unity.test-framework': '1.9.0', 'com.unity.inputsystem': '1.0.0', 'com.unity.ugui': '2.0.0'}}),
            'Assets/Game/Scripts/Picker.cs': 'class Picker : MonoBehaviour { void Update() { var r = cam.ScreenPointToRay(p); Physics.Raycast(r, out h); } }',
            'Assets/Game/Scripts/Menu.cs': 'using UnityEngine.UIElements; class Menu : MonoBehaviour { UIDocument d; }',
            'Assets/Game/Scripts/Tools/Probe.cs': '// probe\n#if UNITY_EDITOR\nclass Probe { void A() { Physics.Linecast(a, b); } }\n#endif',
            'Assets/Game/UI/Main.uxml': '<ui:UXML/>',
            'Assets/Game/Prefabs/Crate.prefab': '--- !u!1 &1\n--- !u!54 &2\n--- !u!65 &3\n',
            'Assets/ThirdParty/Pack/Ball.prefab': '--- !u!54 &1\n--- !u!223 &2\n',
            'Assets/ThirdParty/Pack/Ball.cs': 'using UnityEngine.UI; class Ball : MonoBehaviour { void OnCollisionEnter(Collision c) {} }',
            'Assets/Editor/Tool.cs': 'using UnityEngine.EventSystems; class Tool { [MenuItem("A/B")] static void Run() {} }',
            'Assets/Editor/Tests/ToolTests.cs': 'class ToolTests { [Test] public void Works() {} }',
            'Assets/Tools/LightingCLI/Editor/Lighting.asmdef': '{}',
        }
        for rel, text in files.items():
            path = cls.tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        cls.result = detect(cls.tmp, use_cli=False, optional=['Rendering=lighting is out of scope'])
        cls.rows = {r['lens']: r for r in cls.result['lenses']}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def label(self, lens):
        return self.rows[lens]['label']

    def test_vendor_excluded_but_counted_raw(self):
        physics = self.rows['Physics']
        self.assertGreater(physics['raw'], physics['firstParty'])
        self.assertEqual(NOT_DETECTED, self.label('uGUI'))  # Canvas and UnityEngine.UI only in vendor

    def test_pointer_picking_and_tooling_queries_are_weak(self):
        self.assertEqual(OPTIONAL, self.label('Physics'))
        self.assertIn('pointer picking', self.rows['Physics']['reason'])

    def test_runtime_signals_recommended(self):
        for lens in ('Performance', 'Scenes', 'UI Toolkit', 'Editor tooling', 'Testing'):
            self.assertEqual(RECOMMENDED, self.label(lens), lens)

    def test_package_alone_is_weak(self):
        self.assertEqual(OPTIONAL, self.label('Input'))

    def test_documented_policies(self):
        self.assertEqual(OPTIONAL, self.label('Assemblies'))
        self.assertIn('AGENTS.md:1', self.rows['Assemblies']['reason'])
        self.assertEqual(NOT_DETECTED, self.label('Rendering'))  # a decision never invents a signal

    def test_absent_asmdefs_are_not_a_signal(self):
        self.assertFalse(ASMDEF_POLICY.search('Each feature has its own asmdef.'))
        self.assertTrue(ASMDEF_POLICY.search('Code uses the predefined assemblies.'))

    def test_markdown_and_json(self):
        text = markdown(self.result)
        self.assertIn('| Physics |', text)
        json.dumps(self.result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project', nargs='?')
    parser.add_argument('--format', choices=('markdown', 'json'), default='markdown')
    parser.add_argument('--json-out', help='also write the JSON result to this file')
    parser.add_argument('--exclude', action='append', default=[], help='extra folder name to treat as vendor/generated')
    parser.add_argument('--no-default-excludes', action='store_true')
    parser.add_argument('--optional', action='append', default=[], metavar='LENS=REASON',
                        help='a documented project decision that limits a detected lens to Optional')
    parser.add_argument('--policy-doc', action='append', default=[], help='extra document to scan for policies')
    parser.add_argument('--no-cli', action='store_true', help='skip the Unity CLI rungs')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(argv)
    if args.self_test or not args.project:
        result = unittest.TextTestRunner(stream=sys.stdout).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(DetectorSelfTests))
        return 0 if result.wasSuccessful() else 1
    excludes = ([] if args.no_default_excludes else DEFAULT_EXCLUDES) + args.exclude
    result = detect(args.project, excludes, args.optional, args.policy_doc, not args.no_cli)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2) if args.format == 'json' else markdown(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
