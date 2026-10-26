"""Stage the documented reference layout in a temporary project and validate local links.

This is a repository cross-folder check, not an installer. It never writes to a user project.
"""
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'AuditInstructions/SetupInstructions/installation.json'


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


def validate_links(project):
    errors = []
    for page in project.rglob('*.md'):
        for target in local_links(page.read_text()):
            filename, _, anchor = unquote(target).partition('#')
            destination = (page.parent / filename).resolve() if filename else page
            if not destination.is_relative_to(project):
                errors.append(f'{page.relative_to(project)}: escapes staged project: {target}')
                continue
            if not destination.exists():
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
    rules = source.split('## Working rules', 1)[1].split('\n## Maintaining this repository', 1)[0]
    text = ('# AGENTS.md — Unity starter conventions\n\n'
            'Adapt [the stack profile](AgentsInstructions/UnityTechStack/UnityTechStack.md) to this project.\n\n'
            '## Working rules' + rules)
    return re.sub(r'\[([^]]+)\]\(([^)]+)\)',
                  lambda match: match.group(0) if match[2].startswith('#') or
                  re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', match[2]) else
                  f'[{match[1]}]({prefix}/{match[2]})', text)


def main():
    manifest = json.loads(MANIFEST.read_text())
    with tempfile.TemporaryDirectory(prefix='starter-installation-') as temp:
        project = Path(temp).resolve()
        prefix = manifest['snapshot_destination']
        if Path(prefix).is_absolute() or '..' in Path(prefix).parts or Path(prefix).parts[0] == 'Assets':
            raise SystemExit('Snapshot must stay outside Assets inside the staged project')
        snapshot = project / prefix
        snapshot.mkdir(parents=True)
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
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'bin', 'obj'))
            else:
                shutil.copy2(source, destination)
        (project / 'AGENTS.md').write_text(target_agents((ROOT / 'AGENTS.md').read_text(), prefix))
        (project / 'CLAUDE.md').write_text('Read [AGENTS.md](AGENTS.md) for project instructions.\n')
        config = ROOT / manifest['root_editorconfig_source']
        shutil.copy2(config, project / '.editorconfig')
        errors = validate_links(project)
        if (project / '.editorconfig').read_bytes() != config.read_bytes():
            errors.append('Root EditorConfig differs from selected source')
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
        print('PASS installation: staged snapshot and root routing, local links/anchors/case, EditorConfig; 4 negative probes')


if __name__ == '__main__':
    main()
