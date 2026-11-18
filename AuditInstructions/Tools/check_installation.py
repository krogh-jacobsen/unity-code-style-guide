"""Stage the documented reference layout in a temporary project and validate local links.

This is a repository cross-folder check, not an installer. It never writes to a user project.
With `--target <project>` it instead checks a real installation read-only: root AGENTS.md and
CLAUDE.md links and anchors, the root .editorconfig, and the reference snapshot.
"""
import argparse
import fnmatch
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'AuditInstructions/SetupInstructions/installation.json'
# Files the installation places at the project root; rebasing leaves links to them unchanged.
ROOT_FILES = ('AGENTS.md', 'CLAUDE.md', '.editorconfig', '.gitignore', 'Documentation/UnityStarterKit-installation.json')


def local_links(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    return [raw.strip().strip('<>') for raw in re.findall(r'\[[^]]*\]\(([^)]+)\)', text)
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', raw.strip())]


def anchors(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    counts, found = {}, set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', text, re.M):
        heading = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', heading)
        base = re.sub(r'[^\w\-\s]', '', heading.lower()).replace(' ', '-')
        number = counts.get(base, 0)
        found.add(base if not number else f'{base}-{number}')
        counts[base] = number + 1
    return found


def upstream_only(path, snapshot, excluded):
    """True when a staged link target was excluded from the snapshot but exists in this repository."""
    if snapshot is None or not path.is_relative_to(snapshot):
        return False
    relative = path.relative_to(snapshot).as_posix()
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in excluded) and (ROOT / relative).is_file()


def validate_links(project, pages=None, snapshot=None, excluded=()):
    errors = []
    for page in pages if pages is not None else project.rglob('*.md'):
        for target in local_links(page.read_text()):
            filename, _, anchor = unquote(target).partition('#')
            destination = (page.parent / filename).resolve() if filename else page
            if not destination.is_relative_to(project):
                errors.append(f'{page.relative_to(project)}: escapes staged project: {target}')
                continue
            if not destination.exists():
                if upstream_only(destination, snapshot, excluded):
                    continue
                errors.append(f'{page.relative_to(project)}: missing link {target}')
                continue
            current = project
            for part in destination.relative_to(project).parts:
                if part not in {entry.name for entry in current.iterdir()}:
                    errors.append(f'{page.relative_to(project)}: case mismatch {target}')
                    break
                current /= part
            if anchor and destination.is_file() and destination.suffix == '.md':
                if anchor not in anchors(destination.read_text()):
                    errors.append(f'{page.relative_to(project)}: missing anchor {target}')
    return errors


def target_agents(source, prefix):
    # Model the documented merge for a fresh target. Existing projects still require a real merge.
    rules = source.split('## This project', 1)[1].split('\n## Maintaining this repository', 1)[0]
    text = ('# AGENTS.md — Unity starter conventions\n\n'
            'Adapt [the stack profile](AgentsInstructions/UnityTechStack/UnityTechStack.md) to this project.\n\n'
            '## This project' + rules)
    return re.sub(r'\[([^]]+)\]\(([^)]+)\)',
                  lambda match: match.group(0) if match[2].startswith(('#', prefix + '/')) or
                  match[2].split('#', 1)[0] in ROOT_FILES or
                  re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', match[2]) else
                  f'[{match[1]}]({prefix}/{match[2]})', text)


def check_target(project, prefix):
    """Read-only checks of an installed project; returns (errors, notes)."""
    project = project.resolve()
    errors, notes = [], []
    record = project / 'Documentation/UnityStarterKit-installation.json'
    if record.is_file():
        try:
            prefix = json.loads(record.read_text()).get('snapshot_path', prefix)
        except json.JSONDecodeError as error:
            errors.append(f'{record.relative_to(project)}: invalid JSON ({error})')
    else:
        notes.append('no installation record; assuming the default snapshot path')
    pages = [project / name for name in ('AGENTS.md', 'CLAUDE.md') if (project / name).is_file()]
    if not (project / 'AGENTS.md').is_file():
        errors.append('missing root AGENTS.md')
    errors += validate_links(project, pages)
    if not (project / '.editorconfig').is_file():
        errors.append('missing root .editorconfig')
    snapshot = project / prefix
    if not snapshot.is_dir():
        errors.append(f'missing reference snapshot at {prefix}')
    elif not (snapshot / 'AGENTS.md').is_file():
        errors.append(f'reference snapshot at {prefix} has no AGENTS.md')
    return errors, notes


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--target', type=Path, help='check this installed Unity project read-only')
    arguments = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    if arguments.target:
        errors, notes = check_target(arguments.target, manifest['snapshot_destination'])
        for note in notes:
            print(f'NOTE {note}')
        if errors:
            raise SystemExit('\n'.join(f'FAIL {error}' for error in errors))
        print(f'PASS target installation: root instruction links, .editorconfig, snapshot ({arguments.target})')
        return
    with tempfile.TemporaryDirectory(prefix='starter-installation-') as temp:
        project = Path(temp).resolve()
        prefix = manifest['snapshot_destination']
        if Path(prefix).is_absolute() or '..' in Path(prefix).parts or Path(prefix).parts[0] == 'Assets':
            raise SystemExit('Snapshot must stay outside Assets inside the staged project')
        snapshot = project / prefix
        snapshot.mkdir(parents=True)
        excluded = manifest.get('snapshot_exclude', [])
        for name in manifest['snapshot_sources']:
            source = ROOT / name
            if Path(name).is_absolute() or '..' in Path(name).parts or not source.exists():
                raise SystemExit(f'Invalid snapshot source: {name}')
            entries = [source, *source.rglob('*')] if source.is_dir() else [source]
            if any(entry.is_symlink() for entry in entries):
                raise SystemExit(f'Snapshot source contains symlinks: {name}')
            destination = snapshot / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                def ignore(directory, names, source=source, name=name):
                    skipped = set(shutil.ignore_patterns('__pycache__', '*.pyc', 'bin', 'obj')(directory, names))
                    base = Path(name) / Path(directory).relative_to(source)
                    return skipped | {entry for entry in names
                                      if any(fnmatch.fnmatchcase((base / entry).as_posix(), pattern) for pattern in excluded)}
                shutil.copytree(source, destination, ignore=ignore)
            else:
                shutil.copy2(source, destination)
        (project / 'AGENTS.md').write_text(target_agents((ROOT / 'AGENTS.md').read_text(), prefix))
        (project / 'CLAUDE.md').write_text('Read [AGENTS.md](AGENTS.md) for project instructions.\n')
        config = ROOT / manifest['root_editorconfig_source']
        shutil.copy2(config, project / '.editorconfig')
        errors = validate_links(project, snapshot=snapshot, excluded=excluded)
        for pattern in excluded:
            if not list(ROOT.glob(pattern)):
                errors.append(f'snapshot_exclude pattern matches nothing: {pattern}')
            if list(snapshot.glob(pattern)):
                errors.append(f'snapshot_exclude pattern was copied: {pattern}')
        if (project / '.editorconfig').read_bytes() != config.read_bytes():
            errors.append('Root EditorConfig differs from selected source')
        errors += check_target(project, prefix)[0]
        if errors:
            raise SystemExit('\n'.join(errors))

        # Failure-sensitive probes prove that destination checking catches missing sources,
        # incorrect root rebasing, anchors, and case even on case-insensitive filesystems.
        probe = project / 'Probe.md'
        for link in ('[missing](Missing.md)', '[unrebased](AgentsInstructions/README.md)',
                     f'[case]({prefix}/AgentsInstructions/Readme.md)', '[anchor](AGENTS.md#missing-anchor)'):
            probe.write_text(link)
            if not validate_links(project):
                raise SystemExit(f'Installation check failed to reject {link}')
        probe.unlink()
        print('PASS installation: staged snapshot and root routing, local links/anchors/case, EditorConfig; --target self-check; 4 negative probes')


if __name__ == '__main__':
    main()
