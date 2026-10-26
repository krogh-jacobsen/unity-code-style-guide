"""Validate rendered checklist structure within this topic folder."""
from pathlib import Path
import re
import sys
import unittest

FOLDER = Path(__file__).resolve().parents[1]


def separator(line):
    cells = line.strip().strip('|').split('|')
    return bool(cells) and all(re.fullmatch(r'\s*:?-{3,}:?\s*', cell) for cell in cells)


def table_errors(text):
    """A blank line ends a GFM table; subsequent rows need a new header/separator."""
    errors, block, fenced = [], [], False

    def finish():
        if block and (len(block) < 2 or not separator(block[1][1])):
            errors.append(f'line {block[0][0]}: table rows lack a header/separator (possibly a blank line inside a checklist)')
        block.clear()

    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r'^\s*(`{3,}|~{3,})', line):
            finish()
            fenced = not fenced
        elif not fenced and line.lstrip().startswith('|'):
            block.append((number, line))
        else:
            finish()
    finish()
    return errors


class TableRegressionTests(unittest.TestCase):
    def test_complete_table(self):
        self.assertEqual([], table_errors('| Check | Evidence |\n|---|---|\n| A | B |\n| C | D |'))

    def test_blank_line_detaches_rows(self):
        self.assertTrue(table_errors('| Check | Evidence |\n|---|---|\n| A | B |\n\n| C | D |'))

    def test_multiple_detached_rows(self):
        self.assertTrue(table_errors('| A | B |\n| C | D |'))

    def test_fenced_example(self):
        self.assertEqual([], table_errors('```markdown\n| incomplete |\n```'))

    def test_separate_valid_tables(self):
        table = '| A | B |\n| :--- | ---: |\n| C | D |'
        self.assertEqual([], table_errors(table + '\n\n' + table))


def main():
    result = unittest.TextTestRunner(stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(TableRegressionTests))
    errors = []
    pages = sorted(FOLDER.rglob('*.md'))
    for page in pages:
        errors.extend(f'{page.relative_to(FOLDER)}: {error}' for error in table_errors(page.read_text()))
    if not result.wasSuccessful() or errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS audit guides: {len(pages)} Markdown files, checklist table structure; {result.testsRun} parser regressions')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
