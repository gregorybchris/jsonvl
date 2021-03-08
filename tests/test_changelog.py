import re
from pathlib import Path

CHANGELOG_FILEPATH = Path(__file__).parent.parent / 'CHANGELOG.rst'


class TestChangelog:
    def test_changelog(self):
        with open(CHANGELOG_FILEPATH, 'r') as f:
            lines = f.readlines()
            assert lines[-1][-1] == '\n'

            n_lines = len(lines)
            for i in range(n_lines):
                line = lines[i]
                if line.startswith('v'):
                    if i != 0:
                        self.check_blank_line(lines[i - 1])
                    self.check_version_line(line)
                    self.check_sep_line(lines[i + 1], len(line))
                elif line.startswith('*'):
                    pass
                elif line.startswith('----'):
                    pass
                elif line == '\n':
                    pass
                else:
                    raise ValueError(f"Invalid CHANGELOG on line {i}: {line}")

    def check_blank_line(self, line):
        assert line == '\n', "Expected blank line"

    def check_sep_line(self, line, length):
        assert re.match(r'^[-]+$', line), "Expected separator line"
        assert len(line) == length, f"Expected separator line to have {length} dashes"

    def check_version_line(self, line):
        assert re.match(r'^v[0-9]+\.[0-9]+\.[0-9]+\n$', line), "Expected valid version line"
